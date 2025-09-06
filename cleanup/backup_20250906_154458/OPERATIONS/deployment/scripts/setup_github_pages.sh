#!/bin/bash

# Configuration GitHub Pages pour paninifs.org
# Ce script guide la configuration DNS et GitHub Pages

echo "🌐 Configuration GitHub Pages pour paninifs.org"
echo "================================================"

# Vérification des prérequis
echo "📋 Prérequis à vérifier :"
echo "   ✅ Domaine paninifs.org configuré"
echo "   ✅ CNAME GitHub créé"
echo "   ✅ Repository public sur GitHub"

echo ""
echo "🔧 Configuration DNS requise :"
echo "   Type: CNAME"
echo "   Nom: @"
echo "   Valeur: stephanedenis.github.io"
echo "   TTL: 3600 (1 heure)"

echo ""
echo "🔧 Configuration DNS pour www :"
echo "   Type: CNAME" 
echo "   Nom: www"
echo "   Valeur: stephanedenis.github.io"
echo "   TTL: 3600 (1 heure)"

echo ""
echo "⚙️  Configuration GitHub Pages :"
echo "   1. Aller dans Settings > Pages"
echo "   2. Source: Deploy from a branch"
echo "   3. Branch: gh-pages / root"
echo "   4. Custom domain: paninifs.org"
echo "   5. Enforce HTTPS: ✅"

echo ""
echo "🚀 Déploiement automatique :"
echo "   - Push sur master/main déclenche le déploiement"
echo "   - GitHub Actions build et deploy automatiquement"
echo "   - Notifications en cas d'erreur"

echo ""
echo "🧪 Test de déploiement local :"
echo "   ./deploy_docs.sh test"

echo ""
echo "🌍 Test de déploiement production :"
echo "   ./deploy_docs.sh production"

echo ""
echo "📊 Vérification après déploiement :"
echo "   - https://paninifs.org (site principal)"
echo "   - https://www.paninifs.org (redirection)"
echo "   - Certificat SSL actif"
echo "   - Responsive sur mobile/tablette"

echo ""
echo "✅ Configuration terminée !"
echo "La documentation sera automatiquement publiée sur paninifs.org"
