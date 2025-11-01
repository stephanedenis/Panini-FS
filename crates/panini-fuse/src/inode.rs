//! Inode management for Panini-FS FUSE
//!
//! Maps filesystem paths to internal storage structures

use chrono::{DateTime, Utc};
use std::collections::HashMap;

/// Inode number (unique identifier for each file/directory)
pub type InodeNum = u64;

/// Root inode number
pub const ROOT_INODE: InodeNum = 1;

/// Special inodes
pub const CONCEPTS_DIR_INODE: InodeNum = 2;
pub const SNAPSHOTS_DIR_INODE: InodeNum = 3;
pub const TIME_TRAVEL_DIR_INODE: InodeNum = 4;

/// Type of inode
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InodeType {
    Directory,
    File,
    Symlink,
}

/// Inode metadata
#[derive(Debug, Clone)]
pub struct Inode {
    pub ino: InodeNum,
    pub inode_type: InodeType,
    pub size: u64,
    pub created: DateTime<Utc>,
    pub modified: DateTime<Utc>,
    pub name: String,
    pub parent: Option<InodeNum>,
    
    /// For files: content hash in CAS
    pub content_hash: Option<String>,
    
    /// For symlinks: target path
    pub symlink_target: Option<String>,
    
    /// For directories: child inodes
    pub children: Vec<InodeNum>,
}

impl Inode {
    pub fn new_dir(ino: InodeNum, name: String, parent: Option<InodeNum>) -> Self {
        let now = Utc::now();
        Self {
            ino,
            inode_type: InodeType::Directory,
            size: 4096,
            created: now,
            modified: now,
            name,
            parent,
            content_hash: None,
            symlink_target: None,
            children: Vec::new(),
        }
    }
    
    pub fn new_file(
        ino: InodeNum,
        name: String,
        parent: Option<InodeNum>,
        size: u64,
        content_hash: String,
    ) -> Self {
        let now = Utc::now();
        Self {
            ino,
            inode_type: InodeType::File,
            size,
            created: now,
            modified: now,
            name,
            parent,
            content_hash: Some(content_hash),
            symlink_target: None,
            children: Vec::new(),
        }
    }
    
    pub fn new_symlink(
        ino: InodeNum,
        name: String,
        parent: Option<InodeNum>,
        target: String,
    ) -> Self {
        let now = Utc::now();
        Self {
            ino,
            inode_type: InodeType::Symlink,
            size: target.len() as u64,
            created: now,
            modified: now,
            name,
            parent,
            content_hash: None,
            symlink_target: Some(target),
            children: Vec::new(),
        }
    }
    
    pub fn add_child(&mut self, child_ino: InodeNum) {
        if !self.children.contains(&child_ino) {
            self.children.push(child_ino);
        }
    }
}

/// Inode table for the filesystem
#[derive(Debug)]
pub struct InodeTable {
    next_ino: InodeNum,
    inodes: HashMap<InodeNum, Inode>,
    path_to_inode: HashMap<String, InodeNum>,
}

impl InodeTable {
    pub fn new() -> Self {
        let mut table = Self {
            next_ino: TIME_TRAVEL_DIR_INODE + 1,
            inodes: HashMap::new(),
            path_to_inode: HashMap::new(),
        };
        
        // Create root directory
        let root = Inode::new_dir(ROOT_INODE, "/".to_string(), None);
        table.insert(root);
        
        // Create special directories
        let concepts = Inode::new_dir(
            CONCEPTS_DIR_INODE,
            "concepts".to_string(),
            Some(ROOT_INODE),
        );
        table.insert(concepts);
        
        let snapshots = Inode::new_dir(
            SNAPSHOTS_DIR_INODE,
            "snapshots".to_string(),
            Some(ROOT_INODE),
        );
        table.insert(snapshots);
        
        let time_travel = Inode::new_dir(
            TIME_TRAVEL_DIR_INODE,
            "time".to_string(),
            Some(ROOT_INODE),
        );
        table.insert(time_travel);
        
        // Add children to root
        if let Some(root) = table.inodes.get_mut(&ROOT_INODE) {
            root.add_child(CONCEPTS_DIR_INODE);
            root.add_child(SNAPSHOTS_DIR_INODE);
            root.add_child(TIME_TRAVEL_DIR_INODE);
        }
        
        table
    }
    
    pub fn allocate_inode(&mut self) -> InodeNum {
        let ino = self.next_ino;
        self.next_ino += 1;
        ino
    }
    
    pub fn insert(&mut self, inode: Inode) -> InodeNum {
        let ino = inode.ino;
        let path = self.compute_path(ino);
        self.path_to_inode.insert(path, ino);
        self.inodes.insert(ino, inode);
        ino
    }
    
    pub fn get(&self, ino: InodeNum) -> Option<&Inode> {
        self.inodes.get(&ino)
    }
    
    pub fn get_mut(&mut self, ino: InodeNum) -> Option<&mut Inode> {
        self.inodes.get_mut(&ino)
    }
    
    pub fn lookup_path(&self, path: &str) -> Option<InodeNum> {
        self.path_to_inode.get(path).copied()
    }
    
    fn compute_path(&self, ino: InodeNum) -> String {
        let mut path_parts = Vec::new();
        let mut current = ino;
        
        while let Some(inode) = self.inodes.get(&current) {
            if current == ROOT_INODE {
                break;
            }
            path_parts.push(inode.name.clone());
            if let Some(parent) = inode.parent {
                current = parent;
            } else {
                break;
            }
        }
        
        if path_parts.is_empty() {
            return "/".to_string();
        }
        
        path_parts.reverse();
        format!("/{}", path_parts.join("/"))
    }
    
    /// Create a new directory inode and return its number
    pub fn create_directory(&mut self, name: String, parent: InodeNum) -> InodeNum {
        let ino = self.allocate_inode();
        let inode = Inode::new_dir(ino, name, Some(parent));
        self.insert(inode);
        ino
    }
    
    /// Create a new file inode and return its number
    pub fn create_file(
        &mut self,
        name: String,
        parent: InodeNum,
        content_hash: Option<String>,
        size: usize,
    ) -> InodeNum {
        let ino = self.allocate_inode();
        let hash = content_hash.unwrap_or_else(|| String::new());
        let inode = Inode::new_file(ino, name, Some(parent), size as u64, hash);
        self.insert(inode);
        ino
    }
}

impl Default for InodeTable {
    fn default() -> Self {
        Self::new()
    }
}
