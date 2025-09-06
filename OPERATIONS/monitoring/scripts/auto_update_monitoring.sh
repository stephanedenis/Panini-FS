#!/bin/bash
#
# 🔄 MISE À JOUR CONTINUE MONITORING
# ==================================
#
# Script à exécuter périodiquement (cron) pour maintenir
# les données de monitoring à jour automatiquement.
#

set -euo pipefail

# Configuration
BASE_DIR="/home/stephane/GitHub/PaniniFS-1"
LOG_FILE="$BASE_DIR/OPERATIONS/monitoring/logs/auto_update.log"

# Fonction de log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Créer répertoire logs
mkdir -p "$(dirname "$LOG_FILE")"

log "🔄 Début mise à jour automatique monitoring"

cd "$BASE_DIR"

# 1. Mise à jour données système
log "📊 Mise à jour system_status.json..."
if python3 OPERATIONS/monitoring/scripts/update_system_status.py >> "$LOG_FILE" 2>&1; then
    log "✅ Données système mises à jour"
else
    log "❌ Erreur mise à jour données système"
    exit 1
fi

# 2. Vérifier s'il y a des changements
if git diff --quiet docs/data/system_status.json; then
    log "ℹ️ Aucun changement de statut détecté"
    exit 0
fi

# 3. Commit automatique si changements
log "📤 Changements détectés, commit automatique..."
git add docs/data/system_status.json

git commit -m "🤖 Auto-update system status $(date '+%Y-%m-%d %H:%M:%S')

- Updated agent status monitoring
- Refreshed domain health checks  
- Updated workflow status
- Camping strategy status refresh

Automated by: OPERATIONS/monitoring/scripts/auto_update_monitoring.sh"

# 4. Push si nécessaire
if git push origin master >> "$LOG_FILE" 2>&1; then
    log "✅ Changements publiés sur GitHub"
else
    log "⚠️ Erreur push GitHub (sera retenté)"
fi

log "🏁 Mise à jour automatique terminée"
