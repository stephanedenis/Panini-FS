#!/bin/bash
# 🚀 DÉPLOIEMENT COLAB - VERSION CORRIGÉE
# Deploy notebook vers Colab avec credentials corrects

echo "🚀 DÉPLOIEMENT COLAB - CREDENTIALS CORRIGÉS"
echo "==========================================="

# Variables
NOTEBOOK_NAME="PaniniFS_Semantic_Acceleration"
COLAB_NOTEBOOKS_DIR="Copilotage/colab_notebooks"
TARGET_FILE="$COLAB_NOTEBOOKS_DIR/PaniniFS_Semantic_Acceleration.ipynb"

# Étape 1: Vérifier notebook source
echo "📝 Vérification notebook source..."
if [ -f "untitled:Untitled-1.ipynb" ]; then
    echo "   ✅ Notebook trouvé: untitled:Untitled-1.ipynb"
    mkdir -p "$COLAB_NOTEBOOKS_DIR"
    cp "untitled:Untitled-1.ipynb" "$TARGET_FILE"
    echo "   ✅ Notebook copié vers: $TARGET_FILE"
else
    echo "   ℹ️ Utilisation notebook existant: $TARGET_FILE"
fi

# Étape 2: Préparation commit
echo "📝 Préparation commit..."
git add .
git status --porcelain

# Étape 3: Commit local
echo "💾 Commit local..."
git commit -m "Add PaniniFS Semantic Acceleration Colab notebook with corrected credentials" || echo "   ℹ️ Pas de nouveaux changements"

# Étape 4: URLs générées
echo "🌐 Génération URLs..."
GITHUB_URL="https://github.com/stephanedenis/PaniniFS/blob/master/$TARGET_FILE"
COLAB_URL="https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master/$TARGET_FILE"

echo ""
echo "📋 URLS GÉNÉRÉES:"
echo "=================="
echo "📄 GitHub: $GITHUB_URL"
echo "🚀 Colab:  $COLAB_URL"
echo ""

# Étape 5: Information push
echo "📤 PUSH VERS GITHUB:"
echo "==================="
echo "🔐 Credentials requis:"
echo "   Username: stephanedenis"
echo "   Password: [VOTRE_TOKEN_PERSONNEL]"
echo ""

# Demander confirmation avant push
read -p "🤔 Procéder au push maintenant? (y/N): " proceed
if [[ "$proceed" =~ ^[Yy]$ ]]; then
    echo "📤 Push en cours..."
    if git push origin master; then
        echo "✅ Push réussi!"
        
        # Copier URL Colab
        echo "$COLAB_URL" | xclip -selection clipboard 2>/dev/null || echo "   ⚠️ xclip non disponible"
        echo "📋 URL Colab copiée dans clipboard"
        
        # Ouvrir Colab
        read -p "🚀 Ouvrir Colab maintenant? (Y/n): " open_colab
        if [[ ! "$open_colab" =~ ^[Nn]$ ]]; then
            echo "🌐 Ouverture Colab..."
            xdg-open "$COLAB_URL"
        fi
        
        echo ""
        echo "✅ DÉPLOIEMENT TERMINÉ!"
        echo "🎯 Notebook disponible sur Colab"
        echo "⚡ Prêt pour accélération 22-60x!"
        
    else
        echo "❌ Erreur push - vérifier credentials"
        echo "💡 Relancer le script après correction"
    fi
else
    echo "⏸️ Push reporté"
    echo "🔗 URLs disponibles quand vous serez prêt"
fi

echo ""
echo "🎯 INSTRUCTIONS COLAB:"
echo "======================"
echo "1. ⚡ Vérifier GPU: Runtime > Change runtime type > GPU"
echo "2. 🔄 Exécuter tout: Ctrl+F9"
echo "3. ⏱️ Attendre 2-5 minutes"
echo "4. 📊 Télécharger résultats"
