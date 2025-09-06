#!/usr/bin/env python3
"""
🦉 TOTORO OPTIMIZATION PROTOCOL
🎯 Libération mémoire + processus + VSCode plugins optimization
⚡ Maximum focus pour mission cloud acceleration
"""

import subprocess
import json
import os
from typing import List, Dict, Any

class TotoroOptimizer:
    """Optimiseur performance Totoro pour mission focus"""
    
    def __init__(self):
        self.mission = "Cloud acceleration setup - Maximum focus"
        self.target_memory_free = "4GB+"
        self.target_cpu_free = "30%+"
        
    def analyze_memory_usage(self) -> Dict[str, Any]:
        """Analyse utilisation mémoire actuelle"""
        print("💾 ANALYSE UTILISATION MÉMOIRE...")
        
        # Get memory info
        try:
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            memory_lines = result.stdout.strip().split('\n')
            
            # Parse memory info
            mem_line = memory_lines[1].split()
            swap_line = memory_lines[2].split() if len(memory_lines) > 2 else None
            
            memory_analysis = {
                "total": mem_line[1],
                "used": mem_line[2], 
                "free": mem_line[3],
                "available": mem_line[6] if len(mem_line) > 6 else mem_line[3],
                "swap_used": swap_line[2] if swap_line else "0",
                "memory_pressure": "HIGH" if "G" in mem_line[2] and float(mem_line[2][:-1]) > 8 else "NORMAL"
            }
            
        except Exception as e:
            memory_analysis = {"error": str(e)}
            
        return memory_analysis
    
    def identify_unnecessary_processes(self) -> List[Dict[str, Any]]:
        """Identifier processus non-essentiels pour la mission"""
        print("🔍 IDENTIFICATION PROCESSUS NON-ESSENTIELS...")
        
        unnecessary_candidates = [
            {
                "pattern": "firefox.*backup",
                "description": "Firefox avec pages backup",
                "priority": "HIGH",
                "memory_impact": "500MB-2GB",
                "action": "Close backup tabs, keep only essential"
            },
            {
                "pattern": "discord|slack|teams",
                "description": "Applications communication",
                "priority": "MEDIUM", 
                "memory_impact": "200-800MB",
                "action": "Close pendant focus session"
            },
            {
                "pattern": "thunderbird|evolution",
                "description": "Clients email",
                "priority": "MEDIUM",
                "memory_impact": "100-400MB", 
                "action": "Close pendant mission"
            },
            {
                "pattern": "spotify|vlc|music",
                "description": "Applications multimédia",
                "priority": "LOW",
                "memory_impact": "50-200MB",
                "action": "Close si nécessaire"
            },
            {
                "pattern": "libreoffice|gimp|inkscape",
                "description": "Applications bureautique/graphique",
                "priority": "HIGH",
                "memory_impact": "200MB-1GB",
                "action": "Close si ouvertes"
            }
        ]
        
        # Check which are actually running
        running_candidates = []
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = result.stdout.lower()
            
            for candidate in unnecessary_candidates:
                pattern = candidate["pattern"].lower()
                if any(p in processes for p in pattern.split("|")):
                    running_candidates.append(candidate)
                    
        except Exception as e:
            print(f"Error checking processes: {e}")
            
        return running_candidates
    
    def create_vscode_optimization_plan(self) -> Dict[str, Any]:
        """Plan optimisation VSCode plugins"""
        print("🔧 CRÉATION PLAN OPTIMISATION VSCODE...")
        
        optimization_plan = {
            "plugins_to_disable_temporarily": [
                {
                    "name": "GitHub Copilot Chat",
                    "id": "GitHub.copilot-chat", 
                    "reason": "Sollicitation continue events, on garde juste Copilot core",
                    "memory_impact": "100-300MB",
                    "priority": "MEDIUM"
                },
                {
                    "name": "CodeQL", 
                    "id": "GitHub.vscode-codeql",
                    "reason": "Très gourmand CPU/Memory, pas essentiel aujourd'hui",
                    "memory_impact": "200-500MB",
                    "priority": "HIGH"
                },
                {
                    "name": "Remote Development Pack",
                    "id": "ms-vscode-remote.vscode-remote-extensionpack",
                    "reason": "Pas de remote work aujourd'hui",
                    "memory_impact": "50-200MB", 
                    "priority": "MEDIUM"
                },
                {
                    "name": "Docker",
                    "id": "ms-azuretools.vscode-docker",
                    "reason": "Pas de containerization aujourd'hui",
                    "memory_impact": "50-150MB",
                    "priority": "LOW"
                },
                {
                    "name": "Azure Tools",
                    "id": "ms-azuretools.vscode-azureresourcegroups",
                    "reason": "Focus Google Cloud aujourd'hui",
                    "memory_impact": "30-100MB",
                    "priority": "LOW"
                }
            ],
            
            "plugins_to_keep_active": [
                {
                    "name": "GitHub Copilot",
                    "id": "GitHub.copilot",
                    "reason": "ESSENTIEL pour collaboration AI",
                    "priority": "CRITICAL"
                },
                {
                    "name": "Python", 
                    "id": "ms-python.python",
                    "reason": "Développement Python core mission",
                    "priority": "CRITICAL"
                },
                {
                    "name": "Pylance",
                    "id": "ms-python.vscode-pylance", 
                    "reason": "Intelligence Python nécessaire",
                    "priority": "HIGH"
                },
                {
                    "name": "Rust Analyzer",
                    "id": "rust-lang.rust-analyzer",
                    "reason": "PaniniFS-2 Rust development",
                    "priority": "HIGH"
                },
                {
                    "name": "GitLens",
                    "id": "eamodio.gitlens",
                    "reason": "Git workflow essentiel",
                    "priority": "MEDIUM"
                }
            ],
            
            "vscode_settings_optimization": {
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
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/.pyc": True
                },
                "python.analysis.autoImportCompletions": False,
                "python.analysis.indexing": False,
                "editor.hover.delay": 1000,
                "editor.quickSuggestions": {
                    "other": False,
                    "comments": False,
                    "strings": False
                }
            }
        }
        
        return optimization_plan
    
    def generate_cleanup_commands(self) -> Dict[str, List[str]]:
        """Générer commandes nettoyage système"""
        print("🧹 GÉNÉRATION COMMANDES NETTOYAGE...")
        
        commands = {
            "memory_cleanup": [
                "# Vider caches système",
                "sudo sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'",
                "",
                "# Nettoyer tmp files",
                "sudo rm -rf /tmp/* 2>/dev/null || true",
                "",
                "# Nettoyer journaux anciens", 
                "sudo journalctl --vacuum-time=1d",
                "",
                "# Nettoyer cache Python",
                "find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true"
            ],
            
            "browser_optimization": [
                "# Firefox: Fermer onglets backup/inutiles",
                "# 1. Ouvrir Firefox",
                "# 2. Fermer tous onglets sauf essentiels",
                "# 3. about:memory → Minimize memory usage",
                "# 4. Garder seulement: Google Colab + GitHub"
            ],
            
            "process_management": [
                "# Vérifier processus gourmands",
                "ps aux --sort=-%cpu | head -10",
                "",
                "# Kill processus inutiles identifiés", 
                "# (commands will be generated based on analysis)"
            ]
        }
        
        return commands
    
    def create_focus_workspace_config(self) -> Dict[str, Any]:
        """Configuration workspace focus mission"""
        print("🎯 CRÉATION CONFIG WORKSPACE FOCUS...")
        
        focus_config = {
            "workspace_name": "PaniniFS_Cloud_Acceleration_Focus",
            "focus_mode_settings": {
                "zenMode.centerLayout": False,
                "zenMode.fullScreen": False,
                "zenMode.hideTabs": False,
                "workbench.activityBar.visible": True,
                "workbench.statusBar.visible": True,
                "breadcrumbs.enabled": True,
                "editor.minimap.enabled": False,
                "explorer.decorations.badges": False,
                "explorer.decorations.colors": False
            },
            
            "files_to_keep_open": [
                "google_colab_setup.py",
                "COLAB_SETUP_GUIDE.md", 
                "totoro_resource_management.py"
            ],
            
            "files_to_close": [
                "All other Python files",
                "Documentation files not essential",
                "Test files",
                "Config files not needed"
            ],
            
            "terminal_optimization": {
                "keep_terminals": 2,
                "purpose": ["Main work terminal", "Monitoring terminal"],
                "close_idle_terminals": True
            }
        }
        
        return focus_config

def main():
    print("🦉 TOTORO OPTIMIZATION PROTOCOL")
    print("=" * 50) 
    print("🎯 Mission: Cloud acceleration maximum focus")
    print("⚡ Objectif: Libération mémoire + CPU + VSCode optimization")
    print("")
    
    optimizer = TotoroOptimizer()
    
    # Analyse mémoire
    memory_analysis = optimizer.analyze_memory_usage()
    print("💾 ANALYSE MÉMOIRE ACTUELLE:")
    if "error" not in memory_analysis:
        print(f"   📊 Total: {memory_analysis['total']}")
        print(f"   📈 Utilisée: {memory_analysis['used']}")
        print(f"   🟢 Disponible: {memory_analysis['available']}")
        print(f"   ⚠️ Pression: {memory_analysis['memory_pressure']}")
    
    # Processus non-essentiels
    unnecessary = optimizer.identify_unnecessary_processes()
    print(f"\n🔍 PROCESSUS NON-ESSENTIELS DÉTECTÉS:")
    if unnecessary:
        for i, proc in enumerate(unnecessary, 1):
            print(f"   {i}. {proc['description']}")
            print(f"      → Impact: {proc['memory_impact']}")
            print(f"      → Action: {proc['action']}")
            print(f"      → Priorité: {proc['priority']}")
    else:
        print("   ✅ Aucun processus gourmand non-essentiel détecté")
    
    # Plan optimisation VSCode
    vscode_plan = optimizer.create_vscode_optimization_plan()
    print(f"\n🔧 PLAN OPTIMISATION VSCODE:")
    
    to_disable = vscode_plan["plugins_to_disable_temporarily"]
    print(f"   ⏸️ Plugins à désactiver temporairement ({len(to_disable)}):")
    for plugin in to_disable:
        name = plugin["name"]
        impact = plugin["memory_impact"]
        priority = plugin["priority"]
        print(f"      • {name} ({impact}) - {priority}")
    
    to_keep = vscode_plan["plugins_to_keep_active"]
    print(f"\n   ✅ Plugins à garder actifs ({len(to_keep)}):")
    for plugin in to_keep:
        name = plugin["name"]
        priority = plugin["priority"]
        print(f"      • {name} - {priority}")
    
    # Commandes nettoyage
    commands = optimizer.generate_cleanup_commands()
    print(f"\n🧹 COMMANDES NETTOYAGE SYSTÈME:")
    
    memory_cmds = commands["memory_cleanup"]
    print(f"   💾 Nettoyage mémoire:")
    for cmd in memory_cmds[:3]:  # Show first few
        if cmd.strip() and not cmd.startswith("#"):
            print(f"      → {cmd}")
    
    # Configuration focus
    focus_config = optimizer.create_focus_workspace_config()
    print(f"\n🎯 CONFIGURATION WORKSPACE FOCUS:")
    
    files_open = focus_config["files_to_keep_open"]
    print(f"   📂 Fichiers à garder ouverts ({len(files_open)}):")
    for file in files_open:
        print(f"      • {file}")
    
    terminal_config = focus_config["terminal_optimization"]
    terminals_keep = terminal_config["keep_terminals"]
    print(f"\n   💻 Terminals à garder: {terminals_keep}")
    
    # Sauvegarde configuration
    timestamp = "20250817_focus"
    
    complete_optimization = {
        "memory_analysis": memory_analysis,
        "unnecessary_processes": unnecessary,
        "vscode_optimization": vscode_plan,
        "cleanup_commands": commands,
        "focus_configuration": focus_config,
        "mission_metadata": {
            "created": timestamp,
            "mission": optimizer.mission,
            "target_memory": optimizer.target_memory_free,
            "target_cpu": optimizer.target_cpu_free
        }
    }
    
    config_path = f"/home/stephane/GitHub/PaniniFS-1/scripts/scripts/totoro_optimization_{timestamp}.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(complete_optimization, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 CONFIGURATION SAUVEGARDÉE:")
    print(f"   📁 {config_path.split('/')[-1]}")
    
    print(f"\n🚀 ACTIONS IMMÉDIATES RECOMMANDÉES:")
    print(f"1. 🔧 VSCode: Désactiver plugins non-essentiels")
    print(f"2. 🧹 Système: Nettoyer caches et tmp files")
    print(f"3. 🌐 Firefox: Fermer onglets backup, garder Colab")
    print(f"4. 📂 VSCode: Fermer fichiers non-essentiels")
    print(f"5. 💻 Terminals: Garder seulement 2 actifs")
    
    print(f"\n🎯 RÉSULTAT ATTENDU:")
    print(f"✅ Mémoire libérée: 1-3GB")
    print(f"⚡ CPU libéré: 20-40%")
    print(f"🦉 Totoro optimisée pour mission cloud!")
    
    print(f"\n🌟 TOTORO SERA UNE MACHINE DE GUERRE FOCALISÉE!")

if __name__ == "__main__":
    main()
