#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

echo "== Normalisation remote (HTTPS) =="
Copilotage/scripts/devops/fix_remotes.sh https || true

echo
echo "== Installation requirements Copilotage =="
if [ -f Copilotage/scripts/requirements.txt ]; then
  pip3 install -r Copilotage/scripts/requirements.txt || true
fi
if [ -f Copilotage/agents/requirements.txt ]; then
  pip3 install -r Copilotage/agents/requirements.txt || true
fi

echo
echo "== Audit Git =="
Copilotage/scripts/devops/git_audit.sh || true

echo
echo "== Rappel =="
echo "- Pour init submodules: Copilotage/scripts/devops/bootstrap_submodules.sh"
echo "- Pour basculer en SSH: Copilotage/scripts/devops/fix_remotes.sh ssh"
