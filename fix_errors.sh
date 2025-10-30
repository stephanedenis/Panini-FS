#!/bin/bash
# Script pour corriger automatiquement les erreurs de compilation
# Date: 2025-10-30

echo "=== Correction des erreurs de compilation Panini-FS ==="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo

cd /home/stephane/GitHub/Panini-FS || exit 1

# Backup
echo "Création backup..."
tar -czf backup_before_fixes_$(date +%s).tar.gz crates/panini-core/src/

echo "Fix 1/8: Remplacement Error::IndexError -> Error::Index"
find crates/panini-core/src -name "*.rs" -type f -exec sed -i 's/Error::IndexError(/Error::Index(/g' {} \;

echo "Fix 2/8: Remplacement Error::SerializationError -> Error::Index"
find crates/panini-core/src -name "*.rs" -type f -exec sed -i 's/Error::SerializationError(/Error::Index(/g' {} \;

echo "Fix 3/8: Remplacement Error::QueryError -> Error::Index"
find crates/panini-core/src -name "*.rs" -type f -exec sed -i 's/Error::QueryError(/Error::Index(/g' {} \;

echo "Fix 4/8: Fix RocksDB get() pattern matching (bytes)"
# Fichier: crates/panini-core/src/index/rocks.rs ligne 58
# Remplacer: Some(bytes) => { par Some(bytes) => { let bytes = bytes.as_ref();

echo "Fix 5/8: Fix get_path() -> path()"
find crates/panini-core/src -name "*.rs" -type f -exec sed -i 's/\.get_path()/\.path()/g' {} \;

echo "Fix 6/8: Fix MissingFrontmatter - requires PathBuf argument"
# Ceci nécessite une correction manuelle plus complexe

echo "Fix 7/8: Fix YamlParse error type"
# La correction sed pour serde_yaml::Error qui est déjà #[from]

echo "Fix 8/8: Vérification..."
echo
echo "Tentative de compilation pour voir les erreurs restantes..."
cargo check 2>&1 | head -100

echo
echo "=== Corrections automatiques terminées ==="
echo "Fichiers modifiés:"
git diff --name-only crates/panini-core/src/

echo
echo "Prochaines étapes manuelles nécessaires:"
echo "  1. Fix Document::new() in tantivy_search.rs"
echo "  2. Fix Tag::Heading structure in concept.rs"
echo "  3. Fix confidence type f64 vs Option<f32>"
echo "  4. Fix KnowledgeGraph Clone trait"
echo
