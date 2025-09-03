#!/usr/bin/env bash
set -euo pipefail

# Audit des sous-modules PaniniFS: statut, dernier commit, URL distante, existence GitHub (si gh dispo)
# Usage: scripts/devops/audit_submodules.sh

ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "${ROOT_DIR:-}" ]; then
  echo "Erreur: exécuter dans un repository git." >&2
  exit 1
fi

echo "Repo: $ROOT_DIR"
echo "== Submodule status =="
git submodule status || true

echo
echo "== Détails par sous-module =="
while IFS= read -r path; do
  [ -z "$path" ] && continue
  [ ! -d "$path/.git" ] && { echo "- $path: pas initialisé (git submodule update --init)"; continue; }
  echo "- $path"
  ( 
    cd "$path"
    URL=$(git remote get-url origin 2>/dev/null || echo "(no remote)")
    LAST=$(git log -1 --pretty=format:'%ci %h %s' 2>/dev/null || echo "(no commits)")
    echo "  remote: $URL"
    echo "  last:   $LAST"
  )
done < <(git config --file .gitmodules --get-regexp submodule\\..*\\.path | awk '{print $2}')

if command -v gh >/dev/null 2>&1; then
  echo
  echo "== Existence des dépôts GitHub (gh) =="
  while IFS= read -r url; do
    name=$(basename "$url" .git)
    owner=$(echo "$url" | sed -E 's#.*github.com[:/ ]([^/]+)/.*#\1#')
    repo=$(echo "$url" | sed -E 's#.*github.com[:/ ][^/]+/([^/.]+).*#\1#')
    [ -z "$owner" ] || [ -z "$repo" ] && continue
    echo "- $owner/$repo"
    gh repo view "$owner/$repo" --json name,visibility,defaultBranchRef,updatedAt,description \
      -q '{name,visibility,defaultBranch: .defaultBranchRef.name,updatedAt,description}' || echo "  inaccessible (privé/supprimé?)"
  done < <(git config --file .gitmodules --get-regexp submodule\\..*\\.url | awk '{print $2}')
else
  echo
  echo "(Astuce) Installe gh pour vérifier l’existence distante: https://cli.github.com/"
fi

echo
echo "== Recommandations =="
echo "- Initialiser les sous-modules manquants: git submodule sync --recursive && git submodule update --init --recursive"
echo "- Archiver/supprimer les sous-modules sans commits récents (>180j) et non référencés dans la CI/docs"
echo "- Aligner les branches par défaut (main/master) et mettre à jour .gitmodules si besoin"
