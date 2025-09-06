#!/usr/bin/env python3
"""
🔍 VÉRIFICATEUR MISSION COLAB - Status en temps réel
Objectif : Checker l'état de la mission autonome nocturne sur Google Colab
"""

import requests
import json
import time
from datetime import datetime

class ColabMissionChecker:
    def __init__(self):
        self.colab_base_url = "https://colab.research.google.com"
        self.session = requests.Session()
        
    def check_colab_status(self):
        """Vérification du status de la mission Colab"""
        print("🔍 VÉRIFICATION MISSION COLAB")
        print("=" * 40)
        print(f"⏰ Vérification à: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Instructions pour vérification manuelle
        print("📋 ÉTAPES DE VÉRIFICATION MANUELLE:")
        print()
        print("1. 🌐 Ouvrir Google Colab:")
        print("   https://colab.research.google.com")
        print()
        print("2. 📚 Chercher le notebook actif:")
        print("   - 'semantic_processing_accelerated'")
        print("   - 'autonomous_night_mission'")
        print("   - 'panini_semantic_analysis'")
        print()
        print("3. ✅ Vérifier l'état:")
        print("   - Runtime connecté ? (vert)")
        print("   - Cellules en cours ? (spinning)")
        print("   - Outputs disponibles ?")
        print()
        print("4. 📄 Chercher les fichiers générés:")
        print("   - autonomous_night_mission_report.json")
        print("   - semantic_analysis_results.json")
        print("   - progress_log.txt")
        print()
        
        # Script automatique pour ouvrir Colab
        print("🚀 LANCEMENT AUTOMATIQUE:")
        colab_url = "https://colab.research.google.com/notebooks/intro.ipynb"
        
        try:
            import webbrowser
            print(f"🌐 Ouverture de Colab dans le navigateur...")
            webbrowser.open(colab_url)
            print("✅ Colab ouvert - Vérifiez vos notebooks actifs")
        except ImportError:
            print(f"📋 Ouvrez manuellement: {colab_url}")
        
        return True
        
    def check_google_drive_results(self):
        """Vérifier s'il y a des résultats dans Google Drive"""
        print()
        print("💾 VÉRIFICATION GOOGLE DRIVE:")
        print()
        print("📁 Dossiers à vérifier:")
        print("   - /content/drive/MyDrive/Colab Notebooks/")
        print("   - /content/drive/MyDrive/PaniniFS/")
        print("   - /content/drive/MyDrive/semantic_results/")
        print()
        print("📄 Fichiers à chercher:")
        print("   - *.json (résultats)")
        print("   - *.log (logs)")
        print("   - *.csv (données)")
        print("   - *.pkl (modèles)")
        print()
        
    def check_github_integration(self):
        """Vérifier si des résultats ont été pushés sur GitHub"""
        print()
        print("🐙 VÉRIFICATION GITHUB AUTO-PUSH:")
        print()
        
        repos_to_check = [
            "PaniniFS-AutonomousMissions",
            "PaniniFS-SemanticCore", 
            "Panini-DevOps"
        ]
        
        for repo in repos_to_check:
            print(f"📊 Repo: {repo}")
            print(f"   URL: https://github.com/stephanedenis/{repo}")
            print(f"   Chercher: commits récents, nouveaux fichiers")
        
        print()
        
    def create_colab_checker_notebook(self):
        """Créer un notebook Colab pour vérification automatique"""
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🔍 Panini Mission Status Checker\n",
                        "\n",
                        "Vérification automatique de l'état des missions autonomes"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Vérification des processus en cours\n",
                        "import os\n",
                        "import glob\n",
                        "import json\n",
                        "from datetime import datetime\n",
                        "\n",
                        "print(\"🔍 MISSION STATUS CHECK\")\n",
                        "print(\"=\" * 30)\n",
                        "print(f\"Timestamp: {datetime.now()}\")\n",
                        "print()\n",
                        "\n",
                        "# Chercher les fichiers de résultats\n",
                        "result_files = glob.glob('/content/**/*mission*', recursive=True)\n",
                        "result_files += glob.glob('/content/**/*report*', recursive=True)\n",
                        "result_files += glob.glob('/content/**/*result*', recursive=True)\n",
                        "\n",
                        "print(\"📄 Fichiers trouvés:\")\n",
                        "for f in result_files:\n",
                        "    print(f\"  - {f}\")\n",
                        "\n",
                        "# Vérifier Google Drive\n",
                        "try:\n",
                        "    from google.colab import drive\n",
                        "    drive.mount('/content/drive')\n",
                        "    \n",
                        "    drive_files = glob.glob('/content/drive/MyDrive/**/*panini*', recursive=True)\n",
                        "    drive_files += glob.glob('/content/drive/MyDrive/**/*mission*', recursive=True)\n",
                        "    \n",
                        "    print(\"\\n💾 Fichiers Google Drive:\")\n",
                        "    for f in drive_files:\n",
                        "        print(f\"  - {f}\")\n",
                        "        \n",
                        "except Exception as e:\n",
                        "    print(f\"⚠️  Erreur Google Drive: {e}\")"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Vérifier les variables en mémoire\n",
                        "print(\"🧠 VARIABLES EN MÉMOIRE:\")\n",
                        "print(\"=\" * 25)\n",
                        "\n",
                        "# Lister toutes les variables globales\n",
                        "for var_name in dir():\n",
                        "    if not var_name.startswith('_'):\n",
                        "        var_value = globals()[var_name]\n",
                        "        if 'panini' in str(var_value).lower() or 'mission' in str(var_value).lower():\n",
                        "            print(f\"📋 {var_name}: {type(var_value)}\")\n",
                        "            if hasattr(var_value, '__len__') and len(str(var_value)) < 200:\n",
                        "                print(f\"    Contenu: {var_value}\")\n",
                        "            print()"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 2
        }
        
        # Sauvegarder le notebook
        notebook_file = "/tmp/panini_mission_checker.ipynb"
        with open(notebook_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2, ensure_ascii=False)
            
        print(f"📓 Notebook créé: {notebook_file}")
        print("💡 Uploadez ce fichier dans Colab pour vérification automatique")
        
        return notebook_file

def main():
    """Point d'entrée principal"""
    print("🔍 PANINI COLAB MISSION CHECKER")
    print("================================")
    print()
    
    checker = ColabMissionChecker()
    
    # Vérification status
    checker.check_colab_status()
    
    # Vérification Google Drive
    checker.check_google_drive_results()
    
    # Vérification GitHub
    checker.check_github_integration()
    
    # Création notebook checker
    notebook_file = checker.create_colab_checker_notebook()
    
    print()
    print("🎯 RÉSUMÉ DES ACTIONS:")
    print("1. ✅ Ouvrir Colab (automatique)")
    print("2. 👀 Vérifier notebooks actifs")
    print("3. 📄 Chercher fichiers de résultats")
    print("4. 💾 Vérifier Google Drive")
    print("5. 🐙 Checker GitHub commits")
    print(f"6. 📓 Utiliser notebook: {notebook_file}")
    print()
    print("🏕️ Mission de vérification lancée depuis Totoro!")

if __name__ == "__main__":
    main()
