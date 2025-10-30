//! Content deduplication using content-addressable storage

use crate::error::{Error, Result};
use crate::storage::backend::{StorageBackend, UploadResult};
use bytes::Bytes;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

/// Content deduplication manager
pub struct DedupManager<B: StorageBackend> {
    backend: Arc<B>,
    index: Arc<RwLock<DedupIndex>>,
}

impl<B: StorageBackend> DedupManager<B> {
    /// Create new deduplication manager
    pub fn new(backend: Arc<B>) -> Self {
        Self {
            backend,
            index: Arc::new(RwLock::new(DedupIndex::new())),
        }
    }
    
    /// Upload with deduplication
    pub async fn upload_deduplicated(&self, data: Bytes) -> Result<DedupResult> {
        // Calculate hash
        let hash = blake3::hash(&data).to_hex().to_string();
        
        // Check if already exists
        {
            let index = self.index.read()
                .map_err(|_| Error::generic("Failed to acquire read lock".to_string()))?;
            
            if let Some(info) = index.get(&hash) {
                // Clone values before dropping lock
                let key = info.key.clone();
                let size = info.size;
                // Already exists, increment ref count
                drop(index);
                
                let mut index = self.index.write()
                    .map_err(|_| Error::generic("Failed to acquire write lock".to_string()))?;
                
                index.increment_refs(&hash);
                
                return Ok(DedupResult {
                    hash: hash.clone(),
                    key,
                    size,
                    deduplicated: true,
                    saved_bytes: size,
                });
            }
        }
        
        // Upload new content
        let key = format!("content/{}", hash);
        let result = self.backend.upload(&key, data).await?;
        
        // Add to index
        {
            let mut index = self.index.write()
                .map_err(|_| Error::generic("Failed to acquire write lock".to_string()))?;
            
            index.add(hash.clone(), ContentInfo {
                key: result.key.clone(),
                size: result.size,
                refs: 1,
            });
        }
        
        Ok(DedupResult {
            hash,
            key: result.key,
            size: result.size,
            deduplicated: false,
            saved_bytes: 0,
        })
    }
    
    /// Download by hash
    pub async fn download_by_hash(&self, hash: &str) -> Result<Bytes> {
        let key = {
            let index = self.index.read()
                .map_err(|_| Error::generic("Failed to acquire read lock".to_string()))?;
            
            let info = index.get(hash)
                .ok_or_else(|| Error::generic(format!("Hash {} not found", hash)))?;
            
            info.key.clone()
        };
        
        self.backend.download(&key).await
    }
    
    /// Delete with reference counting
    pub async fn delete_by_hash(&self, hash: &str) -> Result<bool> {
        let should_delete = {
            let mut index = self.index.write()
                .map_err(|_| Error::generic("Failed to acquire write lock".to_string()))?;
            
            index.decrement_refs(hash)
        };
        
        if should_delete {
            let key = format!("content/{}", hash);
            self.backend.delete(&key).await?;
            Ok(true)
        } else {
            Ok(false)
        }
    }
    
    /// Get deduplication statistics
    pub fn dedup_stats(&self) -> Result<DedupStats> {
        let index = self.index.read()
            .map_err(|_| Error::generic("Failed to acquire read lock".to_string()))?;
        
        Ok(index.stats())
    }
    
    /// Garbage collection (remove unreferenced content)
    pub async fn garbage_collect(&self) -> Result<GcResult> {
        let to_delete = {
            let index = self.index.read()
                .map_err(|_| Error::generic("Failed to acquire read lock".to_string()))?;
            
            index.get_unreferenced()
        };
        
        let mut deleted = 0;
        let mut freed_bytes = 0u64;
        
        for (hash, info) in to_delete {
            match self.backend.delete(&info.key).await {
                Ok(_) => {
                    deleted += 1;
                    freed_bytes += info.size;
                }
                Err(e) => {
                    eprintln!("Failed to delete {}: {}", hash, e);
                }
            }
        }
        
        // Remove from index
        {
            let mut index = self.index.write()
                .map_err(|_| Error::generic("Failed to acquire write lock".to_string()))?;
            
            index.remove_unreferenced();
        }
        
        Ok(GcResult {
            deleted,
            freed_bytes,
        })
    }
}

/// Deduplication index
struct DedupIndex {
    content: HashMap<String, ContentInfo>,
}

impl DedupIndex {
    fn new() -> Self {
        Self {
            content: HashMap::new(),
        }
    }
    
    fn get(&self, hash: &str) -> Option<&ContentInfo> {
        self.content.get(hash)
    }
    
    fn add(&mut self, hash: String, info: ContentInfo) {
        self.content.insert(hash, info);
    }
    
    fn increment_refs(&mut self, hash: &str) {
        if let Some(info) = self.content.get_mut(hash) {
            info.refs += 1;
        }
    }
    
    fn decrement_refs(&mut self, hash: &str) -> bool {
        if let Some(info) = self.content.get_mut(hash) {
            info.refs = info.refs.saturating_sub(1);
            info.refs == 0
        } else {
            false
        }
    }
    
    fn get_unreferenced(&self) -> Vec<(String, ContentInfo)> {
        self.content
            .iter()
            .filter(|(_, info)| info.refs == 0)
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect()
    }
    
    fn remove_unreferenced(&mut self) {
        self.content.retain(|_, info| info.refs > 0);
    }
    
    fn stats(&self) -> DedupStats {
        let total_content = self.content.len();
        let total_size: u64 = self.content.values().map(|i| i.size).sum();
        let total_refs: usize = self.content.values().map(|i| i.refs).sum();
        
        let unique_bytes = total_size;
        let logical_bytes: u64 = self.content.values()
            .map(|i| i.size * i.refs as u64)
            .sum();
        
        let saved_bytes = logical_bytes.saturating_sub(unique_bytes);
        let dedup_ratio = if logical_bytes > 0 {
            (saved_bytes as f64 / logical_bytes as f64) * 100.0
        } else {
            0.0
        };
        
        DedupStats {
            total_content,
            total_refs,
            unique_bytes,
            logical_bytes,
            saved_bytes,
            dedup_ratio,
        }
    }
}

/// Content information
#[derive(Debug, Clone)]
struct ContentInfo {
    key: String,
    size: u64,
    refs: usize,
}

/// Deduplication result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DedupResult {
    pub hash: String,
    pub key: String,
    pub size: u64,
    pub deduplicated: bool,
    pub saved_bytes: u64,
}

/// Deduplication statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DedupStats {
    pub total_content: usize,
    pub total_refs: usize,
    pub unique_bytes: u64,
    pub logical_bytes: u64,
    pub saved_bytes: u64,
    pub dedup_ratio: f64,
}

/// Garbage collection result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GcResult {
    pub deleted: usize,
    pub freed_bytes: u64,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::storage::backend::LocalStorage;
    use tempfile::TempDir;
    
    #[tokio::test]
    async fn test_dedup_upload() {
        let tmp = TempDir::new().unwrap();
        let backend = Arc::new(LocalStorage::new(tmp.path()).unwrap());
        let manager = DedupManager::new(backend);
        
        let data = Bytes::from("test content");
        
        // First upload
        let result1 = manager.upload_deduplicated(data.clone()).await.unwrap();
        assert!(!result1.deduplicated);
        assert_eq!(result1.saved_bytes, 0);
        
        // Second upload (same content)
        let result2 = manager.upload_deduplicated(data).await.unwrap();
        assert!(result2.deduplicated);
        assert_eq!(result2.hash, result1.hash);
        assert_eq!(result2.saved_bytes, result1.size);
    }
    
    #[tokio::test]
    async fn test_dedup_stats() {
        let tmp = TempDir::new().unwrap();
        let backend = Arc::new(LocalStorage::new(tmp.path()).unwrap());
        let manager = DedupManager::new(backend);
        
        let data = Bytes::from("test content");
        
        // Upload same content twice
        manager.upload_deduplicated(data.clone()).await.unwrap();
        manager.upload_deduplicated(data).await.unwrap();
        
        let stats = manager.dedup_stats().unwrap();
        
        assert_eq!(stats.total_content, 1); // Only one unique content
        assert_eq!(stats.total_refs, 2); // Two references
        assert!(stats.saved_bytes > 0);
        assert!(stats.dedup_ratio > 0.0);
    }
    
    #[tokio::test]
    async fn test_dedup_delete() {
        let tmp = TempDir::new().unwrap();
        let backend = Arc::new(LocalStorage::new(tmp.path()).unwrap());
        let manager = DedupManager::new(backend);
        
        let data = Bytes::from("test content");
        
        let result = manager.upload_deduplicated(data).await.unwrap();
        
        // Delete (should remove)
        let deleted = manager.delete_by_hash(&result.hash).await.unwrap();
        assert!(deleted);
    }
    
    #[tokio::test]
    async fn test_dedup_refcount() {
        let tmp = TempDir::new().unwrap();
        let backend = Arc::new(LocalStorage::new(tmp.path()).unwrap());
        let manager = DedupManager::new(backend);
        
        let data = Bytes::from("test content");
        
        // Upload twice
        let result = manager.upload_deduplicated(data.clone()).await.unwrap();
        manager.upload_deduplicated(data).await.unwrap();
        
        // First delete (should not remove, refs=1)
        let deleted1 = manager.delete_by_hash(&result.hash).await.unwrap();
        assert!(!deleted1);
        
        // Second delete (should remove, refs=0)
        let deleted2 = manager.delete_by_hash(&result.hash).await.unwrap();
        assert!(deleted2);
    }
    
    #[tokio::test]
    async fn test_garbage_collection() {
        let tmp = TempDir::new().unwrap();
        let backend = Arc::new(LocalStorage::new(tmp.path()).unwrap());
        let manager = DedupManager::new(backend);
        
        let data = Bytes::from("test content");
        let result = manager.upload_deduplicated(data).await.unwrap();
        
        // Delete to make unreferenced
        manager.delete_by_hash(&result.hash).await.unwrap();
        
        // Run GC
        let gc_result = manager.garbage_collect().await.unwrap();
        
        assert_eq!(gc_result.deleted, 1);
        assert!(gc_result.freed_bytes > 0);
    }
}
