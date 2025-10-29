//! Conflict detection and resolution

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::schema::concept::Concept;
use crate::schema::crud::{read_concept, update_concept};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Conflict resolver
pub struct ConflictResolver {
    repo: PaniniRepo,
}

impl ConflictResolver {
    /// Create new conflict resolver
    pub fn new(repo: PaniniRepo) -> Self {
        Self { repo }
    }
    
    /// Auto-resolve all conflicts
    pub fn auto_resolve_all(&self) -> Result<usize> {
        let conflicts = self.repo.get_conflicts()?;
        let mut resolved = 0;
        
        for conflict in conflicts {
            match self.auto_resolve_conflict(&conflict.path) {
                Ok(true) => resolved += 1,
                Ok(false) => {
                    // Could not auto-resolve, skip
                }
                Err(e) => {
                    eprintln!("Failed to resolve {}: {}", conflict.path, e);
                }
            }
        }
        
        Ok(resolved)
    }
    
    /// Auto-resolve a single conflict
    fn auto_resolve_conflict(&self, path: &str) -> Result<bool> {
        // Check if this is a concept file
        if !path.starts_with("knowledge/") || !path.ends_with(".md") {
            return Ok(false);
        }
        
        // Try YAML merge strategy
        self.resolve_yaml_conflict(path)
    }
    
    /// Resolve YAML frontmatter conflict
    fn resolve_yaml_conflict(&self, path: &str) -> Result<bool> {
        // Read both versions
        let ours = self.read_file_version(path, "HEAD")?;
        let theirs = self.read_file_version(path, "MERGE_HEAD")?;
        let base = self.read_file_version(path, "ORIG_HEAD").ok();
        
        // Parse concepts
        let ours_concept = Concept::from_markdown(&ours)?;
        let theirs_concept = Concept::from_markdown(&theirs)?;
        let base_concept = base.and_then(|b| Concept::from_markdown(&b).ok());
        
        // Merge concepts
        let merged = self.merge_concepts(ours_concept, theirs_concept, base_concept)?;
        
        // Write merged version
        let merged_md = merged.to_markdown()?;
        std::fs::write(self.repo.get_path().join(path), merged_md)
            .map_err(|e| Error::IoError(e.to_string()))?;
        
        // Mark as resolved
        self.repo.resolve_conflict(path)?;
        
        Ok(true)
    }
    
    /// Merge two concepts (3-way merge if base available)
    fn merge_concepts(
        &self,
        ours: Concept,
        theirs: Concept,
        base: Option<Concept>,
    ) -> Result<Concept> {
        let mut merged = ours.clone();
        
        // Merge strategy based on timestamps
        if theirs.updated > ours.updated {
            // Their version is newer
            merged.title = theirs.title.clone();
            merged.updated = theirs.updated;
        }
        
        // Merge tags (union)
        let mut tags_set: std::collections::HashSet<_> = ours.tags.iter().cloned().collect();
        tags_set.extend(theirs.tags.iter().cloned());
        merged.tags = tags_set.into_iter().collect();
        merged.tags.sort();
        
        // Merge relations (union, prefer higher confidence)
        let mut relation_map: HashMap<(String, String), _> = HashMap::new();
        
        for rel in &ours.relations {
            let key = (rel.rel_type.to_string(), rel.target.clone());
            relation_map.insert(key, rel.clone());
        }
        
        for rel in &theirs.relations {
            let key = (rel.rel_type.to_string(), rel.target.clone());
            
            relation_map
                .entry(key)
                .and_modify(|existing| {
                    // Keep higher confidence
                    if let (Some(new_conf), Some(existing_conf)) = (rel.confidence, existing.confidence) {
                        if new_conf > existing_conf {
                            *existing = rel.clone();
                        }
                    }
                })
                .or_insert_with(|| rel.clone());
        }
        
        merged.relations = relation_map.into_values().collect();
        
        // Merge content_refs (union)
        let mut refs_set: std::collections::HashSet<_> = ours.content_refs.iter().cloned().collect();
        refs_set.extend(theirs.content_refs.iter().cloned());
        merged.content_refs = refs_set.into_iter().collect();
        
        // Merge markdown body (prefer newer)
        if theirs.updated > ours.updated {
            merged.markdown_body = theirs.markdown_body;
        }
        
        Ok(merged)
    }
    
    /// Read file version from Git
    fn read_file_version(&self, path: &str, ref_name: &str) -> Result<String> {
        // This is a simplified implementation
        // In production, use git2-rs to read from Git objects
        
        let repo_git = git2::Repository::open(self.repo.get_path())
            .map_err(|e| Error::GitError(e.to_string()))?;
        
        let reference = repo_git.find_reference(ref_name)
            .map_err(|e| Error::GitError(format!("Reference {} not found: {}", ref_name, e)))?;
        
        let commit = reference.peel_to_commit()
            .map_err(|e| Error::GitError(e.to_string()))?;
        
        let tree = commit.tree()
            .map_err(|e| Error::GitError(e.to_string()))?;
        
        let entry = tree.get_path(std::path::Path::new(path))
            .map_err(|e| Error::GitError(format!("Path {} not found: {}", path, e)))?;
        
        let object = entry.to_object(&repo_git)
            .map_err(|e| Error::GitError(e.to_string()))?;
        
        let blob = object.as_blob()
            .ok_or_else(|| Error::GitError("Not a blob".to_string()))?;
        
        let content = std::str::from_utf8(blob.content())
            .map_err(|e| Error::GitError(format!("Invalid UTF-8: {}", e)))?;
        
        Ok(content.to_string())
    }
    
    /// Get conflict statistics
    pub fn conflict_stats(&self) -> Result<ConflictStats> {
        let conflicts = self.repo.get_conflicts()?;
        
        let mut yaml_conflicts = 0;
        let mut content_conflicts = 0;
        let mut other_conflicts = 0;
        
        for conflict in &conflicts {
            if conflict.path.starts_with("knowledge/") && conflict.path.ends_with(".md") {
                yaml_conflicts += 1;
            } else if conflict.path.starts_with("content/") {
                content_conflicts += 1;
            } else {
                other_conflicts += 1;
            }
        }
        
        Ok(ConflictStats {
            total: conflicts.len(),
            yaml_conflicts,
            content_conflicts,
            other_conflicts,
        })
    }
}

/// Conflict statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConflictStats {
    pub total: usize,
    pub yaml_conflicts: usize,
    pub content_conflicts: usize,
    pub other_conflicts: usize,
}

impl ConflictStats {
    pub fn auto_resolvable(&self) -> usize {
        self.yaml_conflicts // YAML conflicts are auto-resolvable
    }
    
    pub fn manual_required(&self) -> usize {
        self.content_conflicts + self.other_conflicts
    }
    
    pub fn auto_resolve_rate(&self) -> f64 {
        if self.total == 0 {
            return 100.0;
        }
        
        (self.auto_resolvable() as f64 / self.total as f64) * 100.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::dhatu::Dhatu;
    use crate::schema::relation::{Relation, RelationType};
    use chrono::Utc;
    use tempfile::TempDir;
    
    #[test]
    fn test_conflict_resolver_creation() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        let resolver = ConflictResolver::new(repo);
        
        let stats = resolver.conflict_stats().unwrap();
        assert_eq!(stats.total, 0);
    }
    
    #[test]
    fn test_merge_concepts_simple() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        let resolver = ConflictResolver::new(repo);
        
        let ours = Concept {
            id: "test".to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: "Original Title".to_string(),
            tags: vec!["tag1".to_string()],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: "Original body".to_string(),
        };
        
        let mut theirs = ours.clone();
        theirs.title = "Updated Title".to_string();
        theirs.updated = Utc::now() + chrono::Duration::seconds(60);
        theirs.tags = vec!["tag2".to_string()];
        
        let merged = resolver.merge_concepts(ours, theirs, None).unwrap();
        
        assert_eq!(merged.title, "Updated Title"); // Newer version
        assert_eq!(merged.tags.len(), 2); // Union of tags
        assert!(merged.tags.contains(&"tag1".to_string()));
        assert!(merged.tags.contains(&"tag2".to_string()));
    }
    
    #[test]
    fn test_merge_relations() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        let resolver = ConflictResolver::new(repo);
        
        let mut ours = Concept {
            id: "test".to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: "Test".to_string(),
            tags: vec![],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![Relation {
                rel_type: RelationType::IsA,
                target: "target1".to_string(),
                confidence: Some(0.8),
            }],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: "Body".to_string(),
        };
        
        let mut theirs = ours.clone();
        theirs.relations = vec![
            Relation {
                rel_type: RelationType::IsA,
                target: "target1".to_string(),
                confidence: Some(0.9), // Higher confidence
            },
            Relation {
                rel_type: RelationType::PartOf,
                target: "target2".to_string(),
                confidence: Some(0.7),
            },
        ];
        
        let merged = resolver.merge_concepts(ours, theirs, None).unwrap();
        
        assert_eq!(merged.relations.len(), 2);
        
        // Should keep higher confidence
        let is_a_rel = merged
            .relations
            .iter()
            .find(|r| r.rel_type == RelationType::IsA)
            .unwrap();
        assert_eq!(is_a_rel.confidence, Some(0.9));
    }
    
    #[test]
    fn test_conflict_stats() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        let resolver = ConflictResolver::new(repo);
        
        let stats = resolver.conflict_stats().unwrap();
        
        assert_eq!(stats.total, 0);
        assert_eq!(stats.auto_resolve_rate(), 100.0);
    }
}
