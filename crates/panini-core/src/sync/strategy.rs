//! Sync strategies

use serde::{Deserialize, Serialize};

/// Conflict resolution strategy
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SyncStrategy {
    /// Auto-resolve all conflicts (90% target)
    AutoResolve,
    
    /// Prompt for manual resolution
    Manual,
    
    /// Take ours (local version)
    Ours,
    
    /// Take theirs (remote version)
    Theirs,
    
    /// Merge with union (tags, relations)
    Union,
    
    /// Prefer newer (by timestamp)
    PreferNewer,
}

impl Default for SyncStrategy {
    fn default() -> Self {
        Self::AutoResolve
    }
}

impl SyncStrategy {
    /// Check if strategy is automatic
    pub fn is_automatic(&self) -> bool {
        !matches!(self, Self::Manual)
    }
    
    /// Get description
    pub fn description(&self) -> &'static str {
        match self {
            Self::AutoResolve => "Automatically resolve conflicts using smart merge",
            Self::Manual => "Prompt for manual resolution",
            Self::Ours => "Always take local version",
            Self::Theirs => "Always take remote version",
            Self::Union => "Merge by taking union of all changes",
            Self::PreferNewer => "Prefer version with newer timestamp",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_default_strategy() {
        let strategy = SyncStrategy::default();
        assert_eq!(strategy, SyncStrategy::AutoResolve);
        assert!(strategy.is_automatic());
    }
    
    #[test]
    fn test_manual_strategy() {
        let strategy = SyncStrategy::Manual;
        assert!(!strategy.is_automatic());
    }
}
