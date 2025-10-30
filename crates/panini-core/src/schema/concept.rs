//! Concept model, validation, and YAML frontmatter parsing

use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use chrono::{DateTime, Utc};
use crate::error::{Error, Result};
use crate::schema::{Relation, Dhatu};
use pulldown_cmark::{Parser, Event, Tag};

/// Concept type
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ConceptType {
    Concept,
    Relation,
    Metadata,
}

/// Main concept structure
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Concept {
    pub id: String,
    pub r#type: ConceptType,
    pub dhatu: Dhatu,
    pub title: String,
    pub tags: Vec<String>,
    pub created: DateTime<Utc>,
    pub updated: DateTime<Utc>,
    pub author: Option<String>,
    pub relations: Vec<Relation>,
    pub content_refs: Vec<ContentRef>,
    pub metadata: serde_json::Value,
    
    #[serde(skip)]
    pub markdown_body: String,
}

/// Content reference (for S3-stored content)
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ContentRef {
    pub hash: String,
    pub r#type: Dhatu,
    pub size: u64,
    pub mime: String,
    pub storage: String,
    pub description: Option<String>,
    pub created: Option<DateTime<Utc>>,
    pub thumbnail: Option<String>,
}

/// Builder for Concept
pub struct ConceptBuilder {
    id: Option<String>,
    title: Option<String>,
    dhatu: Option<Dhatu>,
    tags: Vec<String>,
    markdown_body: String,
}

impl ConceptBuilder {
    pub fn new() -> Self {
        Self {
            id: None,
            title: None,
            dhatu: None,
            tags: Vec::new(),
            markdown_body: String::new(),
        }
    }
    
    pub fn id(mut self, id: impl Into<String>) -> Self {
        self.id = Some(id.into());
        self
    }
    
    pub fn title(mut self, title: impl Into<String>) -> Self {
        self.title = Some(title.into());
        self
    }
    
    pub fn dhatu(mut self, dhatu: Dhatu) -> Self {
        self.dhatu = Some(dhatu);
        self
    }
    
    pub fn tag(mut self, tag: impl Into<String>) -> Self {
        self.tags.push(tag.into());
        self
    }
    
    pub fn tags(mut self, tags: Vec<String>) -> Self {
        self.tags = tags;
        self
    }
    
    pub fn markdown_body(mut self, body: impl Into<String>) -> Self {
        self.markdown_body = body.into();
        self
    }
    
    pub fn build(self) -> crate::Result<Concept> {
        let now = Utc::now();
        
        Ok(Concept {
            id: self.id.ok_or_else(|| crate::Error::generic("Missing concept ID"))?,
            r#type: ConceptType::Concept,
            dhatu: self.dhatu.ok_or_else(|| crate::Error::generic("Missing dhatu"))?,
            title: self.title.ok_or_else(|| crate::Error::generic("Missing title"))?,
            tags: self.tags,
            created: now,
            updated: now,
            author: None,
            relations: Vec::new(),
            content_refs: Vec::new(),
            metadata: serde_json::Value::Null,
            markdown_body: self.markdown_body,
        })
    }
}

impl Concept {
    pub fn builder() -> ConceptBuilder {
        ConceptBuilder::new()
    }
}

impl Default for ConceptBuilder {
    fn default() -> Self {
        Self::new()
    }
}

/// Parse Markdown with YAML frontmatter
pub fn parse_concept_markdown(content: &str) -> Result<Concept> {
    // Split frontmatter and body
    let (frontmatter, body) = extract_frontmatter(content)?;
    
    // Parse YAML frontmatter
    let mut concept: Concept = serde_yaml::from_str(&frontmatter)
        .map_err(|e| Error::InvalidFrontmatter(e.to_string()))?;
    
    // Set markdown body
    concept.markdown_body = body;
    
    // Validate
    validate_concept(&concept)?;
    
    Ok(concept)
}

/// Extract YAML frontmatter from Markdown
fn extract_frontmatter(content: &str) -> Result<(String, String)> {
    let trimmed = content.trim_start();
    
    if !trimmed.starts_with("---") {
        return Err(Error::MissingFrontmatter(PathBuf::from(".")));
    }
    
    let after_first = &trimmed[3..];
    
    if let Some(end_pos) = after_first.find("\n---\n") {
        let frontmatter = after_first[..end_pos].trim().to_string();
        let body = after_first[end_pos + 5..].trim().to_string();
        Ok((frontmatter, body))
    } else {
        Err(Error::InvalidFrontmatter(
            "Missing closing --- for frontmatter".to_string()
        ))
    }
}

/// Validate concept
pub fn validate_concept(concept: &Concept) -> Result<()> {
    // Validate ID (alphanumeric, dash, underscore only)
    if concept.id.is_empty() {
        return Err(Error::Validation("Concept ID cannot be empty".to_string()));
    }
    
    if !concept.id.chars().all(|c| c.is_alphanumeric() || c == '-' || c == '_') {
        return Err(Error::Validation(
            "Concept ID must contain only alphanumeric, dash, or underscore".to_string()
        ));
    }
    
    // Validate title
    if concept.title.is_empty() {
        return Err(Error::Validation("Concept title cannot be empty".to_string()));
    }
    
    if concept.title.len() > 200 {
        return Err(Error::Validation(
            "Concept title must be 200 characters or less".to_string()
        ));
    }
    
    // Validate tags
    for tag in &concept.tags {
        if tag.is_empty() {
            return Err(Error::Validation("Tag cannot be empty".to_string()));
        }
        
        if tag.len() > 50 {
            return Err(Error::Validation(
                "Tag must be 50 characters or less".to_string()
            ));
        }
    }
    
    // Validate relations
    for relation in &concept.relations {
        if relation.target.is_empty() {
            return Err(Error::Validation(
                "Relation target cannot be empty".to_string()
            ));
        }
    }
    
    Ok(())
}

/// Serialize concept to Markdown with YAML frontmatter
pub fn serialize_concept_markdown(concept: &Concept) -> Result<String> {
    // Serialize frontmatter
    let frontmatter = serde_yaml::to_string(concept)
        .map_err(|e| Error::YamlParse(e))?;
    
    // Combine with body
    Ok(format!("---\n{}---\n\n{}", frontmatter, concept.markdown_body))
}

/// Extract title from Markdown body (first H1)
pub fn extract_title_from_markdown(markdown: &str) -> Option<String> {
    let parser = Parser::new(markdown);
    
    let mut in_heading = false;
    let mut title = String::new();
    
    for event in parser {
        match event {
            Event::Start(Tag::Heading(pulldown_cmark::HeadingLevel::H1, _, _)) => {
                in_heading = true;
            }
            Event::End(Tag::Heading(_, _, _)) => {
                if in_heading {
                    return Some(title.trim().to_string());
                }
            }
            Event::Text(text) if in_heading => {
                title.push_str(&text);
            }
            _ => {}
        }
    }
    
    None
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_concept_markdown() {
        let content = r#"---
id: rust-lang
type: concept
dhatu: TEXT
title: Rust Programming Language
tags:
  - programming
  - systems
created: 2025-01-01T00:00:00Z
updated: 2025-01-01T00:00:00Z
author: test
relations: []
content_refs: []
metadata: null
---

# Rust Programming Language

Rust is a systems programming language.
"#;
        
        let concept = parse_concept_markdown(content).unwrap();
        
        assert_eq!(concept.id, "rust-lang");
        assert_eq!(concept.title, "Rust Programming Language");
        assert_eq!(concept.tags.len(), 2);
        assert!(concept.markdown_body.contains("systems programming"));
    }
    
    #[test]
    fn test_extract_frontmatter() {
        let content = "---\nid: test\n---\n\nBody";
        let (fm, body) = extract_frontmatter(content).unwrap();
        
        assert_eq!(fm, "id: test");
        assert_eq!(body, "Body");
    }
    
    #[test]
    fn test_validate_concept_valid() {
        let concept = Concept {
            id: "valid-id".to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: "Valid Title".to_string(),
            tags: vec!["tag1".to_string()],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: "Body".to_string(),
        };
        
        assert!(validate_concept(&concept).is_ok());
    }
    
    #[test]
    fn test_validate_concept_empty_id() {
        let mut concept = Concept {
            id: "".to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: "Title".to_string(),
            tags: vec![],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: "".to_string(),
        };
        
        assert!(validate_concept(&concept).is_err());
    }
    
    #[test]
    fn test_validate_concept_invalid_id() {
        let concept = Concept {
            id: "invalid id!".to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: "Title".to_string(),
            tags: vec![],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: "".to_string(),
        };
        
        assert!(validate_concept(&concept).is_err());
    }
    
    #[test]
    fn test_serialize_concept_markdown() {
        let concept = Concept {
            id: "test".to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: "Test".to_string(),
            tags: vec![],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: "Body".to_string(),
        };
        
        let markdown = serialize_concept_markdown(&concept).unwrap();
        
        assert!(markdown.starts_with("---\n"));
        assert!(markdown.contains("id: test"));
        assert!(markdown.ends_with("Body"));
    }
    
    #[test]
    fn test_extract_title_from_markdown() {
        let markdown = "# Main Title\n\nSome content\n\n## Subtitle";
        let title = extract_title_from_markdown(markdown).unwrap();
        
        assert_eq!(title, "Main Title");
    }
}
