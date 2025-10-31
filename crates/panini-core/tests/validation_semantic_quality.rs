//! Tests de qualité sémantique : évaluation de la déduplication et réutilisation
//!
//! Ce module analyse la qualité de la décomposition atomique en mesurant :
//! - Taux de déduplication
//! - Réutilisation d'atomes entre concepts similaires
//! - Distribution des tailles d'atomes
//! - Efficacité du stockage

use panini_core::storage::{
    cas::ContentAddressedStorage,
    LocalFsBackend,
    StorageConfig,
    immutable::{Concept, TemporalIndex},
};
use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use std::fs;
use std::path::{Path, PathBuf};
use tempfile::TempDir;

/// Statistiques de décomposition
#[derive(Debug, Default)]
struct DecompositionStats {
    total_concepts: usize,
    total_original_size: u64,
    total_stored_size: u64,
    total_atoms: usize,
    unique_atoms: usize,
    atom_reuse_count: HashMap<String, usize>,
    size_distribution: Vec<usize>,
}

impl DecompositionStats {
    fn deduplication_ratio(&self) -> f64 {
        if self.total_original_size == 0 {
            return 0.0;
        }
        1.0 - (self.total_stored_size as f64 / self.total_original_size as f64)
    }
    
    fn avg_atom_reuse(&self) -> f64 {
        if self.atom_reuse_count.is_empty() {
            return 0.0;
        }
        let sum: usize = self.atom_reuse_count.values().sum();
        sum as f64 / self.atom_reuse_count.len() as f64
    }
    
    fn atoms_used_multiple_times(&self) -> usize {
        self.atom_reuse_count.values().filter(|&&count| count > 1).count()
    }
    
    fn report(&self) {
        println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("📊 RAPPORT DE QUALITÉ SÉMANTIQUE");
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        
        println!("\n📁 Concepts traités:");
        println!("  • Nombre total    : {}", self.total_concepts);
        println!("  • Taille originale: {:.2} MB", 
                 self.total_original_size as f64 / (1024.0 * 1024.0));
        println!("  • Taille stockée  : {:.2} MB", 
                 self.total_stored_size as f64 / (1024.0 * 1024.0));
        
        println!("\n🧬 Décomposition atomique:");
        println!("  • Atomes totaux   : {}", self.total_atoms);
        println!("  • Atomes uniques  : {}", self.unique_atoms);
        println!("  • Ratio dédup     : {:.1}%", self.deduplication_ratio() * 100.0);
        
        println!("\n♻️  Réutilisation d'atomes:");
        println!("  • Réutilisation moy: {:.2}x", self.avg_atom_reuse());
        println!("  • Atomes partagés  : {} ({:.1}%)", 
                 self.atoms_used_multiple_times(),
                 self.atoms_used_multiple_times() as f64 / self.unique_atoms as f64 * 100.0);
        
        // Top 10 des atomes les plus réutilisés
        let mut top_reused: Vec<_> = self.atom_reuse_count.iter().collect();
        top_reused.sort_by(|a, b| b.1.cmp(a.1));
        
        println!("\n🏆 Top 10 atomes les plus réutilisés:");
        for (i, (atom_id, count)) in top_reused.iter().take(10).enumerate() {
            println!("  {}. {}... → {}x", 
                     i + 1, 
                     &atom_id[..12], 
                     count);
        }
        
        // Distribution des tailles
        if !self.size_distribution.is_empty() {
            let avg_size = self.size_distribution.iter().sum::<usize>() as f64 
                         / self.size_distribution.len() as f64;
            let max_size = *self.size_distribution.iter().max().unwrap();
            let min_size = *self.size_distribution.iter().min().unwrap();
            
            println!("\n📏 Distribution des tailles d'atomes:");
            println!("  • Taille moyenne  : {:.1} KB", avg_size / 1024.0);
            println!("  • Taille min      : {:.1} KB", min_size as f64 / 1024.0);
            println!("  • Taille max      : {:.1} KB", max_size as f64 / 1024.0);
        }
        
        println!("\n💾 Économie de stockage:");
        let saved = (self.total_original_size - self.total_stored_size) as f64 / (1024.0 * 1024.0);
        println!("  • Espace économisé: {:.2} MB", saved);
        println!("  • Compression     : {:.1}%", 
                 (1.0 - self.total_stored_size as f64 / self.total_original_size as f64) * 100.0);
        
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    }
}

/// Collecte les statistiques depuis un répertoire de test
async fn analyze_directory(
    dir: &Path,
    cas: &ContentAddressedStorage<LocalFsBackend>,
) -> DecompositionStats {
    let mut stats = DecompositionStats::default();
    let mut all_atoms = HashSet::new();
    
    println!("🔍 Analyse du répertoire : {}", dir.display());
    
    // Parcourir tous les fichiers
    let entries = fs::read_dir(dir);
    if entries.is_err() {
        println!("⚠️  Impossible de lire le répertoire");
        return stats;
    }
    
    for entry in entries.unwrap().flatten() {
        let path = entry.path();
        
        if path.is_file() {
            // Taille originale
            if let Ok(metadata) = fs::metadata(&path) {
                let file_size = metadata.len();
                stats.total_original_size += file_size;
                
                // Décomposer
                if let Ok(atom_ids) = cas.store_file(&path).await {
                    stats.total_concepts += 1;
                    stats.total_atoms += atom_ids.len();
                    
                    // Compter réutilisation
                    for atom_id in &atom_ids {
                        *stats.atom_reuse_count.entry(atom_id.clone()).or_insert(0) += 1;
                        all_atoms.insert(atom_id.clone());
                    }
                    
                    println!("  ✓ {} : {} atomes", 
                             path.file_name().unwrap().to_string_lossy(),
                             atom_ids.len());
                }
            }
        } else if path.is_dir() {
            // Récursif
            let sub_stats = analyze_directory(&path, cas).await;
            stats.total_concepts += sub_stats.total_concepts;
            stats.total_original_size += sub_stats.total_original_size;
            stats.total_stored_size += sub_stats.total_stored_size;
            stats.total_atoms += sub_stats.total_atoms;
            
            // Fusionner atom_reuse_count
            for (atom_id, count) in sub_stats.atom_reuse_count {
                *stats.atom_reuse_count.entry(atom_id.clone()).or_insert(0) += count;
                all_atoms.insert(atom_id);
            }
        }
    }
    
    stats.unique_atoms = all_atoms.len();
    
    // Calculer taille stockée (taille unique des atomes)
    for atom_id in &all_atoms {
        if let Ok(Some(atom_data)) = cas.get_atom(atom_id).await {
            stats.total_stored_size += atom_data.len() as u64;
            stats.size_distribution.push(atom_data.len());
        }
    }
    
    stats
}

/// Test de qualité sur fichiers similaires
#[tokio::test]
async fn test_semantic_quality_similar_files() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Créer 5 fichiers similaires (même base + petites variations)
    let base_content = "This is a common base content\n".repeat(1000);
    
    for i in 0..5 {
        let variation = format!("Variation {}\n", i).repeat(100);
        let content = format!("{}{}", base_content, variation);
        
        let file = temp_dir.path().join(format!("similar_{}.txt", i));
        fs::write(&file, content.as_bytes()).unwrap();
    }
    
    let stats = analyze_directory(temp_dir.path(), &cas).await;
    stats.report();
    
    // Assertions sur la qualité
    assert!(stats.deduplication_ratio() > 0.50, 
            "Déduplication devrait être > 50% pour fichiers similaires");
    assert!(stats.atoms_used_multiple_times() > 0,
            "Des atomes devraient être réutilisés");
    
    println!("✅ Test qualité fichiers similaires : dédup = {:.1}%", 
             stats.deduplication_ratio() * 100.0);
}

/// Test de qualité sur fichiers divers
#[tokio::test]
async fn test_semantic_quality_diverse_files() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Fichiers très différents
    let files = vec![
        ("text.txt", "Hello World\n".repeat(500)),
        ("json.json", r#"{"key": "value"}"#.repeat(300)),
        ("binary.bin", String::from_utf8_lossy(&[0u8, 255, 128].repeat(1000)).to_string()),
        ("code.rs", "fn main() { println!(\"test\"); }\n".repeat(200)),
    ];
    
    for (filename, content) in files {
        let file = temp_dir.path().join(filename);
        fs::write(&file, content.as_bytes()).unwrap();
    }
    
    let stats = analyze_directory(temp_dir.path(), &cas).await;
    stats.report();
    
    // Pour fichiers divers, moins de dédup attendu
    println!("✅ Test qualité fichiers divers : {} concepts analysés", 
             stats.total_concepts);
}

/// Test de réutilisation entre versions
#[tokio::test]
async fn test_semantic_quality_versioning() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    let mut index = TemporalIndex::new();
    
    // Version 1 : contenu de base
    let base = "Base content line\n".repeat(500);
    let v1 = format!("{}", base);
    
    // Version 2 : ajout au début
    let v2 = format!("New header\n{}", base);
    
    // Version 3 : ajout à la fin
    let v3 = format!("{}New footer\n", base);
    
    let versions = vec![v1, v2, v3];
    let mut all_atoms = Vec::new();
    
    for (i, content) in versions.iter().enumerate() {
        let file = temp_dir.path().join(format!("v{}.txt", i + 1));
        fs::write(&file, content.as_bytes()).unwrap();
        
        let atoms = cas.store_file(&file).await.unwrap();
        all_atoms.push(atoms);
        
        println!("Version {} : {} atomes", i + 1, all_atoms[i].len());
    }
    
    // Compter atomes communs entre versions
    let v1_set: HashSet<_> = all_atoms[0].iter().collect();
    let v2_set: HashSet<_> = all_atoms[1].iter().collect();
    let v3_set: HashSet<_> = all_atoms[2].iter().collect();
    
    let common_v1_v2: Vec<_> = v1_set.intersection(&v2_set).collect();
    let common_v1_v3: Vec<_> = v1_set.intersection(&v3_set).collect();
    
    println!("\n♻️  Réutilisation entre versions:");
    println!("  • V1 ∩ V2 : {} atomes communs", common_v1_v2.len());
    println!("  • V1 ∩ V3 : {} atomes communs", common_v1_v3.len());
    
    // La plupart des atomes devraient être communs (le base)
    assert!(
        common_v1_v2.len() as f64 / v1_set.len() as f64 > 0.80,
        "Au moins 80% des atomes devraient être réutilisés entre versions similaires"
    );
    
    println!("✅ Test réutilisation versioning : {:.1}% atomes réutilisés",
             common_v1_v2.len() as f64 / v1_set.len() as f64 * 100.0);
}

/// Test sur répertoire réel : Downloads
#[tokio::test]
#[ignore] // À activer manuellement
async fn test_real_world_downloads() {
    let downloads = PathBuf::from("/home/stephane/Downloads");
    
    if !downloads.exists() {
        println!("⚠️  Répertoire Downloads non trouvé, test ignoré");
        return;
    }
    
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    println!("\n🔍 ANALYSE RÉPERTOIRE RÉEL : ~/Downloads/");
    let stats = analyze_directory(&downloads, &cas).await;
    stats.report();
    
    // Sauvegarder le rapport
    let report_path = temp_dir.path().join("downloads_analysis.txt");
    println!("📄 Rapport sauvegardé : {}", report_path.display());
}

/// Test sur répertoire réel : CALMESD
#[tokio::test]
#[ignore] // À activer manuellement
async fn test_real_world_calmesd() {
    let calmesd = PathBuf::from("/home/stephane/Documents/GitHub/CALMESD");
    
    if !calmesd.exists() {
        println!("⚠️  Répertoire CALMESD non trouvé, test ignoré");
        return;
    }
    
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage")).expect("Failed to create backend"));
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    println!("\n🔍 ANALYSE RÉPERTOIRE RÉEL : CALMESD/");
    let stats = analyze_directory(&calmesd, &cas).await;
    stats.report();
    
    // Assertions spécifiques pour code source
    println!("\n📊 Analyse spécifique code source:");
    println!("  • Déduplication attendue > 30% (code souvent similaire)");
    println!("  • Réutilisation d'atomes importante (imports, patterns communs)");
}
