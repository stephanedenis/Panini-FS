#!/bin/bash
# 🚀 COLAB LAUNCHER AUTOMATION
# Notebook: semantic_processing_accelerated

echo "🚀 LANCEMENT COLAB: semantic_processing_accelerated"
echo "=================================="

# Étape 1: Upload vers GitHub (si pas déjà fait)
echo "📤 Upload vers GitHub..."
cd /home/stephane/GitHub/PaniniFS-1
git add /home/stephane/GitHub/PaniniFS-1/Copilotage/colab_notebooks/semantic_processing_accelerated.ipynb
git commit -m "Add Colab notebook: semantic_processing_accelerated" || echo "   ℹ️ Pas de nouveaux changements"
git push origin master

# Étape 2: Générer URL Colab
GITHUB_URL="https://github.com/stephanedenis/PaniniFS/blob/master/Copilotage/colab_notebooks/semantic_processing_accelerated.ipynb"
COLAB_URL="https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master/Copilotage/colab_notebooks/semantic_processing_accelerated.ipynb"

echo "🌐 URLs générées:"
echo "   📄 GitHub: $GITHUB_URL"
echo "   🚀 Colab:  $COLAB_URL"

# Étape 3: Ouvrir Colab (optionnel)
read -p "🤔 Ouvrir Colab maintenant? (y/N): " open_colab
if [[ "$open_colab" =~ ^[Yy]$ ]]; then
    echo "🌐 Ouverture Colab..."
    xdg-open "$COLAB_URL"
else
    echo "📋 URL Colab copiée dans clipboard:"
    echo "$COLAB_URL" | xclip -selection clipboard 2>/dev/null || echo "   ⚠️ xclip non disponible"
fi

echo ""
echo "✅ COLAB PRÊT!"
echo "🎯 Notebook: semantic_processing_accelerated"
echo "⚡ GPU: Tesla T4 (22-60x speedup)"
echo "🔄 Monitoring: Manual via Colab interface"
echo ""
echo "📝 NEXT STEPS:"
echo "1. Exécuter cells dans Colab (Ctrl+F9)"
echo "2. Vérifier GPU activation"
echo "3. Attendre completion (notification Colab)"
echo "4. Télécharger résultats"
