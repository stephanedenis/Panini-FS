//! Atomic content representation for decomposed binary formats

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;

/// Type of content atom
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum AtomType {
    /// File container metadata (MP4 ftyp, moov, PNG header)
    Container,
    
    /// Video stream (H.264, VP8, etc.)
    VideoStream,
    
    /// Audio stream (AAC, MP3, etc.)
    AudioStream,
    
    /// Video I-Frame (keyframe)
    IFrame,
    
    /// Video P-Frame (predictive frame)
    PFrame,
    
    /// Video B-Frame (bidirectional frame)
    BFrame,
    
    /// Subtitle track (SRT, VTT, etc.)
    Subtitle,
    
    /// Image data (PNG IDAT, JPEG scan, etc.)
    ImageData,
    
    /// Metadata (EXIF, ID3, etc.)
    Metadata,
    
    /// Audio chunk (AAC frame, MP3 frame)
    AudioChunk,
    
    /// Compressed data (ZIP entry, etc.)
    Compressed,
    
    /// Raw binary data
    Raw,
}

impl AtomType {
    /// Check if atom type typically has high deduplication potential
    pub fn is_dedupable(&self) -> bool {
        matches!(
            self,
            AtomType::IFrame
                | AtomType::AudioChunk
                | AtomType::Subtitle
                | AtomType::Metadata
                | AtomType::Container
        )
    }

    /// Get typical size range for this atom type (min, max in bytes)
    pub fn size_range(&self) -> (u64, u64) {
        match self {
            AtomType::Container => (1024, 10 * 1024),               // 1-10 KB
            AtomType::Metadata => (512, 100 * 1024),                // 512B-100KB
            AtomType::IFrame => (50 * 1024, 5 * 1024 * 1024),       // 50KB-5MB
            AtomType::PFrame | AtomType::BFrame => (10 * 1024, 500 * 1024), // 10-500KB
            AtomType::AudioChunk => (1024, 50 * 1024),              // 1-50KB
            AtomType::Subtitle => (100, 10 * 1024),                 // 100B-10KB
            AtomType::ImageData => (1024, 10 * 1024 * 1024),        // 1KB-10MB
            AtomType::VideoStream | AtomType::AudioStream => (100 * 1024, 1024 * 1024 * 1024), // 100KB-1GB
            AtomType::Compressed => (1024, 100 * 1024 * 1024),      // 1KB-100MB
            AtomType::Raw => (0, u64::MAX),
        }
    }
}

impl std::fmt::Display for AtomType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AtomType::Container => write!(f, "Container"),
            AtomType::VideoStream => write!(f, "VideoStream"),
            AtomType::AudioStream => write!(f, "AudioStream"),
            AtomType::IFrame => write!(f, "VideoStream/IFrame"),
            AtomType::PFrame => write!(f, "VideoStream/PFrame"),
            AtomType::BFrame => write!(f, "VideoStream/BFrame"),
            AtomType::Subtitle => write!(f, "Subtitle"),
            AtomType::ImageData => write!(f, "ImageData"),
            AtomType::Metadata => write!(f, "Metadata"),
            AtomType::AudioChunk => write!(f, "AudioChunk"),
            AtomType::Compressed => write!(f, "Compressed"),
            AtomType::Raw => write!(f, "Raw"),
        }
    }
}

/// Content atom - smallest unit of storage
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Atom {
    /// SHA-256 content hash
    pub hash: String,
    
    /// Atom type
    pub atom_type: AtomType,
    
    /// Size in bytes
    pub size: u64,
    
    /// Optional parent atom hash (for hierarchical decomposition)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parent: Option<String>,
    
    /// Optional child atom hashes
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub children: Vec<String>,
    
    /// Format-specific metadata
    #[serde(default, skip_serializing_if = "HashMap::is_empty")]
    pub metadata: HashMap<String, String>,
    
    /// Original offset in source file
    #[serde(default)]
    pub source_offset: u64,
    
    /// Reference count (how many concepts use this atom)
    #[serde(default)]
    pub ref_count: u32,
}

impl Atom {
    /// Create new atom from data
    pub fn new(data: &[u8], atom_type: AtomType) -> Self {
        let hash = Self::compute_hash(data);
        Self {
            hash,
            atom_type,
            size: data.len() as u64,
            parent: None,
            children: Vec::new(),
            metadata: HashMap::new(),
            source_offset: 0,
            ref_count: 0,
        }
    }

    /// Create atom with metadata
    pub fn with_metadata(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.metadata.insert(key.into(), value.into());
        self
    }

    /// Set parent atom
    pub fn with_parent(mut self, parent_hash: String) -> Self {
        self.parent = Some(parent_hash);
        self
    }

    /// Add child atom
    pub fn add_child(&mut self, child_hash: String) {
        if !self.children.contains(&child_hash) {
            self.children.push(child_hash);
        }
    }

    /// Compute SHA-256 hash of data
    pub fn compute_hash(data: &[u8]) -> String {
        let mut hasher = Sha256::new();
        hasher.update(data);
        format!("{:x}", hasher.finalize())
    }

    /// Increment reference count
    pub fn increment_refs(&mut self) {
        self.ref_count = self.ref_count.saturating_add(1);
    }

    /// Decrement reference count
    pub fn decrement_refs(&mut self) {
        self.ref_count = self.ref_count.saturating_sub(1);
    }

    /// Check if atom is orphaned (no references)
    pub fn is_orphaned(&self) -> bool {
        self.ref_count == 0
    }
}

/// Lightweight atom metadata (for indexing)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AtomMetadata {
    pub hash: String,
    pub atom_type: AtomType,
    pub size: u64,
    pub ref_count: u32,
    #[serde(default)]
    pub created_at: u64,
}

impl From<&Atom> for AtomMetadata {
    fn from(atom: &Atom) -> Self {
        Self {
            hash: atom.hash.clone(),
            atom_type: atom.atom_type,
            size: atom.size,
            ref_count: atom.ref_count,
            created_at: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_atom_creation() {
        let data = b"test data";
        let atom = Atom::new(data, AtomType::Container);
        
        assert_eq!(atom.size, 9);
        assert_eq!(atom.atom_type, AtomType::Container);
        assert!(!atom.hash.is_empty());
        assert_eq!(atom.ref_count, 0);
    }

    #[test]
    fn test_atom_hash_consistency() {
        let data = b"consistent data";
        let atom1 = Atom::new(data, AtomType::Container);
        let atom2 = Atom::new(data, AtomType::Raw);
        
        assert_eq!(atom1.hash, atom2.hash);
    }

    #[test]
    fn test_atom_with_metadata() {
        let atom = Atom::new(b"data", AtomType::VideoStream)
            .with_metadata("codec", "h264")
            .with_metadata("fps", "30");
        
        assert_eq!(atom.metadata.get("codec"), Some(&"h264".to_string()));
        assert_eq!(atom.metadata.get("fps"), Some(&"30".to_string()));
    }

    #[test]
    fn test_atom_ref_counting() {
        let mut atom = Atom::new(b"data", AtomType::Container);
        
        assert_eq!(atom.ref_count, 0);
        assert!(atom.is_orphaned());
        
        atom.increment_refs();
        assert_eq!(atom.ref_count, 1);
        assert!(!atom.is_orphaned());
        
        atom.decrement_refs();
        assert_eq!(atom.ref_count, 0);
        assert!(atom.is_orphaned());
    }

    #[test]
    fn test_atom_type_dedupable() {
        assert!(AtomType::IFrame.is_dedupable());
        assert!(AtomType::AudioChunk.is_dedupable());
        assert!(AtomType::Metadata.is_dedupable());
        assert!(!AtomType::PFrame.is_dedupable());
        assert!(!AtomType::Raw.is_dedupable());
    }

    #[test]
    fn test_atom_parent_child() {
        let mut parent = Atom::new(b"parent", AtomType::Container);
        let child1 = Atom::new(b"child1", AtomType::IFrame);
        let child2 = Atom::new(b"child2", AtomType::PFrame);
        
        parent.add_child(child1.hash.clone());
        parent.add_child(child2.hash.clone());
        
        assert_eq!(parent.children.len(), 2);
        assert!(parent.children.contains(&child1.hash));
        
        // Test duplicate prevention
        parent.add_child(child1.hash.clone());
        assert_eq!(parent.children.len(), 2);
    }
}
