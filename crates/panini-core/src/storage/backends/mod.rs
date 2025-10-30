//! Storage backends for content-addressed storage

pub mod localfs;

pub use localfs::LocalFsBackend;

use crate::error::Result;
use async_trait::async_trait;
use bytes::Bytes;
use serde::{Deserialize, Serialize};

/// Storage backend trait
#[async_trait]
pub trait StorageBackend: Send + Sync {
    /// Upload data with given key (hash)
    async fn upload(&self, key: &str, data: Bytes) -> Result<UploadResult>;
    
    /// Download data by key (hash)
    async fn download(&self, key: &str) -> Result<Bytes>;
    
    /// Delete data by key (hash)
    async fn delete(&self, key: &str) -> Result<()>;
    
    /// Check if key exists
    async fn exists(&self, key: &str) -> Result<bool>;
    
    /// List all keys (hashes)
    async fn list_keys(&self) -> Result<Vec<String>>;
    
    /// Get backend statistics
    async fn stats(&self) -> Result<BackendStats>;
}

/// Upload result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UploadResult {
    pub key: String,
    pub size: u64,
    pub already_existed: bool,
}

/// Backend statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BackendStats {
    pub total_objects: u64,
    pub total_size: u64,
}
