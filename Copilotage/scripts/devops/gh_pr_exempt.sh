#!/usr/bin/env bash
set -euo pipefail

# gh_pr_exempt.sh — applique/retire le label de bypass `copilotage-exempt` sur une PR
# Usage: gh_pr_exempt.sh <pr-number> [--remove]

PR=${1:-}
ACTION="add"
if [[ ${2:-} == "--remove" ]]; then ACTION="remove"; fi

if [[ -z "$PR" ]]; then
  echo "Usage: $0 <pr-number> [--remove]" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI requis" >&2
  exit 3
fi

if [[ "$ACTION" == "add" ]]; then
  exec gh pr edit "$PR" --add-label copilotage-exempt
else
  exec gh pr edit "$PR" --remove-label copilotage-exempt || true
fi
