//! Relation management operations

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::schema::concept::Concept;
use crate::schema::crud::{read_concept, update_concept};
use crate::schema::relation::{Relation, RelationType};
use chrono::Utc;

/// Add a relation to a concept
pub fn add_relation(
    repo: &PaniniRepo,
    source_id: &str,
    rel_type: RelationType,
    target_id: &str,
    confidence: Option<f32>,
) -> Result<()> {
    // Read source concept
    let mut concept = read_concept(repo, source_id)?;
    
    // Check if relation already exists
    if concept.relations.iter().any(|r| {
        r.rel_type == rel_type && r.target == target_id
    }) {
        return Err(Error::Validation(format!(
            "Relation already exists: {} -> {:?} -> {}",
            source_id, rel_type, target_id
        )));
    }
    
    // Create relation
    let relation = Relation {
        rel_type,
        target: target_id.to_string(),
        confidence: confidence.unwrap_or(1.0) as f64,
        evidence: vec![],
        created: Some(Utc::now()),
        author: None,
    };
    
    // Add to concept
    concept.relations.push(relation);
    concept.updated = Utc::now();
    
    // Update concept
    update_concept(repo, &concept)?;
    
    Ok(())
}

/// Remove a relation from a concept
pub fn remove_relation(
    repo: &PaniniRepo,
    source_id: &str,
    rel_type: RelationType,
    target_id: &str,
) -> Result<()> {
    // Read source concept
    let mut concept = read_concept(repo, source_id)?;
    
    // Find and remove relation
    let initial_len = concept.relations.len();
    concept.relations.retain(|r| {
        !(r.rel_type == rel_type && r.target == target_id)
    });
    
    if concept.relations.len() == initial_len {
        return Err(Error::NotFound(format!(
            "Relation not found: {} -> {:?} -> {}",
            source_id, rel_type, target_id
        )));
    }
    
    concept.updated = Utc::now();
    
    // Update concept
    update_concept(repo, &concept)?;
    
    Ok(())
}

/// Get all relations from a concept
pub fn get_relations(repo: &PaniniRepo, concept_id: &str) -> Result<Vec<Relation>> {
    let concept = read_concept(repo, concept_id)?;
    Ok(concept.relations.clone())
}

/// Get relations by type
pub fn get_relations_by_type(
    repo: &PaniniRepo,
    concept_id: &str,
    rel_type: RelationType,
) -> Result<Vec<Relation>> {
    let concept = read_concept(repo, concept_id)?;
    
    Ok(concept
        .relations
        .into_iter()
        .filter(|r| r.rel_type == rel_type)
        .collect())
}

/// Get all relations pointing to a concept (reverse lookup)
pub fn get_incoming_relations(
    repo: &PaniniRepo,
    target_id: &str,
) -> Result<Vec<(String, Relation)>> {
    let concept_ids = crate::schema::crud::list_concepts(repo)?;
    let mut incoming = Vec::new();
    
    for id in concept_ids {
        let concept = read_concept(repo, &id)?;
        
        for relation in concept.relations {
            if relation.target == target_id {
                incoming.push((id.clone(), relation));
            }
        }
    }
    
    Ok(incoming)
}

/// Update relation confidence
pub fn update_relation_confidence(
    repo: &PaniniRepo,
    source_id: &str,
    rel_type: RelationType,
    target_id: &str,
    confidence: f32,
) -> Result<()> {
    // Validate confidence
    if !(0.0..=1.0).contains(&confidence) {
        return Err(Error::Validation(
            "Confidence must be between 0.0 and 1.0".to_string()
        ));
    }
    
    // Read source concept
    let mut concept = read_concept(repo, source_id)?;
    
    // Find and update relation
    let relation = concept
        .relations
        .iter_mut()
        .find(|r| r.rel_type == rel_type && r.target == target_id)
        .ok_or_else(|| {
            Error::NotFound(format!(
                "Relation not found: {} -> {:?} -> {}",
                source_id, rel_type, target_id
            ))
        })?;
    
    relation.confidence = confidence as f64;
    concept.updated = Utc::now();
    
    // Update concept
    update_concept(repo, &concept)?;
    
    Ok(())
}

/// Check if relation exists
pub fn relation_exists(
    repo: &PaniniRepo,
    source_id: &str,
    rel_type: RelationType,
    target_id: &str,
) -> Result<bool> {
    let concept = read_concept(repo, source_id)?;
    
    Ok(concept.relations.iter().any(|r| {
        r.rel_type == rel_type && r.target == target_id
    }))
}

/// Get relation count for concept
pub fn get_relation_count(repo: &PaniniRepo, concept_id: &str) -> Result<usize> {
    let concept = read_concept(repo, concept_id)?;
    Ok(concept.relations.len())
}

/// Get relation statistics
pub fn get_relation_stats(repo: &PaniniRepo, concept_id: &str) -> Result<RelationStats> {
    let concept = read_concept(repo, concept_id)?;
    
    let mut stats = RelationStats {
        total: concept.relations.len(),
        by_type: std::collections::HashMap::new(),
        avg_confidence: 0.0,
    };
    
    let mut confidence_sum = 0.0;
    let mut confidence_count = 0;
    
    for relation in &concept.relations {
        *stats.by_type.entry(relation.rel_type).or_insert(0) += 1;
        
        if relation.confidence > 0.0 {
            confidence_sum += relation.confidence;
            confidence_count += 1;
        }
    }
    
    if confidence_count > 0 {
        stats.avg_confidence = (confidence_sum as f32) / (confidence_count as f32);
    }
    
    Ok(stats)
}

/// Relation statistics
#[derive(Debug, Clone)]
pub struct RelationStats {
    pub total: usize,
    pub by_type: std::collections::HashMap<RelationType, usize>,
    pub avg_confidence: f32,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::crud::create_concept;
    use crate::schema::dhatu::Dhatu;
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
    fn test_add_relation() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source");
        create_test_concept(&repo, "target");
        
        add_relation(&repo, "source", RelationType::IsA, "target", None).unwrap();
        
        let relations = get_relations(&repo, "source").unwrap();
        assert_eq!(relations.len(), 1);
        assert_eq!(relations[0].target, "target");
    }
    
    #[test]
    fn test_remove_relation() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source");
        create_test_concept(&repo, "target");
        
        add_relation(&repo, "source", RelationType::IsA, "target", None).unwrap();
        remove_relation(&repo, "source", RelationType::IsA, "target").unwrap();
        
        let relations = get_relations(&repo, "source").unwrap();
        assert_eq!(relations.len(), 0);
    }
    
    #[test]
    fn test_get_relations_by_type() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source");
        create_test_concept(&repo, "target1");
        create_test_concept(&repo, "target2");
        
        add_relation(&repo, "source", RelationType::IsA, "target1", None).unwrap();
        add_relation(&repo, "source", RelationType::PartOf, "target2", None).unwrap();
        
        let is_a_relations = get_relations_by_type(&repo, "source", RelationType::IsA).unwrap();
        assert_eq!(is_a_relations.len(), 1);
        assert_eq!(is_a_relations[0].target, "target1");
    }
    
    #[test]
    fn test_get_incoming_relations() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source1");
        create_test_concept(&repo, "source2");
        create_test_concept(&repo, "target");
        
        add_relation(&repo, "source1", RelationType::IsA, "target", None).unwrap();
        add_relation(&repo, "source2", RelationType::PartOf, "target", None).unwrap();
        
        let incoming = get_incoming_relations(&repo, "target").unwrap();
        assert_eq!(incoming.len(), 2);
    }
    
    #[test]
    fn test_update_relation_confidence() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source");
        create_test_concept(&repo, "target");
        
        add_relation(&repo, "source", RelationType::IsA, "target", Some(0.5)).unwrap();
        update_relation_confidence(&repo, "source", RelationType::IsA, "target", 0.9).unwrap();
        
        let relations = get_relations(&repo, "source").unwrap();
        assert_eq!(relations[0].confidence, Some(0.9));
    }
    
    #[test]
    fn test_relation_exists() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source");
        create_test_concept(&repo, "target");
        
        assert!(!relation_exists(&repo, "source", RelationType::IsA, "target").unwrap());
        
        add_relation(&repo, "source", RelationType::IsA, "target", None).unwrap();
        
        assert!(relation_exists(&repo, "source", RelationType::IsA, "target").unwrap());
    }
    
    #[test]
    fn test_get_relation_stats() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "source");
        create_test_concept(&repo, "target1");
        create_test_concept(&repo, "target2");
        
        add_relation(&repo, "source", RelationType::IsA, "target1", Some(0.8)).unwrap();
        add_relation(&repo, "source", RelationType::PartOf, "target2", Some(0.6)).unwrap();
        
        let stats = get_relation_stats(&repo, "source").unwrap();
        
        assert_eq!(stats.total, 2);
        assert_eq!(stats.avg_confidence, 0.7);
    }
}
