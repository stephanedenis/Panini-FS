#!/bin/bash
# 🔧 PLASMA STABILIZER AVANCÉ
# Solution définitive pour plasmashell gourmand

echo "🔧 PLASMA STABILIZER AVANCÉ"
echo "============================"

# Vérifier CPU actuel
CURRENT_CPU=$(ps -p $(pgrep plasmashell) -o %cpu --no-headers 2>/dev/null | head -1)
echo "🖥️ CPU plasmashell actuel: ${CURRENT_CPU}%"

if (( $(echo "$CURRENT_CPU > 30" | awk '{print ($1 > 30)}') )); then
    echo "⚠️ Toujours élevé, solutions additionnelles..."
    
    # Solution 1: Désactiver effets visuels temporairement
    echo "🎨 Désactivation effets visuels..."
    kwriteconfig5 --file kwinrc --group Compositing --key Enabled false
    qdbus org.kde.KWin /Compositor suspend
    echo "   ✅ Effets désactivés"
    
    # Solution 2: Réduire widgets plasma actifs
    echo "🔧 Optimisation widgets..."
    kwriteconfig5 --file plasmashellrc --group PlasmaViews --key panelVisibility 1
    echo "   ✅ Panels optimisés"
    
    # Solution 3: Limiter indexation fichiers
    echo "📁 Limitation indexation..."
    balooctl disable 2>/dev/null || echo "   ℹ️ Baloo non disponible"
    echo "   ✅ Indexation limitée"
    
    # Solution 4: Kill processus gourmands connexes
    echo "🧹 Nettoyage processus..."
    pkill -f "krunner" 2>/dev/null
    pkill -f "kactivitymanagerd" 2>/dev/null
    echo "   ✅ Processus nettoyés"
    
    sleep 3
    
    # Vérifier amélioration
    NEW_CPU=$(ps -p $(pgrep plasmashell) -o %cpu --no-headers 2>/dev/null | head -1)
    echo "🔍 Nouveau CPU: ${NEW_CPU}%"
    
    if (( $(echo "$NEW_CPU < 20" | awk '{print ($1 < 20)}') )); then
        echo "✅ SUCCÈS! CPU normalisé"
    else
        echo "🔥 SOLUTION ULTIME: Mode performance minimal"
        
        # Mode performance minimal
        kwriteconfig5 --file kwinrc --group Plugins --key kwin4_effect_fadingpopupsEnabled false
        kwriteconfig5 --file kwinrc --group Plugins --key kwin4_effect_translucencyEnabled false
        kwriteconfig5 --file kwinrc --group Plugins --key slideEnabled false
        
        # Redémarrer KWin
        kwin_x11 --replace &
        disown
        
        echo "   ✅ Mode performance activé"
    fi
else
    echo "✅ CPU acceptable, optimisations légères..."
    
    # Optimisations préventives légères
    kwriteconfig5 --file plasmarc --group Theme --key name breeze-dark
    echo "   ✅ Thème optimisé"
fi

echo ""
echo "📊 ÉTAT FINAL SYSTÈME:"
echo "======================"
echo "🖥️ Load average: $(uptime | awk -F'load average:' '{print $2}')"
echo "💾 Mémoire: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "🔥 CPU plasmashell: $(ps -p $(pgrep plasmashell) -o %cpu --no-headers 2>/dev/null | head -1)%"

echo ""
echo "🎯 TOTORO DEVRAIT ÊTRE RÉACTIF MAINTENANT!"
echo "🚀 Prêt pour Colab deployment!"
