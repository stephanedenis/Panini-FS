# Panini-FS Implementation Plan v2.0 (Git-Native)

**Status**: ✅ APPROVED  
**Version**: 2.0.0  
**Date**: 2025-10-29  
**Duration**: 9 weeks (45 days)  
**Estimated Effort**: 320-360 hours

---

## Table of Contents

1. [Overview](#1-overview)
2. [Phase Timeline](#2-phase-timeline)
3. [Phase 2.0.1: Git Core (2 weeks)](#3-phase-201-git-core-2-weeks)
4. [Phase 2.0.2: Knowledge Schema (2 weeks)](#4-phase-202-knowledge-schema-2-weeks)
5. [Phase 2.0.3: Local Index (1.5 weeks)](#5-phase-203-local-index-15-weeks)
6. [Phase 2.0.4: Sync & Collaboration (1.5 weeks)](#6-phase-204-sync--collaboration-15-weeks)
7. [Phase 2.0.5: Content Management (1 week)](#7-phase-205-content-management-1-week)
8. [Phase 2.0.6: API & CLI (1 week)](#8-phase-206-api--cli-1-week)
9. [Testing Strategy](#9-testing-strategy)
10. [Dependencies](#10-dependencies)
11. [Milestones](#11-milestones)
12. [Risk Mitigation](#12-risk-mitigation)

---

## 1. Overview

### 1.1 Project Structure

```
panini-fs/
├── Cargo.toml                 # Workspace manifest
├── .cargo/
│   └── config.toml            # Cargo configuration
├── crates/
│   ├── panini-core/           # Core library (Phase 1-5)
│   │   ├── Cargo.toml
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── git/           # Phase 2.0.1
│   │   │   ├── schema/        # Phase 2.0.2
│   │   │   ├── index/         # Phase 2.0.3
│   │   │   ├── sync/          # Phase 2.0.4
│   │   │   ├── storage/       # Phase 2.0.5
│   │   │   └── query/         # Phase 2.0.3
│   │   └── tests/
│   ├── panini-cli/            # CLI tool (Phase 2.0.6)
│   │   ├── Cargo.toml
│   │   └── src/
│   └── panini-server/         # REST API (Phase 2.0.6, optional)
│       ├── Cargo.toml
│       └── src/
├── tests/                     # Integration tests
├── benches/                   # Criterion benchmarks
├── docs/                      # Documentation
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
└── README.md
```

### 1.2 Core Dependencies

**Cargo.toml (workspace)**:
```toml
[workspace]
members = ["crates/panini-core", "crates/panini-cli", "crates/panini-server"]
resolver = "2"

[workspace.package]
version = "2.0.0"
edition = "2021"
rust-version = "1.75"
authors = ["Panini-FS Contributors"]
license = "MIT OR Apache-2.0"

[workspace.dependencies]
# Git operations
git2 = "0.18"

# Storage & indexing
rocksdb = "0.21"
tantivy = "0.21"

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
serde_yaml = "0.9"

# Markdown & parsing
pulldown-cmark = "0.9"

# Graph algorithms
petgraph = "0.6"

# Async runtime
tokio = { version = "1.35", features = ["full"] }

# HTTP/REST (server)
axum = "0.7"
tower = "0.4"
tower-http = "0.5"

# CLI
clap = { version = "4.4", features = ["derive", "cargo"] }

# Error handling
thiserror = "1.0"
anyhow = "1.0"

# Crypto
sha2 = "0.10"

# Utilities
chrono = "0.4"
uuid = { version = "1.6", features = ["v4", "serde"] }
walkdir = "2.4"
glob = "0.3"

# Testing
criterion = "0.5"
tempfile = "3.8"
pretty_assertions = "1.4"
```

### 1.3 Total Task Count

| Phase | Duration | Tasks | LOC Estimate |
|-------|----------|-------|--------------|
| 2.0.1: Git Core | 2 weeks | 12 | 2,500 |
| 2.0.2: Knowledge Schema | 2 weeks | 14 | 2,800 |
| 2.0.3: Local Index | 1.5 weeks | 10 | 2,200 |
| 2.0.4: Sync & Collaboration | 1.5 weeks | 11 | 2,000 |
| 2.0.5: Content Management | 1 week | 8 | 1,500 |
| 2.0.6: API & CLI | 1 week | 10 | 2,000 |
| **Total** | **9 weeks** | **65** | **~13,000** |

---

## 2. Phase Timeline

### 2.1 Gantt Chart (ASCII)

```
Week:        1    2    3    4    5    6    7    8    9
Phase 2.0.1: [========]
Phase 2.0.2:      [========]
Phase 2.0.3:           [======]
Phase 2.0.4:                  [======]
Phase 2.0.5:                         [====]
Phase 2.0.6:                              [====]
Testing:     [  ...  continuous  ...          ]
Docs:        [  ...  continuous  ...          ]
```

### 2.2 Milestones

| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 2 | Git Core Complete | Init, commit, clone, submodules working |
| 4 | Schema & Validation Complete | Markdown parser, YAML validation, concepts |
| 5.5 | Index Complete | RocksDB + Tantivy indexing, queries |
| 7 | Sync Complete | Pull, push, conflict resolution |
| 8 | Content Storage Complete | S3-compatible storage working |
| 9 | **v1.0 MVP** | CLI tool + REST API + docs |

---

## 3. Phase 2.0.1: Git Core (2 weeks)

**Goal**: Implement Git repository operations with git2-rs.

### 3.1 Tasks

#### T2.1.1: Project Setup (4h)
**Priority**: Critical  
**Dependencies**: None

- Create Cargo workspace
- Configure `Cargo.toml` with dependencies
- Set up directory structure
- Configure CI (GitHub Actions)
- Set up pre-commit hooks

**Acceptance Criteria**:
- ✅ `cargo build` succeeds
- ✅ `cargo test` runs (no tests yet)
- ✅ CI pipeline executes on push

**Code Example**:
```toml
# Cargo.toml (workspace root)
[workspace]
members = ["crates/panini-core", "crates/panini-cli"]
resolver = "2"

[workspace.package]
version = "2.0.0"
edition = "2021"
rust-version = "1.75"
```

---

#### T2.1.2: Repository Initialization (6h)
**Priority**: Critical  
**Dependencies**: T2.1.1

- Implement `PaniniRepo::init(path)`
- Create `.panini/` directory structure
- Write default `config.yaml`
- Initial Git commit
- Tests

**Module**: `crates/panini-core/src/git/init.rs`

**Code Example**:
```rust
use git2::Repository;
use std::path::Path;
use std::fs;

pub fn init_repo(path: &Path) -> Result<Repository, Error> {
    // Initialize Git repository
    let repo = Repository::init(path)?;
    
    // Create .panini/ structure
    fs::create_dir_all(path.join(".panini/index/rocksdb"))?;
    fs::create_dir_all(path.join(".panini/index/tantivy"))?;
    fs::create_dir_all(path.join(".panini/cache"))?;
    fs::create_dir_all(path.join("knowledge"))?;
    
    // Write default config
    let config = PaniniConfig::default();
    config.write_to_file(path.join(".panini/config.yaml"))?;
    
    // Write schema version
    let schema = SchemaVersion::v1_0();
    schema.write_to_file(path.join(".panini/schema.yaml"))?;
    
    // Create .gitignore
    fs::write(path.join(".gitignore"), GITIGNORE_TEMPLATE)?;
    
    // Initial commit
    let sig = repo.signature()?;
    let tree_id = {
        let mut index = repo.index()?;
        index.add_path(Path::new(".gitignore"))?;
        index.add_path(Path::new(".panini/config.yaml"))?;
        index.add_path(Path::new(".panini/schema.yaml"))?;
        index.write_tree()?
    };
    let tree = repo.find_tree(tree_id)?;
    
    repo.commit(
        Some("HEAD"),
        &sig,
        &sig,
        "Initial commit: Panini-FS v2.0",
        &tree,
        &[]
    )?;
    
    Ok(repo)
}

const GITIGNORE_TEMPLATE: &str = r#"
.panini/index/
.panini/cache/
*.swp
*.tmp
"#;
```

**Tests**:
```rust
#[test]
fn test_init_repo() {
    let tmp = tempfile::tempdir().unwrap();
    let repo = init_repo(tmp.path()).unwrap();
    
    assert!(tmp.path().join(".git").exists());
    assert!(tmp.path().join(".panini").exists());
    assert!(tmp.path().join(".panini/config.yaml").exists());
    
    // Verify initial commit
    let head = repo.head().unwrap();
    assert_eq!(head.shorthand(), Some("main"));
}
```

---

#### T2.1.3: Repository Opening (4h)
**Priority**: Critical  
**Dependencies**: T2.1.2

- Implement `PaniniRepo::open(path)`
- Load config and schema
- Validate schema version
- Tests

**Module**: `crates/panini-core/src/git/open.rs`

---

#### T2.1.4: Commit Operations (8h)
**Priority**: Critical  
**Dependencies**: T2.1.3

- Implement single file commit
- Implement batch commit (multiple files)
- Automatic staging
- Commit message formatting
- Tests

**Module**: `crates/panini-core/src/git/commit.rs`

**Code Example**:
```rust
pub fn commit_file(
    repo: &Repository,
    path: &Path,
    content: &[u8],
    message: &str
) -> Result<Oid, Error> {
    // Write file
    fs::write(path, content)?;
    
    // Stage file
    let mut index = repo.index()?;
    let relative_path = path.strip_prefix(repo.workdir().unwrap())?;
    index.add_path(relative_path)?;
    index.write()?;
    
    // Commit
    let sig = repo.signature()?;
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;
    let parent = repo.head()?.peel_to_commit()?;
    
    let oid = repo.commit(
        Some("HEAD"),
        &sig,
        &sig,
        message,
        &tree,
        &[&parent]
    )?;
    
    Ok(oid)
}
```

---

#### T2.1.5: Submodule Support (10h)
**Priority**: High  
**Dependencies**: T2.1.4

- Implement `add_submodule(url, path)`
- Implement `remove_submodule(path)`
- Implement `update_submodules()`
- Implement `list_submodules()`
- Tests

**Module**: `crates/panini-core/src/git/submodule.rs`

---

#### T2.1.6: Clone Operation (6h)
**Priority**: High  
**Dependencies**: T2.1.3

- Implement `clone_repo(url, path)`
- Recursive submodule cloning
- Progress callback
- Tests

**Module**: `crates/panini-core/src/git/clone.rs`

---

#### T2.1.7: Fetch & Pull (8h)
**Priority**: High  
**Dependencies**: T2.1.6

- Implement `fetch(remote_name)`
- Implement `pull(remote_name)`
- Fast-forward merge detection
- Tests

**Module**: `crates/panini-core/src/git/fetch.rs`

---

#### T2.1.8: Push Operation (6h)
**Priority**: High  
**Dependencies**: T2.1.7

- Implement `push(remote_name)`
- SSH authentication callback
- Error handling (rejected, auth)
- Tests

**Module**: `crates/panini-core/src/git/push.rs`

---

#### T2.1.9: Status & Diff (6h)
**Priority**: Medium  
**Dependencies**: T2.1.4

- Implement `status()` (like git status)
- Implement `diff()` between commits
- Changed files detection
- Tests

**Module**: `crates/panini-core/src/git/status.rs`

---

#### T2.1.10: Conflict Detection (6h)
**Priority**: High  
**Dependencies**: T2.1.7

- Implement `has_conflicts()`
- Implement `list_conflicts()`
- Parse conflict markers
- Tests

**Module**: `crates/panini-core/src/git/conflict.rs`

---

#### T2.1.11: Git History Traversal (4h)
**Priority**: Low  
**Dependencies**: T2.1.4

- Implement `log(limit)` (commit history)
- Implement `blame(file)` (line authorship)
- Tests

**Module**: `crates/panini-core/src/git/history.rs`

---

#### T2.1.12: Integration Tests (6h)
**Priority**: High  
**Dependencies**: T2.1.1-T2.1.11

- End-to-end Git workflow tests
- Submodule integration tests
- Error scenario tests

**File**: `crates/panini-core/tests/git_integration.rs`

---

### 3.2 Phase 2.0.1 Deliverables

- ✅ Git repository operations working
- ✅ Submodule support complete
- ✅ 80%+ test coverage
- ✅ Documentation (rustdoc)
- ✅ CI passing

**Estimated LOC**: 2,500

---

## 4. Phase 2.0.2: Knowledge Schema (2 weeks)

**Goal**: Implement concept/relation parsing, validation, and models.

### 4.1 Tasks

#### T2.2.1: Concept Model (6h)
**Priority**: Critical  
**Dependencies**: T2.1.2

- Define `Concept` struct
- Define `Relation` struct
- Define `ContentRef` struct
- Serde serialization
- Tests

**Module**: `crates/panini-core/src/schema/concept.rs`

**Code Example**:
```rust
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
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

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConceptType {
    Concept,
    Relation,
    Metadata,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum Dhatu {
    TEXT,
    IMAGE,
    VIDEO,
    AUDIO,
    CODE,
    BINARY,
    ARCHIVE,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Relation {
    pub rel_type: RelationType,
    pub target: String,
    pub confidence: f64,
    pub evidence: Vec<Evidence>,
    pub created: Option<DateTime<Utc>>,
    pub author: Option<String>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash)]
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

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Evidence {
    pub r#type: EvidenceType,
    pub url: Option<String>,
    pub title: Option<String>,
    pub text: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EvidenceType {
    Citation,
    Inline,
    External,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
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
```

---

#### T2.2.2: Markdown Parser (10h)
**Priority**: Critical  
**Dependencies**: T2.2.1

- Parse Markdown files with pulldown-cmark
- Extract YAML frontmatter (serde_yaml)
- Separate frontmatter from body
- Handle UTF-8 encoding
- Tests

**Module**: `crates/panini-core/src/schema/parser.rs`

**Code Example**:
```rust
use pulldown_cmark::Parser;

pub fn parse_concept_file(path: &Path) -> Result<Concept, Error> {
    let content = fs::read_to_string(path)?;
    
    // Extract YAML frontmatter
    let (frontmatter, body) = extract_frontmatter(&content)?;
    
    // Parse frontmatter
    let mut concept: Concept = serde_yaml::from_str(&frontmatter)?;
    
    // Store markdown body
    concept.markdown_body = body;
    
    Ok(concept)
}

fn extract_frontmatter(content: &str) -> Result<(String, String), Error> {
    if !content.starts_with("---\n") {
        return Err(Error::MissingFrontmatter);
    }
    
    let mut parts = content.splitn(3, "---\n");
    parts.next(); // Skip first empty part
    
    let frontmatter = parts.next().ok_or(Error::InvalidFrontmatter)?;
    let body = parts.next().ok_or(Error::InvalidFrontmatter)?;
    
    Ok((frontmatter.to_string(), body.trim().to_string()))
}
```

---

#### T2.2.3: Concept Serializer (6h)
**Priority**: Critical  
**Dependencies**: T2.2.2

- Implement `Concept::to_markdown()`
- Generate YAML frontmatter
- Combine with body
- Format correctly
- Tests

**Module**: `crates/panini-core/src/schema/serializer.rs`

---

#### T2.2.4: Validation Engine (10h)
**Priority**: Critical  
**Dependencies**: T2.2.1

- ID format validation (`concept_<category>_<number>`)
- Required fields validation
- Relation validation (types, targets)
- Content ref validation (hashes, URLs)
- Confidence range [0.0, 1.0]
- Tests

**Module**: `crates/panini-core/src/schema/validator.rs`

**Code Example**:
```rust
pub fn validate_concept(concept: &Concept) -> Result<(), Vec<ValidationError>> {
    let mut errors = Vec::new();
    
    // ID format
    let id_regex = Regex::new(r"^concept_[a-z_]+_\d+$").unwrap();
    if !id_regex.is_match(&concept.id) {
        errors.push(ValidationError::InvalidId(concept.id.clone()));
    }
    
    // Title length
    if concept.title.is_empty() || concept.title.len() > 200 {
        errors.push(ValidationError::InvalidTitle);
    }
    
    // Relations
    for relation in &concept.relations {
        // No self-reference
        if relation.target == concept.id {
            errors.push(ValidationError::SelfReference);
        }
        
        // Confidence range
        if relation.confidence < 0.0 || relation.confidence > 1.0 {
            errors.push(ValidationError::InvalidConfidence(relation.confidence));
        }
    }
    
    // Content refs
    for content_ref in &concept.content_refs {
        if !content_ref.hash.starts_with("sha256:") {
            errors.push(ValidationError::InvalidHash(content_ref.hash.clone()));
        }
        
        if content_ref.size == 0 {
            errors.push(ValidationError::InvalidSize);
        }
    }
    
    if errors.is_empty() {
        Ok(())
    } else {
        Err(errors)
    }
}
```

---

#### T2.2.5: Schema Versioning (4h)
**Priority**: Medium  
**Dependencies**: T2.2.1

- Implement `SchemaVersion` struct
- Version comparison
- Migration hooks (future)
- Tests

**Module**: `crates/panini-core/src/schema/version.rs`

---

#### T2.2.6: Relation Graph Model (8h)
**Priority**: High  
**Dependencies**: T2.2.1

- Build graph from concepts (petgraph)
- Bidirectional relation indexing
- Transitive closure computation
- Tests

**Module**: `crates/panini-core/src/schema/graph.rs`

---

#### T2.2.7: Tag Taxonomy (6h)
**Priority**: Medium  
**Dependencies**: T2.2.1

- Parse `tags.yaml`
- Hierarchical tag structure
- Tag validation
- Tests

**Module**: `crates/panini-core/src/schema/taxonomy.rs`

---

#### T2.2.8: Concept CRUD Operations (8h)
**Priority**: High  
**Dependencies**: T2.1.4, T2.2.2, T2.2.3

- `create_concept(concept)` → commit to Git
- `get_concept(id)` → read from Git
- `update_concept(concept)` → commit changes
- `delete_concept(id)` → git rm
- Tests

**Module**: `crates/panini-core/src/schema/crud.rs`

---

#### T2.2.9: Relation Operations (6h)
**Priority**: High  
**Dependencies**: T2.2.8

- `add_relation(from, to, type)`
- `remove_relation(from, to, type)`
- `get_relations(concept_id)`
- Tests

**Module**: `crates/panini-core/src/schema/relations.rs`

---

#### T2.2.10: Batch Import/Export (6h)
**Priority**: Low  
**Dependencies**: T2.2.8

- Import concepts from JSON
- Export concepts to JSON
- Export to GraphML (graph format)
- Tests

**Module**: `crates/panini-core/src/schema/import_export.rs`

---

#### T2.2.11: Pre-commit Hook Script (4h)
**Priority**: High  
**Dependencies**: T2.2.4

- Shell script for validation
- Install hook on `panini init`
- Configurable (opt-out)
- Tests

**File**: `scripts/pre-commit.sh`

---

#### T2.2.12: Uniqueness Checking (6h)
**Priority**: High  
**Dependencies**: T2.2.8

- Check concept ID uniqueness (main + submodules)
- Efficient check (index-based)
- Tests

**Module**: `crates/panini-core/src/schema/uniqueness.rs`

---

#### T2.2.13: Markdown Rendering (4h)
**Priority**: Low  
**Dependencies**: T2.2.2

- Render Markdown to HTML (for web UI)
- Syntax highlighting for code blocks
- Tests

**Module**: `crates/panini-core/src/schema/renderer.rs`

---

#### T2.2.14: Integration Tests (6h)
**Priority**: High  
**Dependencies**: T2.2.1-T2.2.13

- End-to-end schema tests
- Complex validation scenarios
- Graph traversal tests

**File**: `crates/panini-core/tests/schema_integration.rs`

---

### 4.2 Phase 2.0.2 Deliverables

- ✅ Concept model complete
- ✅ Markdown parser working
- ✅ Validation engine robust
- ✅ CRUD operations functional
- ✅ 80%+ test coverage
- ✅ Documentation

**Estimated LOC**: 2,800

---

## 5. Phase 2.0.3: Local Index (1.5 weeks)

**Goal**: Implement RocksDB + Tantivy indexing and query engine.

### 5.1 Tasks

#### T2.3.1: RocksDB Setup (6h)
**Priority**: Critical  
**Dependencies**: T2.1.2

- Open RocksDB instance
- Define column families
- Key/value schema
- Tests

**Module**: `crates/panini-core/src/index/rocksdb.rs`

---

#### T2.3.2: Index Update Logic (8h)
**Priority**: Critical  
**Dependencies**: T2.2.8, T2.3.1

- `update_index(changed_files)` implementation
- Insert concepts into RocksDB
- Update Tags CF
- Update Dhatu CF
- Update Relations CF
- Tests

**Module**: `crates/panini-core/src/index/update.rs`

---

#### T2.3.3: Tantivy Setup (6h)
**Priority**: Critical  
**Dependencies**: T2.1.2

- Initialize Tantivy index
- Define schema (id, title, content, tags, language)
- Multi-language analyzers
- Tests

**Module**: `crates/panini-core/src/index/tantivy_setup.rs`

---

#### T2.3.4: Fulltext Indexing (8h)
**Priority**: High  
**Dependencies**: T2.3.3, T2.2.2

- Index concept content in Tantivy
- Language detection (whatlang)
- Update on concept change
- Tests

**Module**: `crates/panini-core/src/index/fulltext.rs`

---

#### T2.3.5: Query Engine Core (10h)
**Priority**: Critical  
**Dependencies**: T2.3.2, T2.3.4

- Parse query DSL
- Execute filters (tag, dhatu, fulltext, relation)
- Combine results (AND logic)
- Sort by relevance
- Tests

**Module**: `crates/panini-core/src/query/engine.rs`

---

#### T2.3.6: Tag Query (4h)
**Priority**: High  
**Dependencies**: T2.3.2

- `query_by_tag(tag)` implementation
- Hierarchical tag matching
- Tests

**Module**: `crates/panini-core/src/query/tag.rs`

---

#### T2.3.7: Dhātu Query (4h)
**Priority**: High  
**Dependencies**: T2.3.2

- `query_by_dhatu(dhatu)` implementation
- Tests

**Module**: `crates/panini-core/src/query/dhatu.rs`

---

#### T2.3.8: Fulltext Query (6h)
**Priority**: High  
**Dependencies**: T2.3.4

- `query_fulltext(text, limit)` implementation
- Ranking by relevance
- Snippet extraction
- Tests

**Module**: `crates/panini-core/src/query/fulltext.rs`

---

#### T2.3.9: Relation Query (6h)
**Priority**: Medium  
**Dependencies**: T2.3.2, T2.2.6

- `query_by_relation(type, target)` implementation
- Transitive closure queries
- Tests

**Module**: `crates/panini-core/src/query/relation.rs`

---

#### T2.3.10: Index Rebuild (6h)
**Priority**: High  
**Dependencies**: T2.3.2, T2.3.4

- `rebuild_index()` implementation
- Walk entire repository
- Reindex all concepts
- Progress reporting
- Tests

**Module**: `crates/panini-core/src/index/rebuild.rs`

---

### 5.2 Phase 2.0.3 Deliverables

- ✅ RocksDB index working
- ✅ Tantivy fulltext search working
- ✅ Query engine functional
- ✅ <50ms P95 query latency
- ✅ 80%+ test coverage

**Estimated LOC**: 2,200

---

## 6. Phase 2.0.4: Sync & Collaboration (1.5 weeks)

**Goal**: Implement sync protocol, conflict resolution, and remote operations.

### 6.1 Tasks

#### T2.4.1: Sync Pull Implementation (8h)
**Priority**: Critical  
**Dependencies**: T2.1.7, T2.3.2

- `sync_pull(remote)` implementation
- Fetch + merge
- Detect changed files
- Update index incrementally
- Tests

**Module**: `crates/panini-core/src/sync/pull.rs`

---

#### T2.4.2: Sync Push Implementation (6h)
**Priority**: Critical  
**Dependencies**: T2.1.8

- `sync_push(remote)` implementation
- Check for unpushed commits
- Handle push rejection
- Tests

**Module**: `crates/panini-core/src/sync/push.rs`

---

#### T2.4.3: Full Sync Workflow (6h)
**Priority**: High  
**Dependencies**: T2.4.1, T2.4.2

- `sync()` (pull + push)
- Automatic conflict detection
- Sync result reporting
- Tests

**Module**: `crates/panini-core/src/sync/sync.rs`

---

#### T2.4.4: Conflict Resolution (Automatic) (8h)
**Priority**: Critical  
**Dependencies**: T2.1.10, T2.2.2

- Disjoint edit detection (no conflict)
- Timestamp-based wins
- YAML merge driver (custom)
- Tests

**Module**: `crates/panini-core/src/sync/conflict_auto.rs`

---

#### T2.4.5: Conflict Resolution (Manual) (6h)
**Priority**: High  
**Dependencies**: T2.4.4

- Present conflicts to user
- Accept ours/theirs/manual
- Manual edit flow
- Validate resolved file
- Tests

**Module**: `crates/panini-core/src/sync/conflict_manual.rs`

---

#### T2.4.6: Submodule Sync (6h)
**Priority**: High  
**Dependencies**: T2.1.5, T2.4.3

- Sync all submodules recursively
- Handle submodule conflicts
- Tests

**Module**: `crates/panini-core/src/sync/submodule.rs`

---

#### T2.4.7: Remote Management (4h)
**Priority**: Medium  
**Dependencies**: T2.1.3

- Add/remove remotes
- List remotes
- Set default remote
- Tests

**Module**: `crates/panini-core/src/sync/remote.rs`

---

#### T2.4.8: Sync Configuration (4h)
**Priority**: Medium  
**Dependencies**: T2.1.3

- Auto-pull on startup
- Auto-push after commit
- Sync interval
- Conflict strategy (prompt/auto/manual)
- Tests

**Module**: `crates/panini-core/src/sync/config.rs`

---

#### T2.4.9: Offline Mode (4h)
**Priority**: Low  
**Dependencies**: T2.4.3

- Detect offline state
- Queue operations
- Sync when online
- Tests

**Module**: `crates/panini-core/src/sync/offline.rs`

---

#### T2.4.10: Sync Statistics (4h)
**Priority**: Low  
**Dependencies**: T2.4.3

- Track sync history
- Report: pulled, pushed, conflicts
- Tests

**Module**: `crates/panini-core/src/sync/stats.rs`

---

#### T2.4.11: Integration Tests (6h)
**Priority**: High  
**Dependencies**: T2.4.1-T2.4.10

- Multi-user sync scenarios
- Conflict resolution tests
- Submodule sync tests

**File**: `crates/panini-core/tests/sync_integration.rs`

---

### 6.2 Phase 2.0.4 Deliverables

- ✅ Sync protocol working
- ✅ Conflict resolution (90% auto)
- ✅ Submodule sync functional
- ✅ 80%+ test coverage

**Estimated LOC**: 2,000

---

## 7. Phase 2.0.5: Content Management (1 week)

**Goal**: Implement S3-compatible storage for binary content.

### 7.1 Tasks

#### T2.5.1: Storage Backend Trait (4h)
**Priority**: Critical  
**Dependencies**: T2.2.1

- Define `StorageBackend` trait
- `upload(hash, data)` method
- `download(hash)` method
- `exists(hash)` method
- `delete(hash)` method

**Module**: `crates/panini-core/src/storage/backend.rs`

---

#### T2.5.2: S3 Backend (MinIO) (10h)
**Priority**: High  
**Dependencies**: T2.5.1

- Implement S3 backend (rusoto or aws-sdk-rust)
- Configure endpoint, bucket, credentials
- Upload/download operations
- Tests (with MinIO test server)

**Module**: `crates/panini-core/src/storage/s3.rs`

---

#### T2.5.3: Local Filesystem Backend (6h)
**Priority**: High  
**Dependencies**: T2.5.1

- Implement local file storage
- Content-addressed directory structure
- Tests

**Module**: `crates/panini-core/src/storage/local.rs`

---

#### T2.5.4: Content Hashing (4h)
**Priority**: Critical  
**Dependencies**: T2.2.1

- SHA-256 hashing utility
- Hash verification
- Tests

**Module**: `crates/panini-core/src/storage/hash.rs`

---

#### T2.5.5: Content Upload Flow (6h)
**Priority**: High  
**Dependencies**: T2.5.2, T2.5.4

- `upload_content(data, dhatu)` implementation
- Auto-select backend
- Update concept content_refs
- Tests

**Module**: `crates/panini-core/src/storage/upload.rs`

---

#### T2.5.6: Content Download Flow (4h)
**Priority**: High  
**Dependencies**: T2.5.2

- `download_content(hash)` implementation
- Verify hash after download
- Tests

**Module**: `crates/panini-core/src/storage/download.rs`

---

#### T2.5.7: Storage Configuration (4h)
**Priority**: Medium  
**Dependencies**: T2.5.1

- Define backends in `config.yaml`
- Default backend selection
- Credential management (env vars)
- Tests

**Module**: `crates/panini-core/src/storage/config.rs`

---

#### T2.5.8: Integration Tests (4h)
**Priority**: High  
**Dependencies**: T2.5.1-T2.5.7

- End-to-end content upload/download
- Multi-backend tests

**File**: `crates/panini-core/tests/storage_integration.rs`

---

### 7.2 Phase 2.0.5 Deliverables

- ✅ S3-compatible storage working
- ✅ Local storage working
- ✅ Content hashing verified
- ✅ 80%+ test coverage

**Estimated LOC**: 1,500

---

## 8. Phase 2.0.6: API & CLI (1 week)

**Goal**: Implement CLI tool and REST API (optional).

### 8.1 Tasks

#### T2.6.1: CLI Framework Setup (4h)
**Priority**: Critical  
**Dependencies**: T2.1.1

- Create `panini-cli` crate
- Configure Clap with derive macros
- Subcommand structure
- Help messages

**Module**: `crates/panini-cli/src/main.rs`

---

#### T2.6.2: CLI: Repository Commands (6h)
**Priority**: High  
**Dependencies**: T2.6.1, T2.1.2, T2.1.3

- `panini init [path]`
- `panini open <path>`
- `panini status`
- `panini config get/set`

**Module**: `crates/panini-cli/src/commands/repo.rs`

---

#### T2.6.3: CLI: Concept Commands (8h)
**Priority**: Critical  
**Dependencies**: T2.6.1, T2.2.8

- `panini concept create`
- `panini concept get <id>`
- `panini concept edit <id>`
- `panini concept delete <id>`
- `panini concept list`

**Module**: `crates/panini-cli/src/commands/concept.rs`

---

#### T2.6.4: CLI: Relation Commands (6h)
**Priority**: High  
**Dependencies**: T2.6.1, T2.2.9

- `panini relation add`
- `panini relation list`
- `panini relation delete`
- `panini relation graph`

**Module**: `crates/panini-cli/src/commands/relation.rs`

---

#### T2.6.5: CLI: Query Commands (6h)
**Priority**: Critical  
**Dependencies**: T2.6.1, T2.3.5

- `panini query <query_string>`
- `panini search <text>`

**Module**: `crates/panini-cli/src/commands/query.rs`

---

#### T2.6.6: CLI: Sync Commands (6h)
**Priority**: High  
**Dependencies**: T2.6.1, T2.4.3

- `panini sync`
- `panini sync pull`
- `panini sync push`

**Module**: `crates/panini-cli/src/commands/sync.rs`

---

#### T2.6.7: CLI: Submodule Commands (4h)
**Priority**: Medium  
**Dependencies**: T2.6.1, T2.1.5

- `panini submodule add`
- `panini submodule remove`
- `panini submodule update`
- `panini submodule list`

**Module**: `crates/panini-cli/src/commands/submodule.rs`

---

#### T2.6.8: CLI: Index Commands (4h)
**Priority**: Medium  
**Dependencies**: T2.6.1, T2.3.10

- `panini index rebuild`
- `panini index stats`
- `panini index verify`

**Module**: `crates/panini-cli/src/commands/index.rs`

---

#### T2.6.9: REST API Setup (Optional) (6h)
**Priority**: Low  
**Dependencies**: T2.1.1

- Create `panini-server` crate
- Axum router setup
- Middleware (CORS, logging)
- Tests

**Module**: `crates/panini-server/src/main.rs`

---

#### T2.6.10: REST API Endpoints (Optional) (8h)
**Priority**: Low  
**Dependencies**: T2.6.9

- Implement 15 endpoints (see specification)
- Authentication (API keys)
- Error handling
- Tests

**Module**: `crates/panini-server/src/routes.rs`

---

### 8.2 Phase 2.0.6 Deliverables

- ✅ CLI tool functional (40+ commands)
- ✅ REST API optional server
- ✅ Documentation (README, examples)
- ✅ Integration tests

**Estimated LOC**: 2,000

---

## 9. Testing Strategy

### 9.1 Unit Tests

- **Target**: 80%+ code coverage
- **Tool**: `cargo test` + `cargo tarpaulin`
- **Frequency**: On every commit (CI)

**Example**:
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_concept_validation() {
        let concept = Concept {
            id: "concept_test_001".to_string(),
            // ... other fields
        };
        assert!(validate_concept(&concept).is_ok());
    }
}
```

### 9.2 Integration Tests

- **Location**: `crates/panini-core/tests/`
- **Scope**: End-to-end workflows
- **Frequency**: On every PR

**Example**:
```rust
#[test]
fn test_full_sync_workflow() {
    let repo1 = setup_repo("repo1");
    let repo2 = setup_repo("repo2");
    
    // Create concept in repo1
    repo1.create_concept(test_concept()).unwrap();
    repo1.sync_push("origin").unwrap();
    
    // Pull in repo2
    repo2.sync_pull("origin").unwrap();
    
    // Verify concept exists
    assert!(repo2.get_concept("concept_test_001").is_ok());
}
```

### 9.3 Benchmarks

- **Tool**: Criterion
- **Metrics**: Query latency, index update time, Git operations
- **Frequency**: Weekly

**Example**:
```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_query_by_tag(c: &mut Criterion) {
    let engine = setup_engine();
    c.bench_function("query_by_tag", |b| {
        b.iter(|| engine.query_by_tag(black_box("storage/distributed")))
    });
}

criterion_group!(benches, bench_query_by_tag);
criterion_main!(benches);
```

### 9.4 Property-Based Testing

- **Tool**: proptest
- **Use Cases**: Validation, parsing, serialization

**Example**:
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn concept_roundtrip(id in "[a-z_]+_\\d+") {
        let concept = Concept { id, /* ... */ };
        let markdown = concept.to_markdown();
        let parsed = parse_concept_string(&markdown).unwrap();
        assert_eq!(concept, parsed);
    }
}
```

---

## 10. Dependencies

### 10.1 Task Dependency Graph

```
T2.1.1 (Setup)
  ├─> T2.1.2 (Init)
  │     ├─> T2.1.3 (Open)
  │     │     ├─> T2.1.4 (Commit)
  │     │     │     ├─> T2.1.5 (Submodules)
  │     │     │     ├─> T2.1.9 (Status)
  │     │     │     └─> T2.1.11 (History)
  │     │     ├─> T2.1.6 (Clone)
  │     │     │     └─> T2.1.7 (Fetch/Pull)
  │     │     │           ├─> T2.1.8 (Push)
  │     │     │           └─> T2.1.10 (Conflicts)
  │     └─> T2.2.1 (Concept Model)
  │           ├─> T2.2.2 (Parser)
  │           │     └─> T2.2.3 (Serializer)
  │           ├─> T2.2.4 (Validator)
  │           ├─> T2.2.5 (Schema Version)
  │           ├─> T2.2.6 (Graph)
  │           └─> T2.2.7 (Taxonomy)
  ├─> T2.3.1 (RocksDB)
  │     └─> T2.3.2 (Index Update)
  │           ├─> T2.3.6 (Tag Query)
  │           ├─> T2.3.7 (Dhātu Query)
  │           └─> T2.3.9 (Relation Query)
  └─> T2.3.3 (Tantivy)
        └─> T2.3.4 (Fulltext Index)
              └─> T2.3.8 (Fulltext Query)

T2.2.2 + T2.2.3 + T2.1.4 -> T2.2.8 (CRUD)
                              └─> T2.2.9 (Relations)

T2.3.2 + T2.3.4 + T2.3.6 + T2.3.7 + T2.3.8 + T2.3.9 -> T2.3.5 (Query Engine)

T2.1.7 + T2.3.2 -> T2.4.1 (Sync Pull)
T2.1.8 -> T2.4.2 (Sync Push)
T2.4.1 + T2.4.2 -> T2.4.3 (Full Sync)
T2.1.10 + T2.2.2 -> T2.4.4 (Conflict Auto)
T2.4.4 -> T2.4.5 (Conflict Manual)

T2.2.1 -> T2.5.1 (Storage Trait)
          ├─> T2.5.2 (S3)
          └─> T2.5.3 (Local)

All core -> T2.6.1-T2.6.10 (CLI/API)
```

### 10.2 Critical Path

**Critical tasks** (cannot be parallelized):
1. T2.1.1 (Setup) → T2.1.2 (Init) → T2.1.3 (Open) → T2.1.4 (Commit)
2. T2.2.1 (Concept) → T2.2.2 (Parser) → T2.2.8 (CRUD)
3. T2.3.1 (RocksDB) → T2.3.2 (Index Update) → T2.3.5 (Query Engine)
4. T2.4.3 (Sync) → T2.6.6 (CLI Sync)

**Total critical path**: ~6 weeks (can be reduced with parallelization)

---

## 11. Milestones

### M1: Git Foundation (End of Week 2)

**Deliverables**:
- ✅ Repository init/open/clone
- ✅ Commit operations
- ✅ Submodule support
- ✅ Fetch/pull/push
- ✅ Conflict detection

**Acceptance Criteria**:
- Can initialize a Panini repo
- Can add/update/remove submodules
- Can push/pull with remote
- CI passing

---

### M2: Schema & Validation (End of Week 4)

**Deliverables**:
- ✅ Concept model complete
- ✅ Markdown parser working
- ✅ Validation engine
- ✅ CRUD operations
- ✅ Relation management

**Acceptance Criteria**:
- Can create/read/update/delete concepts
- Can parse/serialize Markdown + YAML
- Validation catches all schema errors
- CI passing

---

### M3: Index & Query (End of Week 5.5)

**Deliverables**:
- ✅ RocksDB index operational
- ✅ Tantivy fulltext search
- ✅ Query engine functional
- ✅ Tag/dhātu/fulltext/relation queries

**Acceptance Criteria**:
- Queries return correct results
- Query latency <50ms P95
- Index rebuilds in <30s (10k concepts)
- CI passing

---

### M4: Sync & Collaboration (End of Week 7)

**Deliverables**:
- ✅ Sync protocol working
- ✅ Conflict resolution (90% auto)
- ✅ Submodule sync
- ✅ Remote management

**Acceptance Criteria**:
- Can sync with remote (pull + push)
- Conflicts detected and resolved
- Submodules sync correctly
- CI passing

---

### M5: Content Storage (End of Week 8)

**Deliverables**:
- ✅ S3-compatible storage
- ✅ Local storage backend
- ✅ Content upload/download
- ✅ Hash verification

**Acceptance Criteria**:
- Can upload/download binary content
- S3 backend works with MinIO
- Content hashes verified
- CI passing

---

### M6: v1.0 MVP (End of Week 9)

**Deliverables**:
- ✅ CLI tool (40+ commands)
- ✅ REST API (optional)
- ✅ Documentation (README, examples)
- ✅ CI/CD pipeline
- ✅ Release binaries

**Acceptance Criteria**:
- CLI functional and tested
- All 65 tasks complete
- 80%+ test coverage
- Documentation complete
- Performance targets met:
  - Query <50ms P95
  - Commit <100ms P95
  - Index rebuild <30s (10k concepts)
- CI passing
- Release v1.0.0 tagged

---

## 12. Risk Mitigation

### Risk 1: Git Performance with Large Repos

**Risk**: Git operations slow with 10k+ files.

**Mitigation**:
- Benchmark early (Week 2)
- Use sparse checkout if needed
- Optimize index structure
- Consider file sharding

**Contingency**: Limit v1.0 to 5k concepts, optimize in v1.5.

---

### Risk 2: Merge Conflicts Too Common

**Risk**: Users frustrated by frequent conflicts.

**Mitigation**:
- Aggressive automatic resolution (90% target)
- Custom YAML merge driver
- Clear conflict UI
- Test with realistic scenarios (Week 7)

**Contingency**: Add "lock" feature (concept editing locks).

---

### Risk 3: Tantivy Multi-Language Issues

**Risk**: Non-English fulltext search quality poor.

**Mitigation**:
- Test with French, Spanish, Chinese (Week 5)
- Use whatlang for auto-detection
- Allow manual language override

**Contingency**: English-only in v1.0, expand in v1.5.

---

### Risk 4: S3 Bandwidth Costs

**Risk**: Users hit S3 bandwidth limits.

**Mitigation**:
- Document MinIO self-hosting
- Local filesystem backend
- Recommend Cloudflare R2 (free egress)

**Contingency**: Defer large binary content to v1.5.

---

### Risk 5: Submodule Complexity

**Risk**: Users confused by submodule management.

**Mitigation**:
- Simplify with `panini submodule` commands
- Automatic submodule updates
- Clear documentation

**Contingency**: Hide submodules in CLI, expose only in advanced mode.

---

### Risk 6: Schema Evolution Breaking Changes

**Risk**: v1.1 schema incompatible with v1.0 repos.

**Mitigation**:
- Design migration system early (Week 4)
- Version schema files
- Backward compatibility where possible

**Contingency**: Manual migration guide for v1.0 → v1.1.

---

## 13. Post-MVP Roadmap

### v1.5 (4-6 weeks after v1.0)

**Features**:
- Real-time sync (WebSocket)
- Graph visualization UI
- User-extensible relation types
- Advanced conflict resolution
- Performance optimizations (100k concepts)

### v2.0 (3-6 months after v1.0)

**Features**:
- Web UI (React/Svelte)
- Mobile apps (Flutter)
- AI-powered tagging
- Community knowledge repos
- Enterprise features (SSO, audit logs)

---

**Document Status**: ✅ Complete  
**Next Steps**: Begin implementation (Phase 2.0.1: Git Core)  
**Approval**: Pending stakeholder review
