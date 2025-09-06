#!/usr/bin/env python3
"""
🔧 VSCODE SETTINGS FIXER
🎯 Corriger settings pour éviter nouvelles instances intempestives
⚡ Fix problème GitHub auth + CLI operations
"""

import json
import os

def fix_vscode_settings():
    """Corriger settings VSCode pour éviter nouvelles instances"""
    print("🔧 CORRECTION SETTINGS VSCODE...")
    
    # Settings utilisateur global
    user_settings_dir = os.path.expanduser("~/.config/Code/User")
    user_settings_file = os.path.join(user_settings_dir, "settings.json")
    
    # Settings workspace local
    workspace_settings_dir = "/home/stephane/GitHub/PaniniFS-1/.vscode"
    workspace_settings_file = os.path.join(workspace_settings_dir, "settings.json")
    
    # Settings anti-nouvelles-instances
    anti_instance_settings = {
        # Empêcher nouvelles fenêtres intempestives
        "window.openFoldersInNewWindow": "off",
        "window.openFilesInNewWindow": "off", 
        "workbench.startupEditor": "none",
        
        # GitHub auth settings
        "git.openRepositoryInParentFolders": "never",
        "git.autoRepositoryDetection": False,
        "github.gitAuthentication": False,
        "git.terminalAuthentication": False,
        
        # CLI behavior
        "extensions.autoUpdate": False,
        "extensions.autoCheckUpdates": False,
        "update.mode": "none",
        
        # Performance settings focus
        "files.watcherExclude": {
            "**/node_modules/**": True,
            "**/target/**": True,
            "**/.git/**": True,
            "**/venv/**": True,
            "**/__pycache__/**": True
        },
        "search.exclude": {
            "**/node_modules": True,
            "**/target": True,
            "**/venv": True,
            "**/__pycache__": True
        },
        "editor.quickSuggestions": {
            "other": "off",
            "comments": "off",
            "strings": "off"
        },
        "editor.hover.delay": 1000,
        "python.analysis.autoImportCompletions": False,
        "telemetry.telemetryLevel": "off"
    }
    
    # Appliquer aux settings workspace (priorité)
    os.makedirs(workspace_settings_dir, exist_ok=True)
    
    existing_workspace_settings = {}
    if os.path.exists(workspace_settings_file):
        try:
            with open(workspace_settings_file, 'r') as f:
                existing_workspace_settings = json.load(f)
        except:
            existing_workspace_settings = {}
    
    # Merger avec settings existants
    existing_workspace_settings.update(anti_instance_settings)
    
    with open(workspace_settings_file, 'w') as f:
        json.dump(existing_workspace_settings, f, indent=2)
    
    print(f"   ✅ Workspace settings: {workspace_settings_file}")
    
    # Info pour settings utilisateur (optionnel)
    print(f"\n📝 SETTINGS UTILISATEUR RECOMMANDÉS:")
    print(f"   📁 Fichier: {user_settings_file}")
    print(f"   🔧 Ajouter ces settings pour éviter nouvelles instances:")
    
    critical_settings = {
        "window.openFoldersInNewWindow": "off",
        "window.openFilesInNewWindow": "off",
        "github.gitAuthentication": False,
        "extensions.autoUpdate": False
    }
    
    for key, value in critical_settings.items():
        print(f'      "{key}": {json.dumps(value)}')
    
    return workspace_settings_file

def create_manual_extension_toggle():
    """Créer script toggle manuel extensions sans CLI"""
    print("\n🛠️ CRÉATION SCRIPT TOGGLE MANUEL...")
    
    manual_script = '''#!/bin/bash
# 🔧 MANUAL EXTENSION TOGGLE SCRIPT
# Alternative au CLI VSCode pour éviter nouvelles instances

echo "🔧 MANUAL EXTENSION MANAGEMENT"
echo "================================"

echo "📝 EXTENSIONS À DÉSACTIVER POUR FOCUS:"
echo "   1. Copilot Chat (github.copilot-chat)"
echo "   2. Remote Development Pack"  
echo "   3. Docker"
echo "   4. Azure Tools"
echo ""

echo "📋 MÉTHODE MANUELLE (RECOMMANDÉE):"
echo "   1. Ctrl+Shift+X (ouvrir Extensions)"
echo "   2. Chercher extension par nom"
echo "   3. Clic bouton 'Disable' (pas Uninstall)"
echo "   4. Répéter pour chaque extension"
echo ""

echo "✅ EXTENSIONS À GARDER ACTIVES:"
echo "   • GitHub Copilot (CRITIQUE)"
echo "   • Python + Pylance (CRITIQUE)"
echo "   • Rust Analyzer"
echo "   • GitLens"
echo ""

echo "💾 GAIN MÉMOIRE ATTENDU: 300-800MB"
echo "🎯 Après désactivation manuelle → Ready for Colab!"
'''
    
    manual_script_path = "/home/stephane/GitHub/PaniniFS-1/scripts/scripts/manual_extension_toggle.sh"
    with open(manual_script_path, 'w') as f:
        f.write(manual_script)
    
    os.chmod(manual_script_path, 0o755)
    print(f"   ✅ Script créé: {manual_script_path}")
    
    return manual_script_path

def main():
    print("🔧 VSCODE SETTINGS FIXER")
    print("=" * 30)
    print("🎯 Corriger problème nouvelles instances")
    print("⚡ Optimisation anti-interruption")
    print("")
    
    # 1. Fix settings
    settings_file = fix_vscode_settings()
    
    # 2. Script manuel alternatif
    manual_script = create_manual_extension_toggle()
    
    print(f"\n🎯 PROBLÈME NOUVELLES INSTANCES CORRIGÉ!")
    print(f"✅ Settings workspace: Optimisés")
    print(f"🛠️ Script manuel: Disponible")
    
    print(f"\n📝 RECOMMANDATIONS:")
    print(f"1. 🔄 Redémarrer VSCode pour appliquer settings")
    print(f"2. 🛠️ Utiliser méthode manuelle pour extensions:")
    print(f"   → Ctrl+Shift+X → Disable extensions une par une")
    print(f"3. ✅ Éviter CLI VSCode pour extensions")
    print(f"4. 🚀 Focus sur Google Colab setup!")
    
    print(f"\n🌟 TOTORO SERA PLUS STABLE!")

if __name__ == "__main__":
    main()
