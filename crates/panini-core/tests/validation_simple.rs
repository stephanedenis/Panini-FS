//! Test de validation simple : bit-perfect avec l'API existante

use panini_core::storage::{
    ContentAddressedStorage, LocalFsBackend, StorageConfig, Decomposer, Reconstructor, FileFormat,
};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::Path;
use std::sync::Arc;
use tempfile::TempDir;

fn hash_file(path: &Path) -> Result<String, std::io::Error> {
    let content = fs::read(path)?;
    let hash = Sha256::digest(&content);
    Ok(format!("{:x}", hash))
}

#[tokio::test]
async fn test_bitperfect_simple() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = Arc::new(ContentAddressedStorage::new(backend.clone(), config));
    
    // Créer fichier test
    let test_file = temp_dir.path().join("test.txt");
    let content = "Hello World\n".repeat(1000);
    fs::write(&test_file, &content).unwrap();
    
    let original_hash = hash_file(&test_file).unwrap();
    println!("✓ Hash original : {}", &original_hash[..16]);
    
    // Décomposer
    let decomposer = Decomposer::new(cas.clone(), FileFormat::Auto);
    let atom_ids = decomposer.decompose_file(&test_file).await.unwrap();
    println!("✓ Décomposé en {} atomes", atom_ids.len());
    
    // Reconstruire
    let reconstructed = temp_dir.path().join("reconstructed.txt");
    let reconstructor = Reconstructor::new(cas.clone());
    reconstructor
        .reconstruct_file(&atom_ids, &reconstructed)
        .await
        .unwrap();
    
    // Vérifier
    let reconstructed_hash = hash_file(&reconstructed).unwrap();
    
    assert_eq!(
        original_hash, reconstructed_hash,
        "Reconstruction doit être bit-perfect"
    );
    
    println!("✅ Test bit-perfect réussi !");
}

#[tokio::test]
async fn test_semantic_quality_simple() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = Arc::new(ContentAddressedStorage::new(backend.clone(), config));
    
    // Créer 3 fichiers similaires
    let decomposer = Decomposer::new(cas.clone(), FileFormat::Auto);
    let base = "Base content\n".repeat(100);
    
    let mut all_atoms = Vec::new();
    for i in 0..3 {
        let variation = format!("Variation {}\n", i).repeat(10);
        let content = format!("{}{}", base, variation);
        
        let file = temp_dir.path().join(format!("file_{}.txt", i));
        fs::write(&file, content).unwrap();
        
        let atoms = decomposer.decompose_file(&file).await.unwrap();
        all_atoms.push(atoms);
        println!("✓ Fichier {} : {} atomes", i, all_atoms[i].len());
    }
    
    // Compter atomes communs
    let common: Vec<_> = all_atoms[0]
        .iter()
        .filter(|a| all_atoms[1].contains(a) && all_atoms[2].contains(a))
        .collect();
    
    let reuse_pct = common.len() as f64 / all_atoms[0].len() as f64 * 100.0;
    
    println!("♻️  Réutilisation : {:.1}%", reuse_pct);
    println!("✅ Test qualité sémantique réussi !");
    
    assert!(reuse_pct > 70.0, "Au moins 70% des atomes devraient être réutilisés");
}
