# Constitution v2.0 - Panini-FS Git-Native Knowledge Graph

**Version**: 2.0.0-draft  
**Date**: 2025-10-29  
**Status**: 🔄 DRAFT - Architecture Pivot  
**Previous Version**: [v1.0 (RocksDB-based)](./constitution.md)

---

## 1. Project Vision

### 1.1 Mission Statement

**Panini-FS v2.0** is a **distributed, versioned knowledge graph system** that enables individuals and teams to build, share, and collaborate on structured knowledge using Git as the foundational storage and versioning layer.

**Core Principle**: *"Every piece of knowledge has a history, every connection has a reason, and every user owns their truth."*

### 1.2 Strategic Goals

1. **Distributed Ownership**: Each user maintains complete control over their knowledge repository
2. **Selective Sharing**: Fine-grained permissions via Git submodules (private/team/public)
3. **Full Provenance**: Git history provides complete audit trail of knowledge evolution
4. **Collaborative Intelligence**: Pull request workflow for knowledge contribution and review
5. **Offline-First**: Full functionality without network connectivity
6. **Human-Readable**: All knowledge stored in Markdown and YAML (diff-friendly, grep-able)

### 1.3 Inspiration from Panini

The Sanskrit grammarian **Panini** (पाणिनि, ~5th century BCE) created the **Ashtadhyayi** (अष्टाध्यायी), a generative grammar of Sanskrit consisting of ~4000 rules (sutras). Key parallels:

| Panini's Grammar | Panini-FS v2.0 |
|-----------------|----------------|
| Sutras (rules) | Concepts (knowledge nodes) |
| Metalanguage | Relation types & schemas |
| Derivational history | Git commit history |
| Contextual rules | Submodule hierarchy |
| Compositional | Graph-based knowledge |

---

## 2. Core Primitives

### 2.1 The Seven Dhātus (Redefined)

In v1.0, dhātus were content types. In v2.0, **dhātus are knowledge representation formats**:

| Dhātu | Format | Use Case | Example |
|-------|--------|----------|---------|
| **TEXT** | Markdown + YAML | Conceptual knowledge, documentation | `concept_cas.md` |
| **IMAGE** | PNG/JPEG/SVG + metadata | Visual knowledge, diagrams | `architecture_diagram.png` |
| **VIDEO** | MP4/WebM + metadata | Temporal knowledge, lectures | `lecture_distributed_systems.mp4` |
| **AUDIO** | MP3/FLAC + metadata | Auditory knowledge, podcasts | `interview_linus_torvalds.mp3` |
| **CODE** | Source files + metadata | Executable knowledge, algorithms | `quicksort.rs`, `neural_network.py` |
| **BINARY** | Executables + metadata | Compiled knowledge, models | `trained_model.onnx` |
| **ARCHIVE** | ZIP/TAR + metadata | Packaged knowledge, datasets | `dataset_imagenet.tar.gz` |

**Key Change**: Dhātus now describe *how knowledge is represented*, not just content type.

### 2.2 Knowledge Components

**Primary Building Blocks**:

1. **Concept**: A discrete unit of knowledge
   - File: `knowledge/concepts/{name}.md`
   - Format: Markdown with YAML frontmatter
   - Content: Title, definition, explanation, examples, references

2. **Relation**: A typed link between concepts
   - File: `knowledge/relations/{type}.yaml`
   - Types: `is_a`, `part_of`, `related_to`, `uses`, `contradicts`, etc.
   - Attributes: Confidence, bidirectionality, evidence

3. **Metadata**: Contextual information
   - File: `knowledge/metadata/{type}.yaml`
   - Types: Tags, authors, status, visibility
   - Purpose: Filtering, searching, organization

4. **Content**: Binary or large files
   - Storage: Git LFS or external (S3, IPFS)
   - Reference: SHA-256 hash in concept frontmatter
   - Extractors: Automated metadata extraction

### 2.3 Repository Hierarchy

**Three-Tier Model**:

```
Tier 1: Private User Repository
├── All personal knowledge
├── Configuration (.panini/)
└── Submodules → Tier 2 & 3

Tier 2: Team Repositories (Submodules)
├── Shared project knowledge
├── Access via SSH keys
└── Team-specific permissions

Tier 3: Public Repositories (Submodules)
├── Common knowledge base
├── Access via HTTPS
└── Open collaboration
```

**Example Hierarchy**:
```
stephane/knowledge-base/              # Tier 1: Private
├── .panini/                          # Local config & index
├── knowledge/
│   ├── public/                       # Tier 3: Submodule
│   │   └── .git/ → github.com/panini-community/shared
│   ├── work_acme/                    # Tier 2: Submodule
│   │   └── .git/ → git@github.com:acme-corp/team-knowledge.git
│   └── personal/                     # Tier 1: Direct
│       ├── concepts/
│       ├── relations/
│       └── content/
└── .git/
```

---

## 3. Architectural Principles

### 3.1 Git-First Design

**All operations must leverage Git semantics**:

| Operation | Git Equivalent | Benefit |
|-----------|---------------|---------|
| Create concept | `git commit` | Atomic, versioned |
| Update concept | `git commit` + `git log` | Full history |
| Delete concept | `git rm` + `git commit` | Recoverable |
| Link concepts | `git commit` (relation file) | Versioned relationships |
| Share knowledge | `git push` | Distributed |
| Collaborate | `git pull` + `git merge` | Proven workflow |
| Branch | `git branch` | Parallel exploration |
| Tag milestone | `git tag` | Version landmarks |

**Constraint**: No operation should require a database write without a corresponding Git commit.

### 3.2 Local-First Performance

**Problem**: Git operations can be slow on large repositories.

**Solution**: Local RocksDB index for queries.

```
┌──────────────────────────────────────┐
│  Query (fast path)                   │
│  - Fulltext search                   │
│  - Graph traversal                   │
│  - Tag filtering                     │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Local Index (RocksDB + Tantivy)     │
│  - Automatically synced              │
│  - Git hooks trigger reindex         │
│  - Eventual consistency OK           │
└──────────┬───────────────────────────┘
           │
           ▼ (on index miss)
┌──────────────────────────────────────┐
│  Git Repository (source of truth)    │
│  - Always authoritative              │
│  - Slow but correct                  │
└──────────────────────────────────────┘
```

**Guarantee**: Index can be deleted and rebuilt from Git at any time.

### 3.3 Schema Evolution

**Challenge**: Knowledge schema will evolve over time.

**Strategy**: Versioned schemas with migration scripts.

```yaml
# .panini/schema.yaml
version: 2.1.0
compatibleWith:
  - 2.0.0
  - 2.1.0

concept:
  required:
    - id
    - type
    - dhatu
    - title
  optional:
    - tags
    - relations
    - content_refs
    - status
    - visibility

relation:
  required:
    - id
    - from
    - to
    - type
  optional:
    - confidence
    - bidirectional
    - evidence
```

**Migration Path**:
```bash
# Automatic migration on schema update
panini migrate --from=2.0.0 --to=2.1.0
# Creates migration commit with all file updates
```

### 3.4 Conflict Resolution

**Git merge conflicts are inevitable in collaborative knowledge.**

**Strategies**:

1. **Automatic** (90% of cases):
   - Disjoint edits → Auto-merge
   - Same field, different values → Timestamp wins
   - Relation additions → Union

2. **Semi-Automatic** (8% of cases):
   - Custom merge driver for YAML frontmatter
   - Confidence score adjustment on conflicts
   - Flagged for review (status: `conflicted`)

3. **Manual** (2% of cases):
   - Semantic conflicts (contradictory claims)
   - UI for side-by-side comparison
   - Expert review required

**Example Conflict**:
```yaml
# Concept A: Stephen says "CAS is immutable"
# Concept B: Alice says "CAS supports updates"

# Resolution:
---
status: conflicted
conflict_resolution:
  - author: stephen@example.com
    claim: "CAS is immutable"
    evidence: [url1, url2]
  - author: alice@example.com
    claim: "CAS supports updates"
    evidence: [url3]
  resolution: pending_review
---
```

---

## 4. Technology Stack

### 4.1 Core Technologies

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Storage** | Git | 2.40+ | Industry-standard VCS |
| **Git Bindings** | git2-rs | 0.18 | Rust libgit2 wrapper |
| **Query Index** | RocksDB | 0.21 | Fast key-value store |
| **Fulltext Search** | Tantivy | 0.21 | Pure Rust search engine |
| **Parsing** | pulldown-cmark | 0.9 | Markdown parser |
| **YAML** | serde_yaml | 0.9 | YAML parsing |
| **Graph** | petgraph | 0.6 | Graph algorithms |
| **API** | Axum | 0.7 | Async HTTP framework |
| **Runtime** | Tokio | 1.35 | Async runtime |
| **CLI** | Clap | 4.4 | Command-line parser |

### 4.2 Language Choices

**Backend: Rust**
- ✅ Memory safety without GC
- ✅ Performance (near C++)
- ✅ Rich crate ecosystem (git2, rocksdb, tantivy)
- ✅ Excellent error handling
- ✅ Async/await support

**Frontend: TypeScript** (future, not v1.0)
- ✅ Type safety
- ✅ React ecosystem
- ✅ VS Code integration

**Configuration: YAML**
- ✅ Human-readable
- ✅ Comments supported
- ✅ Standard for metadata

**Content: Markdown**
- ✅ Git-friendly diffs
- ✅ Plain text
- ✅ Widely supported
- ✅ Extensible (frontmatter, custom blocks)

### 4.3 Optional Dependencies

**Large File Storage**:
- Git LFS (GitHub-hosted)
- S3-compatible (self-hosted)
- IPFS (decentralized)

**Content Delivery**:
- CloudFlare (CDN)
- GitHub Pages (static hosting)

---

## 5. Design Decisions

### 5.1 Why Markdown + YAML?

**Alternatives Considered**:
1. ❌ JSON: No comments, harder to diff
2. ❌ XML: Verbose, poor Git diffs
3. ❌ TOML: Good, but YAML more standard
4. ✅ **Markdown + YAML frontmatter**: Best of both worlds

**Benefits**:
- Human-readable and writable
- Excellent Git diffs (line-based)
- Comments supported (YAML)
- Rich content (Markdown)
- Standard tooling (VS Code, GitHub preview)

### 5.2 Why Git Submodules?

**Alternatives Considered**:
1. ❌ Monorepo: No permission boundaries
2. ❌ Git subtrees: Harder to maintain
3. ❌ Manual multi-repo: Complex sync
4. ✅ **Git submodules**: Natural permission model

**Benefits**:
- Each submodule = separate repository = separate permissions
- Public/private/team boundaries enforced by Git hosting
- Standard Git workflow (no custom auth system)
- Users can fork/contribute to public knowledge

### 5.3 Why Local Index?

**Alternatives Considered**:
1. ❌ Pure Git (no index): Too slow for queries
2. ❌ Server-side index: Requires always-online
3. ✅ **Local RocksDB + Tantivy**: Fast, offline, rebuil dable

**Trade-offs**:
- ✅ Sub-millisecond queries
- ✅ Fulltext search
- ✅ Offline capability
- ⚠️ Disk space (~10-20% of repo size)
- ⚠️ Eventual consistency (acceptable)

### 5.4 Why Rust?

**Alternatives Considered**:
1. ❌ Python: Too slow for indexing large repos
2. ❌ Go: Good, but Rust has better git2 bindings
3. ❌ C++: Memory safety concerns
4. ✅ **Rust**: Performance + safety + ecosystem

---

## 6. Quality Standards

### 6.1 Code Quality

**Enforced via CI/CD**:
- ✅ `cargo fmt` (rustfmt): Code formatting
- ✅ `cargo clippy -- -D warnings`: Linting (zero warnings)
- ✅ `cargo test`: All tests pass
- ✅ `cargo doc --no-deps`: Documentation builds
- ✅ `cargo audit`: No vulnerable dependencies

**Coverage Target**: ≥80% (maintained, not relaxed)

### 6.2 Git Commit Standards

**Convention**: [Conventional Commits](https://www.conventionalcommits.org/)

```
type(scope): subject

body

footer
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code restructure
- `test`: Test addition/modification
- `chore`: Maintenance

**Example**:
```
feat(concept): Add CAS concept with relations

- Created concept_cas_001.md
- Added is_a relation to concept_storage_002
- Added related_to relation to concept_git_004

Refs: #42
```

### 6.3 Schema Validation

**All concepts must validate against schema**:

```bash
# Pre-commit hook
panini validate knowledge/concepts/cas.md
# ✅ Valid concept (schema v2.0.0)
# ✅ All required fields present
# ✅ Relations reference existing concepts
# ✅ Tags exist in taxonomy
```

**Invalid concepts blocked at commit time**.

### 6.4 Testing Strategy

| Test Type | Coverage | Tools |
|-----------|----------|-------|
| **Unit** | 85%+ | cargo test |
| **Integration** | Key flows | tests/integration/ |
| **Property-based** | Git operations | proptest |
| **Performance** | Query latency | criterion benchmarks |
| **E2E** | CLI commands | shell scripts |

**Non-Negotiable**: No PR merges without tests.

---

## 7. Performance Targets

### 7.1 Query Performance

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Fulltext search (1000 concepts) | <50ms | P95 |
| Graph traversal (depth 3) | <20ms | P95 |
| Tag filtering | <10ms | P95 |
| Concept retrieval | <5ms | P95 |
| Index rebuild (1000 concepts) | <2s | P95 |

### 7.2 Git Performance

| Operation | Target | Notes |
|-----------|--------|-------|
| Commit concept | <100ms | Including index update |
| Push to remote | Depends on network | Not measured |
| Pull from remote | Depends on network | Not measured |
| Shallow clone | <5s | For 1000 concepts |
| Submodule update | <10s | For 3 submodules |

### 7.3 Scalability Targets

| Metric | v1.0 Target | v2.0 Stretch |
|--------|-------------|---------------|
| Concepts per repo | 10,000 | 100,000 |
| Relations per concept | 50 | 500 |
| Submodules per user | 10 | 100 |
| Users collaborating | 100 | 10,000 |

**Scaling Strategy**: If single repo exceeds targets, shard into multiple repos.

---

## 8. Security & Privacy

### 8.1 Permission Model

**Enforced by Git hosting** (GitHub, GitLab, etc.):

| Repository Type | Access Control | Mechanism |
|----------------|---------------|-----------|
| Private user repo | Owner only | Private GitHub repo |
| Team repo | Team members | GitHub org/team |
| Public repo | Everyone (read) | Public GitHub repo |

**Write Access**:
- Private: Owner only
- Team: Team members (managed by org admins)
- Public: Contributors via PR (maintainer approval)

### 8.2 Data At Rest

**Private repositories**:
- ✅ Encrypted by Git hosting (GitHub: AES-256)
- ✅ Local clone: OS filesystem encryption recommended
- ✅ Backups: User responsibility (git push = backup)

**Public repositories**:
- ⚠️ Visible to everyone
- ⚠️ Permanent (even if deleted, forks may exist)
- ⚠️ No sensitive data should ever be committed

### 8.3 Data In Transit

**All Git operations over HTTPS or SSH**:
- ✅ TLS 1.3 for HTTPS
- ✅ SSH keys for private repos
- ✅ GitHub tokens with scoped permissions

### 8.4 Sensitive Information

**CRITICAL**: Never commit secrets/credentials/PII.

**Safeguards**:
- Pre-commit hook to detect common secrets
- `.gitignore` for sensitive files
- Git history rewriting for accidents (BFG, git-filter-repo)

**If leaked**:
1. Rotate credentials immediately
2. Rewrite Git history
3. Force push (risky, but necessary)
4. Notify affected parties

---

## 9. Deployment Model

### 9.1 Distribution

**Panini-FS is a client-side tool**, not a hosted service.

**Deployment Options**:

1. **Desktop Application** (v1.0):
   - CLI tool (`panini-cli`)
   - Library crate (`panini-core`)
   - Rust binary (single executable)

2. **Server API** (v1.5, optional):
   - REST API for web clients
   - Runs locally or on VPS
   - Wraps CLI functionality

3. **VS Code Extension** (v2.0, future):
   - Inline concept editing
   - Graph visualization
   - Query UI

### 9.2 Installation

```bash
# Cargo (Rust package manager)
cargo install panini-cli

# Homebrew (macOS/Linux)
brew install panini

# Binary download (all platforms)
curl -sSL https://get.panini.dev | sh
```

### 9.3 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Linux/macOS/Windows 10+ | Linux/macOS |
| Rust | 1.70+ | 1.75+ |
| RAM | 512MB | 2GB |
| Disk | 100MB + repo size | SSD recommended |
| Git | 2.30+ | 2.40+ |

---

## 10. Roadmap

### 10.1 Version 1.0 (9 weeks)

**MVP Features**:
- ✅ Concept CRUD (create, read, update, delete)
- ✅ Relation management (typed links)
- ✅ Query (tags, dhātu, fulltext)
- ✅ Sync (pull/push with remotes)
- ✅ Submodule management (add/remove/update)
- ✅ CLI tool (20+ commands)
- ✅ REST API (15+ endpoints)
- ✅ Local index (RocksDB + Tantivy)

**Out of Scope**:
- ❌ Web UI
- ❌ Real-time collaboration
- ❌ AI features
- ❌ Mobile apps

### 10.2 Version 1.5 (4-6 weeks after 1.0)

- Graph visualization (DOT export, D3.js)
- Advanced queries (graph patterns, path finding)
- Conflict resolution UI
- Import/export (JSON, CSV, RDF)

### 10.3 Version 2.0 (6-9 months after 1.0)

- Web UI (React + TypeScript)
- Real-time collaboration (WebRTC)
- AI-powered suggestions (concept generation, relation inference)
- Mobile apps (React Native)
- Federation (knowledge exchange protocol)

---

## 11. Success Criteria

### 11.1 Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test coverage | ≥80% | cargo tarpaulin |
| Query performance | <50ms P95 | criterion benchmarks |
| CLI commands | 20+ | Feature complete |
| API endpoints | 15+ | REST API coverage |
| Documentation | 100% public API | cargo doc |

### 11.2 User Experience Metrics

| Metric | Target | Method |
|--------|--------|--------|
| Onboarding time | <15 min | User testing |
| Concept creation time | <2 min | User testing |
| Query satisfaction | >80% | Survey |
| Sync reliability | >99% | Telemetry (opt-in) |

### 11.3 Community Metrics

| Metric | v1.0 Target | v2.0 Target |
|--------|-------------|-------------|
| GitHub stars | 100+ | 1000+ |
| Contributors | 5+ | 25+ |
| Public knowledge repos | 10+ | 100+ |
| Active users | 50+ | 500+ |

---

## 12. Non-Goals (Explicitly Out of Scope)

❌ **Not Building**:
1. Web hosting service (users self-host or use GitHub)
2. AI training on user data (privacy-first)
3. Blockchain/crypto integration (not needed)
4. Enterprise SSO/SAML (v1.0)
5. Windows GUI (CLI first)

---

## 13. Open Questions

⏳ **To be resolved during respec**:

1. **Relation schema**: Fixed types vs. user-defined?
2. **Content storage**: Git LFS vs. external (S3/IPFS)?
3. **Conflict resolution**: How much automation?
4. **Fulltext search**: Tantivy limitations with non-English?
5. **Mobile strategy**: Native apps or PWA?

---

## 14. Approval

**Required Sign-Off**:
- [ ] Project stakeholder (Stéphane)
- [ ] Technical lead (TBD)
- [ ] Community review (GitHub Discussions)

**Approval Timeline**:
- Draft: 2025-10-29
- Review: 1 week
- Approval: TBD
- Implementation start: After approval + 1 week respec

---

**Document Owner**: GitHub Copilot  
**Last Updated**: 2025-10-29  
**Next Review**: After specification v2.0 complete

