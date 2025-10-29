//! Dhātu types - Knowledge representation formats

use serde::{Deserialize, Serialize};
use std::fmt;

/// Dhātu (धातु) - Knowledge representation format
///
/// In Panini's grammar, dhātus are verbal roots. In Panini-FS,
/// dhātus represent the fundamental formats of knowledge representation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "UPPERCASE")]
pub enum Dhatu {
    /// Textual prose (Markdown)
    TEXT,
    
    /// Visual diagrams, photos (PNG, JPG, SVG)
    IMAGE,
    
    /// Video tutorials, demos (MP4, WebM)
    VIDEO,
    
    /// Audio podcasts, lectures (MP3, OGG)
    AUDIO,
    
    /// Code snippets (syntax-highlighted)
    CODE,
    
    /// Binary executables, PDFs
    BINARY,
    
    /// Datasets, bundles (TAR, ZIP)
    ARCHIVE,
}

impl Dhatu {
    /// Check if dhātu should be stored in Git (vs S3)
    pub fn is_git_storable(&self) -> bool {
        matches!(self, Dhatu::TEXT | Dhatu::CODE)
    }

    /// Get recommended storage backend
    pub fn storage_backend(&self) -> &'static str {
        match self {
            Dhatu::TEXT | Dhatu::CODE => "git",
            _ => "s3",
        }
    }

    /// Get MIME type pattern
    pub fn mime_pattern(&self) -> &'static str {
        match self {
            Dhatu::TEXT => "text/*",
            Dhatu::IMAGE => "image/*",
            Dhatu::VIDEO => "video/*",
            Dhatu::AUDIO => "audio/*",
            Dhatu::CODE => "text/plain",
            Dhatu::BINARY => "application/octet-stream",
            Dhatu::ARCHIVE => "application/*",
        }
    }
}

impl fmt::Display for Dhatu {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Dhatu::TEXT => write!(f, "TEXT"),
            Dhatu::IMAGE => write!(f, "IMAGE"),
            Dhatu::VIDEO => write!(f, "VIDEO"),
            Dhatu::AUDIO => write!(f, "AUDIO"),
            Dhatu::CODE => write!(f, "CODE"),
            Dhatu::BINARY => write!(f, "BINARY"),
            Dhatu::ARCHIVE => write!(f, "ARCHIVE"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dhatu_is_git_storable() {
        assert!(Dhatu::TEXT.is_git_storable());
        assert!(Dhatu::CODE.is_git_storable());
        assert!(!Dhatu::IMAGE.is_git_storable());
        assert!(!Dhatu::VIDEO.is_git_storable());
    }

    #[test]
    fn test_dhatu_storage_backend() {
        assert_eq!(Dhatu::TEXT.storage_backend(), "git");
        assert_eq!(Dhatu::IMAGE.storage_backend(), "s3");
    }

    #[test]
    fn test_dhatu_serialization() {
        let dhatu = Dhatu::TEXT;
        let json = serde_json::to_string(&dhatu).unwrap();
        assert_eq!(json, "\"TEXT\"");
        
        let deserialized: Dhatu = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized, dhatu);
    }
}
