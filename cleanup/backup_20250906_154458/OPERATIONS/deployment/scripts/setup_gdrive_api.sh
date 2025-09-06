#!/bin/bash
# Script de setup rapide Google Drive API

echo "🚀 SETUP RAPIDE GOOGLE DRIVE API"
echo "================================"

# Variables
PROJECT_NAME="PaniniFS-Research-Platform"
CREDENTIALS_DIR="$(pwd)/gdrive_credentials"

echo "📁 Création répertoire credentials..."
mkdir -p "$CREDENTIALS_DIR"

echo "🌐 Ouverture Google Cloud Console..."
# Ouvrir directement la page de création de projet
python3 -c "import webbrowser; webbrowser.open('https://console.cloud.google.com/projectcreate')"

echo ""
echo "📋 ACTIONS MANUELLES REQUISES:"
echo "1. Créer projet: $PROJECT_NAME"
echo "2. Activer Google Drive API"
echo "3. Créer credentials OAuth 2.0 Desktop"
echo "4. Télécharger et placer dans: $CREDENTIALS_DIR/credentials.json"
echo ""
echo "🔧 Après configuration, lancer:"
echo "   python3 Copilotage/scripts/autonomous_gdrive_manager.py"

read -p "Appuyez sur Entrée pour continuer..."
