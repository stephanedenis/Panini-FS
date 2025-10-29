//! Git history traversal and commit information

use crate::error::{Error, Result};
use git2::{Commit, Oid, Repository, Revwalk, Sort};
use std::collections::HashMap;

/// Commit information
#[derive(Debug, Clone)]
pub struct CommitInfo {
    pub oid: String,
    pub author: String,
    pub email: String,
    pub message: String,
    pub timestamp: i64,
    pub parent_oids: Vec<String>,
}

impl<'repo> From<Commit<'repo>> for CommitInfo {
    fn from(commit: Commit) -> Self {
        let author = commit.author();
        
        Self {
            oid: commit.id().to_string(),
            author: author.name().unwrap_or("Unknown").to_string(),
            email: author.email().unwrap_or("unknown@localhost").to_string(),
            message: commit.message().unwrap_or("").to_string(),
            timestamp: commit.time().seconds(),
            parent_oids: commit.parent_ids().map(|id| id.to_string()).collect(),
        }
    }
}

/// Get commit history
pub fn history(repo: &Repository, max_count: Option<usize>) -> Result<Vec<CommitInfo>> {
    let mut revwalk = repo.revwalk()?;
    revwalk.set_sorting(Sort::TIME)?;
    revwalk.push_head()?;
    
    let mut commits = Vec::new();
    let limit = max_count.unwrap_or(usize::MAX);
    
    for (i, oid) in revwalk.enumerate() {
        if i >= limit {
            break;
        }
        
        let oid = oid?;
        let commit = repo.find_commit(oid)?;
        commits.push(commit.into());
    }
    
    Ok(commits)
}

/// Get commit by ID
pub fn get_commit(repo: &Repository, oid: &str) -> Result<CommitInfo> {
    let oid = Oid::from_str(oid)?;
    let commit = repo.find_commit(oid)?;
    Ok(commit.into())
}

/// Get file history
pub fn file_history(repo: &Repository, path: &str, max_count: Option<usize>) -> Result<Vec<CommitInfo>> {
    let mut revwalk = repo.revwalk()?;
    revwalk.set_sorting(Sort::TIME)?;
    revwalk.push_head()?;
    
    let mut commits = Vec::new();
    let limit = max_count.unwrap_or(usize::MAX);
    
    for oid in revwalk {
        if commits.len() >= limit {
            break;
        }
        
        let oid = oid?;
        let commit = repo.find_commit(oid)?;
        
        // Check if commit touches the file
        if commit_touches_file(repo, &commit, path)? {
            commits.push(commit.into());
        }
    }
    
    Ok(commits)
}

/// Check if commit touches file
fn commit_touches_file(repo: &Repository, commit: &Commit, path: &str) -> Result<bool> {
    let tree = commit.tree()?;
    
    // Check if file exists in this commit
    let file_exists = tree.get_path(std::path::Path::new(path)).is_ok();
    
    if commit.parent_count() == 0 {
        // First commit
        return Ok(file_exists);
    }
    
    // Compare with parent
    let parent = commit.parent(0)?;
    let parent_tree = parent.tree()?;
    
    let diff = repo.diff_tree_to_tree(Some(&parent_tree), Some(&tree), None)?;
    
    for delta in diff.deltas() {
        let old_path = delta.old_file().path().map(|p| p.to_string_lossy());
        let new_path = delta.new_file().path().map(|p| p.to_string_lossy());
        
        if old_path.as_deref() == Some(path) || new_path.as_deref() == Some(path) {
            return Ok(true);
        }
    }
    
    Ok(false)
}

/// Get commits between two refs
pub fn commits_between(repo: &Repository, from: &str, to: &str) -> Result<Vec<CommitInfo>> {
    let from_oid = repo.revparse_single(from)?.id();
    let to_oid = repo.revparse_single(to)?.id();
    
    let mut revwalk = repo.revwalk()?;
    revwalk.set_sorting(Sort::TIME)?;
    revwalk.push(to_oid)?;
    revwalk.hide(from_oid)?;
    
    let mut commits = Vec::new();
    
    for oid in revwalk {
        let oid = oid?;
        let commit = repo.find_commit(oid)?;
        commits.push(commit.into());
    }
    
    Ok(commits)
}

/// Get branches containing commit
pub fn branches_containing(repo: &Repository, oid: &str) -> Result<Vec<String>> {
    let oid = Oid::from_str(oid)?;
    let mut branches = Vec::new();
    
    for branch in repo.branches(Some(git2::BranchType::Local))? {
        let (branch, _) = branch?;
        
        if let Some(branch_oid) = branch.get().target() {
            // Check if commit is ancestor of branch
            if repo.graph_descendant_of(branch_oid, oid)? || branch_oid == oid {
                if let Some(name) = branch.name()? {
                    branches.push(name.to_string());
                }
            }
        }
    }
    
    Ok(branches)
}

/// Get common ancestor of two commits
pub fn merge_base(repo: &Repository, one: &str, two: &str) -> Result<String> {
    let one_oid = repo.revparse_single(one)?.id();
    let two_oid = repo.revparse_single(two)?.id();
    
    let base_oid = repo.merge_base(one_oid, two_oid)?;
    
    Ok(base_oid.to_string())
}

/// Get commit graph statistics
pub fn graph_stats(repo: &Repository) -> Result<GraphStats> {
    let mut revwalk = repo.revwalk()?;
    revwalk.push_head()?;
    
    let mut total_commits = 0;
    let mut authors = HashMap::new();
    let mut merge_commits = 0;
    
    for oid in revwalk {
        total_commits += 1;
        let oid = oid?;
        let commit = repo.find_commit(oid)?;
        
        if commit.parent_count() > 1 {
            merge_commits += 1;
        }
        
        let author = commit.author().name().unwrap_or("Unknown").to_string();
        *authors.entry(author).or_insert(0) += 1;
    }
    
    Ok(GraphStats {
        total_commits,
        merge_commits,
        unique_authors: authors.len(),
        author_commits: authors,
    })
}

/// Graph statistics
#[derive(Debug, Clone)]
pub struct GraphStats {
    pub total_commits: usize,
    pub merge_commits: usize,
    pub unique_authors: usize,
    pub author_commits: HashMap<String, usize>,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use tempfile::TempDir;
    use std::fs;
    
    #[test]
    fn test_history() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let commits = history(&repo, None).unwrap();
        
        assert_eq!(commits.len(), 1); // Initial commit
        assert!(commits[0].message.contains("Initialize"));
    }
    
    #[test]
    fn test_history_limit() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let commits = history(&repo, Some(5)).unwrap();
        
        assert!(commits.len() <= 5);
    }
    
    #[test]
    fn test_get_commit() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let commits = history(&repo, None).unwrap();
        let first_oid = &commits[0].oid;
        
        let commit = get_commit(&repo, first_oid).unwrap();
        
        assert_eq!(commit.oid, *first_oid);
    }
    
    #[test]
    fn test_file_history() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let commits = file_history(&repo, "README.md", None).unwrap();
        
        assert_eq!(commits.len(), 1); // README created in init
    }
    
    #[test]
    fn test_graph_stats() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let stats = graph_stats(&repo).unwrap();
        
        assert_eq!(stats.total_commits, 1);
        assert_eq!(stats.merge_commits, 0);
        assert_eq!(stats.unique_authors, 1);
    }
    
    #[test]
    fn test_branches_containing() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let commits = history(&repo, None).unwrap();
        let oid = &commits[0].oid;
        
        let branches = branches_containing(&repo, oid).unwrap();
        
        assert!(!branches.is_empty());
    }
}
