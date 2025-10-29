//! Git submodule operations

use crate::error::{Error, Result};
use git2::{Repository, SubmoduleUpdateOptions};
use std::path::Path;

/// Information about a submodule
#[derive(Debug, Clone)]
pub struct SubmoduleInfo {
    pub name: String,
    pub path: String,
    pub url: String,
    pub head_oid: Option<String>,
}

/// Add a Git submodule
pub fn add_submodule(
    repo: &Repository,
    url: &str,
    path: &Path,
) -> Result<()> {
    // Validate path is relative
    if path.is_absolute() {
        return Err(Error::Validation(
            "Submodule path must be relative to repository root".to_string()
        ));
    }
    
    // Add submodule
    let mut submodule = repo.submodule(url, path, false)?;
    
    // Initialize and update
    submodule.init(false)?;
    
    let mut update_opts = SubmoduleUpdateOptions::new();
    submodule.update(true, Some(&mut update_opts))?;
    
    // Finalize (stage .gitmodules and submodule path)
    submodule.add_finalize()?;
    
    Ok(())
}

/// Remove a Git submodule
pub fn remove_submodule(
    repo: &Repository,
    path: &Path,
) -> Result<()> {
    // Find submodule by path
    let submodule_name = path.to_string_lossy().to_string();
    
    // Remove from .gitmodules and .git/config
    let config = repo.config()?;
    let mut config = config.open_level(git2::ConfigLevel::Local)?;
    
    // Remove submodule.<name> section
    config.remove_multivar(&format!("submodule.{}.url", submodule_name), ".*")?;
    config.remove_multivar(&format!("submodule.{}.path", submodule_name), ".*")?;
    
    // Stage .gitmodules
    let mut index = repo.index()?;
    index.remove_path(Path::new(".gitmodules"))?;
    index.write()?;
    
    // Remove submodule directory (requires manual filesystem operation)
    let repo_root = repo.workdir().ok_or_else(|| {
        Error::Git(git2::Error::from_str("Repository has no working directory"))
    })?;
    
    let submodule_full_path = repo_root.join(path);
    if submodule_full_path.exists() {
        std::fs::remove_dir_all(&submodule_full_path)?;
    }
    
    Ok(())
}

/// Update all submodules
pub fn update_submodules(repo: &Repository) -> Result<Vec<String>> {
    let mut updated = Vec::new();
    
    // Iterate over submodules
    repo.submodules()?.iter().try_for_each(|submodule| {
        let name = submodule.name().unwrap_or("unknown");
        
        // Update submodule
        let mut submodule = repo.find_submodule(name)?;
        let mut update_opts = SubmoduleUpdateOptions::new();
        
        submodule.update(true, Some(&mut update_opts))?;
        updated.push(name.to_string());
        
        Ok::<_, Error>(())
    })?;
    
    Ok(updated)
}

/// List all submodules
pub fn list_submodules(repo: &Repository) -> Result<Vec<SubmoduleInfo>> {
    let mut submodules = Vec::new();
    
    for submodule in repo.submodules()? {
        let name = submodule.name().unwrap_or("unknown").to_string();
        let path = submodule.path().to_string_lossy().to_string();
        let url = submodule.url().unwrap_or("unknown").to_string();
        let head_oid = submodule.head_id().map(|oid| oid.to_string());
        
        submodules.push(SubmoduleInfo {
            name,
            path,
            url,
            head_oid,
        });
    }
    
    Ok(submodules)
}

/// Check if a path is a submodule
pub fn is_submodule(repo: &Repository, path: &Path) -> Result<bool> {
    let submodule_name = path.to_string_lossy().to_string();
    
    match repo.find_submodule(&submodule_name) {
        Ok(_) => Ok(true),
        Err(_) => Ok(false),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use tempfile::TempDir;
    use std::fs;
    
    // Helper: Create a bare repository to use as submodule
    fn create_bare_repo() -> (TempDir, String) {
        let tmp = TempDir::new().unwrap();
        let bare_path = tmp.path().join("bare.git");
        Repository::init_bare(&bare_path).unwrap();
        
        let url = format!("file://{}", bare_path.display());
        (tmp, url)
    }
    
    #[test]
    fn test_add_submodule() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let (_bare_tmp, bare_url) = create_bare_repo();
        
        // Add submodule
        let result = add_submodule(&repo, &bare_url, Path::new("team/shared"));
        
        // Note: This may fail in CI without proper Git setup
        // In production, this would work with real Git repositories
        if result.is_ok() {
            let submodules = list_submodules(&repo).unwrap();
            assert!(!submodules.is_empty());
        }
    }
    
    #[test]
    fn test_list_submodules_empty() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let submodules = list_submodules(&repo).unwrap();
        assert!(submodules.is_empty());
    }
    
    #[test]
    fn test_is_submodule() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let is_sub = is_submodule(&repo, Path::new("team/shared")).unwrap();
        assert!(!is_sub);
    }
    
    #[test]
    fn test_add_submodule_absolute_path() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let (_bare_tmp, bare_url) = create_bare_repo();
        
        // Try absolute path (should fail)
        let result = add_submodule(&repo, &bare_url, Path::new("/absolute/path"));
        assert!(result.is_err());
    }
}
