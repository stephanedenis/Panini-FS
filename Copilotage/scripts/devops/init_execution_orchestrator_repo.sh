#!/usr/bin/env bash
set -euo pipefail

REPO="stephanedenis/PaniniFS-ExecutionOrchestrator"

cat <<'EOF'
Ce script prépare un nouveau dépôt GitHub ExecutionOrchestrator via gh, ajoute un scaffold minimal, et pousse main.
Il n’exécute rien sans votre confirmation.
EOF

read -rp "Créer le repo ${REPO} ? [y/N] " yn
if [[ "${yn:-N}" != "y" ]]; then
  echo "Annulé."
  exit 0
fi

# Créer le repo (privé par défaut, vous pouvez le rendre public ensuite)
gh repo create "$REPO" --private --description "Execution orchestrator (drivers: local, colab, cloud)"

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
cd "$tmpdir"

git clone "git@github.com:${REPO}.git"
cd PaniniFS-ExecutionOrchestrator

# Copier le scaffold
rsync -a --exclude ".github" "${OLDPWD}/../scaffolds/execution-orchestrator/" ./
mkdir -p .github/workflows
cp -a "${OLDPWD}/../scaffolds/execution-orchestrator/.github/workflows/ci.yml" .github/workflows/ci.yml

echo "MIT License" > LICENSE

git add -A
git commit -m "chore: initial scaffold (pyproject, CLI, CI)"
git branch -M main
git push -u origin main

echo "Dépôt initialisé: https://github.com/${REPO}"
