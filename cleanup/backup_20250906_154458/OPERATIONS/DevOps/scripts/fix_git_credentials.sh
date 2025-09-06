#!/bin/bash
# 🔧 CORRECTION CREDENTIALS GIT
# Fix paramètres Git et credentials pour GitHub

echo "🔧 CORRECTION CREDENTIALS GIT"
echo "============================="

# Étape 1: Nettoyer credentials existants
echo "🧹 Nettoyage credentials existants..."
rm -f ~/.git-credentials 2>/dev/null
git config --global --unset credential.username 2>/dev/null
git config --global --unset credential.password 2>/dev/null

# Étape 2: Configuration correcte
echo "⚙️ Configuration Git correcte..."
git config --global user.name "stephanedenis"
git config --global user.email "stephane@sdenis.com"
git config --global credential.helper store

echo "   ✅ user.name: stephanedenis"
echo "   ✅ user.email: stephane@sdenis.com"
echo "   ✅ credential.helper: store"

# Étape 3: Vérifier remote URL
echo "🔗 Vérification remote origin..."
git remote -v

# Étape 4: Test authentification
echo ""
echo "🔐 PROCHAINE ÉTAPE: AUTHENTIFICATION"
echo "====================================="
echo "Lors du prochain push, GitHub demandera:"
echo "   Username: stephanedenis"
echo "   Password: [VOTRE_TOKEN_GITHUB_PERSONNEL]"
echo ""
echo "💡 IMPORTANT:"
echo "   - Username: stephanedenis (PAS votre email)"
echo "   - Password: Utiliser un Personal Access Token"
echo "   - Token créé sur: GitHub > Settings > Developer settings > Personal access tokens"
echo ""
echo "🚀 Ready pour nouveau push!"
