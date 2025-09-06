#!/bin/bash
# Script de lancement pour l'analyse autonome
# Exécute tous les scripts d'analyse et génère un rapport complet

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COPILOTAGE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Lancement de l'analyse autonome PaniniFS"
echo "Répertoire de scripts: $SCRIPT_DIR"
echo "Répertoire Copilotage: $COPILOTAGE_DIR"

# Vérifier que Python 3 est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python 3 n'est pas installé"
    exit 1
fi

# Créer le répertoire de sortie s'il n'existe pas
mkdir -p "$SCRIPT_DIR/output"

echo
echo "📊 Étape 1: Analyse des préférences de développement..."
cd "$SCRIPT_DIR"
python3 analyze_preferences.py

echo
echo "📁 Étape 2: Collecte des échantillons de fichiers..."
python3 collect_samples.py

echo
echo "🧠 Étape 3: Analyse autonome complète..."
python3 autonomous_analyzer.py

echo
echo "✅ Analyse terminée!"
echo "📋 Rapports générés dans: $SCRIPT_DIR/"
echo
echo "Fichiers disponibles:"
ls -la "$SCRIPT_DIR"/*.json 2>/dev/null || echo "Aucun rapport JSON généré"

echo
echo "🎯 Pour consulter les recommandations:"
echo "   cat $SCRIPT_DIR/autonomous_analysis_report.json | jq '.recommendations[] | select(.priority == \"high\")'"
echo
echo "📈 Pour voir les statistiques:"
echo "   cat $SCRIPT_DIR/sample_collection_report.json | jq '.statistics'"
