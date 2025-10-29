//! Taxonomy system for concept classification

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::schema::crud::{list_concepts, read_concept};
use crate::schema::graph::KnowledgeGraph;
use crate::schema::relation::RelationType;
use std::collections::{HashMap, HashSet};

/// Taxonomy hierarchy
pub struct Taxonomy {
    /// Root concepts (no parent)
    pub roots: Vec<String>,
    /// Parent-child relationships
    pub hierarchy: HashMap<String, Vec<String>>,
    /// Child-parent relationships (inverse)
    pub parents: HashMap<String, Vec<String>>,
}

impl Taxonomy {
    /// Build taxonomy from is_a relations
    pub fn build(repo: &PaniniRepo) -> Result<Self> {
        let concept_ids = list_concepts(repo)?;
        
        let mut hierarchy: HashMap<String, Vec<String>> = HashMap::new();
        let mut parents: HashMap<String, Vec<String>> = HashMap::new();
        let mut all_children = HashSet::new();
        
        // Build hierarchy
        for id in &concept_ids {
            let concept = read_concept(repo, id)?;
            
            let is_a_relations: Vec<_> = concept
                .relations
                .iter()
                .filter(|r| r.rel_type == RelationType::IsA)
                .collect();
            
            if !is_a_relations.is_empty() {
                for relation in is_a_relations {
                    // id is_a target => target is parent of id
                    hierarchy
                        .entry(relation.target.clone())
                        .or_default()
                        .push(id.clone());
                    
                    parents
                        .entry(id.clone())
                        .or_default()
                        .push(relation.target.clone());
                    
                    all_children.insert(id.clone());
                }
            }
        }
        
        // Find roots (concepts with no parent)
        let roots: Vec<String> = concept_ids
            .into_iter()
            .filter(|id| !all_children.contains(id))
            .collect();
        
        Ok(Self {
            roots,
            hierarchy,
            parents,
        })
    }
    
    /// Get direct children of a concept
    pub fn children(&self, id: &str) -> Vec<String> {
        self.hierarchy.get(id).cloned().unwrap_or_default()
    }
    
    /// Get all descendants (recursive)
    pub fn descendants(&self, id: &str) -> Vec<String> {
        let mut result = Vec::new();
        let mut stack = vec![id.to_string()];
        let mut visited = HashSet::new();
        
        while let Some(current) = stack.pop() {
            if visited.contains(&current) {
                continue;
            }
            visited.insert(current.clone());
            
            if let Some(children) = self.hierarchy.get(&current) {
                for child in children {
                    result.push(child.clone());
                    stack.push(child.clone());
                }
            }
        }
        
        result
    }
    
    /// Get direct parents
    pub fn get_parents(&self, id: &str) -> Vec<String> {
        self.parents.get(id).cloned().unwrap_or_default()
    }
    
    /// Get all ancestors (recursive)
    pub fn ancestors(&self, id: &str) -> Vec<String> {
        let mut result = Vec::new();
        let mut stack = vec![id.to_string()];
        let mut visited = HashSet::new();
        
        while let Some(current) = stack.pop() {
            if visited.contains(&current) {
                continue;
            }
            visited.insert(current.clone());
            
            if let Some(parents) = self.parents.get(&current) {
                for parent in parents {
                    result.push(parent.clone());
                    stack.push(parent.clone());
                }
            }
        }
        
        result
    }
    
    /// Get depth of concept in taxonomy (0 = root)
    pub fn depth(&self, id: &str) -> usize {
        if self.roots.contains(&id.to_string()) {
            return 0;
        }
        
        let parents = self.get_parents(id);
        if parents.is_empty() {
            return 0;
        }
        
        parents
            .iter()
            .map(|p| self.depth(p) + 1)
            .max()
            .unwrap_or(0)
    }
    
    /// Get leaves (concepts with no children)
    pub fn leaves(&self) -> Vec<String> {
        let concept_ids: HashSet<_> = self.parents.keys().cloned().collect();
        
        concept_ids
            .into_iter()
            .filter(|id| self.children(id).is_empty())
            .collect()
    }
    
    /// Get taxonomy statistics
    pub fn stats(&self) -> TaxonomyStats {
        let total_concepts = self.parents.len() + self.roots.len();
        let max_depth = self.roots
            .iter()
            .flat_map(|root| self.descendants(root))
            .map(|id| self.depth(&id))
            .max()
            .unwrap_or(0);
        
        TaxonomyStats {
            root_count: self.roots.len(),
            total_concepts,
            max_depth,
            leaf_count: self.leaves().len(),
        }
    }
    
    /// Check if A is ancestor of B
    pub fn is_ancestor(&self, ancestor: &str, descendant: &str) -> bool {
        self.ancestors(descendant).contains(&ancestor.to_string())
    }
    
    /// Get lowest common ancestor
    pub fn lowest_common_ancestor(&self, a: &str, b: &str) -> Option<String> {
        let ancestors_a: HashSet<_> = self.ancestors(a).into_iter().collect();
        let ancestors_b: HashSet<_> = self.ancestors(b).into_iter().collect();
        
        let common: Vec<_> = ancestors_a.intersection(&ancestors_b).collect();
        
        // Find the deepest common ancestor
        common
            .into_iter()
            .max_by_key(|id| self.depth(id))
            .map(|s| s.to_string())
    }
}

/// Taxonomy statistics
#[derive(Debug, Clone)]
pub struct TaxonomyStats {
    pub root_count: usize,
    pub total_concepts: usize,
    pub max_depth: usize,
    pub leaf_count: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::crud::create_concept;
    use crate::schema::dhatu::Dhatu;
    use crate::schema::relations::add_relation;
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(repo: &PaniniRepo, id: &str) -> Concept {
        let concept = Concept {
            id: id.to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: format!("Test {}", id),
            tags: vec![],
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
    fn test_build_taxonomy() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        // Create: animal -> mammal -> dog
        create_test_concept(&repo, "animal");
        create_test_concept(&repo, "mammal");
        create_test_concept(&repo, "dog");
        
        add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
        add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
        
        let taxonomy = Taxonomy::build(&repo).unwrap();
        
        assert_eq!(taxonomy.roots.len(), 1);
        assert!(taxonomy.roots.contains(&"animal".to_string()));
    }
    
    #[test]
    fn test_children() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "animal");
        create_test_concept(&repo, "mammal");
        create_test_concept(&repo, "reptile");
        
        add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
        add_relation(&repo, "reptile", RelationType::IsA, "animal", None).unwrap();
        
        let taxonomy = Taxonomy::build(&repo).unwrap();
        let children = taxonomy.children("animal");
        
        assert_eq!(children.len(), 2);
        assert!(children.contains(&"mammal".to_string()));
        assert!(children.contains(&"reptile".to_string()));
    }
    
    #[test]
    fn test_descendants() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "animal");
        create_test_concept(&repo, "mammal");
        create_test_concept(&repo, "dog");
        create_test_concept(&repo, "cat");
        
        add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
        add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
        add_relation(&repo, "cat", RelationType::IsA, "mammal", None).unwrap();
        
        let taxonomy = Taxonomy::build(&repo).unwrap();
        let descendants = taxonomy.descendants("animal");
        
        assert_eq!(descendants.len(), 3); // mammal, dog, cat
    }
    
    #[test]
    fn test_ancestors() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "animal");
        create_test_concept(&repo, "mammal");
        create_test_concept(&repo, "dog");
        
        add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
        add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
        
        let taxonomy = Taxonomy::build(&repo).unwrap();
        let ancestors = taxonomy.ancestors("dog");
        
        assert_eq!(ancestors.len(), 2); // mammal, animal
        assert!(ancestors.contains(&"mammal".to_string()));
        assert!(ancestors.contains(&"animal".to_string()));
    }
    
    #[test]
    fn test_depth() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "animal");
        create_test_concept(&repo, "mammal");
        create_test_concept(&repo, "dog");
        
        add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
        add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
        
        let taxonomy = Taxonomy::build(&repo).unwrap();
        
        assert_eq!(taxonomy.depth("animal"), 0);
        assert_eq!(taxonomy.depth("mammal"), 1);
        assert_eq!(taxonomy.depth("dog"), 2);
    }
    
    #[test]
    fn test_lowest_common_ancestor() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "animal");
        create_test_concept(&repo, "mammal");
        create_test_concept(&repo, "dog");
        create_test_concept(&repo, "cat");
        
        add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
        add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
        add_relation(&repo, "cat", RelationType::IsA, "mammal", None).unwrap();
        
        let taxonomy = Taxonomy::build(&repo).unwrap();
        let lca = taxonomy.lowest_common_ancestor("dog", "cat");
        
        assert_eq!(lca, Some("mammal".to_string()));
    }
}
