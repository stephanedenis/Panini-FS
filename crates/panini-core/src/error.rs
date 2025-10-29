//! Error types for Panini Core

use std::path::PathBuf;
use thiserror::Error;

/// Result type alias with Panini Error
pub type Result<T> = std::result::Result<T, Error>;

/// Main error type for Panini Core operations
#[derive(Debug, Error)]
pub enum Error {
    /// Git operation error
    #[error("Git error: {0}")]
    Git(#[from] git2::Error),

    /// IO error
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    /// Index error (RocksDB or Tantivy)
    #[error("Index error: {0}")]
    Index(String),

    /// Validation error
    #[error("Validation error: {0}")]
    Validation(String),

    /// Concept not found
    #[error("Concept not found: {0}")]
    NotFound(String),

    /// Merge conflict detected
    #[error("Merge conflict in: {}", .0.display())]
    MergeConflict(PathBuf),

    /// Schema version mismatch
    #[error("Schema version mismatch: expected {expected}, got {actual}")]
    SchemaVersionMismatch { expected: String, actual: String },

    /// Invalid concept ID format
    #[error("Invalid concept ID: {0}")]
    InvalidId(String),

    /// Missing frontmatter in Markdown file
    #[error("Missing YAML frontmatter in: {}", .0.display())]
    MissingFrontmatter(PathBuf),

    /// Invalid YAML frontmatter
    #[error("Invalid YAML frontmatter: {0}")]
    InvalidFrontmatter(String),

    /// YAML parsing error
    #[error("YAML parse error: {0}")]
    YamlParse(#[from] serde_yaml::Error),

    /// JSON parsing error
    #[error("JSON parse error: {0}")]
    JsonParse(#[from] serde_json::Error),

    /// Repository not initialized
    #[error("Repository not initialized at: {}", .0.display())]
    RepoNotInitialized(PathBuf),

    /// Repository already exists
    #[error("Repository already exists at: {}", .0.display())]
    RepoAlreadyExists(PathBuf),

    /// Configuration error
    #[error("Configuration error: {0}")]
    Config(String),

    /// Storage backend error
    #[error("Storage error: {0}")]
    Storage(String),

    /// Query parsing error
    #[error("Query parse error: {0}")]
    QueryParse(String),

    /// Submodule error
    #[error("Submodule error: {0}")]
    Submodule(String),

    /// Remote operation error
    #[error("Remote error: {0}")]
    Remote(String),

    /// Conflict resolution error
    #[error("Conflict resolution error: {0}")]
    ConflictResolution(String),

    /// Generic error
    #[error("{0}")]
    Generic(String),
}

impl Error {
    /// Create a generic error from a string
    pub fn generic(msg: impl Into<String>) -> Self {
        Error::Generic(msg.into())
    }

    /// Check if error is due to merge conflict
    pub fn is_conflict(&self) -> bool {
        matches!(self, Error::MergeConflict(_))
    }

    /// Check if error is due to not found
    pub fn is_not_found(&self) -> bool {
        matches!(self, Error::NotFound(_))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_display() {
        let err = Error::NotFound("concept_test_001".to_string());
        assert_eq!(err.to_string(), "Concept not found: concept_test_001");
    }

    #[test]
    fn test_error_is_conflict() {
        let err = Error::MergeConflict(PathBuf::from("test.md"));
        assert!(err.is_conflict());
    }

    #[test]
    fn test_error_is_not_found() {
        let err = Error::NotFound("test".to_string());
        assert!(err.is_not_found());
    }
}
