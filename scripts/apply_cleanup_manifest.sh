#!/usr/bin/env bash
set -euo pipefail

MANIFEST="cleanup/manifest.txt"
BACKUP_DIR="cleanup/backup_$(date +%Y%m%d_%H%M%S)"

if [[ ! -f "$MANIFEST" ]]; then
  echo "Manifeste introuvable: $MANIFEST" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"

while IFS= read -r path; do
  [[ -z "$path" || "$path" =~ ^# ]] && continue
  if [[ -e "$path" ]]; then
    echo "[backup] $path -> $BACKUP_DIR/$path"
    mkdir -p "$BACKUP_DIR/$(dirname "$path")"
    cp -a "$path" "$BACKUP_DIR/$path" || true
    echo "[remove] $path"
    rm -rf "$path"
  else
    echo "[skip] $path (absent)"
  fi
done < "$MANIFEST"

echo "Nettoyage terminé. Backup: $BACKUP_DIR"
