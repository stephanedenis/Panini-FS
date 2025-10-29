//! Sync operations (pull, push, status)

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::git::sync::{ConflictStrategy, PushStatus};
use crate::index::builder::IndexBuilder;
use crate::sync::conflict::ConflictResolver;
use serde::{Deserialize, Serialize};
use std::path::Path;

/// Sync manager for distributed collaboration
pub struct SyncManager {
    repo: PaniniRepo,
    conflict_resolver: ConflictResolver,
}

impl SyncManager {
    /// Create new sync manager
    pub fn new(repo: PaniniRepo) -> Self {
        let conflict_resolver = ConflictResolver::new(repo.clone());
        
        Self {
            repo,
            conflict_resolver,
        }
    }
    
    /// Pull changes from remote
    pub fn pull(&self, strategy: ConflictStrategy) -> Result<PullResult> {
        let start = std::time::Instant::now();
        
        // Check current status
        let pre_pull_status = self.repo.status()?;
        if !pre_pull_status.is_clean {
            return Err(Error::SyncError(
                "Working directory is not clean. Commit or stash changes first.".to_string(),
            ));
        }
        
        // Fetch from remote
        self.repo.fetch("origin")?;
        
        // Check divergence
        let divergence = self.repo.divergence("origin/main")?;
        
        if divergence.ahead == 0 && divergence.behind == 0 {
            return Ok(PullResult {
                status: PullStatus::UpToDate,
                commits_pulled: 0,
                conflicts_detected: 0,
                conflicts_resolved: 0,
                files_updated: 0,
                duration_ms: start.elapsed().as_millis() as u64,
            });
        }
        
        // Pull with conflict strategy
        let result = self.repo.pull_with_strategy("origin", "main", strategy)?;
        
        // Get conflicts
        let conflicts = self.repo.get_conflicts()?;
        let conflicts_detected = conflicts.len();
        
        let mut conflicts_resolved = 0;
        
        // Auto-resolve conflicts if any
        if conflicts_detected > 0 {
            conflicts_resolved = self.conflict_resolver.auto_resolve_all()?;
        }
        
        // Count updated files
        let post_pull_status = self.repo.status()?;
        let files_updated = post_pull_status.staged_changes.len()
            + post_pull_status.unstaged_changes.len();
        
        let duration_ms = start.elapsed().as_millis() as u64;
        
        let status = if conflicts_detected > conflicts_resolved {
            PullStatus::ConflictsRemaining
        } else if conflicts_resolved > 0 {
            PullStatus::ConflictsResolved
        } else {
            PullStatus::Success
        };
        
        Ok(PullResult {
            status,
            commits_pulled: divergence.behind,
            conflicts_detected,
            conflicts_resolved,
            files_updated,
            duration_ms,
        })
    }
    
    /// Push changes to remote
    pub fn push(&self, force: bool) -> Result<PushResult> {
        let start = std::time::Instant::now();
        
        // Check divergence
        let divergence = self.repo.divergence("origin/main")?;
        
        if divergence.behind > 0 && !force {
            return Err(Error::SyncError(
                "Remote has new commits. Pull first or use --force.".to_string(),
            ));
        }
        
        // Push with status tracking
        let push_status = self.repo.push_with_status("origin", "main")?;
        
        let duration_ms = start.elapsed().as_millis() as u64;
        
        Ok(PushResult {
            status: push_status,
            commits_pushed: divergence.ahead,
            duration_ms,
        })
    }
    
    /// Get sync status
    pub fn status(&self) -> Result<SyncStatus> {
        let repo_status = self.repo.status()?;
        let divergence = self.repo.divergence("origin/main")?;
        let conflicts = self.repo.get_conflicts()?;
        
        Ok(SyncStatus {
            is_clean: repo_status.is_clean,
            commits_ahead: divergence.ahead,
            commits_behind: divergence.behind,
            staged_changes: repo_status.staged_changes.len(),
            unstaged_changes: repo_status.unstaged_changes.len(),
            untracked_files: repo_status.untracked_files.len(),
            conflicts: conflicts.len(),
        })
    }
    
    /// Sync with remote (pull + push)
    pub fn sync(&self, strategy: ConflictStrategy) -> Result<SyncResult> {
        let start = std::time::Instant::now();
        
        // Pull first
        let pull_result = self.pull(strategy)?;
        
        // Push if no conflicts remain
        let push_result = if pull_result.status != PullStatus::ConflictsRemaining {
            Some(self.push(false)?)
        } else {
            None
        };
        
        let duration_ms = start.elapsed().as_millis() as u64;
        
        Ok(SyncResult {
            pull: pull_result,
            push: push_result,
            duration_ms,
        })
    }
    
    /// Rebuild index after sync
    pub fn rebuild_index(&self, index_path: &Path) -> Result<()> {
        let builder = IndexBuilder::new(self.repo.clone(), index_path)?;
        builder.rebuild()?;
        Ok(())
    }
}

/// Pull result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PullResult {
    pub status: PullStatus,
    pub commits_pulled: usize,
    pub conflicts_detected: usize,
    pub conflicts_resolved: usize,
    pub files_updated: usize,
    pub duration_ms: u64,
}

/// Push result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PushResult {
    pub status: PushStatus,
    pub commits_pushed: usize,
    pub duration_ms: u64,
}

/// Sync status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyncStatus {
    pub is_clean: bool,
    pub commits_ahead: usize,
    pub commits_behind: usize,
    pub staged_changes: usize,
    pub unstaged_changes: usize,
    pub untracked_files: usize,
    pub conflicts: usize,
}

impl SyncStatus {
    pub fn needs_pull(&self) -> bool {
        self.commits_behind > 0
    }
    
    pub fn needs_push(&self) -> bool {
        self.commits_ahead > 0
    }
    
    pub fn has_conflicts(&self) -> bool {
        self.conflicts > 0
    }
    
    pub fn has_changes(&self) -> bool {
        self.staged_changes > 0 || self.unstaged_changes > 0
    }
}

/// Combined sync result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyncResult {
    pub pull: PullResult,
    pub push: Option<PushResult>,
    pub duration_ms: u64,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::crud::create_concept;
    use crate::schema::dhatu::Dhatu;
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(repo: &PaniniRepo, id: &str) -> Concept {
        let concept = Concept {
            id: id.to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: format!("Test {}", id),
            tags: vec!["test".to_string()],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: format!("# Test {}", id),
        };
        
        create_concept(repo, &concept).unwrap();
        concept
    }
    
    #[test]
    fn test_sync_manager_creation() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let manager = SyncManager::new(repo);
        
        // Should be able to get status
        let status = manager.status();
        assert!(status.is_ok());
    }
    
    #[test]
    fn test_sync_status() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let manager = SyncManager::new(repo.clone());
        
        let status = manager.status().unwrap();
        
        assert!(status.is_clean);
        assert_eq!(status.commits_ahead, 0);
        assert_eq!(status.staged_changes, 0);
        assert!(!status.needs_pull());
        assert!(!status.needs_push());
    }
    
    #[test]
    fn test_status_with_changes() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        // Create a concept (makes changes)
        create_test_concept(&repo, "test1");
        
        let manager = SyncManager::new(repo);
        let status = manager.status().unwrap();
        
        // Should detect changes
        assert!(status.has_changes() || !status.is_clean);
    }
}
