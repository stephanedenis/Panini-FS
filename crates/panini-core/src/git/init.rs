//! Repository initialization
use std::sync::Arc;

use crate::error::{Error, Result};
use git2::{Repository, Signature};
use std::fs;
use std::path::{Path, PathBuf};

/// Gitignore template for Panini repositories
const GITIGNORE_TEMPLATE: &str = r#"# Panini-FS
.panini/index/
.panini/cache/
*.swp
*.tmp
.DS_Store
"#;

/// Default config.yaml template
const CONFIG_YAML_TEMPLATE: &str = r#"version: "1.0"

repository:
  name: "My Knowledge Base"
  created: "{created}"

storage:
  default: local
  backends:
    local:
      path: .panini/content

sync:
  auto_pull: false
  auto_push: false
  interval: 300
  conflict_strategy: prompt

index:
  rebuild_on_startup: false
  fulltext_languages:
    - en
  cache_size_mb: 256

query:
  default_limit: 50
  max_limit: 1000
  result_format: json
"#;

/// Default schema.yaml template
const SCHEMA_YAML_TEMPLATE: &str = r#"version: "1.0.0"
created: "{created}"

relation_types:
  - is_a
  - part_of
  - causes
  - contradicts
  - supports
  - derives_from
  - used_by
  - related_to

dhatu_types:
  - TEXT
  - IMAGE
  - VIDEO
  - AUDIO
  - CODE
  - BINARY
  - ARCHIVE
"#;

/// Initialize a new Panini repository
pub fn init_repo(path: &Path) -> Result<Repository> {
    let path = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
    
    // Check if already initialized
    if path.join(".git").exists() {
        return Err(Error::RepoAlreadyExists(path.clone()));
    }
    
    if path.join(".panini").exists() {
        return Err(Error::RepoAlreadyExists(path.clone()));
    }
    
    // Create directory if it doesn't exist
    if !path.exists() {
        fs::create_dir_all(&path)?;
    }
    
    // Initialize Git repository
    let repo = Repository::init(&path)?;
    
    // Create .panini directory structure
    create_panini_structure(&path)?;
    
    // Write configuration files
    write_config_files(&path)?;
    
    // Create .gitignore
    fs::write(path.join(".gitignore"), GITIGNORE_TEMPLATE)?;
    
    // Create initial README
    let readme_content = format!(
        "# Panini Knowledge Base\n\n\
         Initialized: {}\n\n\
         This is a Git-native distributed knowledge graph.\n\n\
         ## Usage\n\n\
         ```bash\n\
         # Create a concept\n\
         panini concept create\n\n\
         # Query concepts\n\
         panini query \"tag:your-tag\"\n\n\
         # Sync with remote\n\
         panini sync\n\
         ```\n",
        chrono::Utc::now().format("%Y-%m-%d")
    );
    fs::write(path.join("README.md"), readme_content)?;
    
    // Create initial commit
    create_initial_commit(&repo)?;
    
    Ok(repo)
}

/// Create .panini directory structure
fn create_panini_structure(path: &Path) -> Result<()> {
    let panini_path = path.join(".panini");
    
    // Create directories
    fs::create_dir_all(panini_path.join("index/rocksdb"))?;
    fs::create_dir_all(panini_path.join("index/tantivy"))?;
    fs::create_dir_all(panini_path.join("cache"))?;
    fs::create_dir_all(panini_path.join("content"))?;
    
    // Create knowledge directory
    fs::create_dir_all(path.join("knowledge"))?;
    
    Ok(())
}

/// Write configuration files
fn write_config_files(path: &Path) -> Result<()> {
    let panini_path = path.join(".panini");
    let now = chrono::Utc::now().to_rfc3339();
    
    // Write config.yaml
    let config_content = CONFIG_YAML_TEMPLATE.replace("{created}", &now);
    fs::write(panini_path.join("config.yaml"), config_content)?;
    
    // Write schema.yaml
    let schema_content = SCHEMA_YAML_TEMPLATE.replace("{created}", &now);
    fs::write(panini_path.join("schema.yaml"), schema_content)?;
    
    Ok(())
}

/// Create initial Git commit
fn create_initial_commit(repo: &Repository) -> Result<()> {
    // Stage files
    let mut index = repo.index()?;
    index.add_path(Path::new(".gitignore"))?;
    index.add_path(Path::new("README.md"))?;
    index.add_path(Path::new(".panini/config.yaml"))?;
    index.add_path(Path::new(".panini/schema.yaml"))?;
    index.write()?;
    
    // Create tree
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;
    
    // Create signature
    let sig = Signature::now("Panini", "panini@localhost")?;
    
    // Create initial commit
    repo.commit(
        Some("HEAD"),
        &sig,
        &sig,
        "🎉 Initialize Panini-FS repository\n\nInitial commit with:\n- Configuration files\n- Directory structure\n- README",
        &tree,
        &[],
    )?;
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[test]
    fn test_init_repo_creates_structure() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        // Check Git repository
        assert!(tmp.path().join(".git").exists());
        
        // Check .panini structure
        assert!(tmp.path().join(".panini").exists());
        assert!(tmp.path().join(".panini/config.yaml").exists());
        assert!(tmp.path().join(".panini/schema.yaml").exists());
        assert!(tmp.path().join(".panini/index").exists());
        
        // Check knowledge directory
        assert!(tmp.path().join("knowledge").exists());
        
        // Check initial commit
        let head = repo.head().unwrap();
        assert!(head.is_branch());
        
        let commit = head.peel_to_commit().unwrap();
        assert!(commit.message().unwrap().contains("Initialize Panini-FS"));
    }
    
    #[test]
    #[ignore] // FIXME: Result<PaniniRepo> unwrap_err needs Debug
    fn test_init_repo_already_exists() {
        let tmp = TempDir::new().unwrap();
        init_repo(tmp.path()).unwrap();
        
        // Try to initialize again
        let result = init_repo(tmp.path());
        assert!(result.is_err());
        assert!(result.is_err() && result.err().map(|e| e.to_string().to_string().contains("already exists")).unwrap_or(false));
    }
    
    #[test]
    fn test_config_yaml_valid() {
        let tmp = TempDir::new().unwrap();
        init_repo(tmp.path()).unwrap();
        
        let config_path = tmp.path().join(".panini/config.yaml");
        let config_content = fs::read_to_string(config_path).unwrap();
        
        // Parse YAML to ensure it's valid
        let _config: serde_yaml::Value = serde_yaml::from_str(&config_content).unwrap();
    }
}
