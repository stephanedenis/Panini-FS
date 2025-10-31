//! Tests de validation bit-perfect : reconstruction identique aux originaux
//!
//! Ce module teste que la décomposition/reconstruction produit des fichiers
//! binaires identiques bit-à-bit aux originaux.

use panini_core::storage::{
    cas::ContentAddressedStorage,
    LocalFsBackend,
    immutable::{Concept, ConceptVersion, TemporalIndex},
    StorageConfig,
};
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use tempfile::TempDir;

/// Calcule le hash SHA256 d'un fichier
fn hash_file(path: &Path) -> Result<String, std::io::Error> {
    let content = fs::read(path)?;
    let hash = Sha256::digest(&content);
    Ok(format!("{:x}", hash))
}

/// Calcule le hash d'une slice de bytes
fn hash_bytes(data: &[u8]) -> String {
    let hash = Sha256::digest(data);
    format!("{:x}", hash)
}

/// Test de reconstruction bit-perfect d'un fichier
#[tokio::test]
async fn test_bitperfect_reconstruction_single_file() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Créer un fichier test avec contenu aléatoire
    let test_file = temp_dir.path().join("original.bin");
    let original_content: Vec<u8> = (0..1024 * 1024) // 1 MB
        .map(|i| ((i * 7 + 13) % 256) as u8)
        .collect();
    fs::write(&test_file, &original_content).unwrap();
    
    // Hash original
    let original_hash = hash_bytes(&original_content);
    
    // Décomposer le fichier
    let atom_ids = cas.store_file(&test_file).await.unwrap();
    println!("✓ Fichier décomposé en {} atomes", atom_ids.len());
    
    // Reconstruire le fichier
    let reconstructed_file = temp_dir.path().join("reconstructed.bin");
    cas.reconstruct_file(&atom_ids, &reconstructed_file)
        .await
        .unwrap();
    
    // Vérifier bit-perfect
    let reconstructed_content = fs::read(&reconstructed_file).unwrap();
    let reconstructed_hash = hash_bytes(&reconstructed_content);
    
    assert_eq!(
        original_hash, reconstructed_hash,
        "Reconstruction doit être bit-perfect"
    );
    assert_eq!(
        original_content.len(),
        reconstructed_content.len(),
        "Taille doit être identique"
    );
    assert_eq!(
        original_content, reconstructed_content,
        "Contenu doit être identique byte par byte"
    );
    
    println!("✅ Reconstruction bit-perfect validée");
}

/// Test sur plusieurs fichiers de types différents
#[tokio::test]
async fn test_bitperfect_multiple_file_types() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Créer différents types de fichiers
    let test_files = vec![
        ("text.txt", b"Hello World!\n".repeat(1000).as_slice()),
        ("binary.bin", &[0u8, 255, 128, 64, 32, 16, 8, 4, 2, 1].repeat(10000)),
        ("zeros.dat", &[0u8; 100000]),
        ("pattern.dat", &(0u8..255).cycle().take(50000).collect::<Vec<_>>()),
    ];
    
    for (filename, content) in test_files {
        let original_file = temp_dir.path().join(filename);
        fs::write(&original_file, content).unwrap();
        let original_hash = hash_bytes(content);
        
        // Décomposer
        let atom_ids = cas.store_file(&original_file).await.unwrap();
        
        // Reconstruire
        let reconstructed_file = temp_dir.path().join(format!("reconstructed_{}", filename));
        cas.reconstruct_file(&atom_ids, &reconstructed_file)
            .await
            .unwrap();
        
        // Vérifier
        let reconstructed_content = fs::read(&reconstructed_file).unwrap();
        let reconstructed_hash = hash_bytes(&reconstructed_content);
        
        assert_eq!(
            original_hash, reconstructed_hash,
            "Reconstruction bit-perfect échouée pour {}",
            filename
        );
        
        println!("✅ {} : bit-perfect validé ({} bytes)", filename, content.len());
    }
}

/// Test avec versioning : plusieurs versions doivent rester bit-perfect
#[tokio::test]
async fn test_bitperfect_versioning() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    let mut index = TemporalIndex::new();
    
    // Version 1
    let v1_content = b"Version 1 content\n".repeat(1000);
    let v1_file = temp_dir.path().join("v1.txt");
    fs::write(&v1_file, &v1_content).unwrap();
    let v1_hash = hash_bytes(&v1_content);
    
    let v1_atoms = cas.store_file(&v1_file).await.unwrap();
    let concept_v1 = Concept::new("test-concept".to_string(), v1_atoms.clone());
    index.add_concept(concept_v1.clone());
    
    // Version 2 (modification)
    let v2_content = b"Version 2 modified content\n".repeat(1500);
    let v2_file = temp_dir.path().join("v2.txt");
    fs::write(&v2_file, &v2_content).unwrap();
    let v2_hash = hash_bytes(&v2_content);
    
    let v2_atoms = cas.store_file(&v2_file).await.unwrap();
    index.update_concept("test-concept", v2_atoms.clone());
    
    // Reconstruire v1
    let reconstructed_v1 = temp_dir.path().join("reconstructed_v1.txt");
    cas.reconstruct_file(&v1_atoms, &reconstructed_v1)
        .await
        .unwrap();
    let recon_v1_hash = hash_bytes(&fs::read(&reconstructed_v1).unwrap());
    
    // Reconstruire v2
    let reconstructed_v2 = temp_dir.path().join("reconstructed_v2.txt");
    cas.reconstruct_file(&v2_atoms, &reconstructed_v2)
        .await
        .unwrap();
    let recon_v2_hash = hash_bytes(&fs::read(&reconstructed_v2).unwrap());
    
    assert_eq!(v1_hash, recon_v1_hash, "Version 1 doit rester bit-perfect");
    assert_eq!(v2_hash, recon_v2_hash, "Version 2 doit être bit-perfect");
    
    println!("✅ Versioning bit-perfect : V1 et V2 validées");
}

/// Test de reconstruction après snapshot
#[tokio::test]
async fn test_bitperfect_after_snapshot() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    let mut index = TemporalIndex::new();
    
    // Créer plusieurs concepts
    let mut original_hashes = HashMap::new();
    
    for i in 0..5 {
        let content = format!("Concept {} content\n", i).repeat(500).into_bytes();
        let file = temp_dir.path().join(format!("concept_{}.txt", i));
        fs::write(&file, &content).unwrap();
        
        let hash = hash_bytes(&content);
        original_hashes.insert(format!("concept-{}", i), hash);
        
        let atoms = cas.store_file(&file).await.unwrap();
        let concept = Concept::new(format!("concept-{}", i), atoms);
        index.add_concept(concept);
    }
    
    // Créer snapshot
    index.create_snapshot("test-snapshot".to_string());
    
    // Reconstruire tous les concepts depuis le snapshot
    let snapshot = index.get_snapshot("test-snapshot").unwrap();
    
    for (concept_id, version) in &snapshot.concepts {
        let reconstructed = temp_dir.path().join(format!("reconstructed_{}.txt", concept_id));
        cas.reconstruct_file(&version.atom_ids, &reconstructed)
            .await
            .unwrap();
        
        let reconstructed_hash = hash_bytes(&fs::read(&reconstructed).unwrap());
        let original_hash = original_hashes.get(concept_id).unwrap();
        
        assert_eq!(
            original_hash, &reconstructed_hash,
            "Concept {} doit être bit-perfect après snapshot",
            concept_id
        );
        
        println!("✅ {} : bit-perfect après snapshot", concept_id);
    }
}

/// Test de stress : 100 fichiers aléatoires
#[tokio::test]
#[ignore] // Long à exécuter
async fn test_bitperfect_stress() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    let mut successes = 0;
    let mut total_size = 0u64;
    
    for i in 0..100 {
        // Générer contenu aléatoire de taille variable
        let size = 1024 + (i * 10240); // De 1KB à ~1MB
        let content: Vec<u8> = (0..size)
            .map(|j| ((i + j) % 256) as u8)
            .collect();
        
        let original_file = temp_dir.path().join(format!("stress_{}.bin", i));
        fs::write(&original_file, &content).unwrap();
        let original_hash = hash_bytes(&content);
        
        // Décomposer
        let atoms = cas.store_file(&original_file).await.unwrap();
        
        // Reconstruire
        let reconstructed_file = temp_dir.path().join(format!("stress_recon_{}.bin", i));
        cas.reconstruct_file(&atoms, &reconstructed_file)
            .await
            .unwrap();
        
        // Vérifier
        let reconstructed_content = fs::read(&reconstructed_file).unwrap();
        let reconstructed_hash = hash_bytes(&reconstructed_content);
        
        if original_hash == reconstructed_hash {
            successes += 1;
            total_size += size as u64;
        }
        
        if i % 10 == 0 {
            println!("✓ Progression : {}/100 fichiers", i);
        }
    }
    
    assert_eq!(successes, 100, "Tous les fichiers doivent être bit-perfect");
    println!("✅ Stress test : 100/100 fichiers bit-perfect ({} MB total)", 
             total_size / (1024 * 1024));
}
