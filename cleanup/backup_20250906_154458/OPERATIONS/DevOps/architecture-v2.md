# PaniniFS-2 Architecture

## General Vision

PaniniFS-2 is a Git-based virtual file system that decomposes information into universal semantic atoms. Each piece of data is associated with its authors/proposers/affirmers and can be recombined according to different perspectives.

## Conceptual Model

### Semantic Atoms
- **Extended RDF triplet**: Subject-Predicate-Object + Context + Provenance
- **Universality**: Maximum reuse across domains
- **Versioning**: Evolution of concepts via Git

### Repository Hierarchy
```
/semantic-universe/          # Public repo: universal concepts
  /core-concepts/
  /languages/
  /relationships/
  
/domain-specific/            # Semi-public repos: domains
  /science/
  /technology/
  /arts/
  
/private-instances/          # Private repos: personal data
  /user-data/
  /local-interpretations/
```

### Data Model

```rust
// Basic semantic atom
struct SemanticAtom {
    id: AtomId,
    content: Content,
    authors: Vec<AuthorId>,
    provenance: GitCommit,
    relationships: Vec<Relationship>,
    confidence: f64,
}

// Relationship between atoms
struct Relationship {
    predicate: PredicateType,
    target: AtomId,
    strength: f64,
    context: Option<ContextId>,
}
```

## Technical Architecture

### Layers
1. **VFS Layer** (FUSE): Filesystem interface
2. **Semantic Layer**: Atom business logic
3. **Git Storage Layer**: Persistence and versioning
4. **Query Engine**: Conversational queries

### Interfaces
- **Filesystem**: Classic hierarchical navigation
- **Conversation**: Natural language queries
- **REST API**: Integration with other tools
- **Web Interface**: Graphical visualization of relationships

## Data Flow

### Writing
1. File written to VFS → Semantic analyzer
2. Decomposition into atoms → Duplicate search
3. Optimized storage → Git commit with metadata
4. Local index updated → Remote repo synchronization

### Reading
1. VFS/conversation query → Query Engine
2. Index search → Contextual reconstruction
3. View generation → User presentation

## Technical Challenges

- **Performance**: Efficient index for billions of atoms
- **Consistency**: Multi-repo synchronization
- **Privacy**: Public/private separation
- **Scalability**: Data structure migration
