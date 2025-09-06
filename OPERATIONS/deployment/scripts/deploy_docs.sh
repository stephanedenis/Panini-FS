#!/bin/bash

# Script de déploiement automatique de la documentation PFS
# Usage: ./deploy_docs.sh [test|production]

set -e

ENVIRONMENT=${1:-test}
DOCS_DIR="docs"
BUILD_DIR="site"
DOMAIN_PROD="paninifs.org"
DOMAIN_TEST="docs.paninifs.org"

echo "🚀 Déploiement de la documentation PFS - Mode: $ENVIRONMENT"

# Validation de l'environnement
if [ ! -d "$DOCS_DIR" ]; then
    echo "❌ Erreur: Répertoire $DOCS_DIR introuvable"
    exit 1
fi

# Activation de l'environnement virtuel
if [ -d "mkdocs_env" ]; then
    echo "📦 Activation de l'environnement virtuel..."
    source mkdocs_env/bin/activate
else
    echo "⚠️  Environnement virtuel non trouvé, utilisation de l'environnement système"
fi

# Validation de la configuration
echo "🔍 Validation de la configuration MkDocs..."
if ! mkdocs --help > /dev/null 2>&1; then
    echo "❌ Erreur: MkDocs non installé ou non accessible"
    exit 1
fi

# Construction de la documentation
echo "🏗️  Construction de la documentation..."
mkdocs build --clean

# Vérification du build
if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Erreur: Build échoué, répertoire $BUILD_DIR non créé"
    exit 1
fi

echo "✅ Documentation construite avec succès"

# Statistiques du build
echo "📊 Statistiques du build:"
echo "   - Fichiers HTML: $(find $BUILD_DIR -name "*.html" | wc -l)"
echo "   - Fichiers CSS:  $(find $BUILD_DIR -name "*.css" | wc -l)"
echo "   - Fichiers JS:   $(find $BUILD_DIR -name "*.js" | wc -l)"
echo "   - Taille totale: $(du -sh $BUILD_DIR | cut -f1)"

# Instructions de déploiement selon l'environnement
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🌐 Instructions de déploiement en production:"
    echo "   1. Vérifier que le CNAME pointe vers GitHub Pages"
    echo "   2. Configurer le domaine $DOMAIN_PROD dans les paramètres GitHub"
    echo "   3. Activer HTTPS dans les paramètres Pages"
    echo "   4. Le déploiement automatique se fera via GitHub Actions"
elif [ "$ENVIRONMENT" = "test" ]; then
    echo "🧪 Mode test - Documentation disponible localement"
    echo "   URL: http://localhost:8000"
    echo "   Pour servir: mkdocs serve"
fi

# Génération du fichier CNAME pour GitHub Pages
if [ "$ENVIRONMENT" = "production" ]; then
    echo "$DOMAIN_PROD" > "$BUILD_DIR/CNAME"
    echo "📝 Fichier CNAME créé pour $DOMAIN_PROD"
fi

echo "🎉 Déploiement terminé avec succès!"
