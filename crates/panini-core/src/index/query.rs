//! Unified query engine combining RocksDB and Tantivy

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::index::builder::IndexBuilder;
use crate::index::rocks::RocksIndex;
use crate::index::tantivy_search::{SearchResult, TantivyIndex};
use crate::schema::concept::Concept;
use crate::schema::graph::KnowledgeGraph;
use crate::schema::relation::{Relation, RelationType};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;
use std::sync::{Arc, RwLock};

/// Unified query engine
pub struct QueryEngine {
    repo: PaniniRepo,
    rocks: Arc<RocksIndex>,
    tantivy: Arc<RwLock<TantivyIndex>>,
    cache: Arc<RwLock<QueryCache>>,
    index_path: std::path::PathBuf,
}

impl QueryEngine {
    /// Create new query engine
    pub fn new(repo: PaniniRepo, index_path: &Path) -> Result<Self> {
        let rocks_path = index_path.join("rocks");
        let tantivy_path = index_path.join("tantivy");
        
        let rocks = Arc::new(RocksIndex::open(&rocks_path)?);
        let tantivy = Arc::new(RwLock::new(TantivyIndex::open(tantivy_path)?));
        let cache = Arc::new(RwLock::new(QueryCache::new(1000)));
        
        Ok(Self {
            repo,
            rocks,
            tantivy,
            cache,
            index_path: index_path.to_path_buf(),
        })
    }
    
    /// Full rebuild of both indexes
    pub fn rebuild(&self) -> Result<()> {
        // PROBLEM: We can't open two RocksDB instances on the same path
        // Solution: Read concepts from repo, build both indexes in parallel
        
        // Get all concepts from repo
        let concept_ids = crate::schema::crud::list_concepts(&self.repo)?;
        let mut concepts = Vec::new();
        for id in &concept_ids {
            if let Ok(concept) = crate::schema::crud::read_concept(&self.repo, &id) {
                concepts.push(concept);
            }
        }
        
        // Build RocksDB index
        for concept in &concepts {
            self.rocks.put_concept(concept)?;
            for relation in &concept.relations {
                self.rocks.put_relation(&concept.id, relation)?;
            }
        }
        self.rocks.flush()?;
        
        // Build Tantivy index
        let mut tantivy = self.tantivy.write()
            .map_err(|_| Error::Index("Failed to acquire write lock".to_string()))?;
        
        for concept in &concepts {
            tantivy.add_concept(concept)?;
        }
        
        tantivy.commit()?;
        
        // Clear cache
        self.cache.write()
            .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?
            .clear();
        
        Ok(())
    }
    
    /// Get concept by ID (cached)
    pub fn get_concept(&self, id: &str) -> Result<Option<Concept>> {
        // Check cache
        let cache_key = format!("concept:{}", id);
        {
            let mut cache = self.cache.write()
                .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
            
            if let Some(result) = cache.get(&cache_key) {
                return Ok(result.clone());
            }
        }
        
        // Query RocksDB
        let concept = self.rocks.get_concept(id)?;
        
        // Update cache
        {
            let mut cache = self.cache.write()
                .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
            
            cache.put(cache_key, concept.clone());
        }
        
        Ok(concept)
    }
    
    /// Get relations (cached)
    pub fn get_relations(&self, id: &str) -> Result<Vec<Relation>> {
        let cache_key = format!("relations:{}", id);
        {
            let mut cache = self.cache.write()
                .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
            
            if let Some(result) = cache.get_relations(&cache_key) {
                return Ok(result.clone());
            }
        }
        
        let relations = self.rocks.get_relations(id)?;
        
        {
            let mut cache = self.cache.write()
                .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
            
            cache.put_relations(cache_key, relations.clone());
        }
        
        Ok(relations)
    }
    
    /// Fulltext search
    pub fn search(&self, query: &str, limit: usize) -> Result<Vec<SearchResult>> {
        let tantivy = self.tantivy.write()
            .map_err(|_| Error::Index("Failed to acquire read lock".to_string()))?;
        
        tantivy.search(query, limit)
    }
    
    /// Find concepts by relation type
    pub fn find_by_relation(&self, rel_type: RelationType) -> Result<Vec<String>> {
        let concept_ids = self.rocks.list_concept_ids()?;
        
        let mut results = Vec::new();
        for id in concept_ids {
            let relations = self.rocks.get_relations(&id)?;
            
            if relations.iter().any(|r| r.rel_type == rel_type) {
                results.push(id);
            }
        }
        
        Ok(results)
    }
    
    /// Build knowledge graph (cached)
    pub fn build_graph(&self) -> Result<KnowledgeGraph> {
        // Check if graph is cached
        {
            let mut cache = self.cache.write()
                .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
            
            if let Some(graph) = cache.get_graph() {
                return Ok(graph.clone());
            }
        }
        
        let graph = KnowledgeGraph::build(&self.repo)?;
        
        {
            let mut cache = self.cache.write()
                .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
            
            cache.put_graph(graph.clone());
        }
        
        Ok(graph)
    }
    
    /// Clear cache
    pub fn clear_cache(&self) -> Result<()> {
        self.cache.write()
            .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?
            .clear();
        
        Ok(())
    }
    
    /// Get query statistics
    pub fn stats(&self) -> Result<QueryStats> {
        let rocks_stats = self.rocks.stats()?;
        
        let tantivy = self.tantivy.write()
            .map_err(|_| Error::Index("Failed to acquire read lock".to_string()))?;
        let tantivy_stats = tantivy.stats()?;
        
        let cache = self.cache.write()
            .map_err(|_| Error::Index("Failed to acquire cache lock".to_string()))?;
        
        Ok(QueryStats {
            concepts_indexed: rocks_stats.concept_count,
            relations_indexed: rocks_stats.relation_count,
            fulltext_docs: tantivy_stats.num_docs,
            cache_size: cache.size(),
            cache_hits: cache.hits,
            cache_misses: cache.misses,
        })
    }
    
    fn rocks_path(&self) -> Result<std::path::PathBuf> {
        // This is a simplified implementation
        // In practice, get from config
        Ok(self.repo.path().join(".panini/index/rocks"))
    }
}

/// Query cache
struct QueryCache {
    concepts: HashMap<String, Option<Concept>>,
    relations: HashMap<String, Vec<Relation>>,
    graph: Option<KnowledgeGraph>,
    max_size: usize,
    hits: u64,
    misses: u64,
}

impl QueryCache {
    fn new(max_size: usize) -> Self {
        Self {
            concepts: HashMap::new(),
            relations: HashMap::new(),
            graph: None,
            max_size,
            hits: 0,
            misses: 0,
        }
    }
    
    fn get(&mut self, key: &str) -> Option<&Option<Concept>> {
        match self.concepts.get(key) {
            Some(v) => {
                self.hits += 1;
                Some(v)
            }
            None => {
                self.misses += 1;
                None
            }
        }
    }
    
    fn put(&mut self, key: String, value: Option<Concept>) {
        if self.concepts.len() >= self.max_size {
            // Simple eviction: clear half the cache
            self.concepts.clear();
        }
        
        self.concepts.insert(key, value);
    }
    
    fn get_relations(&mut self, key: &str) -> Option<&Vec<Relation>> {
        match self.relations.get(key) {
            Some(v) => {
                self.hits += 1;
                Some(v)
            }
            None => {
                self.misses += 1;
                None
            }
        }
    }
    
    fn put_relations(&mut self, key: String, value: Vec<Relation>) {
        if self.relations.len() >= self.max_size {
            self.relations.clear();
        }
        
        self.relations.insert(key, value);
    }
    
    fn get_graph(&mut self) -> Option<&KnowledgeGraph> {
        match &self.graph {
            Some(g) => {
                self.hits += 1;
                Some(g)
            }
            None => {
                self.misses += 1;
                None
            }
        }
    }
    
    fn put_graph(&mut self, graph: KnowledgeGraph) {
        self.graph = Some(graph);
    }
    
    fn clear(&mut self) {
        self.concepts.clear();
        self.relations.clear();
        self.graph = None;
        self.hits = 0;
        self.misses = 0;
    }
    
    fn size(&self) -> usize {
        self.concepts.len() + self.relations.len() + if self.graph.is_some() { 1 } else { 0 }
    }
}

/// Query statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueryStats {
    pub concepts_indexed: usize,
    pub relations_indexed: usize,
    pub fulltext_docs: usize,
    pub cache_size: usize,
    pub cache_hits: u64,
    pub cache_misses: u64,
}

impl QueryStats {
    pub fn cache_hit_rate(&self) -> f64 {
        let total = self.cache_hits + self.cache_misses;
        if total == 0 {
            return 0.0;
        }
        
        (self.cache_hits as f64 / total as f64) * 100.0
    }
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
    fn test_query_engine_creation() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
        
        let stats = engine.stats().unwrap();
        assert_eq!(stats.concepts_indexed, 0);
    }
    
    #[test]
    fn test_rebuild_and_query() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "test1", "Test One");
        create_test_concept(&repo, "test2", "Test Two");
        
        let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
        engine.rebuild().unwrap();
        
        let stats = engine.stats().unwrap();
        assert_eq!(stats.concepts_indexed, 2);
        assert_eq!(stats.fulltext_docs, 2);
    }
    
    #[test]
    fn test_get_concept_caching() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "test1", "Test");
        
        let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
        engine.rebuild().unwrap();
        
        // First query (cache miss)
        let _ = engine.get_concept("test1").unwrap();
        
        // Second query (cache hit)
        let concept = engine.get_concept("test1").unwrap();
        assert!(concept.is_some());
        
        let stats = engine.stats().unwrap();
        assert!(stats.cache_hits > 0);
    }
    
    #[test]
    fn test_fulltext_search() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "rust", "Rust Programming");
        create_test_concept(&repo, "python", "Python Programming");
        
        let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
        engine.rebuild().unwrap();
        
        let results = engine.search("Rust", 10).unwrap();
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].id, "rust");
    }
    
    #[test]
    fn test_find_by_relation() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
        
        create_test_concept(&repo, "concept1", "Concept 1");
        create_test_concept(&repo, "concept2", "Concept 2");
        
        add_relation(&repo, "concept1", RelationType::IsA, "concept2", None).unwrap();
        
        let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
        engine.rebuild().unwrap();
        
        let results = engine.find_by_relation(RelationType::IsA).unwrap();
        assert!(results.contains(&"concept1".to_string()));
    }
}
