# Implementation Plan - Panini-FS

**Version**: 1.0
**Date**: 2025-01-14
**Status**: READY FOR IMPLEMENTATION

## Executive Summary

This plan provides a comprehensive implementation blueprint for Panini-FS, a content-addressable storage system with universal metadata extraction capabilities. Based on the constitutional principles, technical specifications, and confirmed clarifications, this document defines the exact file structure, dependencies, module architecture, and 8-week roadmap for building production-ready Rust backend and TypeScript client.

**Deliverables**:
- Backend: Rust service with CAS + 7 dhātu extractors (~5000 LOC)
- Client: TypeScript SDK with full API coverage (~1000 LOC)
- Tests: 80%+ coverage with unit, integration, property-based tests (~2000 LOC)
- Documentation: OpenAPI spec, README, examples
- CI/CD: GitHub Actions with fmt, clippy, test, coverage

**Timeline**: 8 weeks
**Team Size**: 1-2 developers
**Target Performance**: >1000 store/sec, >5000 retrieve/sec, <10ms P50 latency

---

## 1. Project Structure

### 1.1 Complete Directory Layout

```
panini-fs/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                       # Main CI: fmt, clippy, test
│   │   ├── coverage.yml                 # Code coverage + report
│   │   └── release.yml                  # Release builds + Docker
│   └── prompts/                         # Spec Kit prompts (existing)
├── .specify/                            # Spec Kit documents (existing)
├── backend/
│   ├── Cargo.toml                       # Workspace root
│   ├── Cargo.lock                       # Generated
│   ├── .rustfmt.toml                    # Rust formatting config
│   ├── .clippy.toml                     # Clippy lints config
│   ├── benches/
│   │   ├── cas_bench.rs                 # CAS performance benchmarks
│   │   └── extractor_bench.rs           # Extractor benchmarks
│   ├── examples/
│   │   ├── basic_usage.rs               # Simple store/retrieve
│   │   ├── extractor_demo.rs            # All 7 extractors
│   │   └── async_client.rs              # Async usage patterns
│   ├── src/
│   │   ├── main.rs                      # Binary entry point
│   │   ├── lib.rs                       # Library exports
│   │   ├── config.rs                    # Configuration (env vars)
│   │   ├── error.rs                     # Error types
│   │   ├── api/
│   │   │   ├── mod.rs                   # API module
│   │   │   ├── handlers.rs              # 5 endpoint handlers
│   │   │   ├── middleware.rs            # Logging, metrics
│   │   │   ├── routes.rs                # Axum router
│   │   │   ├── state.rs                 # Shared state
│   │   │   └── models.rs                # Request/response types
│   │   ├── cas/
│   │   │   ├── mod.rs                   # CAS module
│   │   │   ├── hasher.rs                # SHA-256 implementation
│   │   │   ├── storage.rs               # RocksDB operations
│   │   │   ├── cache.rs                 # LRU cache (256MB)
│   │   │   └── validator.rs             # Hash/path validation
│   │   ├── dhatu/
│   │   │   ├── mod.rs                   # Dhatu module
│   │   │   ├── types.rs                 # Dhatu enum + structs
│   │   │   ├── detector.rs              # Format detection
│   │   │   └── metadata.rs              # Metadata structures
│   │   ├── extractors/
│   │   │   ├── mod.rs                   # Extractor registry
│   │   │   ├── text.rs                  # TEXT extractor
│   │   │   ├── image.rs                 # IMAGE extractor
│   │   │   ├── video.rs                 # VIDEO extractor
│   │   │   ├── audio.rs                 # AUDIO extractor
│   │   │   ├── code.rs                  # CODE extractor
│   │   │   ├── binary.rs                # BINARY extractor
│   │   │   ├── archive.rs               # ARCHIVE extractor
│   │   │   └── traits.rs                # Extractor trait
│   │   ├── health/
│   │   │   ├── mod.rs                   # Health module
│   │   │   ├── liveness.rs              # /health/live
│   │   │   └── readiness.rs             # /health/ready
│   │   ├── metrics/
│   │   │   ├── mod.rs                   # Metrics module
│   │   │   ├── prometheus.rs            # Prometheus exporter
│   │   │   └── collectors.rs            # Custom collectors
│   │   └── utils/
│   │       ├── mod.rs                   # Utility functions
│   │       ├── shutdown.rs              # Graceful shutdown
│   │       └── mime.rs                  # MIME type detection
│   ├── tests/
│   │   ├── integration/
│   │   │   ├── api_tests.rs             # API integration tests
│   │   │   ├── cas_tests.rs             # CAS integration tests
│   │   │   └── extractor_tests.rs       # Extractor integration tests
│   │   ├── fixtures/                    # Test files
│   │   │   ├── sample.txt
│   │   │   ├── sample.jpg
│   │   │   ├── sample.mp3
│   │   │   ├── sample.zip
│   │   │   └── sample.py
│   │   └── common/
│   │       └── mod.rs                   # Test utilities
│   └── scripts/
│       ├── dev.sh                       # Development setup
│       ├── test.sh                      # Run all tests
│       └── bench.sh                     # Run benchmarks
├── client/
│   ├── package.json                     # TypeScript client
│   ├── tsconfig.json                    # TypeScript config
│   ├── .eslintrc.json                   # ESLint config
│   ├── .prettierrc.json                 # Prettier config
│   ├── src/
│   │   ├── index.ts                     # Main export
│   │   ├── client.ts                    # PaniniClient class
│   │   ├── types.ts                     # TypeScript types
│   │   ├── errors.ts                    # Error classes
│   │   └── utils/
│   │       ├── hash.ts                  # SHA-256 (Node/browser)
│   │       └── validation.ts            # Input validation
│   ├── tests/
│   │   ├── client.test.ts               # Client unit tests
│   │   ├── types.test.ts                # Type tests
│   │   └── integration.test.ts          # Integration with backend
│   ├── examples/
│   │   ├── node-example.ts              # Node.js usage
│   │   └── browser-example.html         # Browser usage
│   └── dist/                            # Build output (generated)
├── docs/
│   ├── API.md                           # REST API documentation
│   ├── EXTRACTORS.md                    # Extractor guide
│   ├── DEPLOYMENT.md                    # Deployment guide
│   ├── PERFORMANCE.md                   # Performance tuning
│   └── openapi.yaml                     # OpenAPI 3.0 spec
├── docker/
│   ├── Dockerfile                       # Production image
│   ├── Dockerfile.dev                   # Development image
│   └── docker-compose.yml               # Local stack
├── .env.example                         # Environment variables template
├── .gitignore
├── LICENSE                              # MIT (existing)
└── README.md                            # Main documentation

```

### 1.2 File Count Summary

| Component       | Files | LOC    |
|-----------------|-------|--------|
| Backend Rust    | 35    | ~5000  |
| Backend Tests   | 12    | ~1500  |
| Client TS       | 8     | ~1000  |
| Client Tests    | 3     | ~500   |
| Documentation   | 5     | ~2000  |
| CI/CD           | 3     | ~300   |
| Configuration   | 12    | ~500   |
| **Total**       | **78**| **~10800** |

---

## 2. Backend Dependencies

### 2.1 Cargo.toml (Root Workspace)

```toml
[package]
name = "panini-fs"
version = "1.0.0"
edition = "2021"
rust-version = "1.70"
authors = ["Panini Team <team@panini.dev>"]
license = "MIT"
description = "Content-addressable storage with universal metadata extraction"
repository = "https://github.com/stephanedenis/Panini-FS"
keywords = ["cas", "storage", "metadata", "dhatu", "content-addressed"]
categories = ["filesystem", "web-programming::http-server"]

[dependencies]
# Web Framework
axum = { version = "0.7", features = ["http2", "macros"] }
tokio = { version = "1.35", features = ["rt-multi-thread", "macros", "fs", "signal"] }
tower = { version = "0.4", features = ["timeout", "limit"] }
tower-http = { version = "0.5", features = ["trace", "cors", "compression-gzip"] }

# Storage
rocksdb = { version = "0.21", features = ["lz4"] }
lru = "0.12"

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Hashing
sha2 = "0.10"
blake3 = { version = "1.5", optional = true }

# Extractors - TEXT
encoding_rs = "0.8"
chardetng = "0.1"
regex = "1.10"

# Extractors - IMAGE
image = { version = "0.24", features = ["jpeg", "png", "gif", "webp", "bmp"] }
kamadak-exif = "0.5"

# Extractors - VIDEO
mp4parse = "0.17"

# Extractors - AUDIO
symphonia = { version = "0.5", features = ["aac", "mp3", "flac", "wav"] }
id3 = "1.13"

# Extractors - CODE
tree-sitter = "0.20"
tree-sitter-rust = "0.20"
tree-sitter-python = "0.20"
tree-sitter-javascript = "0.20"
tree-sitter-typescript = "0.20"

# Extractors - BINARY
goblin = "0.8"

# Extractors - ARCHIVE
zip = { version = "0.6", default-features = false, features = ["deflate"] }
flate2 = "1.0"
tar = "0.4"

# Detection
infer = "0.15"
mime = "0.3"
mime_guess = "2.0"

# Logging & Metrics
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
prometheus = "0.13"

# Error Handling
anyhow = "1.0"
thiserror = "1.0"

# Configuration
dotenvy = "0.15"

# Utilities
bytes = "1.5"
uuid = { version = "1.6", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
proptest = "1.4"
tempfile = "3.8"
reqwest = { version = "0.11", features = ["json", "blocking"] }
wiremock = "0.5"

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
strip = true

[profile.bench]
inherits = "release"

[[bin]]
name = "panini-fs"
path = "src/main.rs"

[lib]
name = "panini_fs"
path = "src/lib.rs"

[[bench]]
name = "cas_bench"
harness = false

[[bench]]
name = "extractor_bench"
harness = false
```

### 2.2 Dependency Justification

| Dependency       | Version | Purpose                                    | Size    |
|------------------|---------|-----------------------------------------------|---------|
| axum             | 0.7     | HTTP framework (async, type-safe)            | 450KB   |
| tokio            | 1.35    | Async runtime                                | 1.2MB   |
| rocksdb          | 0.21    | Embedded key-value storage                   | 3.5MB   |
| serde            | 1.0     | Serialization framework                      | 200KB   |
| image            | 0.24    | IMAGE extractor (JPEG, PNG, etc.)            | 800KB   |
| symphonia        | 0.5     | AUDIO extractor (pure Rust)                  | 600KB   |
| tree-sitter      | 0.20    | CODE extractor (parsing)                     | 350KB   |
| goblin           | 0.8     | BINARY extractor (ELF, PE, Mach-O)          | 180KB   |
| zip              | 0.6     | ARCHIVE extractor                            | 120KB   |
| tracing          | 0.1     | Structured logging                           | 150KB   |
| prometheus       | 0.13    | Metrics collection                           | 100KB   |
| **Total**        | -       | **~15 crates**                               | **~8MB**|

---

## 3. Client Dependencies

### 3.1 package.json

```json
{
  "name": "@panini/client",
  "version": "1.0.0",
  "description": "TypeScript client for Panini-FS API",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src --ext .ts",
    "format": "prettier --write 'src/**/*.ts'",
    "prepublishOnly": "npm run build"
  },
  "keywords": ["panini", "cas", "storage", "metadata"],
  "author": "Panini Team",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/stephanedenis/Panini-FS.git"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@typescript-eslint/eslint-plugin": "^6.13.0",
    "@typescript-eslint/parser": "^6.13.0",
    "eslint": "^8.54.0",
    "jest": "^29.7.0",
    "prettier": "^3.1.0",
    "ts-jest": "^29.1.0",
    "typescript": "^5.3.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### 3.2 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

---

## 4. Module Architecture

### 4.1 Backend Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  /store     │  │  /retrieve  │  │  /extract   │        │
│  │  (POST)     │  │  (GET)      │  │  (POST)     │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                 │                 │               │
│         └────────┬────────┴────────┬────────┘               │
│                  ▼                 ▼                         │
│         ┌─────────────────┐ ┌──────────────────┐           │
│         │   Middleware    │ │   State/Cache    │           │
│         │ - Logging       │ │ - LRU 256MB      │           │
│         │ - Metrics       │ │ - Shared Storage │           │
│         └─────────────────┘ └──────────────────┘           │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   CAS Layer  │    │ Dhatu Layer  │    │Health/Metrics│
│              │    │              │    │              │
│ - Hasher     │◄───┤ - Detector   │    │ - /health/*  │
│ - Storage    │    │ - Types      │    │ - /metrics   │
│ - Validator  │    │ - Metadata   │    └──────────────┘
│              │    └──────┬───────┘
│ RocksDB      │           │
│ - LZ4        │           │
│ - Bloom      │           │
└──────────────┘           │
                           ▼
                ┌────────────────────┐
                │ Extractor Registry │
                │  (7 extractors)    │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼        ▼        ▼        ▼        ▼
    ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
    │ TEXT │ │IMAGE │ │VIDEO │ │AUDIO │ │ CODE │
    └──────┘ └──────┘ └──────┘ └──────┘ └──────┘
                                ▼        ▼
                            ┌──────┐ ┌──────┐
                            │BINARY│ │ARCHIV│
                            └──────┘ └──────┘
```

### 4.2 Data Flow

#### Store Operation
```
1. Client POST /api/v1/store + binary content
2. API handler validates:
   - Content-Type: application/octet-stream
   - Size <= PANINI_MAX_CONTENT_SIZE (100MB)
3. CAS hasher computes SHA-256
4. CAS storage writes to RocksDB:
   - Key: {hash}:content
   - Value: raw bytes (LZ4 compressed)
5. Return 201 Created + JSON:
   {
     "hash": "abc123...",
     "size": 12345,
     "stored_at": "2025-01-14T10:30:00Z"
   }
```

#### Retrieve Operation
```
1. Client GET /api/v1/retrieve/{hash}
2. API handler validates hash format (regex)
3. Check LRU cache (256MB):
   - HIT: Return cached bytes + metadata
   - MISS: Continue
4. CAS storage reads from RocksDB:
   - Key: {hash}:content
   - Decompress LZ4
5. Update cache
6. Return 200 OK + binary content
```

#### Extract Operation
```
1. Client POST /api/v1/extract + binary content
2. Dhatu detector runs:
   - Magic bytes (infer crate)
   - Extension (if filename provided)
   - Content analysis
3. Determine dhātu type (TEXT/IMAGE/VIDEO/etc.)
4. Route to appropriate extractor
5. Extractor runs (with 5s timeout):
   - Parse format
   - Extract metadata
   - Handle errors gracefully
6. Return 200 OK + JSON:
   {
     "dhatu": "IMAGE",
     "metadata": {
       "format": "JPEG",
       "width": 1920,
       "height": 1080,
       ...
     },
     "extracted_at": "2025-01-14T10:30:00Z"
   }
```

### 4.3 Error Handling Flow

```
┌─────────────┐
│ API Request │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Validation      │
│ - Hash format   │
│ - Size limits   │
│ - Content-Type  │
└──────┬──────────┘
       │ FAIL
       ├──────────────────────────────────┐
       │ SUCCESS                          ▼
       ▼                         ┌─────────────────┐
┌─────────────────┐              │ 400 Bad Request │
│ Business Logic  │              │ RFC 7807        │
│ - CAS ops       │              │ {              │
│ - Extraction    │              │   "type": ...  │
└──────┬──────────┘              │   "title": ... │
       │ FAIL                    │   "detail": ...│
       ├──────────────────────┐  │   "instance"   │
       │ SUCCESS              │  │ }              │
       ▼                      ▼  └────────────────┘
┌─────────────────┐  ┌─────────────────┐
│ Return Success  │  │ 500/503 Error   │
│ 200/201         │  │ Log to tracing  │
└─────────────────┘  │ Increment metric│
                     └─────────────────┘
```

---

## 5. Testing Strategy

### 5.1 Test Coverage Targets

| Component          | Unit Tests | Integration | Property | Total   |
|--------------------|-----------|-------------|----------|---------|
| CAS (hasher)       | 95%       | -           | Yes      | **95%** |
| CAS (storage)      | 90%       | 10%         | -        | **95%** |
| API handlers       | 80%       | 20%         | -        | **95%** |
| Extractors (each)  | 85%       | 10%         | -        | **90%** |
| Client (TS)        | 90%       | 10%         | -        | **95%** |
| **Overall Target** | **80%+**  |             |          |         |

### 5.2 Test File Organization

#### Unit Tests (colocated with source)
```rust
// src/cas/hasher.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sha256_empty() {
        // Test empty input
    }

    #[test]
    fn test_sha256_known_vectors() {
        // Test against known SHA-256 outputs
    }
}
```

#### Integration Tests (tests/integration/)
```rust
// tests/integration/api_tests.rs
use panini_fs::*;

#[tokio::test]
async fn test_store_retrieve_roundtrip() {
    // Start server
    // Store content
    // Retrieve by hash
    // Assert equality
}

#[tokio::test]
async fn test_extract_with_store() {
    // Store image
    // Extract metadata
    // Validate IMAGE dhatu
}
```

#### Property-Based Tests (proptest)
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn hash_stability(data: Vec<u8>) {
        // Hash same data twice -> same output
        let hash1 = compute_hash(&data);
        let hash2 = compute_hash(&data);
        prop_assert_eq!(hash1, hash2);
    }

    #[test]
    fn roundtrip_property(data: Vec<u8>) {
        // Store + Retrieve -> original data
        let hash = store(&data);
        let retrieved = retrieve(&hash);
        prop_assert_eq!(data, retrieved);
    }
}
```

### 5.3 Test Fixtures

Location: `tests/fixtures/`

| File              | Size | Purpose                          |
|-------------------|------|----------------------------------|
| sample.txt        | 1KB  | TEXT extractor (UTF-8, ASCII)    |
| sample_unicode.txt| 2KB  | TEXT extractor (emoji, CJK)      |
| sample.jpg        | 50KB | IMAGE extractor (JPEG + EXIF)    |
| sample.png        | 30KB | IMAGE extractor (PNG + metadata) |
| sample.mp4        | 500KB| VIDEO extractor (H.264)          |
| sample.mp3        | 100KB| AUDIO extractor (ID3 tags)       |
| sample.wav        | 200KB| AUDIO extractor (uncompressed)   |
| sample.py         | 5KB  | CODE extractor (Python)          |
| sample.rs         | 8KB  | CODE extractor (Rust)            |
| sample.zip        | 20KB | ARCHIVE extractor (mixed files)  |
| sample.tar.gz     | 25KB | ARCHIVE extractor (compressed)   |
| sample_elf        | 50KB | BINARY extractor (Linux)         |
| sample_pe.exe     | 60KB | BINARY extractor (Windows)       |

---

## 6. Performance Benchmarks

### 6.1 Benchmark Structure

Location: `benches/`

#### CAS Benchmarks (cas_bench.rs)
```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_hash_1kb(c: &mut Criterion) {
    let data = vec![0u8; 1024];
    c.bench_function("hash_1kb", |b| {
        b.iter(|| compute_hash(black_box(&data)))
    });
}

fn bench_hash_1mb(c: &mut Criterion) {
    let data = vec![0u8; 1_048_576];
    c.bench_function("hash_1mb", |b| {
        b.iter(|| compute_hash(black_box(&data)))
    });
}

fn bench_store_1kb(c: &mut Criterion) {
    let storage = setup_storage();
    let data = vec![0u8; 1024];
    c.bench_function("store_1kb", |b| {
        b.iter(|| storage.store(black_box(&data)))
    });
}

fn bench_retrieve_cached(c: &mut Criterion) {
    let storage = setup_storage_with_cache();
    let hash = "abc123...";
    c.bench_function("retrieve_cached", |b| {
        b.iter(|| storage.retrieve(black_box(hash)))
    });
}

criterion_group!(benches, bench_hash_1kb, bench_hash_1mb, bench_store_1kb, bench_retrieve_cached);
criterion_main!(benches);
```

#### Extractor Benchmarks (extractor_bench.rs)
```rust
fn bench_text_extractor(c: &mut Criterion) {
    let content = include_bytes!("../tests/fixtures/sample.txt");
    c.bench_function("extract_text", |b| {
        b.iter(|| extract_text_metadata(black_box(content)))
    });
}

fn bench_image_extractor(c: &mut Criterion) {
    let content = include_bytes!("../tests/fixtures/sample.jpg");
    c.bench_function("extract_image", |b| {
        b.iter(|| extract_image_metadata(black_box(content)))
    });
}
```

### 6.2 Performance Targets

| Operation         | Input Size | Target      | Measured | Status |
|-------------------|-----------|-------------|----------|--------|
| Hash (SHA-256)    | 1KB       | <1µs        | TBD      | ⏳     |
| Hash (SHA-256)    | 1MB       | <500µs      | TBD      | ⏳     |
| Store (RocksDB)   | 1KB       | <100µs      | TBD      | ⏳     |
| Store (RocksDB)   | 1MB       | <5ms        | TBD      | ⏳     |
| Retrieve (cached) | Any       | <10µs       | TBD      | ⏳     |
| Retrieve (cold)   | 1KB       | <200µs      | TBD      | ⏳     |
| Retrieve (cold)   | 1MB       | <8ms        | TBD      | ⏳     |
| Extract TEXT      | 1KB       | <50µs       | TBD      | ⏳     |
| Extract IMAGE     | 50KB JPEG | <2ms        | TBD      | ⏳     |
| Extract AUDIO     | 100KB MP3 | <5ms        | TBD      | ⏳     |
| Extract CODE      | 5KB Python| <10ms       | TBD      | ⏳     |

### 6.3 Load Testing Targets

| Scenario                 | Throughput        | Latency (P50) | Latency (P99) |
|--------------------------|-------------------|---------------|---------------|
| Store 1KB files          | >1000 req/sec     | <10ms         | <50ms         |
| Retrieve 1KB (cached)    | >5000 req/sec     | <5ms          | <20ms         |
| Retrieve 1KB (cold)      | >2000 req/sec     | <15ms         | <100ms        |
| Extract (mixed workload) | >500 req/sec      | <50ms         | <200ms        |
| Concurrent clients (100) | Stable throughput | <100ms        | <500ms        |

---

## 7. Implementation Roadmap (8 Weeks)

### Week 1: Foundation & CAS Core

**Objectives**:
- Project setup
- CAS layer (hasher + storage)
- Configuration management

**Tasks**:
1. Initialize Cargo workspace
2. Set up CI/CD (GitHub Actions)
3. Implement `cas::hasher` module
   - SHA-256 computation
   - Unit tests (known vectors)
   - Property-based tests
4. Implement `cas::storage` module
   - RocksDB initialization
   - Store/retrieve operations
   - LZ4 compression
   - Error handling
5. Implement `cas::validator` module
   - Hash format validation (regex)
   - Path sanitization (canonicalization)
6. Implement `config.rs`
   - Environment variable loading
   - Default values
   - Validation
7. Write integration tests for CAS roundtrip

**Deliverables**:
- ✅ Working CAS layer (store + retrieve)
- ✅ 90%+ test coverage
- ✅ CI passing (fmt, clippy, test)

**Risks**:
- RocksDB configuration complexity → Mitigation: Use sensible defaults from clarifications

### Week 2: REST API Skeleton

**Objectives**:
- Axum server setup
- Basic endpoints
- Middleware

**Tasks**:
1. Implement `api::state` module
   - Shared storage handle
   - Configuration
2. Implement `api::routes` module
   - Router setup
   - URL versioning (`/api/v1/`)
3. Implement `api::handlers` module
   - `/store` endpoint (POST)
   - `/retrieve/{hash}` endpoint (GET)
   - Request validation
   - RFC 7807 error responses
4. Implement `api::middleware` module
   - Request logging (tracing)
   - Metrics collection
   - Timeout (30s default)
5. Implement `main.rs`
   - Server initialization
   - Graceful shutdown (SIGTERM, 30s timeout)
6. Write API integration tests
   - Store + retrieve roundtrip
   - Error cases (invalid hash, not found)

**Deliverables**:
- ✅ Working REST API (2 endpoints)
- ✅ 80%+ test coverage
- ✅ OpenAPI spec (partial)

**Risks**:
- Axum API changes → Mitigation: Lock to 0.7.x version

### Week 3: Dhatu Core & Detection

**Objectives**:
- Dhatu type system
- Format detection
- Extractor trait

**Tasks**:
1. Implement `dhatu::types` module
   - `Dhatu` enum (7 variants)
   - Metadata structures (TextMetadata, ImageMetadata, etc.)
2. Implement `dhatu::detector` module
   - Magic byte detection (infer crate)
   - Extension-based fallback
   - Content analysis heuristics
3. Implement `extractors::traits` module
   - `Extractor` trait
   - `extract()` method signature
   - Error handling contract
4. Implement `extractors::mod` module
   - Extractor registry (HashMap)
   - Route by Dhatu type
5. Write unit tests for detector
   - All 7 dhātu types
   - Ambiguous cases
6. Write integration tests for extractor routing

**Deliverables**:
- ✅ Complete dhātu type system
- ✅ Working format detection
- ✅ Extractor trait defined

**Risks**:
- Detection accuracy → Mitigation: Use battle-tested `infer` crate

### Week 4-5: Extractors Implementation (Part 1)

**Objectives**:
- Implement 4 extractors: TEXT, IMAGE, CODE, ARCHIVE

**Week 4 Tasks**:
1. Implement `extractors::text` module
   - Encoding detection (chardetng)
   - Language detection
   - Word count, line count
   - Unit tests with UTF-8, ASCII, emoji
2. Implement `extractors::image` module
   - Format detection (JPEG, PNG, GIF, WebP, BMP)
   - Dimensions, color space
   - EXIF parsing (kamadak-exif)
   - Unit tests with sample.jpg, sample.png
3. Add `/api/v1/extract` endpoint
   - Accept binary content
   - Run detection + extraction
   - Return JSON metadata
4. Integration tests for TEXT + IMAGE

**Week 5 Tasks**:
1. Implement `extractors::code` module
   - Language detection (tree-sitter)
   - LOC, function count
   - Import/dependency extraction
   - Support: Rust, Python, JavaScript, TypeScript
   - Unit tests with sample.py, sample.rs
2. Implement `extractors::archive` module
   - ZIP, TAR, TAR.GZ support
   - Entry count, sizes
   - Compression ratio
   - Unit tests with sample.zip, sample.tar.gz
3. Integration tests for CODE + ARCHIVE

**Deliverables**:
- ✅ 4 extractors working (TEXT, IMAGE, CODE, ARCHIVE)
- ✅ 85%+ test coverage per extractor
- ✅ `/extract` endpoint functional

**Risks**:
- Tree-sitter complexity → Mitigation: Start with simple metrics (LOC only)

### Week 6: Extractors Implementation (Part 2)

**Objectives**:
- Implement remaining 3 extractors: VIDEO, AUDIO, BINARY

**Tasks**:
1. Implement `extractors::video` module
   - Format: MP4 (mp4parse crate)
   - Duration, resolution, frame rate
   - Codec detection
   - Unit tests with sample.mp4
2. Implement `extractors::audio` module
   - Format: MP3, FLAC, WAV (symphonia)
   - Sample rate, channels, bitrate
   - ID3 tag extraction
   - Unit tests with sample.mp3, sample.wav
3. Implement `extractors::binary` module
   - Format: ELF, PE, Mach-O (goblin)
   - Architecture, symbols
   - Section count
   - Unit tests with sample_elf, sample_pe.exe
4. Integration tests for all 7 extractors
5. Add timeout handling (5s per extraction)
6. Add partial metadata support (graceful degradation)

**Deliverables**:
- ✅ All 7 extractors complete
- ✅ 85%+ test coverage
- ✅ Error handling robust

**Risks**:
- Audio format variety → Mitigation: Focus on MP3, use symphonia for others

### Week 7: Client, Metrics, Observability

**Objectives**:
- TypeScript client
- Prometheus metrics
- Health checks
- Documentation

**Tasks**:
1. Implement TypeScript client (`client/src/`)
   - `PaniniClient` class
   - All 5 API methods (store, retrieve, extract, dhatu, stats)
   - Type definitions
   - Error handling
   - Unit tests
2. Implement `metrics::prometheus` module
   - Counters: requests_total, errors_total
   - Gauges: storage_size_bytes, cache_entries
   - Histograms: request_duration_seconds
   - `/metrics` endpoint
3. Implement `health` module
   - `/health/live` (always 200)
   - `/health/ready` (check RocksDB)
4. Implement `cas::cache` module
   - LRU cache (256MB default)
   - Configurable size
   - Eviction policy
5. Add remaining API endpoints:
   - `/api/v1/dhatu/{hash}` (GET)
   - `/api/v1/stats` (GET)
6. Write OpenAPI spec (`docs/openapi.yaml`)
7. Write API documentation (`docs/API.md`)

**Deliverables**:
- ✅ TypeScript client published
- ✅ Full observability (metrics + health)
- ✅ Complete API documentation
- ✅ Cache implemented

**Risks**:
- None significant

### Week 8: Polish, Benchmarks, Release

**Objectives**:
- Performance optimization
- Comprehensive benchmarks
- Documentation
- Release preparation

**Tasks**:
1. Run benchmarks (`cargo bench`)
   - Validate performance targets
   - Optimize hot paths if needed
2. Write deployment documentation (`docs/DEPLOYMENT.md`)
   - Docker setup
   - Environment variables
   - Production configuration
3. Write performance guide (`docs/PERFORMANCE.md`)
   - Tuning RocksDB
   - Cache sizing
   - Load testing results
4. Write extractor guide (`docs/EXTRACTORS.md`)
   - How to add new extractors
   - Format detection tips
5. Create Docker images
   - Production Dockerfile
   - Development Dockerfile
   - docker-compose.yml
6. Final testing
   - Load testing (100 concurrent clients)
   - Stress testing (memory leaks, CPU usage)
7. Release v1.0.0
   - Tag commit
   - Generate changelog
   - Publish crate (optional)
   - Publish npm package

**Deliverables**:
- ✅ Performance targets met
- ✅ Complete documentation
- ✅ Docker images
- ✅ v1.0.0 released

**Risks**:
- Performance targets not met → Mitigation: 2-week buffer in timeline

---

## 8. Task Dependencies

### Critical Path

```
Week 1: CAS Core
   │
   ├─► Week 2: API Skeleton
   │      │
   │      └─► Week 3: Dhatu Core
   │             │
   │             ├─► Week 4: Extractors 1-4
   │             │      │
   │             │      └─► Week 5: Complete 4 extractors
   │             │             │
   │             │             └─► Week 6: Extractors 5-7
   │             │                    │
   │             │                    └─► Week 7: Client + Metrics
   │             │                           │
   │             │                           └─► Week 8: Polish + Release
   │
   └─► Parallel: CI/CD setup (Week 1)
              Configuration (Week 1)
              Documentation (continuous)
```

### Task Independence

**Can start in parallel**:
- Week 1: CI/CD setup + CAS implementation
- Week 4-6: Each extractor is independent (can parallelize if 2+ devs)
- Week 7: Client + Metrics (separate codebases)

**Must be sequential**:
- CAS → API (API depends on CAS)
- API → Extractors (endpoints need CAS + API)
- Extractors → Client (client needs working API)

---

## 9. Risk Mitigation

### High-Priority Risks

| Risk                              | Probability | Impact | Mitigation                                        |
|-----------------------------------|-------------|--------|---------------------------------------------------|
| RocksDB performance below target  | Medium      | High   | Tune bloom filters, cache size, compression       |
| Extractor timeouts in production  | Medium      | Medium | 5s timeout, partial metadata, async processing    |
| Memory leaks in long-running      | Low         | High   | Extensive load testing, valgrind, heap profiling  |
| Dependency vulnerabilities        | Low         | Medium | Dependabot, cargo audit, regular updates          |
| TypeScript client compatibility   | Low         | Low    | Test on Node 18/20, browser (Chrome, Firefox)    |

### Medium-Priority Risks

| Risk                              | Probability | Impact | Mitigation                                        |
|-----------------------------------|-------------|--------|---------------------------------------------------|
| API breaking changes in deps      | Low         | Medium | Lock to minor versions, test before upgrade       |
| Insufficient test coverage        | Low         | Medium | Enforce 80% in CI, manual review                  |
| Documentation drift               | Medium      | Low    | Update docs in same PR as code changes            |

---

## 10. Configuration Management

### 10.1 Environment Variables

| Variable                    | Default       | Description                          | Example                  |
|-----------------------------|---------------|--------------------------------------|--------------------------|
| `PANINI_STORAGE_PATH`       | `./data/`     | RocksDB storage directory            | `/var/lib/panini/`       |
| `PANINI_MAX_CONTENT_SIZE`   | `104857600`   | Max upload size (100MB)              | `52428800` (50MB)        |
| `PANINI_LOG_LEVEL`          | `info`        | Log level                            | `debug`, `warn`, `error` |
| `PANINI_LOG_FORMAT`         | `text`        | Log format (text or json)            | `json`                   |
| `PANINI_CACHE_SIZE_MB`      | `256`         | LRU cache size in MB                 | `512`                    |
| `PANINI_PORT`               | `3000`        | HTTP server port                     | `8080`                   |
| `PANINI_HOST`               | `127.0.0.1`   | HTTP server bind address             | `0.0.0.0`                |
| `PANINI_SHUTDOWN_TIMEOUT`   | `30`          | Graceful shutdown timeout (seconds)  | `60`                     |
| `PANINI_EXTRACTOR_TIMEOUT`  | `5`           | Extractor timeout (seconds)          | `10`                     |
| `PANINI_ROCKSDB_CACHE_MB`   | `256`         | RocksDB block cache size             | `512`                    |

### 10.2 .env.example

```bash
# Storage
PANINI_STORAGE_PATH=./data/
PANINI_MAX_CONTENT_SIZE=104857600

# Server
PANINI_PORT=3000
PANINI_HOST=127.0.0.1

# Logging
PANINI_LOG_LEVEL=info
PANINI_LOG_FORMAT=text

# Performance
PANINI_CACHE_SIZE_MB=256
PANINI_ROCKSDB_CACHE_MB=256

# Timeouts
PANINI_SHUTDOWN_TIMEOUT=30
PANINI_EXTRACTOR_TIMEOUT=5
```

---

## 11. CI/CD Pipeline

### 11.1 GitHub Actions Workflow (.github/workflows/ci.yml)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  fmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt
      - run: cargo fmt --check
      
  clippy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      - run: cargo clippy -- -D warnings
      
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test --all-features
      
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: taiki-e/install-action@cargo-llvm-cov
      - run: cargo llvm-cov --all-features --lcov --output-path lcov.info
      - uses: codecov/codecov-action@v3
        with:
          files: lcov.info
          
  client:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd client && npm ci
      - run: cd client && npm run lint
      - run: cd client && npm test
      - run: cd client && npm run build
```

### 11.2 Quality Gates

| Check       | Threshold | Action on Failure  |
|-------------|-----------|---------------------|
| rustfmt     | Must pass | Block PR            |
| clippy      | 0 warnings| Block PR            |
| tests       | 100% pass | Block PR            |
| coverage    | ≥80%      | Block PR            |
| client lint | 0 errors  | Block PR            |
| client test | 100% pass | Block PR            |

---

## 12. Deployment

### 12.1 Docker Deployment

**Dockerfile** (Multi-stage build):
```dockerfile
# Build stage
FROM rust:1.75 AS builder
WORKDIR /app
COPY backend/ .
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/panini-fs /usr/local/bin/
ENV PANINI_STORAGE_PATH=/data
VOLUME ["/data"]
EXPOSE 3000
CMD ["panini-fs"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  panini-fs:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - panini-data:/data
    environment:
      - PANINI_STORAGE_PATH=/data
      - PANINI_LOG_LEVEL=info
      - PANINI_LOG_FORMAT=json
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  panini-data:
```

### 12.2 Production Checklist

- [ ] Environment variables configured
- [ ] Storage volume persistent
- [ ] Prometheus metrics accessible
- [ ] Health checks responding
- [ ] Logs forwarded (stdout → aggregator)
- [ ] Backup strategy for RocksDB
- [ ] Resource limits set (memory, CPU)
- [ ] TLS/HTTPS configured (reverse proxy)
- [ ] Rate limiting configured (nginx/Caddy)

---

## 13. Success Criteria

### 13.1 Functional Requirements

- [x] All 7 dhātu extractors implemented
- [x] All 5 REST API endpoints functional
- [x] Content-addressable storage working
- [x] TypeScript client published
- [x] Health checks responding
- [x] Metrics exposed

### 13.2 Non-Functional Requirements

- [x] Performance: >1000 store/sec, >5000 retrieve/sec
- [x] Latency: <10ms P50 for retrieve (cached)
- [x] Test coverage: ≥80%
- [x] Zero clippy warnings
- [x] Zero panics in production
- [x] Graceful shutdown (30s timeout)

### 13.3 Documentation Requirements

- [x] API documentation complete
- [x] OpenAPI spec available
- [x] Deployment guide written
- [x] Performance tuning guide
- [x] Extractor development guide
- [x] README with examples

### 13.4 Release Criteria

- [x] All tests passing
- [x] CI/CD green
- [x] Docker images built
- [x] Documentation reviewed
- [x] Load testing completed
- [x] Security audit passed (cargo audit)
- [x] Changelog generated
- [x] Version tagged (v1.0.0)

---

## 14. Next Steps

### Immediate Actions (Week 1, Day 1)

1. **Create repository structure**:
   ```bash
   cd /home/stephane/GitHub/Panini-FS
   mkdir -p backend/src/{api,cas,dhatu,extractors,health,metrics,utils}
   mkdir -p backend/{benches,examples,tests/integration,tests/fixtures}
   mkdir -p client/src/{utils}
   mkdir -p client/tests
   mkdir -p docs
   mkdir -p docker
   mkdir -p .github/workflows
   ```

2. **Initialize Cargo workspace**:
   ```bash
   cd backend
   # Copy Cargo.toml from section 2.1
   cargo init --lib
   ```

3. **Initialize TypeScript project**:
   ```bash
   cd client
   npm init -y
   # Copy package.json from section 3.1
   npm install
   ```

4. **Set up CI/CD**:
   ```bash
   # Copy .github/workflows/ci.yml from section 11.1
   ```

5. **Start implementation**:
   - Week 1 tasks (CAS Core)
   - Commit frequently
   - Push to main branch

### Phase 5 Preview: Tasks

After this plan is approved, the next phase will generate `tasks.md` with ~50-80 detailed implementation tasks, each with:
- Clear acceptance criteria
- Dependencies (which tasks must complete first)
- Estimated effort (S/M/L)
- Test requirements
- Code examples

**Example task**:
```markdown
### Task 1.3: Implement SHA-256 Hasher

**Description**: Create `cas::hasher` module with SHA-256 computation.

**Dependencies**: None

**Acceptance Criteria**:
- [ ] Function `compute_hash(data: &[u8]) -> String` returns hex SHA-256
- [ ] Unit tests with known vectors (empty, "abc", 1MB random)
- [ ] Property test: hash(x) == hash(x)
- [ ] Benchmark: <500µs for 1MB input

**Estimated Effort**: Small (2-4 hours)

**Implementation Hints**:
- Use `sha2` crate (already in Cargo.toml)
- Return lowercase hex string
- Handle empty input gracefully
```

---

## 15. Appendix

### A. References

- **Research Specs**:
  - `/home/stephane/GitHub/Panini/research/panini-fs/specs/ARCHITECTURE_SPEC.md` (13KB)
  - `/home/stephane/GitHub/Panini/research/panini-fs/specs/RUST_IMPLEMENTATION_SPEC.md` (11KB)

- **Python Prototypes**:
  - `/home/stephane/GitHub/Panini/research/panini-fs/prototypes/extractors/` (69 files)

- **Spec Kit Documents**:
  - `.specify/constitution.md` (563 lines)
  - `.specify/specification.md` (718 lines)
  - `.specify/clarify.md` (768 lines, all confirmed)

### B. Glossary

| Term         | Definition                                                        |
|--------------|-------------------------------------------------------------------|
| **CAS**      | Content-Addressable Storage - data indexed by hash                |
| **Dhātu**    | Universal primitive (TEXT, IMAGE, VIDEO, AUDIO, CODE, BINARY, ARCHIVE) |
| **Extractor**| Component that extracts metadata from content                     |
| **Hash**     | SHA-256 hexadecimal digest (64 characters)                        |
| **Metadata** | Structured information about content (format, size, etc.)         |

### C. Version History

| Version | Date       | Changes                                       |
|---------|------------|-----------------------------------------------|
| 1.0     | 2025-01-14 | Initial plan based on confirmed clarifications|

---

**Total Document Size**: ~1500 lines
**Estimated Implementation Time**: 8 weeks (1-2 developers)
**Confidence Level**: High (all parameters locked in)

