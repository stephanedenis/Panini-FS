#!/bin/bash
# 🚨 EMERGENCY PLASMA FIXER
# Résoudre plasmashell 100% CPU + libérer mémoire

echo "🚨 EMERGENCY PLASMA FIXER"
echo "========================="
echo "🎯 Problème: plasmashell 100% CPU (PID $(pgrep plasmashell))"
echo "💾 Mémoire: $(free -h | grep Mem | awk '{print $3 "/" $2 " (" $3/$2*100 "%)"}') utilisée"
echo ""

echo "🔧 SOLUTION RAPIDE - REDÉMARRAGE PLASMASHELL"
echo "============================================="

# Étape 1: Sauvegarder session actuelle
echo "💾 Sauvegarde session..."
kwriteconfig5 --file ksmserverrc --group General --key loginMode restorePreviousLogout
echo "   ✅ Session sauvegardée"

# Étape 2: Tuer plasmashell proprement
echo "🔄 Redémarrage plasmashell..."
killall plasmashell 2>/dev/null
sleep 2

# Vérifier si toujours actif
if pgrep plasmashell > /dev/null; then
    echo "   ⚠️ Processus résistant, force kill..."
    pkill -9 plasmashell
    sleep 1
fi

# Étape 3: Nettoyer cache plasma
echo "🧹 Nettoyage cache Plasma..."
rm -rf ~/.cache/plasma* 2>/dev/null
rm -rf ~/.cache/plasmashell* 2>/dev/null
rm -rf ~/.cache/kwin* 2>/dev/null
echo "   ✅ Cache nettoyé"

# Étape 4: Redémarrer plasmashell
echo "🚀 Redémarrage plasmashell..."
nohup plasmashell --no-respawn > /dev/null 2>&1 &
sleep 3

# Vérifier redémarrage
if pgrep plasmashell > /dev/null; then
    NEW_PID=$(pgrep plasmashell)
    echo "   ✅ Plasmashell redémarré (PID: $NEW_PID)"
else
    echo "   ❌ Échec redémarrage"
fi

echo ""
echo "🔍 VÉRIFICATION PERFORMANCE..."
echo "=============================="

# Vérifier CPU usage du nouveau processus
sleep 5
PLASMA_CPU=$(ps -p $(pgrep plasmashell) -o %cpu --no-headers 2>/dev/null || echo "0")
echo "🖥️ CPU plasmashell: ${PLASMA_CPU}%"

# Vérifier mémoire totale
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2*100}')
echo "💾 Mémoire système: ${MEMORY_USAGE}%"

# Vérifier load average
LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}')
echo "⚡ Load average: $LOAD_AVG"

echo ""
if (( $(echo "$PLASMA_CPU < 20" | bc -l) )); then
    echo "✅ PROBLÈME RÉSOLU!"
    echo "🎯 Plasmashell fonctionne normalement"
else
    echo "⚠️ PROBLÈME PERSISTE"
    echo "🔧 Solutions additionnelles nécessaires"
fi

echo ""
echo "💡 PRÉVENTION FUTURE:"
echo "===================="
echo "• Redémarrer système si load > 5.0 persistant"
echo "• Vider cache Plasma weekly: rm -rf ~/.cache/plasma*"
echo "• Monitorer: watch 'ps aux | grep plasmashell'"
echo ""
echo "🚀 TOTORO SHOULD BE RESPONSIVE AGAIN!"
