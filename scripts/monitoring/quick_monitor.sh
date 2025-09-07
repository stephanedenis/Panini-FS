#!/bin/bash
# 🔍 QUICK TERMINAL MONITOR
# Surveillance rapide des terminaux et processus actifs

echo "🔍 SURVEILLANCE TERMINAUX & PROCESSUS PANINIFS"
echo "==============================================="
echo ""

echo "📱 TERMINAUX ACTIFS:"
ps aux | grep -E "(bash|zsh|sh)" | grep -v grep | wc -l | xargs echo "   Terminaux bash actifs:"
echo ""

echo "🐍 PROCESSUS PYTHON PANINIFS:"
ps aux | grep python | grep -i paninifs | grep -v grep || echo "   Aucun processus PaniniFS actif"
echo ""

echo "🔧 PROCESSUS PLAYWRIGHT/FIREFOX:"
ps aux | grep -E "(firefox|playwright)" | grep -v grep || echo "   Aucun processus Playwright/Firefox actif"
echo ""

echo "📊 TOP 5 PROCESSUS CPU:"
ps aux --sort=-%cpu | head -6
echo ""

echo "💾 UTILISATION MÉMOIRE:"
free -h
echo ""

echo "💽 UTILISATION DISQUE:"
df -h / | tail -1
echo ""

echo "🔗 GITHUB CLI STATUS:"
gh auth status 2>/dev/null || echo "   GitHub CLI non configuré ou non connecté"
echo ""

echo "📝 DERNIÈRES LIGNES LOG DASHBOARD:"
if [ -f "/tmp/paninifs_dashboard.log" ]; then
    tail -5 /tmp/paninifs_dashboard.log
else
    echo "   Aucun log dashboard trouvé"
fi
echo ""

echo "⚡ MONITORING EN TEMPS RÉEL (Ctrl+C pour arrêter):"
echo "   Dashboard: http://localhost:8080"
echo "   Métriques JSON: /tmp/paninifs_local_dashboard.json"
echo "   Logs: /tmp/paninifs_dashboard.log"
