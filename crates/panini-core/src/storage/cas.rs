//! Content-Addressed Storage (CAS) with atomic decomposition

use crate::error::{Error, Result};
use crate::storage::atom::{Atom, AtomMetadata, AtomType};
use crate::storage::backends::StorageBackend;
use bytes::Bytes;
use petgraph::graph::{DiGraph, NodeIndex};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

/// Content-Addressed Storage manager
pub struct ContentAddressedStorage<B: StorageBackend> {
    /// Storage backend (S3, LocalFS, etc.)
    backend: Arc<B>,
    
    /// Atom index for fast lookups
    atom_index: Arc<RwLock<HashMap<String, AtomMetadata>>>,
    
    /// Atom composition graph (parent-child relationships)
    atom_graph: Arc<RwLock<DiGraph<String, String>>>,
    
    /// Hash to graph node mapping
    node_map: Arc<RwLock<HashMap<String, NodeIndex>>>,
    
    /// Configuration
    config: StorageConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageConfig {
    /// Maximum atom size before splitting (bytes)
    pub max_atom_size: u64,
    
    /// Enable automatic deduplication
    pub enable_dedup: bool,
    
    /// Compression algorithm
    pub compression: Option<String>,
}

impl Default for StorageConfig {
    fn default() -> Self {
        Self {
            max_atom_size: 10 * 1024 * 1024, // 10 MB
            enable_dedup: true,
            compression: None,
        }
    }
}

impl<B: StorageBackend> ContentAddressedStorage<B> {
    /// Create new CAS manager
    pub fn new(backend: Arc<B>, config: StorageConfig) -> Self {
        Self {
            backend,
            atom_index: Arc::new(RwLock::new(HashMap::new())),
            atom_graph: Arc::new(RwLock::new(DiGraph::new())),
            node_map: Arc::new(RwLock::new(HashMap::new())),
            config,
        }
    }

    /// Add atom to storage
    pub async fn add_atom(&self, data: &[u8], atom_type: AtomType) -> Result<Atom> {
        let atom = Atom::new(data, atom_type);
        
        // Check if atom already exists (deduplication)
        if self.config.enable_dedup {
            let index = self.atom_index.read().unwrap();
            if let Some(existing) = index.get(&atom.hash) {
                // Atom exists, increment ref count
                drop(index);
                self.increment_atom_refs(&atom.hash)?;
                return Ok(atom);
            }
        }
        
        // Store atom data in backend
        self.backend
            .upload(&atom.hash, Bytes::copy_from_slice(data))
            .await?;
        
        // Add to index
        let mut metadata = AtomMetadata::from(&atom);
        metadata.ref_count = 1;
        self.atom_index
            .write()
            .unwrap()
            .insert(atom.hash.clone(), metadata);
        
        // Add to graph
        self.add_to_graph(&atom)?;
        
        Ok(atom)
    }

    /// Get atom data from storage
    pub async fn get_atom(&self, hash: &str) -> Result<Bytes> {
        // Check if atom exists
        {
            let index = self.atom_index.read().unwrap();
            if !index.contains_key(hash) {
                return Err(Error::generic(format!("Atom not found: {}", hash)));
            }
        }
        
        // Fetch from backend
        self.backend.download(hash).await
    }

    /// Get atom metadata
    pub fn get_atom_metadata(&self, hash: &str) -> Result<AtomMetadata> {
        let index = self.atom_index.read().unwrap();
        index
            .get(hash)
            .cloned()
            .ok_or_else(|| Error::generic(format!("Atom not found: {}", hash)))
    }

    /// List all atoms
    pub fn list_atoms(&self) -> Vec<AtomMetadata> {
        let index = self.atom_index.read().unwrap();
        index.values().cloned().collect()
    }

    /// Get atoms by type
    pub fn get_atoms_by_type(&self, atom_type: AtomType) -> Vec<AtomMetadata> {
        let index = self.atom_index.read().unwrap();
        index
            .values()
            .filter(|m| m.atom_type == atom_type)
            .cloned()
            .collect()
    }

    /// Get storage statistics
    pub async fn get_stats(&self) -> StorageStats {
        let index = self.atom_index.read().unwrap();
        
        let total_atoms = index.len() as u64;
        let total_size: u64 = index.values().map(|m| m.size).sum();
        let dedup_atoms = index.values().filter(|m| m.ref_count > 1).count() as u64;
        let dedup_savings: u64 = index
            .values()
            .filter(|m| m.ref_count > 1)
            .map(|m| m.size * (m.ref_count as u64 - 1))
            .sum();
        
        StorageStats {
            total_atoms,
            total_size,
            dedup_atoms,
            dedup_savings,
            unique_atoms: total_atoms - dedup_atoms,
        }
    }

    /// Increment atom reference count
    pub fn increment_atom_refs(&self, hash: &str) -> Result<()> {
        let mut index = self.atom_index.write().unwrap();
        if let Some(metadata) = index.get_mut(hash) {
            metadata.ref_count = metadata.ref_count.saturating_add(1);
            Ok(())
        } else {
            Err(Error::generic(format!("Atom not found: {}", hash)))
        }
    }

    /// Decrement atom reference count
    pub fn decrement_atom_refs(&self, hash: &str) -> Result<()> {
        let mut index = self.atom_index.write().unwrap();
        if let Some(metadata) = index.get_mut(hash) {
            metadata.ref_count = metadata.ref_count.saturating_sub(1);
            Ok(())
        } else {
            Err(Error::generic(format!("Atom not found: {}", hash)))
        }
    }

    /// Find orphaned atoms (ref_count == 0)
    pub fn find_orphaned_atoms(&self) -> Vec<String> {
        let index = self.atom_index.read().unwrap();
        index
            .iter()
            .filter(|(_, m)| m.ref_count == 0)
            .map(|(hash, _)| hash.clone())
            .collect()
    }

    /// Garbage collect orphaned atoms
    pub async fn gc_orphaned_atoms(&self) -> Result<GcStats> {
        let orphaned = self.find_orphaned_atoms();
        let mut deleted = 0;
        let mut freed_size = 0u64;
        
        for hash in orphaned {
            if let Ok(metadata) = self.get_atom_metadata(&hash) {
                // Delete from backend
                self.backend.delete(&hash).await?;
                
                // Remove from index
                self.atom_index.write().unwrap().remove(&hash);
                
                // Remove from graph
                self.remove_from_graph(&hash)?;
                
                deleted += 1;
                freed_size += metadata.size;
            }
        }
        
        Ok(GcStats {
            atoms_deleted: deleted,
            bytes_freed: freed_size,
        })
    }

    /// Add atom to composition graph
    fn add_to_graph(&self, atom: &Atom) -> Result<()> {
        let mut graph = self.atom_graph.write().unwrap();
        let mut node_map = self.node_map.write().unwrap();
        
        // Add node for this atom
        let node_idx = graph.add_node(atom.hash.clone());
        node_map.insert(atom.hash.clone(), node_idx);
        
        // Add edges to children
        for child_hash in &atom.children {
            if let Some(&child_idx) = node_map.get(child_hash) {
                graph.add_edge(node_idx, child_idx, "contains".to_string());
            }
        }
        
        // Add edge from parent
        if let Some(parent_hash) = &atom.parent {
            if let Some(&parent_idx) = node_map.get(parent_hash) {
                graph.add_edge(parent_idx, node_idx, "contains".to_string());
            }
        }
        
        Ok(())
    }

    /// Remove atom from composition graph
    fn remove_from_graph(&self, hash: &str) -> Result<()> {
        let mut graph = self.atom_graph.write().unwrap();
        let mut node_map = self.node_map.write().unwrap();
        
        if let Some(node_idx) = node_map.remove(hash) {
            graph.remove_node(node_idx);
        }
        
        Ok(())
    }

    /// Get atom children (direct descendants)
    pub fn get_atom_children(&self, hash: &str) -> Result<Vec<String>> {
        let graph = self.atom_graph.read().unwrap();
        let node_map = self.node_map.read().unwrap();
        
        if let Some(&node_idx) = node_map.get(hash) {
            let children = graph
                .neighbors(node_idx)
                .map(|idx| graph[idx].clone())
                .collect();
            Ok(children)
        } else {
            Ok(Vec::new())
        }
    }
    /// Decompose binary data into atoms and store them
    /// Returns list of atom hashes in order
    pub async fn decompose_and_store(
        &self,
        data: &[u8],
        format: &crate::storage::decomposer::FileFormat,
    ) -> Result<Vec<String>> {
        // For now, use simple chunking strategy
        // TODO: Implement proper format-aware decomposition
        let mut hashes = Vec::new();
        const CHUNK_SIZE: usize = 64 * 1024; // 64KB chunks
        
        if data.len() <= CHUNK_SIZE {
            // Small file, store as single atom
            let atom = self.add_atom(data, AtomType::Raw).await?;
            hashes.push(atom.hash);
        } else {
            // Large file, chunk it
            for (i, chunk) in data.chunks(CHUNK_SIZE).enumerate() {
                let atom_type = if i == 0 {
                    AtomType::Container // First chunk
                } else {
                    AtomType::Raw
                };
                let atom = self.add_atom(chunk, atom_type).await?;
                hashes.push(atom.hash);
            }
        }
        
        Ok(hashes)
    }


    }

/// Storage statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageStats {
    pub total_atoms: u64,
    pub total_size: u64,
    pub dedup_atoms: u64,
    pub dedup_savings: u64,
    pub unique_atoms: u64,
}

impl StorageStats {
    pub fn dedup_ratio(&self) -> f64 {
        if self.total_atoms == 0 {
            0.0
        } else {
            (self.dedup_atoms as f64 / self.total_atoms as f64) * 100.0
        }
    }
}

/// Garbage collection statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GcStats {
    pub atoms_deleted: u64,
    pub bytes_freed: u64,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::storage::backend::{LocalFsBackend, UploadResult};
    use tempfile::TempDir;

    #[tokio::test]
    async fn test_cas_add_atom() {
        let temp_dir = TempDir::new().unwrap();
        let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
        let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
        
        let data = b"test atom data";
        let atom = cas.add_atom(data, AtomType::Container).await.unwrap();
        
        assert_eq!(atom.size, 14);
        assert_eq!(atom.atom_type, AtomType::Container);
    }

    #[tokio::test]
    async fn test_cas_deduplication() {
        let temp_dir = TempDir::new().unwrap();
        let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
        let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
        
        let data = b"duplicate data";
        
        // Add same data twice
        let atom1 = cas.add_atom(data, AtomType::Container).await.unwrap();
        let atom2 = cas.add_atom(data, AtomType::Raw).await.unwrap();
        
        // Should have same hash
        assert_eq!(atom1.hash, atom2.hash);
        
        // Check ref count
        let metadata = cas.get_atom_metadata(&atom1.hash).unwrap();
        assert_eq!(metadata.ref_count, 2);
    }

    #[tokio::test]
    async fn test_cas_get_atom() {
        let temp_dir = TempDir::new().unwrap();
        let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
        let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
        
        let data = b"retrievable data";
        let atom = cas.add_atom(data, AtomType::Container).await.unwrap();
        
        let retrieved = cas.get_atom(&atom.hash).await.unwrap();
        assert_eq!(&retrieved[..], data);
    }

    #[tokio::test]
    async fn test_cas_stats() {
        let temp_dir = TempDir::new().unwrap();
        let backend = Arc::new(LocalFsBackend::new(temp_dir.path()).unwrap());
        let cas = ContentAddressedStorage::new(backend, StorageConfig::default());
        
        cas.add_atom(b"atom1", AtomType::Container).await.unwrap();
        cas.add_atom(b"atom2", AtomType::IFrame).await.unwrap();
        
        let stats = cas.get_stats();
        assert_eq!(stats.total_atoms, 2);
        assert!(stats.total_size > 0);
    }
}
