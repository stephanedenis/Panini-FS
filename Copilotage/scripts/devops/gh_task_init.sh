#!/usr/bin/env bash
set -euo pipefail

# gh_task_init.sh — ouvre (ou réutilise) une issue et crée une branche dédiée
# Usage: gh_task_init.sh "[feat] Implémenter X" docs|feat|fix|chore|ci|refactor|test "slug-kebab"

TITLE=${1:-}
TYPE=${2:-docs}
SLUG=${3:-}

if [[ -z "$TITLE" || -z "$SLUG" ]]; then
  echo "Usage: $0 \"[feat] Mon titre\" <type> <slug>" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI requis" >&2
  exit 3
fi

# Outils facultatifs
HAS_JQ=1
if ! command -v jq >/dev/null 2>&1; then HAS_JQ=0; fi

# Cherche une issue ouverte de même titre (si jq disponible)
ISSUE_NUM=""
if [[ "$HAS_JQ" -eq 1 ]]; then
  ISSUE_NUM=$(gh issue list --search "$TITLE" --state open --json number,title 2>/dev/null \
    | jq -r --arg T "$TITLE" '.[] | select(.title==$T) | .number' || true)
fi
if [[ -z "$ISSUE_NUM" ]]; then
  ISSUE_URL=$(gh issue create --title "$TITLE" --body "Créée via gh_task_init.sh" || true)
  ISSUE_NUM=${ISSUE_URL##*/}
fi

BRANCH="${TYPE}/issue-${ISSUE_NUM}-${SLUG}"
if git show-ref --verify --quiet refs/heads/$BRANCH; then
  git checkout $BRANCH
else
  git checkout -b $BRANCH
fi

git push -u origin HEAD || true

# Astuce PR: utilisez Copilotage/scripts/devops/gh_pr_open.sh pour ajouter automatiquement le label provenance
echo "Astuce PR: utilisez Copilotage/scripts/devops/gh_pr_open.sh \"<résumé>\" [--model <nom>] [--owner human|agent]" >&2

echo "Issue #$ISSUE_NUM" >&2
echo "Branche: $BRANCH" >&2
