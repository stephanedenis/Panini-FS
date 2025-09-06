#!/usr/bin/env bash
set -euo pipefail
# Génère Copilotage/journal/INDEX.md listant toutes les entrées, triées par date décroissante.
ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
JDIR="$ROOT_DIR/Copilotage/journal"
OUT="$JDIR/INDEX.md"
mkdir -p "$JDIR"
TMP="$(mktemp)"
DATE_ISO=$(date -Iseconds)
{
  echo "# Index des journaux — Copilotage"
  echo
  echo "Généré: ${DATE_ISO}"
  echo
  echo "## Entrées"
  echo
  # Lister les .md (hors INDEX.md), triés par nom décroissant (YYYY-MM-DD…)
  ls -1 "$JDIR"/*.md 2>/dev/null | grep -v "/INDEX.md$" | sort -r | while read -r f; do
    base=$(basename "$f")
    # Extraire date et slug
    date_part=${base%%-*}
    # lien relatif
    echo "- [${base}](${base})"
  done
} > "$TMP"
# Écrire seulement si différent
if [[ ! -f "$OUT" ]] || ! cmp -s "$TMP" "$OUT"; then
  mv "$TMP" "$OUT"
  echo "$OUT"
else
  rm -f "$TMP"
  echo ""
fi
