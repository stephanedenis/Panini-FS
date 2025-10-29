//! Index builder - builds index from Git repository

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::index::rocks::RocksIndex;
use crate::schema::crud::{list_concepts, read_concept};
use std::path::Path;

/// Index builder
pub struct IndexBuilder {
    repo: PaniniRepo,
    index: RocksIndex,
}

impl IndexBuilder {
    /// Create new index builder
    pub fn new(repo: PaniniRepo, index_path: &Path) -> Result<Self> {
        let index = RocksIndex::open(index_path)?;
        Ok(Self { repo, index })
    }
    
    /// Build full index from repository
    pub fn build(&self) -> Result<BuildStats> {
        let start = std::time::Instant::now();
        
        let concept_ids = list_concepts(&self.repo)?;
        let mut concepts_indexed = 0;
        let mut relations_indexed = 0;
        let mut errors = Vec::new();
        
        for id in &concept_ids {
            match self.index_concept(id) {
                Ok((_, rel_count)) => {
                    concepts_indexed += 1;
                    relations_indexed += rel_count;
                }
                Err(e) => {
                    errors.push(format!("Failed to index {}: {}", id, e));
                }
            }
        }
        
        self.index.flush()?;
        
        let duration = start.elapsed();
        
        Ok(BuildStats {
            concepts_indexed,
            relations_indexed,
            errors,
            duration_ms: duration.as_millis() as u64,
        })
    }
    
    /// Index a single concept
    fn index_concept(&self, id: &str) -> Result<((), usize)> {
        let concept = read_concept(&self.repo, id)?;
        
        // Index concept
        self.index.put_concept(&concept)?;
        
        // Index relations
        let relation_count = concept.relations.len();
        for relation in &concept.relations {
            self.index.put_relation(id, relation)?;
        }
        
        Ok(((), relation_count))
    }
    
    /// Update index for a single concept
    pub fn update_concept(&self, id: &str) -> Result<()> {
        // Delete old relations
        self.index.delete_relations(id)?;
        
        // Re-index concept
        self.index_concept(id)?;
        
        self.index.flush()?;
        
        Ok(())
    }
    
    /// Remove concept from index
    pub fn remove_concept(&self, id: &str) -> Result<()> {
        self.index.delete_concept(id)?;
        self.index.delete_relations(id)?;
        self.index.flush()?;
        Ok(())
    }
    
    /// Rebuild index from scratch
    pub fn rebuild(&self) -> Result<BuildStats> {
        // Clear existing index would require dropping and recreating DB
        // For now, just overwrite existing entries
        self.build()
    }
    
    /// Get index reference
    pub fn index(&self) -> &RocksIndex {
        &self.index
    }
}

/// Build statistics
#[derive(Debug, Clone)]
pub struct BuildStats {
    pub concepts_indexed: usize,
    pub relations_indexed: usize,
    pub errors: Vec<String>,
    pub duration_ms: u64,
}

impl BuildStats {
    /// Check if build was successful
    pub fn is_success(&self) -> bool {
        self.errors.is_empty()
    }
    
    /// Get indexing rate (concepts per second)
    pub fn rate(&self) -> f64 {
        if self.duration_ms == 0 {
            return 0.0;
        }
        (self.concepts_indexed as f64 / self.duration_ms as f64) * 1000.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::crud::create_concept;
    use crate::schema::dhatu::Dhatu;
    use crate::schema::relation::{Relation, RelationType};
    use crate::schema::relations::add_relation;
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(repo: &PaniniRepo, id: &str) -> Concept {
        let concept = Concept {
            id: id.to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: format!("Test {}", id),
            tags: vec!["test".to_string()],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: format!("# Test {}", id),
        };
        
        create_concept(repo, &concept).unwrap();
        concept
    }
    
    #[test]
    fn test_build_index() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        // Create test concepts
        for i in 0..5 {
            create_test_concept(&repo, &format!("test{}", i));
        }
        
        // Build index
        let builder = IndexBuilder::new(
            repo,
            &tmp.path().join("index"),
        ).unwrap();
        
        let stats = builder.build().unwrap();
        
        assert_eq!(stats.concepts_indexed, 5);
        assert!(stats.is_success());
        assert!(stats.rate() > 0.0);
    }
    
    #[test]
    fn test_index_with_relations() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "concept1");
        create_test_concept(&repo, "concept2");
        
        add_relation(&repo, "concept1", RelationType::IsA, "concept2", None).unwrap();
        
        let builder = IndexBuilder::new(
            repo,
            &tmp.path().join("index"),
        ).unwrap();
        
        let stats = builder.build().unwrap();
        
        assert_eq!(stats.concepts_indexed, 2);
        assert_eq!(stats.relations_indexed, 1);
        
        // Verify relation is indexed
        let relations = builder.index().get_relations("concept1").unwrap();
        assert_eq!(relations.len(), 1);
    }
    
    #[test]
    fn test_update_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "concept1");
        create_test_concept(&repo, "concept2");
        
        let builder = IndexBuilder::new(
            repo.clone(),
            &tmp.path().join("index"),
        ).unwrap();
        
        builder.build().unwrap();
        
        // Add relation
        add_relation(&repo, "concept1", RelationType::IsA, "concept2", None).unwrap();
        
        // Update index
        builder.update_concept("concept1").unwrap();
        
        // Verify
        let relations = builder.index().get_relations("concept1").unwrap();
        assert_eq!(relations.len(), 1);
    }
    
    #[test]
    fn test_remove_concept() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "concept1");
        
        let builder = IndexBuilder::new(
            repo,
            &tmp.path().join("index"),
        ).unwrap();
        
        builder.build().unwrap();
        
        // Remove from index
        builder.remove_concept("concept1").unwrap();
        
        // Verify
        let concept = builder.index().get_concept("concept1").unwrap();
        assert!(concept.is_none());
    }
    
    #[test]
    fn test_performance_large_build() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        // Create 100 concepts
        for i in 0..100 {
            create_test_concept(&repo, &format!("concept{}", i));
        }
        
        // Add relations
        for i in 0..99 {
            add_relation(
                &repo,
                &format!("concept{}", i),
                RelationType::Causes,
                &format!("concept{}", i + 1),
                None,
            )
            .unwrap();
        }
        
        let builder = IndexBuilder::new(
            repo,
            &tmp.path().join("index"),
        ).unwrap();
        
        let stats = builder.build().unwrap();
        
        assert_eq!(stats.concepts_indexed, 100);
        assert_eq!(stats.relations_indexed, 99);
        assert!(stats.is_success());
        
        println!("Build time: {}ms", stats.duration_ms);
        println!("Rate: {:.2} concepts/sec", stats.rate());
        
        assert!(stats.duration_ms < 5000); // Should complete in < 5s
    }
}
