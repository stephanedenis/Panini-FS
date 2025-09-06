#!/usr/bin/env bash
set -euo pipefail

# run_safe.sh — exécute une commande en neutralisant les éditeurs/pagers interactifs
# Usage: Copilotage/scripts/devops/run_safe.sh <commande> [args...]

export GIT_PAGER=cat
export PAGER=cat
export LESS=FRX
export GH_PAGER=cat
export EDITOR=true
export VISUAL=true
export GIT_EDITOR=true
export GH_EDITOR=true
# Empêcher les merges d’ouvrir un éditeur si on passe --no-edit
export GIT_MERGE_AUTOEDIT=no

exec "$@"
