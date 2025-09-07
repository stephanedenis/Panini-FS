#!/bin/bash
# Monitoring d'urgence - alerte seulement si TOUT est cassé

check_critical() {
    local failures=0
    
    # Vérifie GitHub Pages
    if ! curl -s -o /dev/null -w "%{http_code}" https://paninifs.org | grep -q "200"; then
        ((failures++))
    fi
    
    # Vérifie DNS principal
    if ! nslookup paninifs.org > /dev/null 2>&1; then
        ((failures++))
    fi
    
    # Vérifie Doctor
    if ! python3 doctor_control.py status > /dev/null 2>&1; then
        ((failures++))
    fi
    
    # Si tout est cassé (3+ échecs)
    if [ $failures -ge 3 ]; then
        echo "🚨 URGENCE: $failures composants critiques down"
        echo "Timestamp: $(date)"
        echo "Action: Vérification manuelle requise"
        
        # Log l'urgence
        echo "$(date): EMERGENCY - $failures critical failures" >> vacation_emergencies.log
        
        # Tente redémarrage Doctor
        python3 doctor_control.py start
        
        return 1
    fi
    
    return 0
}

if ! check_critical; then
    echo "🚨 Urgence détectée - voir vacation_emergencies.log"
else
    echo "✅ Systèmes critiques OK"
fi
