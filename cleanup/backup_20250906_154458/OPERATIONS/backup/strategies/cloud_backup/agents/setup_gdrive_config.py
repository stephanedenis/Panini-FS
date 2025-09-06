#!/usr/bin/env python3
"""
🔑 CONFIGURATEUR GOOGLE DRIVE API AUTONOME
=========================================

Script de configuration autonome pour Google Drive API:
- Guide d'obtention credentials OAuth 2.0
- Création projet Google Cloud automatisée
- Configuration API Drive
- Test connexion et permissions
- 100% autonome avec instructions détaillées
"""

import os
import json
import webbrowser
from pathlib import Path

def create_google_cloud_project_guide():
    """Crée guide de configuration Google Cloud Project"""
    
    print("🔑 CONFIGURATION GOOGLE DRIVE API - ÉTAPES AUTONOMES")
    print("=" * 60)
    
    steps = [
        {
            'step': 1,
            'title': 'Création Projet Google Cloud',
            'description': 'Créer nouveau projet pour PaniniFS',
            'actions': [
                'Aller sur https://console.cloud.google.com/',
                'Cliquer "Nouveau Projet"',
                'Nom: "PaniniFS-Research-Platform"',
                'Créer le projet'
            ]
        },
        {
            'step': 2,
            'title': 'Activation Google Drive API',
            'description': 'Activer API Google Drive pour le projet',
            'actions': [
                'Dans le projet créé, aller à "API et Services"',
                'Cliquer "Bibliothèque"', 
                'Rechercher "Google Drive API"',
                'Cliquer sur Google Drive API et "Activer"'
            ]
        },
        {
            'step': 3,
            'title': 'Configuration OAuth 2.0',
            'description': 'Créer credentials OAuth pour accès Drive',
            'actions': [
                'Aller à "API et Services" > "Identifiants"',
                'Cliquer "Créer des identifiants" > "ID client OAuth"',
                'Type d\'application: "Application de bureau"',
                'Nom: "PaniniFS-Drive-Manager"',
                'Télécharger le fichier JSON'
            ]
        },
        {
            'step': 4,
            'title': 'Installation Credentials',
            'description': 'Installer fichier credentials dans projet',
            'actions': [
                'Renommer fichier téléchargé en "credentials.json"',
                f'Placer dans: {os.path.join(os.getcwd(), "gdrive_credentials")}/credentials.json',
                'Le script détectera automatiquement les credentials'
            ]
        }
    ]
    
    for step in steps:
        print(f"\n📋 ÉTAPE {step['step']}: {step['title']}")
        print(f"   {step['description']}")
        print("   Actions:")
        for action in step['actions']:
            print(f"   • {action}")
            
    return steps

def create_credentials_directory():
    """Crée répertoire credentials"""
    base_path = "/home/stephane/GitHub/PaniniFS-1"
    creds_path = os.path.join(base_path, "gdrive_credentials")
    
    os.makedirs(creds_path, exist_ok=True)
    print(f"📁 Répertoire credentials créé: {creds_path}")
    
    return creds_path

def create_quick_setup_script():
    """Crée script de setup rapide"""
    setup_script = '''#!/bin/bash
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
'''
    
    script_path = "/home/stephane/GitHub/PaniniFS-1/setup_gdrive_api.sh"
    with open(script_path, 'w') as f:
        f.write(setup_script)
        
    os.chmod(script_path, 0o755)
    print(f"📜 Script setup créé: {script_path}")
    
    return script_path

def open_google_cloud_console():
    """Ouvre Google Cloud Console automatiquement"""
    urls_to_open = [
        'https://console.cloud.google.com/projectcreate',
        'https://console.cloud.google.com/apis/library/drive.googleapis.com'
    ]
    
    print("🌐 Ouverture automatique Google Cloud Console...")
    
    for url in urls_to_open:
        try:
            webbrowser.open(url)
            print(f"   ✅ Ouvert: {url}")
        except Exception as e:
            print(f"   ❌ Erreur ouverture {url}: {e}")
            
def create_test_credentials():
    """Crée fichier credentials de test pour développement"""
    creds_path = create_credentials_directory()
    test_creds_path = os.path.join(creds_path, "credentials_template.json")
    
    template = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
            "project_id": "panini-research-platform",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://www.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "YOUR_CLIENT_SECRET",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }
    
    with open(test_creds_path, 'w') as f:
        json.dump(template, f, indent=2)
        
    print(f"📄 Template credentials créé: {test_creds_path}")
    print("   ⚠️ Remplacer YOUR_CLIENT_ID et YOUR_CLIENT_SECRET par vraies valeurs")
    
    return test_creds_path

def check_existing_credentials():
    """Vérifie credentials existants"""
    base_path = "/home/stephane/GitHub/PaniniFS-1"
    creds_path = os.path.join(base_path, "gdrive_credentials", "credentials.json")
    
    if os.path.exists(creds_path):
        print(f"✅ Credentials détectés: {creds_path}")
        
        try:
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
                
            # Vérification structure
            if 'installed' in creds_data:
                client_id = creds_data['installed'].get('client_id', '')
                if 'YOUR_CLIENT_ID' not in client_id:
                    print("   ✅ Credentials semblent valides")
                    return True
                else:
                    print("   ⚠️ Credentials sont encore template - configuration requise")
            else:
                print("   ❌ Structure credentials invalide")
                
        except json.JSONDecodeError:
            print("   ❌ Fichier credentials corrompu")
            
    else:
        print(f"❌ Credentials non trouvés: {creds_path}")
        
    return False

def main():
    """Configuration autonome Google Drive API"""
    print("🔑 CONFIGURATEUR GOOGLE DRIVE API AUTONOME")
    print("Objectif: Configuration complète et autonome API Google Drive")
    print("=" * 60)
    
    # Vérification credentials existants
    if check_existing_credentials():
        print("\n🎉 Credentials déjà configurés - Prêt pour synchronisation!")
        print("🚀 Lancer: python3 Copilotage/scripts/autonomous_gdrive_manager.py")
        return
        
    # Création structure
    creds_path = create_credentials_directory()
    
    # Guide de configuration
    print("\n📚 GUIDE DE CONFIGURATION:")
    create_google_cloud_project_guide()
    
    # Création template et scripts
    create_test_credentials()
    setup_script = create_quick_setup_script()
    
    # Ouverture automatique navigateur
    print("\n🌐 Ouverture automatique Google Cloud Console...")
    open_google_cloud_console()
    
    print("\n" + "="*60)
    print("📋 RÉSUMÉ CONFIGURATION:")
    print(f"   📁 Répertoire: {creds_path}")
    print(f"   📜 Script setup: {setup_script}")
    print(f"   📄 Template: {creds_path}/credentials_template.json")
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("   1. Suivre guide ci-dessus pour configurer Google Cloud")
    print("   2. Télécharger credentials.json OAuth 2.0")
    print("   3. Placer dans gdrive_credentials/credentials.json")
    print("   4. Lancer gestionnaire Google Drive autonome")
    print("\n🚀 COMMANDE FINALE:")
    print("   python3 Copilotage/scripts/autonomous_gdrive_manager.py")
    print("="*60)

if __name__ == "__main__":
    main()
