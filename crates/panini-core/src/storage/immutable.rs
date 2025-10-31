//! Immutable Data Structures for Temporal Filesystem
//! 
//! This module implements Copy-on-Write (CoW) structures for versioned content.
//! Every modification creates a new version, allowing time-travel navigation.

use crate::error::Result;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashMap};
use std::sync::Arc;

/// Unique identifier for a concept (content-addressed)
pub type ConceptId = String;

/// Unique identifier for a version (timestamp + hash)
pub type VersionId = String;

/// Unique identifier for a snapshot
pub type SnapshotId = String;

/// A versioned concept with immutable history
/// 
/// Each modification creates a new ConceptVersion linked to previous version.
/// This forms a directed acyclic graph (DAG) of versions.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Concept {
    /// Unique concept identifier (derived from initial content)
    pub id: ConceptId,
    
    /// Human-readable name
    pub name: String,
    
    /// Current version (head)
    pub current_version: VersionId,
    
    /// All versions (version_id -> ConceptVersion)
    pub versions: BTreeMap<VersionId, ConceptVersion>,
    
    /// Creation timestamp
    pub created_at: DateTime<Utc>,
    
    /// Last modification timestamp
    pub updated_at: DateTime<Utc>,
    
    /// Metadata
    pub metadata: HashMap<String, String>,
}

/// A single version of a concept (immutable)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConceptVersion {
    /// Version identifier (timestamp + content hash)
    pub version_id: VersionId,
    
    /// Parent version (None for initial version)
    pub parent: Option<VersionId>,
    
    /// List of atom hashes composing this version
    pub atoms: Vec<String>,
    
    /// Total size in bytes
    pub size: u64,
    
    /// Content hash (SHA-256 of concatenated atoms)
    pub content_hash: String,
    
    /// Timestamp of this version
    pub timestamp: DateTime<Utc>,
    
    /// Author/source of modification
    pub author: String,
    
    /// Commit message
    pub message: String,
    
    /// Version-specific metadata
    pub metadata: HashMap<String, String>,
}

impl ConceptVersion {
    /// Create new version from atoms
    pub fn new(
        atoms: Vec<String>,
        size: u64,
        parent: Option<VersionId>,
        author: String,
        message: String,
    ) -> Self {
        let timestamp = Utc::now();
        let content_hash = Self::compute_content_hash(&atoms);
        let version_id = Self::generate_version_id(&timestamp, &content_hash);
        
        Self {
            version_id,
            parent,
            atoms,
            size,
            content_hash,
            timestamp,
            author,
            message,
            metadata: HashMap::new(),
        }
    }
    
    /// Compute content hash from atoms
    fn compute_content_hash(atoms: &[String]) -> String {
        let mut hasher = Sha256::new();
        for atom in atoms {
            hasher.update(atom.as_bytes());
        }
        format!("{:x}", hasher.finalize())
    }
    
    /// Generate version ID from timestamp and content hash
    fn generate_version_id(timestamp: &DateTime<Utc>, content_hash: &str) -> String {
        format!("{}_{}", timestamp.timestamp_millis(), &content_hash[..16])
    }
    
    /// Check if this version is descendant of another
    pub fn is_descendant_of(&self, ancestor_id: &VersionId) -> bool {
        let mut current = self.parent.as_ref();
        
        while let Some(parent_id) = current {
            if parent_id == ancestor_id {
                return true;
            }
            // Note: Would need access to parent versions to traverse further
            break;
        }
        
        false
    }
}

impl Concept {
    /// Create new concept with initial version
    pub fn new(
        name: String,
        atoms: Vec<String>,
        size: u64,
        author: String,
        message: String,
    ) -> Self {
        let created_at = Utc::now();
        let initial_version = ConceptVersion::new(atoms, size, None, author, message);
        let version_id = initial_version.version_id.clone();
        let content_hash = initial_version.content_hash.clone();
        
        // Concept ID is based on initial content hash
        let id = format!("concept_{}", &content_hash[..16]);
        
        let mut versions = BTreeMap::new();
        versions.insert(version_id.clone(), initial_version);
        
        Self {
            id,
            name,
            current_version: version_id,
            versions,
            created_at,
            updated_at: created_at,
            metadata: HashMap::new(),
        }
    }
    
    /// Add new version (Copy-on-Write)
    /// 
    /// Returns the new version ID
    pub fn add_version(
        &mut self,
        atoms: Vec<String>,
        size: u64,
        author: String,
        message: String,
    ) -> VersionId {
        let parent = Some(self.current_version.clone());
        let new_version = ConceptVersion::new(atoms, size, parent, author, message);
        let version_id = new_version.version_id.clone();
        
        self.versions.insert(version_id.clone(), new_version);
        self.current_version = version_id.clone();
        self.updated_at = Utc::now();
        
        version_id
    }
    
    /// Get specific version
    pub fn get_version(&self, version_id: &VersionId) -> Option<&ConceptVersion> {
        self.versions.get(version_id)
    }
    
    /// Get current version
    pub fn get_current_version(&self) -> Option<&ConceptVersion> {
        self.versions.get(&self.current_version)
    }
    
    /// Get version history (chronologically ordered)
    pub fn get_history(&self) -> Vec<&ConceptVersion> {
        let mut history: Vec<_> = self.versions.values().collect();
        history.sort_by_key(|v| v.timestamp);
        history
    }
    
    /// Revert to specific version (creates new version pointing to old content)
    pub fn revert_to(&mut self, version_id: &VersionId, author: String) -> Result<VersionId> {
        let target_version = self.versions.get(version_id)
            .ok_or_else(|| crate::error::Error::generic(format!("Version not found: {}", version_id)))?;
        
        let message = format!("Revert to version {}", version_id);
        let new_version_id = self.add_version(
            target_version.atoms.clone(),
            target_version.size,
            author,
            message,
        );
        
        Ok(new_version_id)
    }
    
    /// Get diff between two versions (simplified)
    pub fn diff(&self, from: &VersionId, to: &VersionId) -> Option<VersionDiff> {
        let from_version = self.versions.get(from)?;
        let to_version = self.versions.get(to)?;
        
        // Find added and removed atoms
        let from_set: std::collections::HashSet<_> = from_version.atoms.iter().collect();
        let to_set: std::collections::HashSet<_> = to_version.atoms.iter().collect();
        
        let added: Vec<String> = to_set.difference(&from_set).map(|s| s.to_string()).collect();
        let removed: Vec<String> = from_set.difference(&to_set).map(|s| s.to_string()).collect();
        
        Some(VersionDiff {
            from: from.clone(),
            to: to.clone(),
            added_atoms: added,
            removed_atoms: removed,
            size_change: to_version.size as i64 - from_version.size as i64,
        })
    }
}

/// Difference between two versions
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VersionDiff {
    pub from: VersionId,
    pub to: VersionId,
    pub added_atoms: Vec<String>,
    pub removed_atoms: Vec<String>,
    pub size_change: i64,
}

/// A snapshot of the entire filesystem at a point in time
/// 
/// Snapshots are immutable and can be used to restore or browse historical state.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Snapshot {
    /// Unique snapshot identifier
    pub id: SnapshotId,
    
    /// Human-readable name/tag
    pub name: String,
    
    /// Timestamp when snapshot was taken
    pub timestamp: DateTime<Utc>,
    
    /// Map of concept_id -> version_id at this point in time
    pub concepts: HashMap<ConceptId, VersionId>,
    
    /// Snapshot metadata
    pub metadata: HashMap<String, String>,
    
    /// Parent snapshot (for incremental snapshots)
    pub parent: Option<SnapshotId>,
}

impl Snapshot {
    /// Create new snapshot
    pub fn new(
        name: String,
        concepts: HashMap<ConceptId, VersionId>,
        parent: Option<SnapshotId>,
    ) -> Self {
        let timestamp = Utc::now();
        let id = Self::generate_snapshot_id(&timestamp, &name);
        
        Self {
            id,
            name,
            timestamp,
            concepts,
            metadata: HashMap::new(),
            parent,
        }
    }
    
    /// Generate snapshot ID
    fn generate_snapshot_id(timestamp: &DateTime<Utc>, name: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(timestamp.to_rfc3339().as_bytes());
        hasher.update(name.as_bytes());
        let hash = format!("{:x}", hasher.finalize());
        format!("snap_{}_{}", timestamp.format("%Y%m%d_%H%M%S"), &hash[..8])
    }
}

/// Temporal index for efficient time-travel queries
/// 
/// Maintains a timeline of all changes and allows querying state at any point in time.
pub struct TemporalIndex {
    /// Map of concept_id -> Concept
    concepts: HashMap<ConceptId, Arc<Concept>>,
    
    /// Chronological timeline of all events
    timeline: BTreeMap<DateTime<Utc>, TimelineEvent>,
    
    /// All snapshots
    snapshots: HashMap<SnapshotId, Snapshot>,
}

/// An event in the timeline
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TimelineEvent {
    ConceptCreated {
        concept_id: ConceptId,
        version_id: VersionId,
    },
    ConceptModified {
        concept_id: ConceptId,
        version_id: VersionId,
        previous_version: VersionId,
    },
    SnapshotCreated {
        snapshot_id: SnapshotId,
    },
}

impl TemporalIndex {
    /// Create new temporal index
    pub fn new() -> Self {
        Self {
            concepts: HashMap::new(),
            timeline: BTreeMap::new(),
            snapshots: HashMap::new(),
        }
    }
    
    /// Add concept to index
    pub fn add_concept(&mut self, concept: Concept) {
        let timestamp = concept.created_at;
        let event = TimelineEvent::ConceptCreated {
            concept_id: concept.id.clone(),
            version_id: concept.current_version.clone(),
        };
        
        self.timeline.insert(timestamp, event);
        self.concepts.insert(concept.id.clone(), Arc::new(concept));
    }
    
    /// Update concept (creates new event)
    pub fn update_concept(&mut self, concept: Concept) {
        if let Some(previous_version) = concept.versions.values()
            .filter(|v| v.version_id != concept.current_version)
            .max_by_key(|v| v.timestamp)
        {
            let event = TimelineEvent::ConceptModified {
                concept_id: concept.id.clone(),
                version_id: concept.current_version.clone(),
                previous_version: previous_version.version_id.clone(),
            };
            
            self.timeline.insert(concept.updated_at, event);
        }
        
        self.concepts.insert(concept.id.clone(), Arc::new(concept));
    }
    
    /// Create snapshot of current state
    pub fn create_snapshot(&mut self, name: String) -> Snapshot {
        let concepts: HashMap<_, _> = self.concepts.iter()
            .map(|(id, concept)| (id.clone(), concept.current_version.clone()))
            .collect();
        
        let snapshot = Snapshot::new(name, concepts, None);
        
        let event = TimelineEvent::SnapshotCreated {
            snapshot_id: snapshot.id.clone(),
        };
        
        self.timeline.insert(snapshot.timestamp, event);
        self.snapshots.insert(snapshot.id.clone(), snapshot.clone());
        
        snapshot
    }
    
    /// Get state at specific point in time
    pub fn get_state_at(&self, timestamp: DateTime<Utc>) -> HashMap<ConceptId, VersionId> {
        let mut state = HashMap::new();
        
        // Replay events up to timestamp
        for (event_time, event) in self.timeline.range(..=timestamp) {
            match event {
                TimelineEvent::ConceptCreated { concept_id, version_id } => {
                    state.insert(concept_id.clone(), version_id.clone());
                }
                TimelineEvent::ConceptModified { concept_id, version_id, .. } => {
                    state.insert(concept_id.clone(), version_id.clone());
                }
                TimelineEvent::SnapshotCreated { .. } => {
                    // Snapshots don't change state
                }
            }
        }
        
        state
    }
    
    /// Get timeline between two timestamps
    pub fn get_timeline_range(
        &self,
        start: DateTime<Utc>,
        end: DateTime<Utc>,
    ) -> Vec<(&DateTime<Utc>, &TimelineEvent)> {
        self.timeline.range(start..=end).collect()
    }
    
    /// Get all snapshots
    pub fn get_snapshots(&self) -> Vec<&Snapshot> {
        let mut snapshots: Vec<_> = self.snapshots.values().collect();
        snapshots.sort_by_key(|s| s.timestamp);
        snapshots
    }
    
    /// Get concept by ID
    pub fn get_concept(&self, id: &ConceptId) -> Option<Arc<Concept>> {
        self.concepts.get(id).cloned()
    }
    
    /// Get all concepts
    pub fn get_all_concepts(&self) -> Vec<Arc<Concept>> {
        self.concepts.values().cloned().collect()
    }
}

impl Default for TemporalIndex {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_concept_versioning() {
        let mut concept = Concept::new(
            "test.txt".to_string(),
            vec!["atom1".to_string(), "atom2".to_string()],
            1024,
            "Alice".to_string(),
            "Initial version".to_string(),
        );
        
        assert_eq!(concept.versions.len(), 1);
        
        // Add new version
        let v2 = concept.add_version(
            vec!["atom1".to_string(), "atom3".to_string()],
            2048,
            "Bob".to_string(),
            "Updated content".to_string(),
        );
        
        assert_eq!(concept.versions.len(), 2);
        assert_eq!(concept.current_version, v2);
    }
    
    #[test]
    fn test_concept_revert() {
        let mut concept = Concept::new(
            "test.txt".to_string(),
            vec!["atom1".to_string()],
            512,
            "Alice".to_string(),
            "v1".to_string(),
        );
        
        let v1 = concept.current_version.clone();
        
        concept.add_version(
            vec!["atom2".to_string()],
            1024,
            "Bob".to_string(),
            "v2".to_string(),
        );
        
        // Revert to v1
        let v3 = concept.revert_to(&v1, "Alice".to_string()).unwrap();
        
        assert_eq!(concept.versions.len(), 3);
        assert_eq!(concept.current_version, v3);
        
        // Check content matches v1
        let current = concept.get_current_version().unwrap();
        let original = concept.get_version(&v1).unwrap();
        assert_eq!(current.atoms, original.atoms);
    }
    
    #[test]
    fn test_temporal_index() {
        let mut index = TemporalIndex::new();
        
        let concept1 = Concept::new(
            "file1.txt".to_string(),
            vec!["atom1".to_string()],
            512,
            "Alice".to_string(),
            "Create file1".to_string(),
        );
        
        let c1_id = concept1.id.clone();
        index.add_concept(concept1);
        
        // Create snapshot
        let snap1 = index.create_snapshot("Before changes".to_string());
        
        // Modify concept
        let mut concept1 = (*index.get_concept(&c1_id).unwrap()).clone();
        concept1.add_version(
            vec!["atom2".to_string()],
            1024,
            "Bob".to_string(),
            "Update file1".to_string(),
        );
        index.update_concept(concept1);
        
        // Check timeline
        assert_eq!(index.timeline.len(), 3); // Create, snapshot, modify
        assert_eq!(index.snapshots.len(), 1);
    }
    
    #[test]
    fn test_time_travel() {
        let mut index = TemporalIndex::new();
        
        let concept = Concept::new(
            "file.txt".to_string(),
            vec!["atom1".to_string()],
            512,
            "Alice".to_string(),
            "Initial".to_string(),
        );
        
        let c_id = concept.id.clone();
        let v1 = concept.current_version.clone();
        let t1 = concept.created_at;
        index.add_concept(concept);
        
        // Wait a bit and modify
        std::thread::sleep(std::time::Duration::from_millis(10));
        
        let mut concept = (*index.get_concept(&c_id).unwrap()).clone();
        concept.add_version(
            vec!["atom2".to_string()],
            1024,
            "Bob".to_string(),
            "Modified".to_string(),
        );
        let t2 = concept.updated_at;
        index.update_concept(concept);
        
        // Travel to t1
        let state_at_t1 = index.get_state_at(t1);
        assert_eq!(state_at_t1.get(&c_id), Some(&v1));
        
        // Travel to t2
        let state_at_t2 = index.get_state_at(t2);
        assert_ne!(state_at_t2.get(&c_id), Some(&v1));
    }
}
