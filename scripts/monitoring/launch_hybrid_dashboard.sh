#!/bin/bash
# 🎯 LANCEUR DASHBOARD LOCAL HYBRIDE
# Dashboard local + cloud intégré avec surveillance autonome

echo "🎯 Démarrage Dashboard Local Hybride PaniniFS..."

# Vérification des dépendances
echo "🔍 Vérification dépendances..."
python3 -c "import psutil, json, http.server" 2>/dev/null || {
    echo "❌ Installation dépendances manquantes..."
    pip install psutil || echo "⚠️  psutil non installé - fonctionnalités limitées"
}

# Nettoyage logs précédents (garde 100 dernières lignes)
if [ -f "/tmp/paninifs_dashboard.log" ]; then
    tail -100 /tmp/paninifs_dashboard.log > /tmp/paninifs_dashboard.log.tmp
    mv /tmp/paninifs_dashboard.log.tmp /tmp/paninifs_dashboard.log
fi

# Navigation vers répertoire
cd /home/stephane/GitHub/PaniniFS-1

echo "🚀 Lancement dashboard sur http://localhost:8080"
echo "📊 Intégration locale + cloud"
echo "🔄 Auto-refresh 5 secondes"
echo ""
echo "💡 Fonctionnalités:"
echo "   - Métriques système temps réel"
echo "   - Surveillance processus Python"
echo "   - Status GitHub CLI"
echo "   - Dashboard cloud intégré (iframe)"
echo "   - Monitoring détaillé"
echo "   - Actions rapides (démarrage/arrêt)"
echo ""
echo "🛑 Appuyez sur Ctrl+C pour arrêter"
echo "======================================"

# Lancement dashboard
python3 OPERATIONS/monitoring/local_cloud_dashboard.py
