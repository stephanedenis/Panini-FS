# Architecture Transition: RocksDB → Git-Native Knowledge Graph

**Date**: 2025-10-29  
**Status**: 🔄 MAJOR PIVOT  
**Decision**: Pivot from RocksDB-based CAS to Git-native hierarchical knowledge system

---

## 1. Strategic Rationale

### 1.1 Original Vision (Phases 1-6)
- **Primary Goal**: Content-addressable storage with metadata extraction
- **Storage**: RocksDB (embedded key-value)
- **Use Case**: Store binary content, extract dhātu metadata
- **Architecture**: Centralized service (REST API)

### 1.2 New Vision (Git-Native)
- **Primary Goal**: Distributed knowledge graph with content versioning
- **Storage**: Git repositories (hierarchical, versioned)
- **Use Case**: Personal/team/public knowledge bases with full history
- **Architecture**: Distributed repositories with submodule hierarchy

### 1.3 Why Pivot?

**Strategic Advantages**:
1. ✅ **Version Control**: Every knowledge change tracked with full git history
2. ✅ **Collaboration**: Git workflow = proven collaboration model (PR, review, merge)
3. ✅ **Distribution**: Each user owns complete copy of their knowledge
4. ✅ **Permissions**: Git submodules = natural public/private/team boundaries
5. ✅ **Ecosystem**: Leverage GitHub/GitLab infrastructure (hosting, CI, issues)
6. ✅ **Offline-First**: Git's distributed nature = full offline capability
7. ✅ **Provenance**: Git commits = natural provenance tracking
8. ✅ **Branching**: Experiment with knowledge without affecting main

**Technical Advantages**:
1. ✅ **No DB maintenance**: Git handles persistence, replication, backup
2. ✅ **Standard tooling**: git CLI, GitHub Desktop, VS Code integration
3. ✅ **Human-readable**: Markdown files = diff-friendly, grep-able
4. ✅ **Conflict resolution**: Git merge = proven conflict handling
5. ✅ **Scalability**: Repository sharding via submodules

**Philosophical Alignment**:
- Panini's Sanskrit grammar = versioned knowledge system
- Git commits = atomic knowledge updates
- Branches = parallel knowledge evolution
- Merge = knowledge synthesis

---

## 2. Architecture Comparison

### 2.1 Original Architecture (Phases 1-6)

```
┌─────────────────────────────────────────┐
│         REST API (Axum)                 │
│  /store  /retrieve  /extract  /dhatu   │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│  RocksDB     │    │  LRU Cache   │
│  - Content   │    │  - 256MB     │
│  - Metadata  │    │  - In-memory │
└──────────────┘    └──────────────┘
        │
        ▼
┌─────────────────────────┐
│  Extractors (7 dhātus)  │
│  TEXT IMAGE VIDEO AUDIO │
│  CODE BINARY ARCHIVE    │
└─────────────────────────┘
```

### 2.2 New Architecture (Git-Native)

```
┌───────────────────────────────────────────────────────────┐
│                    Panini-FS v2.0                         │
│              Knowledge Graph Manager (Rust)                │
└───────────┬───────────────────────────────────────────────┘
            │
    ┌───────┴────────┐
    ▼                ▼
┌────────────────┐  ┌──────────────────────────────┐
│  Git Hierarchy │  │   Local Index (RocksDB)      │
│                │  │   - Fast queries             │
│  user_repo/    │◄─┤   - Fulltext search          │
│  ├─ .panini/   │  │   - Graph traversal cache    │
│  ├─ knowledge/ │  └──────────────────────────────┘
│  │  ├─ public/│               │
│  │  │  └─.git │               ▼
│  │  ├─ work/  │  ┌──────────────────────────────┐
│  │  │  └─.git │  │  Content Store (Optional)    │
│  │  └─personal│  │  - Git LFS for large files   │
│  │     ├─ con │  │  - Or external CAS (S3, etc) │
│  │     ├─ rel │  └──────────────────────────────┘
│  │     └─ met │               │
│  └─ .git      │               ▼
└────────────────┘  ┌──────────────────────────────┐
                    │  Extractors (7 dhātus)       │
                    │  - Run on file changes       │
                    │  - Store metadata in .panini/│
                    └──────────────────────────────┘
```

---

## 3. Core Concepts Redefined

### 3.1 Storage Model

**Before (RocksDB)**:
```
Key: {hash}:content
Value: binary content (LZ4 compressed)

Example:
abc123...:content → [binary image data]
abc123...:metadata → {"dhatu": "IMAGE", "format": "JPEG", ...}
```

**After (Git)**:
```
File: knowledge/concepts/dhatu_primitive.md
Content:
---
id: concept_dhatu_001
type: concept
dhatu: TEXT
tags: [sanskrit, primitive]
content_hash: abc123...  # Reference to binary in Git LFS or external
---
# Dhātu Primitive
...content...

Commit: a1b2c3d "Add dhātu primitive concept"
Author: user@example.com
Date: 2025-10-29T10:00:00Z
```

### 3.2 Dhātu Redefined

**Original**: Content type classification (TEXT, IMAGE, VIDEO, etc.)

**New**: Knowledge representation format
- **TEXT**: Markdown files with YAML frontmatter
- **IMAGE**: Visual knowledge (diagrams, photos) with metadata
- **VIDEO**: Temporal knowledge (lectures, demos)
- **AUDIO**: Auditory knowledge (podcasts, interviews)
- **CODE**: Executable knowledge (scripts, notebooks)
- **BINARY**: Compiled knowledge (executables, models)
- **ARCHIVE**: Packaged knowledge (datasets, collections)

### 3.3 Relations Model

**Before**: Implicit (metadata links)

**After**: Explicit Git-based relations
```yaml
# knowledge/relations/is_a.yaml
relations:
  - from: concept_dhatu_001
    to: concept_primitive_002
    type: is_a
    confidence: 1.0
    created: 2025-10-29T10:00:00Z
    commit: a1b2c3d

  - from: concept_panini_fs_003
    to: concept_dhatu_001
    type: uses
    confidence: 1.0
    created: 2025-10-29T11:00:00Z
    commit: b2c3d4e
```

---

## 4. Repository Hierarchy

### 4.1 Structure

```
user_private_repo/               # Main private repo
├── .git/
├── .panini/
│   ├── config.yaml              # User preferences
│   ├── index.db                 # Local RocksDB index
│   ├── schema.yaml              # Knowledge schema
│   └── hooks/                   # Git hooks for automation
│       ├── pre-commit           # Validate knowledge format
│       └── post-merge           # Reindex after sync
├── .gitmodules                  # Submodule definitions
├── knowledge/
│   ├── public/                  # Submodule → shared_public_repo
│   │   ├── .git/
│   │   ├── computer_science/
│   │   │   ├── algorithms/
│   │   │   │   ├── sorting.md
│   │   │   │   └── graphs.md
│   │   │   └── data_structures/
│   │   └── mathematics/
│   │       └── linear_algebra.md
│   ├── work_project_a/          # Submodule → team_repo_a
│   │   ├── .git/
│   │   ├── design_docs/
│   │   └── meeting_notes/
│   └── personal/                # Direct in private repo
│       ├── concepts/
│       │   ├── dhatu.md
│       │   └── panini.md
│       ├── relations/
│       │   └── links.yaml
│       ├── metadata/
│       │   └── tags.yaml
│       └── content/             # Git LFS or external refs
│           ├── .gitattributes   # LFS config
│           ├── diagram.png
│           └── lecture.mp4
└── README.md

shared_public_repo/              # Separate public repo
├── .git/
├── computer_science/
├── mathematics/
└── philosophy/
```

### 4.2 Permission Model

| Repository Type | Visibility | Use Case | Example |
|----------------|-----------|----------|---------|
| **Private User Repo** | Only owner | Personal knowledge, drafts | `user_stephane/knowledge-base` |
| **Team Repo** | Team members | Shared project knowledge | `team_panini/project-docs` |
| **Public Repo** | Everyone | Common knowledge | `panini-community/shared-concepts` |

**Submodule Mapping**:
```yaml
# .gitmodules
[submodule "knowledge/public"]
  path = knowledge/public
  url = https://github.com/panini-community/shared-concepts.git
  
[submodule "knowledge/work"]
  path = knowledge/work
  url = git@github.com:team_panini/project-docs.git  # SSH = private
```

---

## 5. File Formats

### 5.1 Concept File (Markdown + YAML)

```markdown
---
id: concept_cas_001
type: concept
dhatu: TEXT
tags: [storage, content-addressable, distributed]
created: 2025-10-29T10:00:00Z
updated: 2025-10-29T12:00:00Z
author: stephane@panini.dev
visibility: public
status: draft  # draft | reviewed | published | archived
version: 1.0.0
relations:
  - type: is_a
    target: concept_storage_002
    confidence: 1.0
  - type: used_in
    target: project_panini_fs_003
    confidence: 1.0
  - type: related_to
    target: concept_git_004
    confidence: 0.8
content_refs:
  - hash: abc123def456...
    type: IMAGE
    description: "CAS architecture diagram"
  - hash: def456abc789...
    type: VIDEO
    description: "CAS explanation video"
citations:
  - url: https://en.wikipedia.org/wiki/Content-addressable_storage
    title: "Content-addressable storage - Wikipedia"
    accessed: 2025-10-29T10:00:00Z
---

# Content-Addressable Storage (CAS)

## Definition

A **Content-Addressable Storage** (CAS) system is a storage mechanism where
data is accessed based on its content rather than its location.

## Key Properties

1. **Immutability**: Content address = hash of content
2. **Deduplication**: Same content = same hash = single storage
3. **Integrity**: Hash verification ensures data hasn't changed

## Use Cases

- Git repository storage
- Docker image layers
- IPFS distributed filesystem
- Panini-FS knowledge system

## Implementation

```rust
pub fn store(content: &[u8]) -> Hash {
    let hash = sha256(content);
    storage.put(&hash, content);
    hash
}
```

## Related Concepts

- [[concept_git_004|Git]] uses CAS for object storage
- [[concept_ipfs_005|IPFS]] extends CAS to distributed networks
- [[concept_merkle_tree_006|Merkle Trees]] provide efficient CAS verification

## History

- First conceptualized in 1970s
- Popularized by Git (2005)
- Now standard in distributed systems

## References

1. [Wikipedia: Content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
2. [Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
```

### 5.2 Relation File (YAML)

```yaml
# knowledge/relations/is_a.yaml
version: 1.0.0
relation_type: is_a
description: "Hierarchical classification relations"

relations:
  - id: rel_001
    from: concept_cas_001
    to: concept_storage_002
    confidence: 1.0
    bidirectional: false
    created: 2025-10-29T10:00:00Z
    author: stephane@panini.dev
    evidence:
      - type: definition
        source: "CAS is a type of storage system"
      - type: citation
        url: https://example.com/cas-definition
    
  - id: rel_002
    from: concept_panini_fs_003
    to: concept_cas_001
    confidence: 0.9
    bidirectional: false
    created: 2025-10-29T11:00:00Z
    author: stephane@panini.dev
    metadata:
      implementation_phase: "planned"
      priority: "high"
```

### 5.3 Tag Taxonomy (YAML)

```yaml
# knowledge/metadata/tags.yaml
version: 1.0.0
taxonomies:
  domain:
    - computer_science
    - mathematics
    - philosophy
    - linguistics
  
  dhatu:
    - TEXT
    - IMAGE
    - VIDEO
    - AUDIO
    - CODE
    - BINARY
    - ARCHIVE
  
  status:
    - draft
    - reviewed
    - published
    - archived
  
  visibility:
    - private
    - team
    - public

tag_relations:
  - parent: computer_science
    children:
      - algorithms
      - data_structures
      - distributed_systems
  
  - parent: distributed_systems
    children:
      - cas
      - p2p
      - blockchain
```

---

## 6. Implementation Strategy

### 6.1 Phase Breakdown

**Phase 2.0.1: Git Core (2 weeks)**
- Rust git2 wrapper with high-level API
- Repository initialization and cloning
- Submodule management (add, remove, update)
- Commit, push, pull operations
- Conflict detection and basic resolution

**Phase 2.0.2: Knowledge Schema (2 weeks)**
- Markdown + YAML parser
- Concept validation (schema enforcement)
- Relation graph builder
- Tag system implementation
- File watcher for auto-reindexing

**Phase 2.0.3: Local Index (1.5 weeks)**
- RocksDB index for fast queries
- Fulltext search (tantivy crate)
- Graph traversal algorithms (BFS, DFS, shortest path)
- Query DSL design and implementation

**Phase 2.0.4: Sync & Collaboration (1.5 weeks)**
- Multi-remote sync (public + private + team)
- Automatic submodule updates
- Conflict resolution strategies
- Merge conflict UI/CLI

**Phase 2.0.5: Content Management (1 week)**
- Git LFS integration for large files
- External content store (S3, IPFS) support
- Content hash verification
- Extractor integration (metadata from binaries)

**Phase 2.0.6: API & CLI (1 week)**
- REST API (store, retrieve, query, sync)
- CLI tool (panini-cli)
- Library crate (panini-core)
- Documentation

**Total: 9 weeks** (vs 8 weeks original)

### 6.2 Technology Stack Update

**Core Dependencies**:
```toml
[dependencies]
# Git integration
git2 = "0.18"                    # libgit2 bindings
git-lfs = "0.3"                  # LFS support

# Storage (index only)
rocksdb = "0.21"                 # Local query index
tantivy = "0.21"                 # Fulltext search

# Parsing
pulldown-cmark = "0.9"           # Markdown parser
serde_yaml = "0.9"               # YAML frontmatter

# Graph
petgraph = "0.6"                 # Graph algorithms

# Async runtime
tokio = "1.35"
axum = "0.7"                     # REST API

# CLI
clap = "4.4"                     # Command-line parser
```

---

## 7. API Design

### 7.1 Core API

```rust
use panini_core::{KnowledgeRepo, Concept, Relation, Query};

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize repository
    let repo = KnowledgeRepo::open("~/knowledge")?;
    
    // Create a concept
    let concept = Concept::builder()
        .id("concept_cas_001")
        .dhatu(Dhatu::Text)
        .title("Content-Addressable Storage")
        .content("A storage system where...")
        .tags(&["storage", "distributed"])
        .build()?;
    
    repo.store_concept(concept).await?;
    
    // Create relation
    let relation = Relation::new(
        "concept_cas_001",
        "concept_storage_002",
        RelationType::IsA,
    );
    
    repo.add_relation(relation).await?;
    
    // Query
    let results = repo.query(
        Query::builder()
            .tags(&["storage"])
            .dhatu(Dhatu::Text)
            .fulltext("distributed")
            .build()
    ).await?;
    
    for concept in results {
        println!("{}: {}", concept.id, concept.title);
    }
    
    // Sync
    repo.sync().await?;  // Pull from all remotes, push changes
    
    Ok(())
}
```

### 7.2 CLI Interface

```bash
# Initialize new knowledge repo
panini init ~/knowledge --template=personal

# Add public knowledge submodule
panini add-remote public https://github.com/panini-community/shared-concepts.git

# Create concept
panini create concept --title "CAS" --tags storage,distributed

# Edit concept
panini edit concept_cas_001

# Link concepts
panini link concept_cas_001 --is-a-> concept_storage_002

# Query
panini search "distributed storage" --dhatu=TEXT --tags=storage

# Graph visualization
panini graph concept_cas_001 --depth=2 --output=graph.dot

# Sync
panini sync  # Pull all remotes, push changes

# Status
panini status  # Show modified concepts, pending syncs
```

### 7.3 REST API

```
POST   /api/v2/concepts              Create concept
GET    /api/v2/concepts/:id          Get concept
PUT    /api/v2/concepts/:id          Update concept
DELETE /api/v2/concepts/:id          Delete concept

POST   /api/v2/relations             Create relation
GET    /api/v2/relations/:id         Get relation

GET    /api/v2/query                 Query knowledge graph
  ?tags=storage,distributed
  &dhatu=TEXT
  &fulltext=content-addressable

POST   /api/v2/sync                  Sync repositories
GET    /api/v2/sync/status           Sync status

GET    /api/v2/graph/:id             Get subgraph
  ?depth=2
  &relations=is_a,related_to
```

---

## 8. Migration Path from Phases 1-6

### 8.1 What to Keep

✅ **Constitution (563 lines)**:
- 7 Dhātu primitives → Now file types in Git
- Quality standards → Still applicable
- Testing requirements → Still 80%+ coverage
- Performance targets → Different but still relevant

✅ **Specification Concepts**:
- Dhātu taxonomy → Knowledge representation formats
- Metadata extraction → Still needed for binary content
- API versioning → /api/v2/ for Git-native

✅ **Technology Stack (Partial)**:
- Rust + TypeScript → Keep
- Axum REST API → Keep
- CI/CD pipeline → Keep
- Docker deployment → Keep

### 8.2 What to Replace

🔄 **Storage Layer**:
- ❌ RocksDB for content → Git repositories
- ✅ RocksDB for index only → Keep for queries

🔄 **CAS Operations**:
- ❌ store/retrieve by hash → Git commit/checkout
- ✅ Hash verification → Git's built-in integrity

🔄 **API Endpoints**:
- ❌ /store, /retrieve → /concepts CRUD
- ❌ /extract → Metadata in YAML frontmatter
- ✅ /query → Enhanced with graph traversal

### 8.3 Respec Required

**New Constitution (Phase 2.0)**:
1. Project Vision: Distributed knowledge graph system
2. Core Principles:
   - Git-native storage
   - Hierarchical permissions (submodules)
   - Human-readable formats (Markdown)
   - Full version control
3. Technology Stack:
   - Git (git2-rs) + RocksDB (index) + Tantivy (search)
   - Rust + TypeScript
   - Markdown + YAML
4. Quality Standards:
   - 80%+ test coverage
   - Git commit conventions
   - Schema validation

**New Specification (Phase 2.0)**:
1. Repository structure
2. File formats (Markdown, YAML)
3. Relation types and schema
4. Sync protocols
5. Query language

**New Plan (Phase 2.0)**:
- 9 weeks implementation
- 65-70 tasks
- Git-native architecture

---

## 9. Risks & Mitigations

### 9.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Git performance with 100k+ files | Medium | High | Shard into multiple repos, use index |
| Merge conflicts on structured data | High | Medium | Custom merge drivers, conflict UI |
| Sync latency with large repos | Medium | Medium | Shallow clones, partial checkout |
| Git LFS costs (if used) | Low | Low | Use external content store (S3/IPFS) |
| Schema evolution breaking changes | Medium | High | Version schema, migration scripts |

### 9.2 Schedule Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Git2-rs learning curve | Medium | Prototype in week 1 |
| Conflict resolution complexity | High | Start simple, iterate |
| Submodule UX challenges | Medium | Good CLI design |

---

## 10. Success Criteria

### 10.1 MVP (Minimum Viable Product)

After 9 weeks, system must support:

✅ **Core Operations**:
- [ ] Create/read/update/delete concepts (Markdown files)
- [ ] Link concepts with typed relations
- [ ] Query by tags, dhātu, fulltext
- [ ] Sync with remote repositories
- [ ] Manage submodules (add/remove/update)

✅ **Multi-User**:
- [ ] Private user repos
- [ ] Shared public repo (submodule)
- [ ] Team repos (submodule with SSH)

✅ **Developer Experience**:
- [ ] CLI tool (10+ commands)
- [ ] REST API (10+ endpoints)
- [ ] Rust library crate
- [ ] Documentation site

✅ **Quality**:
- [ ] 80%+ test coverage
- [ ] CI/CD pipeline
- [ ] Benchmarks (query performance)

### 10.2 Non-Goals (v1.0)

❌ Out of scope for initial release:
- Web UI (CLI + API only)
- Real-time collaboration
- AI-powered suggestions
- Mobile apps
- GraphQL API

---

## 11. Next Steps

### 11.1 Immediate Actions

1. **Create new constitution** (2 days)
   - Define Git-native vision
   - Update technology stack
   - Redefine dhātu semantics

2. **Create new specification** (3 days)
   - Repository structure
   - File format schemas
   - API design
   - Sync protocols

3. **Create new plan** (2 days)
   - 9-week roadmap
   - Task breakdown (65-70 tasks)
   - Dependency graph

4. **Prototype** (1 week)
   - Git2-rs basic operations
   - Markdown + YAML parsing
   - Simple concept storage
   - Validate approach

5. **Review & Approve** (2 days)
   - Stakeholder review
   - Architecture validation
   - Timeline approval

**Total Respec Time**: ~2 weeks before implementation starts

---

## 12. Decision Point

**This pivot requires stakeholder approval due to**:
1. ✅ Complete architecture change
2. ⏱️ +1 week implementation time (9 vs 8 weeks)
3. 📋 2 weeks respec effort
4. 🎯 Different target use case

**Benefits justify pivot**:
1. ✅ Distributed, versioned knowledge = strategic advantage
2. ✅ Git ecosystem = proven collaboration model
3. ✅ Submodules = elegant permission system
4. ✅ Future-proof (knowledge evolution tracked)

**Recommendation**: ✅ **APPROVE PIVOT**

---

**Author**: GitHub Copilot  
**Review Status**: ⏳ Pending Stakeholder Approval  
**Target Start**: After approval (2-week respec → 9-week implementation)

