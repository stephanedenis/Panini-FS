#!/bin/bash

# 🌥️ PaniniFS Cloud Autonomous Launcher
# Lance l'écosystème cloud autonome complet

set -e

echo "🌥️ PANINI-FS CLOUD AUTONOMOUS ECOSYSTEM"
echo "======================================="
echo "🎯 100% Cloud, 0% Dépendance Totoro"
echo ""

# Variables de configuration
GITHUB_USER="stephanedenis"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
COLAB_NOTEBOOK_URL="https://colab.research.google.com/github/stephanedenis/PaniniFS/blob/master/Copilotage/colab_notebooks/semantic_processing_accelerated.ipynb"

# Fonctions utilitaires
show_progress() {
    echo "🔄 $1..."
}

show_success() {
    echo "✅ $1"
}

show_error() {
    echo "❌ $1"
}

# Étape 1: Vérification prérequis
show_progress "Vérification configuration"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️ Variable GITHUB_TOKEN non définie"
    echo "💡 Utilisez: export GITHUB_TOKEN=<VOTRE_TOKEN_PAT>"
    echo "🔗 Ou lancez sans token pour repos publics uniquement"
fi

# Étape 2: Setup repos si nécessaire
show_progress "Vérification écosystème repos"

setup_repos_if_needed() {
    local repos=("PaniniFS-Public" "PaniniFS-Academic" "PaniniFS-OpenSource")
    local missing_repos=0
    
    for repo in "${repos[@]}"; do
        if ! curl -s "https://api.github.com/repos/$GITHUB_USER/$repo" | grep -q '"name"'; then
            ((missing_repos++))
        fi
    done
    
    if [ $missing_repos -gt 0 ]; then
        echo "📦 $missing_repos repos manquants dans l'écosystème"
        echo "🚀 Lancement setup automatique..."
        
        if [ -f "Copilotage/scripts/setup_cloud_autonomous.sh" ]; then
            chmod +x Copilotage/scripts/setup_cloud_autonomous.sh
            ./Copilotage/scripts/setup_cloud_autonomous.sh
        else
            show_error "Script setup non trouvé"
            exit 1
        fi
    else
        show_success "Écosystème repos complet"
    fi
}

setup_repos_if_needed

# Étape 3: Push notebook mis à jour
show_progress "Mise à jour notebook Colab"

git add Copilotage/colab_notebooks/semantic_processing_accelerated.ipynb 2>/dev/null || true
git add Copilotage/cloud_autonomous_architecture.md 2>/dev/null || true
git add Copilotage/scripts/setup_cloud_autonomous.sh 2>/dev/null || true

if git diff --staged --quiet; then
    show_success "Notebook déjà à jour"
else
    git commit -m "🌥️ Update autonomous cloud ecosystem

- GitHub repos direct access without Totoro dependencies
- Hierarchical data architecture: Public < Communities < Personal  
- 100% cloud autonomous processing
- Real ecosystem data processing
- Version-based model evolution
- Complete independence from local resources

Ready for fully autonomous cloud operation!"

    git push origin master
    show_success "Notebook mis à jour sur GitHub"
fi

# Étape 4: Test accès repos écosystème
show_progress "Test accès repos écosystème"

test_repo_access() {
    local test_repos=("PaniniFS" "PaniniFS-Public")
    local accessible=0
    
    for repo in "${test_repos[@]}"; do
        if curl -s --max-time 10 "https://api.github.com/repos/$GITHUB_USER/$repo" | grep -q '"name"'; then
            echo "   ✅ $repo accessible"
            ((accessible++))
        else
            echo "   ⚠️ $repo non accessible"
        fi
    done
    
    if [ $accessible -gt 0 ]; then
        show_success "Accès repos validé ($accessible/$(${#test_repos[@]}))"
        return 0
    else
        show_error "Aucun repo accessible"
        return 1
    fi
}

if test_repo_access; then
    echo "🌍 Repos de l'écosystème accessibles"
else
    echo "⚠️ Problème d'accès aux repos, mais continuons..."
fi

# Étape 5: Préparation launch Colab
show_progress "Préparation lancement Colab"

# Créer script de lancement direct
cat > launch_colab_autonomous.sh << EOF
#!/bin/bash

echo "🚀 LANCEMENT COLAB AUTONOMOUS"
echo "============================"

COLAB_URL="$COLAB_NOTEBOOK_URL"

echo "📓 Notebook: semantic_processing_accelerated.ipynb"
echo "🌥️ Mode: 100% Cloud Autonomous" 
echo "📊 Données: Écosystème GitHub hiérarchique"
echo ""

echo "🔗 URL Colab:"
echo "\$COLAB_URL"
echo ""

# Copier dans presse-papier si possible
echo "\$COLAB_URL" | xclip -selection clipboard 2>/dev/null || echo "(xclip non disponible)"

# Ouvrir navigateur si possible
if command -v xdg-open &> /dev/null; then
    echo "🌐 Ouverture navigateur..."
    xdg-open "\$COLAB_URL" &
elif command -v firefox &> /dev/null; then
    echo "🦊 Ouverture Firefox..."
    firefox "\$COLAB_URL" &
else
    echo "💡 Copiez l'URL ci-dessus dans votre navigateur"
fi

echo ""
echo "📋 INSTRUCTIONS COLAB:"
echo "1. ⚡ Activer GPU: Runtime > Change runtime type > GPU"
echo "2. 🔄 Exécuter toutes les cellules"
echo "3. 📊 Le notebook va:"
echo "   - Cloner automatiquement l'écosystème GitHub"
echo "   - Traiter vos données hiérarchiques"
echo "   - Générer analyse sémantique complète"
echo "   - Télécharger résultats automatiquement"
echo ""
echo "🎯 Traitement 100% autonome de votre écosystème!"
EOF

chmod +x launch_colab_autonomous.sh

# Étape 6: Monitoring setup
show_progress "Configuration monitoring autonome"

# Créer monitoring basic
cat > monitor_ecosystem.py << 'EOF'
#!/usr/bin/env python3
"""Monitoring simple de l'écosystème autonomous"""

import requests
import json
from datetime import datetime

def check_ecosystem_health():
    repos = [
        "stephanedenis/PaniniFS",
        "stephanedenis/PaniniFS-Public"
    ]
    
    print("🌥️ MONITORING ÉCOSYSTÈME AUTONOMOUS")
    print("=" * 40)
    
    for repo in repos:
        try:
            url = f"https://api.github.com/repos/{repo}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {repo}")
                print(f"   Dernière maj: {data.get('updated_at', 'N/A')}")
                print(f"   Taille: {data.get('size', 0)} KB")
            else:
                print(f"⚠️ {repo}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {repo}: {e}")
    
    print(f"\n📊 Check terminé: {datetime.now()}")

if __name__ == "__main__":
    check_ecosystem_health()
EOF

chmod +x monitor_ecosystem.py

show_success "Monitoring configuré"

# Étape 7: Résumé final et lancement
echo ""
echo "🎉 ÉCOSYSTÈME CLOUD AUTONOMOUS PRÊT!"
echo "===================================="
echo ""
echo "🌍 Architecture déployée:"
echo "   📦 Repos hiérarchiques: Public < Communautés < Personnel"
echo "   🔄 Versioning automatique par modèle"
echo "   ⚡ Processing GPU Colab intégré"
echo "   📊 Monitoring ecosystem continu"
echo ""
echo "🚀 Lancement immédiat:"
echo "   ./launch_colab_autonomous.sh"
echo ""
echo "📋 Fonctionnalités autonomes:"
echo "   ✅ Clonage automatique écosystème GitHub"
echo "   ✅ Accès direct Pensine via GitHub"
echo "   ✅ Processing hiérarchique des données"
echo "   ✅ 0% dépendance Totoro"
echo "   ✅ 100% cloud gratuit"
echo ""
echo "🔗 URL directe Colab:"
echo "$COLAB_NOTEBOOK_URL"
echo ""

# Demander si lancer immédiatement
read -p "🚀 Lancer Colab maintenant? (y/N): " launch_now

if [[ $launch_now =~ ^[Yy]$ ]]; then
    echo "🌥️ Lancement Colab Autonomous..."
    ./launch_colab_autonomous.sh
else
    echo "💡 Lancez plus tard avec: ./launch_colab_autonomous.sh"
fi

echo ""
echo "🌟 ÉCOSYSTÈME AUTONOME OPÉRATIONNEL!"
echo "🔍 Monitoring: ./monitor_ecosystem.py"
echo "📊 100% Cloud, 0% Totoro, ∞% Autonomous!"
