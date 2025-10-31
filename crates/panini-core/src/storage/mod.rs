//! Storage module - Content-addressed storage with atomic decomposition
//!
//! This module provides:
//! - Atomic decomposition of binary files (PNG, JPEG, MP4, etc.)
//! - Content-addressed storage (CAS) with SHA-256 hashing
//! - Automatic deduplication
//! - Multiple storage backends (LocalFS, S3-compatible)
//! - Lossless reconstruction

pub mod atom;
pub mod cas;
pub mod backends;
pub mod decomposer;
pub mod reconstructor;

// Re-export from existing modules
pub use dedup::DedupManager;
pub use backend::{StorageBackend as LegacyStorageBackend, UploadResult as LegacyUploadResult};

// Re-export main types
pub use atom::{Atom, AtomType, AtomMetadata};
pub use cas::{ContentAddressedStorage, StorageConfig, StorageStats, GcStats};
pub use backends::{StorageBackend, LocalFsBackend, UploadResult, BackendStats};
pub use decomposer::{Decomposer, FileFormat};
pub use reconstructor::Reconstructor;

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Reference to a content atom in storage
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ContentRef {
    /// SHA-256 hash of the atom
    pub atom_hash: String,
    
    /// Type of the atom
    pub atom_type: AtomType,
    
    /// Offset in the reconstructed file (bytes)
    pub offset: u64,
    
    /// Size of the atom (bytes)
    pub size: u64,
    
    /// Optional metadata (codec, resolution, etc.)
    #[serde(default)]
    pub metadata: HashMap<String, String>,
}

impl ContentRef {
    pub fn new(atom_hash: String, atom_type: AtomType, offset: u64, size: u64) -> Self {
        Self {
            atom_hash,
            atom_type,
            offset,
            size,
            metadata: HashMap::new(),
        }
    }
    
    pub fn with_metadata(mut self, key: String, value: String) -> Self {
        self.metadata.insert(key, value);
        self
    }
}

// Keep existing modules for backwards compatibility
mod backend;
mod dedup;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_content_ref_creation() {
        let cref = ContentRef::new(
            "abc123".to_string(),
            AtomType::Container,
            0,
            1024,
        );
        
        assert_eq!(cref.atom_hash, "abc123");
        assert_eq!(cref.offset, 0);
        assert_eq!(cref.size, 1024);
    }
}
pub mod immutable;
