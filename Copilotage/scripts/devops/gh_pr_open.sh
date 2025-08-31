#!/usr/bin/env bash
set -euo pipefail

# gh_pr_open.sh — ouvre une PR et ajoute un label provenance parsable
# Usage: gh_pr_open.sh "<résumé court>" [--base <base-branch>] [--model <nom>] [--owner <human|agent>]
# - Détecte type/issue depuis le nom de branche: <type>/issue-<num>-<slug>
# - Construit le titre: <type>: <résumé> (Refs #<num>)
# - Ajoute le label: provenance:host=HOST,pid=PID,agent=GitHubCopilot,model=MODELE,owner=OWNER

SUMMARY=${1:-}
BASE_BRANCH="master"
MODEL_TAG=${MODEL_TAG:-}
OWNER_TAG=${OWNER_TAG:-agent}

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_BRANCH=${2:-master}; shift 2;;
    --model)
      MODEL_TAG=${2:-}; shift 2;;
    --owner)
      OWNER_TAG=${2:-agent}; shift 2;;
    *)
      shift;;
  esac
done

if [[ -z "${SUMMARY}" ]]; then
  echo "Usage: $0 \"<résumé court>\" [--base <base-branch>] [--model <nom>]" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI requis" >&2
  exit 3
fi

CURR_BRANCH=$(git rev-parse --abbrev-ref HEAD)
TYPE="docs"
ISSUE_NUM=""
if [[ "$CURR_BRANCH" =~ ^([^/]+)/issue-([0-9]+)-(.+)$ ]]; then
  TYPE="${BASH_REMATCH[1]}"
  ISSUE_NUM="${BASH_REMATCH[2]}"
fi

HOST_SHORT=${HOSTNAME:-$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "host")}
PID_HINT=$$
TITLE="${TYPE}: ${SUMMARY}"
if [[ -n "$ISSUE_NUM" ]]; then
  TITLE+=" (Refs #${ISSUE_NUM})"
fi

BODY="PR ouverte via gh_pr_open.sh.\n\n- Branche: ${CURR_BRANCH}\n- Modèle: ${MODEL_TAG:-n/a}\n\nCloses #${ISSUE_NUM}"

# Crée la PR
gh pr create --title "$TITLE" --body "$BODY" --base "$BASE_BRANCH" --head "$CURR_BRANCH"

# Ajoute le label provenance parsable
HOST_SHORT=${HOSTNAME:-$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "host")}
PID_HINT=$$
PROVENANCE_LABEL="provenance:host=${HOST_SHORT},pid=${PID_HINT},agent=GitHubCopilot,model=${MODEL_TAG:-unspecified},owner=${OWNER_TAG}"
gh label list --limit 200 | grep -Fq "$PROVENANCE_LABEL" || gh label create "$PROVENANCE_LABEL" --color FFFFFF --description "Agent provenance metadata" || true
PR_NUMBER=$(gh pr view --json number --jq .number)
exec gh pr edit "$PR_NUMBER" --add-label "$PROVENANCE_LABEL"
