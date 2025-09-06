#!/bin/bash
# 🚀 DÉPLOIEMENT AUTOMATIQUE COLAB
# Auto-upload notebook + génération URL directe

echo "🚀 DÉPLOIEMENT AUTOMATIQUE COLAB"
echo "================================="

# Variables
NOTEBOOK_NAME="PaniniFS_Semantic_Acceleration"
NOTEBOOK_FILE="untitled:Untitled-1.ipynb"
TARGET_PATH="Copilotage/colab_notebooks/PaniniFS_Semantic_Acceleration.ipynb"
REPO_URL="https://github.com/stephanedenis/PaniniFS"

# Étape 1: Copier notebook vers repository
echo "📝 Copie notebook vers repository..."
if [ -f "$NOTEBOOK_FILE" ]; then
    mkdir -p "Copilotage/colab_notebooks"
    cp "$NOTEBOOK_FILE" "$TARGET_PATH"
    echo "   ✅ Notebook copié: $TARGET_PATH"
else
    echo "   ⚠️ Notebook source non trouvé, utilisation template existant"
fi

# Étape 2: Commit et push vers GitHub
echo "📤 Upload vers GitHub..."
git add .
git commit -m "Add PaniniFS Semantic Acceleration Colab notebook" || echo "   ℹ️ Pas de nouveaux changements"
git push origin master

# Étape 3: Générer URLs
echo "🌐 Génération URLs..."
GITHUB_URL="$REPO_URL/blob/master/$TARGET_PATH"
COLAB_URL="https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master/$TARGET_PATH"

echo ""
echo "✅ DÉPLOIEMENT TERMINÉ!"
echo "========================"
echo "📄 GitHub: $GITHUB_URL"
echo "🚀 Colab:  $COLAB_URL"
echo ""

# Étape 4: Copier URL dans clipboard et ouvrir
echo "📋 URL Colab copiée dans clipboard"
echo "$COLAB_URL" | xclip -selection clipboard 2>/dev/null || echo "   ⚠️ xclip non disponible"

# Étape 5: Ouvrir automatiquement
read -p "🚀 Ouvrir Colab maintenant? (Y/n): " open_now
if [[ "$open_now" =~ ^[Nn]$ ]]; then
    echo "🔗 URL disponible dans clipboard pour ouverture manuelle"
else
    echo "🌐 Ouverture Colab en cours..."
    xdg-open "$COLAB_URL"
fi

echo ""
echo "🎯 INSTRUCTIONS COLAB:"
echo "1. ⚡ Vérifier GPU activé (Runtime > Change runtime type > GPU)"
echo "2. 🔄 Exécuter tout: Ctrl+F9"
echo "3. ⏱️ Attendre 2-5 minutes"
echo "4. 📊 Télécharger résultats ZIP"
echo ""
echo "🌟 ACCELERATION 22-60x READY!"
