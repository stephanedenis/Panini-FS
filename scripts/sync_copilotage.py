#!/usr/bin/env python3
"""
Script de synchronisation automatique de la configuration copilotage.

Synchronise la configuration partagée depuis copilotage/shared vers tous les modules
et met à jour les submodules.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import yaml

ROOT = Path(__file__).parent.parent
COPILOTAGE_SHARED = ROOT / "copilotage" / "shared"
MODULES_DIR = ROOT / "modules"

def run_cmd(cmd, cwd=None, check=True):
    """Exécuter une commande shell."""
    print(f"Running: {cmd} (in {cwd or 'current dir'})")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def get_active_modules():
    """Récupérer la liste des modules actifs (submodules Git)."""
    try:
        output = run_cmd("git submodule status", cwd=ROOT)
        modules = []
        for line in output.split('\n'):
            if line.strip() and 'modules/' in line:
                # Format: " hash modules/module-name (commit-info)"
                module_path = line.split()[1]
                module_name = module_path.split('/')[-1]
                modules.append(module_name)
        return modules
    except:
        print("Warning: Could not get submodule status, scanning directory")
        return [d.name for d in MODULES_DIR.iterdir() if d.is_dir() and (d / ".git").exists()]

def sync_copilotage_to_module(module_name):
    """Synchroniser la config copilotage vers un module."""
    module_path = MODULES_DIR / module_name
    module_copilotage = module_path / "copilotage"
    
    if not module_path.exists():
        print(f"Warning: Module {module_name} not found")
        return False
        
    # Créer le dossier copilotage si nécessaire
    module_copilotage.mkdir(exist_ok=True)
    
    # Copier la config de base
    base_config = {
        "include": ["../../copilotage/shared/rules/**/*.yml", "../../copilotage/shared/workflows/**/*.yml"],
        "project": {
            "name": module_name,
            "module": True,
            "parent": "PaniniFS"
        },
        "extends": "../../copilotage/shared/config.yml"
    }
    
    config_file = module_copilotage / "config.yml"
    with open(config_file, 'w') as f:
        yaml.dump(base_config, f, default_flow_style=False, allow_unicode=True)
    
    # Créer un README expliquant la configuration
    readme_content = f"""# Copilotage - {module_name}

Configuration de copilotage héritée du repository principal PaniniFS.

## Configuration

- Base: `../../copilotage/shared/config.yml`
- Règles: `../../copilotage/shared/rules/**/*.yml`
- Workflows: `../../copilotage/shared/workflows/**/*.yml`

## Mise à jour

La configuration est synchronisée automatiquement depuis le repository principal.
Pour modifier les règles partagées, éditer dans PaniniFS/copilotage/shared/.

Pour personnaliser ce module spécifiquement, créer des fichiers locaux :
- `rules/module-specific.yml` 
- `preferences.yml`
"""
    
    readme_file = module_copilotage / "README.md"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Synchronized copilotage config to {module_name}")
    return True

def update_submodule_reference():
    """Mettre à jour la référence du submodule copilotage/shared dans le repo principal."""
    print("Updating copilotage/shared submodule reference...")
    run_cmd("git add copilotage/shared", cwd=ROOT)
    
def main():
    print("🔄 Starting copilotage synchronization...")
    
    # Vérifier que le submodule shared est à jour
    if not COPILOTAGE_SHARED.exists():
        print("❌ copilotage/shared not found. Initialize submodules first.")
        sys.exit(1)
    
    # Récupérer les modules actifs
    modules = get_active_modules()
    print(f"📋 Found {len(modules)} active modules: {', '.join(modules)}")
    
    # Synchroniser chaque module
    success_count = 0
    for module in modules:
        if sync_copilotage_to_module(module):
            success_count += 1
    
    # Mettre à jour la référence du submodule
    update_submodule_reference()
    
    print(f"✅ Synchronization complete: {success_count}/{len(modules)} modules updated")
    print("💡 Don't forget to commit and push changes in individual module repositories")

if __name__ == "__main__":
    main()
