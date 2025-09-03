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

echo "[1/5] Splitting history of '$DIR' using git subtree"
SUBTREE_SHA=$(git subtree split --prefix="$DIR" "$BRANCH")

echo "[2/5] Pushing split history to new repository: $REMOTE_URL"
git remote remove split-target 2>/dev/null || true
git remote add split-target "$REMOTE_URL"
git push split-target "$SUBTREE_SHA":master

echo "[3/5] Removing '$DIR' from main repo"
git rm -r "$DIR"
git commit -m "submodules: extract $DIR into dedicated repo"

echo "[4/5] Adding submodule at '$SUB_PATH'"
git submodule add "$REMOTE_URL" "$SUB_PATH"
git commit -m "submodules: add $SUB_PATH submodule"

echo "[5/5] Done. Next: (cd $SUB_PATH && git checkout master)."
