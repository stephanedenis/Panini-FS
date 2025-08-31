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

HOST_SHORT=${HOSTNAME:-$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "host")}
PID_HINT=$$
<<<<<<< HEAD
SANITIZE() { printf '%s' "$1" | sed 's/[\[\]\n\r]/_/g; s/[[:space:]]\+/_/g'; }
AGENT_SAFE=$(SANITIZE "${AGENT_TAG:-copilot}")
MODEL_SAFE=$(SANITIZE "${MODEL_TAG:-unknown}")
PREFIX="[${HOST_SHORT}-${PID_HINT}-${AGENT_SAFE}-${MODEL_SAFE}]"

TITLE="${PREFIX} ${TYPE}: ${SUMMARY}"
=======
TITLE="${TYPE}: ${SUMMARY}"
>>>>>>> ffd6a72 (CI/Governance: migrate PR metadata from journal: to provenance:, update workflows, scripts, and templates)
if [[ -n "$ISSUE_NUM" ]]; then
  TITLE+=" (Refs #${ISSUE_NUM})"
fi

BODY="PR ouverte via gh_pr_open.sh.\n\n- Branche: ${CURR_BRANCH}\n- Modèle: ${MODEL_TAG:-n/a}\n\nCloses #${ISSUE_NUM}"

# Crée la PR
gh pr create --title "$TITLE" --body "$BODY" --base "$BASE_BRANCH" --head "$CURR_BRANCH"

# Ajoute les labels de provenance courts
HOST_SHORT=${HOSTNAME:-$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "host")}
PID_HINT=$$
PR_NUMBER=$(gh pr view --json number --jq .number)

add_label() {
  local label="$1"; local desc="$2"; local color="${3:-FFFFFF}"
  gh label list --limit 200 | grep -Fq "$label" || gh label create "$label" --color "$color" --description "$desc" || true
  gh pr edit "$PR_NUMBER" --add-label "$label" || true
}

add_label "prov:host=${HOST_SHORT}" "Host provenance" "EEEEEE"
add_label "prov:pid=${PID_HINT}" "PID provenance" "DDDDDD"
add_label "agent:${AGENT_TAG}" "Agent name" "CCCCCC"
add_label "model:${MODEL_TAG:-unspecified}" "Model name" "BBBBBB"
add_label "owner:${OWNER_TAG}" "Work owner" "AAAAAA"
