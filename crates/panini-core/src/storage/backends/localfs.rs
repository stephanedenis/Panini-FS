//! Local filesystem storage backend

use crate::error::{Error, Result};
use crate::storage::backends::{BackendStats, StorageBackend, UploadResult};
use async_trait::async_trait;
use bytes::Bytes;
use std::path::{Path, PathBuf};
use tokio::fs;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

/// Local filesystem storage backend
pub struct LocalFsBackend {
    /// Root storage directory
    root_path: PathBuf,
}

impl LocalFsBackend {
    /// Create new local filesystem backend
    pub fn new<P: AsRef<Path>>(root_path: P) -> Result<Self> {
        let root_path = root_path.as_ref().to_path_buf();
        
        // Create root directory if it doesn't exist
        std::fs::create_dir_all(&root_path).map_err(|e| {
            Error::generic(format!("Failed to create storage directory: {}", e))
        })?;
        
        Ok(Self { root_path })
    }

    /// Get file path for given key (hash)
    /// Uses 2-level sharding: aa/bb/aabbcc...
    fn key_to_path(&self, key: &str) -> PathBuf {
        if key.len() < 4 {
            return self.root_path.join(key);
        }
        
        // Shard: first 2 chars / next 2 chars / full hash
        let prefix1 = &key[0..2];
        let prefix2 = &key[2..4];
        
        self.root_path
            .join(prefix1)
            .join(prefix2)
            .join(key)
    }

    /// Ensure parent directories exist
    async fn ensure_parent_dirs(&self, path: &Path) -> Result<()> {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).await.map_err(|e| {
                Error::generic(format!("Failed to create parent directories: {}", e))
            })?;
        }
        Ok(())
    }
}

#[async_trait]
impl StorageBackend for LocalFsBackend {
    async fn upload(&self, key: &str, data: Bytes) -> Result<UploadResult> {
        let path = self.key_to_path(key);
        
        // Check if already exists
        let already_existed = path.exists();
        
        if !already_existed {
            self.ensure_parent_dirs(&path).await?;
            
            let mut file = fs::File::create(&path).await.map_err(|e| {
                Error::generic(format!("Failed to create file: {}", e))
            })?;
            
            file.write_all(&data).await.map_err(|e| {
                Error::generic(format!("Failed to write data: {}", e))
            })?;
            
            file.flush().await.map_err(|e| {
                Error::generic(format!("Failed to flush file: {}", e))
            })?;
        }
        
        Ok(UploadResult {
            key: key.to_string(),
            size: data.len() as u64,
            already_existed,
        })
    }

    async fn download(&self, key: &str) -> Result<Bytes> {
        let path = self.key_to_path(key);
        
        if !path.exists() {
            return Err(Error::generic(format!("Key not found: {}", key)));
        }
        
        let mut file = fs::File::open(&path).await.map_err(|e| {
            Error::generic(format!("Failed to open file: {}", e))
        })?;
        
        let mut buffer = Vec::new();
        file.read_to_end(&mut buffer).await.map_err(|e| {
            Error::generic(format!("Failed to read file: {}", e))
        })?;
        
        Ok(Bytes::from(buffer))
    }

    async fn delete(&self, key: &str) -> Result<()> {
        let path = self.key_to_path(key);
        
        if path.exists() {
            fs::remove_file(&path).await.map_err(|e| {
                Error::generic(format!("Failed to delete file: {}", e))
            })?;
        }
        
        Ok(())
    }

    async fn exists(&self, key: &str) -> Result<bool> {
        let path = self.key_to_path(key);
        Ok(path.exists())
    }

    async fn list_keys(&self) -> Result<Vec<String>> {
        let mut keys = Vec::new();
        self.collect_keys(&self.root_path, &mut keys).await?;
        Ok(keys)
    }

    async fn stats(&self) -> Result<BackendStats> {
        let keys = self.list_keys().await?;
        let mut total_size = 0u64;
        
        for key in &keys {
            let path = self.key_to_path(key);
            if let Ok(metadata) = fs::metadata(&path).await {
                total_size += metadata.len();
            }
        }
        
        Ok(BackendStats {
            total_objects: keys.len() as u64,
            total_size,
        })
    }
}

impl LocalFsBackend {
    /// Recursively collect all keys (file names) in storage
    async fn collect_keys(&self, dir: &Path, keys: &mut Vec<String>) -> Result<()> {
        let mut entries = fs::read_dir(dir).await.map_err(|e| {
            Error::generic(format!("Failed to read directory: {}", e))
        })?;
        
        while let Some(entry) = entries.next_entry().await.map_err(|e| {
            Error::generic(format!("Failed to read entry: {}", e))
        })? {
            let path = entry.path();
            
            if path.is_dir() {
                // Recurse into subdirectories
                Box::pin(self.collect_keys(&path, keys)).await?;
            } else if path.is_file() {
                // Extract key (filename)
                if let Some(filename) = path.file_name() {
                    if let Some(key) = filename.to_str() {
                        keys.push(key.to_string());
                    }
                }
            }
        }
        
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[tokio::test]
    async fn test_localfs_upload_download() {
        let temp_dir = TempDir::new().unwrap();
        let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
        
        let key = "abc123";
        let data = Bytes::from("test data");
        
        // Upload
        let result = backend.upload(key, data.clone()).await.unwrap();
        assert_eq!(result.key, key);
        assert_eq!(result.size, 9);
        assert!(!result.already_existed);
        
        // Download
        let retrieved = backend.download(key).await.unwrap();
        assert_eq!(retrieved, data);
    }

    #[tokio::test]
    async fn test_localfs_dedup_upload() {
        let temp_dir = TempDir::new().unwrap();
        let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
        
        let key = "dedup123";
        let data = Bytes::from("duplicate data");
        
        // First upload
        let result1 = backend.upload(key, data.clone()).await.unwrap();
        assert!(!result1.already_existed);
        
        // Second upload (should detect existing)
        let result2 = backend.upload(key, data.clone()).await.unwrap();
        assert!(result2.already_existed);
    }

    #[tokio::test]
    async fn test_localfs_delete() {
        let temp_dir = TempDir::new().unwrap();
        let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
        
        let key = "delete123";
        let data = Bytes::from("data to delete");
        
        backend.upload(key, data).await.unwrap();
        assert!(backend.exists(key).await.unwrap());
        
        backend.delete(key).await.unwrap();
        assert!(!backend.exists(key).await.unwrap());
    }

    #[tokio::test]
    async fn test_localfs_list_keys() {
        let temp_dir = TempDir::new().unwrap();
        let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
        
        backend.upload("key1", Bytes::from("data1")).await.unwrap();
        backend.upload("key2", Bytes::from("data2")).await.unwrap();
        backend.upload("key3", Bytes::from("data3")).await.unwrap();
        
        let keys = backend.list_keys().await.unwrap();
        assert_eq!(keys.len(), 3);
        assert!(keys.contains(&"key1".to_string()));
        assert!(keys.contains(&"key2".to_string()));
        assert!(keys.contains(&"key3".to_string()));
    }

    #[tokio::test]
    async fn test_localfs_stats() {
        let temp_dir = TempDir::new().unwrap();
        let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
        
        backend.upload("stat1", Bytes::from("12345")).await.unwrap();
        backend.upload("stat2", Bytes::from("67890")).await.unwrap();
        
        let stats = backend.stats().await.unwrap();
        assert_eq!(stats.total_objects, 2);
        assert_eq!(stats.total_size, 10);
    }

    #[test]
    fn test_key_to_path_sharding() {
        let temp_dir = TempDir::new().unwrap();
        let backend = LocalFsBackend::new(temp_dir.path()).unwrap();
        
        let key = "abcdef1234567890";
        let path = backend.key_to_path(key);
        
        let path_str = path.to_str().unwrap();
        assert!(path_str.contains("/ab/cd/"));
        assert!(path_str.ends_with(key));
    }
}
