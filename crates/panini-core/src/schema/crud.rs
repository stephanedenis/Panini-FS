//! Concept CRUD operations (Create, Read, Update, Delete)

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::schema::concept::{parse_concept_markdown, serialize_concept_markdown, validate_concept, Concept};
use std::fs;
use std::path::{Path, PathBuf};

/// Create a new concept
pub fn create_concept(repo: &PaniniRepo, concept: &Concept) -> Result<PathBuf> {
    // Validate concept
    validate_concept(concept)?;
    
    // Generate file path
    let file_path = concept_path(repo.path(), &concept.id);
    
    // Check if already exists
    if file_path.exists() {
        return Err(Error::Validation(format!(
            "Concept already exists: {}",
            concept.id
        )));
    }
    
    // Ensure directory exists
    if let Some(parent) = file_path.parent() {
        fs::create_dir_all(parent)?;
    }
    
    // Serialize and write
    let markdown = serialize_concept_markdown(concept)?;
    fs::write(&file_path, markdown)?;
    
    // Commit
    let message = format!("feat(concept): Create {}", concept.title);
    repo.commit_file(&file_path, &message)?;
    
    Ok(file_path)
}

/// Read a concept by ID
pub fn read_concept(repo: &PaniniRepo, id: &str) -> Result<Concept> {
    let file_path = concept_path(repo.path(), id);
    
    if !file_path.exists() {
        return Err(Error::NotFound(format!("Concept not found: {}", id)));
    }
    
    let content = fs::read_to_string(&file_path)?;
    parse_concept_markdown(&content)
}

/// Update an existing concept
pub fn update_concept(repo: &PaniniRepo, concept: &Concept) -> Result<PathBuf> {
    // Validate concept
    validate_concept(concept)?;
    
    // Generate file path
    let file_path = concept_path(repo.path(), &concept.id);
    
    // Check if exists
    if !file_path.exists() {
        return Err(Error::NotFound(format!(
            "Concept not found: {}",
            concept.id
        )));
    }
    
    // Serialize and write
    let markdown = serialize_concept_markdown(concept)?;
    fs::write(&file_path, markdown)?;
    
    // Commit
    let message = format!("feat(concept): Update {}", concept.title);
    repo.commit_file(&file_path, &message)?;
    
    Ok(file_path)
}

/// Delete a concept by ID
pub fn delete_concept(repo: &PaniniRepo, id: &str) -> Result<PathBuf> {
    let file_path = concept_path(repo.path(), id);
    
    // Check if exists
    if !file_path.exists() {
        return Err(Error::NotFound(format!("Concept not found: {}", id)));
    }
    
    // Read concept for commit message
    let concept = read_concept(repo, id)?;
    
    // Delete file
    fs::remove_file(&file_path)?;
    
    // Stage deletion
    repo.stage_all()?;
    
    // Commit
    let message = format!("feat(concept): Delete {}", concept.title);
    repo.commit_file(&file_path, &message)?;
    
    Ok(file_path)
}

/// List all concepts
pub fn list_concepts(repo: &PaniniRepo) -> Result<Vec<String>> {
    let knowledge_dir = repo.path().join("knowledge");
    
    if !knowledge_dir.exists() {
        return Ok(Vec::new());
    }
    
    let mut concept_ids = Vec::new();
    
    // Walk directory
    for entry in walkdir::WalkDir::new(&knowledge_dir)
        .follow_links(false)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        
        // Check if Markdown file
        if path.is_file() && path.extension().and_then(|s| s.to_str()) == Some("md") {
            // Extract concept ID from filename
            if let Some(stem) = path.file_stem().and_then(|s| s.to_str()) {
                concept_ids.push(stem.to_string());
            }
        }
    }
    
    Ok(concept_ids)
}

/// Check if concept exists
pub fn exists_concept(repo: &PaniniRepo, id: &str) -> bool {
    concept_path(repo.path(), id).exists()
}

/// Get concept file path
fn concept_path(repo_path: &Path, id: &str) -> PathBuf {
    repo_path.join("knowledge").join(format!("{}.md", id))
}

/// Rename/move a concept
pub fn rename_concept(repo: &PaniniRepo, old_id: &str, new_id: &str) -> Result<PathBuf> {
    let old_path = concept_path(repo.path(), old_id);
    let new_path = concept_path(repo.path(), new_id);
    
    // Check old exists
    if !old_path.exists() {
        return Err(Error::NotFound(format!("Concept not found: {}", old_id)));
    }
    
    // Check new doesn't exist
    if new_path.exists() {
        return Err(Error::Validation(format!(
            "Target concept already exists: {}",
            new_id
        )));
    }
    
    // Read concept
    let mut concept = read_concept(repo, old_id)?;
    
    // Update ID
    concept.id = new_id.to_string();
    
    // Delete old
    fs::remove_file(&old_path)?;
    
    // Create new
    let markdown = serialize_concept_markdown(&concept)?;
    fs::write(&new_path, markdown)?;
    
    // Stage changes
    repo.stage_all()?;
    
    // Commit
    let message = format!("refactor(concept): Rename {} to {}", old_id, new_id);
    repo.commit_batch(&[&old_path, &new_path], &message)?;
    
    Ok(new_path)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::Concept;
    use crate::schema::dhatu::Dhatu;
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(id: &str) -> Concept {
        Concept {
            id: id.to_string(),
            r#type: crate::schema::concept::ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: format!("Test Concept {}", id),
            tags: vec!["test".to_string()],
            created: Utc::now(),
            updated: Utc::now(),
            author: Some("tester".to_string()),
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: format!("# Test Concept {}\n\nBody", id),
        }
    }
    
    #[test]
    fn test_create_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let concept = create_test_concept("test-1");
        let path = create_concept(&repo, &concept).unwrap();
        
        assert!(path.exists());
        assert!(path.to_str().unwrap().contains("test-1.md"));
    }
    
    #[test]
    fn test_read_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let concept = create_test_concept("test-2");
        create_concept(&repo, &concept).unwrap();
        
        let read = read_concept(&repo, "test-2").unwrap();
        
        assert_eq!(read.id, "test-2");
        assert_eq!(read.title, "Test Concept test-2");
    }
    
    #[test]
    fn test_update_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let mut concept = create_test_concept("test-3");
        create_concept(&repo, &concept).unwrap();
        
        // Update
        concept.title = "Updated Title".to_string();
        update_concept(&repo, &concept).unwrap();
        
        // Read back
        let read = read_concept(&repo, "test-3").unwrap();
        assert_eq!(read.title, "Updated Title");
    }
    
    #[test]
    fn test_delete_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let concept = create_test_concept("test-4");
        let path = create_concept(&repo, &concept).unwrap();
        
        assert!(path.exists());
        
        delete_concept(&repo, "test-4").unwrap();
        
        assert!(!path.exists());
    }
    
    #[test]
    fn test_list_concepts() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_concept(&repo, &create_test_concept("list-1")).unwrap();
        create_concept(&repo, &create_test_concept("list-2")).unwrap();
        create_concept(&repo, &create_test_concept("list-3")).unwrap();
        
        let list = list_concepts(&repo).unwrap();
        
        assert_eq!(list.len(), 3);
        assert!(list.contains(&"list-1".to_string()));
    }
    
    #[test]
    fn test_exists_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        assert!(!exists_concept(&repo, "nonexistent"));
        
        create_concept(&repo, &create_test_concept("exists")).unwrap();
        
        assert!(exists_concept(&repo, "exists"));
    }
    
    #[test]
    fn test_rename_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_concept(&repo, &create_test_concept("old-id")).unwrap();
        
        rename_concept(&repo, "old-id", "new-id").unwrap();
        
        assert!(!exists_concept(&repo, "old-id"));
        assert!(exists_concept(&repo, "new-id"));
        
        let concept = read_concept(&repo, "new-id").unwrap();
        assert_eq!(concept.id, "new-id");
    }
}
