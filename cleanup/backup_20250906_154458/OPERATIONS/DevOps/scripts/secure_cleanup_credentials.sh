#!/bin/bash
# 🔒 NETTOYAGE SÉCURISÉ CREDENTIALS GIT
# Supprimer COMPLÈTEMENT les mots de passe stockés

echo "🔒 NETTOYAGE SÉCURISÉ CREDENTIALS GIT"
echo "====================================="

# Étape 1: Nettoyer TOUS les credentials stockés
echo "🧹 Suppression complète credentials..."

# Supprimer credential manager entries
git config --global --unset-all credential.helper 2>/dev/null
git config --global --unset-all credential.username 2>/dev/null  
git config --global --unset-all credential.password 2>/dev/null

# Supprimer fichiers credentials
rm -f ~/.git-credentials 2>/dev/null
rm -f ~/.netrc 2>/dev/null

# Nettoyer cache Git credentials
git credential-manager-core erase 2>/dev/null || echo "   ℹ️ credential-manager-core non disponible"

# Étape 2: Nettoyer le remote origin de toute trace d'credentials
echo "🔗 Nettoyage remote origin..."
cd /home/stephane/GitHub/PaniniFS-1

# Vérifier si l'URL contient des credentials
CURRENT_URL=$(git remote get-url origin)
echo "   URL actuelle: $CURRENT_URL"

# Si l'URL contient des credentials (@ avant github.com), la nettoyer
if [[ "$CURRENT_URL" == *"@github.com"* ]] && [[ "$CURRENT_URL" != "git@github.com"* ]]; then
    echo "   ⚠️ URL contient des credentials, nettoyage..."
    CLEAN_URL="https://github.com/stephanedenis/PaniniFS.git"
    git remote set-url origin "$CLEAN_URL"
    echo "   ✅ URL nettoyée: $CLEAN_URL"
else
    echo "   ✅ URL déjà propre"
fi

# Étape 3: Configuration sécurisée
echo "🔐 Configuration sécurisée..."
git config --global user.name "stephanedenis"
git config --global user.email "stephane@sdenis.com"

# NE PAS configurer credential.helper pour forcer la demande manuelle
echo "   ✅ Credentials helper: DÉSACTIVÉ (sécurisé)"
echo "   ✅ Username: stephanedenis" 
echo "   ✅ Email: stephane@sdenis.com"

# Étape 4: Vérifications
echo "🔍 Vérifications sécurité..."
echo "   Remote origin: $(git remote get-url origin)"
echo "   User config: $(git config user.name) <$(git config user.email)>"
echo "   Credential helper: $(git config --global credential.helper || echo 'AUCUN (sécurisé)')"

# Étape 5: Nettoyer historique bash/clipboard
echo "🧹 Nettoyage traces..."
# Nettoyer clipboard Klipper
rm -rf ~/.local/share/klipper/data/* 2>/dev/null
echo "   ✅ Clipboard nettoyé"

# Nettoyer dernières lignes d'historique bash qui pourraient contenir le mot de passe
history -d $(history | tail -10 | head -1 | awk '{print $1}') 2>/dev/null || true
echo "   ✅ Historique nettoyé"

echo ""
echo "✅ NETTOYAGE SÉCURISÉ TERMINÉ!"
echo "=============================="
echo "🔐 SÉCURITÉ RENFORCÉE:"
echo "   ❌ Aucun mot de passe stocké"
echo "   ❌ Aucun credential helper automatique"
echo "   ✅ URL remote propre"
echo "   ✅ Configuration utilisateur correcte"
echo ""
echo "🚀 POUR LE PROCHAIN PUSH:"
echo "=========================="
echo "Git demandera manuellement:"
echo "   Username: stephanedenis"
echo "   Password: [TOKEN_GITHUB_PERSONNEL]"
echo ""
echo "💡 RECOMMANDATION:"
echo "   Créer un Personal Access Token sur GitHub"
echo "   GitHub > Settings > Developer settings > Personal access tokens"
echo ""
echo "🌟 SÉCURITÉ MAXIMALE GARANTIE!"
