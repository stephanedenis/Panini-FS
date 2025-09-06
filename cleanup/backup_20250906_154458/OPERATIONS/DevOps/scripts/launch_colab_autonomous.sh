#!/bin/bash

# 🚀 PaniniFS - Lanceur Cloud Autonome Ultra-Simplifié
# Usage: Copier-coller dans une cellule Colab

echo "🚀 PANINI FS - CLOUD AUTONOME LAUNCHER"
echo "======================================"

# Vérification environnement Colab
if [[ -d "/content" ]]; then
    echo "✅ Mode Colab détecté"
    cd /content
else
    echo "⚠️  Mode local détecté - utiliser les scripts locaux"
    exit 1
fi

# Nettoyage rapide
echo "🧹 Nettoyage environnement..."
rm -rf PaniniFS-* Pensine totoro-automation hexagonal-demo 2>/dev/null

# Clonage repo principal
echo "📥 Clonage PaniniFS principal..."
git clone https://github.com/stephanedenis/PaniniFS.git PaniniFS-1 --quiet

if [[ -d "PaniniFS-1" ]]; then
    echo "✅ PaniniFS-1 cloné avec succès"
    
    # Lancement direct du notebook cloud autonome
    echo "🚀 Ouverture notebook cloud autonome..."
    echo ""
    echo "📖 INSTRUCTIONS:"
    echo "1. Ouvrir: PaniniFS-1/Copilotage/colab_cloud_autonomous.ipynb"
    echo "2. Exécuter toutes les cellules (Ctrl+F9)"
    echo "3. Le système clone automatiquement tous les repos"
    echo "4. Performance garantie: ~10-15 secondes total"
    echo ""
    echo "🎯 READY TO GO!"
else
    echo "❌ Erreur clonage - vérifiez la connexion réseau"
    exit 1
fi
