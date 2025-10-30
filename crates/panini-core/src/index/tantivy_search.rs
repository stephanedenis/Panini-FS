//! Tantivy-based fulltext search index

use crate::error::{Error, Result};
use tantivy::IndexReader;
use crate::schema::concept::Concept;
use serde::{Deserialize, Serialize};
use std::path::Path;
use tantivy::{
    collector::TopDocs,
    query::QueryParser,
    schema::*,
    Index, IndexWriter, ReloadPolicy,
};

/// Tantivy fulltext search index
pub struct TantivyIndex {
    index: Index,
    reader: IndexReader,
    writer: IndexWriter,
    schema: SearchSchema,
}

/// Search schema fields
pub struct SearchSchema {
    pub id: Field,
    pub title: Field,
    pub body: Field,
    pub tags: Field,
    pub dhatu: Field,
}

impl TantivyIndex {
    /// Create or open Tantivy index
    pub fn open<P: AsRef<Path>>(path: P) -> Result<Self> {
        let path = path.as_ref();
        std::fs::create_dir_all(path)
            .map_err(|e| Error::Index(format!("Failed to create directory: {}", e)))?;
        
        let mut schema_builder = Schema::builder();
        
        // ID field (stored, not indexed for search)
        let id = schema_builder.add_text_field("id", STRING | STORED);
        
        // Title field (indexed, stored, high weight)
        let title = schema_builder.add_text_field("title", TEXT | STORED);
        
        // Body field (indexed, stored)
        let body = schema_builder.add_text_field("body", TEXT | STORED);
        
        // Tags field (indexed, stored, for filtering)
        let tags = schema_builder.add_text_field("tags", TEXT | STORED);
        
        // Dhatu field (stored, for filtering)
        let dhatu = schema_builder.add_text_field("dhatu", STRING | STORED);
        
        let schema = schema_builder.build();
        let index = Index::create_in_ram(schema.clone());
        
        let reader = index
            .reader_builder()
            .reload_policy(ReloadPolicy::OnCommitWithDelay)
            .try_into()
            .map_err(|e| Error::Index(format!("Failed to create reader: {}", e)))?;
        
        let writer = index
            .writer(50_000_000) // 50 MB buffer
            .map_err(|e| Error::Index(format!("Failed to create writer: {}", e)))?;
        
        let search_schema = SearchSchema {
            id,
            title,
            body,
            tags,
            dhatu,
        };
        
        Ok(Self {
            index,
            reader,
            writer,
            schema: search_schema,
        })
    }
    
    /// Add concept to index
    pub fn add_concept(&mut self, concept: &Concept) -> Result<()> {
        let mut doc = TantivyDocument::default();
        
        doc.add_text(self.schema.id, &concept.id);
        doc.add_text(self.schema.title, &concept.title);
        doc.add_text(self.schema.body, &concept.markdown_body);
        doc.add_text(self.schema.tags, &concept.tags.join(" "));
        doc.add_text(self.schema.dhatu, &format!("{:?}", concept.dhatu));
        
        self.writer
            .add_document(doc)
            .map_err(|e| Error::Index(format!("Failed to add document: {}", e)))?;
        
        Ok(())
    }
    
    /// Delete concept from index
    pub fn delete_concept(&mut self, id: &str) -> Result<()> {
        let term = Term::from_field_text(self.schema.id, id);
        self.writer.delete_term(term);
        Ok(())
    }
    
    /// Commit changes to index
    pub fn commit(&mut self) -> Result<()> {
        self.writer
            .commit()
            .map_err(|e| Error::Index(format!("Failed to commit: {}", e)))?;
        
        // Force reload for immediate visibility (important for tests)
        self.reader
            .reload()
            .map_err(|e| Error::Index(format!("Failed to reload reader: {}", e)))?;
        
        Ok(())
    }
    
    /// Search concepts
    pub fn search(&self, query: &str, limit: usize) -> Result<Vec<SearchResult>> {
        let searcher = self.reader.searcher();
        
        let query_parser = QueryParser::for_index(
            &self.index,
            vec![self.schema.title, self.schema.body, self.schema.tags],
        );
        
        let query = query_parser
            .parse_query(query)
            .map_err(|e| Error::Index(format!("Failed to parse query: {}", e)))?;
        
        let top_docs = searcher
            .search(&query, &TopDocs::with_limit(limit))
            .map_err(|e| Error::Index(format!("Search failed: {}", e)))?;
        
        let mut results = Vec::new();
        
        for (score, doc_address) in top_docs {
            let doc: TantivyDocument = searcher
                .doc(doc_address)
                .map_err(|e| Error::Index(format!("Failed to retrieve document: {}", e)))?;
            
            let id = doc
                .get_first(self.schema.id)
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string();
            
            let title = doc
                .get_first(self.schema.title)
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string();
            
            let snippet = doc
                .get_first(self.schema.body)
                .and_then(|v| v.as_str())
                .map(|s| extract_snippet(s, 200))
                .unwrap_or_default();
            
            results.push(SearchResult {
                id,
                title,
                snippet,
                score,
            });
        }
        
        Ok(results)
    }
    
    /// Get index statistics
    pub fn stats(&self) -> Result<SearchStats> {
        let searcher = self.reader.searcher();
        let num_docs = searcher.num_docs() as usize;
        
        Ok(SearchStats { num_docs })
    }
}

/// Search result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchResult {
    pub id: String,
    pub title: String,
    pub snippet: String,
    pub score: f32,
}

/// Search statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchStats {
    pub num_docs: usize,
}

/// Extract snippet from text
fn extract_snippet(text: &str, max_len: usize) -> String {
    if text.len() <= max_len {
        return text.to_string();
    }
    
    let mut end = max_len;
    while end > 0 && !text.is_char_boundary(end) {
        end -= 1;
    }
    
    format!("{}...", &text[..end])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::dhatu::Dhatu;
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(id: &str, title: &str, body: &str) -> Concept {
        Concept {
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
            markdown_body: body.to_string(),
        }
    }
    
    #[test]
    fn test_open_index() {
        let tmp = TempDir::new().unwrap();
        let index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        let stats = index.stats().unwrap();
        assert_eq!(stats.num_docs, 0);
    }
    
    #[test]
    fn test_add_and_search() {
        let tmp = TempDir::new().unwrap();
        let mut index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        let concept = create_test_concept(
            "rust",
            "Rust Programming Language",
            "Rust is a systems programming language that runs blazingly fast.",
        );
        
        index.add_concept(&concept).unwrap();
        index.commit().unwrap();
        
        let results = index.search("rust", 10).unwrap();
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].id, "rust");
    }
    
    #[test]
    fn test_search_title() {
        let tmp = TempDir::new().unwrap();
        let mut index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        let concept = create_test_concept(
            "rust",
            "Rust Programming Language",
            "Content about Rust.",
        );
        
        index.add_concept(&concept).unwrap();
        index.commit().unwrap();
        
        let results = index.search("Programming", 10).unwrap();
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].title, "Rust Programming Language");
    }
    
    #[test]
    fn test_search_body() {
        let tmp = TempDir::new().unwrap();
        let mut index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        let concept = create_test_concept(
            "rust",
            "Rust",
            "Rust is a systems programming language that runs blazingly fast.",
        );
        
        index.add_concept(&concept).unwrap();
        index.commit().unwrap();
        
        let results = index.search("blazingly", 10).unwrap();
        assert_eq!(results.len(), 1);
        assert!(results[0].snippet.contains("blazingly"));
    }
    
    #[test]
    fn test_delete_concept() {
        let tmp = TempDir::new().unwrap();
        let mut index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        let concept = create_test_concept("test1", "Test", "Content");
        
        index.add_concept(&concept).unwrap();
        index.commit().unwrap();
        
        index.delete_concept("test1").unwrap();
        index.commit().unwrap();
        
        let results = index.search("Test", 10).unwrap();
        assert_eq!(results.len(), 0);
    }
    
    #[test]
    fn test_multiple_concepts() {
        let tmp = TempDir::new().unwrap();
        let mut index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        for i in 0..5 {
            let concept = create_test_concept(
                &format!("test{}", i),
                &format!("Test {}", i),
                &format!("Content {}", i),
            );
            index.add_concept(&concept).unwrap();
        }
        
        index.commit().unwrap();
        
        let stats = index.stats().unwrap();
        assert_eq!(stats.num_docs, 5);
        
        let results = index.search("Test", 10).unwrap();
        assert_eq!(results.len(), 5);
    }
    
    #[test]
    fn test_relevance_ranking() {
        let tmp = TempDir::new().unwrap();
        let mut index = TantivyIndex::open(tmp.path().join("search")).unwrap();
        
        // Concept with "rust" in title (high relevance)
        let c1 = create_test_concept(
            "rust",
            "Rust Programming",
            "General content",
        );
        
        // Concept with "rust" in body (lower relevance)
        let c2 = create_test_concept(
            "other",
            "Other Language",
            "Some content mentioning rust",
        );
        
        index.add_concept(&c1).unwrap();
        index.add_concept(&c2).unwrap();
        index.commit().unwrap();
        
        let results = index.search("rust", 10).unwrap();
        assert_eq!(results.len(), 2);
        
        // First result should be the one with "rust" in title
        assert_eq!(results[0].id, "rust");
        assert!(results[0].score > results[1].score);
    }
}
