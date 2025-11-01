//! Bridge between FUSE (sync) and ContentAddressedStorage (async)
//!
//! FUSE operations run in synchronous context, but our CAS is async.
//! This module provides a bridge using tokio Runtime.

use anyhow::Result;
use bytes::Bytes;
use panini_core::storage::{
    backends::LocalFsBackend,
    cas::ContentAddressedStorage,
};
use std::path::PathBuf;
use std::sync::Arc;
use tokio::runtime::Runtime;

/// Synchronous wrapper around async ContentAddressedStorage
pub struct StorageBridge {
    cas: Arc<ContentAddressedStorage<LocalFsBackend>>,
    runtime: Runtime,
}

impl StorageBridge {
    /// Create new storage bridge
    pub fn new(storage_path: PathBuf) -> Result<Self> {
        // Create tokio runtime for async operations
        let runtime = tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .build()?;
        
        // Initialize CAS in async context
        let cas = runtime.block_on(async {
            let backend = LocalFsBackend::new(&storage_path)
                .map_err(|e| anyhow::anyhow!("{}", e))?;
            let config = panini_core::storage::cas::StorageConfig::default();
            let cas = ContentAddressedStorage::new(Arc::new(backend), config);
            Ok::<_, anyhow::Error>(Arc::new(cas))
        })?;
        
        Ok(Self { cas, runtime })
    }
    
    /// Read atom content by hash (synchronous wrapper)
    pub fn read_atom(&self, hash: &str) -> Result<Bytes> {
        self.runtime.block_on(async {
            self.cas.get_atom(hash).await
        })
        .map_err(|e| anyhow::anyhow!("{}", e))
    }
    
    /// Get atom metadata (synchronous wrapper)
    pub fn get_atom_metadata(&self, hash: &str) -> Result<panini_core::storage::atom::AtomMetadata> {
        // This method is actually sync in CAS
        self.cas.get_atom_metadata(hash)
            .map_err(|e| anyhow::anyhow!("{}", e))
    }
    
    /// List all atoms (synchronous wrapper)
    pub fn list_atoms(&self) -> Vec<panini_core::storage::atom::AtomMetadata> {
        // This method is actually sync in CAS
        self.cas.list_atoms()
    }
    
    /// Get storage statistics (synchronous wrapper)
    pub fn get_stats(&self) -> panini_core::storage::cas::StorageStats {
        self.runtime.block_on(async {
            self.cas.get_stats().await
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn test_storage_bridge_creation() {
        let temp_dir = TempDir::new().unwrap();
        let bridge = StorageBridge::new(temp_dir.path().to_path_buf());
        assert!(bridge.is_ok());
    }
}
