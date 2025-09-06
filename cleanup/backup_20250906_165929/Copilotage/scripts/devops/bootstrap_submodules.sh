#!/usr/bin/env bash
set -euo pipefail

# bootstrap_submodules.sh — Ajoute/initialise les submodules cibles s'ils n'existent pas.
declare -A MODULES=(
  [modules/ultra-reactive]="git@github.com:stephanedenis/PaniniFS-UltraReactive.git"
  [modules/colab-controller]="git@github.com:stephanedenis/PaniniFS-CoLabController.git"
  [modules/autonomous-missions]="git@github.com:stephanedenis/PaniniFS-AutonomousMissions.git"
  [modules/semantic-core]="git@github.com:stephanedenis/PaniniFS-SemanticCore.git"
  [modules/publication-engine]="git@github.com:stephanedenis/PaniniFS-PublicationEngine.git"
  [modules/cloud-orchestrator]="git@github.com:stephanedenis/PaniniFS-CloudOrchestrator.git"
)

mkdir -p modules

for path in "${!MODULES[@]}"; do
  url="${MODULES[$path]}"
  # Vérifie l'accès au dépôt distant (évite d'écrire si inexistant)
  if git ls-remote -h "$url" >/dev/null 2>&1; then
    if [ ! -d "$path/.git" ]; then
      echo "Ajout submodule: $path -> $url"
      git submodule add "$url" "$path" || true
    else
      echo "Submodule déjà initialisé: $path"
    fi
  else
    echo "SKIP: $path (repo inaccessible ou inexistant: $url)"
  fi
done

if [ -f .gitmodules ]; then
  echo "Sync et init submodules (best-effort)"
  git submodule sync --recursive || true
  git submodule update --init --recursive || true
  git submodule status --recursive || true
else
  echo "Aucun submodule configuré (.gitmodules absent)"
fi
