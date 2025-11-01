//! Dynamic tree builder for FUSE filesystem
//!
//! Builds the inode tree dynamically from CAS storage contents.
//! Populates /concepts/, /snapshots/, and /time/ directories.

use crate::inode::{InodeTable, CONCEPTS_DIR_INODE, SNAPSHOTS_DIR_INODE, TIME_TRAVEL_DIR_INODE};
use crate::storage_bridge::StorageBridge;
use anyhow::Result;
use std::collections::HashMap;
use tracing;

/// Build the complete directory tree from storage
pub fn populate_tree(inodes: &mut InodeTable, storage: &StorageBridge) -> Result<()> {
    tracing::info!("Populating filesystem tree from storage...");
    
    // Use pre-created special directories
    populate_concepts(inodes, storage, CONCEPTS_DIR_INODE)?;
    populate_snapshots(inodes, storage, SNAPSHOTS_DIR_INODE)?;
    populate_time_travel(inodes, storage, TIME_TRAVEL_DIR_INODE)?;
    
    tracing::info!("Filesystem tree populated successfully");
    Ok(())
}

/// Populate /concepts/ directory with atoms organized by concept
fn populate_concepts(
    inodes: &mut InodeTable,
    storage: &StorageBridge,
    concepts_ino: u64,
) -> Result<()> {
    tracing::debug!("Populating /concepts/ directory...");
    
    // Get all atoms from storage
    let atoms = storage.list_atoms();
    tracing::info!("Found {} atoms in storage", atoms.len());
    
    // Group atoms by first 4 chars of hash for organization
    // TODO: Use proper concept metadata when available
    let mut concept_map: HashMap<String, Vec<_>> = HashMap::new();
    
    for atom in atoms {
        // Group by first 4 chars of hash as a simple categorization
        let concept = atom.hash.chars().take(4).collect::<String>();
        concept_map.entry(concept).or_insert_with(Vec::new).push(atom);
    }
    
    // Count concepts before consuming the map
    let num_concepts = concept_map.len();
    
    // Create directory for each concept
    for (concept, atoms) in concept_map {
        // Create concept directory
        let concept_ino = inodes.create_directory(concept.clone(), concepts_ino);
        
        // Add concept to parent's children
        if let Some(concepts_parent) = inodes.get_mut(concepts_ino) {
            concepts_parent.children.push(concept_ino);
        }
        
        // Add atoms as files in this concept
        for atom in atoms {
            // Create file inode for this atom
            let filename = format!("{}.txt", &atom.hash[..8]); // Use first 8 chars as filename
            let file_ino = inodes.create_file(
                filename,
                concept_ino,
                Some(atom.hash.clone()),
                atom.size as usize,
            );
            
            // Add file to concept directory
            if let Some(concept_dir) = inodes.get_mut(concept_ino) {
                concept_dir.children.push(file_ino);
            }
        }
    }
    
    tracing::debug!("Populated {} concepts", num_concepts);
    Ok(())
}

/// Populate /snapshots/ directory with repository snapshots
fn populate_snapshots(
    inodes: &mut InodeTable,
    _storage: &StorageBridge,
    snapshots_ino: u64,
) -> Result<()> {
    tracing::debug!("Populating /snapshots/ directory...");
    
    // TODO: Implement snapshot detection from storage metadata
    // For now, create a placeholder
    let placeholder_ino = inodes.create_file(
        ".placeholder".to_string(),
        snapshots_ino,
        None,
        0,
    );
    
    if let Some(snapshots_parent) = inodes.get_mut(snapshots_ino) {
        snapshots_parent.children.push(placeholder_ino);
    }
    
    tracing::debug!("Snapshots directory populated");
    Ok(())
}

/// Populate /time/ directory with temporal views
fn populate_time_travel(
    inodes: &mut InodeTable,
    _storage: &StorageBridge,
    time_ino: u64,
) -> Result<()> {
    tracing::debug!("Populating /time/ directory...");
    
    // TODO: Implement time-travel views from storage timeline
    // For now, create a placeholder
    let placeholder_ino = inodes.create_file(
        ".placeholder".to_string(),
        time_ino,
        None,
        0,
    );
    
    if let Some(time_parent) = inodes.get_mut(time_ino) {
        time_parent.children.push(placeholder_ino);
    }
    
    tracing::debug!("Time-travel directory populated");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;
    
    #[test]
    fn test_populate_tree() {
        use crate::inode::ROOT_INODE;
        
        // Create test storage
        let temp_dir = tempfile::tempdir().unwrap();
        let storage = StorageBridge::new(temp_dir.path().to_path_buf()).unwrap();
        
        // Create inode table (already has special directories)
        let mut inodes = InodeTable::new();
        
        // Populate tree
        let result = populate_tree(&mut inodes, &storage);
        assert!(result.is_ok());
        
        // Verify directories exist
        assert!(inodes.get(CONCEPTS_DIR_INODE).is_some());
        assert!(inodes.get(SNAPSHOTS_DIR_INODE).is_some());
        assert!(inodes.get(TIME_TRAVEL_DIR_INODE).is_some());
    }
}
