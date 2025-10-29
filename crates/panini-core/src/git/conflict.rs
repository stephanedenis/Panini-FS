//! Git conflict detection and resolution

use crate::error::{Error, Result};
use git2::{Index, IndexEntry, Repository};
use std::path::{Path, PathBuf};

/// Conflict information
#[derive(Debug, Clone)]
pub struct Conflict {
    pub path: PathBuf,
    pub ancestor: Option<ConflictEntry>,
    pub ours: Option<ConflictEntry>,
    pub theirs: Option<ConflictEntry>,
}

/// Conflict entry (one version of the conflicted file)
#[derive(Debug, Clone)]
pub struct ConflictEntry {
    pub oid: git2::Oid,
    pub mode: i32,
}

impl From<IndexEntry> for ConflictEntry {
    fn from(entry: IndexEntry) -> Self {
        Self {
            oid: entry.id,
            mode: entry.mode as i32,
        }
    }
}

/// Get all conflicts
pub fn get_conflicts(repo: &Repository) -> Result<Vec<Conflict>> {
    let index = repo.index()?;
    
    if !index.has_conflicts() {
        return Ok(Vec::new());
    }
    
    let mut conflicts = Vec::new();
    
    for conflict in index.conflicts()? {
        let conflict = conflict?;
        
        let path = if let Some(ours) = &conflict.our {
            PathBuf::from(String::from_utf8_lossy(&ours.path).to_string())
        } else if let Some(theirs) = &conflict.their {
            PathBuf::from(String::from_utf8_lossy(&theirs.path).to_string())
        } else {
            continue;
        };
        
        conflicts.push(Conflict {
            path,
            ancestor: conflict.ancestor.map(|e| e.into()),
            ours: conflict.our.map(|e| e.into()),
            theirs: conflict.their.map(|e| e.into()),
        });
    }
    
    Ok(conflicts)
}

/// Check if file has conflicts
pub fn has_conflict(repo: &Repository, path: &Path) -> Result<bool> {
    let index = repo.index()?;
    
    if !index.has_conflicts() {
        return Ok(false);
    }
    
    for conflict in index.conflicts()? {
        let conflict = conflict?;
        
        let conflict_path = if let Some(ours) = &conflict.our {
            PathBuf::from(String::from_utf8_lossy(&ours.path).to_string())
        } else if let Some(theirs) = &conflict.their {
            PathBuf::from(String::from_utf8_lossy(&theirs.path).to_string())
        } else {
            continue;
        };
        
        if conflict_path == path {
            return Ok(true);
        }
    }
    
    Ok(false)
}

/// Resolve conflict by choosing a version
pub fn resolve_conflict(
    repo: &Repository,
    path: &Path,
    resolution: ConflictResolution,
) -> Result<()> {
    let conflicts = get_conflicts(repo)?;
    
    let conflict = conflicts
        .iter()
        .find(|c| c.path == path)
        .ok_or_else(|| Error::Validation(format!("No conflict found for {:?}", path)))?;
    
    let mut index = repo.index()?;
    
    // Remove conflict entries
    index.remove_path(path)?;
    
    // Add resolved version
    match resolution {
        ConflictResolution::Ours => {
            if let Some(ours) = &conflict.ours {
                add_blob_to_index(repo, &mut index, path, ours.oid)?;
            }
        }
        ConflictResolution::Theirs => {
            if let Some(theirs) = &conflict.theirs {
                add_blob_to_index(repo, &mut index, path, theirs.oid)?;
            }
        }
        ConflictResolution::Ancestor => {
            if let Some(ancestor) = &conflict.ancestor {
                add_blob_to_index(repo, &mut index, path, ancestor.oid)?;
            }
        }
    }
    
    index.write()?;
    
    Ok(())
}

/// Add blob to index
fn add_blob_to_index(
    repo: &Repository,
    index: &mut Index,
    path: &Path,
    oid: git2::Oid,
) -> Result<()> {
    let blob = repo.find_blob(oid)?;
    let repo_root = repo.workdir().ok_or_else(|| {
        Error::Git(git2::Error::from_str("No working directory"))
    })?;
    
    // Write blob to working directory
    let full_path = repo_root.join(path);
    if let Some(parent) = full_path.parent() {
        std::fs::create_dir_all(parent)?;
    }
    std::fs::write(&full_path, blob.content())?;
    
    // Add to index
    index.add_path(path)?;
    
    Ok(())
}

/// Conflict resolution strategy
#[derive(Debug, Clone, Copy)]
pub enum ConflictResolution {
    /// Use local version
    Ours,
    /// Use remote version
    Theirs,
    /// Use common ancestor version
    Ancestor,
}

/// Auto-resolve all conflicts using strategy
pub fn auto_resolve_conflicts(
    repo: &Repository,
    strategy: ConflictResolution,
) -> Result<Vec<PathBuf>> {
    let conflicts = get_conflicts(repo)?;
    let mut resolved = Vec::new();
    
    for conflict in conflicts {
        resolve_conflict(repo, &conflict.path, strategy)?;
        resolved.push(conflict.path);
    }
    
    Ok(resolved)
}

/// Detect YAML frontmatter conflicts (specialized for Panini)
pub fn detect_yaml_conflicts(conflicts: &[Conflict]) -> Vec<&Conflict> {
    conflicts
        .iter()
        .filter(|c| {
            c.path
                .extension()
                .and_then(|e| e.to_str())
                .map(|e| e == "md" || e == "yaml" || e == "yml")
                .unwrap_or(false)
        })
        .collect()
}

/// Analyze conflict complexity
pub fn analyze_conflict(conflict: &Conflict) -> ConflictComplexity {
    match (&conflict.ours, &conflict.theirs, &conflict.ancestor) {
        (Some(_), Some(_), Some(_)) => ConflictComplexity::ThreeWay,
        (Some(_), Some(_), None) => ConflictComplexity::TwoWay,
        (Some(_), None, _) => ConflictComplexity::Deletion,
        (None, Some(_), _) => ConflictComplexity::Addition,
        (None, None, _) => ConflictComplexity::Unknown,
    }
}

/// Conflict complexity
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConflictComplexity {
    /// Three-way merge conflict
    ThreeWay,
    /// Two-way conflict (no ancestor)
    TwoWay,
    /// Deletion conflict
    Deletion,
    /// Addition conflict
    Addition,
    /// Unknown
    Unknown,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use tempfile::TempDir;
    
    #[test]
    fn test_get_conflicts_empty() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let conflicts = get_conflicts(&repo).unwrap();
        assert!(conflicts.is_empty());
    }
    
    #[test]
    fn test_has_conflict_false() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let has_conflict = has_conflict(&repo, Path::new("test.md")).unwrap();
        assert!(!has_conflict);
    }
    
    #[test]
    fn test_conflict_resolution_variants() {
        let resolutions = vec![
            ConflictResolution::Ours,
            ConflictResolution::Theirs,
            ConflictResolution::Ancestor,
        ];
        
        assert_eq!(resolutions.len(), 3);
    }
    
    #[test]
    fn test_conflict_complexity() {
        let conflict = Conflict {
            path: PathBuf::from("test.md"),
            ancestor: Some(ConflictEntry {
                oid: git2::Oid::zero(),
                mode: 0o100644,
            }),
            ours: Some(ConflictEntry {
                oid: git2::Oid::zero(),
                mode: 0o100644,
            }),
            theirs: Some(ConflictEntry {
                oid: git2::Oid::zero(),
                mode: 0o100644,
            }),
        };
        
        assert_eq!(analyze_conflict(&conflict), ConflictComplexity::ThreeWay);
    }
    
    #[test]
    fn test_detect_yaml_conflicts() {
        let conflicts = vec![
            Conflict {
                path: PathBuf::from("test.md"),
                ancestor: None,
                ours: None,
                theirs: None,
            },
            Conflict {
                path: PathBuf::from("config.yaml"),
                ancestor: None,
                ours: None,
                theirs: None,
            },
            Conflict {
                path: PathBuf::from("image.png"),
                ancestor: None,
                ours: None,
                theirs: None,
            },
        ];
        
        let yaml_conflicts = detect_yaml_conflicts(&conflicts);
        assert_eq!(yaml_conflicts.len(), 2);
    }
}
