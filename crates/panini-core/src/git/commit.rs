//! Git commit operations

use crate::error::{Error, Result};
use git2::{IndexAddOption, Repository, Signature};
use std::path::Path;

/// Commit a single file
pub fn commit_file(
    repo: &Repository,
    file_path: &Path,
    message: &str,
) -> Result<git2::Oid> {
    // Get relative path from repo root
    let repo_root = repo.workdir().ok_or_else(|| {
        Error::Git(git2::Error::from_str("Repository has no working directory"))
    })?;
    
    let rel_path = file_path.strip_prefix(repo_root).map_err(|_| {
        Error::Validation(format!(
            "File {:?} is not inside repository {:?}",
            file_path, repo_root
        ))
    })?;
    
    // Add file to index
    let mut index = repo.index()?;
    index.add_path(rel_path)?;
    index.write()?;
    
    // Create commit
    create_commit(repo, message)
}

/// Commit multiple files in batch
pub fn commit_batch(
    repo: &Repository,
    file_paths: &[&Path],
    message: &str,
) -> Result<git2::Oid> {
    let repo_root = repo.workdir().ok_or_else(|| {
        Error::Git(git2::Error::from_str("Repository has no working directory"))
    })?;
    
    let mut index = repo.index()?;
    
    // Add all files to index
    for file_path in file_paths {
        let rel_path = file_path.strip_prefix(repo_root).map_err(|_| {
            Error::Validation(format!(
                "File {:?} is not inside repository {:?}",
                file_path, repo_root
            ))
        })?;
        
        index.add_path(rel_path)?;
    }
    
    index.write()?;
    
    // Create commit
    create_commit(repo, message)
}

/// Stage all changes
pub fn stage_all(repo: &Repository) -> Result<()> {
    let mut index = repo.index()?;
    index.add_all(["*"].iter(), IndexAddOption::DEFAULT, None)?;
    index.write()?;
    Ok(())
}

/// Create commit with current index
pub fn create_commit(repo: &Repository, message: &str) -> Result<git2::Oid> {
    let mut index = repo.index()?;
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;
    
    // Get HEAD commit (if exists)
    let parent_commit = match repo.head() {
        Ok(head) => {
            let commit = head.peel_to_commit()?;
            Some(commit)
        }
        Err(_) => None, // First commit
    };
    
    // Create signature
    let sig = create_signature(repo)?;
    
    // Create commit
    let parents: Vec<&git2::Commit> = parent_commit.as_ref().map(|c| vec![c]).unwrap_or_default();
    
    let oid = repo.commit(
        Some("HEAD"),
        &sig,
        &sig,
        message,
        &tree,
        &parents,
    )?;
    
    Ok(oid)
}

/// Create Git signature from repo config or defaults
fn create_signature(repo: &Repository) -> Result<Signature<'static>> {
    // Try to get from Git config
    let config = repo.config()?;
    
    let name = config
        .get_string("user.name")
        .unwrap_or_else(|_| "Panini User".to_string());
    
    let email = config
        .get_string("user.email")
        .unwrap_or_else(|_| "panini@localhost".to_string());
    
    Ok(Signature::now(&name, &email)?)
}

/// Format commit message with Conventional Commits style
pub fn format_message(type_: &str, scope: Option<&str>, description: &str) -> String {
    match scope {
        Some(s) => format!("{type_}({s}): {description}"),
        None => format!("{type_}: {description}"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use std::fs;
    use tempfile::TempDir;
    
    #[test]
    fn test_commit_single_file() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        // Create a new file
        let file_path = tmp.path().join("knowledge/test.md");
        fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
        fs::write(&file_path, "# Test Concept\n\nContent").unwrap();
        
        // Commit the file
        let oid = commit_file(&repo, &file_path, "feat: Add test concept").unwrap();
        assert!(!oid.is_zero());
        
        // Verify commit exists
        let commit = repo.find_commit(oid).unwrap();
        assert!(commit.message().unwrap().contains("Add test concept"));
    }
    
    #[test]
    fn test_commit_batch() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        // Create multiple files
        fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
        let file1 = tmp.path().join("knowledge/concept1.md");
        let file2 = tmp.path().join("knowledge/concept2.md");
        
        fs::write(&file1, "# Concept 1").unwrap();
        fs::write(&file2, "# Concept 2").unwrap();
        
        // Commit batch
        let files: Vec<&Path> = vec![&file1, &file2];
        let oid = commit_batch(&repo, &files, "feat: Add two concepts").unwrap();
        
        assert!(!oid.is_zero());
        
        // Verify commit
        let commit = repo.find_commit(oid).unwrap();
        assert!(commit.message().unwrap().contains("two concepts"));
    }
    
    #[test]
    fn test_stage_all() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        // Create files
        fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
        fs::write(tmp.path().join("knowledge/test.md"), "Test").unwrap();
        
        // Stage all
        stage_all(&repo).unwrap();
        
        // Verify staged
        let statuses = repo.statuses(None).unwrap();
        assert!(statuses.iter().any(|s| s.status().is_index_new()));
    }
    
    #[test]
    fn test_format_message() {
        assert_eq!(
            format_message("feat", Some("schema"), "Add new dhatu type"),
            "feat(schema): Add new dhatu type"
        );
        
        assert_eq!(
            format_message("fix", None, "Resolve conflict"),
            "fix: Resolve conflict"
        );
    }
    
    #[test]
    fn test_commit_file_outside_repo() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        // Try to commit file outside repo
        let outside_file = Path::new("/tmp/outside.md");
        let result = commit_file(&repo, outside_file, "test");
        
        assert!(result.is_err());
    }
}
