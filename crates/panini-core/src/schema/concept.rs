//! Concept model and builder

use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use crate::schema::{Relation, Dhatu};

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
