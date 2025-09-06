#!/usr/bin/env python3
"""
🔧 VSCODE EXTENSIONS MANAGER AUTOMATIQUE
🎯 Script pour désactiver/réactiver extensions via CLI et config
⚡ Optimisation automatique pour session focus
"""

import json
import subprocess
import os
import shutil
from typing import List, Dict, Any

class VSCodeExtensionManager:
    """Gestionnaire automatique extensions VSCode"""
    
    def __init__(self):
        self.vscode_extensions_dir = os.path.expanduser("~/.vscode/extensions")
        self.disabled_extensions_file = "/home/stephane/GitHub/PaniniFS-1/scripts/scripts/disabled_extensions.json"
        
    def list_installed_extensions(self) -> List[str]:
        """Lister extensions installées"""
        print("📋 LISTING EXTENSIONS INSTALLÉES...")
        
        try:
            result = subprocess.run(['code', '--list-extensions'], 
                                  capture_output=True, text=True, check=True)
            extensions = result.stdout.strip().split('\n')
            extensions = [ext for ext in extensions if ext.strip()]
            
            print(f"   ✅ {len(extensions)} extensions trouvées")
            return extensions
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erreur listing extensions: {e}")
            return []
        except FileNotFoundError:
            print("   ❌ Command 'code' not found - VSCode CLI pas installé")
            return []
    
    def create_focus_session_config(self) -> Dict[str, Any]:
        """Configuration session focus"""
        
        config = {
            "extensions_to_disable": [
                {
                    "id": "github.copilot-chat",
                    "name": "GitHub Copilot Chat",
                    "reason": "Interface chat gourmande, Copilot core suffit",
                    "priority": "MEDIUM"
                },
                {
                    "id": "GitHub.vscode-codeql",
                    "name": "CodeQL",
                    "reason": "Très gourmand CPU/Memory (200-500MB)",
                    "priority": "HIGH"
                },
                {
                    "id": "ms-vscode-remote.vscode-remote-extensionpack",
                    "name": "Remote Development Pack", 
                    "reason": "Pas de remote work today",
                    "priority": "MEDIUM"
                },
                {
                    "id": "ms-azuretools.vscode-docker",
                    "name": "Docker",
                    "reason": "Pas de containers today",
                    "priority": "LOW"
                },
                {
                    "id": "ms-azuretools.vscode-azureresourcegroups",
                    "name": "Azure Tools",
                    "reason": "Focus Google Cloud today",
                    "priority": "LOW"
                }
            ],
            
            "extensions_to_keep": [
                {
                    "id": "github.copilot",
                    "name": "GitHub Copilot",
                    "reason": "CRITIQUE - AI collaboration core (suggestions inline)",
                    "priority": "CRITICAL"
                },
                {
                    "id": "ms-python.python",
                    "name": "Python",
                    "reason": "Development core",
                    "priority": "CRITICAL"
                },
                {
                    "id": "ms-python.vscode-pylance",
                    "name": "Pylance",
                    "reason": "Python intelligence",
                    "priority": "CRITICAL"
                },
                {
                    "id": "rust-lang.rust-analyzer",
                    "name": "Rust Analyzer", 
                    "reason": "PaniniFS-2 development",
                    "priority": "HIGH"
                },
                {
                    "id": "eamodio.gitlens",
                    "name": "GitLens",
                    "reason": "Git workflow",
                    "priority": "MEDIUM"
                }
            ]
        }
        
        return config
    
    def disable_extensions_cli(self, extensions_to_disable: List[str]) -> bool:
        """Désactiver extensions via CLI"""
        print("🔧 DÉSACTIVATION EXTENSIONS VIA CLI...")
        
        success = True
        disabled = []
        
        for ext_id in extensions_to_disable:
            try:
                print(f"   🔄 Désactivation {ext_id}...")
                # Utiliser --wait et --new-window=false pour éviter nouvelles instances
                result = subprocess.run(['code', '--disable-extension', ext_id, '--wait', '--reuse-window'],
                                      capture_output=True, text=True, check=True)
                print(f"   ✅ {ext_id} désactivée")
                disabled.append(ext_id)
                
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Erreur désactivation {ext_id}: {e}")
                success = False
            except FileNotFoundError:
                print("   ❌ VSCode CLI non disponible")
                return False
        
        # Sauvegarder liste désactivées pour restore
        if disabled:
            with open(self.disabled_extensions_file, 'w') as f:
                json.dump(disabled, f, indent=2)
            print(f"   💾 Liste sauvée: {self.disabled_extensions_file}")
        
        return success
    
    def enable_extensions_cli(self, extensions_to_enable: List[str]) -> bool:
        """Réactiver extensions via CLI"""
        print("🔄 RÉACTIVATION EXTENSIONS VIA CLI...")
        
        success = True
        
        for ext_id in extensions_to_enable:
            try:
                print(f"   🔄 Réactivation {ext_id}...")
                result = subprocess.run(['code', '--enable-extension', ext_id, '--wait', '--reuse-window'],
                                      capture_output=True, text=True, check=True)
                print(f"   ✅ {ext_id} réactivée")
                
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Erreur réactivation {ext_id}: {e}")
                success = False
        
        return success
    
    def create_workspace_settings(self) -> str:
        """Créer settings workspace optimisé"""
        print("⚙️ CRÉATION SETTINGS WORKSPACE OPTIMISÉ...")
        
        optimized_settings = {
            "files.watcherExclude": {
                "**/node_modules/**": True,
                "**/target/**": True,
                "**/.git/**": True,
                "**/venv/**": True,
                "**/__pycache__/**": True,
                "**/scripts/scripts/**/*.json": True
            },
            "search.exclude": {
                "**/node_modules": True,
                "**/target": True,
                "**/venv": True,
                "**/__pycache__": True,
                "**/*.json": True
            },
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True
            },
            "python.analysis.autoImportCompletions": False,
            "python.analysis.indexing": False,
            "editor.hover.delay": 1000,
            "editor.quickSuggestions": {
                "other": "off",
                "comments": "off", 
                "strings": "off"
            },
            "extensions.autoUpdate": False,
            "extensions.autoCheckUpdates": False,
            "telemetry.telemetryLevel": "off",
            "workbench.enableExperiments": False
        }
        
        workspace_dir = "/home/stephane/GitHub/PaniniFS-1/.vscode"
        os.makedirs(workspace_dir, exist_ok=True)
        
        settings_file = os.path.join(workspace_dir, "settings.json")
        
        with open(settings_file, 'w') as f:
            json.dump(optimized_settings, f, indent=2)
        
        print(f"   ✅ Settings sauvés: {settings_file}")
        return settings_file
    
    def start_focus_session(self):
        """Démarrer session focus complète"""
        print("🚀 DÉMARRAGE SESSION FOCUS...")
        
        # 1. Lister extensions
        installed = self.list_installed_extensions()
        
        # 2. Configuration focus
        config = self.create_focus_session_config()
        
        # 3. Identifier extensions à désactiver (qui sont installées)
        to_disable = []
        for ext_config in config["extensions_to_disable"]:
            ext_id = ext_config["id"]
            if ext_id in installed:
                to_disable.append(ext_id)
                print(f"   🎯 À désactiver: {ext_config['name']} ({ext_config['reason']})")
        
        # 4. Vérifier extensions critiques présentes
        critical_present = []
        for ext_config in config["extensions_to_keep"]:
            if ext_config["priority"] == "CRITICAL" and ext_config["id"] in installed:
                critical_present.append(ext_config["name"])
        
        print(f"   ✅ Extensions critiques présentes: {len(critical_present)}")
        for ext in critical_present:
            print(f"      • {ext}")
        
        if len(critical_present) < 3:  # Copilot + Python + Pylance
            print("   ⚠️ ATTENTION: Extensions critiques manquantes!")
            return False
        
        # 5. Désactiver extensions
        if to_disable:
            success = self.disable_extensions_cli(to_disable)
            if not success:
                print("   ⚠️ Désactivation partielle seulement")
        else:
            print("   ✅ Aucune extension à désactiver trouvée")
        
        # 6. Créer settings optimisés
        settings_file = self.create_workspace_settings()
        
        print("\n🎯 SESSION FOCUS CONFIGURÉE!")
        print(f"   🔧 Extensions désactivées: {len(to_disable)}")
        print(f"   ⚙️ Settings optimisés: {settings_file}")
        
        return True
    
    def restore_session(self):
        """Restaurer session normale"""
        print("🔄 RESTAURATION SESSION NORMALE...")
        
        # Lire liste extensions désactivées
        if os.path.exists(self.disabled_extensions_file):
            with open(self.disabled_extensions_file, 'r') as f:
                disabled_extensions = json.load(f)
            
            if disabled_extensions:
                success = self.enable_extensions_cli(disabled_extensions)
                if success:
                    os.remove(self.disabled_extensions_file)
                    print("   ✅ Toutes extensions restaurées")
                else:
                    print("   ⚠️ Restauration partielle")
            else:
                print("   ✅ Aucune extension à restaurer")
        else:
            print("   ✅ Aucune session focus précédente trouvée")
    
    def status_check(self):
        """Vérifier statut actuel"""
        print("📊 STATUT EXTENSIONS ACTUEL...")
        
        installed = self.list_installed_extensions()
        config = self.create_focus_session_config()
        
        print("\n   🔍 État extensions critiques:")
        for ext_config in config["extensions_to_keep"]:
            if ext_config["priority"] == "CRITICAL":
                status = "✅ PRÉSENTE" if ext_config["id"] in installed else "❌ MANQUANTE"
                print(f"      • {ext_config['name']}: {status}")
        
        print("\n   🔍 État extensions à optimiser:")
        for ext_config in config["extensions_to_disable"]:
            status = "🔄 INSTALLÉE" if ext_config["id"] in installed else "✅ ABSENTE"
            print(f"      • {ext_config['name']}: {status}")

def main():
    print("🔧 VSCODE EXTENSIONS MANAGER AUTOMATIQUE")
    print("=" * 50)
    print("🎯 Optimisation extensions pour session focus")
    print("🛡️ Préservation outils collaboration critiques")
    print("")
    
    manager = VSCodeExtensionManager()
    
    import sys
    
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        
        if action == "focus":
            print("🚀 MODE: Focus Session")
            success = manager.start_focus_session()
            if success:
                print("\n🌟 SESSION FOCUS ACTIVÉE!")
                print("   💾 Mémoire économisée: 300-800MB attendu")
                print("   🔄 Pour restaurer: python3 vscode_manager.py restore")
            else:
                print("\n❌ Erreur activation focus session")
                
        elif action == "restore":
            print("🔄 MODE: Restore Session")
            manager.restore_session()
            print("\n🌟 SESSION RESTAURÉE!")
            
        elif action == "status":
            print("📊 MODE: Status Check")
            manager.status_check()
            
        else:
            print(f"❌ Action inconnue: {action}")
            print("Usage: python3 vscode_manager.py [focus|restore|status]")
    else:
        print("📊 MODE: Status Check par défaut")
        manager.status_check()
        print("\n🚀 ACTIONS DISPONIBLES:")
        print("   • python3 vscode_manager.py focus    - Activer session focus")
        print("   • python3 vscode_manager.py restore  - Restaurer session normale")
        print("   • python3 vscode_manager.py status   - Vérifier statut")

if __name__ == "__main__":
    main()
