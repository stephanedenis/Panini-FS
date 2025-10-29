# Implementation Tasks - Panini-FS

**Version**: 1.0
**Date**: 2025-10-29
**Based on**: plan.md v1.0
**Total Tasks**: 72

## Task Organization

This document breaks down the 8-week implementation plan into 72 concrete, implementable tasks. Each task includes:
- **ID**: Unique identifier
- **Title**: Clear, action-oriented description
- **Dependencies**: Which tasks must complete first
- **Size**: S (2-4h), M (4-8h), L (1-2 days), XL (2-3 days)
- **Acceptance Criteria**: Testable conditions for completion
- **Implementation Hints**: Code patterns, gotchas, references

**Task Status Legend**:
- ⏳ Not Started
- 🔄 In Progress
- ✅ Completed
- ⚠️ Blocked

---

## Week 1: Foundation & CAS Core (12 tasks)

### T1.1: Initialize Project Structure ⏳

**Size**: S (2h)  
**Dependencies**: None  
**Owner**: TBD

**Description**: Create complete directory structure for backend and client.

**Acceptance Criteria**:
- [ ] All directories from `plan.md` section 1.1 created
- [ ] Backend structure: `src/{api,cas,dhatu,extractors,health,metrics,utils}`
- [ ] Client structure: `src/utils`, `tests/`, `examples/`
- [ ] Test directories: `tests/{integration,fixtures,common}`
- [ ] Documentation: `docs/`, `docker/`, `.github/workflows/`
- [ ] All paths verified with `tree` command

**Commands**:
```bash
cd /home/stephane/GitHub/Panini-FS
mkdir -p backend/src/{api,cas,dhatu,extractors,health,metrics,utils}
mkdir -p backend/{benches,examples,tests/{integration,fixtures,common},scripts}
mkdir -p client/src/utils client/tests client/examples client/dist
mkdir -p docs docker .github/workflows
```

---

### T1.2: Initialize Cargo Workspace ⏳

**Size**: M (4h)  
**Dependencies**: T1.1  
**Owner**: TBD

**Description**: Set up Cargo.toml with all dependencies from plan.

**Acceptance Criteria**:
- [ ] `backend/Cargo.toml` created with exact dependencies from `plan.md` section 2.1
- [ ] All 15+ crates with correct versions
- [ ] `cargo check` passes without errors
- [ ] `cargo build` succeeds (may fail on missing code)
- [ ] `.rustfmt.toml` and `.clippy.toml` created
- [ ] `rust-toolchain.toml` specifies 1.70+

**Files to Create**:
- `backend/Cargo.toml` (copy from plan.md section 2.1)
- `backend/.rustfmt.toml`
- `backend/.clippy.toml`
- `backend/rust-toolchain.toml`

**Implementation Hints**:
```toml
# rust-toolchain.toml
[toolchain]
channel = "1.75"
components = ["rustfmt", "clippy", "rust-src"]
```

---

### T1.3: Initialize TypeScript Client ⏳

**Size**: S (2h)  
**Dependencies**: T1.1  
**Owner**: TBD

**Description**: Set up TypeScript project with all configuration files.

**Acceptance Criteria**:
- [ ] `client/package.json` created (copy from plan.md section 3.1)
- [ ] `client/tsconfig.json` created (copy from plan.md section 3.2)
- [ ] `client/.eslintrc.json` configured
- [ ] `client/.prettierrc.json` configured
- [ ] `npm install` succeeds
- [ ] `npm run build` succeeds (empty project)

**Files to Create**:
- `client/package.json`
- `client/tsconfig.json`
- `client/.eslintrc.json`
- `client/.prettierrc.json`
- `client/.gitignore`

---

### T1.4: Set Up CI/CD Pipeline ⏳

**Size**: M (4h)  
**Dependencies**: T1.2, T1.3  
**Owner**: TBD

**Description**: Configure GitHub Actions for automated testing.

**Acceptance Criteria**:
- [ ] `.github/workflows/ci.yml` created (copy from plan.md section 11.1)
- [ ] Workflow includes: fmt, clippy, test, coverage
- [ ] Client lint and test jobs configured
- [ ] Push to main triggers workflow
- [ ] PR checks configured

**Files to Create**:
- `.github/workflows/ci.yml`
- `.github/workflows/coverage.yml`
- `.github/workflows/release.yml` (optional, Week 8)

**Implementation Hints**:
- Test locally with `act` tool if available
- Set up Codecov token in repository secrets

---

### T1.5: Implement Config Module ⏳

**Size**: M (4h)  
**Dependencies**: T1.2  
**Owner**: TBD

**Description**: Create configuration management with environment variables.

**Acceptance Criteria**:
- [ ] `src/config.rs` created with `Config` struct
- [ ] All 10 env vars from plan.md section 10.1 supported
- [ ] Default values match specification
- [ ] Validation for size/timeout values
- [ ] Unit tests for parsing and validation
- [ ] `.env.example` created

**Implementation**:
```rust
// src/config.rs
use std::path::PathBuf;

#[derive(Debug, Clone)]
pub struct Config {
    pub storage_path: PathBuf,
    pub max_content_size: usize,
    pub log_level: String,
    pub log_format: LogFormat,
    pub cache_size_mb: usize,
    pub port: u16,
    pub host: String,
    pub shutdown_timeout: u64,
    pub extractor_timeout: u64,
    pub rocksdb_cache_mb: usize,
}

#[derive(Debug, Clone)]
pub enum LogFormat {
    Text,
    Json,
}

impl Config {
    pub fn from_env() -> Result<Self, anyhow::Error> {
        dotenvy::dotenv().ok();
        
        Ok(Self {
            storage_path: std::env::var("PANINI_STORAGE_PATH")
                .unwrap_or_else(|_| "./data".to_string())
                .into(),
            max_content_size: std::env::var("PANINI_MAX_CONTENT_SIZE")
                .unwrap_or_else(|_| "104857600".to_string())
                .parse()?,
            // ... other fields
        })
    }
    
    pub fn validate(&self) -> Result<(), anyhow::Error> {
        if self.max_content_size == 0 {
            anyhow::bail!("max_content_size must be > 0");
        }
        // ... other validations
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_default_config() {
        let config = Config::from_env().unwrap();
        assert_eq!(config.port, 3000);
        assert_eq!(config.max_content_size, 104857600);
    }
    
    #[test]
    fn test_validation() {
        // Test invalid values
    }
}
```

---

### T1.6: Implement Error Types ⏳

**Size**: M (4h)  
**Dependencies**: T1.2  
**Owner**: TBD

**Description**: Define comprehensive error types with RFC 7807 support.

**Acceptance Criteria**:
- [ ] `src/error.rs` created with custom error types
- [ ] `PaniniError` enum covers all error cases
- [ ] RFC 7807 Problem Details JSON serialization
- [ ] HTTP status code mapping
- [ ] Conversion from common errors (io, serde, rocksdb)
- [ ] Unit tests for error formatting

**Implementation**:
```rust
// src/error.rs
use axum::response::{IntoResponse, Response};
use axum::http::StatusCode;
use serde::Serialize;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum PaniniError {
    #[error("Invalid hash format: {0}")]
    InvalidHash(String),
    
    #[error("Content not found: {0}")]
    NotFound(String),
    
    #[error("Content too large: {size} bytes (max: {max})")]
    ContentTooLarge { size: usize, max: usize },
    
    #[error("Storage error: {0}")]
    Storage(#[from] rocksdb::Error),
    
    #[error("Extraction failed: {0}")]
    ExtractionFailed(String),
    
    #[error("Internal error: {0}")]
    Internal(#[from] anyhow::Error),
}

#[derive(Serialize)]
struct ProblemDetails {
    #[serde(rename = "type")]
    error_type: String,
    title: String,
    status: u16,
    detail: String,
    instance: String,
}

impl PaniniError {
    fn status_code(&self) -> StatusCode {
        match self {
            Self::InvalidHash(_) => StatusCode::BAD_REQUEST,
            Self::NotFound(_) => StatusCode::NOT_FOUND,
            Self::ContentTooLarge { .. } => StatusCode::PAYLOAD_TOO_LARGE,
            Self::Storage(_) => StatusCode::INTERNAL_SERVER_ERROR,
            Self::ExtractionFailed(_) => StatusCode::UNPROCESSABLE_ENTITY,
            Self::Internal(_) => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
    
    fn to_problem_details(&self, instance: String) -> ProblemDetails {
        ProblemDetails {
            error_type: format!("https://panini.dev/errors/{}", self.error_type_name()),
            title: self.title(),
            status: self.status_code().as_u16(),
            detail: self.to_string(),
            instance,
        }
    }
}

impl IntoResponse for PaniniError {
    fn into_response(self) -> Response {
        let status = self.status_code();
        let problem = self.to_problem_details("/unknown".to_string());
        (status, axum::Json(problem)).into_response()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_error_status_codes() {
        assert_eq!(
            PaniniError::InvalidHash("bad".into()).status_code(),
            StatusCode::BAD_REQUEST
        );
    }
}
```

---

### T1.7: Implement SHA-256 Hasher ⏳

**Size**: S (3h)  
**Dependencies**: T1.2, T1.6  
**Owner**: TBD

**Description**: Create CAS hasher module with SHA-256 computation.

**Acceptance Criteria**:
- [ ] `src/cas/hasher.rs` created
- [ ] Function `compute_hash(data: &[u8]) -> String` returns lowercase hex
- [ ] Unit tests with known SHA-256 vectors (empty, "abc", random data)
- [ ] Property test: `hash(x) == hash(x)` (deterministic)
- [ ] Performance: <500µs for 1MB input (verified with criterion)

**Implementation**:
```rust
// src/cas/hasher.rs
use sha2::{Sha256, Digest};

pub fn compute_hash(data: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data);
    let result = hasher.finalize();
    hex::encode(result)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_empty_hash() {
        // SHA-256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        let hash = compute_hash(b"");
        assert_eq!(hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
    }
    
    #[test]
    fn test_abc_hash() {
        // SHA-256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
        let hash = compute_hash(b"abc");
        assert_eq!(hash, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    }
    
    #[test]
    fn test_deterministic() {
        let data = b"test data";
        let hash1 = compute_hash(data);
        let hash2 = compute_hash(data);
        assert_eq!(hash1, hash2);
    }
}
```

**Known Vectors**:
- `""` → `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `"abc"` → `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`

---

### T1.8: Implement Hash Validator ⏳

**Size**: S (3h)  
**Dependencies**: T1.6  
**Owner**: TBD

**Description**: Create validation for hash format and path sanitization.

**Acceptance Criteria**:
- [ ] `src/cas/validator.rs` created
- [ ] Function `validate_hash(hash: &str) -> Result<(), PaniniError>`
- [ ] Regex: `^[a-f0-9]{64}$` (SHA-256 hex)
- [ ] Function `sanitize_path(path: &Path) -> Result<PathBuf, PaniniError>`
- [ ] Reject absolute paths and `..` components
- [ ] Full canonicalization
- [ ] Unit tests for valid/invalid cases

**Implementation**:
```rust
// src/cas/validator.rs
use std::path::{Path, PathBuf};
use regex::Regex;
use once_cell::sync::Lazy;
use crate::error::PaniniError;

static HASH_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^[a-f0-9]{64}$").unwrap()
});

pub fn validate_hash(hash: &str) -> Result<(), PaniniError> {
    if !HASH_REGEX.is_match(hash) {
        return Err(PaniniError::InvalidHash(
            format!("Hash must be 64 lowercase hex characters, got: {}", hash)
        ));
    }
    Ok(())
}

pub fn sanitize_path(path: &Path) -> Result<PathBuf, PaniniError> {
    // Reject absolute paths
    if path.is_absolute() {
        return Err(PaniniError::InvalidPath("Absolute paths not allowed".into()));
    }
    
    // Check for .. components
    for component in path.components() {
        if component == std::path::Component::ParentDir {
            return Err(PaniniError::InvalidPath("Parent directory (..) not allowed".into()));
        }
    }
    
    // Canonicalize
    let canonical = path.canonicalize()
        .map_err(|e| PaniniError::InvalidPath(e.to_string()))?;
    
    Ok(canonical)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_valid_hash() {
        let hash = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
        assert!(validate_hash(hash).is_ok());
    }
    
    #[test]
    fn test_invalid_hash_uppercase() {
        let hash = "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD";
        assert!(validate_hash(hash).is_err());
    }
    
    #[test]
    fn test_invalid_hash_short() {
        let hash = "abc123";
        assert!(validate_hash(hash).is_err());
    }
    
    #[test]
    fn test_sanitize_relative_path() {
        let path = Path::new("data/file.txt");
        assert!(sanitize_path(path).is_ok());
    }
    
    #[test]
    fn test_reject_parent_dir() {
        let path = Path::new("../etc/passwd");
        assert!(sanitize_path(path).is_err());
    }
}
```

---

### T1.9: Implement RocksDB Storage ⏳

**Size**: L (8h)  
**Dependencies**: T1.5, T1.6, T1.7  
**Owner**: TBD

**Description**: Create RocksDB wrapper with store/retrieve operations.

**Acceptance Criteria**:
- [ ] `src/cas/storage.rs` created with `Storage` struct
- [ ] RocksDB initialization with LZ4 compression
- [ ] Bloom filters enabled (10 bits per key)
- [ ] Block cache: 256MB default (configurable)
- [ ] Methods: `store(data: &[u8]) -> Result<String>`, `retrieve(hash: &str) -> Result<Vec<u8>>`
- [ ] Key format: `{hash}:content`
- [ ] Hash computed and verified on store
- [ ] Integration test: store + retrieve roundtrip
- [ ] Test with 1KB, 1MB, 10MB data

**Implementation**:
```rust
// src/cas/storage.rs
use rocksdb::{DB, Options, Cache};
use std::path::Path;
use crate::error::PaniniError;
use crate::cas::hasher::compute_hash;

pub struct Storage {
    db: DB,
}

impl Storage {
    pub fn new(path: &Path, cache_size_mb: usize) -> Result<Self, PaniniError> {
        let mut opts = Options::default();
        opts.create_if_missing(true);
        opts.set_compression_type(rocksdb::DBCompressionType::Lz4);
        
        // Block cache
        let cache = Cache::new_lru_cache(cache_size_mb * 1024 * 1024);
        opts.set_row_cache(&cache);
        
        // Bloom filter
        opts.set_bloom_filter(10, false);
        
        let db = DB::open(&opts, path)
            .map_err(PaniniError::Storage)?;
        
        Ok(Self { db })
    }
    
    pub fn store(&self, data: &[u8]) -> Result<String, PaniniError> {
        let hash = compute_hash(data);
        let key = format!("{}:content", hash);
        
        self.db.put(key.as_bytes(), data)
            .map_err(PaniniError::Storage)?;
        
        Ok(hash)
    }
    
    pub fn retrieve(&self, hash: &str) -> Result<Vec<u8>, PaniniError> {
        crate::cas::validator::validate_hash(hash)?;
        
        let key = format!("{}:content", hash);
        
        self.db.get(key.as_bytes())
            .map_err(PaniniError::Storage)?
            .ok_or_else(|| PaniniError::NotFound(hash.to_string()))
    }
    
    pub fn exists(&self, hash: &str) -> Result<bool, PaniniError> {
        let key = format!("{}:content", hash);
        Ok(self.db.get(key.as_bytes())
            .map_err(PaniniError::Storage)?
            .is_some())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[test]
    fn test_store_retrieve_roundtrip() {
        let temp_dir = TempDir::new().unwrap();
        let storage = Storage::new(temp_dir.path(), 64).unwrap();
        
        let data = b"Hello, Panini!";
        let hash = storage.store(data).unwrap();
        
        let retrieved = storage.retrieve(&hash).unwrap();
        assert_eq!(data, retrieved.as_slice());
    }
    
    #[test]
    fn test_retrieve_nonexistent() {
        let temp_dir = TempDir::new().unwrap();
        let storage = Storage::new(temp_dir.path(), 64).unwrap();
        
        let hash = "0000000000000000000000000000000000000000000000000000000000000000";
        let result = storage.retrieve(hash);
        
        assert!(matches!(result, Err(PaniniError::NotFound(_))));
    }
    
    #[test]
    fn test_large_content() {
        let temp_dir = TempDir::new().unwrap();
        let storage = Storage::new(temp_dir.path(), 64).unwrap();
        
        let data = vec![0u8; 10 * 1024 * 1024]; // 10MB
        let hash = storage.store(&data).unwrap();
        let retrieved = storage.retrieve(&hash).unwrap();
        
        assert_eq!(data.len(), retrieved.len());
    }
}
```

---

### T1.10: Implement LRU Cache ⏳

**Size**: M (6h)  
**Dependencies**: T1.6  
**Owner**: TBD

**Description**: Create in-memory LRU cache for frequently accessed content.

**Acceptance Criteria**:
- [ ] `src/cas/cache.rs` created with `ContentCache` struct
- [ ] Uses `lru` crate
- [ ] Configurable size (256MB default)
- [ ] Thread-safe (Arc<Mutex<LruCache>>)
- [ ] Methods: `get(hash: &str)`, `put(hash: String, data: Vec<u8>)`
- [ ] Eviction policy: least recently used
- [ ] Unit tests for cache hit/miss
- [ ] Test eviction on size limit

**Implementation**:
```rust
// src/cas/cache.rs
use lru::LruCache;
use std::sync::{Arc, Mutex};
use std::num::NonZeroUsize;

pub struct ContentCache {
    cache: Arc<Mutex<LruCache<String, Vec<u8>>>>,
    max_bytes: usize,
    current_bytes: Arc<Mutex<usize>>,
}

impl ContentCache {
    pub fn new(max_size_mb: usize) -> Self {
        let capacity = NonZeroUsize::new(1000).unwrap(); // Max entries
        let cache = LruCache::new(capacity);
        
        Self {
            cache: Arc::new(Mutex::new(cache)),
            max_bytes: max_size_mb * 1024 * 1024,
            current_bytes: Arc::new(Mutex::new(0)),
        }
    }
    
    pub fn get(&self, hash: &str) -> Option<Vec<u8>> {
        let mut cache = self.cache.lock().unwrap();
        cache.get(hash).cloned()
    }
    
    pub fn put(&self, hash: String, data: Vec<u8>) {
        let data_size = data.len();
        let mut cache = self.cache.lock().unwrap();
        let mut current = self.current_bytes.lock().unwrap();
        
        // Evict until we have space
        while *current + data_size > self.max_bytes && !cache.is_empty() {
            if let Some((_, evicted_data)) = cache.pop_lru() {
                *current -= evicted_data.len();
            }
        }
        
        // Only cache if it fits
        if data_size <= self.max_bytes {
            cache.put(hash, data);
            *current += data_size;
        }
    }
    
    pub fn clear(&self) {
        let mut cache = self.cache.lock().unwrap();
        let mut current = self.current_bytes.lock().unwrap();
        cache.clear();
        *current = 0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_cache_hit() {
        let cache = ContentCache::new(10); // 10MB
        let data = b"test data".to_vec();
        
        cache.put("hash1".into(), data.clone());
        let retrieved = cache.get("hash1");
        
        assert_eq!(retrieved, Some(data));
    }
    
    #[test]
    fn test_cache_miss() {
        let cache = ContentCache::new(10);
        let retrieved = cache.get("nonexistent");
        assert_eq!(retrieved, None);
    }
    
    #[test]
    fn test_eviction() {
        let cache = ContentCache::new(1); // 1MB
        
        // Fill cache
        let data1 = vec![0u8; 512 * 1024]; // 512KB
        let data2 = vec![1u8; 512 * 1024]; // 512KB
        let data3 = vec![2u8; 512 * 1024]; // 512KB (will evict data1)
        
        cache.put("hash1".into(), data1.clone());
        cache.put("hash2".into(), data2.clone());
        cache.put("hash3".into(), data3.clone());
        
        assert_eq!(cache.get("hash1"), None); // Evicted
        assert!(cache.get("hash2").is_some());
        assert!(cache.get("hash3").is_some());
    }
}
```

---

### T1.11: Add CAS Benchmarks ⏳

**Size**: M (4h)  
**Dependencies**: T1.7, T1.9, T1.10  
**Owner**: TBD

**Description**: Create performance benchmarks for CAS operations.

**Acceptance Criteria**:
- [ ] `benches/cas_bench.rs` created
- [ ] Benchmark: hash 1KB, 1MB, 10MB
- [ ] Benchmark: store 1KB, 1MB
- [ ] Benchmark: retrieve (cold, cached)
- [ ] Uses criterion crate
- [ ] HTML reports generated
- [ ] Baseline established for future comparisons

**Implementation**:
```rust
// benches/cas_bench.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use panini_fs::cas::{hasher::compute_hash, storage::Storage, cache::ContentCache};
use tempfile::TempDir;

fn bench_hash(c: &mut Criterion) {
    let mut group = c.benchmark_group("hash");
    
    for size in [1024, 1024 * 1024, 10 * 1024 * 1024] {
        let data = vec![0u8; size];
        group.bench_with_input(BenchmarkId::from_parameter(size), &data, |b, data| {
            b.iter(|| compute_hash(black_box(data)))
        });
    }
    
    group.finish();
}

fn bench_store(c: &mut Criterion) {
    let temp_dir = TempDir::new().unwrap();
    let storage = Storage::new(temp_dir.path(), 256).unwrap();
    
    let mut group = c.benchmark_group("store");
    
    for size in [1024, 1024 * 1024] {
        let data = vec![0u8; size];
        group.bench_with_input(BenchmarkId::from_parameter(size), &data, |b, data| {
            b.iter(|| storage.store(black_box(data)))
        });
    }
    
    group.finish();
}

fn bench_retrieve(c: &mut Criterion) {
    let temp_dir = TempDir::new().unwrap();
    let storage = Storage::new(temp_dir.path(), 256).unwrap();
    let cache = ContentCache::new(256);
    
    // Prepare data
    let data = vec![0u8; 1024];
    let hash = storage.store(&data).unwrap();
    cache.put(hash.clone(), data.clone());
    
    c.bench_function("retrieve_cached", |b| {
        b.iter(|| cache.get(black_box(&hash)))
    });
    
    c.bench_function("retrieve_cold", |b| {
        b.iter(|| storage.retrieve(black_box(&hash)))
    });
}

criterion_group!(benches, bench_hash, bench_store, bench_retrieve);
criterion_main!(benches);
```

**Run**:
```bash
cargo bench --bench cas_bench
```

---

### T1.12: Write CAS Integration Tests ⏳

**Size**: M (6h)  
**Dependencies**: T1.9, T1.10  
**Owner**: TBD

**Description**: Comprehensive integration tests for CAS layer.

**Acceptance Criteria**:
- [ ] `tests/integration/cas_tests.rs` created
- [ ] Test: store + retrieve roundtrip (1KB, 1MB, 10MB)
- [ ] Test: retrieve nonexistent hash
- [ ] Test: cache hit/miss behavior
- [ ] Test: concurrent stores
- [ ] Test: storage persistence (restart)
- [ ] All tests pass with `cargo test`

**Implementation**:
```rust
// tests/integration/cas_tests.rs
use panini_fs::cas::{storage::Storage, cache::ContentCache};
use tempfile::TempDir;

#[test]
fn test_roundtrip_small() {
    let temp_dir = TempDir::new().unwrap();
    let storage = Storage::new(temp_dir.path(), 64).unwrap();
    
    let data = b"Small content";
    let hash = storage.store(data).unwrap();
    let retrieved = storage.retrieve(&hash).unwrap();
    
    assert_eq!(data, retrieved.as_slice());
}

#[test]
fn test_roundtrip_large() {
    let temp_dir = TempDir::new().unwrap();
    let storage = Storage::new(temp_dir.path(), 64).unwrap();
    
    let data = vec![42u8; 10 * 1024 * 1024]; // 10MB
    let hash = storage.store(&data).unwrap();
    let retrieved = storage.retrieve(&hash).unwrap();
    
    assert_eq!(data, retrieved);
}

#[test]
fn test_cache_integration() {
    let temp_dir = TempDir::new().unwrap();
    let storage = Storage::new(temp_dir.path(), 64).unwrap();
    let cache = ContentCache::new(256);
    
    let data = b"Cached content".to_vec();
    let hash = storage.store(&data).unwrap();
    
    // First retrieve: cache miss
    assert_eq!(cache.get(&hash), None);
    let retrieved = storage.retrieve(&hash).unwrap();
    cache.put(hash.clone(), retrieved.clone());
    
    // Second retrieve: cache hit
    let cached = cache.get(&hash).unwrap();
    assert_eq!(data, cached.as_slice());
}

#[tokio::test]
async fn test_concurrent_stores() {
    let temp_dir = TempDir::new().unwrap();
    let storage = std::sync::Arc::new(Storage::new(temp_dir.path(), 64).unwrap());
    
    let mut handles = vec![];
    
    for i in 0..10 {
        let storage = storage.clone();
        let handle = tokio::spawn(async move {
            let data = format!("Content {}", i).into_bytes();
            storage.store(&data).unwrap()
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
}
```

---

## Week 2: REST API Skeleton (10 tasks)

### T2.1: Implement API State ⏳

**Size**: S (3h)  
**Dependencies**: T1.9, T1.10  
**Owner**: TBD

**Description**: Create shared state for Axum handlers.

**Acceptance Criteria**:
- [ ] `src/api/state.rs` created with `AppState` struct
- [ ] Fields: storage, cache, config
- [ ] Thread-safe (Arc wrappers)
- [ ] Clone-able for handler injection
- [ ] Unit tests for state creation

**Implementation**:
```rust
// src/api/state.rs
use std::sync::Arc;
use crate::cas::{storage::Storage, cache::ContentCache};
use crate::config::Config;

#[derive(Clone)]
pub struct AppState {
    pub storage: Arc<Storage>,
    pub cache: Arc<ContentCache>,
    pub config: Arc<Config>,
}

impl AppState {
    pub fn new(storage: Storage, cache: ContentCache, config: Config) -> Self {
        Self {
            storage: Arc::new(storage),
            cache: Arc::new(cache),
            config: Arc::new(config),
        }
    }
}
```

---

### T2.2: Implement API Models ⏳

**Size**: M (4h)  
**Dependencies**: T1.6  
**Owner**: TBD

**Description**: Define request/response types for API.

**Acceptance Criteria**:
- [ ] `src/api/models.rs` created
- [ ] `StoreResponse`, `ExtractRequest`, `ExtractResponse` structs
- [ ] Serde serialization/deserialization
- [ ] Validation traits
- [ ] Unit tests for JSON serialization

**Implementation**:
```rust
// src/api/models.rs
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize)]
pub struct StoreResponse {
    pub hash: String,
    pub size: usize,
    pub stored_at: DateTime<Utc>,
}

#[derive(Debug, Deserialize)]
pub struct ExtractRequest {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub filename: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct ExtractResponse {
    pub dhatu: String,
    pub metadata: serde_json::Value,
    pub extracted_at: DateTime<Utc>,
}

#[derive(Debug, Serialize)]
pub struct StatsResponse {
    pub total_stored: u64,
    pub storage_size_bytes: u64,
    pub cache_hit_rate: f64,
}

#[derive(Debug, Serialize)]
pub struct HealthResponse {
    pub status: String,
    pub timestamp: DateTime<Utc>,
}
```

---

### T2.3: Implement Store Endpoint ⏳

**Size**: M (6h)  
**Dependencies**: T2.1, T2.2  
**Owner**: TBD

**Description**: POST /api/v1/store endpoint with binary upload.

**Acceptance Criteria**:
- [ ] `src/api/handlers.rs` with `store_handler` function
- [ ] Accept `application/octet-stream`
- [ ] Validate content size <= max_content_size
- [ ] Store in CAS + cache
- [ ] Return 201 Created + JSON response
- [ ] Return 413 Payload Too Large if exceeded
- [ ] Unit tests with test client

**Implementation**:
```rust
// src/api/handlers.rs
use axum::{
    extract::{State, DefaultBodyLimit},
    http::StatusCode,
    response::IntoResponse,
    body::Bytes,
};
use crate::api::{state::AppState, models::StoreResponse};
use crate::error::PaniniError;

pub async fn store_handler(
    State(state): State<AppState>,
    body: Bytes,
) -> Result<impl IntoResponse, PaniniError> {
    // Validate size
    if body.len() > state.config.max_content_size {
        return Err(PaniniError::ContentTooLarge {
            size: body.len(),
            max: state.config.max_content_size,
        });
    }
    
    // Store in CAS
    let hash = state.storage.store(&body)?;
    
    // Update cache
    state.cache.put(hash.clone(), body.to_vec());
    
    // Increment metrics
    metrics::counter!("panini_stores_total").increment(1);
    
    let response = StoreResponse {
        hash,
        size: body.len(),
        stored_at: chrono::Utc::now(),
    };
    
    Ok((StatusCode::CREATED, axum::Json(response)))
}

#[cfg(test)]
mod tests {
    use super::*;
    use axum::body::Body;
    use axum::http::Request;
    use tower::ServiceExt;
    
    #[tokio::test]
    async fn test_store_handler() {
        // Create test state
        // Send request
        // Assert 201 + valid hash
    }
}
```

---

### T2.4: Implement Retrieve Endpoint ⏳

**Size**: M (6h)  
**Dependencies**: T2.1, T2.3  
**Owner**: TBD

**Description**: GET /api/v1/retrieve/{hash} endpoint.

**Acceptance Criteria**:
- [ ] Handler function `retrieve_handler`
- [ ] Extract hash from path parameter
- [ ] Validate hash format
- [ ] Check cache first, then storage
- [ ] Return 200 OK + binary content
- [ ] Return 404 Not Found if missing
- [ ] Return 400 Bad Request if invalid hash
- [ ] Content-Type: application/octet-stream
- [ ] Integration test: store + retrieve

**Implementation**:
```rust
// src/api/handlers.rs (continued)
use axum::extract::Path;

pub async fn retrieve_handler(
    State(state): State<AppState>,
    Path(hash): Path<String>,
) -> Result<impl IntoResponse, PaniniError> {
    // Validate hash format
    crate::cas::validator::validate_hash(&hash)?;
    
    // Try cache first
    if let Some(data) = state.cache.get(&hash) {
        metrics::counter!("panini_cache_hits_total").increment(1);
        return Ok((
            StatusCode::OK,
            [(axum::http::header::CONTENT_TYPE, "application/octet-stream")],
            data,
        ));
    }
    
    // Retrieve from storage
    let data = state.storage.retrieve(&hash)?;
    
    // Update cache
    state.cache.put(hash.clone(), data.clone());
    
    metrics::counter!("panini_cache_misses_total").increment(1);
    
    Ok((
        StatusCode::OK,
        [(axum::http::header::CONTENT_TYPE, "application/octet-stream")],
        data,
    ))
}
```

---

### T2.5: Implement Router ⏳

**Size**: M (4h)  
**Dependencies**: T2.3, T2.4  
**Owner**: TBD

**Description**: Set up Axum router with versioned API.

**Acceptance Criteria**:
- [ ] `src/api/routes.rs` created with `create_router` function
- [ ] Base path: `/api/v1/`
- [ ] Routes: `POST /store`, `GET /retrieve/:hash`
- [ ] Body size limit middleware
- [ ] CORS middleware (development)
- [ ] Compression middleware (gzip)

**Implementation**:
```rust
// src/api/routes.rs
use axum::{
    Router,
    routing::{get, post},
    extract::DefaultBodyLimit,
};
use tower_http::{
    cors::CorsLayer,
    compression::CompressionLayer,
    trace::TraceLayer,
};
use crate::api::{state::AppState, handlers};

pub fn create_router(state: AppState) -> Router {
    let api_v1 = Router::new()
        .route("/store", post(handlers::store_handler))
        .route("/retrieve/:hash", get(handlers::retrieve_handler));
    
    Router::new()
        .nest("/api/v1", api_v1)
        .layer(DefaultBodyLimit::max(state.config.max_content_size))
        .layer(CorsLayer::permissive()) // TODO: Restrict in production
        .layer(CompressionLayer::new())
        .layer(TraceLayer::new_for_http())
        .with_state(state)
}
```

---

### T2.6: Implement Middleware ⏳

**Size**: M (5h)  
**Dependencies**: T2.5  
**Owner**: TBD

**Description**: Add logging, metrics, and timeout middleware.

**Acceptance Criteria**:
- [ ] `src/api/middleware.rs` created
- [ ] Request logging with tracing
- [ ] Metrics collection (counters, histograms)
- [ ] Request timeout (30s default)
- [ ] Request ID generation (UUID)
- [ ] Integration with tracing-subscriber

**Implementation**:
```rust
// src/api/middleware.rs
use axum::{
    middleware::Next,
    response::Response,
    http::Request,
};
use uuid::Uuid;
use std::time::Instant;

pub async fn logging_middleware<B>(
    req: Request<B>,
    next: Next<B>,
) -> Response {
    let request_id = Uuid::new_v4();
    let method = req.method().clone();
    let uri = req.uri().clone();
    
    tracing::info!(
        request_id = %request_id,
        method = %method,
        uri = %uri,
        "Request started"
    );
    
    let start = Instant::now();
    let response = next.run(req).await;
    let duration = start.elapsed();
    
    tracing::info!(
        request_id = %request_id,
        status = response.status().as_u16(),
        duration_ms = duration.as_millis(),
        "Request completed"
    );
    
    metrics::histogram!("panini_request_duration_seconds")
        .record(duration.as_secs_f64());
    
    response
}
```

---

### T2.7: Implement Main Binary ⏳

**Size**: M (5h)  
**Dependencies**: T2.5, T2.6, T1.5  
**Owner**: TBD

**Description**: Create main.rs with server initialization.

**Acceptance Criteria**:
- [ ] `src/main.rs` created
- [ ] Load configuration from environment
- [ ] Initialize storage, cache, state
- [ ] Create router
- [ ] Bind to host:port
- [ ] Graceful shutdown on SIGTERM/SIGINT (30s timeout)
- [ ] Logging initialized (text/json)
- [ ] Metrics server started (optional)

**Implementation**:
```rust
// src/main.rs
use panini_fs::{
    config::Config,
    cas::{storage::Storage, cache::ContentCache},
    api::{state::AppState, routes::create_router},
};
use tokio::signal;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Load config
    let config = Config::from_env()?;
    config.validate()?;
    
    // Initialize logging
    match config.log_format {
        LogFormat::Text => {
            tracing_subscriber::registry()
                .with(tracing_subscriber::fmt::layer())
                .with(tracing_subscriber::EnvFilter::new(&config.log_level))
                .init();
        }
        LogFormat::Json => {
            tracing_subscriber::registry()
                .with(tracing_subscriber::fmt::layer().json())
                .with(tracing_subscriber::EnvFilter::new(&config.log_level))
                .init();
        }
    }
    
    tracing::info!("Starting Panini-FS server");
    tracing::info!("Storage path: {:?}", config.storage_path);
    
    // Initialize storage
    let storage = Storage::new(&config.storage_path, config.rocksdb_cache_mb)?;
    let cache = ContentCache::new(config.cache_size_mb);
    
    // Create state
    let state = AppState::new(storage, cache, config.clone());
    
    // Create router
    let app = create_router(state);
    
    // Bind server
    let addr = format!("{}:{}", config.host, config.port);
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    
    tracing::info!("Listening on {}", addr);
    
    // Serve with graceful shutdown
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal(config.shutdown_timeout))
        .await?;
    
    tracing::info!("Server stopped");
    Ok(())
}

async fn shutdown_signal(timeout: u64) {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("Failed to install Ctrl+C handler");
    };
    
    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("Failed to install SIGTERM handler")
            .recv()
            .await;
    };
    
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();
    
    tokio::select! {
        _ = ctrl_c => { tracing::info!("Received SIGINT"); },
        _ = terminate => { tracing::info!("Received SIGTERM"); },
    }
    
    tracing::info!("Shutdown initiated, waiting {}s for connections to close", timeout);
    tokio::time::sleep(tokio::time::Duration::from_secs(timeout)).await;
}
```

---

### T2.8: Implement Library Exports ⏳

**Size**: S (2h)  
**Dependencies**: T2.7  
**Owner**: TBD

**Description**: Create lib.rs with public API.

**Acceptance Criteria**:
- [ ] `src/lib.rs` created
- [ ] Public modules: config, error, cas, api
- [ ] Documentation comments
- [ ] `cargo doc` generates docs

**Implementation**:
```rust
// src/lib.rs
//! Panini-FS: Content-Addressable Storage with Universal Metadata Extraction
//! 
//! This library provides a high-performance CAS (Content-Addressable Storage) system
//! with support for 7 universal dhātu primitives (TEXT, IMAGE, VIDEO, AUDIO, CODE,
//! BINARY, ARCHIVE).

pub mod config;
pub mod error;
pub mod cas;
pub mod api;
pub mod dhatu;
pub mod extractors;
pub mod health;
pub mod metrics;
pub mod utils;

pub use config::Config;
pub use error::PaniniError;
```

---

### T2.9: Write API Integration Tests ⏳

**Size**: L (8h)  
**Dependencies**: T2.7  
**Owner**: TBD

**Description**: End-to-end tests for API endpoints.

**Acceptance Criteria**:
- [ ] `tests/integration/api_tests.rs` created
- [ ] Test: POST /store + GET /retrieve roundtrip
- [ ] Test: Invalid hash returns 400
- [ ] Test: Nonexistent hash returns 404
- [ ] Test: Content too large returns 413
- [ ] Test: Concurrent requests
- [ ] Test: Graceful shutdown
- [ ] Uses reqwest client

**Implementation**:
```rust
// tests/integration/api_tests.rs
use reqwest::Client;
use tempfile::TempDir;
use tokio::task::JoinHandle;
use panini_fs::{config::Config, api::routes::create_router, /* ... */};

async fn start_test_server() -> (String, JoinHandle<()>) {
    let temp_dir = TempDir::new().unwrap();
    let config = Config {
        storage_path: temp_dir.path().to_path_buf(),
        port: 0, // Random port
        // ... other fields
    };
    
    let storage = Storage::new(&config.storage_path, 64).unwrap();
    let cache = ContentCache::new(64);
    let state = AppState::new(storage, cache, config.clone());
    
    let app = create_router(state);
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();
    
    let handle = tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });
    
    (format!("http://{}", addr), handle)
}

#[tokio::test]
async fn test_store_retrieve_roundtrip() {
    let (base_url, _handle) = start_test_server().await;
    let client = Client::new();
    
    // Store
    let data = b"Test content";
    let response = client
        .post(format!("{}/api/v1/store", base_url))
        .header("Content-Type", "application/octet-stream")
        .body(data.to_vec())
        .send()
        .await
        .unwrap();
    
    assert_eq!(response.status(), 201);
    let store_resp: serde_json::Value = response.json().await.unwrap();
    let hash = store_resp["hash"].as_str().unwrap();
    
    // Retrieve
    let response = client
        .get(format!("{}/api/v1/retrieve/{}", base_url, hash))
        .send()
        .await
        .unwrap();
    
    assert_eq!(response.status(), 200);
    let retrieved = response.bytes().await.unwrap();
    assert_eq!(data, retrieved.as_ref());
}

#[tokio::test]
async fn test_invalid_hash() {
    let (base_url, _handle) = start_test_server().await;
    let client = Client::new();
    
    let response = client
        .get(format!("{}/api/v1/retrieve/INVALID", base_url))
        .send()
        .await
        .unwrap();
    
    assert_eq!(response.status(), 400);
}
```

---

### T2.10: Create OpenAPI Spec (Partial) ⏳

**Size**: M (4h)  
**Dependencies**: T2.3, T2.4  
**Owner**: TBD

**Description**: Document store and retrieve endpoints in OpenAPI 3.0.

**Acceptance Criteria**:
- [ ] `docs/openapi.yaml` created
- [ ] Info section with project details
- [ ] `/api/v1/store` documented
- [ ] `/api/v1/retrieve/{hash}` documented
- [ ] Request/response schemas
- [ ] Error responses (400, 404, 413, 500)
- [ ] Validated with Swagger Editor

**Implementation**:
```yaml
# docs/openapi.yaml
openapi: 3.0.3
info:
  title: Panini-FS API
  description: Content-Addressable Storage with Universal Metadata Extraction
  version: 1.0.0
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:3000/api/v1
    description: Local development

paths:
  /store:
    post:
      summary: Store content
      description: Store binary content and return SHA-256 hash
      requestBody:
        required: true
        content:
          application/octet-stream:
            schema:
              type: string
              format: binary
      responses:
        '201':
          description: Content stored successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StoreResponse'
        '413':
          description: Content too large
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '500':
          description: Internal server error
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
  
  /retrieve/{hash}:
    get:
      summary: Retrieve content
      description: Retrieve content by SHA-256 hash
      parameters:
        - name: hash
          in: path
          required: true
          schema:
            type: string
            pattern: '^[a-f0-9]{64}$'
          description: SHA-256 hash (64 lowercase hex characters)
      responses:
        '200':
          description: Content retrieved successfully
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary
        '400':
          description: Invalid hash format
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '404':
          description: Content not found
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

components:
  schemas:
    StoreResponse:
      type: object
      required:
        - hash
        - size
        - stored_at
      properties:
        hash:
          type: string
          pattern: '^[a-f0-9]{64}$'
          example: "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        size:
          type: integer
          format: int64
          example: 12345
        stored_at:
          type: string
          format: date-time
          example: "2025-10-29T10:30:00Z"
    
    ProblemDetails:
      type: object
      required:
        - type
        - title
        - status
        - detail
      properties:
        type:
          type: string
          format: uri
          example: "https://panini.dev/errors/invalid-hash"
        title:
          type: string
          example: "Invalid hash format"
        status:
          type: integer
          example: 400
        detail:
          type: string
          example: "Hash must be 64 lowercase hex characters"
        instance:
          type: string
          example: "/api/v1/retrieve/INVALID"
```

---

## Week 3: Dhatu Core & Detection (8 tasks)

### T3.1: Implement Dhatu Types ⏳

**Size**: M (5h)  
**Dependencies**: T1.6  
**Owner**: TBD

**Description**: Define complete dhātu type system with metadata structures.

**Acceptance Criteria**:
- [ ] `src/dhatu/types.rs` created
- [ ] `Dhatu` enum with 7 variants
- [ ] Metadata structs: `TextMetadata`, `ImageMetadata`, `VideoMetadata`, etc.
- [ ] Serde serialization
- [ ] Unit tests for all types

**Implementation**:
```rust
// src/dhatu/types.rs
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Dhatu {
    #[serde(rename = "TEXT")]
    Text,
    #[serde(rename = "IMAGE")]
    Image,
    #[serde(rename = "VIDEO")]
    Video,
    #[serde(rename = "AUDIO")]
    Audio,
    #[serde(rename = "CODE")]
    Code,
    #[serde(rename = "BINARY")]
    Binary,
    #[serde(rename = "ARCHIVE")]
    Archive,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct TextMetadata {
    pub encoding: String,
    pub language: Option<String>,
    pub word_count: usize,
    pub line_count: usize,
    pub char_count: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ImageMetadata {
    pub format: String,
    pub width: u32,
    pub height: u32,
    pub color_space: String,
    pub has_alpha: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub exif: Option<ExifData>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ExifData {
    pub make: Option<String>,
    pub model: Option<String>,
    pub datetime: Option<String>,
    pub gps_latitude: Option<f64>,
    pub gps_longitude: Option<f64>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct VideoMetadata {
    pub format: String,
    pub duration_seconds: f64,
    pub width: u32,
    pub height: u32,
    pub frame_rate: f64,
    pub codec: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AudioMetadata {
    pub format: String,
    pub duration_seconds: f64,
    pub sample_rate: u32,
    pub channels: u8,
    pub bitrate: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub id3_tags: Option<Id3Tags>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Id3Tags {
    pub title: Option<String>,
    pub artist: Option<String>,
    pub album: Option<String>,
    pub year: Option<u32>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CodeMetadata {
    pub language: String,
    pub line_count: usize,
    pub function_count: usize,
    pub import_count: usize,
    pub has_syntax_errors: bool,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BinaryMetadata {
    pub format: String, // ELF, PE, Mach-O
    pub architecture: String,
    pub section_count: usize,
    pub symbol_count: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ArchiveMetadata {
    pub format: String, // ZIP, TAR, TAR.GZ
    pub entry_count: usize,
    pub total_size_uncompressed: u64,
    pub compression_ratio: Option<f64>,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "dhatu", content = "metadata")]
pub enum DhatuMetadata {
    #[serde(rename = "TEXT")]
    Text(TextMetadata),
    #[serde(rename = "IMAGE")]
    Image(ImageMetadata),
    #[serde(rename = "VIDEO")]
    Video(VideoMetadata),
    #[serde(rename = "AUDIO")]
    Audio(AudioMetadata),
    #[serde(rename = "CODE")]
    Code(CodeMetadata),
    #[serde(rename = "BINARY")]
    Binary(BinaryMetadata),
    #[serde(rename = "ARCHIVE")]
    Archive(ArchiveMetadata),
}
```

---

### T3.2: Implement Format Detector ⏳

**Size**: M (6h)  
**Dependencies**: T3.1  
**Owner**: TBD

**Description**: Magic byte detection and format identification.

**Acceptance Criteria**:
- [ ] `src/dhatu/detector.rs` created
- [ ] Function `detect_dhatu(content: &[u8], filename: Option<&str>) -> Result<Dhatu>`
- [ ] Priority: magic bytes → extension → analysis
- [ ] Uses `infer` crate for magic bytes
- [ ] Unit tests for all 7 dhātu types
- [ ] Test with fixtures from `tests/fixtures/`

**Implementation**: See full code in next message due to length...

---

*[Tasks continue through T7.12 with similar detail level]*

---

## Summary Statistics

**Total Tasks**: 72
**Total Estimated Effort**: ~320 hours (8 weeks × 40 hours)

**By Size**:
- S (2-4h): 18 tasks = 54 hours
- M (4-8h): 38 tasks = 228 hours
- L (8-16h): 14 tasks = 168 hours
- XL (16-24h): 2 tasks = 40 hours

**By Week**:
- Week 1: 12 tasks (Foundation)
- Week 2: 10 tasks (API)
- Week 3: 8 tasks (Dhatu)
- Week 4-5: 14 tasks (Extractors 1-4)
- Week 6: 10 tasks (Extractors 5-7)
- Week 7: 12 tasks (Client, Metrics)
- Week 8: 6 tasks (Polish, Release)

**Critical Path**: T1.2 → T1.9 → T2.1 → T2.3 → T3.1 → T4.1 → T7.1

---

**Next Actions**:
1. Review and approve this task list
2. Assign owners to Week 1 tasks
3. Start with T1.1 (project structure)
4. Use GitHub Projects or similar for tracking

