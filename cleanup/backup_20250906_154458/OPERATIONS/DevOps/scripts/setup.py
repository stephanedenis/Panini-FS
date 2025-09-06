#!/usr/bin/env python3
"""
Script de configuration pour les outils d'analyse autonome
Installe les dépendances et configure l'environnement
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Installe les dépendances Python nécessaires"""
    dependencies = [
        'tomllib',  # Pour parser les fichiers Cargo.toml (Python 3.11+)
        'walkdir',  # Alternative: utiliser os.walk intégré
        'pyyaml',   # Pour parser les fichiers YAML
    ]
    
    # Pour Python < 3.11, utiliser tomli au lieu de tomllib
    if sys.version_info < (3, 11):
        dependencies.append('tomli')
    
    print("📦 Installation des dépendances Python...")
    
    for dep in dependencies:
        try:
            if dep == 'tomllib' and sys.version_info >= (3, 11):
                # tomllib est intégré dans Python 3.11+
                continue
            
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✅ {dep} installé")
        except subprocess.CalledProcessError:
            print(f"⚠️  Impossible d'installer {dep}, continuons...")
        except Exception as e:
            print(f"❌ Erreur lors de l'installation de {dep}: {e}")

def create_config_file():
    """Crée un fichier de configuration pour les scripts"""
    config = {
        'copilotage_path': '~/Copilotage',
        'pensine_path': '~/GitHub/Pensine',
        'panini_fs_path': '~/GitHub/PaniniFS-1',
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'max_files_per_type': 10,
        'interesting_extensions': [
            '.py', '.rs', '.js', '.ts', '.cpp', '.c', '.h', '.java', '.go',
            '.json', '.yaml', '.yml', '.toml', '.md', '.txt', '.html', '.css'
        ]
    }
    
    config_path = Path(__file__).parent / 'config.json'
    
    import json
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"📝 Fichier de configuration créé: {config_path}")

def check_environment():
    """Vérifie que l'environnement est correct"""
    print("🔍 Vérification de l'environnement...")
    
    # Vérifier Python
    print(f"Python version: {sys.version}")
    
    # Vérifier les chemins importants
    home = Path.home()
    paths_to_check = [
        home / 'Copilotage',
        home / 'GitHub' / 'PaniniFS-1',
        home / 'GitHub' / 'Pensine'
    ]
    
    for path in paths_to_check:
        if path.exists():
            print(f"✅ {path} existe")
        else:
            print(f"⚠️  {path} n'existe pas")
    
    # Vérifier git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(f"✅ Git disponible: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Git n'est pas installé")

def main():
    """Fonction principale de configuration"""
    print("🔧 CONFIGURATION DES OUTILS D'ANALYSE AUTONOME")
    print("=" * 50)
    
    # Vérifier l'environnement
    check_environment()
    
    print()
    # Installer les dépendances
    install_dependencies()
    
    print()
    # Créer le fichier de configuration
    create_config_file()
    
    print()
    print("✅ Configuration terminée!")
    print()
    print("🚀 Pour lancer l'analyse autonome:")
    print("   ./run_analysis.sh")
    print()
    print("📋 Ou individuellement:")
    print("   python3 analyze_preferences.py")
    print("   python3 collect_samples.py")
    print("   python3 autonomous_analyzer.py")

if __name__ == "__main__":
    main()
