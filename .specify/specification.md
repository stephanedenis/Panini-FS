# Panini-FS Specification

**Project**: Panini-FS - Content-Addressed Semantic Filesystem  
**Version**: 1.0.0  
**Created**: 2025-10-28  
**Status**: Phase 2 - Baseline Specification

---

## 📚 Specification Sources

This specification is based on comprehensive research and prototypes from the **Panini Research Repository**.

### Primary Specification Documents

1. **Architecture Specification**
   - **Location**: `../Panini/research/panini-fs/specs/ARCHITECTURE_SPEC.md`
   - **Size**: 13KB
   - **Content**: Complete system architecture, dhātu theory, content addressing model
   - **Key Sections**:
     - 7 Universal Dhātu primitives
     - Content Addressing System (CAS)
     - Storage architecture (RocksDB)
     - API design patterns
     - Data flow diagrams

2. **Rust Implementation Specification**
   - **Location**: `../Panini/research/panini-fs/specs/RUST_IMPLEMENTATION_SPEC.md`
   - **Size**: 11KB
   - **Content**: Detailed Rust implementation guide
   - **Key Sections**:
     - Module structure
     - Type definitions
     - Error handling patterns
     - Async/await patterns
     - Testing strategies

3. **Prototype Extractors**
   - **Location**: `../Panini/research/panini-fs/prototypes/extractors/`
   - **Count**: 69 Python extractors
   - **Coverage**: All 7 dhātu types with multiple variants
   - **Purpose**: Reference implementations to be ported to Rust

### Supporting Documentation

4. **Format Grammars**
   - **Location**: `../Panini/research/panini-fs/format_grammars/`
   - **Content**: Formal grammars for file format parsing

5. **Benchmarks**
   - **Location**: `../Panini/research/panini-fs/benchmarks/`
   - **Content**: Performance benchmarks and test datasets

6. **Vision Documentation**
   - **Location**: `../Panini/research/panini-fs/docs/VISION_ECOSYSTEME.md`
   - **Content**: High-level project vision and ecosystem overview

---

## 🎯 Core Requirements

### 1. Content-Addressed Storage (CAS)

**Requirement**: Implement immutable content storage with cryptographic addressing

**Details**:
- Use SHA-256 for content hashing (64-character hex strings)
- Store content with hash as key in RocksDB
- Support deduplication automatically (same content = same hash)
- Verify integrity on retrieval

**API**:
```rust
pub async fn store(content: &[u8]) -> Result<String, PaniniError>;
pub async fn retrieve(hash: &str) -> Result<Vec<u8>, PaniniError>;
pub async fn exists(hash: &str) -> Result<bool, PaniniError>;
```

**Example**:
```rust
let content = b"Hello, Panini!";
let hash = storage.store(content).await?;
// hash: "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447"

let retrieved = storage.retrieve(&hash).await?;
assert_eq!(content, retrieved.as_slice());
```

### 2. Seven Dhātu Extractors

**Requirement**: Implement extractors for all 7 universal semantic primitives

#### 2.1 TEXT Extractor

**Dhātu Type**: `TEXT`

**Purpose**: Extract and analyze textual content

**Supported Formats**:
- Plain text (UTF-8, ASCII)
- Markdown (.md)
- Rich text formats (RTF)
- Document formats (TXT, DOC via conversion)

**Extraction Output**:
```rust
pub struct TextMetadata {
    pub dhatu: Dhatu,           // TEXT
    pub encoding: String,        // "utf-8", "ascii", etc.
    pub language: Option<String>, // "en", "fr", etc.
    pub line_count: usize,
    pub word_count: usize,
    pub char_count: usize,
    pub has_markdown: bool,
}
```

**Reference**: 12 Python prototype extractors in `prototypes/extractors/text_*.py`

#### 2.2 IMAGE Extractor

**Dhātu Type**: `IMAGE`

**Purpose**: Extract visual content metadata

**Supported Formats**:
- Raster: PNG, JPEG, GIF, BMP, WEBP
- Vector: SVG (as text-like)
- Raw: TIFF, RAW formats

**Extraction Output**:
```rust
pub struct ImageMetadata {
    pub dhatu: Dhatu,           // IMAGE
    pub format: String,          // "png", "jpeg", etc.
    pub width: u32,
    pub height: u32,
    pub color_space: String,     // "RGB", "RGBA", "Grayscale"
    pub bit_depth: u8,
    pub has_transparency: bool,
    pub exif: Option<ExifData>,
}
```

**Reference**: 10 Python prototype extractors in `prototypes/extractors/image_*.py`

#### 2.3 VIDEO Extractor

**Dhātu Type**: `VIDEO`

**Purpose**: Extract motion picture metadata

**Supported Formats**:
- MP4, AVI, MKV, MOV, WEBM
- FLV, WMV, M4V

**Extraction Output**:
```rust
pub struct VideoMetadata {
    pub dhatu: Dhatu,           // VIDEO
    pub format: String,          // "mp4", "avi", etc.
    pub duration_secs: f64,
    pub width: u32,
    pub height: u32,
    pub frame_rate: f64,
    pub codec: String,
    pub bitrate: u64,
    pub has_audio: bool,
}
```

**Reference**: 8 Python prototype extractors in `prototypes/extractors/video_*.py`

#### 2.4 AUDIO Extractor

**Dhātu Type**: `AUDIO`

**Purpose**: Extract sound/music metadata

**Supported Formats**:
- Compressed: MP3, AAC, OGG, OPUS
- Lossless: FLAC, WAV, AIFF
- Streaming: M4A, WMA

**Extraction Output**:
```rust
pub struct AudioMetadata {
    pub dhatu: Dhatu,           // AUDIO
    pub format: String,          // "mp3", "flac", etc.
    pub duration_secs: f64,
    pub sample_rate: u32,
    pub channels: u8,
    pub bitrate: u64,
    pub codec: String,
    pub id3_tags: Option<Id3Tags>,
}
```

**Reference**: 9 Python prototype extractors in `prototypes/extractors/audio_*.py`

#### 2.5 CODE Extractor

**Dhātu Type**: `CODE`

**Purpose**: Extract source code metadata

**Supported Languages**:
- Compiled: Rust, C, C++, Go, Java
- Interpreted: Python, JavaScript, Ruby, PHP
- Functional: Haskell, Lisp, Erlang
- Shell: Bash, Zsh, PowerShell

**Extraction Output**:
```rust
pub struct CodeMetadata {
    pub dhatu: Dhatu,           // CODE
    pub language: String,        // "rust", "python", etc.
    pub line_count: usize,
    pub comment_lines: usize,
    pub code_lines: usize,
    pub blank_lines: usize,
    pub functions: Vec<String>,
    pub imports: Vec<String>,
    pub syntax_valid: bool,
}
```

**Reference**: 15 Python prototype extractors in `prototypes/extractors/code_*.py`

#### 2.6 BINARY Extractor

**Dhātu Type**: `BINARY`

**Purpose**: Extract compiled executable metadata

**Supported Formats**:
- Linux: ELF (x86_64, ARM, RISC-V)
- Windows: PE/PE32+ (EXE, DLL)
- macOS: Mach-O
- Libraries: .so, .dylib, .dll

**Extraction Output**:
```rust
pub struct BinaryMetadata {
    pub dhatu: Dhatu,           // BINARY
    pub format: String,          // "elf", "pe", "macho"
    pub arch: String,            // "x86_64", "arm64"
    pub bits: u8,                // 32 or 64
    pub entry_point: u64,
    pub sections: Vec<String>,
    pub symbols: Vec<String>,
    pub is_stripped: bool,
}
```

**Reference**: 7 Python prototype extractors in `prototypes/extractors/binary_*.py`

#### 2.7 ARCHIVE Extractor

**Dhātu Type**: `ARCHIVE`

**Purpose**: Extract container/compressed archive metadata

**Supported Formats**:
- Compressed: ZIP, TAR.GZ, TAR.BZ2, 7Z, RAR
- Package: JAR, WAR, APK, DEB, RPM
- Container: ISO, IMG

**Extraction Output**:
```rust
pub struct ArchiveMetadata {
    pub dhatu: Dhatu,           // ARCHIVE
    pub format: String,          // "zip", "tar.gz", etc.
    pub compression: Option<String>, // "gzip", "bzip2", "xz"
    pub entry_count: usize,
    pub total_size: u64,
    pub compressed_size: u64,
    pub compression_ratio: f64,
    pub entries: Vec<ArchiveEntry>,
}

pub struct ArchiveEntry {
    pub path: String,
    pub size: u64,
    pub compressed_size: u64,
    pub modified: SystemTime,
}
```

**Reference**: 8 Python prototype extractors in `prototypes/extractors/archive_*.py`

---

## 🏗️ System Architecture

### Module Structure

**Backend Layout** (Rust):
```
backend/
├── Cargo.toml
├── src/
│   ├── main.rs              # Server entry point
│   ├── lib.rs               # Library exports
│   ├── api/                 # REST API handlers
│   │   ├── mod.rs
│   │   ├── store.rs         # POST /api/v1/store
│   │   ├── retrieve.rs      # GET /api/v1/content/:hash
│   │   ├── extract.rs       # POST /api/v1/extract
│   │   └── stats.rs         # GET /api/v1/stats
│   ├── cas/                 # Content Addressing System
│   │   ├── mod.rs
│   │   ├── hasher.rs        # SHA-256 hashing
│   │   └── storage.rs       # RocksDB interface
│   ├── extractors/          # Dhātu extractors
│   │   ├── mod.rs
│   │   ├── traits.rs        # Extractor trait
│   │   ├── text.rs          # TEXT extractor
│   │   ├── image.rs         # IMAGE extractor
│   │   ├── video.rs         # VIDEO extractor
│   │   ├── audio.rs         # AUDIO extractor
│   │   ├── code.rs          # CODE extractor
│   │   ├── binary.rs        # BINARY extractor
│   │   └── archive.rs       # ARCHIVE extractor
│   ├── dhatu/               # Dhātu types and logic
│   │   ├── mod.rs
│   │   ├── types.rs         # Dhatu enum
│   │   └── detector.rs      # Auto-detect dhātu
│   ├── error.rs             # Error types
│   ├── config.rs            # Configuration
│   └── utils.rs             # Utilities
└── tests/
    ├── integration/
    │   ├── api_tests.rs
    │   ├── cas_tests.rs
    │   └── extractor_tests.rs
    └── fixtures/
        └── test_files/      # Sample files for each dhātu
```

**Client Layout** (TypeScript):
```
client/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts             # Main export
│   ├── client.ts            # PaniniClient class
│   ├── types.ts             # Type definitions
│   ├── errors.ts            # Error classes
│   └── utils/
│       ├── hash.ts          # Client-side hashing
│       └── detector.ts      # Dhātu detection
├── tests/
│   └── client.test.ts
└── examples/
    ├── basic.ts
    └── advanced.ts
```

### Data Flow

**Store Operation**:
```
1. Client sends content → POST /api/v1/store
2. Server computes SHA-256 hash
3. Server checks if hash exists in RocksDB
4. If new: write content to RocksDB
5. Return hash to client
```

**Retrieve Operation**:
```
1. Client requests hash → GET /api/v1/content/:hash
2. Server looks up hash in RocksDB
3. If found: return content
4. If not found: return 404
```

**Extract Operation**:
```
1. Client sends content → POST /api/v1/extract
2. Server detects dhātu type (magic bytes, file extension)
3. Server calls appropriate extractor
4. Extractor analyzes content and returns metadata
5. Server optionally stores metadata with content hash
6. Return metadata to client
```

---

## 🔌 REST API Specification

### Base URL

```
http://localhost:8080/api/v1
```

### Endpoints

#### 1. Store Content

**Request**:
```http
POST /api/v1/store
Content-Type: application/octet-stream

<binary content>
```

**Response** (200 OK):
```json
{
  "hash": "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447",
  "size": 14,
  "already_exists": false
}
```

**Errors**:
- 400: Invalid content
- 413: Content too large (>100MB default)
- 500: Storage error

#### 2. Retrieve Content

**Request**:
```http
GET /api/v1/content/:hash
```

**Response** (200 OK):
```http
Content-Type: application/octet-stream
Content-Length: 14

<binary content>
```

**Errors**:
- 400: Invalid hash format
- 404: Content not found
- 500: Storage error

#### 3. Extract Metadata

**Request**:
```http
POST /api/v1/extract
Content-Type: application/json

{
  "hash": "a948904f...",
  "dhatu_hint": "TEXT"
}
```

**Response** (200 OK):
```json
{
  "hash": "a948904f...",
  "dhatu": "TEXT",
  "metadata": {
    "encoding": "utf-8",
    "language": "en",
    "line_count": 1,
    "word_count": 2,
    "char_count": 14
  }
}
```

**Errors**:
- 400: Invalid request
- 404: Content not found
- 422: Extraction failed
- 500: Server error

#### 4. Get Dhātu by Hash

**Request**:
```http
GET /api/v1/dhatu/:hash
```

**Response** (200 OK):
```json
{
  "hash": "a948904f...",
  "dhatu": "TEXT",
  "extracted_at": "2025-10-28T23:00:00Z",
  "metadata": { ... }
}
```

#### 5. System Statistics

**Request**:
```http
GET /api/v1/stats
```

**Response** (200 OK):
```json
{
  "total_content": 12345,
  "total_size_bytes": 987654321,
  "dhatu_counts": {
    "TEXT": 5000,
    "IMAGE": 3000,
    "VIDEO": 500,
    "AUDIO": 800,
    "CODE": 2000,
    "BINARY": 800,
    "ARCHIVE": 245
  },
  "uptime_secs": 86400
}
```

---

## 🧪 Testing Requirements

### Unit Tests

**Coverage Target**: 80% minimum (100% for critical paths)

**Critical Modules**:
- `cas::hasher` - 100% coverage
- `cas::storage` - 100% coverage
- All extractor modules - 90%+ coverage
- API handlers - 85%+ coverage

**Test Structure**:
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sha256_deterministic() {
        let content = b"test";
        let hash1 = compute_sha256(content);
        let hash2 = compute_sha256(content);
        assert_eq!(hash1, hash2);
    }

    #[tokio::test]
    async fn test_store_retrieve_roundtrip() {
        let storage = Storage::new_temp().await.unwrap();
        let content = b"Hello, World!";
        let hash = storage.store(content).await.unwrap();
        let retrieved = storage.retrieve(&hash).await.unwrap();
        assert_eq!(content, retrieved.as_slice());
    }
}
```

### Integration Tests

**API Tests**: Test all endpoints with real HTTP requests

**Example**:
```rust
#[tokio::test]
async fn test_api_store_and_retrieve() {
    let app = create_test_app().await;
    
    // Store content
    let response = app.post("/api/v1/store")
        .body(b"test content")
        .send()
        .await;
    assert_eq!(response.status(), 200);
    let json: StoreResponse = response.json().await;
    
    // Retrieve content
    let response = app.get(&format!("/api/v1/content/{}", json.hash))
        .send()
        .await;
    assert_eq!(response.status(), 200);
    assert_eq!(response.bytes().await, b"test content");
}
```

### Extractor Tests

**Test Fixtures**: One file per dhātu type in `tests/fixtures/test_files/`

**Required Tests**:
- Valid file detection
- Metadata extraction accuracy
- Error handling for corrupted files
- Performance benchmarks

---

## 🚀 Implementation Phases

### Phase 1: Core CAS (Week 1-2)

**Deliverables**:
- [ ] RocksDB storage implementation
- [ ] SHA-256 hashing
- [ ] Store/retrieve operations
- [ ] Basic error handling
- [ ] Unit tests (100% coverage)

### Phase 2: REST API (Week 3)

**Deliverables**:
- [ ] Axum server setup
- [ ] Store endpoint (POST /api/v1/store)
- [ ] Retrieve endpoint (GET /api/v1/content/:hash)
- [ ] Stats endpoint (GET /api/v1/stats)
- [ ] Integration tests

### Phase 3: Dhātu Extractors (Week 4-6)

**Deliverables**:
- [ ] Extractor trait design
- [ ] TEXT extractor (reference: 12 Python prototypes)
- [ ] IMAGE extractor (reference: 10 Python prototypes)
- [ ] VIDEO extractor (reference: 8 Python prototypes)
- [ ] AUDIO extractor (reference: 9 Python prototypes)
- [ ] CODE extractor (reference: 15 Python prototypes)
- [ ] BINARY extractor (reference: 7 Python prototypes)
- [ ] ARCHIVE extractor (reference: 8 Python prototypes)
- [ ] Auto-detection logic
- [ ] Extract endpoint (POST /api/v1/extract)
- [ ] Extractor tests (90%+ coverage)

### Phase 4: TypeScript Client (Week 7)

**Deliverables**:
- [ ] PaniniClient class
- [ ] Type definitions
- [ ] Error handling
- [ ] Examples and documentation
- [ ] Client tests

### Phase 5: Documentation & CI/CD (Week 8)

**Deliverables**:
- [ ] API documentation (OpenAPI)
- [ ] User guide with examples
- [ ] GitHub Actions CI/CD
- [ ] Docker deployment
- [ ] Performance benchmarks

---

## 📊 Performance Benchmarks

### Target Metrics

**Store Operations**:
- Small files (<1MB): >1000 ops/sec
- Medium files (1-10MB): >100 ops/sec
- Large files (10-100MB): >10 ops/sec

**Retrieve Operations**:
- Cached: >5000 ops/sec
- Uncached: >1000 ops/sec

**Extraction Operations**:
- TEXT: >500 ops/sec
- IMAGE: >200 ops/sec
- VIDEO: >50 ops/sec (metadata only)
- AUDIO: >300 ops/sec
- CODE: >400 ops/sec
- BINARY: >100 ops/sec
- ARCHIVE: >150 ops/sec

### Latency Targets

- P50: <10ms
- P95: <50ms
- P99: <100ms

---

## 🔗 References

### Research Repository

**Main Repository**: [Panini-Research](https://github.com/stephanedenis/Panini-Research)

**Key Documents**:
1. Architecture Spec: `research/panini-fs/specs/ARCHITECTURE_SPEC.md`
2. Rust Implementation Spec: `research/panini-fs/specs/RUST_IMPLEMENTATION_SPEC.md`
3. Prototype Extractors: `research/panini-fs/prototypes/extractors/` (69 files)
4. Format Grammars: `research/panini-fs/format_grammars/`
5. Vision Document: `research/panini-fs/docs/VISION_ECOSYSTEME.md`

### External Dependencies

**Rust Crates**:
- `tokio` - Async runtime
- `axum` - Web framework
- `rocksdb` - Storage backend
- `serde` - Serialization
- `sha2` - Hashing
- `anyhow` - Error handling

**TypeScript Packages**:
- `axios` - HTTP client
- `typescript` - Type system

---

**End of Specification**

This specification provides the complete baseline for implementing Panini-FS. All design decisions align with the constitution principles and reference the comprehensive research materials available in the Panini-Research repository.

**Next Phase**: `/speckit.plan` - Generate detailed implementation plan
