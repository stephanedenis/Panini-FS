//! Git fetch and pull operations

use crate::error::{Error, Result};
use git2::{AnnotatedCommit, FetchOptions, Repository};

/// Fetch from remote
pub fn fetch(
    repo: &Repository,
    remote_name: &str,
    refspecs: &[&str],
) -> Result<()> {
    let mut remote = repo.find_remote(remote_name)?;
    
    let mut fetch_opts = FetchOptions::new();
    
    // Fetch
    remote.fetch(refspecs, Some(&mut fetch_opts), None)?;
    
    Ok(())
}

/// Fetch all remotes
pub fn fetch_all(repo: &Repository) -> Result<Vec<String>> {
    let mut fetched = Vec::new();
    
    for remote_name in repo.remotes()?.iter() {
        if let Some(name) = remote_name {
            let mut remote = repo.find_remote(name)?;
            let mut fetch_opts = FetchOptions::new();
            
            // Fetch with default refspecs
            remote.fetch(&[] as &[&str], Some(&mut fetch_opts), None)?;
            fetched.push(name.to_string());
        }
    }
    
    Ok(fetched)
}

/// Pull (fetch + merge)
pub fn pull(repo: &Repository, remote_name: &str, branch: &str) -> Result<()> {
    // Fetch
    fetch(repo, remote_name, &[branch])?;
    
    // Get fetch head
    let fetch_head = repo.find_reference("FETCH_HEAD")?;
    let fetch_commit = repo.reference_to_annotated_commit(&fetch_head)?;
    
    // Perform merge analysis
    let analysis = repo.merge_analysis(&[&fetch_commit])?;
    
    if analysis.0.is_up_to_date() {
        // Already up to date
        return Ok(());
    } else if analysis.0.is_fast_forward() {
        // Fast-forward merge
        fast_forward(repo, branch, &fetch_commit)?;
    } else {
        // Normal merge required
        normal_merge(repo, &fetch_commit)?;
    }
    
    Ok(())
}

/// Fast-forward merge
fn fast_forward(
    repo: &Repository,
    branch: &str,
    fetch_commit: &AnnotatedCommit,
) -> Result<()> {
    let refname = format!("refs/heads/{}", branch);
    
    // Update reference
    let mut reference = repo.find_reference(&refname)?;
    reference.set_target(fetch_commit.id(), "Fast-forward")?;
    
    // Update HEAD
    repo.set_head(&refname)?;
    
    // Checkout
    repo.checkout_head(Some(git2::build::CheckoutBuilder::default().force()))?;
    
    Ok(())
}

/// Normal merge (creates merge commit)
fn normal_merge(repo: &Repository, fetch_commit: &AnnotatedCommit) -> Result<()> {
    // Get HEAD commit
    let head = repo.head()?;
    let head_commit = head.peel_to_commit()?;
    
    // Perform merge
    let mut merge_opts = git2::MergeOptions::new();
    let mut checkout_opts = git2::build::CheckoutBuilder::new();
    checkout_opts.force();
    
    repo.merge(
        &[fetch_commit],
        Some(&mut merge_opts),
        Some(&mut checkout_opts),
    )?;
    
    // Check for conflicts
    if repo.index()?.has_conflicts() {
        return Err(Error::MergeConflict(
            "Merge resulted in conflicts. Please resolve manually.".to_string()
        ));
    }
    
    // Create merge commit
    let mut index = repo.index()?;
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;
    
    let sig = git2::Signature::now("Panini", "panini@localhost")?;
    
    let message = format!(
        "Merge remote tracking branch\n\nMerge commit {}",
        fetch_commit.id()
    );
    
    repo.commit(
        Some("HEAD"),
        &sig,
        &sig,
        &message,
        &tree,
        &[&head_commit, &fetch_commit.into_commit()],
    )?;
    
    // Cleanup merge state
    repo.cleanup_state()?;
    
    Ok(())
}

/// Pull with automatic conflict resolution
pub fn pull_with_strategy(
    repo: &Repository,
    remote_name: &str,
    branch: &str,
    strategy: ConflictStrategy,
) -> Result<PullResult> {
    // Fetch first
    fetch(repo, remote_name, &[branch])?;
    
    let fetch_head = repo.find_reference("FETCH_HEAD")?;
    let fetch_commit = repo.reference_to_annotated_commit(&fetch_head)?;
    
    let analysis = repo.merge_analysis(&[&fetch_commit])?;
    
    if analysis.0.is_up_to_date() {
        return Ok(PullResult::UpToDate);
    } else if analysis.0.is_fast_forward() {
        fast_forward(repo, branch, &fetch_commit)?;
        return Ok(PullResult::FastForward);
    }
    
    // Try normal merge
    let merge_result = normal_merge(repo, &fetch_commit);
    
    match merge_result {
        Ok(_) => Ok(PullResult::Merged),
        Err(Error::MergeConflict(_)) => {
            match strategy {
                ConflictStrategy::Prompt => Ok(PullResult::Conflict),
                ConflictStrategy::Ours => {
                    // Resolve with ours
                    repo.checkout_head(Some(
                        git2::build::CheckoutBuilder::default()
                            .force()
                            .use_ours(true)
                    ))?;
                    Ok(PullResult::ResolvedOurs)
                }
                ConflictStrategy::Theirs => {
                    // Resolve with theirs
                    repo.checkout_head(Some(
                        git2::build::CheckoutBuilder::default()
                            .force()
                            .use_theirs(true)
                    ))?;
                    Ok(PullResult::ResolvedTheirs)
                }
            }
        }
        Err(e) => Err(e),
    }
}

/// Conflict resolution strategy
#[derive(Debug, Clone, Copy)]
pub enum ConflictStrategy {
    /// Prompt user for resolution
    Prompt,
    /// Use local version
    Ours,
    /// Use remote version
    Theirs,
}

/// Pull result
#[derive(Debug, Clone, PartialEq)]
pub enum PullResult {
    /// Already up to date
    UpToDate,
    /// Fast-forward merge
    FastForward,
    /// Merge commit created
    Merged,
    /// Conflicts detected
    Conflict,
    /// Resolved with ours
    ResolvedOurs,
    /// Resolved with theirs
    ResolvedTheirs,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::git::init::init_repo;
    use std::fs;
    use tempfile::TempDir;
    
    #[test]
    fn test_fetch_nonexistent_remote() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = fetch(&repo, "nonexistent", &["main"]);
        assert!(result.is_err());
    }
    
    #[test]
    fn test_fetch_all_empty() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = fetch_all(&repo).unwrap();
        assert!(result.is_empty());
    }
    
    #[test]
    fn test_pull_no_remote() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = pull(&repo, "origin", "main");
        assert!(result.is_err());
    }
    
    #[test]
    fn test_conflict_strategy_variants() {
        let strategies = vec![
            ConflictStrategy::Prompt,
            ConflictStrategy::Ours,
            ConflictStrategy::Theirs,
        ];
        
        assert_eq!(strategies.len(), 3);
    }
    
    #[test]
    fn test_pull_result_variants() {
        let results = vec![
            PullResult::UpToDate,
            PullResult::FastForward,
            PullResult::Merged,
            PullResult::Conflict,
            PullResult::ResolvedOurs,
            PullResult::ResolvedTheirs,
        ];
        
        assert_eq!(results.len(), 6);
    }
}
