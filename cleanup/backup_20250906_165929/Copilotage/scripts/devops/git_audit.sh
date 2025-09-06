#!/usr/bin/env bash
set -euo pipefail

# git_audit.sh — Audit rapide d'un dépôt Git

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erreur: ce dossier n'est pas un dépôt git" >&2
  exit 1
fi

printf "== REMOTES ==\n"
git --no-pager remote -v || true

echo
printf "== BRANCH STATUS ==\n"
git --no-pager status -sb || true

echo
printf "== FETCH (best-effort) ==\n"
if ! git fetch --all --prune 2>/dev/null; then
  echo "(fetch ignoré: hors-ligne ?)"
fi

echo
printf "== SUBMODULES ==\n"
if [ -f .gitmodules ]; then
  git submodule sync --recursive || true
  git submodule status --recursive || true
else
  echo "Aucun .gitmodules"
fi

echo
printf "== LAST COMMIT ==\n"
git --no-pager log -1 --oneline --decorate --graph || true