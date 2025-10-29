# Panini-FS Constitution

**Project**: Panini-FS - Content-Addressed Semantic Filesystem  
**Created**: 2025-10-28  
**Version**: 1.0.0

---

## 🎯 Project Vision

Panini-FS is a revolutionary content-addressed filesystem with semantic compression capabilities, based on the discovery of **7 universal semantic primitives (dhātu)** present in all information:

1. **TEXT** - Human language, markup, structured text
2. **IMAGE** - Visual data, graphics, photos
3. **VIDEO** - Motion pictures, animations
4. **AUDIO** - Sound, music, speech
5. **CODE** - Programming languages, scripts
6. **BINARY** - Compiled executables, machine code
7. **ARCHIVE** - Compressed containers, packages

The system provides native deduplication through semantic hashing and enables unprecedented compression ratios by leveraging information theory and linguistic principles.

---

## 🏗️ Architectural Principles

### 1. Type Safety First
- **Rust Backend**: Leverage Rust's type system for compile-time guarantees
- **Zero Panics**: All errors must be properly handled with `Result<T, E>`
- **TypeScript Client**: Full type definitions for all API interactions
- **Serde Serialization**: Type-safe data serialization/deserialization

### 2. Performance & Efficiency
- **Zero-Copy Operations**: Minimize memory allocations and copies
- **Async Runtime**: Tokio for high-performance concurrency
- **Embedded Storage**: RocksDB for fast key-value access
- **Content Addressing**: Native deduplication at the storage layer
- **Lazy Evaluation**: Load and process data only when needed

### 3. Reliability & Correctness
- **Immutable Data**: Content-addressed storage prevents tampering
- **Atomic Operations**: All storage operations are atomic
- **Error Recovery**: Graceful degradation and retry mechanisms
- **Data Integrity**: Hash verification for all content

### 4. Developer Experience
- **Clear APIs**: RESTful endpoints with intuitive naming
- **Comprehensive Docs**: Auto-generated API documentation
- **Type Hints**: Full IntelliSense support in TypeScript client
- **Examples**: Working code samples for common use cases

---

## 🔧 Technology Stack

### Backend (Rust)

**Core Framework**:
- **Language**: Rust 1.70+ (2021 edition)
- **Runtime**: Tokio (async/await)
- **Web Framework**: Axum (type-safe routing)
- **Serialization**: Serde (JSON support)

**Storage Layer**:
- **Database**: RocksDB (embedded key-value store)
- **Content Addressing**: SHA-256 hashing
- **Indexing**: In-memory caching for hot data

**Key Dependencies**:
```toml
tokio = { version = "1.35", features = ["full"] }
axum = "0.7"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
rocksdb = "0.21"
sha2 = "0.10"
blake3 = "1.5"  # Fast hashing for content addressing
anyhow = "1.0"  # Error handling
tracing = "0.1"  # Structured logging
```

### Client (TypeScript)

**Framework**:
- **Language**: TypeScript 5.0+
- **Runtime**: Node.js 18+ / Browser
- **HTTP Client**: Axios (with interceptors)
- **Build Tool**: esbuild (fast compilation)

**Key Dependencies**:
```json
{
  "axios": "^1.6.0",
  "typescript": "^5.0.0",
  "esbuild": "^0.19.0"
}
```

---

## 📐 Design Decisions

### Storage Architecture

**Decision**: Use RocksDB as embedded database
- **Rationale**: Single binary deployment, no external DB required
- **Trade-offs**: Limited to single-node (acceptable for v1.0)
- **Future**: Consider distributed storage for multi-node

**Decision**: SHA-256 for content addressing
- **Rationale**: Industry standard, good balance of speed/security
- **Trade-offs**: Slower than BLAKE3 but more widely trusted
- **Alternative**: BLAKE3 for performance-critical paths

### API Design

**Decision**: REST over HTTP/JSON
- **Rationale**: Universal compatibility, easy debugging
- **Trade-offs**: Slightly slower than gRPC/binary protocols
- **Future**: Add gRPC support for high-throughput scenarios

**Endpoints**:
```
POST   /api/v1/store        - Store content, return CAS hash
GET    /api/v1/content/:hash - Retrieve content by hash
POST   /api/v1/extract      - Extract dhātu from content
GET    /api/v1/dhatu/:hash  - Get dhātu metadata
GET    /api/v1/stats        - System statistics
```

### Error Handling

**Decision**: Structured error types with proper HTTP status codes
```rust
#[derive(Debug, thiserror::Error)]
pub enum PaniniError {
    #[error("Content not found: {0}")]
    NotFound(String),           // 404
    
    #[error("Invalid content format: {0}")]
    InvalidFormat(String),      // 400
    
    #[error("Storage error: {0}")]
    StorageError(String),       // 500
    
    #[error("Extraction failed: {0}")]
    ExtractionError(String),    // 500
}
```

### Concurrency Model

**Decision**: Async/await with Tokio runtime
- **Rationale**: Non-blocking I/O for high throughput
- **Trade-offs**: Slightly more complex than sync code
- **Pattern**: Use `tokio::spawn` for CPU-intensive work

---

## 🧪 Testing Strategy

### Test Coverage Requirements

**Minimum Coverage**: 80% for all modules
- **Critical Paths**: 100% coverage (storage, CAS, extractors)
- **API Endpoints**: Integration tests for all routes
- **Error Cases**: Test all error handling paths

### Test Types

**1. Unit Tests** (Rust)
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_content_addressing() {
        let content = b"Hello, Panini!";
        let hash = compute_hash(content);
        assert_eq!(hash.len(), 64); // SHA-256 hex
    }
}
```

**2. Integration Tests** (Rust)
```rust
#[tokio::test]
async fn test_store_and_retrieve() {
    let store = Storage::new_temp().await.unwrap();
    let content = b"test data";
    let hash = store.put(content).await.unwrap();
    let retrieved = store.get(&hash).await.unwrap();
    assert_eq!(content, retrieved.as_slice());
}
```

**3. API Tests** (TypeScript)
```typescript
describe('Panini API', () => {
  test('store content returns valid hash', async () => {
    const client = new PaniniClient();
    const content = Buffer.from('test');
    const hash = await client.store(content);
    expect(hash).toMatch(/^[a-f0-9]{64}$/);
  });
});
```

**4. Property-Based Tests** (Rust + proptest)
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_hash_deterministic(content in ".*") {
        let hash1 = compute_hash(content.as_bytes());
        let hash2 = compute_hash(content.as_bytes());
        prop_assert_eq!(hash1, hash2);
    }
}
```

---

## 📝 Code Quality Standards

### Rust Code Style

**Formatting**: Use `rustfmt` (2021 edition)
```toml
# rustfmt.toml
edition = "2021"
max_width = 100
use_small_heuristics = "Max"
```

**Linting**: Use `clippy` with strict settings
```toml
# Cargo.toml
[lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"

[lints.clippy]
all = "warn"
pedantic = "warn"
```

**Documentation**: All public APIs must have doc comments
```rust
/// Stores content in the content-addressed storage.
///
/// # Arguments
/// * `content` - The raw bytes to store
///
/// # Returns
/// Returns the SHA-256 hash of the content as a hex string
///
/// # Errors
/// Returns `PaniniError::StorageError` if storage fails
pub async fn store(&self, content: &[u8]) -> Result<String, PaniniError>
```

### TypeScript Code Style

**Formatting**: Use Prettier
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 100
}
```

**Linting**: Use ESLint with TypeScript rules
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

---

## 🚀 Performance Targets

### Backend Performance

**Throughput**:
- Store operations: >1000 ops/sec (small files <1MB)
- Retrieve operations: >5000 ops/sec (cached)
- Extract operations: >100 ops/sec (depending on dhātu type)

**Latency**:
- P50: <10ms (store/retrieve)
- P95: <50ms
- P99: <100ms

**Resource Usage**:
- Memory: <500MB baseline, <2GB under load
- CPU: <80% average, <100% P95
- Disk I/O: Optimized sequential writes

### Client Performance

**Bundle Size**:
- Minified: <50KB (core client)
- Gzipped: <15KB

**Network**:
- Connection pooling (max 10 concurrent)
- Automatic retry with exponential backoff
- Request timeout: 30s default

---

## 🔒 Security Guidelines

### Input Validation

**All user input must be validated**:
- Content size limits (configurable, default 100MB)
- Hash format validation (64-char hex for SHA-256)
- Path traversal prevention
- Sanitize all error messages (no internal paths)

### Content Security

**Hash Verification**:
```rust
pub fn verify_content(content: &[u8], expected_hash: &str) -> Result<(), PaniniError> {
    let actual_hash = compute_hash(content);
    if actual_hash != expected_hash {
        return Err(PaniniError::HashMismatch {
            expected: expected_hash.to_string(),
            actual: actual_hash,
        });
    }
    Ok(())
}
```

**No Sensitive Data in Logs**:
- Never log content or hashes in production
- Use structured logging with appropriate levels
- Sanitize all user-provided strings

---

## 📦 Deployment Strategy

### Build Configuration

**Release Profile** (Cargo.toml):
```toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

**Docker Support**:
```dockerfile
FROM rust:1.70-slim as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=builder /app/target/release/panini-fs /usr/local/bin/
EXPOSE 8080
CMD ["panini-fs"]
```

### Configuration

**Environment Variables**:
```bash
PANINI_PORT=8080              # Server port
PANINI_STORAGE_PATH=/data     # Storage directory
PANINI_LOG_LEVEL=info         # Log level (trace/debug/info/warn/error)
PANINI_MAX_CONTENT_SIZE=100MB # Max upload size
```

**Configuration File** (optional TOML):
```toml
[server]
host = "0.0.0.0"
port = 8080

[storage]
path = "/var/lib/panini-fs"
cache_size_mb = 256

[limits]
max_content_size_mb = 100
max_concurrent_requests = 1000
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

**On Push**:
1. Run `cargo fmt --check`
2. Run `cargo clippy -- -D warnings`
3. Run `cargo test --all-features`
4. Run `cargo build --release`
5. Generate coverage report (90%+ required)

**On PR**:
- All above checks must pass
- Require code review approval
- Check for breaking API changes

**On Release Tag**:
- Build release binaries (Linux, macOS, Windows)
- Generate API documentation
- Create GitHub release
- Publish crates to crates.io (future)

---

## 📚 Documentation Requirements

### API Documentation

**OpenAPI Spec**: Generate from code
```yaml
openapi: 3.0.0
info:
  title: Panini-FS API
  version: 1.0.0
paths:
  /api/v1/store:
    post:
      summary: Store content
      requestBody:
        content:
          application/octet-stream:
            schema:
              type: string
              format: binary
      responses:
        '200':
          description: Content stored successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  hash:
                    type: string
                    example: "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447"
```

### Code Examples

**Rust**:
```rust
// Store content
let client = PaniniClient::new("http://localhost:8080");
let content = b"Hello, World!";
let hash = client.store(content).await?;
println!("Stored with hash: {}", hash);

// Retrieve content
let retrieved = client.get(&hash).await?;
assert_eq!(content, retrieved.as_slice());
```

**TypeScript**:
```typescript
// Store and retrieve
const client = new PaniniClient('http://localhost:8080');
const content = Buffer.from('Hello, World!');
const hash = await client.store(content);
const retrieved = await client.get(hash);
console.log(retrieved.toString()); // "Hello, World!"
```

---

## 🎓 Development Workflow

### Setup

1. **Install Rust**: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. **Clone repo**: `git clone https://github.com/stephanedenis/Panini-FS.git`
3. **Build backend**: `cd backend && cargo build`
4. **Run tests**: `cargo test`
5. **Start server**: `cargo run`

### Feature Development

1. Create feature branch: `git checkout -b feature/my-feature`
2. Write tests first (TDD)
3. Implement feature
4. Run all tests: `cargo test && npm test`
5. Format code: `cargo fmt && npm run format`
6. Commit with conventional commits: `feat: add new extractor`
7. Open PR with description and tests

---

## 🎯 Success Metrics

### V1.0 Acceptance Criteria

**Functionality**:
- ✓ Store and retrieve content via CAS
- ✓ Extract all 7 dhātu types
- ✓ REST API with all endpoints
- ✓ TypeScript client library
- ✓ CLI tool for basic operations

**Quality**:
- ✓ >80% test coverage
- ✓ Zero clippy warnings
- ✓ All integration tests pass
- ✓ Performance targets met

**Documentation**:
- ✓ Complete API documentation
- ✓ User guide with examples
- ✓ Architecture decision records
- ✓ Contributing guide

---

## 🔮 Future Considerations

### Phase 2 (Post-V1.0)

**Features**:
- [ ] Distributed storage (multi-node)
- [ ] gRPC API for performance
- [ ] Advanced compression algorithms
- [ ] Semantic search capabilities
- [ ] WebAssembly client

**Optimizations**:
- [ ] BLAKE3 hashing option
- [ ] Memory-mapped files for large content
- [ ] Streaming API for large uploads
- [ ] Delta encoding for similar content

---

**End of Constitution**

This document serves as the foundation for all implementation decisions in Panini-FS. Any deviations from these principles must be documented with clear rationale.
