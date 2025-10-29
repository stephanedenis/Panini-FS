//! High-level repository operations

use crate::error::Result;
use crate::git::init::init_repo;
use crate::git::open::{load_config, load_schema, open_repo, PaniniConfig, SchemaVersion};
use git2::Repository;
use std::path::{Path, PathBuf};

/// High-level Panini repository wrapper
pub struct PaniniRepo {
    pub repo: Repository,
    pub path: PathBuf,
    pub config: PaniniConfig,
    pub schema: SchemaVersion,
}

impl PaniniRepo {
    /// Initialize a new repository
    pub fn init(path: impl AsRef<Path>) -> Result<Self> {
        let path = path.as_ref();
        let repo = init_repo(path)?;
        let path = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
        let config = load_config(&path)?;
        let schema = load_schema(&path)?;
        
        Ok(Self {
            repo,
            path,
            config,
            schema,
        })
    }

    /// Open an existing repository
    pub fn open(path: impl AsRef<Path>) -> Result<Self> {
        let path = path.as_ref();
        let repo = open_repo(path)?;
        let path = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
        let config = load_config(&path)?;
        let schema = load_schema(&path)?;
        
        Ok(Self {
            repo,
            path,
            config,
            schema,
        })
    }
    
    /// Get repository path
    pub fn path(&self) -> &Path {
        &self.path
    }
    
    /// Get Git repository
    pub fn git(&self) -> &Repository {
        &self.repo
    }
    
    /// Get configuration
    pub fn config(&self) -> &PaniniConfig {
        &self.config
    }
    
    /// Get schema version
    pub fn schema(&self) -> &SchemaVersion {
        &self.schema
    }
    
    /// Commit a single file
    pub fn commit_file(&self, file_path: &Path, message: &str) -> Result<git2::Oid> {
        crate::git::commit::commit_file(&self.repo, file_path, message)
    }
    
    /// Commit multiple files
    pub fn commit_batch(&self, file_paths: &[&Path], message: &str) -> Result<git2::Oid> {
        crate::git::commit::commit_batch(&self.repo, file_paths, message)
    }
    
    /// Stage all changes
    pub fn stage_all(&self) -> Result<()> {
        crate::git::commit::stage_all(&self.repo)
    }
    
    /// Add a submodule
    pub fn add_submodule(&self, url: &str, path: &Path) -> Result<()> {
        crate::git::submodule::add_submodule(&self.repo, url, path)
    }
    
    /// Remove a submodule
    pub fn remove_submodule(&self, path: &Path) -> Result<()> {
        crate::git::submodule::remove_submodule(&self.repo, path)
    }
    
    /// Update all submodules
    pub fn update_submodules(&self) -> Result<Vec<String>> {
        crate::git::submodule::update_submodules(&self.repo)
    }
    
    /// List all submodules
    pub fn list_submodules(&self) -> Result<Vec<crate::git::submodule::SubmoduleInfo>> {
        crate::git::submodule::list_submodules(&self.repo)
    }
    
    /// Clone a repository
    pub fn clone(url: &str, path: &Path, options: crate::git::clone::CloneOptions) -> Result<Self> {
        let repo = crate::git::clone::clone_repo(url, path, options)?;
        let path = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
        let config = load_config(&path)?;
        let schema = load_schema(&path)?;
        
        Ok(Self {
            repo,
            path,
            config,
            schema,
        })
    }
    
    /// Fetch from remote
    pub fn fetch(&self, remote_name: &str, refspecs: &[&str]) -> Result<()> {
        crate::git::sync::fetch(&self.repo, remote_name, refspecs)
    }
    
    /// Fetch all remotes
    pub fn fetch_all(&self) -> Result<Vec<String>> {
        crate::git::sync::fetch_all(&self.repo)
    }
    
    /// Pull (fetch + merge)
    pub fn pull(&self, remote_name: &str, branch: &str) -> Result<()> {
        crate::git::sync::pull(&self.repo, remote_name, branch)
    }
    
    /// Pull with conflict strategy
    pub fn pull_with_strategy(
        &self,
        remote_name: &str,
        branch: &str,
        strategy: crate::git::sync::ConflictStrategy,
    ) -> Result<crate::git::sync::PullResult> {
        crate::git::sync::pull_with_strategy(&self.repo, remote_name, branch, strategy)
    }
    
    /// Push to remote
    pub fn push(&self, remote_name: &str, refspecs: &[&str]) -> Result<()> {
        crate::git::sync::push(&self.repo, remote_name, refspecs)
    }
    
    /// Push current branch
    pub fn push_current_branch(&self, remote_name: &str) -> Result<()> {
        crate::git::sync::push_current_branch(&self.repo, remote_name)
    }
    
    /// Push all branches
    pub fn push_all_branches(&self, remote_name: &str) -> Result<Vec<String>> {
        crate::git::sync::push_all_branches(&self.repo, remote_name)
    }
    
    /// Push with tags
    pub fn push_with_tags(&self, remote_name: &str) -> Result<()> {
        crate::git::sync::push_with_tags(&self.repo, remote_name)
    }
    
    /// Force push
    pub fn force_push(&self, remote_name: &str, branch: &str) -> Result<()> {
        crate::git::sync::force_push(&self.repo, remote_name, branch)
    }
    
    /// Push with status check
    pub fn push_with_status(
        &self,
        remote_name: &str,
        branch: &str,
    ) -> Result<crate::git::sync::PushResult> {
        crate::git::sync::push_with_status(&self.repo, remote_name, branch)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[test]
    fn test_panini_repo_init() {
        let tmp = TempDir::new().unwrap();
        let panini_repo = PaniniRepo::init(tmp.path()).unwrap();
        
        assert!(panini_repo.path().exists());
        assert_eq!(panini_repo.config().version, "1.0");
        assert_eq!(panini_repo.schema().version, "1.0.0");
    }
    
    #[test]
    fn test_panini_repo_open() {
        let tmp = TempDir::new().unwrap();
        PaniniRepo::init(tmp.path()).unwrap();
        
        let panini_repo = PaniniRepo::open(tmp.path()).unwrap();
        assert!(panini_repo.path().exists());
    }
}
