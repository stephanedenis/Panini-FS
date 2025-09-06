#!/bin/bash
# 🔒 VÉRIFICATION FINALE SÉCURITÉ
# Double-check aucun credential stocké nulle part

echo "🔒 VÉRIFICATION FINALE SÉCURITÉ"
echo "==============================="

# Fonction pour masquer les mots de passe dans la sortie
mask_password() {
    sed 's/vac[*^A-Za-z0-9]*[*u]/***PASSWORD_MASKED***/g'
}

echo "🔍 Vérification complète repositories Git..."

# Vérifier tous les repos dans GitHub folder
for repo in /home/stephane/GitHub/*/; do
    if [ -d "$repo/.git" ]; then
        echo "📁 Repo: $(basename "$repo")"
        cd "$repo"
        
        # Vérifier remote URLs
        git remote -v 2>/dev/null | mask_password | head -2
        
        # Vérifier config local
        SUSPECT_URL=$(git config --local --list 2>/dev/null | grep -E "url.*vac" | mask_password)
        if [ ! -z "$SUSPECT_URL" ]; then
            echo "   ⚠️ URL suspecte trouvée: $SUSPECT_URL"
        fi
    fi
done

echo ""
echo "🔍 Vérification fichiers système..."

# Vérifier tous les fichiers de config Git
for config_file in ~/.gitconfig ~/.git-credentials ~/.netrc; do
    if [ -f "$config_file" ]; then
        echo "📄 $config_file:"
        SUSPECT_LINE=$(grep -E "vac|%2A|%5E" "$config_file" 2>/dev/null | mask_password)
        if [ ! -z "$SUSPECT_LINE" ]; then
            echo "   ⚠️ Ligne suspecte: $SUSPECT_LINE"
        else
            echo "   ✅ Propre"
        fi
    else
        echo "📄 $config_file: ✅ N'existe pas (bon)"
    fi
done

echo ""
echo "🔍 Vérification processus en cours..."

# Vérifier si des processus Git utilisent des URLs avec credentials
SUSPECT_PROCESS=$(ps aux | grep -E "git.*vac" | grep -v grep | mask_password)
if [ ! -z "$SUSPECT_PROCESS" ]; then
    echo "⚠️ Processus suspect: $SUSPECT_PROCESS"
else
    echo "✅ Aucun processus Git suspect"
fi

echo ""
echo "🔍 Vérification dernière commande..."

# Vérifier si la dernière tentative de push a laissé des traces
LAST_PUSH_ERROR=$(git log --oneline -1 2>/dev/null)
echo "📝 Dernier commit: $LAST_PUSH_ERROR"

# Test final avec push dry-run
cd /home/stephane/GitHub/PaniniFS-1
echo ""
echo "🧪 Test push dry-run (simulation)..."
git push --dry-run origin master 2>&1 | mask_password | head -3

echo ""
echo "✅ VÉRIFICATION TERMINÉE"
echo "========================"
echo "Si aucune ligne '⚠️' ci-dessus, le système est sécurisé."
echo "Sinon, indiquer les lignes suspectes pour nettoyage ciblé."
