//! Tests de validation basiques avec l'API directe du CAS

use panini_core::storage::{ContentAddressedStorage, LocalFsBackend, StorageConfig, AtomType};
use sha2::{Digest, Sha256};
use std::sync::Arc;
use tempfile::TempDir;

/// Test basique : ajouter un atome et le récupérer
#[tokio::test]
async fn test_add_and_get_atom() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    // Ajouter un atome
    let data = b"Hello, World!";
    let atom = cas.add_atom(data, AtomType::Container).await.unwrap();
    
    println!("✓ Atome ajouté : {}", &atom.hash[..16]);
    
    // Récupérer l'atome
    let retrieved = cas.get_atom(&atom.hash).await.unwrap();
    
    assert_eq!(data.as_slice(), retrieved.as_ref(), "Données doivent être identiques");
    
    println!("✅ Test add_and_get réussi !");
}

/// Test de déduplication : même données = même hash
#[tokio::test]
async fn test_deduplication() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    let data = b"Same content";
    
    // Ajouter 2 fois
    let atom1 = cas.add_atom(data, AtomType::Container).await.unwrap();
    let atom2 = cas.add_atom(data, AtomType::Container).await.unwrap();
    
    assert_eq!(atom1.hash, atom2.hash, "Hashes doivent être identiques");
    
    // Vérifier stats
    let stats = cas.get_stats().await;
    println!("✓ Total atoms: {}", stats.total_atoms);
    println!("✓ Unique hashes: {}", stats.unique_atoms);
    println!("✓ Dedup ratio: {:.1}%", stats.dedup_ratio() * 100.0);
    
    println!("✅ Test déduplication réussi !");
}

/// Test avec multiples atomes différents
#[tokio::test]
async fn test_multiple_atoms() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    let mut hashes = Vec::new();
    
    // Ajouter 10 atomes différents
    for i in 0..10 {
        let data = format!("Atome numéro {}", i);
        let atom = cas.add_atom(data.as_bytes(), AtomType::Container).await.unwrap();
        hashes.push(atom.hash.clone());
        println!("  Ajouté : {}...", &atom.hash[..12]);
    }
    
    // Vérifier qu'on peut tous les récupérer
    for (i, hash) in hashes.iter().enumerate() {
        let retrieved = cas.get_atom(hash).await.unwrap();
        let expected = format!("Atome numéro {}", i);
        assert_eq!(expected.as_bytes(), retrieved.as_ref());
    }
    
    let stats = cas.get_stats().await;
    println!("✓ Stats : {} atomes, {} uniques", stats.total_atoms, stats.unique_atoms);
    
    println!("✅ Test multiples atomes réussi !");
}

/// Test de réutilisation : atomes communs entre "fichiers"
#[tokio::test]
async fn test_atom_reuse() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    // Simuler 3 "fichiers" avec contenu commun
    let common_chunk = b"Common data that appears in all files";
    
    let mut file1_atoms = Vec::new();
    let mut file2_atoms = Vec::new();
    let mut file3_atoms = Vec::new();
    
    // File 1 : common + unique1
    file1_atoms.push(cas.add_atom(common_chunk, AtomType::Container).await.unwrap().hash);
    file1_atoms.push(cas.add_atom(b"Unique to file 1", AtomType::Container).await.unwrap().hash);
    
    // File 2 : common + unique2
    file2_atoms.push(cas.add_atom(common_chunk, AtomType::Container).await.unwrap().hash);
    file2_atoms.push(cas.add_atom(b"Unique to file 2", AtomType::Container).await.unwrap().hash);
    
    // File 3 : common + unique3
    file3_atoms.push(cas.add_atom(common_chunk, AtomType::Container).await.unwrap().hash);
    file3_atoms.push(cas.add_atom(b"Unique to file 3", AtomType::Container).await.unwrap().hash);
    
    // Vérifier que le chunk commun a le même hash partout
    assert_eq!(file1_atoms[0], file2_atoms[0]);
    assert_eq!(file2_atoms[0], file3_atoms[0]);
    
    let stats = cas.get_stats().await;
    println!("✓ Total atoms: {}", stats.total_atoms); // 6 (3 common + 3 unique)
    println!("✓ Unique: {}", stats.unique_atoms); // 4 (1 common + 3 unique)
    println!("✓ Dedup ratio: {:.1}%", stats.dedup_ratio() * 100.0);
    
    // Ratio devrait être ~33% (2 sur 6 dédupliqués)
    assert!(stats.dedup_ratio() > 0.2, "Dedup ratio devrait être > 20%");
    
    println!("✅ Test réutilisation d'atomes réussi !");
}

/// Test bit-perfect : hash SHA256 avant/après
#[tokio::test]
async fn test_bitperfect_hash() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    // Données de test
    let original_data = b"This is test data for bit-perfect validation\n".repeat(100);
    
    // Hash original
    let original_hash = Sha256::digest(&original_data);
    let original_hash_str = format!("{:x}", original_hash);
    
    // Stocker
    let atom = cas.add_atom(&original_data, AtomType::Container).await.unwrap();
    
    // Récupérer
    let retrieved_data = cas.get_atom(&atom.hash).await.unwrap();
    
    // Hash récupéré
    let retrieved_hash = Sha256::digest(&retrieved_data);
    let retrieved_hash_str = format!("{:x}", retrieved_hash);
    
    assert_eq!(
        original_hash_str, retrieved_hash_str,
        "Hash SHA256 doit être identique (bit-perfect)"
    );
    
    assert_eq!(
        original_data.len(),
        retrieved_data.len(),
        "Taille doit être identique"
    );
    
    assert_eq!(
        original_data.as_slice(),
        retrieved_data.as_ref(),
        "Contenu doit être identique byte par byte"
    );
    
    println!("✓ Hash original   : {}...", &original_hash_str[..16]);
    println!("✓ Hash récupéré   : {}...", &retrieved_hash_str[..16]);
    println!("✅ Validation bit-perfect réussie !");
}
