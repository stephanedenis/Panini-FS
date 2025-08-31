#!/usr/bin/env bash
set -euo pipefail

# fix_remotes.sh — Bascule l'URL des remotes Git entre HTTPS et SSH.
#
# Usage:
#   ./fix_remotes.sh ssh   [remote] [--all|--submodules]
#   ./fix_remotes.sh https [remote] [--all|--submodules]
#   ./fix_remotes.sh                 # affiche l'état actuel du remote par défaut (origin)
#
# Options:
#   --all         Applique au dépôt courant ET à tous les sous-modules (récursif)
#   --submodules  Applique uniquement aux sous-modules (récursif)
#   -h|--help     Affiche cette aide
#
# Notes:
# - Le remote par défaut est "origin" si non précisé.
# - Idempotent: ne change rien si déjà au bon format.

mode=""
remote="origin"
apply_current_repo=true
apply_submodules=false

print_help() {
	sed -n '1,200p' "$0" | sed -n '1,30p' | sed 's/^# //;t;d'
}

# Parse des arguments
if [[ $# -gt 0 ]]; then
	case "${1:-}" in
		ssh|https)
			mode="$1"; shift ;;
		-h|--help)
			print_help; exit 0 ;;
	esac
fi

if [[ $# -gt 0 ]]; then
	case "${1:-}" in
		--all)
			apply_submodules=true
			apply_current_repo=true
			shift ;;
		--submodules)
			apply_submodules=true
			apply_current_repo=false
			shift ;;
		-h|--help)
			print_help; exit 0 ;;
		*)
			remote="$1"; shift ;;
	esac
fi

while [[ $# -gt 0 ]]; do
	case "$1" in
		--all)
			apply_submodules=true
			apply_current_repo=true
			shift ;;
		--submodules)
			apply_submodules=true
			apply_current_repo=false
			shift ;;
		-h|--help)
			print_help; exit 0 ;;
		*)
			echo "Argument inconnu: $1" >&2; exit 3 ;;
	esac
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
	echo "Erreur: ce dossier n'est pas un dépôt git" >&2
	exit 1
fi

to_ssh() {
	# https://github.com/owner/repo(.git) -> git@github.com:owner/repo.git
	local url="$1"
	if [[ "$url" =~ ^https://github.com/([^/]+)/([^/]+?)(\.git)?$ ]]; then
		local owner="${BASH_REMATCH[1]}"
		local name="${BASH_REMATCH[2]}"
		# Retire un éventuel suffixe .git puis le rajoute proprement
		name="${name%.git}"
		echo "git@github.com:${owner}/${name}.git"
	elif [[ "$url" =~ ^ssh://git@github.com/([^/]+)/([^/]+?)(\.git)?$ ]]; then
		# Déjà SSH style; normaliser en git@github.com:owner/repo.git
		local owner="${BASH_REMATCH[1]}"
		local name="${BASH_REMATCH[2]}"
		name="${name%.git}"
		echo "git@github.com:${owner}/${name}.git"
	else
		echo "$url"
	fi
}

to_https() {
	# git@github.com:owner/repo(.git) or ssh://git@github.com/owner/repo(.git) -> https://github.com/owner/repo.git
	local url="$1"
	if [[ "$url" =~ ^git@github.com:([^/]+)/([^/]+?)(\.git)?$ ]]; then
		local owner="${BASH_REMATCH[1]}"
		local name="${BASH_REMATCH[2]}"
		name="${name%.git}"
		echo "https://github.com/${owner}/${name}.git"
	elif [[ "$url" =~ ^ssh://git@github.com/([^/]+)/([^/]+?)(\.git)?$ ]]; then
		local owner="${BASH_REMATCH[1]}"
		local name="${BASH_REMATCH[2]}"
		name="${name%.git}"
		echo "https://github.com/${owner}/${name}.git"
	else
		echo "$url"
	fi
}

apply_repo() {
	local mode_="$1" remote_="$2"
	local current_url_ new_url
	current_url_=$(git remote get-url "$remote_" 2>/dev/null || true)
	if [[ -z "${current_url_:-}" ]]; then
		echo "Remote '$remote_' introuvable dans $(pwd). Remotes disponibles :" >&2
		git remote -v || true
		return 2
	fi
	case "$mode_" in
		ssh)
			new_url=$(to_ssh "$current_url_")
			if [[ "$new_url" == "$current_url_" ]]; then
				echo "Déjà en SSH (ou format non reconnu): $current_url_"
			else
				echo "Mise à jour: '$remote_' -> $new_url"
				git remote set-url "$remote_" "$new_url"
			fi
			;;
		https)
			new_url=$(to_https "$current_url_")
			if [[ "$new_url" == "$current_url_" ]]; then
				echo "Déjà en HTTPS (ou format non reconnu): $current_url_"
			else
				echo "Mise à jour: '$remote_' -> $new_url"
				git remote set-url "$remote_" "$new_url"
				# Nettoyage de réécritures éventuelles
				git config --global --unset url.ssh://git@github.com/.insteadof 2>/dev/null || true
				git config --global --unset "url.ssh://git@github.com/".insteadof 2>/dev/null || true
				git config --global --unset url.git@github.com:.insteadof 2>/dev/null || true
			fi
			;;
		"")
			echo "Remote actuel ($remote_): $current_url_"
			;;
		*)
			echo "Usage: $0 [ssh|https] [remote] [--all|--submodules]" >&2
			return 3
			;;
	esac
	echo
	echo "Remotes de $(pwd):"
	git remote -v || true
}

apply_submodules_recursively() {
	# Liste les sous-modules depuis .gitmodules si disponible, sinon via git submodule
	if [[ -f .gitmodules ]]; then
		# shellcheck disable=SC2016
		awk -F'=' '/path[[:space:]]*=/{gsub(/[[:space:]]*/,"",$2); print $2}' .gitmodules | while read -r sm_path; do
			if [[ -d "$sm_path" ]]; then
				echo
				echo "== Sous-module: $sm_path =="
				(
					cd "$sm_path"
					if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
						apply_repo "$mode" "$remote" || true
						# Recursion sur sous-sous-modules
						if [[ -f .gitmodules ]]; then
							apply_submodules_recursively || true
						fi
					else
						echo "Avertissement: $sm_path n'est pas un dépôt Git initialisé."
					fi
				)
			fi
		done
	else
		# Fallback: git submodule foreach
		git submodule foreach --recursive "echo; echo '== Sous-module: $name =='; \"$toplevel/fix_remotes.sh\" ${mode:+$mode} ${remote:+$remote} || true"
	fi
}

# Exécution
if [[ "$apply_current_repo" == true ]]; then
	apply_repo "$mode" "$remote" || true
fi

if [[ "$apply_submodules" == true ]]; then
	apply_submodules_recursively || true
fi

exit 0

