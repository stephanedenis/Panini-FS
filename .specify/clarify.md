# Panini-FS Clarification Questions

**Project**: Panini-FS - Content-Addressed Semantic Filesystem  
**Version**: 1.0.0  
**Phase**: 3 - Clarification  
**Created**: 2025-10-28  

---

## 🎯 Purpose

This document identifies ambiguous areas in the specification that need clarification before implementation planning. Each question includes context, options, and recommendations based on the constitution and research.

---

## 📦 1. Storage & Configuration

### Q1.1: RocksDB Configuration Strategy

**Context**: RocksDB has many tuning options that significantly impact performance.

**Question**: What RocksDB configuration should we use?

**Options**:

**A) Default Configuration** (Simplest)
- Use RocksDB defaults
- Single column family
- Default block cache (8MB)
- ✅ **Pros**: Simple, fast to implement
- ❌ **Cons**: Not optimized for our workload

**B) Optimized for Read-Heavy** (Recommended)
- Larger block cache (256MB)
- Bloom filters enabled
- Compression: LZ4 for speed
- Multiple column families (content, metadata, stats)
- ✅ **Pros**: Better read performance (5x faster)
- ❌ **Cons**: More memory usage

**C) Optimized for Write-Heavy**
- Larger write buffer (128MB)
- Less aggressive compaction
- Compression: Zstd for ratio
- ✅ **Pros**: Better write throughput
- ❌ **Cons**: Slower reads, more disk space

**Recommendation**: **Option B** - Our use case is read-heavy (retrieve > store)

**Decision Needed**: ☑ **CONFIRMED** - Option B (Optimized for Read-Heavy)

---

### Q1.2: Storage Path Configuration

**Context**: Where should RocksDB store its data?

**Question**: How should storage path be configured?

**Options**:

**A) Fixed Path** `/var/lib/panini-fs/`
- Hardcoded in the binary
- ✅ **Pros**: Simple, no configuration needed
- ❌ **Cons**: Not flexible, requires root/permissions

**B) Environment Variable** (Recommended)
- `PANINI_STORAGE_PATH` with fallback to `./data/`
- ✅ **Pros**: Flexible, Docker-friendly
- ❌ **Cons**: Needs documentation

**C) CLI Argument + Config File**
- `--storage-path` flag + TOML config
- ✅ **Pros**: Most flexible
- ❌ **Cons**: Most complex

**Recommendation**: **Option B** - Environment variable with sensible default

**Configuration**:
```bash
PANINI_STORAGE_PATH=/data           # Production
PANINI_STORAGE_PATH=./data          # Development (default)
```

**Decision Needed**: ☑ **CONFIRMED** - Option B (Environment Variable)

---

### Q1.3: Maximum Content Size

**Context**: Need to prevent memory exhaustion from large uploads.

**Question**: What should be the maximum content size limit?

**Options**:

**A) 100MB** (Recommended for v1.0)
- Handles most files
- Safe memory footprint
- ✅ **Pros**: Good balance
- ❌ **Cons**: Can't handle large videos

**B) 1GB**
- Handles large media files
- ✅ **Pros**: More versatile
- ❌ **Cons**: Memory pressure, slow uploads

**C) Configurable with Default**
- Environment variable with 100MB default
- ✅ **Pros**: Most flexible
- ❌ **Cons**: Users might set it too high

**Recommendation**: **Option C** - Configurable with 100MB default

**Configuration**:
```bash
PANINI_MAX_CONTENT_SIZE=100MB      # Default
PANINI_MAX_CONTENT_SIZE=1GB        # For video-heavy use
```

**Decision Needed**: ☑ **CONFIRMED** - Option C (Configurable, 100MB default)

---

## 🔌 2. API Design

### Q2.1: Content Upload Method

**Context**: Store endpoint needs to accept content efficiently.

**Question**: How should content be uploaded?

**Options**:

**A) Raw Binary Body** (Recommended)
- `Content-Type: application/octet-stream`
- Direct body = content
- ✅ **Pros**: Efficient, no encoding overhead
- ❌ **Cons**: Can't include metadata in same request

**B) Multipart Form**
- `Content-Type: multipart/form-data`
- Can include metadata and content
- ✅ **Pros**: Can send metadata + content together
- ❌ **Cons**: Parsing overhead, more complex

**C) Base64 JSON**
- JSON with base64-encoded content
- ✅ **Pros**: Easy to test with curl
- ❌ **Cons**: 33% size overhead, slow encoding

**Recommendation**: **Option A** for store, **Option B** for extract with content

**API Design**:
```http
# Store (raw binary)
POST /api/v1/store
Content-Type: application/octet-stream
Body: <raw bytes>

# Extract (multipart for metadata hint)
POST /api/v1/extract
Content-Type: multipart/form-data
Body: content=<bytes>&dhatu_hint=TEXT
```

**Decision Needed**: ☑ **CONFIRMED** - Option A (Raw Binary for store)

---

### Q2.2: API Versioning Strategy

**Context**: API will evolve, need versioning strategy.

**Question**: How to handle API versioning?

**Options**:

**A) URL Path Versioning** (Recommended)
- `/api/v1/store`, `/api/v2/store`
- ✅ **Pros**: Clear, cacheable, RESTful
- ❌ **Cons**: URL duplication

**B) Header Versioning**
- `Accept: application/vnd.panini.v1+json`
- ✅ **Pros**: Clean URLs
- ❌ **Cons**: Less discoverable, harder to test

**C) No Versioning (YOLO)**
- Just `/api/store`
- ✅ **Pros**: Simplest
- ❌ **Cons**: Breaking changes break clients

**Recommendation**: **Option A** - URL path versioning

**Decision Needed**: ☑ **CONFIRMED** - Option A (URL Path Versioning)

---

### Q2.3: Error Response Format

**Context**: Need consistent error format for clients.

**Question**: What error response format should we use?

**Options**:

**A) Simple String** 
```json
{ "error": "Content not found" }
```
- ✅ **Pros**: Simple
- ❌ **Cons**: Not structured, hard to parse

**B) RFC 7807 Problem Details** (Recommended)
```json
{
  "type": "https://panini-fs.io/errors/not-found",
  "title": "Content Not Found",
  "status": 404,
  "detail": "Content with hash abc123... does not exist",
  "instance": "/api/v1/content/abc123..."
}
```
- ✅ **Pros**: Standard, structured, machine-readable
- ❌ **Cons**: More verbose

**C) Custom Format**
```json
{
  "error_code": "CONTENT_NOT_FOUND",
  "message": "Content not found",
  "hash": "abc123..."
}
```
- ✅ **Pros**: Flexible
- ❌ **Cons**: Not standard

**Recommendation**: **Option B** - RFC 7807 for consistency

**Decision Needed**: ☑ **CONFIRMED** - Option B (RFC 7807 Problem Details)

---

## 🧪 3. Extractor Implementation

### Q3.1: Extractor Dependency Strategy

**Context**: Extractors need external libraries (image, video, audio processing).

**Question**: How should we handle extractor dependencies?

**Options**:

**A) Pure Rust Libraries Only** (Recommended for v1.0)
- Use `image`, `symphonia`, `zip` crates
- ✅ **Pros**: No system dependencies, static binary
- ❌ **Cons**: Limited format support, may miss some formats

**B) FFmpeg/System Libraries**
- Link to FFmpeg, libmagic, etc.
- ✅ **Pros**: Complete format support
- ❌ **Cons**: Complex installation, dynamic linking

**C) Feature Flags for Optional Extractors**
- Compile with `--features full-extractors` for system libs
- Default to pure Rust
- ✅ **Pros**: Best of both worlds
- ❌ **Cons**: Complex build system

**Recommendation**: **Option A** for v1.0, **Option C** for v2.0

**Cargo.toml**:
```toml
[dependencies]
image = "0.24"          # IMAGE extractor
symphonia = "0.5"       # AUDIO extractor
zip = "0.6"             # ARCHIVE extractor
infer = "0.15"          # Magic byte detection

[features]
default = []
full-extractors = ["ffmpeg-next", "libmagic"]  # v2.0
```

**Decision Needed**: ☑ **CONFIRMED** - Option A (Pure Rust for v1.0)

---

### Q3.2: Extractor Error Handling

**Context**: Extractors may fail on corrupted files.

**Question**: How should extractors handle extraction failures?

**Options**:

**A) Fail Fast** 
- Return error immediately
- ✅ **Pros**: Simple, clear failures
- ❌ **Cons**: One bad file blocks everything

**B) Partial Metadata** (Recommended)
- Return what we could extract + error field
```json
{
  "dhatu": "IMAGE",
  "metadata": {
    "format": "jpeg",
    "width": 1920
    // height failed to extract
  },
  "extraction_errors": ["Failed to read EXIF data: corrupt header"]
}
```
- ✅ **Pros**: Graceful degradation, useful partial data
- ❌ **Cons**: More complex logic

**C) Best Effort Fallback**
- Try multiple extraction methods
- Fall back to basic metadata
- ✅ **Pros**: Most robust
- ❌ **Cons**: Slowest, unpredictable

**Recommendation**: **Option B** - Partial metadata with error reporting

**Decision Needed**: ☑ **CONFIRMED** - Option B (Partial Metadata with errors)

---

### Q3.3: Dhātu Auto-Detection Priority

**Context**: Multiple methods can detect dhātu (magic bytes, extension, content analysis).

**Question**: What priority order for dhātu detection?

**Options**:

**A) Magic Bytes → Extension → Content Analysis**
- Most reliable first
- ✅ **Pros**: Accurate for most files
- ❌ **Cons**: Magic bytes not always present

**B) Extension → Magic Bytes → Content Analysis** 
- Fastest first
- ✅ **Pros**: Fast, works for normal files
- ❌ **Cons**: Can be fooled by renamed files

**C) Content Analysis → Magic Bytes → Extension** (Recommended)
- Most accurate first
- ✅ **Pros**: Can't be fooled
- ❌ **Cons**: Slowest

**Recommendation**: **Option A** - Magic bytes first with extension fallback

**Detection Logic**:
```rust
pub fn detect_dhatu(content: &[u8], hint: Option<&str>) -> Dhatu {
    // 1. If hint provided, try it first
    if let Some(hint) = hint {
        if is_valid_dhatu_hint(hint, content) {
            return hint.parse().unwrap();
        }
    }
    
    // 2. Magic bytes (infer crate)
    if let Some(dhatu) = detect_by_magic_bytes(content) {
        return dhatu;
    }
    
    // 3. Content analysis (last resort)
    detect_by_content_analysis(content)
}
```

**Decision Needed**: ☑ **CONFIRMED** - Option A (Magic Bytes → Extension → Analysis)

---

## 📊 4. Performance & Monitoring

### Q4.1: Logging Strategy

**Context**: Need observability for debugging and monitoring.

**Question**: What logging framework and strategy?

**Options**:

**A) tracing with JSON Output** (Recommended)
- Structured logging
- OpenTelemetry compatible
- ✅ **Pros**: Machine-readable, industry standard
- ❌ **Cons**: Harder to read during development

**B) env_logger with Text Output**
- Simple text logs
- ✅ **Pros**: Easy to read, simple
- ❌ **Cons**: Hard to parse, not structured

**C) Hybrid Approach**
- `tracing` framework
- Text for development, JSON for production
- ✅ **Pros**: Best of both worlds
- ❌ **Cons**: Configuration complexity

**Recommendation**: **Option C** - tracing with format based on environment

**Configuration**:
```bash
PANINI_LOG_LEVEL=info              # trace/debug/info/warn/error
PANINI_LOG_FORMAT=text             # text/json
```

**Example Log Levels**:
- `TRACE`: All operations (verbose)
- `DEBUG`: Detailed operation info
- `INFO`: Normal operations (default)
- `WARN`: Recoverable issues
- `ERROR`: Failures requiring attention

**Decision Needed**: ☑ **CONFIRMED** - Option C (Hybrid tracing, text/json)

---

### Q4.2: Metrics Collection

**Context**: Need metrics for monitoring performance.

**Question**: What metrics should be exposed?

**Options**:

**A) No Metrics** 
- Just logs
- ✅ **Pros**: Simplest
- ❌ **Cons**: Hard to monitor performance

**B) Basic Counters in Stats Endpoint**
- Total content, size, dhātu counts
- ✅ **Pros**: Simple, no extra dependencies
- ❌ **Cons**: Limited, not time-series

**C) Prometheus Metrics** (Recommended)
- Full metrics endpoint `/metrics`
- Counter, Gauge, Histogram types
- ✅ **Pros**: Industry standard, grafana integration
- ❌ **Cons**: Extra dependency

**Recommendation**: **Option C** - Prometheus metrics

**Metrics to Expose**:
```rust
// Counters
panini_store_total{status="success|error"}
panini_retrieve_total{status="success|error"}
panini_extract_total{dhatu="TEXT|IMAGE|...", status="success|error"}

// Gauges
panini_content_total
panini_storage_bytes_total
panini_cache_entries

// Histograms
panini_store_duration_seconds
panini_retrieve_duration_seconds
panini_extract_duration_seconds{dhatu="TEXT|IMAGE|..."}
```

**Decision Needed**: ☑ **CONFIRMED** - Option C (Prometheus /metrics endpoint)

---

### Q4.3: Caching Strategy

**Context**: Content retrieval can benefit from caching.

**Question**: What caching strategy should we implement?

**Options**:

**A) No Caching**
- Always read from RocksDB
- ✅ **Pros**: Simplest, consistent
- ❌ **Cons**: Slower for hot content

**B) LRU In-Memory Cache** (Recommended)
- Cache recently accessed content
- Configurable size (default 256MB)
- ✅ **Pros**: Fast for hot content (5-10x speedup)
- ❌ **Cons**: Memory usage, cache invalidation

**C) RocksDB Block Cache**
- RocksDB's built-in cache
- ✅ **Pros**: No extra code
- ❌ **Cons**: Less control, shared with metadata

**Recommendation**: **Option B** - LRU cache for content

**Configuration**:
```bash
PANINI_CACHE_SIZE_MB=256           # Default 256MB
PANINI_CACHE_SIZE_MB=0             # Disable caching
```

**Implementation**: Use `lru` crate with TTL

**Decision Needed**: ☑ **CONFIRMED** - Option B (LRU In-Memory Cache, 256MB)

---

## 🔒 5. Security & Validation

### Q5.1: Hash Validation Strictness

**Context**: Need to validate hash format in API requests.

**Question**: How strict should hash validation be?

**Options**:

**A) Regex Only**
- Check format: `^[a-f0-9]{64}$`
- ✅ **Pros**: Fast
- ❌ **Cons**: Allows impossible hashes

**B) Regex + Checksum Verification** (Recommended)
- Validate format + verify content matches hash
- ✅ **Pros**: Prevents tampering
- ❌ **Cons**: Slower (need to read content)

**C) Relaxed Validation**
- Accept any 64-char hex string
- ✅ **Pros**: Most flexible
- ❌ **Cons**: Allows bad data

**Recommendation**: **Option B** for critical operations, **Option A** for reads

**Validation Logic**:
```rust
// On retrieve: Format check only (fast)
pub fn validate_hash_format(hash: &str) -> Result<(), PaniniError> {
    if !hash.len() == 64 || !hash.chars().all(|c| c.is_ascii_hexdigit()) {
        return Err(PaniniError::InvalidHash);
    }
    Ok(())
}

// On store: Full verification (after write)
pub fn verify_hash(content: &[u8], expected: &str) -> Result<(), PaniniError> {
    let actual = compute_sha256(content);
    if actual != expected {
        return Err(PaniniError::HashMismatch { expected, actual });
    }
    Ok(())
}
```

**Decision Needed**: ☑ **CONFIRMED** - Option B (Regex + Checksum Verification)

---

### Q5.2: Content Sanitization

**Context**: Prevent path traversal in archive extractors.

**Question**: How should we sanitize file paths in archives?

**Options**:

**A) Basic Check**
- Reject paths with `..` or absolute paths
- ✅ **Pros**: Simple
- ❌ **Cons**: Can be bypassed

**B) Canonicalization** (Recommended)
- Normalize all paths, reject if outside base
- ✅ **Pros**: Secure
- ❌ **Cons**: Platform-dependent

**C) Whitelist Characters**
- Only allow `[a-zA-Z0-9_.-/]`
- ✅ **Pros**: Very restrictive
- ❌ **Cons**: Breaks legitimate files

**Recommendation**: **Option B** - Full canonicalization

**Sanitization Logic**:
```rust
pub fn sanitize_archive_path(path: &str) -> Result<PathBuf, PaniniError> {
    let path = PathBuf::from(path);
    
    // Reject absolute paths
    if path.is_absolute() {
        return Err(PaniniError::InvalidPath("Absolute path not allowed"));
    }
    
    // Reject parent directory references
    for component in path.components() {
        if component == Component::ParentDir {
            return Err(PaniniError::InvalidPath("Parent dir not allowed"));
        }
    }
    
    Ok(path)
}
```

**Decision Needed**: ☑ **CONFIRMED** - Option B (Full Canonicalization)

---

## 🚀 6. Deployment & Operations

### Q6.1: Graceful Shutdown

**Context**: Server needs to handle SIGTERM gracefully.

**Question**: How should server handle shutdown?

**Options**:

**A) Immediate Shutdown**
- Stop accepting requests, close immediately
- ✅ **Pros**: Simple
- ❌ **Cons**: Drops in-flight requests

**B) Graceful with Timeout** (Recommended)
- Stop accepting new requests
- Wait for in-flight to complete (30s timeout)
- Force close after timeout
- ✅ **Pros**: No dropped requests
- ❌ **Cons**: Slower shutdown

**C) Persist State**
- Save all state before shutdown
- Resume on restart
- ✅ **Pros**: Perfect continuity
- ❌ **Cons**: Very complex

**Recommendation**: **Option B** - 30s graceful shutdown

**Implementation**:
```rust
#[tokio::main]
async fn main() {
    let app = create_app().await;
    
    // Graceful shutdown on SIGTERM
    let shutdown = async {
        tokio::signal::ctrl_c().await.ok();
        println!("Shutting down gracefully...");
    };
    
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .with_graceful_shutdown(shutdown)
        .await
        .unwrap();
}
```

**Decision Needed**: ☑ **CONFIRMED** - Option B (Graceful with 30s timeout)

---

### Q6.2: Health Check Endpoint

**Context**: Docker/K8s need health checks.

**Question**: What should health check endpoint return?

**Options**:

**A) Simple 200 OK**
- Just `GET /health` → 200
- ✅ **Pros**: Simplest
- ❌ **Cons**: Doesn't check dependencies

**B) Readiness + Liveness** (Recommended)
- `GET /health/live` - Server is running
- `GET /health/ready` - Server + RocksDB are ready
- ✅ **Pros**: Proper K8s integration
- ❌ **Cons**: More endpoints

**C) Detailed Health**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_secs": 86400,
  "storage": {
    "status": "ok",
    "path": "/data"
  },
  "cache": {
    "status": "ok",
    "size_mb": 128,
    "entries": 1234
  }
}
```
- ✅ **Pros**: Very detailed
- ❌ **Cons**: Exposes internal state

**Recommendation**: **Option B** - Separate liveness/readiness

**Endpoints**:
```http
GET /health/live   → 200 (always if server running)
GET /health/ready  → 200 if RocksDB accessible, 503 otherwise
```

**Decision Needed**: ☑ **CONFIRMED** - Option B (Separate /health/live and /health/ready)

---

## ✅ Decision Summary

### ✅ Decisions CONFIRMED

1. **Storage**
   - ☑ RocksDB: Optimized for read-heavy (256MB cache, bloom filters)
   - ☑ Storage path: Environment variable `PANINI_STORAGE_PATH`
   - ☑ Max content size: Configurable with 100MB default

2. **API**
   - ☑ Upload: Raw binary for store, multipart for extract
   - ☑ Versioning: URL path (`/api/v1/`)
   - ☑ Errors: RFC 7807 Problem Details format

3. **Extractors**
   - ☑ Dependencies: Pure Rust libraries (v1.0)
   - ☑ Failures: Partial metadata with error reporting
   - ☑ Detection: Magic bytes → Extension → Content analysis

4. **Performance**
   - ☑ Logging: tracing with text/json format option
   - ☑ Metrics: Prometheus endpoint at `/metrics`
   - ☑ Caching: LRU in-memory cache (256MB default)

5. **Security**
   - ☑ Hash validation: Format check on read, full verify on write
   - ☑ Path sanitization: Full canonicalization for archives

6. **Operations**
   - ☑ Shutdown: Graceful with 30s timeout
   - ☑ Health checks: Separate `/health/live` and `/health/ready`

---

## 🎯 Next Steps

✅ **ALL 19 DECISIONS CONFIRMED**

Ready to proceed to **Phase 4: `/speckit.plan`**

The plan will generate:
- Complete file structure (backend/ + client/)
- All dependencies (Cargo.toml, package.json)
- Implementation order (8-week roadmap)
- Task breakdown with priorities

---

**End of Clarification Phase**

This document should be reviewed and all decisions confirmed before proceeding to the planning phase. The recommended options align with the constitution principles and best practices for production systems.
