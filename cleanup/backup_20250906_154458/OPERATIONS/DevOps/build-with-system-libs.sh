#!/bin/bash

# Script pour compiler avec les bibliothèques système
# Usage: ./build-with-system-libs.sh [cargo-command]

set -e

echo "🔧 Configuration pour utiliser les bibliothèques système"
echo "======================================================="

# Variables d'environnement pour RocksDB
export ROCKSDB_LIB_DIR="/usr/lib64"
export ROCKSDB_INCLUDE_DIR="/usr/include"
export ROCKSDB_STATIC=0  # Utiliser la bibliothèque dynamique

# Variables pour pkg-config
export PKG_CONFIG_PATH="/usr/lib64/pkgconfig:/usr/share/pkgconfig:$PKG_CONFIG_PATH"

# Variables pour les bibliothèques système
export LD_LIBRARY_PATH="/usr/lib64:$LD_LIBRARY_PATH"

# Affichage des chemins configurés
echo "📚 Bibliothèques configurées:"
echo "   ROCKSDB_LIB_DIR: $ROCKSDB_LIB_DIR"
echo "   ROCKSDB_INCLUDE_DIR: $ROCKSDB_INCLUDE_DIR" 
echo "   PKG_CONFIG_PATH: $PKG_CONFIG_PATH"

# Vérification que RocksDB est disponible
if [ -f "/usr/lib64/librocksdb.so" ]; then
    echo "✅ RocksDB trouvé: $(ls -la /usr/lib64/librocksdb.so*)"
else
    echo "❌ RocksDB non trouvé dans /usr/lib64/"
    exit 1
fi

# Vérification des headers
if [ -d "/usr/include/rocksdb" ]; then
    echo "✅ Headers RocksDB trouvés dans /usr/include/rocksdb"
else
    echo "❌ Headers RocksDB non trouvés"
    exit 1
fi

echo ""
echo "🚀 Lancement de la compilation..."

# Exécuter la commande cargo avec l'environnement configuré
CARGO_CMD=${1:-check}
cargo $CARGO_CMD

echo ""
echo "✅ Compilation terminée avec succès !"
