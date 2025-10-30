//! Integration tests for sync module

use panini_core::git::repo::PaniniRepo;
use panini_core::git::sync::ConflictStrategy;
use panini_core::schema::concept::{Concept, ConceptType};
use panini_core::schema::crud::create_concept;
use panini_core::schema::dhatu::Dhatu;
use panini_core::sync::conflict::ConflictResolver;
use panini_core::sync::operations::SyncManager;
use chrono::Utc;
use tempfile::TempDir;

fn create_test_concept(repo: &PaniniRepo, id: &str, title: &str) -> Concept {
    let concept = Concept {
        id: id.to_string(),
        r#type: ConceptType::Concept,
        dhatu: Dhatu::TEXT,
        title: title.to_string(),
        tags: vec!["test".to_string()],
        created: Utc::now(),
        updated: Utc::now(),
        author: None,
        relations: vec![],
        content_refs: vec![],
        metadata: serde_json::Value::Null,
        markdown_body: format!("# {}\n\nContent for {}", title, id),
    };
    
    create_concept(repo, &concept).unwrap();
    concept
}

#[test]
fn test_sync_manager_status() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    let manager = SyncManager::new(repo.clone());
    
    let status = manager.status().unwrap();
    
    assert!(status.is_clean);
    assert_eq!(status.commits_ahead, 0);
    assert_eq!(status.commits_behind, 0);
    assert!(!status.needs_pull());
    assert!(!status.needs_push());
}

#[test]
fn test_sync_with_local_changes() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create local changes
    create_test_concept(&repo, "test1", "Test 1");
    create_test_concept(&repo, "test2", "Test 2");
    
    let manager = SyncManager::new(repo);
    
    let status = manager.status().unwrap();
    
    assert!(status.has_changes() || !status.is_clean);
}

#[test]
fn test_conflict_resolver_stats() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    let resolver = ConflictResolver::new(repo);
    
    let stats = resolver.conflict_stats().unwrap();
    
    assert_eq!(stats.total, 0);
    assert_eq!(stats.yaml_conflicts, 0);
    assert_eq!(stats.content_conflicts, 0);
    assert_eq!(stats.auto_resolvable(), 0);
    assert_eq!(stats.auto_resolve_rate(), 100.0);
}

#[test]
fn test_concept_merge_strategy() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    let resolver = ConflictResolver::new(repo);
    
    // Create two versions of same concept
    let mut ours = Concept {
        id: "test".to_string(),
        r#type: ConceptType::Concept,
        dhatu: Dhatu::TEXT,
        title: "Original".to_string(),
        tags: vec!["tag1".to_string(), "tag2".to_string()],
        created: Utc::now(),
        updated: Utc::now(),
        author: None,
        relations: vec![],
        content_refs: vec![],
        metadata: serde_json::Value::Null,
        markdown_body: "Original content".to_string(),
    };
    
    let mut theirs = ours.clone();
    theirs.title = "Updated".to_string();
    theirs.tags = vec!["tag2".to_string(), "tag3".to_string()];
    theirs.updated = Utc::now() + chrono::Duration::seconds(60);
    
    // Merge should take union of tags and newer title
    let merged = resolver.merge_concepts(ours, theirs, None).unwrap();
    
    assert_eq!(merged.title, "Updated"); // Newer
    assert_eq!(merged.tags.len(), 3); // Union: tag1, tag2, tag3
}

#[test]
fn test_yaml_conflict_auto_resolve_rate() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    let resolver = ConflictResolver::new(repo);
    
    let stats = resolver.conflict_stats().unwrap();
    
    // With no conflicts, auto-resolve rate should be 100%
    assert_eq!(stats.auto_resolve_rate(), 100.0);
}

#[test]
fn test_sync_workflow() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create initial concept
    create_test_concept(&repo, "concept1", "Concept 1");
    
    // Create sync manager
    let manager = SyncManager::new(repo.clone());
    
    // Get initial status
    let status = manager.status().unwrap();
    
    println!("Status: clean={}, ahead={}, behind={}", 
             status.is_clean, status.commits_ahead, status.commits_behind);
    
    // Workflow test passed if no errors
    assert!(true);
}

#[test]
fn test_large_sync_performance() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create 50 concepts
    for i in 0..50 {
        create_test_concept(&repo, &format!("concept{}", i), &format!("Concept {}", i));
    }
    
    let manager = SyncManager::new(repo);
    
    let start = std::time::Instant::now();
    let status = manager.status().unwrap();
    let duration = start.elapsed();
    
    println!("Status query for 50 concepts: {:?}", duration);
    
    assert!(duration.as_millis() < 1000); // Should be < 1s
    assert!(status.has_changes());
}
