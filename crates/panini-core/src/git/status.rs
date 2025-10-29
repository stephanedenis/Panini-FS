//! Git status and diff operations

use crate::error::Result;
use git2::{Repository, Status, StatusOptions};
use std::path::PathBuf;

/// File status information
#[derive(Debug, Clone)]
pub struct FileStatus {
    pub path: PathBuf,
    pub status: FileStatusType,
}

/// File status type
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FileStatusType {
    /// New file added to index
    New,
    /// Modified file
    Modified,
    /// Deleted file
    Deleted,
    /// Renamed file
    Renamed,
    /// File with type change
    TypeChange,
    /// Untracked file
    Untracked,
    /// Ignored file
    Ignored,
    /// Conflicted file
    Conflicted,
}

/// Repository status
#[derive(Debug, Clone)]
pub struct RepoStatus {
    pub staged: Vec<FileStatus>,
    pub unstaged: Vec<FileStatus>,
    pub untracked: Vec<FileStatus>,
    pub conflicted: Vec<FileStatus>,
}

/// Get repository status
pub fn status(repo: &Repository) -> Result<RepoStatus> {
    let mut opts = StatusOptions::new();
    opts.include_untracked(true);
    opts.include_ignored(false);
    opts.recurse_untracked_dirs(true);
    
    let statuses = repo.statuses(Some(&mut opts))?;
    
    let mut staged = Vec::new();
    let mut unstaged = Vec::new();
    let mut untracked = Vec::new();
    let mut conflicted = Vec::new();
    
    for entry in statuses.iter() {
        let path = PathBuf::from(entry.path().unwrap_or(""));
        let status = entry.status();
        
        // Conflicted files
        if status.is_conflicted() {
            conflicted.push(FileStatus {
                path: path.clone(),
                status: FileStatusType::Conflicted,
            });
            continue;
        }
        
        // Staged changes
        if status.intersects(
            Status::INDEX_NEW
                | Status::INDEX_MODIFIED
                | Status::INDEX_DELETED
                | Status::INDEX_RENAMED
                | Status::INDEX_TYPECHANGE,
        ) {
            let file_status = if status.is_index_new() {
                FileStatusType::New
            } else if status.is_index_modified() {
                FileStatusType::Modified
            } else if status.is_index_deleted() {
                FileStatusType::Deleted
            } else if status.is_index_renamed() {
                FileStatusType::Renamed
            } else {
                FileStatusType::TypeChange
            };
            
            staged.push(FileStatus {
                path: path.clone(),
                status: file_status,
            });
        }
        
        // Unstaged changes
        if status.intersects(
            Status::WT_MODIFIED | Status::WT_DELETED | Status::WT_RENAMED | Status::WT_TYPECHANGE,
        ) {
            let file_status = if status.is_wt_modified() {
                FileStatusType::Modified
            } else if status.is_wt_deleted() {
                FileStatusType::Deleted
            } else if status.is_wt_renamed() {
                FileStatusType::Renamed
            } else {
                FileStatusType::TypeChange
            };
            
            unstaged.push(FileStatus {
                path: path.clone(),
                status: file_status,
            });
        }
        
        // Untracked files
        if status.is_wt_new() {
            untracked.push(FileStatus {
                path,
                status: FileStatusType::Untracked,
            });
        }
    }
    
    Ok(RepoStatus {
        staged,
        unstaged,
        untracked,
        conflicted,
    })
}

/// Check if repository is clean (no changes)
pub fn is_clean(repo: &Repository) -> Result<bool> {
    let status = self::status(repo)?;
    
    Ok(status.staged.is_empty()
        && status.unstaged.is_empty()
        && status.untracked.is_empty()
        && status.conflicted.is_empty())
}

/// Get number of commits ahead/behind remote
pub fn divergence(repo: &Repository, local_branch: &str, remote_branch: &str) -> Result<(usize, usize)> {
    let local_ref = format!("refs/heads/{}", local_branch);
    let remote_ref = format!("refs/remotes/{}", remote_branch);
    
    let local_oid = repo.find_reference(&local_ref)?.target().ok_or_else(|| {
        crate::error::Error::Git(git2::Error::from_str("Local branch has no target"))
    })?;
    
    let remote_oid = repo.find_reference(&remote_ref)?.target().ok_or_else(|| {
        crate::error::Error::Git(git2::Error::from_str("Remote branch has no target"))
    })?;
    
    let (ahead, behind) = repo.graph_ahead_behind(local_oid, remote_oid)?;
    
    Ok((ahead, behind))
}

/// Diff statistics
#[derive(Debug, Clone)]
pub struct DiffStats {
    pub files_changed: usize,
    pub insertions: usize,
    pub deletions: usize,
}

/// Get diff stats between HEAD and working directory
pub fn diff_stats(repo: &Repository) -> Result<DiffStats> {
    let head = repo.head()?;
    let tree = head.peel_to_tree()?;
    
    let diff = repo.diff_tree_to_workdir(Some(&tree), None)?;
    let stats = diff.stats()?;
    
    Ok(DiffStats {
        files_changed: stats.files_changed(),
        insertions: stats.insertions(),
        deletions: stats.deletions(),
    })
}

/// Get diff between two commits
pub fn diff_commits(
    repo: &Repository,
    old_commit: &str,
    new_commit: &str,
) -> Result<DiffStats> {
    let old_oid = repo.revparse_single(old_commit)?.id();
    let new_oid = repo.revparse_single(new_commit)?.id();
    
    let old_tree = repo.find_commit(old_oid)?.tree()?;
    let new_tree = repo.find_commit(new_oid)?.tree()?;
    
    let diff = repo.diff_tree_to_tree(Some(&old_tree), Some(&new_tree), None)?;
    let stats = diff.stats()?;
    
    Ok(DiffStats {
        files_changed: stats.files_changed(),
        insertions: stats.insertions(),
        deletions: stats.deletions(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use std::fs;
    use tempfile::TempDir;
    
    #[test]
    fn test_status_empty() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let status = self::status(&repo).unwrap();
        
        assert!(status.staged.is_empty());
        assert!(status.unstaged.is_empty());
        assert!(status.untracked.is_empty());
    }
    
    #[test]
    fn test_status_untracked() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        // Create untracked file
        fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
        fs::write(tmp.path().join("knowledge/test.md"), "Test").unwrap();
        
        let status = self::status(&repo).unwrap();
        
        assert!(!status.untracked.is_empty());
        assert!(status.untracked[0].path.to_str().unwrap().contains("test.md"));
    }
    
    #[test]
    fn test_is_clean() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        assert!(is_clean(&repo).unwrap());
        
        // Add untracked file
        fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
        fs::write(tmp.path().join("knowledge/test.md"), "Test").unwrap();
        
        assert!(!is_clean(&repo).unwrap());
    }
    
    #[test]
    fn test_diff_stats_empty() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let stats = diff_stats(&repo).unwrap();
        
        assert_eq!(stats.files_changed, 0);
    }
    
    #[test]
    fn test_file_status_type() {
        let types = vec![
            FileStatusType::New,
            FileStatusType::Modified,
            FileStatusType::Deleted,
            FileStatusType::Renamed,
            FileStatusType::TypeChange,
            FileStatusType::Untracked,
            FileStatusType::Ignored,
            FileStatusType::Conflicted,
        ];
        
        assert_eq!(types.len(), 8);
    }
}
