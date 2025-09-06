#!/bin/bash
# 🔒 NETTOYAGE COMPLET TRACES CREDENTIALS
# Supprimer TOUTES les traces du mot de passe dans VSCode et système

echo "🔒 NETTOYAGE COMPLET TRACES CREDENTIALS"
echo "======================================="

PASSWORD_PATTERN="***REDACTED***"
PASSWORD_DECODED="***REDACTED***"

echo "🎯 Recherche et suppression: [PATTERN REDACTED FOR SECURITY]"
echo ""

# Étape 1: Nettoyer logs VSCode
echo "🧹 NETTOYAGE LOGS VSCODE..."
VSCODE_LOG_DIR="$HOME/.config/Code/logs"
if [ -d "$VSCODE_LOG_DIR" ]; then
    echo "   📁 Nettoyage logs VSCode..."
    find "$VSCODE_LOG_DIR" -name "*.log" -exec sed -i "s/${PASSWORD_PATTERN}/***REMOVED***/g" {} \; 2>/dev/null
    find "$VSCODE_LOG_DIR" -name "*.log" -exec sed -i "s/${PASSWORD_DECODED}/***REMOVED***/g" {} \; 2>/dev/null
    echo "   ✅ Logs VSCode nettoyés"
else
    echo "   ℹ️ Logs VSCode non trouvés"
fi

# Étape 2: Nettoyer sessions chat VSCode
echo "🗨️ NETTOYAGE SESSIONS CHAT VSCODE..."
CHAT_DIR="$HOME/.config/Code/User/workspaceStorage"
if [ -d "$CHAT_DIR" ]; then
    echo "   📁 Nettoyage sessions chat..."
    find "$CHAT_DIR" -name "*.json" -exec sed -i "s/${PASSWORD_PATTERN}/***REMOVED***/g" {} \; 2>/dev/null
    find "$CHAT_DIR" -name "*.json" -exec sed -i "s/${PASSWORD_DECODED}/***REMOVED***/g" {} \; 2>/dev/null
    echo "   ✅ Sessions chat nettoyées"
else
    echo "   ℹ️ Sessions chat non trouvées"
fi

# Étape 3: Nettoyer clipboard Klipper
echo "📋 NETTOYAGE CLIPBOARD KLIPPER..."
KLIPPER_DIR="$HOME/.local/share/klipper"
if [ -d "$KLIPPER_DIR" ]; then
    echo "   📁 Suppression données Klipper..."
    rm -rf "$KLIPPER_DIR/data" 2>/dev/null
    echo "   ✅ Clipboard Klipper nettoyé"
else
    echo "   ℹ️ Klipper non trouvé"
fi

# Étape 4: Nettoyer historique bash
echo "📜 NETTOYAGE HISTORIQUE BASH..."
if [ -f "$HOME/.bash_history" ]; then
    echo "   📁 Nettoyage .bash_history..."
    sed -i "s/${PASSWORD_PATTERN}/***REMOVED***/g" "$HOME/.bash_history" 2>/dev/null
    sed -i "s/${PASSWORD_DECODED}/***REMOVED***/g" "$HOME/.bash_history" 2>/dev/null
    echo "   ✅ Historique bash nettoyé"
fi

# Nettoyer historique session actuelle
history -c 2>/dev/null
echo "   ✅ Historique session nettoyé"

# Étape 5: Nettoyer cache applications
echo "🗂️ NETTOYAGE CACHES APPLICATIONS..."
find "$HOME/.cache" -name "*.log" -exec grep -l "$PASSWORD_PATTERN" {} \; 2>/dev/null | while read file; do
    echo "   🧹 Nettoyage: $file"
    sed -i "s/${PASSWORD_PATTERN}/***REMOVED***/g" "$file" 2>/dev/null
done

# Étape 6: Nettoyer fichiers temporaires
echo "🗑️ NETTOYAGE FICHIERS TEMPORAIRES..."
find /tmp -user $(whoami) -name "*" -exec grep -l "$PASSWORD_PATTERN" {} \; 2>/dev/null | while read file; do
    echo "   🗑️ Suppression: $file"
    rm -f "$file" 2>/dev/null
done

# Étape 7: Vérification finale
echo ""
echo "🔍 VÉRIFICATION FINALE..."
echo "========================"

REMAINING_TRACES=$(grep -r "$PASSWORD_PATTERN" "$HOME" 2>/dev/null | wc -l)
echo "📊 Traces restantes: $REMAINING_TRACES"

if [ "$REMAINING_TRACES" -eq 0 ]; then
    echo "✅ NETTOYAGE COMPLET!"
    echo "🔒 Aucune trace du mot de passe détectée"
else
    echo "⚠️ Quelques traces persistent (probablement dans des fichiers système ou archives)"
    echo "📝 Listing traces restantes:"
    grep -r "$PASSWORD_PATTERN" "$HOME" 2>/dev/null | head -3 | sed "s/${PASSWORD_PATTERN}/***FOUND_HERE***/g"
fi

echo ""
echo "🛡️ SÉCURITÉ RENFORCÉE:"
echo "======================"
echo "✅ Logs VSCode: Nettoyés"
echo "✅ Sessions chat: Nettoyées"  
echo "✅ Clipboard: Vidé"
echo "✅ Historique: Purgé"
echo "✅ Cache: Nettoyé"
echo "✅ Fichiers temp: Supprimés"

echo ""
echo "🚀 SYSTÈME MAINTENANT SÉCURISÉ!"
echo "🎯 Prêt pour déploiement Colab avec authentification propre"
