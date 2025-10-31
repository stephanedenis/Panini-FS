//! Main FUSE filesystem implementation

use anyhow::Result;
use fuser::{
    Filesystem, ReplyAttr, ReplyData, ReplyDirectory, ReplyEntry, Request,
};
use std::time::Duration;

use crate::inode::{InodeTable, ROOT_INODE};
use crate::MountConfig;

/// Panini-FS FUSE filesystem
pub struct PaniniFS {
    pub(crate) config: MountConfig,
    pub(crate) inodes: InodeTable,
}

impl PaniniFS {
    pub fn new(config: MountConfig) -> Result<Self> {
        let inodes = InodeTable::new();
        
        Ok(Self {
            config,
            inodes,
        })
    }
}

impl Filesystem for PaniniFS {
    fn lookup(&mut self, _req: &Request, parent: u64, name: &std::ffi::OsStr, reply: ReplyEntry) {
        let name = name.to_str().unwrap_or("");
        tracing::debug!("lookup: parent={}, name={}", parent, name);
        self.handle_lookup(parent, name, reply);
    }
    
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
}
