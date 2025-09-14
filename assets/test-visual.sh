#!/bin/bash

echo "🔍 Test de la page PaniniFS avec texture alvéolaire"
echo "📍 URL: http://localhost:9000/index.html"

# Vérifier que le serveur répond
echo "🌐 Test de connectivité..."
curl -s -I http://localhost:9000/index.html | head -1

# Ouvrir dans Firefox en mode headless (si disponible)
echo "🖥️ Tentative d'ouverture en mode headless..."
if command -v firefox &> /dev/null; then
    echo "✅ Firefox disponible"
    # Prendre une capture d'écran avec Firefox headless
    timeout 30s firefox --headless --screenshot=/tmp/paniniFS-screenshot.png http://localhost:9000/index.html 2>/dev/null || echo "⚠️ Capture échouée"
    
    if [ -f /tmp/paniniFS-screenshot.png ]; then
        echo "📸 Capture d'écran sauvée: /tmp/paniniFS-screenshot.png"
        ls -lh /tmp/paniniFS-screenshot.png
    fi
fi

# Vérifier le contenu HTML
echo ""
echo "📋 Contenu HTML de base:"
curl -s http://localhost:9000/index.html | grep -E "(title|h1|PaniniFS)" | head -5

echo ""
echo "🎨 Recherche de styles CSS:"
curl -s http://localhost:9000/index.html | grep -E "(background|hex|alvéole)" | head -3

echo ""
echo "✨ Page disponible sur: http://localhost:9000/index.html"
