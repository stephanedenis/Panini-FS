//! Tests sur données réelles : validation qualité sémantique
//!
//! Ce module teste le système sur de vrais fichiers des répertoires
//! ~/Downloads/ et ~/Documents/GitHub/CALMESD/

use panini_core::storage::{
    cas::ContentAddressedStorage,
    LocalFsBackend,
    StorageConfig,
    AtomType,
};
use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use tempfile::TempDir;

/// Statistiques d'analyse
#[derive(Debug, Default)]
struct AnalysisStats {
    files_processed: usize,
    files_skipped: usize,
    total_size: u64,
    total_atoms: usize,
    unique_atoms: HashSet<String>,
    atom_reuse: HashMap<String, usize>,
    errors: Vec<String>,
}

impl AnalysisStats {
    fn dedup_ratio(&self) -> f64 {
        if self.total_atoms == 0 {
            return 0.0;
        }
        1.0 - (self.unique_atoms.len() as f64 / self.total_atoms as f64)
    }
    
    fn avg_reuse(&self) -> f64 {
        if self.atom_reuse.is_empty() {
            return 0.0;
        }
        let total: usize = self.atom_reuse.values().sum();
        total as f64 / self.atom_reuse.len() as f64
    }
    
    fn print_report(&self, name: &str) {
        println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("📊 RAPPORT : {}", name);
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        
        println!("\n📁 Fichiers :");
        println!("  • Traités      : {}", self.files_processed);
        println!("  • Ignorés      : {}", self.files_skipped);
        println!("  • Taille totale: {:.2} MB", self.total_size as f64 / (1024.0 * 1024.0));
        
        println!("\n🧬 Décomposition :");
        println!("  • Atomes totaux : {}", self.total_atoms);
        println!("  • Atomes uniques: {}", self.unique_atoms.len());
        println!("  • Ratio dédup   : {:.1}%", self.dedup_ratio() * 100.0);
        
        println!("\n♻️  Réutilisation :");
        println!("  • Moyenne       : {:.2}x", self.avg_reuse());
        
        let shared = self.atom_reuse.values().filter(|&&c| c > 1).count();
        println!("  • Atomes partagés: {} ({:.1}%)",
                 shared,
                 shared as f64 / self.unique_atoms.len().max(1) as f64 * 100.0);
        
        if !self.errors.is_empty() {
            println!("\n⚠️  Erreurs : {} fichiers", self.errors.len());
        }
        
        // Top 5 atomes réutilisés
        let mut top: Vec<_> = self.atom_reuse.iter().collect();
        top.sort_by(|a, b| b.1.cmp(a.1));
        
        if !top.is_empty() {
            println!("\n🏆 Top 5 atomes réutilisés :");
            for (i, (hash, count)) in top.iter().take(5).enumerate() {
                println!("  {}. {}... → {}x", i + 1, &hash[..12], count);
            }
        }
        
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    }
}

/// Analyse un fichier et ajoute ses atomes au CAS
async fn analyze_file(
    path: &Path,
    cas: &ContentAddressedStorage<LocalFsBackend>,
    stats: &mut AnalysisStats,
) -> bool {
    // Lire le fichier
    let content = match fs::read(path) {
        Ok(c) => c,
        Err(e) => {
            stats.errors.push(format!("{}: {}", path.display(), e));
            stats.files_skipped += 1;
            return false;
        }
    };
    
    stats.total_size += content.len() as u64;
    
    // Découper en chunks de 64KB (taille optimale d'atome)
    let chunk_size = 64 * 1024;
    let mut atom_hashes = Vec::new();
    
    for chunk in content.chunks(chunk_size) {
        match cas.add_atom(chunk, AtomType::Container).await {
            Ok(atom) => {
                stats.total_atoms += 1;
                stats.unique_atoms.insert(atom.hash.clone());
                *stats.atom_reuse.entry(atom.hash.clone()).or_insert(0) += 1;
                atom_hashes.push(atom.hash);
            }
            Err(e) => {
                stats.errors.push(format!("Atom error in {}: {}", path.display(), e));
                return false;
            }
        }
    }
    
    // Vérifier bit-perfect : reconstruire et comparer hash
    let mut reconstructed = Vec::new();
    for hash in &atom_hashes {
        match cas.get_atom(hash).await {
            Ok(data) => reconstructed.extend_from_slice(&data),
            Err(e) => {
                stats.errors.push(format!("Reconstruction error: {}", e));
                return false;
            }
        }
    }
    
    // Comparer hashes SHA256
    let original_hash = Sha256::digest(&content);
    let reconstructed_hash = Sha256::digest(&reconstructed);
    
    if original_hash != reconstructed_hash {
        stats.errors.push(format!("Bit-perfect FAILED for {}", path.display()));
        return false;
    }
    
    stats.files_processed += 1;
    true
}

/// Analyse un répertoire (non récursif pour limiter le temps)
async fn analyze_directory(
    dir: &Path,
    cas: &ContentAddressedStorage<LocalFsBackend>,
    max_files: usize,
) -> AnalysisStats {
    let mut stats = AnalysisStats::default();
    
    let entries = match fs::read_dir(dir) {
        Ok(e) => e,
        Err(e) => {
            stats.errors.push(format!("Cannot read {}: {}", dir.display(), e));
            return stats;
        }
    };
    
    for entry in entries.flatten() {
        if stats.files_processed >= max_files {
            println!("  ⚠️  Limite de {} fichiers atteinte", max_files);
            break;
        }
        
        let path = entry.path();
        
        // Seulement les fichiers, pas les répertoires
        if !path.is_file() {
            continue;
        }
        
        // Ignorer les très gros fichiers (>50MB)
        if let Ok(metadata) = fs::metadata(&path) {
            if metadata.len() > 50 * 1024 * 1024 {
                stats.files_skipped += 1;
                continue;
            }
        }
        
        let filename = path.file_name().unwrap().to_string_lossy();
        print!("  📄 {}... ", &filename[..filename.len().min(40)]);
        std::io::Write::flush(&mut std::io::stdout()).ok();
        
        if analyze_file(&path, cas, &mut stats).await {
            println!("✓");
        } else {
            println!("✗");
        }
    }
    
    stats
}

/// Test sur Downloads/ (limité à 20 fichiers)
#[tokio::test]
#[ignore]
async fn test_downloads_directory() {
    let downloads = PathBuf::from("/home/stephane/Downloads");
    
    if !downloads.exists() {
        println!("⚠️  Répertoire Downloads non trouvé");
        return;
    }
    
    println!("\n🔍 ANALYSE : ~/Downloads/ (max 20 fichiers)");
    
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    let stats = analyze_directory(&downloads, &cas, 20).await;
    stats.print_report("~/Downloads/");
    
    // Assertions
    assert!(stats.files_processed > 0, "Au moins quelques fichiers devraient être traités");
    assert_eq!(stats.errors.iter().filter(|e| e.contains("Bit-perfect FAILED")).count(), 0,
               "Aucun échec bit-perfect autorisé");
}

/// Test sur CALMESD/ (limité à 30 fichiers)
#[tokio::test]
#[ignore]
async fn test_calmesd_directory() {
    let calmesd = PathBuf::from("/home/stephane/Documents/GitHub/CALMESD");
    
    if !calmesd.exists() {
        println!("⚠️  Répertoire CALMESD non trouvé");
        return;
    }
    
    println!("\n🔍 ANALYSE : CALMESD/ (max 30 fichiers)");
    
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    let stats = analyze_directory(&calmesd, &cas, 30).await;
    stats.print_report("CALMESD/");
    
    // Assertions
    assert!(stats.files_processed > 0, "Au moins quelques fichiers devraient être traités");
    assert_eq!(stats.errors.iter().filter(|e| e.contains("Bit-perfect FAILED")).count(), 0,
               "Aucun échec bit-perfect autorisé");
    
    // Pour du code source, on s'attend à une bonne déduplication
    if stats.files_processed > 5 {
        println!("ℹ️  Déduplication attendue pour code source : >15%");
    }
}

/// Test simple sur quelques fichiers
#[tokio::test]
async fn test_sample_files() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).unwrap());
    let config = StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend, config);
    
    let mut stats = AnalysisStats::default();
    
    // Créer 3 fichiers de test avec contenu plus gros pour avoir plusieurs chunks
    let common_part = "Common content line\n".repeat(5000); // ~100KB
    let test_files = vec![
        ("file1.txt", common_part.clone() + &"Unique 1\n".repeat(100)),
        ("file2.txt", common_part.clone() + &"Unique 2\n".repeat(100)),
        ("file3.txt", common_part.clone() + &"Unique 3\n".repeat(100)),
    ];
    
    for (name, content) in test_files {
        let path = temp_dir.path().join(name);
        fs::write(&path, content).unwrap();
        
        println!("  Analyse {}...", name);
        assert!(analyze_file(&path, &cas, &mut stats).await, "Devrait réussir");
    }
    
    stats.print_report("Test Sample");
    
    // Vérifications
    assert_eq!(stats.files_processed, 3, "3 fichiers devraient être traités");
    assert!(stats.total_atoms > 3, "Devrait avoir plusieurs atomes par fichier");
    
    // Avec du contenu commun, on devrait avoir de la déduplication
    if stats.total_atoms > 5 {
        assert!(stats.dedup_ratio() > 0.3, 
                "Devrait avoir >30% déduplication avec contenu commun (ratio: {:.1}%)", 
                stats.dedup_ratio() * 100.0);
    }
    
    println!("✅ Test sample réussi !");
}
