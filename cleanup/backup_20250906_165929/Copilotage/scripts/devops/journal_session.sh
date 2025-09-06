#!/usr/bin/env bash
set -euo pipefail

# journal_session.sh — crée une entrée de journal Copilotage pour la date courante
# Usage: journal_session.sh "slug-de-session"  # ex: journal_session.sh session

SESSION=${1:-session}
DATE=$(date +%F)
HOST=$(hostname -s 2>/dev/null || hostname)
# Utiliser le PID VS Code si dispo, sinon PID du shell
PID=${VSCODE_PID:-$$}
DIR="Copilotage/journal"
FILE="$DIR/${DATE}-${HOST}-pid${PID}-${SESSION}.md"

mkdir -p "$DIR"
if [[ -f "$FILE" ]]; then
  echo "Journal déjà existant: $FILE" >&2
  exit 0
fi

cat > "$FILE" <<EOF
# Journal de session — ${DATE} (${HOST}, pid ${PID})

Contexte: ...

Décisions & actions clés:
- ...

Liens:
- Issues/PR: ...

Tests/quality gates:
- ...

Prochaines étapes:
- ...

---

Agent: journal créé automatiquement.
EOF

echo "$FILE"
