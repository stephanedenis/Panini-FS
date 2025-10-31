//! Test de Stress : Décomposition Atomique de Vidéos Réelles
//!
//! Ce programme teste la décomposition atomique sur toutes les vidéos
//! d'un répertoire réel pour évaluer :
//! - Granularité (nombre d'atomes par vidéo)
//! - Déduplication (économies entre vidéos)
//! - Reconstruction bit-perfect (vérification SHA-256)
//! - Performance (temps de traitement)

use bytes::Bytes;
use panini_core::storage::{
    atom::{Atom, AtomType},
    backends::localfs::LocalFsBackend,
    cas::ContentAddressedStorage,
    decomposer::FileFormat,
};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::time::Instant;
use tokio::fs;

#[derive(Debug, Clone)]
struct VideoStats {
    filename: String,
    size: u64,
    format: String,
    atom_count: usize,
    processing_time_ms: u128,
}

#[derive(Debug, Default)]
struct GlobalStats {
    total_videos: usize,
    total_size: u64,
    total_atoms: usize,
    unique_atoms: usize,
    total_processing_time_ms: u128,
    videos_by_format: HashMap<String, usize>,
}

async fn process_video(
    path: &Path,
    cas: &ContentAddressedStorage<LocalFsBackend>,
) -> anyhow::Result<VideoStats> {
    let start = Instant::now();
    
    // Read video file
    let data = fs::read(path).await?;
    let size = data.len() as u64;
    let filename = path.file_name().unwrap().to_string_lossy().to_string();
    
    println!("  📹 Processing: {} ({:.2} MB)", filename, size as f64 / 1_048_576.0);
    
    // Detect format
    let format = FileFormat::detect(&data);
    let format_str = match format {
        FileFormat::PNG => "PNG",
        FileFormat::JPEG => "JPEG",
        FileFormat::MP4 => "MP4",
        FileFormat::Unknown => "Unknown",
    }.to_string();
    
    // Decompose into atoms
    let atoms = cas.decompose_and_store(&data, &format).await?;
    let atom_count = atoms.len();
    
    let processing_time_ms = start.elapsed().as_millis();
    
    Ok(VideoStats {
        filename,
        size,
        format: format_str,
        atom_count,
        processing_time_ms,
    })
}

async fn test_reconstruction(
    original_data: &[u8],
    atom_hashes: &[String],
    cas: &ContentAddressedStorage<LocalFsBackend>,
    filename: &str,
) -> anyhow::Result<bool> {
    use sha2::{Sha256, Digest};
    
    // Reconstruct from atoms
    let mut reconstructed = Vec::new();
    for atom_hash in atom_hashes {
        let atom_data = cas.get_atom(atom_hash).await?;
        reconstructed.extend_from_slice(&atom_data);
    }
    
    // Verify size
    if reconstructed.len() != original_data.len() {
        println!("    ❌ Size mismatch for {}: {} vs {}", 
                 filename, reconstructed.len(), original_data.len());
        return Ok(false);
    }
    
    // Verify SHA-256 hash
    let original_hash = format!("{:x}", Sha256::digest(original_data));
    let reconstructed_hash = format!("{:x}", Sha256::digest(&reconstructed));
    
    if original_hash != reconstructed_hash {
        println!("    ❌ Hash mismatch for {}", filename);
        return Ok(false);
    }
    
    Ok(true)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("╔════════════════════════════════════════════════════════════════╗");
    println!("║  Panini-FS: Test de Stress sur Vidéos Réelles                 ║");
    println!("║  Atomic Storage Stress Test with Real Video Files             ║");
    println!("╚════════════════════════════════════════════════════════════════╝");
    println!();
    
    let video_dir = Path::new("/run/media/stephane/CCCOMA_X64FRE_FR-CA_DV9/Backup Sam/Vidéos");
    
    // Check if directory exists
    if !video_dir.exists() {
        println!("❌ Directory not found: {}", video_dir.display());
        println!("   Please ensure the USB drive is mounted.");
        return Ok(());
    }
    
    println!("📂 Scanning directory: {}", video_dir.display());
    
    // Find all video files
    let mut video_files = Vec::new();
    let mut total_size = 0u64;
    
    for ext in &["mp4", "mkv", "wmv"] {
        let pattern = format!("{}/**/*.{}", video_dir.display(), ext);
        for entry in glob::glob(&pattern)? {
            if let Ok(path) = entry {
                if path.is_file() {
                    if let Ok(metadata) = fs::metadata(&path).await {
                        total_size += metadata.len();
                        video_files.push(path);
                    }
                }
            }
        }
    }
    
    println!("   Found {} video files", video_files.len());
    println!("   Total size: {:.2} GB", total_size as f64 / 1_073_741_824.0);
    println!();
    
    if video_files.is_empty() {
        println!("⚠️  No video files found. Exiting.");
        return Ok(());
    }
    
    // Limit to first 10 videos for faster testing
    let max_videos = 10.min(video_files.len());
    println!("⚠️  Testing first {} videos (for speed)", max_videos);
    video_files.truncate(max_videos);
    println!();
    
    // Create temporary storage backend
    let temp_dir = tempfile::tempdir()?;
    println!("�� Creating storage backend at: {}", temp_dir.path().display());
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path())?);
    
    // Create CAS with default config
    let config = panini_core::storage::cas::StorageConfig::default();
    let cas = ContentAddressedStorage::new(backend.clone(), config);
    
    println!("🔬 Starting atomic decomposition...");
    println!();
    
    let start_time = Instant::now();
    let mut video_stats = Vec::new();
    let mut global_stats = GlobalStats::default();
    let mut verification_failures = 0;
    
    // Process each video
    for (i, video_path) in video_files.iter().enumerate() {
        println!("📹 [{}/{}] {}", 
                 i + 1, 
                 video_files.len(), 
                 video_path.file_name().unwrap().to_string_lossy());
        
        match process_video(video_path, &cas).await {
            Ok(stats) => {
                // Test reconstruction
                let original_data = fs::read(video_path).await?;
                let atoms = cas.decompose_and_store(&original_data, 
                    &FileFormat::detect(&original_data)).await?;
                
                match test_reconstruction(&original_data, &atoms, &cas, &stats.filename).await {
                    Ok(true) => {
                        println!("    ✅ Reconstruction verified (bit-perfect)");
                        println!("    📊 {} atoms, {:.2}ms", 
                                 stats.atom_count,
                                 stats.processing_time_ms);
                    }
                    Ok(false) => {
                        println!("    ❌ RECONSTRUCTION FAILED!");
                        verification_failures += 1;
                    }
                    Err(e) => {
                        println!("    ⚠️  Verification error: {}", e);
                        verification_failures += 1;
                    }
                }
                
                // Update global stats
                global_stats.total_videos += 1;
                global_stats.total_size += stats.size;
                global_stats.total_atoms += stats.atom_count;
                global_stats.total_processing_time_ms += stats.processing_time_ms;
                
                *global_stats.videos_by_format.entry(stats.format.clone()).or_insert(0) += 1;
                
                video_stats.push(stats);
            }
            Err(e) => {
                println!("    ❌ Error processing video: {}", e);
            }
        }
        
        println!();
    }
    
    // Get final CAS stats
    let cas_stats = cas.get_stats().await;
    global_stats.unique_atoms = cas_stats.total_atoms as usize;
    
    let total_time = start_time.elapsed();
    
    // Print summary
    println!("╔════════════════════════════════════════════════════════════════╗");
    println!("║  SUMMARY / RÉSUMÉ                                              ║");
    println!("╚════════════════════════════════════════════════════════════════╝");
    println!();
    
    println!("📊 Global Statistics:");
    println!("   • Total videos processed: {}", global_stats.total_videos);
    println!("   • Total size: {:.2} MB", global_stats.total_size as f64 / 1_048_576.0);
    println!("   • Total atoms created: {}", global_stats.total_atoms);
    println!("   • Unique atoms stored: {} ({:.1}% dedup)", 
             global_stats.unique_atoms,
             if global_stats.total_atoms > 0 {
                 (1.0 - global_stats.unique_atoms as f64 / global_stats.total_atoms as f64) * 100.0
             } else { 0.0 });
    println!("   • Storage savings: {:.2} MB ({:.1}%)", 
             cas_stats.dedup_savings as f64 / 1_048_576.0,
             if global_stats.total_size > 0 {
                 cas_stats.dedup_savings as f64 / global_stats.total_size as f64 * 100.0
             } else { 0.0 });
    println!();
    
    println!("⏱️  Performance:");
    println!("   • Total processing time: {:.2}s", total_time.as_secs_f64());
    if global_stats.total_videos > 0 {
        println!("   • Average per video: {:.2}ms", 
                 global_stats.total_processing_time_ms as f64 / global_stats.total_videos as f64);
    }
    println!("   • Throughput: {:.2} MB/s", 
             global_stats.total_size as f64 / 1_048_576.0 / total_time.as_secs_f64());
    println!();
    
    println!("📹 Videos by Format:");
    for (format, count) in &global_stats.videos_by_format {
        println!("   • {}: {} videos", format, count);
    }
    println!();
    
    println!("🎯 Granularity Analysis:");
    if !video_stats.is_empty() {
        let avg_atoms = global_stats.total_atoms as f64 / global_stats.total_videos as f64;
        let avg_size = global_stats.total_size as f64 / global_stats.total_videos as f64;
        let avg_atom_size = if avg_atoms > 0.0 { avg_size / avg_atoms } else { 0.0 };
        
        println!("   • Average atoms per video: {:.0}", avg_atoms);
        println!("   • Average atom size: {:.2} KB", avg_atom_size / 1024.0);
        
        // Find min/max
        let min_atoms = video_stats.iter().map(|s| s.atom_count).min().unwrap_or(0);
        let max_atoms = video_stats.iter().map(|s| s.atom_count).max().unwrap_or(0);
        println!("   • Min atoms: {}", min_atoms);
        println!("   • Max atoms: {}", max_atoms);
        
        // Git-friendly granularity assessment
        if avg_atom_size < 100_000.0 {  // < 100KB
            println!("   ✅ Granularity EXCELLENT for Git (< 100KB per atom)");
        } else if avg_atom_size < 1_000_000.0 {  // < 1MB
            println!("   ✅ Granularity GOOD for Git (< 1MB per atom)");
        } else {
            println!("   ⚠️  Granularity MODERATE for Git (> 1MB per atom)");
        }
    }
    println!();
    
    println!("✅ Verification Results:");
    println!("   • Successful: {}/{}", 
             global_stats.total_videos - verification_failures,
             global_stats.total_videos);
    if verification_failures > 0 {
        println!("   ❌ Failed: {}", verification_failures);
    } else {
        println!("   🎉 ALL RECONSTRUCTIONS BIT-PERFECT!");
    }
    println!();
    
    // Top 5 videos by atom count (most granular)
    if video_stats.len() > 0 {
        println!("🏆 Top 5 Most Granular Videos (by atom count):");
        let mut sorted_videos = video_stats.clone();
        sorted_videos.sort_by_key(|s| std::cmp::Reverse(s.atom_count));
        for (i, stats) in sorted_videos.iter().take(5.min(sorted_videos.len())).enumerate() {
            println!("   {}. {} - {} atoms ({:.2} MB)", 
                     i + 1,
                     stats.filename,
                     stats.atom_count,
                     stats.size as f64 / 1_048_576.0);
        }
        println!();
    }
    
    println!("✅ Stress Test Complete!");
    println!();
    
    Ok(())
}
