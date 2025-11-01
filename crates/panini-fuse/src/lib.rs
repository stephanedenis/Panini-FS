//! Panini-FS FUSE Filesystem
//!
//! Provides a FUSE interface to mount Panini-FS as a real filesystem.
//! Supports:
//! - Content-addressed storage access
//! - Temporal navigation (time-travel)
//! - Concept/version hierarchy
//! - Read-only immutable views

pub mod filesystem;
pub mod inode;
pub mod operations;
pub mod time_travel;
pub mod storage_bridge;
pub mod tree_builder;

pub use filesystem::PaniniFS;
pub use inode::{Inode, InodeType};

use anyhow::Result;
use std::path::PathBuf;

/// Configuration for mounting Panini-FS
#[derive(Debug, Clone)]
pub struct MountConfig {
    /// Path to the storage directory
    pub storage_path: PathBuf,
    
    /// Mount point for the filesystem
    pub mount_point: PathBuf,
    
    /// Enable time-travel features
    pub enable_time_travel: bool,
    
    /// Enable concept navigation
    pub enable_concepts: bool,
    
    /// Read-only mode (always true for safety)
    pub read_only: bool,
}

impl MountConfig {
    pub fn new(storage_path: PathBuf, mount_point: PathBuf) -> Self {
        Self {
            storage_path,
            mount_point,
            enable_time_travel: true,
            enable_concepts: true,
            read_only: true,
        }
    }
}

/// Mount Panini-FS at the specified mount point
pub fn mount(config: MountConfig) -> Result<()> {
    let fs = PaniniFS::new(config.clone())?;
    
    tracing::info!("Mounting Panini-FS at {:?}", config.mount_point);
    tracing::info!("Storage: {:?}", config.storage_path);
    tracing::info!("Time-travel: {}", config.enable_time_travel);
    tracing::info!("Concepts: {}", config.enable_concepts);
    
    // Mount options
    let options = vec![
        fuser::MountOption::RO, // Read-only
        fuser::MountOption::FSName("panini-fs".to_string()),
    ];
    
    fuser::mount2(fs, &config.mount_point, &options)?;
    
    Ok(())
}
