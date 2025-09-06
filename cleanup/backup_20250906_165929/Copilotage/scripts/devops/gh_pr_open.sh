#!/usr/bin/env bash
set -euo pipefail

# gh_pr_open.sh — ouvre une PR et ajoute des labels de provenance courts
# Usage: gh_pr_open.sh "<résumé court>" [--base <base-branch>] [--model <nom>] [--owner <human|agent>]
# - Détecte type/issue depuis le nom de branche: <type>/issue-<num>-<slug>
# - Construit le titre: <type>: <résumé> (Refs #<num>)
# - Ajoute les labels: prov:host=..., prov:pid=..., agent:GitHubCopilot, model=..., owner=...

SUMMARY=${1:-}
BASE_BRANCH="master"
AGENT_TAG=${AGENT_TAG:-GitHubCopilot}
MODEL_TAG=${MODEL_TAG:-}
OWNER_TAG=${OWNER_TAG:-agent}

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_BRANCH=${2:-master}; shift 2;;
    --agent)
      AGENT_TAG=${2:-}; shift 2;;
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

TITLE="${TYPE}: ${SUMMARY}"
if [[ -n "$ISSUE_NUM" ]]; then
  TITLE+=" (Refs #${ISSUE_NUM})"
fi

BODY="PR ouverte via gh_pr_open.sh.\n\n- Branche: ${CURR_BRANCH}\n- Modèle: ${MODEL_TAG:-n/a}\n\nCloses #${ISSUE_NUM}"

# Crée la PR
gh pr create --title "$TITLE" --body "$BODY" --base "$BASE_BRANCH" --head "$CURR_BRANCH"

# Ajoute des labels provenance courts (<=50 chars chacun)
HOST_RAW=${HOSTNAME:-$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "host")}
# Normalise: minuscules, retire espaces, garde alnum.-_
HOST_NORM=$(echo "$HOST_RAW" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9._-' | cut -c1-24)
[ -z "$HOST_NORM" ] && HOST_NORM="host"
PID_HINT=$$

LBL_HOST="prov:host=${HOST_NORM}"
LBL_PID="prov:pid=${PID_HINT}"
LBL_AGENT="agent:${AGENT_TAG}"
LBL_MODEL="model:${MODEL_TAG:-unspecified}"
LBL_OWNER="owner:${OWNER_TAG}"

# Opt-in par défaut: autofill provenance et auto-merge
LBL_AUTOFILL="autofill-provenance"
LBL_AUTOMERGE="automerge-provenance"

# S'assure que les labels existent (couleur par défaut)
for L in "$LBL_HOST" "$LBL_PID" "$LBL_AGENT" "$LBL_MODEL" "$LBL_OWNER" "$LBL_AUTOFILL" "$LBL_AUTOMERGE"; do
  gh label create "$L" --color BFD4F2 --description "Provenance/agent metadata" || true
done

PR_NUMBER=$(gh pr view --json number --jq .number)
exec gh pr edit "$PR_NUMBER" \
  --add-label "$LBL_HOST" \
  --add-label "$LBL_PID" \
  --add-label "$LBL_AGENT" \
  --add-label "$LBL_MODEL" \
  --add-label "$LBL_OWNER" \
  --add-label "$LBL_AUTOFILL" \
  --add-label "$LBL_AUTOMERGE"
