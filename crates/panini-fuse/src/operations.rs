//! FUSE filesystem operations

use fuser::{FileAttr, FileType, ReplyAttr, ReplyData, ReplyDirectory, ReplyEntry};
use libc::{ENOENT, ENOTDIR};
use std::ffi::OsStr;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use crate::filesystem::PaniniFS;
use crate::inode::{Inode, InodeType};

impl PaniniFS {
    /// Convert Inode to FileAttr for FUSE
    pub(crate) fn inode_to_attr(&self, inode: &Inode) -> FileAttr {
        let file_type = match inode.inode_type {
            InodeType::Directory => FileType::Directory,
            InodeType::File => FileType::RegularFile,
            InodeType::Symlink => FileType::Symlink,
        };
        
        let time = UNIX_EPOCH + Duration::from_secs(inode.created.timestamp() as u64);
        
        FileAttr {
            ino: inode.ino,
            size: inode.size,
            blocks: (inode.size + 511) / 512,
            atime: time,
            mtime: time,
            ctime: time,
            crtime: time,
            kind: file_type,
            perm: match inode.inode_type {
                InodeType::Directory => 0o755,
                InodeType::File => 0o444,
                InodeType::Symlink => 0o777,
            },
            nlink: 1,
            uid: unsafe { libc::getuid() },
            gid: unsafe { libc::getgid() },
            rdev: 0,
            blksize: 4096,
            flags: 0,
        }
    }
    
    /// Handle getattr - get file attributes
    pub(crate) fn handle_getattr(&self, ino: u64, reply: ReplyAttr) {
        if let Some(inode) = self.inodes.get(ino) {
            let attr = self.inode_to_attr(inode);
            reply.attr(&Duration::from_secs(1), &attr);
        } else {
            reply.error(ENOENT);
        }
    }
    
    /// Handle lookup - resolve name in directory
    pub(crate) fn handle_lookup(&self, parent: u64, name: &OsStr, reply: ReplyEntry) {
        let name_str = name.to_string_lossy();
        if let Some(parent_inode) = self.inodes.get(parent) {
            // Search for child with matching name
            for child_ino in &parent_inode.children {
                if let Some(child) = self.inodes.get(*child_ino) {
                    if child.name == name_str.as_ref() {
                        let attr = self.inode_to_attr(child);
                        reply.entry(&Duration::from_secs(1), &attr, 0);
                        return;
                    }
                }
            }
        }
        reply.error(ENOENT);
    }
    
    /// Handle readdir - list directory contents
    pub(crate) fn handle_readdir(
        &self,
        ino: u64,
        _fh: u64,
        offset: i64,
        mut reply: ReplyDirectory,
    ) {
        if let Some(inode) = self.inodes.get(ino) {
            if inode.inode_type != InodeType::Directory {
                reply.error(ENOTDIR);
                return;
            }
            
            let mut entries = vec![
                (ino, FileType::Directory, "."),
                (inode.parent.unwrap_or(ino), FileType::Directory, ".."),
            ];
            
            // Add all children
            for child_ino in &inode.children {
                if let Some(child) = self.inodes.get(*child_ino) {
                    let file_type = match child.inode_type {
                        InodeType::Directory => FileType::Directory,
                        InodeType::File => FileType::RegularFile,
                        InodeType::Symlink => FileType::Symlink,
                    };
                    entries.push((*child_ino, file_type, child.name.as_str()));
                }
            }
            
            // Return entries starting from offset
            for (i, (ino, file_type, name)) in entries.iter().enumerate().skip(offset as usize) {
                if reply.add(*ino, (i + 1) as i64, *file_type, name) {
                    break; // Buffer full
                }
            }
            
            reply.ok();
        } else {
            reply.error(ENOENT);
        }
    }
    
    /// Handle read - read file contents from CAS
    pub(crate) fn handle_read(
        &self,
        ino: u64,
        _fh: u64,
        offset: i64,
        size: u32,
        _flags: i32,
        _lock_owner: Option<u64>,
        reply: ReplyData,
    ) {
        if let Some(inode) = self.inodes.get(ino) {
            if inode.inode_type != InodeType::File {
                reply.error(libc::EISDIR);
                return;
            }
            
            if let Some(hash) = &inode.content_hash {
                // Read from real CAS storage via bridge
                match self.storage.read_atom(hash) {
                    Ok(content) => {
                        let bytes = content.as_ref();
                        let start = offset as usize;
                        let end = (start + size as usize).min(bytes.len());
                        
                        if start >= bytes.len() {
                            reply.data(&[]);
                        } else {
                            reply.data(&bytes[start..end]);
                        }
                    }
                    Err(e) => {
                        tracing::error!("Failed to read atom {}: {}", hash, e);
                        reply.error(libc::EIO);
                    }
                }
            } else {
                reply.error(libc::ENOENT);
            }
        } else {
            reply.error(libc::ENOENT);
        }
    }
    
    /// Handle readlink - read symlink target
    pub(crate) fn handle_readlink(&self, ino: u64, reply: ReplyData) {
        if let Some(inode) = self.inodes.get(ino) {
            if let Some(target) = &inode.symlink_target {
                reply.data(target.as_bytes());
            } else {
                reply.error(libc::EINVAL);
            }
        } else {
            reply.error(ENOENT);
        }
    }
}
