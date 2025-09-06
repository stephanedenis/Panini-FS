#!/usr/bin/env bash
set -euo pipefail
# gh_queue.sh — utilitaires légers de coordination via labels
# Usage:
#   gh_queue.sh list [--queue <name>] [--owner agent|human] [--state open|closed|all]
#   gh_queue.sh move <issue|pr> <number> --queue <name>
#   gh_queue.sh set <issue|pr> <number> [--priority <p>] [--size <s>]
# Requiert gh CLI et jq.

cmd=${1:-}
shift || true

if ! command -v gh >/dev/null 2>&1; then echo "gh requis" >&2; exit 2; fi
if ! command -v jq >/dev/null 2>&1; then echo "jq requis" >&2; exit 2; fi

case "${cmd}" in
  list)
    QUEUE=""; OWNER=""; STATE="open"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --queue) QUEUE=${2:-}; shift 2;;
        --owner) OWNER=${2:-}; shift 2;;
        --state) STATE=${2:-}; shift 2;;
        *) shift;;
      esac
    done
    gh issue list --state "$STATE" --limit 200 --json number,title,labels,url | \
      jq -r --arg Q "$QUEUE" --arg O "$OWNER" '
        .[] | select(($Q=="") or (.labels[].name|startswith("queue:") and .labels[].name==$Q))
            | select(($O=="") or (.labels[].name==("owner:"+$O)))
            | "#\(.number) | \(.title) | \(.labels|map(.name)|join(",")) | \(.url)"'
    ;;
  move)
    TYPE=${1:-}; shift || true
    NUM=${1:-}; shift || true
    QUEUE=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --queue) QUEUE=${2:-}; shift 2;;
        *) shift;;
      esac
    done
    if [[ -z "$TYPE" || -z "$NUM" || -z "$QUEUE" ]]; then echo "Usage: move <issue|pr> <number> --queue <name>" >&2; exit 2; fi
    # Retire autres queue:* et ajoute la nouvelle
    existing=$(gh issue view "$NUM" --json labels | jq -r '.labels[].name // empty' | grep '^queue:' || true)
    for q in $existing; do gh issue edit "$NUM" --remove-label "$q"; done
    gh issue edit "$NUM" --add-label "$QUEUE"
    echo "#${NUM} -> $QUEUE";
    ;;
  set)
    TYPE=${1:-}; shift || true
    NUM=${1:-}; shift || true
    P=""; S=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --priority) P=${2:-}; shift 2;;
        --size) S=${2:-}; shift 2;;
        *) shift;;
      esac
    done
    if [[ -n "$P" ]]; then gh issue edit "$NUM" --add-label "$P"; fi
    if [[ -n "$S" ]]; then gh issue edit "$NUM" --add-label "$S"; fi
    echo "#${NUM} set ${P} ${S}";
    ;;
  *)
    echo "Usage: $0 list|move|set ..." >&2; exit 2;;
 esac
