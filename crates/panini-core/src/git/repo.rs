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
