//! Git fetch, pull, and push operations

use crate::error::{Error, Result};
use git2::{AnnotatedCommit, FetchOptions, PushOptions, Repository};

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

/// Push to remote
pub fn push(
    repo: &Repository,
    remote_name: &str,
    refspecs: &[&str],
) -> Result<()> {
    let mut remote = repo.find_remote(remote_name)?;
    
    let mut push_opts = PushOptions::new();
    
    // Push
    remote.push(refspecs, Some(&mut push_opts))?;
    
    Ok(())
}

/// Push current branch to remote
pub fn push_current_branch(repo: &Repository, remote_name: &str) -> Result<()> {
    // Get current branch
    let head = repo.head()?;
    
    let branch_name = head.shorthand().ok_or_else(|| {
        Error::Git(git2::Error::from_str("Cannot get branch name"))
    })?;
    
    // Push with refspec
    let refspec = format!("refs/heads/{}:refs/heads/{}", branch_name, branch_name);
    push(repo, remote_name, &[&refspec])
}

/// Push all branches
pub fn push_all_branches(repo: &Repository, remote_name: &str) -> Result<Vec<String>> {
    let mut pushed = Vec::new();
    
    // Get all local branches
    for branch in repo.branches(Some(git2::BranchType::Local))? {
        let (branch, _) = branch?;
        
        if let Some(name) = branch.name()? {
            let refspec = format!("refs/heads/{}:refs/heads/{}", name, name);
            
            match push(repo, remote_name, &[&refspec]) {
                Ok(_) => pushed.push(name.to_string()),
                Err(_) => continue, // Skip failed pushes
            }
        }
    }
    
    Ok(pushed)
}

/// Push with tags
pub fn push_with_tags(repo: &Repository, remote_name: &str) -> Result<()> {
    // Push current branch
    push_current_branch(repo, remote_name)?;
    
    // Push all tags
    let mut remote = repo.find_remote(remote_name)?;
    let mut push_opts = PushOptions::new();
    
    remote.push(&["refs/tags/*:refs/tags/*"], Some(&mut push_opts))?;
    
    Ok(())
}

/// Force push (dangerous!)
pub fn force_push(
    repo: &Repository,
    remote_name: &str,
    branch: &str,
) -> Result<()> {
    let refspec = format!("+refs/heads/{}:refs/heads/{}", branch, branch);
    push(repo, remote_name, &[&refspec])
}

/// Push result
#[derive(Debug, Clone, PartialEq)]
pub enum PushResult {
    /// Successfully pushed
    Success,
    /// Nothing to push
    UpToDate,
    /// Rejected (non-fast-forward)
    Rejected,
}

/// Push with status check
pub fn push_with_status(
    repo: &Repository,
    remote_name: &str,
    branch: &str,
) -> Result<PushResult> {
    // Get current commit
    let head = repo.head()?;
    let local_commit = head.peel_to_commit()?;
    
    // Try to get remote commit
    let remote_ref = format!("refs/remotes/{}/{}", remote_name, branch);
    let remote_commit_result = repo.find_reference(&remote_ref)
        .and_then(|r| r.peel_to_commit());
    
    match remote_commit_result {
        Ok(remote_commit) => {
            if local_commit.id() == remote_commit.id() {
                return Ok(PushResult::UpToDate);
            }
            
            // Check if local is ahead
            let is_descendant = repo.graph_descendant_of(
                local_commit.id(),
                remote_commit.id()
            )?;
            
            if !is_descendant {
                return Ok(PushResult::Rejected);
            }
        }
        Err(_) => {
            // Remote ref doesn't exist, first push
        }
    }
    
    // Perform push
    let refspec = format!("refs/heads/{}:refs/heads/{}", branch, branch);
    push(repo, remote_name, &[&refspec])?;
    
    Ok(PushResult::Success)
}

#[cfg(test)]
mod push_tests {
    use super::*;
    use crate::git::init::init_repo;
    use tempfile::TempDir;
    
    #[test]
    fn test_push_no_remote() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = push(&repo, "origin", &["refs/heads/main:refs/heads/main"]);
        assert!(result.is_err());
    }
    
    #[test]
    fn test_push_current_branch_no_remote() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = push_current_branch(&repo, "origin");
        assert!(result.is_err());
    }
    
    #[test]
    fn test_push_all_branches_no_remote() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = push_all_branches(&repo, "origin");
        
        // Should return empty vec (no remotes)
        assert!(result.is_ok());
        assert!(result.unwrap().is_empty());
    }
    
    #[test]
    fn test_push_result_variants() {
        let results = vec![
            PushResult::Success,
            PushResult::UpToDate,
            PushResult::Rejected,
        ];
        
        assert_eq!(results.len(), 3);
    }
    
    #[test]
    fn test_force_push_no_remote() {
        let tmp = TempDir::new().unwrap();
        let repo = init_repo(tmp.path()).unwrap();
        
        let result = force_push(&repo, "origin", "main");
        assert!(result.is_err());
    }
}
