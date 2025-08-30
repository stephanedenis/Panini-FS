#!/usr/bin/env bash
set -euo pipefail

# gh_pr_open.sh — ouvre une PR avec titre auto-préfixé [journal:HOST-pidPID]
# Usage: gh_pr_open.sh "<résumé court>" [--base <base-branch>]
# - Détecte type/issue depuis le nom de branche: <type>/issue-<num>-<slug>
# - Construit le titre: [journal:HOST-pidPID] <type>: <résumé> (Refs #<num>)

SUMMARY=${1:-}
BASE_BRANCH="master"

if [[ -z "${SUMMARY}" ]]; then
  echo "Usage: $0 \"<résumé court>\" [--base <base-branch>]" >&2
  exit 2
fi

if [[ ${2:-} == "--base" ]]; then
  BASE_BRANCH=${3:-master}
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

TITLE="${PREFIX} ${TYPE}: ${SUMMARY}"
if [[ -n "$ISSUE_NUM" ]]; then
  TITLE+=" (Refs #${ISSUE_NUM})"
fi

BODY="PR ouverte via gh_pr_open.sh.\n\n- Branche: ${CURR_BRANCH}\n- Agent/Session: ${PREFIX}\n\nCloses #${ISSUE_NUM}"

# Crée la PR; laisse le template côté repo compléter si besoin
exec gh pr create --title "$TITLE" --body "$BODY" --base "$BASE_BRANCH" --head "$CURR_BRANCH"
