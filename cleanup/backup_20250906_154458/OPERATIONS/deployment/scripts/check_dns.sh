#!/bin/bash

# 🔍 VÉRIFICATION DNS DOMAINES PANINI
echo "🔍 VÉRIFICATION DNS ÉCOSYSTÈME PANINI"
echo "===================================="

DOMAINS=(
    "paninifs.com"
    "o-tomate.com" 
    "stephanedenis.cc"
    "sdenis.net"
    "paninifs.org"
)

echo "📊 Test de résolution DNS..."
echo ""

for domain in "${DOMAINS[@]}"; do
    echo "🌐 $domain:"
    
    # Test CNAME www
    www_result=$(dig +short www.$domain)
    if [[ $www_result == *"stephanedenis.github.io"* ]]; then
        echo "  ✅ www.$domain → $www_result"
    else
        echo "  ❌ www.$domain → $www_result (attendu: stephanedenis.github.io)"
    fi
    
    # Test apex
    apex_result=$(dig +short $domain)
    if [[ -n "$apex_result" ]]; then
        echo "  ✅ $domain → $apex_result"
    else
        echo "  ⏳ $domain → Non configuré (optionnel)"
    fi
    
    echo ""
done

echo "🎯 Configuration terminée!"
echo "⏰ Propagation DNS: 5-30 minutes"
echo "🔗 Test direct: https://paninifs.com/domains.html"
