//! S3-compatible storage backend

use crate::error::{Error, Result};
use async_trait::async_trait;
use bytes::Bytes;
use serde::{Deserialize, Serialize};
use std::path::Path;

/// Storage backend trait
#[async_trait]
pub trait StorageBackend: Send + Sync {
    /// Upload content
    async fn upload(&self, key: &str, data: Bytes) -> Result<UploadResult>;
    
    /// Download content
    async fn download(&self, key: &str) -> Result<Bytes>;
    
    /// Delete content
    async fn delete(&self, key: &str) -> Result<()>;
    
    /// Check if content exists
    async fn exists(&self, key: &str) -> Result<bool>;
    
    /// List content keys with prefix
    async fn list(&self, prefix: &str) -> Result<Vec<String>>;
    
    /// Get storage statistics
    async fn stats(&self) -> Result<StorageStats>;
}

/// Upload result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UploadResult {
    pub key: String,
    pub size: u64,
    pub hash: String,
    pub url: Option<String>,
}

/// Storage statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageStats {
    pub total_objects: usize,
    pub total_size: u64,
    pub backend_type: String,
}

/// Storage configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageConfig {
    pub backend_type: StorageBackendType,
    pub endpoint: String,
    pub bucket: String,
    pub access_key: String,
    pub secret_key: String,
    pub region: Option<String>,
}

/// Storage backend type
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum StorageBackendType {
    MinIO,
    AwsS3,
    CloudflareR2,
    BackblazeB2,
    Local,
}

impl StorageBackendType {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::MinIO => "minio",
            Self::AwsS3 => "aws-s3",
            Self::CloudflareR2 => "cloudflare-r2",
            Self::BackblazeB2 => "backblaze-b2",
            Self::Local => "local",
        }
    }
}

/// Local filesystem storage (for testing)
pub struct LocalStorage {
    base_path: std::path::PathBuf,
}

impl LocalStorage {
    pub fn new<P: AsRef<Path>>(base_path: P) -> Result<Self> {
        let base_path = base_path.as_ref().to_path_buf();
        std::fs::create_dir_all(&base_path)
            .map_err(|e| Error::StorageError(format!("Failed to create storage dir: {}", e)))?;
        
        Ok(Self { base_path })
    }
}

#[async_trait]
impl StorageBackend for LocalStorage {
    async fn upload(&self, key: &str, data: Bytes) -> Result<UploadResult> {
        let path = self.base_path.join(key);
        
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)
                .map_err(|e| Error::StorageError(format!("Failed to create dir: {}", e)))?;
        }
        
        std::fs::write(&path, &data)
            .map_err(|e| Error::StorageError(format!("Failed to write file: {}", e)))?;
        
        let hash = blake3::hash(&data).to_hex().to_string();
        
        Ok(UploadResult {
            key: key.to_string(),
            size: data.len() as u64,
            hash,
            url: Some(format!("file://{}", path.display())),
        })
    }
    
    async fn download(&self, key: &str) -> Result<Bytes> {
        let path = self.base_path.join(key);
        
        let data = std::fs::read(&path)
            .map_err(|e| Error::StorageError(format!("Failed to read file: {}", e)))?;
        
        Ok(Bytes::from(data))
    }
    
    async fn delete(&self, key: &str) -> Result<()> {
        let path = self.base_path.join(key);
        
        std::fs::remove_file(&path)
            .map_err(|e| Error::StorageError(format!("Failed to delete file: {}", e)))?;
        
        Ok(())
    }
    
    async fn exists(&self, key: &str) -> Result<bool> {
        let path = self.base_path.join(key);
        Ok(path.exists())
    }
    
    async fn list(&self, prefix: &str) -> Result<Vec<String>> {
        let prefix_path = self.base_path.join(prefix);
        
        let mut keys = Vec::new();
        
        if prefix_path.is_dir() {
            for entry in walkdir::WalkDir::new(&prefix_path) {
                let entry = entry.map_err(|e| Error::StorageError(e.to_string()))?;
                
                if entry.file_type().is_file() {
                    if let Ok(relative) = entry.path().strip_prefix(&self.base_path) {
                        keys.push(relative.to_string_lossy().to_string());
                    }
                }
            }
        }
        
        Ok(keys)
    }
    
    async fn stats(&self) -> Result<StorageStats> {
        let mut total_objects = 0;
        let mut total_size = 0u64;
        
        for entry in walkdir::WalkDir::new(&self.base_path) {
            let entry = entry.map_err(|e| Error::StorageError(e.to_string()))?;
            
            if entry.file_type().is_file() {
                total_objects += 1;
                if let Ok(metadata) = entry.metadata() {
                    total_size += metadata.len();
                }
            }
        }
        
        Ok(StorageStats {
            total_objects,
            total_size,
            backend_type: "local".to_string(),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[tokio::test]
    async fn test_local_storage_upload() {
        let tmp = TempDir::new().unwrap();
        let storage = LocalStorage::new(tmp.path()).unwrap();
        
        let data = Bytes::from("test content");
        let result = storage.upload("test.txt", data).await.unwrap();
        
        assert_eq!(result.key, "test.txt");
        assert_eq!(result.size, 12);
        assert!(!result.hash.is_empty());
    }
    
    #[tokio::test]
    async fn test_local_storage_download() {
        let tmp = TempDir::new().unwrap();
        let storage = LocalStorage::new(tmp.path()).unwrap();
        
        let data = Bytes::from("test content");
        storage.upload("test.txt", data.clone()).await.unwrap();
        
        let downloaded = storage.download("test.txt").await.unwrap();
        assert_eq!(downloaded, data);
    }
    
    #[tokio::test]
    async fn test_local_storage_exists() {
        let tmp = TempDir::new().unwrap();
        let storage = LocalStorage::new(tmp.path()).unwrap();
        
        assert!(!storage.exists("test.txt").await.unwrap());
        
        storage.upload("test.txt", Bytes::from("test")).await.unwrap();
        
        assert!(storage.exists("test.txt").await.unwrap());
    }
    
    #[tokio::test]
    async fn test_local_storage_delete() {
        let tmp = TempDir::new().unwrap();
        let storage = LocalStorage::new(tmp.path()).unwrap();
        
        storage.upload("test.txt", Bytes::from("test")).await.unwrap();
        
        storage.delete("test.txt").await.unwrap();
        
        assert!(!storage.exists("test.txt").await.unwrap());
    }
    
    #[tokio::test]
    async fn test_local_storage_list() {
        let tmp = TempDir::new().unwrap();
        let storage = LocalStorage::new(tmp.path()).unwrap();
        
        storage.upload("dir1/file1.txt", Bytes::from("test1")).await.unwrap();
        storage.upload("dir1/file2.txt", Bytes::from("test2")).await.unwrap();
        storage.upload("dir2/file3.txt", Bytes::from("test3")).await.unwrap();
        
        let keys = storage.list("dir1").await.unwrap();
        assert_eq!(keys.len(), 2);
    }
    
    #[tokio::test]
    async fn test_local_storage_stats() {
        let tmp = TempDir::new().unwrap();
        let storage = LocalStorage::new(tmp.path()).unwrap();
        
        storage.upload("file1.txt", Bytes::from("test1")).await.unwrap();
        storage.upload("file2.txt", Bytes::from("test2")).await.unwrap();
        
        let stats = storage.stats().await.unwrap();
        
        assert_eq!(stats.total_objects, 2);
        assert!(stats.total_size > 0);
        assert_eq!(stats.backend_type, "local");
    }
}
