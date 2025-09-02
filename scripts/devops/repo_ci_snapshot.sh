#!/usr/bin/env bash
set -euo pipefail

export GIT_PAGER=cat
export GH_PAGER=cat
export PAGER=cat
export LESS=FRSX

OUTDIR="artifacts/snapshots"
mkdir -p "$OUTDIR" 2>/dev/null || true
STAMP=$(date +%Y%m%d-%H%M%S)
OUTFILE="$OUTDIR/snapshot-$STAMP.txt"

exec > >(tee -a "$OUTFILE") 2>&1 || true

echo "=== Repo/CI Snapshot @ $(date -Is) ==="
echo "CWD=$(pwd)"

echo
echo "-- Git --"
echo -n "Branch: "; git branch --show-current || true
git fetch --all -p >/dev/null 2>&1 || true
echo "Status (porcelain):"; git status -s || true
echo "Recent commits (origin/master):"; git --no-pager log origin/master -n 6 --pretty=format:'%h %ad %an %s' --date=short || true

echo
echo "-- Open PRs --"
if command -v gh >/dev/null 2>&1; then
  PR_JSON=$(gh pr list --state open --limit 20 --json number,title,headRefName,mergeStateStatus,isDraft,labels 2>/dev/null || echo '[]')
  echo "$PR_JSON" | jq -r '.[] | "#" + (.number|tostring) + " | " + .title + " | branch=" + .headRefName + " | mergeable=" + (.mergeStateStatus//"?") + " | draft=" + (.isDraft|tostring) + " | labels=" + ((.labels//[])|map(.name)|join(","))' || echo "(no PRs or gh/jq missing)"
  for N in $(echo "$PR_JSON" | jq -r '.[].number' 2>/dev/null); do
    echo; echo "Checks for PR #$N:";
    gh pr checks "$N" --fail-fast=false || true
  done
else
  echo "gh CLI not available"
fi

echo
echo "-- Recent workflows --"
if command -v gh >/dev/null 2>&1; then
  gh run list --limit 12 --json databaseId,workflowName,headBranch,status,conclusion,displayTitle 2>/dev/null \
    | jq -r '.[] | "id=" + (.databaseId|tostring) + " | wf=" + .workflowName + " | branch=" + (.headBranch//"-") + " | status=" + .status + " | conclusion=" + (.conclusion//"-") + " | title=" + .displayTitle' || true
fi

echo
echo "Snapshot saved to: $OUTFILE"
