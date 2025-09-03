#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/split_to_submodule.sh DIR NEW_REPO_SSH_URL [SUBMODULE_PATH]
# Example:
#   scripts/split_to_submodule.sh RESEARCH git@github.com:stephanedenis/PaniniFS-Research.git RESEARCH

DIR=${1:-}
REMOTE_URL=${2:-}
SUB_PATH=${3:-$DIR}
BRANCH=${BRANCH:-master}

if [[ -z "$DIR" || -z "$REMOTE_URL" ]]; then
  echo "Usage: $0 DIR NEW_REPO_SSH_URL [SUBMODULE_PATH]" >&2
  exit 1
fi

if [[ ! -d "$DIR" ]]; then
  echo "Directory '$DIR' not found" >&2
  exit 1
fi

# Ensure clean tree
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree not clean. Commit/stash changes first." >&2
  exit 1
fi

ROOT=$(git rev-parse --show-toplevel)
TMP_BRANCH="split-${DIR//\//-}-$(date +%s)"

echo "[1/6] Creating split branch: $TMP_BRANCH"
git branch -f "$TMP_BRANCH" "$BRANCH" >/dev/null 2>&1 || git checkout -b "$TMP_BRANCH"
git checkout "$TMP_BRANCH"

HAS_FILTER_REPO=0
if command -v git-filter-repo >/dev/null 2>&1; then
  HAS_FILTER_REPO=1
elif command -v git >/dev/null 2>&1 && git help -a | grep -q filter-repo; then
  HAS_FILTER_REPO=1
fi

if [[ $HAS_FILTER_REPO -eq 1 ]]; then
  echo "[2/6] Using git filter-repo to isolate '$DIR'"
  git filter-repo --path "$DIR" --force
else
  echo "[2/6] Using git subtree split to isolate '$DIR' (fallback)"
  SUBTREE_SHA=$(git subtree split --prefix="$DIR" "$BRANCH")
  git checkout --detach "$SUBTREE_SHA"
fi

echo "[3/6] Adding remote and pushing to: $REMOTE_URL"
git remote remove split-target 2>/dev/null || true
git remote add split-target "$REMOTE_URL"
git push split-target HEAD:master

echo "[4/6] Returning to main repo and removing '$DIR'"
cd "$ROOT"
git checkout "$BRANCH"
git rm -r "$DIR"
git commit -m "submodules: extract $DIR into dedicated repo"

echo "[5/6] Adding submodule at '$SUB_PATH' → $REMOTE_URL"
git submodule add "$REMOTE_URL" "$SUB_PATH"
git commit -m "submodules: add $SUB_PATH submodule"

echo "[6/6] Done. Next: (cd $SUB_PATH && git checkout master) and seed docs/workspace there."
