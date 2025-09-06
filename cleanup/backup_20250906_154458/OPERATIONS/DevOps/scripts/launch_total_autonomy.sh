#!/bin/bash
"""
🌙 LANCEUR AUTONOMIE TOTALE - Solution définitive aux micro-confirmations
💡 Développement continu pendant absence utilisateur avec intelligence adaptative
"""

echo "🤖 SOLUTION AUTONOMIE TOTALE ACTIVÉE"
echo "======================================"
echo "🎯 Élimination définitive des micro-confirmations"
echo "🚀 Développement continu pendant absence"
echo ""

# Configuration environnement
cd /home/stephane/GitHub/PaniniFS-1/Copilotage/scripts
source venv/bin/activate

# Option 1: Daemon continu pour absence prolongée (8h par défaut)
echo "🌙 Option 1: Daemon continu (recommandé pour absence)"
echo "Usage: ./launch_total_autonomy.sh daemon [heures]"
echo ""

# Option 2: Moteur autonomie simple pour tâches immédiates
echo "⚡ Option 2: Moteur autonomie immédiat"
echo "Usage: ./launch_total_autonomy.sh engine"
echo ""

# Détection mode demandé
MODE=${1:-daemon}
HOURS=${2:-8}

if [ "$MODE" = "daemon" ]; then
    echo "🌙 LANCEMENT DAEMON AUTONOMIE CONTINUE"
    echo "⏰ Durée: $HOURS heures"
    echo "🤖 Développement continu sans interruption..."
    echo ""
    
    # Lancement daemon en arrière-plan
    nohup python continuous_autonomy_daemon.py $HOURS > daemon_output.log 2>&1 &
    DAEMON_PID=$!
    
    echo "✅ Daemon autonomie lancé (PID: $DAEMON_PID)"
    echo "📄 Logs en temps réel: tail -f daemon_output.log"
    echo "🛑 Arrêt: kill $DAEMON_PID"
    echo ""
    echo "🎯 AUTONOMIE TOTALE ACTIVE - Plus de micro-confirmations !"
    
    # Sauvegarde PID pour arrêt facile
    echo $DAEMON_PID > daemon.pid
    echo "PID sauvé dans daemon.pid"
    
elif [ "$MODE" = "engine" ]; then
    echo "⚡ LANCEMENT MOTEUR AUTONOMIE IMMÉDIAT"
    echo "🤖 Exécution cycle autonome..."
    echo ""
    
    python total_autonomy_engine.py
    
elif [ "$MODE" = "stop" ]; then
    echo "🛑 ARRÊT DAEMON AUTONOMIE"
    
    if [ -f daemon.pid ]; then
        PID=$(cat daemon.pid)
        kill $PID 2>/dev/null
        rm daemon.pid
        echo "✅ Daemon arrêté (PID: $PID)"
    else
        echo "❌ Aucun daemon en cours"
    fi
    
else
    echo "❌ Mode inconnu: $MODE"
    echo "Modes disponibles: daemon, engine, stop"
fi

echo ""
echo "🏆 SOLUTION AUTONOMIE TOTALE DÉPLOYÉE"
echo "💡 Fini les micro-confirmations - développement intelligent continu !"
