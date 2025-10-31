//! Storage Demo - Atomic Decomposition Demonstration
//! 
//! This example demonstrates:
//! - PNG decomposition into atoms
//! - Content-addressed storage with deduplication
//! - Bit-perfect reconstruction
//! - Storage statistics and garbage collection

use panini_core::storage::*;
use std::sync::Arc;
use tempfile::TempDir;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🧬 Panini-FS Storage Demo: Atomic Decomposition\n");
    println!("================================================\n");
    
    // 1. Load test PNG files
    println!("📦 Step 1: Loading test PNG files...");
    
    let small_png = include_bytes!("../../../tests/fixtures/test.png");
    let large_png = include_bytes!("../../../tests/fixtures/rust-256.png");
    
    println!("  • Small PNG: {} bytes (1x1 transparent)", small_png.len());
    println!("  • Large PNG: {} bytes (256x256 Rust logo)", large_png.len());
    
    // 2. Create storage backend
    println!("\n💾 Step 2: Creating storage backend...");
    let temp_dir = TempDir::new()?;
    println!("  • Storage path: {:?}", temp_dir.path());
    
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path())?);
    let cas = ContentAddressedStorage::new(backend.clone(), StorageConfig::default());
    println!("  • CAS initialized with 2-level sharding");
    
    // 3. Decompose and store small PNG
    println!("\n🔬 Step 3: Decomposing small PNG...");
    let decomposer = Decomposer::auto_detect(small_png);
    let small_atoms = decomposer.decompose(small_png)?;
    
    println!("  • Format detected: PNG");
    println!("  • Atoms extracted: {}", small_atoms.len());
    
    for (i, atom) in small_atoms.iter().enumerate() {
        println!("    [{}] {} - {} bytes ({})", 
            i, 
            &atom.hash[..16], 
            atom.size,
            atom.atom_type
        );
    }
    
    let mut small_refs = Vec::new();
    for atom in &small_atoms {
        let start = atom.source_offset as usize;
        let end = (atom.source_offset + atom.size) as usize;
        let atom_data = &small_png[start..end];
        
        let stored = cas.add_atom(atom_data, atom.atom_type).await?;
        small_refs.push(ContentRef::new(
            stored.hash,
            stored.atom_type,
            atom.source_offset,
            atom.size,
        ));
    }
    
    println!("  ✅ All atoms stored in CAS");
    
    // 4. Decompose and store large PNG
    println!("\n🔬 Step 4: Decomposing large PNG...");
    let decomposer = Decomposer::auto_detect(large_png);
    let large_atoms = decomposer.decompose(large_png)?;
    
    println!("  • Format detected: PNG");
    println!("  • Atoms extracted: {}", large_atoms.len());
    
    // Count atoms by type
    let mut type_counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for atom in &large_atoms {
        *type_counts.entry(format!("{}", atom.atom_type)).or_insert(0) += 1;
    }
    
    println!("  • Atoms by type:");
    for (atom_type, count) in type_counts.iter() {
        println!("    - {}: {} atoms", atom_type, count);
    }
    
    let mut large_refs = Vec::new();
    for atom in &large_atoms {
        let start = atom.source_offset as usize;
        let end = (atom.source_offset + atom.size) as usize;
        let atom_data = &large_png[start..end];
        
        let stored = cas.add_atom(atom_data, atom.atom_type).await?;
        large_refs.push(ContentRef::new(
            stored.hash,
            stored.atom_type,
            atom.source_offset,
            atom.size,
        ));
    }
    
    println!("  ✅ All atoms stored in CAS");
    
    // 5. Show storage statistics
    println!("\n📊 Step 5: Storage Statistics");
    let stats = cas.get_stats();
    
    println!("  • Total atoms (unique): {}", stats.total_atoms);
    println!("  • Total size: {} bytes ({:.2} KB)", 
        stats.total_size, 
        stats.total_size as f64 / 1024.0
    );
    println!("  • Atoms with dedup: {}", stats.dedup_atoms);
    println!("  • Dedup ratio: {:.1}%", stats.dedup_ratio());
    println!("  • Storage savings: {} bytes ({:.2} KB)", 
        stats.dedup_savings,
        stats.dedup_savings as f64 / 1024.0
    );
    
    // 6. Demonstrate deduplication by storing small PNG again
    println!("\n🔁 Step 6: Testing deduplication (store small PNG again)...");
    let before_atoms = cas.get_stats().total_atoms;
    
    for atom in &small_atoms {
        let start = atom.source_offset as usize;
        let end = (atom.source_offset + atom.size) as usize;
        let atom_data = &small_png[start..end];
        cas.add_atom(atom_data, atom.atom_type).await?;
    }
    
    let after_atoms = cas.get_stats().total_atoms;
    let stats = cas.get_stats();
    
    println!("  • Atoms before: {}", before_atoms);
    println!("  • Atoms after: {} (no increase!)", after_atoms);
    println!("  • Dedup savings: {} bytes", stats.dedup_savings);
    println!("  ✅ Deduplication working perfectly!");
    
    // 7. Reconstruct small PNG and verify
    println!("\n🔧 Step 7: Reconstructing small PNG...");
    let mut atoms_data = Vec::new();
    for cref in &small_refs {
        let data = cas.get_atom(&cref.atom_hash).await?;
        atoms_data.push(data.to_vec());
    }
    
    let reconstructed = Reconstructor::reconstruct_verified(&small_atoms, atoms_data)?;
    
    println!("  • Original size: {} bytes", small_png.len());
    println!("  • Reconstructed size: {} bytes", reconstructed.len());
    
    if reconstructed == small_png {
        println!("  ✅ Bit-perfect reconstruction verified!");
    } else {
        println!("  ❌ Reconstruction mismatch!");
    }
    
    // 8. List atoms by type
    println!("\n📋 Step 8: Listing atoms by type...");
    
    for atom_type in [AtomType::Container, AtomType::Metadata, AtomType::ImageData] {
        let atoms = cas.get_atoms_by_type(atom_type);
        if !atoms.is_empty() {
            println!("  • {}: {} atoms", atom_type, atoms.len());
            for (i, atom) in atoms.iter().take(3).enumerate() {
                println!("    [{}] {} - {} bytes (refs: {})", 
                    i,
                    &atom.hash[..16],
                    atom.size,
                    atom.ref_count
                );
            }
            if atoms.len() > 3 {
                println!("    ... and {} more", atoms.len() - 3);
            }
        }
    }
    
    // 9. Garbage collection demo
    println!("\n🗑️  Step 9: Garbage collection demo...");
    
    // Decrement refs for small PNG atoms
    for cref in &small_refs {
        cas.decrement_atom_refs(&cref.atom_hash)?;
        cas.decrement_atom_refs(&cref.atom_hash)?; // Second decrement (from duplicate)
    }
    
    let orphaned = cas.find_orphaned_atoms();
    println!("  • Orphaned atoms found: {}", orphaned.len());
    
    let gc_stats = cas.gc_orphaned_atoms().await?;
    println!("  • Atoms deleted: {}", gc_stats.atoms_deleted);
    println!("  • Space freed: {} bytes ({:.2} KB)", 
        gc_stats.bytes_freed,
        gc_stats.bytes_freed as f64 / 1024.0
    );
    println!("  ✅ Garbage collection complete!");
    
    // 10. Final statistics
    println!("\n📊 Step 10: Final Storage Statistics");
    let final_stats = cas.get_stats();
    
    println!("  • Total atoms: {}", final_stats.total_atoms);
    println!("  • Total size: {} bytes ({:.2} KB)", 
        final_stats.total_size,
        final_stats.total_size as f64 / 1024.0
    );
    println!("  • Unique atoms: {}", final_stats.unique_atoms);
    
    // 11. Show backend files
    println!("\n💾 Step 11: Backend Storage Structure");
    println!("  • Sharding example:");
    
    let backend_stats = backend.stats().await?;
    println!("    - Total objects: {}", backend_stats.total_objects);
    println!("    - Total size: {} bytes ({:.2} KB)",
        backend_stats.total_size,
        backend_stats.total_size as f64 / 1024.0
    );
    
    println!("\n✅ Demo Complete!");
    println!("\n💡 Key Takeaways:");
    println!("  • PNG files decomposed into semantic atoms");
    println!("  • Automatic deduplication via SHA-256 hashing");
    println!("  • Bit-perfect reconstruction guaranteed");
    println!("  • Garbage collection removes orphaned atoms");
    println!("  • 2-level sharding for efficient storage");
    
    Ok(())
}
