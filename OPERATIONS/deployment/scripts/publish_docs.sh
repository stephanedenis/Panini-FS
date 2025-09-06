#!/bin/bash

# Script de publication automatique sur paninifs.org
# Usage: ./publish_docs.sh "message de commit"

set -e

COMMIT_MESSAGE=${1:-"Update documentation"}

echo "📚 Publication automatique de la documentation PFS"
echo "=================================================="

# Vérification que nous sommes dans un repo Git
if [ ! -d ".git" ]; then
    echo "❌ Erreur: Pas dans un repository Git"
    exit 1
fi

# Test de build local
echo "🧪 Test de build local..."
./deploy_docs.sh test

if [ $? -ne 0 ]; then
    echo "❌ Erreur: Le build local a échoué"
    exit 1
fi

# Ajout des fichiers modifiés
echo "📝 Ajout des fichiers au staging..."
git add docs/
git add mkdocs.yml
git add requirements.txt
git add CNAME
git add .github/workflows/deploy-docs.yml
git add deploy_docs.sh
git add setup_github_pages.sh
git add publish_docs.sh

# Vérification des changements
if git diff --cached --quiet; then
    echo "ℹ️  Aucun changement à commiter"
    echo "✅ Documentation déjà à jour"
    exit 0
fi

# Commit
echo "💾 Commit des changements..."
git commit -m "$COMMIT_MESSAGE"

# Push vers GitHub (déclenche le déploiement automatique)
echo "🚀 Push vers GitHub et déclenchement du déploiement..."
git push origin master

echo ""
echo "✅ Publication déclenchée avec succès !"
echo ""
echo "📊 Suivi du déploiement :"
echo "   - Actions GitHub: https://github.com/stephanedenis/PaniniFS/actions"
echo "   - Site final: https://paninifs.org"
echo ""
echo "⏱️  Le déploiement prend généralement 2-5 minutes"
echo "🔔 Vous recevrez une notification si le déploiement échoue"
