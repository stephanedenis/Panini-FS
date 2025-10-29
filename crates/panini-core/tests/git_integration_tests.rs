//! Integration tests for Git operations
//!
//! These tests validate complete workflows across multiple modules.

use panini_core::git::conflict::ConflictResolution;
use panini_core::git::sync::ConflictStrategy;
use panini_core::PaniniRepo;
use std::fs;
use tempfile::TempDir;

#[test]
fn test_complete_workflow_init_commit_status() {
    // Setup
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Verify initial state
    assert!(repo.is_clean().unwrap());
    let history = repo.history(None).unwrap();
    assert_eq!(history.len(), 1); // Initial commit
    
    // Create a concept
    fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
    let concept_path = tmp.path().join("knowledge/rust.md");
    fs::write(&concept_path, "# Rust\n\nA systems programming language.").unwrap();
    
    // Check status
    let status = repo.status().unwrap();
    assert!(!status.untracked.is_empty());
    assert!(!repo.is_clean().unwrap());
    
    // Commit
    let oid = repo.commit_file(&concept_path, "feat(knowledge): Add Rust concept").unwrap();
    assert!(!oid.is_zero());
    
    // Verify clean state
    assert!(repo.is_clean().unwrap());
    
    // Check history
    let history = repo.history(None).unwrap();
    assert_eq!(history.len(), 2);
    assert!(history[0].message.contains("Rust concept"));
}

#[test]
fn test_complete_workflow_clone_open() {
    // Create source repository
    let src_tmp = TempDir::new().unwrap();
    let src_repo = PaniniRepo::init(src_tmp.path()).unwrap();
    
    // Add a concept
    fs::create_dir_all(src_tmp.path().join("knowledge")).unwrap();
    let concept_path = src_tmp.path().join("knowledge/test.md");
    fs::write(&concept_path, "# Test").unwrap();
    src_repo.commit_file(&concept_path, "feat: Add test concept").unwrap();
    
    // Clone
    let dst_tmp = TempDir::new().unwrap();
    let dst_path = dst_tmp.path().join("cloned");
    
    let url = format!("file://{}", src_tmp.path().display());
    let cloned_repo = PaniniRepo::clone(
        &url,
        &dst_path,
        panini_core::git::clone::CloneOptions::default(),
    ).unwrap();
    
    // Verify cloned repo
    assert!(cloned_repo.path().exists());
    assert!(dst_path.join(".panini").exists());
    assert!(dst_path.join("knowledge/test.md").exists());
    
    // Re-open cloned repo
    let reopened = PaniniRepo::open(&dst_path).unwrap();
    assert_eq!(reopened.config().version, "1.0");
    assert_eq!(reopened.schema().version, "1.0.0");
}

#[test]
fn test_complete_workflow_multi_file_commit() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create multiple concepts
    fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
    
    let file1 = tmp.path().join("knowledge/concept1.md");
    let file2 = tmp.path().join("knowledge/concept2.md");
    let file3 = tmp.path().join("knowledge/concept3.md");
    
    fs::write(&file1, "# Concept 1").unwrap();
    fs::write(&file2, "# Concept 2").unwrap();
    fs::write(&file3, "# Concept 3").unwrap();
    
    // Batch commit
    let files: Vec<&std::path::Path> = vec![&file1, &file2, &file3];
    let oid = repo.commit_batch(&files, "feat: Add three concepts").unwrap();
    
    assert!(!oid.is_zero());
    assert!(repo.is_clean().unwrap());
    
    // Verify all files in history
    let file1_history = repo.file_history("knowledge/concept1.md", None).unwrap();
    let file2_history = repo.file_history("knowledge/concept2.md", None).unwrap();
    let file3_history = repo.file_history("knowledge/concept3.md", None).unwrap();
    
    assert_eq!(file1_history.len(), 1);
    assert_eq!(file2_history.len(), 1);
    assert_eq!(file3_history.len(), 1);
}

#[test]
fn test_complete_workflow_status_and_diff() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create and commit initial file
    fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
    let file_path = tmp.path().join("knowledge/evolving.md");
    fs::write(&file_path, "# Version 1").unwrap();
    repo.commit_file(&file_path, "feat: Initial version").unwrap();
    
    // Modify file
    fs::write(&file_path, "# Version 1\n\nUpdated content").unwrap();
    
    // Check status
    let status = repo.status().unwrap();
    assert!(!status.unstaged.is_empty());
    
    // Get diff stats
    let diff = repo.diff_stats().unwrap();
    assert!(diff.files_changed > 0);
    
    // Commit changes
    repo.commit_file(&file_path, "feat: Update content").unwrap();
    
    // Verify history
    let history = repo.file_history("knowledge/evolving.md", None).unwrap();
    assert_eq!(history.len(), 2);
}

#[test]
fn test_complete_workflow_graph_stats() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create multiple commits
    for i in 1..=5 {
        fs::create_dir_all(tmp.path().join("knowledge")).unwrap();
        let file_path = tmp.path().join(format!("knowledge/concept{}.md", i));
        fs::write(&file_path, format!("# Concept {}", i)).unwrap();
        repo.commit_file(&file_path, &format!("feat: Add concept {}", i)).unwrap();
    }
    
    // Get stats
    let stats = repo.graph_stats().unwrap();
    
    assert_eq!(stats.total_commits, 6); // 5 + initial
    assert_eq!(stats.merge_commits, 0);
    assert_eq!(stats.unique_authors, 1);
}

#[test]
fn test_error_handling_open_nonexistent() {
    let tmp = TempDir::new().unwrap();
    let result = PaniniRepo::open(tmp.path());
    
    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("not initialized"));
}

#[test]
fn test_error_handling_init_twice() {
    let tmp = TempDir::new().unwrap();
    PaniniRepo::init(tmp.path()).unwrap();
    
    let result = PaniniRepo::init(tmp.path());
    
    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("already exists"));
}

#[test]
fn test_error_handling_commit_outside_repo() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    let outside_file = std::path::Path::new("/tmp/outside.md");
    let result = repo.commit_file(outside_file, "test");
    
    assert!(result.is_err());
}

#[test]
fn test_config_and_schema_validation() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Verify config
    let config = repo.config();
    assert_eq!(config.version, "1.0");
    assert_eq!(config.storage.default, "local");
    assert_eq!(config.sync.conflict_strategy, "prompt");
    
    // Verify schema
    let schema = repo.schema();
    assert_eq!(schema.version, "1.0.0");
    assert_eq!(schema.relation_types.len(), 8);
    assert_eq!(schema.dhatu_types.len(), 7);
    
    assert!(schema.relation_types.contains(&"is_a".to_string()));
    assert!(schema.dhatu_types.contains(&"TEXT".to_string()));
}
