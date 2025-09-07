#!/bin/bash
# Watchdog Doctor - Redémarre si crash
while true; do
    # Vérifie si doctor tourne
    if ! python3 doctor_control.py status > /dev/null 2>&1; then
        echo "🚨 $(date): Doctor crashed - Redémarrage automatique"
        python3 doctor_control.py start
    fi
    sleep 300  # Vérification toutes les 5 minutes
done
