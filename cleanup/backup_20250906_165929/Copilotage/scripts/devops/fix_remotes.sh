#!/usr/bin/env bash
set -euo pipefail

# fix_remotes.sh — Bascule et normalise l'URL du remote (HTTPS <-> SSH)
# Usage:
#   ./fix_remotes.sh ssh   [remote]
#   ./fix_remotes.sh https [remote]
# Sans argument: affiche l'état actuel et une suggestion.

mode="${1:-}"
remote="${2:-origin}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erreur: ce dossier n'est pas un dépôt git" >&2
  exit 1
fi

current_url=$(git remote get-url "$remote" 2>/dev/null || true)
if [[ -z "${current_url:-}" ]]; then
  echo "Remote '$remote' introuvable. Remotes disponibles :" >&2
  git remote -v
  exit 2
fi

normalize_https() {
  local url="$1"
  local prefix="https://github.com/"
  if [[ "$url" == ${prefix}* ]]; then
    local rest="${url#${prefix}}" # owner/repo(.git...)
    local owner="${rest%%/*}"
    local name="${rest#*/}"
    # Retire tous les suffixes .git répétés
    while [[ "$name" == *.git ]]; do name="${name%.git}"; done
    echo "${prefix}${owner}/${name}.git"
  else
    echo "$url"
  fi
}

to_ssh() {
  local url="$1"
  # Si déjà en SSH, normaliser pour un seul .git
  if [[ "$url" =~ ^git@github.com:([^/]+)/([^/]+)$ ]]; then
    local owner="${BASH_REMATCH[1]}"
    local name="${BASH_REMATCH[2]}"
    while [[ "$name" == *.git ]]; do name="${name%.git}"; done
    echo "git@github.com:${owner}/${name}.git"
    return 0
  fi
  # HTTPS -> SSH
  local https_norm
  https_norm=$(normalize_https "$url")
  if [[ "$https_norm" =~ ^https://github.com/([^/]+)/([^/]+)\.git$ ]]; then
    local owner="${BASH_REMATCH[1]}"
    local name="${BASH_REMATCH[2]}"
    echo "git@github.com:${owner}/${name}.git"
  else
    echo "$url"
  fi
}

to_https() {
  local url="$1"
  # SSH -> HTTPS
  if [[ "$url" =~ ^git@github.com:([^/]+)/([^/]+)$ ]]; then
    local owner="${BASH_REMATCH[1]}"
    local name="${BASH_REMATCH[2]}"
    while [[ "$name" == *.git ]]; do name="${name%.git}"; done
    echo "https://github.com/${owner}/${name}.git"
    return 0
  fi
  # Déjà HTTPS: normaliser (retire .git répétés et ajoute un seul .git)
  echo "$(normalize_https "$url")"
}

case "${mode}" in
  ssh)
    new_url=$(to_ssh "$current_url")
    ;;
  https)
    new_url=$(to_https "$current_url")
    ;;
  "")
    echo "Remote actuel ($remote): $current_url"
    echo "Astuce: ./fix_remotes.sh ssh | ./fix_remotes.sh https"
    exit 0
    ;;
  *)
    echo "Usage: $0 [ssh|https] [remote]" >&2
    exit 3
    ;;
esac

if [[ "$new_url" != "$current_url" ]]; then
  echo "Mise à jour du remote '$remote' -> $new_url"
  git remote set-url "$remote" "$new_url"
else
  echo "Remote déjà normalisé: $current_url"
fi

echo
echo "Remotes:"
git remote -v
