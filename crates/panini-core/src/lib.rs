//! # Panini Core Library
//!
//! Git-native distributed knowledge graph system.
//!
//! ## Features
//!
//! - **Git-native storage**: Uses Git repositories for versioned knowledge
//! - **Markdown + YAML**: Human-readable concept files
//! - **Local indexing**: RocksDB + Tantivy for fast queries
//! - **Sync protocol**: Pull/push with conflict resolution
//! - **S3-compatible storage**: For binary content
//! - **Multi-language fulltext search**: 20+ languages supported
//!
/// ## Example
///
/// ```ignore
/// use panini_core::{PaniniRepo, Concept};
///
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// // Initialize a new repository
/// let repo = PaniniRepo::init("my-knowledge")?;
///
/// // Create a concept (example - actual API may differ)
/// let concept = Concept::builder()
///     .id("concept_cas_001")
///     .title("Content-Addressable Storage")
///     .dhatu(Dhatu::TEXT)
///     .tag("storage/distributed")
///     .build()?;

// Public API exports
pub mod error;
pub mod git;
pub mod index;
pub mod query;
pub mod schema;
pub mod storage;
pub mod sync;

// Re-export main types
pub use error::{Error, Result};
pub use git::open::{PaniniConfig, SchemaVersion};
pub use git::repo::PaniniRepo;
pub use schema::concept::{Concept, ConceptBuilder};
pub use schema::dhatu::Dhatu;
pub use schema::relation::{Relation, RelationType};

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Minimum supported Rust version
pub const MSRV: &str = "1.75";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert!(!VERSION.is_empty());
        assert_eq!(VERSION, "2.0.0");
    }
}
