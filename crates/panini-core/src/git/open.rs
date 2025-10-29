//! Repository opening and validation

use crate::error::{Error, Result};
use git2::Repository;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};

/// Panini configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PaniniConfig {
    pub version: String,
    pub repository: RepositoryConfig,
    pub storage: StorageConfig,
    pub sync: SyncConfig,
    pub index: IndexConfig,
    pub query: QueryConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RepositoryConfig {
    pub name: String,
    pub created: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageConfig {
    pub default: String,
    pub backends: serde_yaml::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyncConfig {
    pub auto_pull: bool,
    pub auto_push: bool,
    pub interval: u64,
    pub conflict_strategy: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IndexConfig {
    pub rebuild_on_startup: bool,
    pub fulltext_languages: Vec<String>,
    pub cache_size_mb: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueryConfig {
    pub default_limit: usize,
    pub max_limit: usize,
    pub result_format: String,
}

/// Schema version information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SchemaVersion {
    pub version: String,
    pub created: String,
    pub relation_types: Vec<String>,
    pub dhatu_types: Vec<String>,
}

/// Open an existing Panini repository
pub fn open_repo(path: &Path) -> Result<Repository> {
    let path = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
    
    // Check if .panini exists
    if !path.join(".panini").exists() {
        return Err(Error::RepoNotInitialized(path.clone()));
    }
    
    // Check if .git exists
    if !path.join(".git").exists() {
        return Err(Error::RepoNotInitialized(path.clone()));
    }
    
    // Open Git repository
    let repo = Repository::open(&path)?;
    
    // Validate configuration
    validate_config(&path)?;
    
    // Validate schema
    validate_schema(&path)?;
    
    Ok(repo)
}

/// Load configuration from file
pub fn load_config(path: &Path) -> Result<PaniniConfig> {
    let config_path = path.join(".panini/config.yaml");
    
    if !config_path.exists() {
        return Err(Error::Config("config.yaml not found".to_string()));
    }
    
    let config_content = fs::read_to_string(&config_path)?;
    let config: PaniniConfig = serde_yaml::from_str(&config_content)
        .map_err(|e| Error::Config(format!("Failed to parse config.yaml: {}", e)))?;
    
    Ok(config)
}

/// Load schema from file
pub fn load_schema(path: &Path) -> Result<SchemaVersion> {
    let schema_path = path.join(".panini/schema.yaml");
    
    if !schema_path.exists() {
        return Err(Error::Config("schema.yaml not found".to_string()));
    }
    
    let schema_content = fs::read_to_string(&schema_path)?;
    let schema: SchemaVersion = serde_yaml::from_str(&schema_content)
        .map_err(|e| Error::Config(format!("Failed to parse schema.yaml: {}", e)))?;
    
    Ok(schema)
}

/// Validate configuration
fn validate_config(path: &Path) -> Result<()> {
    let config = load_config(path)?;
    
    // Check version format
    if config.version.is_empty() {
        return Err(Error::Config("Invalid version in config.yaml".to_string()));
    }
    
    // Validate sync strategy
    let valid_strategies = ["prompt", "auto", "manual"];
    if !valid_strategies.contains(&config.sync.conflict_strategy.as_str()) {
        return Err(Error::Config(format!(
            "Invalid conflict_strategy: {}. Must be one of: {:?}",
            config.sync.conflict_strategy, valid_strategies
        )));
    }
    
    Ok(())
}

/// Validate schema
fn validate_schema(path: &Path) -> Result<()> {
    let schema = load_schema(path)?;
    
    // Check version format (semver)
    if !schema.version.contains('.') {
        return Err(Error::SchemaVersionMismatch {
            expected: "x.y.z".to_string(),
            actual: schema.version.clone(),
        });
    }
    
    // Validate relation types
    let expected_relations = vec![
        "is_a", "part_of", "causes", "contradicts", 
        "supports", "derives_from", "used_by", "related_to"
    ];
    
    for rel_type in &expected_relations {
        if !schema.relation_types.contains(&rel_type.to_string()) {
            return Err(Error::Config(format!(
                "Missing required relation type: {}",
                rel_type
            )));
        }
    }
    
    // Validate dhatu types
    let expected_dhatus = vec![
        "TEXT", "IMAGE", "VIDEO", "AUDIO", 
        "CODE", "BINARY", "ARCHIVE"
    ];
    
    for dhatu in &expected_dhatus {
        if !schema.dhatu_types.contains(&dhatu.to_string()) {
            return Err(Error::Config(format!(
                "Missing required dhatu type: {}",
                dhatu
            )));
        }
    }
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use tempfile::TempDir;
    
    #[test]
    fn test_open_repo_success() {
        let tmp = TempDir::new().unwrap();
        init_repo(tmp.path()).unwrap();
        
        let repo = open_repo(tmp.path()).unwrap();
        assert!(repo.path().exists());
    }
    
    #[test]
    fn test_open_repo_not_initialized() {
        let tmp = TempDir::new().unwrap();
        
        let result = open_repo(tmp.path());
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("not initialized"));
    }
    
    #[test]
    fn test_load_config() {
        let tmp = TempDir::new().unwrap();
        init_repo(tmp.path()).unwrap();
        
        let config = load_config(tmp.path()).unwrap();
        assert_eq!(config.version, "1.0");
        assert_eq!(config.storage.default, "local");
    }
    
    #[test]
    fn test_load_schema() {
        let tmp = TempDir::new().unwrap();
        init_repo(tmp.path()).unwrap();
        
        let schema = load_schema(tmp.path()).unwrap();
        assert_eq!(schema.version, "1.0.0");
        assert_eq!(schema.relation_types.len(), 8);
        assert_eq!(schema.dhatu_types.len(), 7);
    }
}
