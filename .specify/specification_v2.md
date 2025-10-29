# Panini-FS Specification v2.0 (Git-Native Architecture)

**Status**: ✅ APPROVED  
**Version**: 2.0.0  
**Date**: 2025-10-29  
**Supersedes**: specification.md v1.0 (RocksDB-based)

---

## Table of Contents

1. [Overview](#1-overview)
2. [File Formats](#2-file-formats)
3. [Repository Structure](#3-repository-structure)
4. [Knowledge Schema](#4-knowledge-schema)
5. [Git Operations](#5-git-operations)
6. [Local Index](#6-local-index)
7. [Query Language](#7-query-language)
8. [API Specifications](#8-api-specifications)
9. [CLI Commands](#9-cli-commands)
10. [Sync Protocol](#10-sync-protocol)
11. [Validation Rules](#11-validation-rules)
12. [Performance Targets](#12-performance-targets)

---

## 1. Overview

### 1.1 Architecture

Panini-FS v2.0 is a **Git-native distributed knowledge graph** system.

**Core Components**:

```
┌─────────────────────────────────────────────────────────┐
│                     User Application                     │
│              (CLI / REST API / Library)                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                  Panini Core (Rust)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Git Ops    │  │  Knowledge   │  │    Query     │  │
│  │  (git2-rs)   │  │   Manager    │  │   Engine     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Parser     │  │  Validator   │  │    Sync      │  │
│  │ (Markdown)   │  │   (Schema)   │  │  (Push/Pull) │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└───────────────────┬─────────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│  Local Index     │  │  Git Repository  │
│  (RocksDB +      │  │  (.git/ +        │
│   Tantivy)       │  │   .panini/)      │
└──────────────────┘  └──────────────────┘
         │                     │
         │                     ▼
         │            ┌──────────────────┐
         │            │  Remote Repos    │
         │            │  (GitHub/GitLab) │
         │            └──────────────────┘
         │                     │
         └─────────────────────┴─── S3-Compatible Storage
                                     (Binary Content)
```

### 1.2 Data Flow

**Concept Creation**:
1. User writes Markdown + YAML frontmatter
2. Parser validates schema
3. Git commit (atomic update)
4. Index update (RocksDB + Tantivy)
5. Optional: Push to remote

**Query Execution**:
1. User submits query (tags, dhātu, fulltext)
2. Query engine checks index first (fast path)
3. Fallback to Git if index stale
4. Return results with metadata

**Sync Operation**:
1. Git pull from remote
2. Detect changed files
3. Reindex changed concepts
4. Resolve conflicts (if any)
5. Git push local changes

---

## 2. File Formats

### 2.1 Concept File (Markdown + YAML)

**Path**: `knowledge/{category}/{concept_id}.md`

**Structure**:
```markdown
---
id: concept_cas_001
type: concept
dhatu: TEXT
title: Content-Addressable Storage
tags: [storage, distributed, hashing]
created: 2025-10-29T10:00:00Z
updated: 2025-10-29T14:30:00Z
author: stephane@example.com
relations:
  - type: is_a
    target: concept_storage_002
    confidence: 1.0
  - type: used_by
    target: concept_git_003
    confidence: 0.9
content_refs:
  - hash: sha256:abc123def456...
    type: IMAGE
    size: 2457600
    mime: image/png
    storage: s3://mybucket/content/abc123def456.png
    description: "CAS architecture diagram"
metadata:
  language: en
  status: published
  version: 2
---

# Content-Addressable Storage

## Definition

Content-addressable storage (CAS) is a mechanism for storing information that can be retrieved based on its content, not its location.

## Key Properties

- **Immutability**: Content cannot change without changing its address
- **Deduplication**: Identical content stored once
- **Integrity**: Hash verifies content authenticity

## Examples

- Git object store
- IPFS
- Docker image layers

## Implementation

```rust
use sha2::{Sha256, Digest};

fn store_content(data: &[u8]) -> String {
    let hash = Sha256::digest(data);
    format!("{:x}", hash)
}
```

## References

- [Wikipedia: Content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
- [IPFS Docs](https://docs.ipfs.io/)
```

### 2.2 YAML Frontmatter Schema

**Required Fields**:
```yaml
id: string              # Unique identifier (concept_<category>_<number>)
type: concept | relation | metadata
dhatu: TEXT | IMAGE | VIDEO | AUDIO | CODE | BINARY | ARCHIVE
title: string           # Human-readable title
```

**Optional Fields**:
```yaml
tags: string[]          # Hierarchical tags (e.g., "storage/distributed")
created: datetime       # ISO 8601 format
updated: datetime       # ISO 8601 format
author: string          # Email or identifier
relations: Relation[]   # See section 2.3
content_refs: ContentRef[]  # External content (see section 2.4)
metadata:               # Custom key-value pairs
  language: string      # ISO 639-1 code (en, fr, es, etc.)
  status: draft | published | archived
  version: integer
  confidence: float     # 0.0 - 1.0
```

### 2.3 Relation Schema

**Fixed Relation Types** (v1.0):

| Type | Description | Example |
|------|-------------|---------|
| `is_a` | Taxonomy (subclass) | "Docker is_a container_runtime" |
| `part_of` | Composition | "Wheel part_of Car" |
| `causes` | Causality | "Rain causes Flood" |
| `contradicts` | Logical negation | "Fact_A contradicts Fact_B" |
| `supports` | Evidence | "Study_X supports Theory_Y" |
| `derives_from` | Derivation | "Calculus derives_from Algebra" |
| `used_by` | Usage | "React used_by Web_Development" |
| `related_to` | Generic link | "AI related_to Machine_Learning" |

**Relation Format** (in frontmatter):
```yaml
relations:
  - type: is_a               # Required: one of 8 types
    target: concept_id       # Required: target concept ID
    confidence: 0.95         # Optional: 0.0 - 1.0 (default 1.0)
    evidence:                # Optional: supporting evidence
      - type: citation
        url: https://example.com/paper.pdf
        title: "Research Paper"
      - type: inline
        text: "As stated in section 3..."
    created: 2025-10-29T10:00:00Z
    author: user@example.com
```

**Bidirectional Relations**: Automatically created in index.

Example: If `A` has `is_a` → `B`, then `B` implicitly has `has_subclass` ← `A`.

### 2.4 Content References (S3-Compatible)

**For large binary content** (images, videos, archives):

```yaml
content_refs:
  - hash: sha256:abc123...      # Content address (SHA-256)
    type: IMAGE                 # Dhātu type
    size: 2457600               # Bytes
    mime: image/png             # MIME type
    storage: s3://mybucket/content/abc123.png  # Storage URL
    description: "Architecture diagram"
    created: 2025-10-29T10:00:00Z
    thumbnail: sha256:def456... # Optional: smaller version
```

**Supported Storage Backends**:
- `s3://` - AWS S3
- `minio://` - Self-hosted MinIO
- `r2://` - Cloudflare R2
- `b2://` - Backblaze B2
- `file://` - Local filesystem (for offline use)

**Storage Configuration** (`.panini/config.yaml`):
```yaml
storage:
  default: minio
  backends:
    minio:
      endpoint: http://localhost:9000
      bucket: panini-content
      access_key: ${MINIO_ACCESS_KEY}  # From environment
      secret_key: ${MINIO_SECRET_KEY}
    s3:
      region: us-east-1
      bucket: my-knowledge-content
      access_key: ${AWS_ACCESS_KEY_ID}
      secret_key: ${AWS_SECRET_ACCESS_KEY}
```

### 2.5 Relation File (Standalone YAML)

**Path**: `knowledge/.relations/{relation_id}.yaml`

**Use Case**: Bulk relations not tied to single concept.

```yaml
id: rel_batch_001
type: relation_batch
created: 2025-10-29T10:00:00Z
author: stephane@example.com
relations:
  - from: concept_cas_001
    to: concept_storage_002
    type: is_a
    confidence: 1.0
  - from: concept_cas_001
    to: concept_git_003
    type: used_by
    confidence: 0.9
  - from: concept_ipfs_004
    to: concept_cas_001
    type: is_a
    confidence: 0.95
```

**Index Behavior**: Relations merged into graph index.

### 2.6 Tag Taxonomy (Optional)

**Path**: `knowledge/.metadata/tags.yaml`

**Hierarchical Tags**:
```yaml
taxonomy:
  - id: storage
    label: Storage Systems
    description: Data persistence and retrieval
    children:
      - id: storage/distributed
        label: Distributed Storage
        children:
          - id: storage/distributed/cas
            label: Content-Addressable Storage
      - id: storage/databases
        label: Database Systems
        children:
          - id: storage/databases/nosql
            label: NoSQL Databases

  - id: programming
    label: Programming Concepts
    children:
      - id: programming/languages
        label: Programming Languages
      - id: programming/paradigms
        label: Programming Paradigms
```

**Tag Usage**: Concepts reference `storage/distributed/cas` in `tags` field.

---

## 3. Repository Structure

### 3.1 Directory Layout

```
user_private_repo/
├── .git/                          # Git repository
├── .gitignore
├── .gitmodules                    # Submodule configuration
├── .panini/                       # Panini configuration
│   ├── config.yaml                # User settings (storage, sync, etc.)
│   ├── schema.yaml                # Knowledge schema version
│   ├── index/                     # Local index (not committed)
│   │   ├── rocksdb/               # RocksDB database
│   │   └── tantivy/               # Tantivy fulltext index
│   └── cache/                     # Temporary files
├── knowledge/                     # Knowledge base
│   ├── public/                    # Submodule → shared_public_repo
│   │   ├── .git/
│   │   ├── computer_science/
│   │   │   ├── algorithms/
│   │   │   │   ├── concept_quicksort_001.md
│   │   │   │   └── concept_mergesort_002.md
│   │   │   ├── data_structures/
│   │   │   └── .relations/
│   │   │       └── rel_batch_cs_001.yaml
│   │   └── mathematics/
│   ├── work_project_a/            # Submodule → team_repo_a (SSH)
│   │   ├── .git/
│   │   ├── design_docs/
│   │   └── meetings/
│   └── personal/                  # Direct in private repo
│       ├── concepts/
│       │   ├── concept_cas_001.md
│       │   └── concept_rust_002.md
│       ├── .relations/
│       │   └── rel_batch_personal_001.yaml
│       └── .metadata/
│           ├── tags.yaml
│           └── schema_v1.yaml
├── README.md                      # Repo description
└── LICENSE                        # Optional
```

### 3.2 Submodule Configuration

**`.gitmodules` Example**:
```ini
[submodule "knowledge/public"]
    path = knowledge/public
    url = https://github.com/community/panini-public-knowledge.git
    branch = main

[submodule "knowledge/work_project_a"]
    path = knowledge/work_project_a
    url = git@github.com:mycompany/project-a-knowledge.git
    branch = main
```

**Adding Submodule** (CLI):
```bash
panini repo add-submodule \
    --path knowledge/team_repo \
    --url git@github.com:myteam/knowledge.git \
    --branch main
```

**Submodule Update** (automatic):
```bash
panini sync  # Pulls all submodules
```

### 3.3 `.panini/config.yaml` Schema

```yaml
version: "1.0"

# Repository metadata
repository:
  name: "Stéphane's Knowledge Base"
  owner: stephane@example.com
  created: 2025-10-29T10:00:00Z

# Storage backends
storage:
  default: minio
  backends:
    minio:
      endpoint: http://localhost:9000
      bucket: panini-content
      access_key: ${MINIO_ACCESS_KEY}
      secret_key: ${MINIO_SECRET_KEY}

# Sync settings
sync:
  auto_pull: true               # Pull on startup
  auto_push: false              # Manual push (default)
  interval: 300                 # Seconds (5 minutes)
  conflict_strategy: prompt     # prompt | auto | manual

# Index settings
index:
  rebuild_on_startup: false     # Incremental by default
  fulltext_languages:
    - en
    - fr
    - es
  cache_size_mb: 256

# Query defaults
query:
  default_limit: 50
  max_limit: 1000
  result_format: json           # json | yaml | markdown

# UI settings (future)
ui:
  theme: dark
  graph_layout: force_directed
```

### 3.4 Schema Version (`.panini/schema.yaml`)

```yaml
version: "1.0.0"
created: 2025-10-29T10:00:00Z
relation_types:
  - is_a
  - part_of
  - causes
  - contradicts
  - supports
  - derives_from
  - used_by
  - related_to
dhatu_types:
  - TEXT
  - IMAGE
  - VIDEO
  - AUDIO
  - CODE
  - BINARY
  - ARCHIVE
```

**Migration**: When schema changes (v1.1, v2.0), migration tool updates all concepts.

---

## 4. Knowledge Schema

### 4.1 Validation Rules

**Concept ID Format**:
- Pattern: `concept_<category>_<number>`
- Example: `concept_cas_001`, `concept_rust_algorithms_042`
- **Must be unique** across repository (including submodules)

**Required Fields**:
```yaml
id: string (matches pattern)
type: concept
dhatu: TEXT | IMAGE | VIDEO | AUDIO | CODE | BINARY | ARCHIVE
title: string (1-200 chars)
```

**Optional but Recommended**:
```yaml
tags: string[] (hierarchical, e.g., "storage/distributed")
created: ISO 8601 datetime
author: email or identifier
```

**Validation on Commit** (pre-commit hook):
```bash
#!/bin/bash
# .git/hooks/pre-commit

panini validate --staged
if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Fix errors and try again."
    exit 1
fi
```

### 4.2 Dhātu Semantics (v2.0)

**Redefined as Knowledge Representation Formats**:

| Dhātu | Content Type | Validation | Example |
|-------|--------------|------------|---------|
| **TEXT** | Markdown prose | UTF-8, valid Markdown | Concept definitions, essays |
| **IMAGE** | Diagrams, photos | PNG/JPG/SVG, <10MB (Git) or S3 | Architecture diagrams |
| **VIDEO** | Tutorials, demos | MP4/WebM, S3-only | YouTube embeds or hosted |
| **AUDIO** | Podcasts, lectures | MP3/OGG, S3-only | Audio notes |
| **CODE** | Code snippets | Syntax-highlighted | Rust/Python examples |
| **BINARY** | Executables, blobs | SHA-256 verified | PDFs, executables |
| **ARCHIVE** | Datasets, bundles | TAR/ZIP, S3-only | Research datasets |

**Storage Policy**:
- `TEXT`, `CODE`: Always in Git (Markdown)
- `IMAGE`: <1MB in Git, >1MB in S3
- `VIDEO`, `AUDIO`, `BINARY`, `ARCHIVE`: Always S3

### 4.3 Relation Semantics

**Transitive Relations**:
- `is_a`: Transitive (A is_a B, B is_a C → A is_a C)
- `part_of`: Transitive (A part_of B, B part_of C → A part_of C)
- `derives_from`: Transitive

**Symmetric Relations**:
- `related_to`: Symmetric (A related_to B ↔ B related_to A)
- `contradicts`: Symmetric

**Confidence Decay**:
- Chain length > 3: Multiply confidences (0.9 × 0.9 × 0.9 = 0.729)
- Display warning if confidence < 0.5

### 4.4 Conflict Resolution

**Three Levels**:

1. **Automatic (90%)**: Disjoint edits
   - Different files: Git merge (no conflict)
   - Same file, different sections: Git merge
   - Timestamp wins: Latest `updated` field

2. **Semi-Automatic (8%)**: Custom YAML merge
   - Relations deduplicated (same type + target = merge)
   - Tags merged (union, no duplicates)
   - Content_refs merged (hash uniqueness)

3. **Manual (2%)**: Semantic conflicts
   - UI shows both versions
   - User chooses: Accept A / Accept B / Merge manually
   - Example: Contradicting facts about same concept

**Merge Driver** (`.gitattributes`):
```
*.md merge=panini-yaml
```

**Driver Implementation**:
```bash
git config merge.panini-yaml.driver "panini merge-yaml %O %A %B %L"
```

---

## 5. Git Operations

### 5.1 Core Operations (git2-rs)

**Initialize Repository**:
```rust
use git2::Repository;

pub fn init_repo(path: &Path) -> Result<Repository, git2::Error> {
    let repo = Repository::init(path)?;
    
    // Create .panini/ structure
    fs::create_dir_all(path.join(".panini/index"))?;
    
    // Write config
    let config = PaniniConfig::default();
    config.write_to_file(path.join(".panini/config.yaml"))?;
    
    // Initial commit
    let sig = repo.signature()?;
    let tree_id = {
        let mut index = repo.index()?;
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
```

**Commit Concept**:
```rust
pub fn commit_concept(
    repo: &Repository,
    concept: &Concept,
    message: &str
) -> Result<Oid, Error> {
    // Write Markdown file
    let path = concept.file_path();
    fs::write(&path, concept.to_markdown())?;
    
    // Stage file
    let mut index = repo.index()?;
    index.add_path(Path::new(&path))?;
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

**Pull Changes**:
```rust
pub fn pull(repo: &Repository, remote_name: &str) -> Result<(), Error> {
    let mut remote = repo.find_remote(remote_name)?;
    remote.fetch(&["main"], None, None)?;
    
    // Merge FETCH_HEAD into HEAD
    let fetch_head = repo.find_reference("FETCH_HEAD")?;
    let fetch_commit = repo.reference_to_annotated_commit(&fetch_head)?;
    
    let analysis = repo.merge_analysis(&[&fetch_commit])?;
    
    if analysis.0.is_up_to_date() {
        Ok(())
    } else if analysis.0.is_fast_forward() {
        // Fast-forward merge
        let refname = "refs/heads/main";
        let mut reference = repo.find_reference(refname)?;
        reference.set_target(fetch_commit.id(), "Fast-forward")?;
        repo.set_head(refname)?;
        repo.checkout_head(Some(git2::build::CheckoutBuilder::default().force()))?;
        Ok(())
    } else {
        // Merge required (potential conflicts)
        repo.merge(&[&fetch_commit], None, None)?;
        // Check for conflicts
        if repo.index()?.has_conflicts() {
            Err(Error::MergeConflict)
        } else {
            // Auto-commit merge
            let sig = repo.signature()?;
            let tree_id = repo.index()?.write_tree()?;
            let tree = repo.find_tree(tree_id)?;
            let parent1 = repo.head()?.peel_to_commit()?;
            let parent2 = repo.find_commit(fetch_commit.id())?;
            
            repo.commit(
                Some("HEAD"),
                &sig,
                &sig,
                &format!("Merge {} into main", remote_name),
                &tree,
                &[&parent1, &parent2]
            )?;
            Ok(())
        }
    }
}
```

**Push Changes**:
```rust
pub fn push(repo: &Repository, remote_name: &str) -> Result<(), Error> {
    let mut remote = repo.find_remote(remote_name)?;
    let mut callbacks = RemoteCallbacks::new();
    
    // SSH authentication
    callbacks.credentials(|_url, username, _allowed| {
        Cred::ssh_key_from_agent(username.unwrap())
    });
    
    let mut push_options = PushOptions::new();
    push_options.remote_callbacks(callbacks);
    
    remote.push(&["refs/heads/main:refs/heads/main"], Some(&mut push_options))?;
    Ok(())
}
```

### 5.2 Submodule Operations

**Add Submodule**:
```rust
pub fn add_submodule(
    repo: &Repository,
    url: &str,
    path: &Path
) -> Result<Submodule, Error> {
    let mut submodule = repo.submodule(url, path, false)?;
    
    // Initialize and update
    submodule.init(false)?;
    submodule.update(true, None)?;
    
    // Commit .gitmodules
    let mut index = repo.index()?;
    index.add_path(Path::new(".gitmodules"))?;
    index.add_path(path)?;
    index.write()?;
    
    let sig = repo.signature()?;
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;
    let parent = repo.head()?.peel_to_commit()?;
    
    repo.commit(
        Some("HEAD"),
        &sig,
        &sig,
        &format!("Add submodule: {}", path.display()),
        &tree,
        &[&parent]
    )?;
    
    Ok(submodule)
}
```

**Update All Submodules**:
```rust
pub fn update_submodules(repo: &Repository) -> Result<(), Error> {
    for mut submodule in repo.submodules()? {
        submodule.update(true, None)?;
    }
    Ok(())
}
```

---

## 6. Local Index

### 6.1 RocksDB Schema

**Purpose**: Fast concept/relation queries without Git traversal.

**Column Families**:
```rust
pub enum ColumnFamily {
    Concepts,      // concept_id → Concept (JSON)
    Relations,     // relation_id → Relation (JSON)
    Tags,          // tag → Vec<concept_id>
    Dhatu,         // dhatu_type → Vec<concept_id>
    FulltextIds,   // Internal: Tantivy doc_id → concept_id
    Metadata,      // System metadata (index_version, last_sync, etc.)
}
```

**Key Formats**:
```
Concepts:      "concept:concept_cas_001" → JSON
Relations:     "relation:rel_batch_001:0" → JSON
Tags:          "tag:storage/distributed" → ["concept_cas_001", "concept_ipfs_004"]
Dhatu:         "dhatu:TEXT" → ["concept_cas_001", "concept_rust_002"]
FulltextIds:   "ft:42" → "concept_cas_001"
Metadata:      "meta:index_version" → "1.0.0"
```

**Index Update** (on Git commit):
```rust
pub fn update_index(
    db: &DB,
    changed_files: Vec<PathBuf>
) -> Result<(), Error> {
    for file in changed_files {
        if file.extension() == Some(OsStr::new("md")) {
            let concept = parse_concept(&file)?;
            
            // Update Concepts CF
            let key = format!("concept:{}", concept.id);
            db.put_cf(cf_handle("Concepts"), key, concept.to_json())?;
            
            // Update Tags CF
            for tag in &concept.tags {
                let key = format!("tag:{}", tag);
                let mut ids: Vec<String> = db.get_cf(cf_handle("Tags"), &key)?
                    .map(|v| serde_json::from_slice(&v).unwrap())
                    .unwrap_or_default();
                if !ids.contains(&concept.id) {
                    ids.push(concept.id.clone());
                }
                db.put_cf(cf_handle("Tags"), key, serde_json::to_vec(&ids)?)?;
            }
            
            // Update Dhatu CF
            let key = format!("dhatu:{}", concept.dhatu);
            let mut ids: Vec<String> = db.get_cf(cf_handle("Dhatu"), &key)?
                .map(|v| serde_json::from_slice(&v).unwrap())
                .unwrap_or_default();
            if !ids.contains(&concept.id) {
                ids.push(concept.id.clone());
            }
            db.put_cf(cf_handle("Dhatu"), key, serde_json::to_vec(&ids)?)?;
            
            // Update Tantivy fulltext (see 6.2)
            update_fulltext_index(&concept)?;
        }
    }
    
    // Update metadata
    db.put_cf(
        cf_handle("Metadata"),
        "meta:last_sync",
        Utc::now().to_rfc3339().as_bytes()
    )?;
    
    Ok(())
}
```

### 6.2 Tantivy Fulltext Index

**Schema**:
```rust
use tantivy::schema::*;

pub fn build_schema() -> Schema {
    let mut schema_builder = Schema::builder();
    
    schema_builder.add_text_field("id", STRING | STORED);
    schema_builder.add_text_field("title", TEXT | STORED);
    schema_builder.add_text_field("content", TEXT);  // Markdown body
    schema_builder.add_text_field("tags", TEXT);     // Joined with spaces
    schema_builder.add_text_field("language", STRING);
    schema_builder.add_date_field("created", STORED);
    schema_builder.add_date_field("updated", STORED);
    
    schema_builder.build()
}
```

**Indexing**:
```rust
use tantivy::{Index, IndexWriter};
use tantivy::doc;

pub fn index_concept(
    writer: &mut IndexWriter,
    concept: &Concept
) -> Result<(), Error> {
    let schema = build_schema();
    
    let id = schema.get_field("id").unwrap();
    let title = schema.get_field("title").unwrap();
    let content = schema.get_field("content").unwrap();
    let tags = schema.get_field("tags").unwrap();
    let language = schema.get_field("language").unwrap();
    
    writer.add_document(doc!(
        id => concept.id.clone(),
        title => concept.title.clone(),
        content => concept.markdown_body(),
        tags => concept.tags.join(" "),
        language => concept.language().unwrap_or("en"),
    ))?;
    
    writer.commit()?;
    Ok(())
}
```

**Search**:
```rust
use tantivy::query::QueryParser;

pub fn fulltext_search(
    index: &Index,
    query_str: &str,
    limit: usize
) -> Result<Vec<String>, Error> {
    let reader = index.reader()?;
    let searcher = reader.searcher();
    
    let schema = build_schema();
    let query_parser = QueryParser::for_index(
        &index,
        vec![
            schema.get_field("title").unwrap(),
            schema.get_field("content").unwrap(),
            schema.get_field("tags").unwrap(),
        ]
    );
    
    let query = query_parser.parse_query(query_str)?;
    let top_docs = searcher.search(&query, &TopDocs::with_limit(limit))?;
    
    let id_field = schema.get_field("id").unwrap();
    let mut results = Vec::new();
    
    for (_score, doc_address) in top_docs {
        let doc = searcher.doc(doc_address)?;
        if let Some(id_value) = doc.get_first(id_field) {
            results.push(id_value.as_text().unwrap().to_string());
        }
    }
    
    Ok(results)
}
```

### 6.3 Index Rebuild

**When Needed**:
- First run (index doesn't exist)
- Schema version change
- Corruption detected
- User triggers manually (`panini index rebuild`)

**Algorithm**:
```rust
pub fn rebuild_index(repo_path: &Path) -> Result<(), Error> {
    let db = open_rocksdb(&repo_path.join(".panini/index/rocksdb"))?;
    let tantivy_index = open_tantivy_index(&repo_path.join(".panini/index/tantivy"))?;
    
    // Clear all data
    for cf in [Concepts, Relations, Tags, Dhatu, FulltextIds] {
        let mut batch = WriteBatch::default();
        let iter = db.iterator_cf(cf_handle(cf), IteratorMode::Start);
        for item in iter {
            let (key, _) = item?;
            batch.delete_cf(cf_handle(cf), key);
        }
        db.write(batch)?;
    }
    
    // Clear Tantivy
    let mut writer = tantivy_index.writer(50_000_000)?;
    writer.delete_all_documents()?;
    writer.commit()?;
    
    // Walk repository
    let knowledge_dir = repo_path.join("knowledge");
    for entry in WalkDir::new(knowledge_dir).into_iter().filter_map(|e| e.ok()) {
        if entry.path().extension() == Some(OsStr::new("md")) {
            let concept = parse_concept(entry.path())?;
            
            // Index in RocksDB
            update_index(&db, vec![entry.path().to_path_buf()])?;
            
            // Index in Tantivy
            index_concept(&mut writer, &concept)?;
        }
    }
    
    // Update metadata
    db.put_cf(
        cf_handle(Metadata),
        "meta:index_version",
        "1.0.0".as_bytes()
    )?;
    db.put_cf(
        cf_handle(Metadata),
        "meta:last_rebuild",
        Utc::now().to_rfc3339().as_bytes()
    )?;
    
    Ok(())
}
```

---

## 7. Query Language

### 7.1 Query DSL

**Grammar** (EBNF):
```ebnf
query       = filter ( " AND " filter )* ;
filter      = tag_filter | dhatu_filter | fulltext_filter | relation_filter ;
tag_filter  = "tag:" tag_name ;
dhatu_filter = "dhatu:" dhatu_type ;
fulltext_filter = "text:" quoted_string ;
relation_filter = "relation:" relation_type ":" concept_id ;
```

**Examples**:
```
tag:storage/distributed
dhatu:TEXT AND tag:programming
text:"content-addressable storage"
relation:is_a:concept_storage_002
tag:rust AND text:"async" AND dhatu:CODE
```

### 7.2 Query Execution

**Query Plan**:
1. Parse query string
2. Check index first (fast path)
3. Combine results (AND/OR logic)
4. Sort by relevance (fulltext score)
5. Limit results
6. Fetch full concepts from index or Git

**Implementation**:
```rust
pub struct QueryEngine {
    db: DB,
    tantivy_index: Index,
}

impl QueryEngine {
    pub fn execute(&self, query: &Query, limit: usize) -> Result<Vec<Concept>, Error> {
        let mut results: Option<HashSet<String>> = None;
        
        // Process each filter
        for filter in &query.filters {
            let filter_results = match filter {
                Filter::Tag(tag) => self.query_by_tag(tag)?,
                Filter::Dhatu(dhatu) => self.query_by_dhatu(dhatu)?,
                Filter::Fulltext(text) => self.query_fulltext(text, limit * 2)?,
                Filter::Relation(rel_type, target) => self.query_by_relation(rel_type, target)?,
            };
            
            // Intersect results (AND logic)
            match results {
                None => results = Some(filter_results.into_iter().collect()),
                Some(ref mut r) => {
                    r.retain(|id| filter_results.contains(id));
                }
            }
        }
        
        // Fetch full concepts
        let concept_ids = results.unwrap_or_default();
        let mut concepts = Vec::new();
        
        for id in concept_ids.iter().take(limit) {
            if let Some(concept) = self.get_concept(id)? {
                concepts.push(concept);
            }
        }
        
        Ok(concepts)
    }
    
    fn query_by_tag(&self, tag: &str) -> Result<Vec<String>, Error> {
        let key = format!("tag:{}", tag);
        let value = self.db.get_cf(cf_handle("Tags"), key)?;
        Ok(value.map(|v| serde_json::from_slice(&v).unwrap()).unwrap_or_default())
    }
    
    fn query_by_dhatu(&self, dhatu: &Dhatu) -> Result<Vec<String>, Error> {
        let key = format!("dhatu:{:?}", dhatu);
        let value = self.db.get_cf(cf_handle("Dhatu"), key)?;
        Ok(value.map(|v| serde_json::from_slice(&v).unwrap()).unwrap_or_default())
    }
    
    fn query_fulltext(&self, text: &str, limit: usize) -> Result<Vec<String>, Error> {
        fulltext_search(&self.tantivy_index, text, limit)
    }
    
    fn query_by_relation(&self, rel_type: &RelationType, target: &str) -> Result<Vec<String>, Error> {
        // Find all concepts with relation of type rel_type pointing to target
        let mut results = Vec::new();
        let iter = self.db.iterator_cf(cf_handle("Concepts"), IteratorMode::Start);
        
        for item in iter {
            let (_key, value) = item?;
            let concept: Concept = serde_json::from_slice(&value)?;
            
            if concept.relations.iter().any(|r| r.rel_type == *rel_type && r.target == target) {
                results.push(concept.id);
            }
        }
        
        Ok(results)
    }
    
    fn get_concept(&self, id: &str) -> Result<Option<Concept>, Error> {
        let key = format!("concept:{}", id);
        let value = self.db.get_cf(cf_handle("Concepts"), key)?;
        Ok(value.map(|v| serde_json::from_slice(&v).unwrap()))
    }
}
```

### 7.3 Graph Queries

**Advanced: Traversal Queries** (v1.5):

```rust
// Find all concepts transitively related via "is_a"
pub fn transitive_closure(
    engine: &QueryEngine,
    start_id: &str,
    rel_type: RelationType,
    max_depth: usize
) -> Result<Vec<Concept>, Error> {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back((start_id.to_string(), 0));
    
    while let Some((id, depth)) = queue.pop_front() {
        if depth >= max_depth || visited.contains(&id) {
            continue;
        }
        visited.insert(id.clone());
        
        let concept = engine.get_concept(&id)?.ok_or(Error::NotFound)?;
        for relation in &concept.relations {
            if relation.rel_type == rel_type {
                queue.push_back((relation.target.clone(), depth + 1));
            }
        }
    }
    
    // Fetch all visited concepts
    visited.into_iter()
        .filter_map(|id| engine.get_concept(&id).ok().flatten())
        .collect()
}
```

---

## 8. API Specifications

### 8.1 Rust Core API

**Public Interface** (`src/lib.rs`):
```rust
pub struct PaniniRepo {
    path: PathBuf,
    git_repo: Repository,
    index: QueryEngine,
    config: PaniniConfig,
}

impl PaniniRepo {
    /// Initialize a new Panini repository
    pub fn init(path: &Path) -> Result<Self, Error>;
    
    /// Open an existing Panini repository
    pub fn open(path: &Path) -> Result<Self, Error>;
    
    /// Create a new concept
    pub fn create_concept(&mut self, concept: Concept) -> Result<String, Error>;
    
    /// Read concept by ID
    pub fn get_concept(&self, id: &str) -> Result<Option<Concept>, Error>;
    
    /// Update existing concept
    pub fn update_concept(&mut self, concept: Concept) -> Result<(), Error>;
    
    /// Delete concept
    pub fn delete_concept(&mut self, id: &str) -> Result<(), Error>;
    
    /// Query concepts
    pub fn query(&self, query: &str, limit: usize) -> Result<Vec<Concept>, Error>;
    
    /// Add relation between concepts
    pub fn add_relation(&mut self, from: &str, to: &str, rel_type: RelationType) -> Result<(), Error>;
    
    /// Sync with remote (pull + push)
    pub fn sync(&mut self) -> Result<SyncResult, Error>;
    
    /// Add submodule
    pub fn add_submodule(&mut self, url: &str, path: &Path) -> Result<(), Error>;
    
    /// Rebuild index
    pub fn rebuild_index(&mut self) -> Result<(), Error>;
}
```

### 8.2 REST API

**Server** (`panini-server`):
```rust
use axum::{Router, routing::{get, post, put, delete}};

pub fn create_router(repo: Arc<Mutex<PaniniRepo>>) -> Router {
    Router::new()
        .route("/api/concepts", get(list_concepts).post(create_concept))
        .route("/api/concepts/:id", get(get_concept).put(update_concept).delete(delete_concept))
        .route("/api/query", post(query_concepts))
        .route("/api/relations", post(create_relation))
        .route("/api/sync", post(sync_repo))
        .route("/api/submodules", post(add_submodule))
        .route("/api/index/rebuild", post(rebuild_index))
        .route("/api/stats", get(get_stats))
        .with_state(repo)
}
```

**Endpoints**:

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| GET | `/api/concepts` | List all concepts | Query params: `limit`, `offset`, `tag`, `dhatu` | `{ concepts: Concept[], total: number }` |
| POST | `/api/concepts` | Create concept | `Concept` (JSON) | `{ id: string }` |
| GET | `/api/concepts/:id` | Get concept | - | `Concept` (JSON) |
| PUT | `/api/concepts/:id` | Update concept | `Concept` (JSON) | `{ success: true }` |
| DELETE | `/api/concepts/:id` | Delete concept | - | `{ success: true }` |
| POST | `/api/query` | Query concepts | `{ query: string, limit: number }` | `{ concepts: Concept[], count: number }` |
| POST | `/api/relations` | Create relation | `{ from: string, to: string, type: string }` | `{ success: true }` |
| POST | `/api/sync` | Sync with remote | `{ remote: string, pull: bool, push: bool }` | `{ pulled: number, pushed: number, conflicts: string[] }` |
| POST | `/api/submodules` | Add submodule | `{ url: string, path: string }` | `{ success: true }` |
| POST | `/api/index/rebuild` | Rebuild index | - | `{ success: true, duration_ms: number }` |
| GET | `/api/stats` | Get statistics | - | `{ concepts: number, relations: number, tags: number, index_size: number }` |

**Authentication** (v1.5):
- API keys (header: `X-Panini-Key`)
- JWT tokens (header: `Authorization: Bearer <token>`)
- Read-only public endpoints (no auth)

---

## 9. CLI Commands

### 9.1 Repository Management

```bash
# Initialize repository
panini init [path]

# Open repository
panini open <path>

# Status (like git status)
panini status

# Configuration
panini config get <key>
panini config set <key> <value>
```

### 9.2 Concept Management

```bash
# Create concept (interactive)
panini concept create

# Create concept (from file)
panini concept create --file concept.md

# Get concept
panini concept get <id>

# Edit concept (opens $EDITOR)
panini concept edit <id>

# Delete concept
panini concept delete <id>

# List concepts
panini concept list --tag <tag> --dhatu <dhatu> --limit 50
```

### 9.3 Relation Management

```bash
# Add relation
panini relation add <from_id> <to_id> --type is_a --confidence 0.9

# List relations for concept
panini relation list <id>

# Delete relation
panini relation delete <from_id> <to_id> --type is_a

# Graph visualization (exports to DOT format)
panini relation graph <id> --depth 2 --output graph.dot
```

### 9.4 Query

```bash
# Simple query
panini query "tag:storage/distributed"

# Complex query
panini query 'tag:rust AND text:"async" AND dhatu:CODE' --limit 20

# Fulltext search
panini search "content-addressable storage"

# Export results
panini query "tag:programming" --format json --output results.json
```

### 9.5 Sync

```bash
# Pull from remote
panini sync pull

# Push to remote
panini sync push

# Full sync (pull + push)
panini sync

# Sync specific submodule
panini sync --submodule knowledge/work_project_a
```

### 9.6 Submodule Management

```bash
# Add submodule
panini submodule add <url> --path knowledge/team_repo

# Remove submodule
panini submodule remove knowledge/team_repo

# Update submodules
panini submodule update

# List submodules
panini submodule list
```

### 9.7 Index Management

```bash
# Rebuild index
panini index rebuild

# Index stats
panini index stats

# Verify index integrity
panini index verify
```

### 9.8 Utilities

```bash
# Validate all concepts
panini validate

# Export to format
panini export --format json --output knowledge.json
panini export --format graphml --output knowledge.graphml

# Import from format
panini import --file knowledge.json

# Statistics
panini stats
```

---

## 10. Sync Protocol

### 10.1 Pull Strategy

**Algorithm**:
1. `git fetch origin main`
2. Detect changed files (diff)
3. Check for conflicts
4. If conflicts: Prompt user or auto-resolve
5. `git merge origin/main`
6. Update index (only changed files)
7. Update submodules (`git submodule update --recursive`)

**Conflict Detection**:
```rust
pub fn has_conflicts(repo: &Repository) -> Result<bool, Error> {
    let index = repo.index()?;
    Ok(index.has_conflicts())
}

pub fn list_conflicts(repo: &Repository) -> Result<Vec<PathBuf>, Error> {
    let index = repo.index()?;
    let conflicts = index.conflicts()?;
    
    let mut paths = Vec::new();
    for conflict in conflicts {
        if let Some(our) = conflict?.our {
            paths.push(PathBuf::from(String::from_utf8_lossy(&our.path).to_string()));
        }
    }
    
    Ok(paths)
}
```

### 10.2 Push Strategy

**Algorithm**:
1. Check for unpushed commits
2. If behind remote: Prompt to pull first
3. `git push origin main`
4. Handle errors (rejected, auth)
5. Push submodules if changed

### 10.3 Conflict Resolution UI

**CLI Prompt**:
```
⚠️  Merge conflict detected in knowledge/personal/concepts/concept_cas_001.md

Options:
  1. Accept ours (local version)
  2. Accept theirs (remote version)
  3. Edit manually (opens $EDITOR)
  4. Skip (leave conflicted)

Choose [1-4]:
```

**Manual Edit Flow**:
1. Open file in `$EDITOR`
2. Git conflict markers present:
   ```markdown
   <<<<<<< HEAD
   Local version...
   =======
   Remote version...
   >>>>>>> origin/main
   ```
3. User resolves manually
4. Save and exit
5. `panini` validates resolved file
6. Auto-commit merge

---

## 11. Validation Rules

### 11.1 Schema Validation

**Pre-commit Hook** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash

# Validate staged Markdown files
panini validate --staged

if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Fix errors and try again."
    exit 1
fi

echo "✅ Validation passed"
exit 0
```

**Validation Checks**:
1. **YAML Frontmatter**:
   - Required fields present (`id`, `type`, `dhatu`, `title`)
   - `id` matches pattern `concept_<category>_<number>`
   - `dhatu` is valid enum value
   - `relations` have valid `type` and `target`
   - `tags` are strings (no nested arrays)

2. **Markdown Body**:
   - Valid UTF-8
   - No syntax errors (parse with pulldown-cmark)

3. **Relations**:
   - Target concepts exist (or warn)
   - No self-references
   - Confidence in range [0.0, 1.0]

4. **Content Refs**:
   - Hash format valid (sha256:...)
   - Storage URL valid
   - Size > 0

**Validator Implementation**:
```rust
pub fn validate_concept(concept: &Concept) -> Result<(), Vec<ValidationError>> {
    let mut errors = Vec::new();
    
    // ID format
    if !concept.id.starts_with("concept_") {
        errors.push(ValidationError::InvalidId(concept.id.clone()));
    }
    
    // Title length
    if concept.title.is_empty() || concept.title.len() > 200 {
        errors.push(ValidationError::InvalidTitle);
    }
    
    // Relations
    for relation in &concept.relations {
        if !VALID_RELATION_TYPES.contains(&relation.rel_type) {
            errors.push(ValidationError::InvalidRelationType(relation.rel_type));
        }
        if relation.target == concept.id {
            errors.push(ValidationError::SelfReference);
        }
    }
    
    // Content refs
    for content_ref in &concept.content_refs {
        if !content_ref.hash.starts_with("sha256:") {
            errors.push(ValidationError::InvalidHash);
        }
    }
    
    if errors.is_empty() {
        Ok(())
    } else {
        Err(errors)
    }
}
```

### 11.2 Uniqueness Constraints

**Concept ID Uniqueness**:
- Checked on create/update
- Scoped to entire repository (including submodules)
- Error if duplicate detected

**Implementation**:
```rust
pub fn is_id_unique(repo: &PaniniRepo, id: &str) -> Result<bool, Error> {
    // Check main repo
    if repo.index.get_concept(id)?.is_some() {
        return Ok(false);
    }
    
    // Check submodules
    for submodule in repo.git_repo.submodules()? {
        let sub_path = submodule.path();
        let sub_repo = PaniniRepo::open(sub_path)?;
        if sub_repo.index.get_concept(id)?.is_some() {
            return Ok(false);
        }
    }
    
    Ok(true)
}
```

---

## 12. Performance Targets

### 12.1 Query Performance

| Operation | Target (P95) | Measurement |
|-----------|--------------|-------------|
| Query by tag | <5ms | Criterion benchmark |
| Query by dhātu | <5ms | Criterion benchmark |
| Fulltext search | <50ms | Criterion benchmark |
| Relation traversal (depth 3) | <20ms | Criterion benchmark |
| Get concept by ID | <2ms | Criterion benchmark |

### 12.2 Git Performance

| Operation | Target (P95) | Notes |
|-----------|--------------|-------|
| Commit concept | <100ms | Single file |
| Pull (no conflicts) | <2s | 100 changed files |
| Push | <3s | 100 commits |
| Clone repository | <10s | 1000 concepts |
| Submodule update | <5s | 5 submodules |

### 12.3 Index Performance

| Operation | Target | Notes |
|-----------|--------|-------|
| Index rebuild | <30s | 10,000 concepts |
| Incremental update | <500ms | 10 changed files |
| RocksDB read | <1ms | Single key lookup |
| Tantivy search | <50ms | 1000 documents |

### 12.4 Scalability

**v1.0 Targets**:
- 10,000 concepts per repository
- 50,000 relations
- 1,000 tags
- 100MB index size

**v2.0 Stretch Goals**:
- 100,000 concepts
- 500,000 relations
- 10,000 tags
- 1GB index size

---

## 13. Implementation Notes

### 13.1 Technology Stack

| Component | Library | Version | Rationale |
|-----------|---------|---------|-----------|
| Git operations | git2-rs | 0.18 | Libgit2 bindings, mature |
| Index (KV store) | RocksDB | 0.21 | Fast, embedded, proven |
| Fulltext search | Tantivy | 0.21 | Pure Rust, multi-language |
| Markdown parsing | pulldown-cmark | 0.9 | Fast, CommonMark-compliant |
| YAML parsing | serde_yaml | 0.9 | Serde integration |
| CLI framework | Clap | 4.4 | Derive macros, ergonomic |
| REST API | Axum | 0.7 | Tokio-based, fast |
| Async runtime | Tokio | 1.35 | Industry standard |
| Graph algorithms | petgraph | 0.6 | Transitive closure, etc. |

### 13.2 Module Structure

```
panini-fs/
├── Cargo.toml
├── crates/
│   ├── panini-core/          # Core library
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── git.rs        # Git operations
│   │   │   ├── index.rs      # RocksDB + Tantivy
│   │   │   ├── query.rs      # Query engine
│   │   │   ├── schema.rs     # Validation
│   │   │   ├── concept.rs    # Concept model
│   │   │   ├── relation.rs   # Relation model
│   │   │   └── sync.rs       # Sync protocol
│   │   └── Cargo.toml
│   ├── panini-cli/           # CLI tool
│   │   ├── src/
│   │   │   ├── main.rs
│   │   │   ├── commands/     # CLI commands
│   │   │   └── ui.rs         # TUI components
│   │   └── Cargo.toml
│   └── panini-server/        # REST API server (optional)
│       ├── src/
│       │   ├── main.rs
│       │   ├── routes.rs
│       │   └── auth.rs
│       └── Cargo.toml
├── tests/                    # Integration tests
├── benches/                  # Criterion benchmarks
├── docs/                     # Documentation
└── README.md
```

### 13.3 Error Handling

**Error Types**:
```rust
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("Git error: {0}")]
    Git(#[from] git2::Error),
    
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("Index error: {0}")]
    Index(String),
    
    #[error("Validation error: {0:?}")]
    Validation(Vec<ValidationError>),
    
    #[error("Concept not found: {0}")]
    NotFound(String),
    
    #[error("Merge conflict")]
    MergeConflict,
    
    #[error("Schema version mismatch: expected {expected}, got {actual}")]
    SchemaVersionMismatch { expected: String, actual: String },
}
```

---

**Document Status**: ✅ Complete  
**Next Steps**: Create `plan_v2.md` with 9-week implementation roadmap  
**Approval**: Pending stakeholder review
