//! Outil CLI d'analyse de répertoires : validation et qualité sémantique
//!
//! Utilisation :
//!   panini-analyzer <path> [options]
//!
//! Options :
//!   --bit-perfect    : Valider reconstruction bit-perfect
//!   --semantic       : Analyser qualité sémantique (dédup, réutilisation)
//!   --report <file>  : Sauvegarder rapport détaillé
//!   --recursive      : Analyser sous-répertoires
//!   --max-size <MB>  : Limiter taille totale analysée

use panini_core::storage::{
    cas::ContentAddressedStorage,
    LocalFsBackend,
    StorageConfig,
};
use clap::{Parser, Subcommand};
use colored::*;
use sha2::Sha256;
use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;

#[derive(Parser)]
#[command(name = "panini-analyzer")]
#[command(about = "Analyse et validation de répertoires avec Panini-FS", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Analyse complète d'un répertoire
    Analyze {
        /// Chemin du répertoire à analyser
        path: PathBuf,
        
        /// Mode bit-perfect : valider reconstruction identique
        #[arg(long)]
        bit_perfect: bool,
        
        /// Mode sémantique : analyser déduplication et réutilisation
        #[arg(long)]
        semantic: bool,
        
        /// Analyser récursivement les sous-répertoires
        #[arg(short, long)]
        recursive: bool,
        
        /// Taille maximale à analyser (en MB)
        #[arg(long, default_value = "1000")]
        max_size: u64,
        
        /// Fichier de sortie pour le rapport
        #[arg(short, long)]
        output: Option<PathBuf>,
    },
    
    /// Comparer deux répertoires
    Compare {
        /// Premier répertoire
        path1: PathBuf,
        
        /// Second répertoire
        path2: PathBuf,
        
        /// Afficher atomes communs
        #[arg(long)]
        show_common: bool,
    },
    
    /// Benchmark de performance
    Benchmark {
        /// Répertoire à tester
        path: PathBuf,
        
        /// Nombre d'itérations
        #[arg(short, long, default_value = "3")]
        iterations: usize,
    },
}

#[derive(Debug, Default)]
struct AnalysisReport {
    start_time: Option<Instant>,
    total_files: usize,
    total_size: u64,
    processed_files: usize,
    processed_size: u64,
    total_atoms: usize,
    unique_atoms: usize,
    atom_reuse: HashMap<String, usize>,
    errors: Vec<String>,
    bit_perfect_ok: usize,
    bit_perfect_fail: usize,
}

impl AnalysisReport {
    fn new() -> Self {
        Self {
            start_time: Some(Instant::now()),
            ..Default::default()
        }
    }
    
    fn dedup_ratio(&self) -> f64 {
        if self.processed_size == 0 {
            return 0.0;
        }
        
        let unique_size: u64 = self.atom_reuse.len() as u64 * 64 * 1024; // Approximation
        1.0 - (unique_size as f64 / self.processed_size as f64)
    }
    
    fn avg_reuse(&self) -> f64 {
        if self.atom_reuse.is_empty() {
            return 0.0;
        }
        let total: usize = self.atom_reuse.values().sum();
        total as f64 / self.atom_reuse.len() as f64
    }
    
    fn print_summary(&self) {
        println!("\n{}", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".bright_purple().bold());
        println!("{}", "📊 RAPPORT D'ANALYSE".bright_purple().bold());
        println!("{}", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".bright_purple().bold());
        
        if let Some(start) = self.start_time {
            let duration = start.elapsed();
            println!("\n⏱️  Durée : {:.2}s", duration.as_secs_f64());
        }
        
        println!("\n{}", "📁 Fichiers analysés :".bright_cyan().bold());
        println!("  • Total trouvés    : {}", self.total_files.to_string().bright_white());
        println!("  • Traités          : {}", self.processed_files.to_string().bright_green());
        println!("  • Taille originale : {:.2} MB", 
                 (self.processed_size as f64 / (1024.0 * 1024.0)).to_string().bright_white());
        
        println!("\n{}", "🧬 Décomposition atomique :".bright_cyan().bold());
        println!("  • Atomes totaux    : {}", self.total_atoms.to_string().bright_white());
        println!("  • Atomes uniques   : {}", self.unique_atoms.to_string().bright_green());
        println!("  • Ratio dédup      : {:.1}%", 
                 (self.dedup_ratio() * 100.0).to_string().bright_yellow());
        
        println!("\n{}", "♻️  Réutilisation :".bright_cyan().bold());
        println!("  • Moyenne          : {:.2}x", 
                 self.avg_reuse().to_string().bright_yellow());
        println!("  • Atomes partagés  : {} ({:.1}%)",
                 self.atom_reuse.values().filter(|&&c| c > 1).count().to_string().bright_green(),
                 (self.atom_reuse.values().filter(|&&c| c > 1).count() as f64 
                  / self.unique_atoms as f64 * 100.0));
        
        if self.bit_perfect_ok > 0 || self.bit_perfect_fail > 0 {
            println!("\n{}", "🎯 Validation bit-perfect :".bright_cyan().bold());
            println!("  • Succès           : {}", self.bit_perfect_ok.to_string().bright_green());
            println!("  • Échecs           : {}", self.bit_perfect_fail.to_string().bright_red());
        }
        
        if !self.errors.is_empty() {
            println!("\n{}", "⚠️  Erreurs :".bright_yellow().bold());
            for (i, error) in self.errors.iter().take(5).enumerate() {
                println!("  {}. {}", i + 1, error);
            }
            if self.errors.len() > 5 {
                println!("  ... et {} autres", self.errors.len() - 5);
            }
        }
        
        // Top 10 atomes réutilisés
        let mut top: Vec<_> = self.atom_reuse.iter().collect();
        top.sort_by(|a, b| b.1.cmp(a.1));
        
        if !top.is_empty() {
            println!("\n{}", "🏆 Top 10 atomes les plus réutilisés :".bright_cyan().bold());
            for (i, (atom_id, count)) in top.iter().take(10).enumerate() {
                println!("  {}. {}... → {}x",
                         (i + 1).to_string().bright_white(),
                         atom_id[..12].bright_yellow(),
                         count.to_string().bright_green());
            }
        }
        
        println!("\n{}", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".bright_purple().bold());
    }
    
    fn save_to_file(&self, path: &Path) -> std::io::Result<()> {
        let mut content = String::new();
        content.push_str("# Panini-FS Analysis Report\n\n");
        content.push_str(&format!("Total files: {}\n", self.total_files));
        content.push_str(&format!("Processed: {}\n", self.processed_files));
        content.push_str(&format!("Total size: {} MB\n", self.processed_size / (1024 * 1024)));
        content.push_str(&format!("Total atoms: {}\n", self.total_atoms));
        content.push_str(&format!("Unique atoms: {}\n", self.unique_atoms));
        content.push_str(&format!("Dedup ratio: {:.1}%\n", self.dedup_ratio() * 100.0));
        content.push_str(&format!("Avg reuse: {:.2}x\n", self.avg_reuse()));
        
        if self.bit_perfect_ok > 0 || self.bit_perfect_fail > 0 {
            content.push_str("\n## Bit-perfect validation\n");
            content.push_str(&format!("Success: {}\n", self.bit_perfect_ok));
            content.push_str(&format!("Failures: {}\n", self.bit_perfect_fail));
        }
        
        fs::write(path, content)?;
        Ok(())
    }
}

async fn analyze_directory(
    path: &Path,
    cas: &ContentAddressedStorage<LocalFsBackend>,
    report: &mut AnalysisReport,
    bit_perfect: bool,
    recursive: bool,
    max_size: u64,
) -> Result<(), Box<dyn std::error::Error>> {
    
    if !path.exists() {
        return Err(format!("Chemin introuvable : {}", path.display()).into());
    }
    
    let entries = fs::read_dir(path)?;
    
    for entry in entries.flatten() {
        let entry_path = entry.path();
        
        if entry_path.is_file() {
            // Vérifier limite de taille
            if report.processed_size >= max_size * 1024 * 1024 {
                println!("{}", "⚠️  Limite de taille atteinte".bright_yellow());
                break;
            }
            
            let metadata = fs::metadata(&entry_path)?;
            let file_size = metadata.len();
            
            report.total_files += 1;
            report.total_size += file_size;
            
            // Décomposer le fichier
            print!("  📄 {} ... ", 
                   entry_path.file_name().unwrap().to_string_lossy().bright_white());
            
            match cas.store_file(&entry_path).await {
                Ok(atom_ids) => {
                    report.processed_files += 1;
                    report.processed_size += file_size;
                    report.total_atoms += atom_ids.len();
                    
                    // Compter réutilisation
                    for atom_id in &atom_ids {
                        *report.atom_reuse.entry(atom_id.clone()).or_insert(0) += 1;
                    }
                    
                    println!("{} ({} atomes)", 
                             "✓".bright_green(),
                             atom_ids.len().to_string().bright_cyan());
                    
                    // Test bit-perfect si demandé
                    if bit_perfect {
                        let temp_file = std::env::temp_dir().join("panini_verify.tmp");
                        
                        if cas.reconstruct_file(&atom_ids, &temp_file).await.is_ok() {
                            let original = fs::read(&entry_path)?;
                            let reconstructed = fs::read(&temp_file)?;
                            
                            if original == reconstructed {
                                report.bit_perfect_ok += 1;
                            } else {
                                report.bit_perfect_fail += 1;
                                println!("    {} Reconstruction différente !",
                                         "⚠️".bright_red());
                            }
                            
                            let _ = fs::remove_file(temp_file);
                        }
                    }
                }
                Err(e) => {
                    println!("{} {}", "✗".bright_red(), e);
                    report.errors.push(format!("{}: {}", entry_path.display(), e));
                }
            }
        } else if entry_path.is_dir() && recursive {
            println!("\n{} {} ...",
                     "📁".bright_blue(),
                     entry_path.file_name().unwrap().to_string_lossy().bright_white());
            
            analyze_directory(&entry_path, cas, report, bit_perfect, recursive, max_size).await?;
        }
    }
    
    report.unique_atoms = report.atom_reuse.len();
    
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Analyze {
            path,
            bit_perfect,
            semantic,
            recursive,
            max_size,
            output,
        } => {
            println!("{}", "🔍 PANINI-FS ANALYZER".bright_purple().bold());
            println!("{}", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".bright_purple());
            println!("\n📂 Analyse : {}", path.display().to_string().bright_white());
            
            if bit_perfect {
                println!("🎯 Mode : {}", "Validation bit-perfect".bright_green());
            }
            if semantic {
                println!("🧬 Mode : {}", "Analyse sémantique".bright_green());
            }
            if recursive {
                println!("♻️  Mode : {}", "Récursif".bright_green());
            }
            
            println!();
            
            // Créer stockage temporaire
            let temp_dir = tempfile::TempDir::new()?;
            let backend = Arc::new(LocalFsBackend::new(temp_dir.path().join("storage"))?);
            let config = StorageConfig::default();
            let cas = ContentAddressedStorage::new(backend, config);
            
            let mut report = AnalysisReport::new();
            
            analyze_directory(&path, &cas, &mut report, bit_perfect, recursive, max_size).await?;
            
            report.print_summary();
            
            if let Some(output_path) = output {
                report.save_to_file(&output_path)?;
                println!("\n📄 Rapport sauvegardé : {}", 
                         output_path.display().to_string().bright_cyan());
            }
        }
        
        Commands::Compare { path1, path2, show_common } => {
            println!("{}", "🔀 COMPARAISON DE RÉPERTOIRES".bright_purple().bold());
            println!("{}", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".bright_purple());
            
            // TODO: Implémenter comparaison
            println!("⚠️  Fonctionnalité en développement");
        }
        
        Commands::Benchmark { path, iterations } => {
            println!("{}", "⚡ BENCHMARK DE PERFORMANCE".bright_purple().bold());
            println!("{}", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".bright_purple());
            
            // TODO: Implémenter benchmark
            println!("⚠️  Fonctionnalité en développement");
        }
    }
    
    Ok(())
}
