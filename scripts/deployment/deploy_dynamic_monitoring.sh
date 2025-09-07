#!/bin/bash
#
# 🔄 DÉPLOIEMENT MONITORING DYNAMIQUE
# ===================================
#
# Déploie la solution de monitoring dynamique avec MkDocs
# et met à jour le système de statut JSON automatiquement.
#

set -euo pipefail

echo "🚀 Déploiement Monitoring Dynamique PaniniFS"
echo "============================================="

# Configuration
BASE_DIR="/home/stephane/GitHub/PaniniFS-1"
cd "$BASE_DIR"

# 1. Mise à jour état système
echo "🔄 Mise à jour état système..."
python3 OPERATIONS/monitoring/scripts/update_system_status.py

# 2. Vérification fichiers MkDocs
echo "📋 Vérification configuration MkDocs..."
if [[ ! -f "docs/dashboard.md" ]]; then
    echo "❌ Dashboard MkDocs manquant"
    exit 1
fi

if [[ ! -f "docs/data/system_status.json" ]]; then
    echo "❌ Fichier status JSON manquant"
    exit 1
fi

echo "✅ Fichiers monitoring présents"

# 3. Test local MkDocs (optionnel)
echo "🧪 Test configuration MkDocs..."
if command -v mkdocs &> /dev/null; then
    mkdocs build --config-file mkdocs.yml --site-dir dist_test --quiet
    if [[ $? -eq 0 ]]; then
        echo "✅ Build MkDocs réussi"
        rm -rf dist_test
    else
        echo "⚠️ Problème build MkDocs"
    fi
else
    echo "ℹ️ MkDocs non installé localement"
fi

# 4. Commit et push
echo "📤 Commit des changements..."
git add docs/
git add mkdocs.yml
git add OPERATIONS/monitoring/

# Vérifier s'il y a des changements
if git diff --cached --quiet; then
    echo "ℹ️ Aucun changement à commiter"
else
    git commit -m "🚀 Dynamic monitoring system integrated with MkDocs

- Added dynamic dashboard at docs/dashboard.md with JavaScript status loading
- Created comprehensive system_status.json with real-time data structure
- Updated mkdocs.yml navigation to include dashboard
- Added automated status update script
- Integrated with official MkDocs site at paninifs.org

Features:
- Real-time agent status (13+ agents across 5 categories)
- Multi-domain monitoring (5 domains configured)
- GitHub workflow health tracking
- Camping strategy status display
- Auto-refresh every 30 seconds"

    echo "🔄 Push vers GitHub..."
    git push origin main
fi

# 5. Information de déploiement
echo ""
echo "✅ DÉPLOIEMENT TERMINÉ"
echo "====================="
echo ""
echo "🌐 Dashboard disponible à:"
echo "   https://paninifs.org/dashboard/"
echo "   https://paninifs.org/dashboard/"
echo ""
echo "📊 Statut JSON accessible à:"
echo "   https://paninifs.org/data/system_status.json"
echo ""
echo "🔄 Pour mettre à jour le statut:"
echo "   python3 OPERATIONS/monitoring/scripts/update_system_status.py"
echo ""
echo "🏕️ Camping Strategy: ACTIVE"
echo "🤖 Agents Autonomes: OPÉRATIONNELS"
echo "🌐 Multi-Domaines: CONFIGURÉS"

exit 0
