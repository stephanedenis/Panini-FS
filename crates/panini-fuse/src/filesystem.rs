//! Main FUSE filesystem implementation

use anyhow::Result;
use fuser::{
    Filesystem, ReplyAttr, ReplyData, ReplyDirectory, ReplyEntry, Request,
};
use std::time::Duration;

use crate::inode::{InodeTable, ROOT_INODE};
use crate::operations::*;
use crate::storage_bridge::StorageBridge;
use crate::MountConfig;

/// Panini-FS FUSE filesystem
pub struct PaniniFS {
    pub(crate) config: MountConfig,
    pub(crate) inodes: InodeTable,
    pub(crate) storage: StorageBridge,
}

impl PaniniFS {
    pub fn new(config: MountConfig) -> Result<Self> {
        let mut inodes = InodeTable::new();
        
        // Initialize storage bridge
        let storage = StorageBridge::new(config.storage_path.clone())?;
        
        // Populate filesystem tree from storage
        if let Err(e) = crate::tree_builder::populate_tree(&mut inodes, &storage) {
            tracing::warn!("Failed to populate tree from storage: {}", e);
            // Continue with empty tree
        }
        
        Ok(Self {
            config,
            inodes,
            storage,
        })
    }
}

impl Filesystem for PaniniFS {
    fn getattr(&mut self, _req: &Request, ino: u64, reply: ReplyAttr) {
        tracing::debug!("getattr: ino={}", ino);
        self.handle_getattr(ino, reply);
    }
    
    fn read(
        &mut self,
        _req: &Request,
        ino: u64,
        fh: u64,
        offset: i64,
        size: u32,
        flags: i32,
        lock_owner: Option<u64>,
        reply: ReplyData,
    ) {
        tracing::debug!("read: ino={}, offset={}, size={}", ino, offset, size);
        self.handle_read(ino, fh, offset, size, flags, lock_owner, reply);
    }
    
    fn readdir(
        &mut self,
        _req: &Request,
        ino: u64,
        fh: u64,
        offset: i64,
        reply: ReplyDirectory,
    ) {
        tracing::debug!("readdir: ino={}, offset={}", ino, offset);
        self.handle_readdir(ino, fh, offset, reply);
    }
    
    fn readlink(&mut self, _req: &Request, ino: u64, reply: ReplyData) {
        tracing::debug!("readlink: ino={}", ino);
        self.handle_readlink(ino, reply);
    }
    
    fn lookup(&mut self, _req: &Request, parent: u64, name: &std::ffi::OsStr, reply: ReplyEntry) {
        tracing::debug!("lookup: parent={}, name={:?}", parent, name);
        self.handle_lookup(parent, name, reply);
    }
}
