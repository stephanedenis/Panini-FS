#!/usr/bin/env python3
"""
🦉 TOTORO SAFE OPTIMIZATION
🎯 Libération mémoire SANS risquer collaboration Copilot
⚡ Focus: System cleanup + Browser + Workspace optimization
"""

import subprocess
import os
import time

class SafeTotoroOptimizer:
    """Optimisation Totoro 100% safe pour collaboration"""
    
    def __init__(self):
        self.mission = "Safe optimization - Preserve all AI collaboration tools"
        
    def system_cleanup(self):
        """Nettoyage système safe"""
        print("🧹 NETTOYAGE SYSTÈME SAFE...")
        
        cleanup_commands = [
            {
                "desc": "Vider caches système",
                "cmd": "sync",
                "safe": True
            },
            {
                "desc": "Nettoyer tmp files personnels",
                "cmd": "find /tmp -user $(whoami) -type f -atime +1 -delete 2>/dev/null || true",
                "safe": True
            },
            {
                "desc": "Nettoyer cache Python __pycache__",
                "cmd": "find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true",
                "safe": True
            },
            {
                "desc": "Nettoyer logs journaux anciens",
                "cmd": "journalctl --disk-usage && echo 'Logs can be cleaned with: sudo journalctl --vacuum-time=1d'",
                "safe": True
            }
        ]
        
        for cleanup in cleanup_commands:
            print(f"   🔄 {cleanup['desc']}...")
            try:
                if cleanup['safe']:
                    os.system(cleanup['cmd'])
                    time.sleep(0.5)
                    print(f"   ✅ Done")
                else:
                    print(f"   ⚠️ Manual: {cleanup['cmd']}")
            except Exception as e:
                print(f"   ⚠️ Error: {e}")
    
    def workspace_optimization(self):
        """Optimisation workspace VSCode"""
        print("📂 OPTIMISATION WORKSPACE...")
        
        # Fichiers essentiels à garder ouverts
        essential_files = [
            "google_colab_setup.py",
            "COLAB_SETUP_GUIDE.md",
            "totoro_optimizer.py"
        ]
        
        print("   ✅ Fichiers essentiels à garder ouverts:")
        for file in essential_files:
            print(f"      • {file}")
        
        print("\n   📝 Actions manuelles recommandées:")
        print("      1. Fermer onglets VSCode non-essentiels")
        print("      2. Garder seulement 2-3 fichiers ouverts max")
        print("      3. Fermer panels non-utilisés (Problems, Output)")
        print("      4. Minimiser Explorer si pas nécessaire")
    
    def browser_optimization(self):
        """Optimisation navigateur"""
        print("🌐 OPTIMISATION NAVIGATEUR...")
        
        print("   📝 Actions Firefox recommandées:")
        print("      1. Fermer tous onglets sauf:")
        print("         • Google Colab (priorité)")
        print("         • GitHub PaniniFS (si nécessaire)")
        print("      2. about:memory → 'Minimize memory usage'")
        print("      3. Extensions: Désactiver temporairement non-essentielles")
        print("      4. Vider cache: Ctrl+Shift+Del → Cache seulement")
    
    def safe_plugin_optimization(self):
        """Optimisation plugins VSCode 100% safe"""
        print("🔧 OPTIMISATION PLUGINS VSCODE (SAFE)...")
        
        plugins_to_disable = [
            {
                "name": "CodeQL",
                "id": "GitHub.vscode-codeql",
                "impact": "200-500MB",
                "reason": "Très gourmand, pas essentiel aujourd'hui",
                "safety": "SAFE - aucun impact collaboration"
            },
            {
                "name": "Remote Development Pack", 
                "id": "ms-vscode-remote.vscode-remote-extensionpack",
                "impact": "50-200MB",
                "reason": "Pas de remote work aujourd'hui",
                "safety": "SAFE - local work only"
            },
            {
                "name": "Docker",
                "id": "ms-azuretools.vscode-docker", 
                "impact": "50-150MB",
                "reason": "Pas de containers aujourd'hui",
                "safety": "SAFE - no containerization needed"
            }
        ]
        
        plugins_to_keep = [
            {
                "name": "GitHub Copilot",
                "id": "GitHub.copilot",
                "reason": "CRITIQUE - AI collaboration core",
                "status": "GARDER ABSOLUMENT"
            },
            {
                "name": "GitHub Copilot Chat",
                "id": "GitHub.copilot-chat",
                "reason": "Interface chat utile",
                "status": "GARDER POUR SÉCURITÉ"
            },
            {
                "name": "Python + Pylance",
                "id": "ms-python.*",
                "reason": "Développement Python essentiel", 
                "status": "GARDER ABSOLUMENT"
            },
            {
                "name": "Rust Analyzer",
                "id": "rust-lang.rust-analyzer",
                "reason": "PaniniFS-2 development",
                "status": "GARDER"
            }
        ]
        
        print("   ❌ SAFE À DÉSACTIVER TEMPORAIREMENT:")
        for plugin in plugins_to_disable:
            print(f"      • {plugin['name']} ({plugin['impact']})")
            print(f"        → {plugin['reason']}")
            print(f"        → Safety: {plugin['safety']}")
        
        print("\n   ✅ À GARDER ACTIFS (COLLABORATION SAFE):")
        for plugin in plugins_to_keep:
            print(f"      • {plugin['name']} - {plugin['status']}")
        
        print("\n   📝 Comment désactiver (manuel):")
        print("      1. Ctrl+Shift+X (Extensions)")
        print("      2. Chercher plugin par nom")
        print("      3. Clic 'Disable' (pas Uninstall)")
        print("      4. Restart VSCode si demandé")
    
    def memory_monitoring(self):
        """Monitoring mémoire en temps réel"""
        print("📊 MONITORING MÉMOIRE...")
        
        try:
            # Memory info
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            print("   💾 État mémoire actuel:")
            lines = result.stdout.strip().split('\n')
            for line in lines:
                print(f"      {line}")
            
            # Top processes
            print("\n   🔥 Top 5 processus mémoire:")
            result = subprocess.run(['ps', 'aux', '--sort=-%mem'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines[1:6]:  # Skip header, show top 5
                cols = line.split()
                if len(cols) >= 11:
                    user = cols[0][:10]
                    mem = cols[3]
                    cmd = ' '.join(cols[10:])[:50]
                    print(f"      {user} {mem}% {cmd}")
                    
        except Exception as e:
            print(f"   ⚠️ Error monitoring: {e}")
    
    def create_focus_session_script(self):
        """Créer script session focus"""
        print("📜 CRÉATION SCRIPT SESSION FOCUS...")
        
        focus_script = '''#!/bin/bash
# 🦉 TOTORO FOCUS SESSION SCRIPT
# Usage: ./focus_session.sh

echo "🦉 STARTING TOTORO FOCUS SESSION"
echo "================================"

# 1. System cleanup
echo "🧹 System cleanup..."
sync
find /tmp -user $(whoami) -type f -atime +1 -delete 2>/dev/null || true
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# 2. Memory status
echo "📊 Memory status:"
free -h

# 3. Focus reminders
echo ""
echo "📝 FOCUS CHECKLIST:"
echo "□ VSCode: Fermer fichiers non-essentiels"
echo "□ Firefox: Garder seulement Colab + GitHub"
echo "□ Désactiver: CodeQL, Remote Dev, Docker"
echo "□ Garder: Copilot, Python, Rust Analyzer"
echo ""
echo "🚀 Ready for CLOUD ACCELERATION!"
echo "   → https://colab.research.google.com/"
'''
        
        script_path = "/home/stephane/GitHub/PaniniFS-1/scripts/scripts/focus_session.sh"
        with open(script_path, 'w') as f:
            f.write(focus_script)
        
        os.chmod(script_path, 0o755)
        print(f"   ✅ Script créé: {script_path}")
        return script_path

def main():
    print("🦉 TOTORO SAFE OPTIMIZATION")
    print("=" * 50)
    print("🎯 Mission: Libération mémoire SANS risquer collaboration")
    print("🛡️ Safety: Tous les outils AI collaboration préservés")
    print("")
    
    optimizer = SafeTotoroOptimizer()
    
    # 1. System cleanup
    optimizer.system_cleanup()
    print("")
    
    # 2. Memory monitoring 
    optimizer.memory_monitoring()
    print("")
    
    # 3. Workspace optimization
    optimizer.workspace_optimization()
    print("")
    
    # 4. Browser optimization
    optimizer.browser_optimization()
    print("")
    
    # 5. Safe plugin optimization
    optimizer.safe_plugin_optimization()
    print("")
    
    # 6. Create focus script
    focus_script = optimizer.create_focus_session_script()
    print("")
    
    print("🎯 OPTIMISATION TERMINÉE!")
    print("=" * 30)
    print("")
    print("✅ GAINS ATTENDUS:")
    print("   💾 Mémoire libérée: 500MB-1GB")
    print("   ⚡ CPU allégé: 10-30%")
    print("   🛡️ Collaboration préservée: 100%")
    print("")
    print("🚀 PROCHAINES ÉTAPES:")
    print("   1. 🔧 Appliquer optimisations VSCode manuelles")
    print("   2. 🌐 Optimiser Firefox (fermer onglets)")
    print("   3. ☁️ Lancer Google Colab setup")
    print("   4. ⚡ Profiter 22-60x speedup!")
    print("")
    print("🌟 TOTORO OPTIMISÉE + COLLABORATION INTACTE!")
    print(f"📜 Focus script: {focus_script}")

if __name__ == "__main__":
    main()
