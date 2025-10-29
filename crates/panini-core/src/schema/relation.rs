//! Relation types and evidence

use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

/// Relation between two concepts
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Relation {
    pub rel_type: RelationType,
    pub target: String,
    pub confidence: f64,
    pub evidence: Vec<Evidence>,
    pub created: Option<DateTime<Utc>>,
    pub author: Option<String>,
}

/// Fixed relation types (v1.0)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RelationType {
    IsA,
    PartOf,
    Causes,
    Contradicts,
    Supports,
    DerivesFrom,
    UsedBy,
    RelatedTo,
}

/// Evidence supporting a relation
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Evidence {
    pub r#type: EvidenceType,
    pub url: Option<String>,
    pub title: Option<String>,
    pub text: Option<String>,
}

/// Evidence type
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum EvidenceType {
    Citation,
    Inline,
    External,
}
