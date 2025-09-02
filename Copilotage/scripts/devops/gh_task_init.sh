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

# Afficher le préfixe PR recommandé
HOST_SHORT=${HOSTNAME:-$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "host")}
PID_HINT=$$
RECOMMENDED_PREFIX="[journal:${HOST_SHORT}-pid${PID_HINT}]"
echo "Astuce PR: Préfixe recommandé: ${RECOMMENDED_PREFIX} <type>: <résumé> (Refs #${ISSUE_NUM})" >&2

echo "Issue #$ISSUE_NUM" >&2
echo "Branche: $BRANCH" >&2

# Auto: créer et commiter une entrée de journal Copilotage pour cette session
if [[ -x Copilotage/scripts/devops/journal_session.sh ]]; then
  JFILE=$(Copilotage/scripts/devops/journal_session.sh session || true)
  if [[ -n "$JFILE" && -f "$JFILE" ]]; then
    echo "Journal créé: $JFILE" >&2
    git add "$JFILE" || true
    DATE_STR=$(date +%F)
    git commit -m "journal(copilotage): init ${DATE_STR} ${HOST_SHORT}-pid${PID_HINT} (auto via gh_task_init)" || true
    git push || true
  else
    echo "(info) Journal non créé (déjà existant ou script silencieux)." >&2
  fi
else
  echo "(warn) Script journal_session.sh introuvable/exécutable, saut de la création auto du journal." >&2
fi
