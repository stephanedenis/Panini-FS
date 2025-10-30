//! Integration tests for atomic storage system

use panini_core::storage::*;
use std::fs;
use std::sync::Arc;
use tempfile::TempDir;

#[tokio::test]
async fn test_full_png_decomposition_and_reconstruction() {
    // 1. Load test PNG file
    let test_png = include_bytes!("../../../tests/fixtures/test.png");
    println!("📦 Loaded test PNG: {} bytes", test_png.len());
    
    // 2. Create storage backend
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // 3. Auto-detect format and decompose
    let decomposer = Decomposer::auto_detect(test_png);
    let atoms = decomposer.decompose(test_png).unwrap();
    
    println!("🔬 Decomposed into {} atoms:", atoms.len());
    for (i, atom) in atoms.iter().enumerate() {
        println!("  Atom {}: {} - {} bytes ({})", 
            i, 
            &atom.hash[..16], 
            atom.size,
            atom.atom_type
        );
    }
    
    // 4. Store all atoms in CAS
    let mut content_refs = Vec::new();
    for atom in &atoms {
        let start = atom.source_offset as usize;
        let end = (atom.source_offset + atom.size) as usize;
        let atom_data = &test_png[start..end];
        
        let stored = cas.add_atom(atom_data, atom.atom_type).await.unwrap();
        content_refs.push(ContentRef::new(
            stored.hash,
            stored.atom_type,
            atom.source_offset,
            atom.size,
        ));
    }
    
    println!("\n💾 Stored {} atoms in CAS", content_refs.len());
    
    // 5. Get storage stats
    let stats = cas.get_stats();
    println!("\n📊 Storage Statistics:");
    println!("  Total atoms: {}", stats.total_atoms);
    println!("  Total size: {} bytes", stats.total_size);
    println!("  Unique atoms: {}", stats.unique_atoms);
    println!("  Dedup ratio: {:.1}%", stats.dedup_ratio());
    
    // 6. Retrieve atoms and reconstruct
    let mut atoms_data = Vec::new();
    for cref in &content_refs {
        let data = cas.get_atom(&cref.atom_hash).await.unwrap();
        atoms_data.push(data.to_vec());
    }
    
    let reconstructed = Reconstructor::reconstruct_verified(&atoms, atoms_data).unwrap();
    
    println!("\n✅ Reconstruction successful!");
    println!("  Original size: {} bytes", test_png.len());
    println!("  Reconstructed size: {} bytes", reconstructed.len());
    
    // 7. Verify bit-perfect reconstruction
    assert_eq!(reconstructed.len(), test_png.len(), "Size mismatch!");
    assert_eq!(&reconstructed[..], test_png, "Content mismatch - not bit-perfect!");
    
    println!("  ✅ Bit-perfect match!");
}

#[tokio::test]
async fn test_deduplication() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Same data added twice
    let data1 = b"duplicate data for testing";
    let data2 = b"duplicate data for testing";
    
    let atom1 = cas.add_atom(data1, AtomType::Container).await.unwrap();
    let atom2 = cas.add_atom(data2, AtomType::IFrame).await.unwrap();
    
    println!("🔍 Deduplication test:");
    println!("  Atom 1 hash: {}", atom1.hash);
    println!("  Atom 2 hash: {}", atom2.hash);
    
    // Should have same hash
    assert_eq!(atom1.hash, atom2.hash, "Hashes should match!");
    
    // Check ref count
    let meta = cas.get_atom_metadata(&atom1.hash).unwrap();
    assert_eq!(meta.ref_count, 2, "Ref count should be 2!");
    
    let stats = cas.get_stats();
    println!("\n📊 After deduplication:");
    println!("  Total atoms: {} (logical)", stats.total_atoms);
    println!("  Unique atoms: {} (physical)", stats.unique_atoms);
    println!("  Dedup savings: {} bytes", stats.dedup_savings);
    println!("  Dedup ratio: {:.1}%", stats.dedup_ratio());
    
}

#[tokio::test]
async fn test_garbage_collection() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Add some atoms
    let atom1 = cas.add_atom(b"atom1 data", AtomType::Container).await.unwrap();
    let atom2 = cas.add_atom(b"atom2 data", AtomType::IFrame).await.unwrap();
    let atom3 = cas.add_atom(b"atom3 data", AtomType::AudioChunk).await.unwrap();
    
    println!("📦 Added 3 atoms");
    
    // Decrement refs to make them orphaned
    cas.decrement_atom_refs(&atom1.hash).unwrap();
    cas.decrement_atom_refs(&atom2.hash).unwrap();
    // Keep atom3 referenced
    
    let orphaned = cas.find_orphaned_atoms();
    println!("\n🗑️  Found {} orphaned atoms", orphaned.len());
    
    assert_eq!(orphaned.len(), 2, "Should have 2 orphaned atoms");
    
    // Run GC
    let gc_stats = cas.gc_orphaned_atoms().await.unwrap();
    
    println!("\n✅ Garbage collection complete:");
    println!("  Atoms deleted: {}", gc_stats.atoms_deleted);
    println!("  Bytes freed: {}", gc_stats.bytes_freed);
    
    assert_eq!(gc_stats.atoms_deleted, 2);
    
    // Verify atom3 still exists
    assert!(cas.get_atom(&atom3.hash).await.is_ok());
    
    // Verify atom1 and atom2 are gone
    assert!(cas.get_atom(&atom1.hash).await.is_err());
    assert!(cas.get_atom(&atom2.hash).await.is_err());
}

#[tokio::test]
async fn test_atom_types_and_metadata() {
    let temp_dir = TempDir::new().unwrap();
    let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
    let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
    
    // Test different atom types
    let types = vec![
        (AtomType::Container, b"container data".as_ref()),
        (AtomType::IFrame, b"iframe data".as_ref()),
        (AtomType::AudioChunk, b"audio data".as_ref()),
        (AtomType::Metadata, b"metadata content".as_ref()),
    ];
    
    println!("🧪 Testing different atom types:");
    
    for (atom_type, data) in types {
        let atom = cas.add_atom(data, atom_type).await.unwrap();
        println!("  {} - hash: {}", atom_type, &atom.hash[..16]);
        
        // Verify storage
        let retrieved = cas.get_atom(&atom.hash).await.unwrap();
        assert_eq!(&retrieved[..], data);
    }
    
    // Test filtering by type
    let iframes = cas.get_atoms_by_type(AtomType::IFrame);
    assert_eq!(iframes.len(), 1);
    println!("\n📊 Found {} I-Frame atoms", iframes.len());
}

#[tokio::test]
async fn test_backend_sharding() {
    let temp_dir = TempDir::new().unwrap();
    let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
    
    // Upload a file
    let test_data = bytes::Bytes::from("test data for sharding");
    let hash = "abcdef1234567890"; // Example hash
    
    let result = backend.upload(hash, test_data.clone()).await.unwrap();
    assert_eq!(result.key, hash);
    
    // Verify sharding structure (ab/cd/abcdef1234567890)
    let expected_path = temp_dir.path()
        .join("ab")
        .join("cd")
        .join(hash);
    
    assert!(expected_path.exists(), "Sharded path should exist!");
    println!("✅ Sharding verified: {:?}", expected_path);
    
    // Download and verify
    let downloaded = backend.download(hash).await.unwrap();
    assert_eq!(downloaded, test_data);
}

#[test]
fn test_atom_creation_and_hashing() {
    let data = b"test atom data for hashing";
    
    let atom1 = Atom::new(data, AtomType::Container);
    let atom2 = Atom::new(data, AtomType::IFrame);
    
    println!("🔐 Hash consistency test:");
    println!("  Atom 1 hash: {}", atom1.hash);
    println!("  Atom 2 hash: {}", atom2.hash);
    
    // Same data should produce same hash regardless of type
    assert_eq!(atom1.hash, atom2.hash);
    assert_eq!(atom1.size, data.len() as u64);
    
    // Test metadata
    let atom_with_meta = Atom::new(data, AtomType::VideoStream)
        .with_metadata("codec", "h264")
        .with_metadata("fps", "30");
    
    assert_eq!(atom_with_meta.metadata.get("codec"), Some(&"h264".to_string()));
    println!("  ✅ Metadata: {:?}", atom_with_meta.metadata);
}

#[test]
fn test_format_detection() {
    // PNG signature
    let png_sig = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
    assert_eq!(FileFormat::detect(&png_sig), FileFormat::PNG);
    println!("✅ PNG detection works");
    
    // JPEG signature
    let jpeg_sig = [0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46]; // Full JFIF
    assert_eq!(FileFormat::detect(&jpeg_sig), FileFormat::JPEG);
    println!("✅ JPEG detection works");
    
    // MP4 signature
    let mp4_sig = b"\x00\x00\x00\x20ftypisom";
    assert_eq!(FileFormat::detect(mp4_sig), FileFormat::MP4);
    println!("✅ MP4 detection works");
    
    // Unknown format
    let unknown = b"unknown data";
    assert_eq!(FileFormat::detect(unknown), FileFormat::Unknown);
    println!("✅ Unknown format detection works");
}
