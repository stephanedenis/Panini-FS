# Panini-FS REST API Documentation

## Overview

The Panini-FS REST API provides HTTP access to the temporal filesystem with time-travel capabilities. All responses follow a consistent JSON format with success/error handling.

## Base URL

```
http://localhost:3000/api
```

## Response Format

All endpoints return JSON with the following structure:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

On error:

```json
{
  "success": false,
  "data": null,
  "error": "Error message"
}
```

## Endpoints

### Health Check

**GET** `/health`

Check if the API server is running.

**Response:**
```json
{
  "success": true,
  "data": "OK",
  "error": null
}
```

---

### List Concepts

**GET** `/concepts`

Get a list of all concepts in the system.

**Response:**
```json
{
  "success": true,
  "data": {
    "concepts": [
      {
        "id": "concept-123",
        "name": "my-document.txt",
        "current_version": "v3",
        "version_count": 3,
        "created_at": "2025-10-31T00:00:00Z",
        "updated_at": "2025-10-31T01:00:00Z"
      }
    ],
    "total": 1
  },
  "error": null
}
```

---

### Get Concept Details

**GET** `/concepts/:id`

Get detailed information about a specific concept including all versions.

**Parameters:**
- `id` (path): Concept ID

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "concept-123",
    "name": "my-document.txt",
    "current_version": "v3",
    "versions": [
      {
        "version_id": "v1",
        "parent": null,
        "timestamp": "2025-10-31T00:00:00Z",
        "author": "user@example.com",
        "message": "Initial version",
        "size": 1024,
        "atom_count": 2
      },
      {
        "version_id": "v2",
        "parent": "v1",
        "timestamp": "2025-10-31T00:30:00Z",
        "author": "user@example.com",
        "message": "Updated content",
        "size": 2048,
        "atom_count": 3
      }
    ],
    "created_at": "2025-10-31T00:00:00Z",
    "updated_at": "2025-10-31T01:00:00Z",
    "metadata": {}
  },
  "error": null
}
```

---

### Get Version Details

**GET** `/concepts/:id/versions/:version_id`

Get detailed information about a specific version of a concept.

**Parameters:**
- `id` (path): Concept ID
- `version_id` (path): Version ID

**Response:**
```json
{
  "success": true,
  "data": {
    "version_id": "v2",
    "parent": "v1",
    "atoms": [
      "sha256:abc123...",
      "sha256:def456...",
      "sha256:ghi789..."
    ],
    "size": 2048,
    "content_hash": "sha256:xyz...",
    "timestamp": "2025-10-31T00:30:00Z",
    "author": "user@example.com",
    "message": "Updated content",
    "metadata": {}
  },
  "error": null
}
```

---

### Get Timeline

**GET** `/timeline`

Get a timeline of all events in the system.

**Query Parameters:**
- `start` (optional): Start timestamp (ISO 8601 format)
- `end` (optional): End timestamp (ISO 8601 format)

**Example:**
```
GET /api/timeline?start=2025-10-31T00:00:00Z&end=2025-10-31T23:59:59Z
```

**Response:**
```json
{
  "success": true,
  "data": {
    "events": [
      {
        "type": "ConceptCreated",
        "timestamp": "2025-10-31T00:00:00Z",
        "concept_id": "concept-123",
        "concept_name": "my-document.txt",
        "version_id": "v1"
      },
      {
        "type": "ConceptModified",
        "timestamp": "2025-10-31T00:30:00Z",
        "concept_id": "concept-123",
        "concept_name": "my-document.txt",
        "version_id": "v2",
        "previous_version": "v1"
      },
      {
        "type": "SnapshotCreated",
        "timestamp": "2025-10-31T01:00:00Z",
        "snapshot_id": "snap-456",
        "snapshot_name": "backup-2025-10-31"
      }
    ],
    "total": 3
  },
  "error": null
}
```

---

### List Snapshots

**GET** `/snapshots`

Get a list of all snapshots in the system.

**Response:**
```json
{
  "success": true,
  "data": {
    "snapshots": [
      {
        "id": "snap-456",
        "name": "backup-2025-10-31",
        "timestamp": "2025-10-31T01:00:00Z",
        "concept_count": 10
      }
    ],
    "total": 1
  },
  "error": null
}
```

---

### Get Snapshot Details

**GET** `/snapshots/:id`

Get detailed information about a specific snapshot.

**Parameters:**
- `id` (path): Snapshot ID

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "snap-456",
    "name": "backup-2025-10-31",
    "timestamp": "2025-10-31T01:00:00Z",
    "concepts": {
      "concept-123": "v2",
      "concept-456": "v1"
    },
    "metadata": {}
  },
  "error": null
}
```

---

### Time Travel Query

**GET** `/time-travel`

Get the state of the system at a specific point in time.

**Query Parameters:**
- `timestamp` (required): Timestamp to query (ISO 8601 format)

**Example:**
```
GET /api/time-travel?timestamp=2025-10-31T00:30:00Z
```

**Response:**
```json
{
  "success": true,
  "data": {
    "timestamp": "2025-10-31T00:30:00Z",
    "concepts": {
      "concept-123": "v2",
      "concept-456": "v1"
    }
  },
  "error": null
}
```

---

### Get Version Diff

**GET** `/concepts/:id/diff`

Get the differences between two versions of a concept.

**Parameters:**
- `id` (path): Concept ID

**Query Parameters:**
- `from` (required): From version ID
- `to` (required): To version ID

**Example:**
```
GET /api/concepts/concept-123/diff?from=v1&to=v2
```

**Response:**
```json
{
  "success": true,
  "data": {
    "from": "v1",
    "to": "v2",
    "added_atoms": [
      "sha256:newatom1...",
      "sha256:newatom2..."
    ],
    "removed_atoms": [
      "sha256:oldatom1..."
    ],
    "size_change": 1024
  },
  "error": null
}
```

---

### Get System Statistics

**GET** `/stats`

Get overall system statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_concepts": 10,
    "total_versions": 25,
    "total_snapshots": 3,
    "total_atoms": 1024,
    "total_size": 10485760,
    "dedup_savings": 2621440
  },
  "error": null
}
```

---

## Configuration

The server can be configured using environment variables:

### Environment Variables

- `PANINI_STORAGE`: Storage directory path (default: `/tmp/panini-storage`)
- `PANINI_HOST`: Server host (default: `127.0.0.1`)
- `PANINI_PORT`: Server port (default: `3000`)
- `RUST_LOG`: Logging level (default: `info`)

### Example

```bash
PANINI_STORAGE=/var/lib/panini \
PANINI_HOST=0.0.0.0 \
PANINI_PORT=8080 \
RUST_LOG=debug \
./panini-api
```

---

## Running the Server

### From Source

```bash
cd /path/to/Panini-FS
cargo run --bin panini-api
```

### From Binary

```bash
./target/release/panini-api
```

### Production

```bash
# Build release binary
cargo build --release --bin panini-api

# Run with production settings
PANINI_STORAGE=/var/lib/panini \
PANINI_HOST=0.0.0.0 \
PANINI_PORT=80 \
RUST_LOG=warn \
./target/release/panini-api
```

---

## Client Examples

### JavaScript/TypeScript

```typescript
const BASE_URL = 'http://localhost:3000/api';

async function getConcepts() {
  const response = await fetch(`${BASE_URL}/concepts`);
  const result = await response.json();
  
  if (result.success) {
    return result.data.concepts;
  } else {
    throw new Error(result.error);
  }
}

async function timeTravelQuery(timestamp: string) {
  const params = new URLSearchParams({ timestamp });
  const response = await fetch(`${BASE_URL}/time-travel?${params}`);
  const result = await response.json();
  
  if (result.success) {
    return result.data;
  } else {
    throw new Error(result.error);
  }
}
```

### Python

```python
import requests
from datetime import datetime

BASE_URL = 'http://localhost:3000/api'

def get_concepts():
    response = requests.get(f'{BASE_URL}/concepts')
    result = response.json()
    
    if result['success']:
        return result['data']['concepts']
    else:
        raise Exception(result['error'])

def time_travel_query(timestamp: datetime):
    params = {'timestamp': timestamp.isoformat()}
    response = requests.get(f'{BASE_URL}/time-travel', params=params)
    result = response.json()
    
    if result['success']:
        return result['data']
    else:
        raise Exception(result['error'])
```

### curl

```bash
# Health check
curl http://localhost:3000/api/health

# Get all concepts
curl http://localhost:3000/api/concepts | jq .

# Time travel query
curl "http://localhost:3000/api/time-travel?timestamp=2025-10-31T00:30:00Z" | jq .

# Get stats
curl http://localhost:3000/api/stats | jq .
```

---

## Error Handling

### HTTP Status Codes

- `200 OK`: Request succeeded
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `501 Not Implemented`: Feature not yet implemented

### Error Response Format

```json
{
  "success": false,
  "data": null,
  "error": "Detailed error message"
}
```

---

## Next Steps

1. **Web UI**: Interactive timeline visualization and concept browser
2. **FUSE Filesystem**: Mount the temporal filesystem at `/mnt/panini/`
3. **Dhātu Classification**: Semantic organization by universal primitives
4. **Real-time Updates**: WebSocket support for live notifications
5. **Authentication**: User authentication and authorization
6. **Rate Limiting**: API rate limiting and quotas

---

## Architecture

The REST API is built with:

- **Axum**: Fast, ergonomic web framework
- **Tower**: Middleware (CORS, tracing)
- **Tokio**: Async runtime
- **Serde**: JSON serialization
- **Tracing**: Structured logging

The API serves as the HTTP interface to the immutable temporal filesystem, providing access to:

- **TemporalIndex**: Time-travel queries, snapshots, timeline
- **ContentAddressedStorage**: Atomic storage, deduplication
- **LocalFsBackend**: Sharded filesystem storage

All operations are Copy-on-Write, ensuring data immutability and enabling perfect time-travel capabilities.
