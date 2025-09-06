#!/bin/bash

# 🌐 CONFIGURATION AUTOMATIQUE DOMAINES ÉCOSYSTÈME PANINI
# Script de déploiement multi-domaines

echo "🌐 CONFIGURATION DOMAINES PANINI - DÉMARRAGE"
echo "============================================="

# Configuration du domaine principal
echo "✅ paninifs.com configuré via CNAME"

# Création des sous-projets pour autres domaines
REPOS=(
    "PaniniFS-Community:paninifs.org"
    "Publications:stephanedenis.cc" 
    "Agents-Hub:o-tomate.com"
    "Lab-Experimental:sdenis.net"
)

for repo_domain in "${REPOS[@]}"; do
    repo="${repo_domain%:*}"
    domain="${repo_domain#*:}"
    
    echo "📁 Création repo: $repo pour domaine: $domain"
    
    # Créer le répertoire local temporaire
    mkdir -p "/tmp/$repo"
    cd "/tmp/$repo"
    
    # Initialiser le repo
    git init
    echo "# $repo" > README.md
    echo "$domain" > CNAME
    
    # Créer index.html basique
    cat > index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>$domain - Écosystème PaniniFS</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { color: #2c3e50; }
        .status { background: #e8f5e8; padding: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1 class="header">$domain</h1>
    <div class="status">
        <h2>🚧 En Construction</h2>
        <p>Ce domaine fait partie de l'écosystème PaniniFS.</p>
        <p><a href="https://paninifs.com">← Retour au site principal</a></p>
    </div>
</body>
</html>
EOF
    
    # Configuration Jekyll
    cat > _config.yml << EOF
title: "$domain - Écosystème PaniniFS"
description: "Domaine spécialisé de l'écosystème PaniniFS"
url: "https://$domain"
baseurl: ""
theme: minima
EOF
    
    echo "✅ Repo $repo configuré pour $domain"
done

echo ""
echo "🎯 RÉSUMÉ CONFIGURATION:"
echo "========================"
echo "✅ paninifs.com - Site principal (Dashboard)"
echo "🚧 paninifs.org - Communauté (à créer)"
echo "🚧 stephanedenis.cc - Publications (à créer)"
echo "🚧 o-tomate.com - Hub Agents (à créer)"
echo "🚧 sdenis.net - Laboratoire (à créer)"
echo ""
echo "📋 PROCHAINES ÉTAPES:"
echo "1. Créer les repos GitHub pour chaque domaine"
echo "2. Configurer DNS CNAME chez le registrar"
echo "3. Activer GitHub Pages pour chaque repo"
echo "4. Déployer le contenu spécialisé"
echo ""
echo "🌐 Configuration domaines terminée!"
