#!/usr/bin/env bash
set -euo pipefail

# gh_pr_open.sh — ouvre une PR avec titre auto-préfixé [journal:HOST-pidPID]
# Usage: gh_pr_open.sh "<résumé court>" [--base <base-branch>] [--model <nom>]
# - Détecte type/issue depuis le nom de branche: <type>/issue-<num>-<slug>
# - Construit le titre: [journal:HOST-pidPID] [model:NOM] <type>: <résumé> (Refs #<num>)

SUMMARY=${1:-}
BASE_BRANCH="master"
MODEL_TAG=${MODEL_TAG:-}

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_BRANCH=${2:-master}; shift 2;;
    --model)
      MODEL_TAG=${2:-}; shift 2;;
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
PREFIX="[journal:${HOST_SHORT}-pid${PID_HINT}]"
MODEL_PREFIX=""
if [[ -n "$MODEL_TAG" ]]; then
  MODEL_PREFIX=" [model:${MODEL_TAG}]"
fi

TITLE="${PREFIX}${MODEL_PREFIX} ${TYPE}: ${SUMMARY}"
if [[ -n "$ISSUE_NUM" ]]; then
  TITLE+=" (Refs #${ISSUE_NUM})"
fi

BODY="PR ouverte via gh_pr_open.sh.\n\n- Branche: ${CURR_BRANCH}\n- Agent/Session: ${PREFIX}\n- Modèle: ${MODEL_TAG:-n/a}\n\nCloses #${ISSUE_NUM}"

exec gh pr create --title "$TITLE" --body "$BODY" --base "$BASE_BRANCH" --head "$CURR_BRANCH"
