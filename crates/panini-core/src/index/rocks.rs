//! RocksDB-based local index for fast concept/relation lookups

use crate::error::{Error, Result};
use crate::schema::concept::Concept;
use crate::schema::relation::Relation;
use rocksdb::{DB, Options, IteratorMode};
use serde::{Deserialize, Serialize};
use std::path::Path;

/// Column families for RocksDB
pub const CF_CONCEPTS: &str = "concepts";
pub const CF_RELATIONS: &str = "relations";
pub const CF_METADATA: &str = "metadata";

/// RocksDB index for concepts and relations
pub struct RocksIndex {
    db: DB,
}

impl RocksIndex {
    /// Open or create RocksDB index
    pub fn open<P: AsRef<Path>>(path: P) -> Result<Self> {
        let mut opts = Options::default();
        opts.create_if_missing(true);
        opts.create_missing_column_families(true);
        
        let cf_names = vec![CF_CONCEPTS, CF_RELATIONS, CF_METADATA];
        
        let db = DB::open_cf(&opts, path, &cf_names)
            .map_err(|e| Error::Index(format!("Failed to open RocksDB: {}", e)))?;
        
        Ok(Self { db })
    }
    
    /// Store concept in index
    pub fn put_concept(&self, concept: &Concept) -> Result<()> {
        let cf = self.db.cf_handle(CF_CONCEPTS)
            .ok_or_else(|| Error::Index("CF_CONCEPTS not found".to_string()))?;
        
        let value = serde_json::to_vec(concept)
            .map_err(|e| Error::Index(e.to_string()))?;
        
        self.db.put_cf(&cf, concept.id.as_bytes(), value)
            .map_err(|e| Error::Index(format!("Failed to put concept: {}", e)))?;
        
        Ok(())
    }
    
    /// Get concept from index
    pub fn get_concept(&self, id: &str) -> Result<Option<Concept>> {
        let cf = self.db.cf_handle(CF_CONCEPTS)
            .ok_or_else(|| Error::Index("CF_CONCEPTS not found".to_string()))?;
        
        let value = self.db.get_cf(&cf, id.as_bytes())
            .map_err(|e| Error::Index(format!("Failed to get concept: {}", e)))?;
        
        match value {
            Some(ref bytes) => {
                let concept = serde_json::from_slice(&bytes)
                    .map_err(|e| Error::Index(e.to_string()))?;
                Ok(Some(concept))
            }
            None => Ok(None),
        }
    }
    
    /// Delete concept from index
    pub fn delete_concept(&self, id: &str) -> Result<()> {
        let cf = self.db.cf_handle(CF_CONCEPTS)
            .ok_or_else(|| Error::Index("CF_CONCEPTS not found".to_string()))?;
        
        self.db.delete_cf(&cf, id.as_bytes())
            .map_err(|e| Error::Index(format!("Failed to delete concept: {}", e)))?;
        
        Ok(())
    }
    
    /// List all concept IDs
    pub fn list_concept_ids(&self) -> Result<Vec<String>> {
        let cf = self.db.cf_handle(CF_CONCEPTS)
            .ok_or_else(|| Error::Index("CF_CONCEPTS not found".to_string()))?;
        
        let iter = self.db.iterator_cf(&cf, IteratorMode::Start);
        
        let mut ids = Vec::new();
        for item in iter {
            let (key, _) = item.map_err(|e| Error::Index(e.to_string()))?;
            let id = String::from_utf8(key.to_vec())
                .map_err(|e| Error::Index(e.to_string()))?;
            ids.push(id);
        }
        
        Ok(ids)
    }
    
    /// Store relation in index (keyed by source_id:type:target_id)
    pub fn put_relation(&self, source_id: &str, relation: &Relation) -> Result<()> {
        let cf = self.db.cf_handle(CF_RELATIONS)
            .ok_or_else(|| Error::Index("CF_RELATIONS not found".to_string()))?;
        
        let key = format!("{}:{}:{}", source_id, relation.rel_type as u8, relation.target);
        
        let value = serde_json::to_vec(relation)
            .map_err(|e| Error::Index(e.to_string()))?;
        
        self.db.put_cf(&cf, key.as_bytes(), value)
            .map_err(|e| Error::Index(format!("Failed to put relation: {}", e)))?;
        
        Ok(())
    }
    
    /// Get all relations from a source concept
    pub fn get_relations(&self, source_id: &str) -> Result<Vec<Relation>> {
        let cf = self.db.cf_handle(CF_RELATIONS)
            .ok_or_else(|| Error::Index("CF_RELATIONS not found".to_string()))?;
        
        let prefix = format!("{}:", source_id);
        let iter = self.db.iterator_cf(&cf, IteratorMode::From(prefix.as_bytes(), rocksdb::Direction::Forward));
        
        let mut relations = Vec::new();
        for item in iter {
            let (key, value) = item.map_err(|e| Error::Index(e.to_string()))?;
            
            let key_str = String::from_utf8(key.to_vec())
                .map_err(|e| Error::Index(e.to_string()))?;
            
            // Stop if we've moved past this source_id
            if !key_str.starts_with(&prefix) {
                break;
            }
            
            let relation: Relation = serde_json::from_slice(&value)
                .map_err(|e| Error::Index(e.to_string()))?;
            
            relations.push(relation);
        }
        
        Ok(relations)
    }
    
    /// Delete all relations from a source concept
    pub fn delete_relations(&self, source_id: &str) -> Result<()> {
        let cf = self.db.cf_handle(CF_RELATIONS)
            .ok_or_else(|| Error::Index("CF_RELATIONS not found".to_string()))?;
        
        let relations = self.get_relations(source_id)?;
        
        for relation in relations {
            let key = format!("{}:{}:{}", source_id, relation.rel_type as u8, relation.target);
            self.db.delete_cf(&cf, key.as_bytes())
                .map_err(|e| Error::Index(format!("Failed to delete relation: {}", e)))?;
        }
        
        Ok(())
    }
    
    /// Store metadata
    pub fn put_metadata(&self, key: &str, value: &[u8]) -> Result<()> {
        let cf = self.db.cf_handle(CF_METADATA)
            .ok_or_else(|| Error::Index("CF_METADATA not found".to_string()))?;
        
        self.db.put_cf(&cf, key.as_bytes(), value)
            .map_err(|e| Error::Index(format!("Failed to put metadata: {}", e)))?;
        
        Ok(())
    }
    
    /// Get metadata
    pub fn get_metadata(&self, key: &str) -> Result<Option<Vec<u8>>> {
        let cf = self.db.cf_handle(CF_METADATA)
            .ok_or_else(|| Error::Index("CF_METADATA not found".to_string()))?;
        
        self.db.get_cf(&cf, key.as_bytes())
            .map_err(|e| Error::Index(format!("Failed to get metadata: {}", e)))
    }
    
    /// Get index statistics
    pub fn stats(&self) -> Result<IndexStats> {
        let concept_count = self.list_concept_ids()?.len();
        
        let cf = self.db.cf_handle(CF_RELATIONS)
            .ok_or_else(|| Error::Index("CF_RELATIONS not found".to_string()))?;
        
        let iter = self.db.iterator_cf(&cf, IteratorMode::Start);
        let relation_count = iter.count();
        
        Ok(IndexStats {
            concept_count,
            relation_count,
        })
    }
    
    /// Flush database to disk
    pub fn flush(&self) -> Result<()> {
        self.db.flush()
            .map_err(|e| Error::Index(format!("Failed to flush: {}", e)))
    }
    
    /// Compact database
    pub fn compact(&self) -> Result<()> {
        self.db.compact_range::<&[u8], &[u8]>(None, None);
        Ok(())
    }
}

/// Index statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IndexStats {
    pub concept_count: usize,
    pub relation_count: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::dhatu::Dhatu;
    use crate::schema::relation::{Relation, RelationType};
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(id: &str) -> Concept {
        Concept {
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
        }
    }
    
    #[test]
    fn test_open_index() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        let stats = index.stats().unwrap();
        assert_eq!(stats.concept_count, 0);
        assert_eq!(stats.relation_count, 0);
    }
    
    #[test]
    fn test_put_get_concept() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        let concept = create_test_concept("test1");
        index.put_concept(&concept).unwrap();
        
        let retrieved = index.get_concept("test1").unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().id, "test1");
    }
    
    #[test]
    fn test_delete_concept() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        let concept = create_test_concept("test1");
        index.put_concept(&concept).unwrap();
        
        index.delete_concept("test1").unwrap();
        
        let retrieved = index.get_concept("test1").unwrap();
        assert!(retrieved.is_none());
    }
    
    #[test]
    fn test_list_concepts() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        for i in 0..5 {
            let concept = create_test_concept(&format!("test{}", i));
            index.put_concept(&concept).unwrap();
        }
        
        let ids = index.list_concept_ids().unwrap();
        assert_eq!(ids.len(), 5);
    }
    
    #[test]
    fn test_put_get_relations() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        let relation = Relation {
            rel_type: RelationType::IsA,
            target: "target1".to_string(),
            confidence: 0.9,
        
            evidence: vec![],
            created: None,
            author: None,};
        
        index.put_relation("source1", &relation).unwrap();
        
        let relations = index.get_relations("source1").unwrap();
        assert_eq!(relations.len(), 1);
        assert_eq!(relations[0].target, "target1");
    }
    
    #[test]
    fn test_delete_relations() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        let relation1 = Relation {
            rel_type: RelationType::IsA,
            target: "target1".to_string(),
            confidence: 0.9,
        
            evidence: vec![],
            created: None,
            author: None,};
        
        let relation2 = Relation {
            rel_type: RelationType::PartOf,
            target: "target2".to_string(),
            confidence: 0.8,
        
            evidence: vec![],
            created: None,
            author: None,};
        
        index.put_relation("source1", &relation1).unwrap();
        index.put_relation("source1", &relation2).unwrap();
        
        index.delete_relations("source1").unwrap();
        
        let relations = index.get_relations("source1").unwrap();
        assert_eq!(relations.len(), 0);
    }
    
    #[test]
    fn test_metadata() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        let data = b"test metadata";
        index.put_metadata("key1", data).unwrap();
        
        let retrieved = index.get_metadata("key1").unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap(), data);
    }
    
    #[test]
    fn test_stats() {
        let tmp = TempDir::new().unwrap();
        let index = RocksIndex::open(tmp.path().join("index")).unwrap();
        
        for i in 0..3 {
            let concept = create_test_concept(&format!("test{}", i));
            index.put_concept(&concept).unwrap();
        }
        
        let relation = Relation {
            rel_type: RelationType::IsA,
            target: "target".to_string(),
            confidence: 0.0,
        
            evidence: vec![],
            created: None,
            author: None,};
        index.put_relation("test0", &relation).unwrap();
        index.put_relation("test1", &relation).unwrap();
        
        let stats = index.stats().unwrap();
        assert_eq!(stats.concept_count, 3);
        assert_eq!(stats.relation_count, 2);
    }
}
