# Panini-FS API Documentation

**Version:** 2.0.0-alpha  
**Base URL:** `http://localhost:3000`  
**Protocol:** REST  
**Content-Type:** `application/json`

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Concepts API](#concepts-api)
4. [Relations API](#relations-api)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

---

## Overview

The Panini-FS REST API provides programmatic access to the Git-native knowledge graph. All data is stored in Git repositories with Markdown+YAML format.

**Key Features:**
- Full CRUD operations on concepts
- Relation management (8 relation types)
- Git-backed versioning
- JSON request/response
- CORS enabled

---

## Authentication

**Current Version:** No authentication (local development)

**Future:** OAuth2 + JWT tokens for production

---

## Concepts API

### List All Concepts

```http
GET /concepts
```

**Response:**
```json
[
  "concept_id_1",
  "concept_id_2",
  "concept_id_3"
]
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Server error

---

### Create Concept

```http
POST /concepts
Content-Type: application/json

{
  "id": "my_concept",
  "title": "My Concept",
  "dhatu": "SEEKING",
  "tags": ["tag1", "tag2"],
  "content": "Detailed description..."
}
```

**Required Fields:**
- `id` (string) - Unique identifier
- `title` (string) - Human-readable name

**Optional Fields:**
- `dhatu` (enum) - Emotional type (SEEKING, RAGE, FEAR, LUST, CARE, PANIC, PLAY)
- `tags` (array) - List of tags
- `content` (string) - Markdown content

**Response:**
```json
{
  "id": "my_concept",
  "title": "My Concept",
  "dhatu": "SEEKING",
  "tags": ["tag1", "tag2"],
  "content": "Detailed description..."
}
```

**Status Codes:**
- `201 Created` - Concept created
- `500 Internal Server Error` - Server error

---

### Get Concept

```http
GET /concepts/:id
```

**Path Parameters:**
- `id` (string) - Concept ID

**Response:**
```json
{
  "id": "my_concept",
  "title": "My Concept",
  "dhatu": "SEEKING",
  "tags": ["tag1", "tag2"],
  "content": "Detailed description..."
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Concept doesn't exist
- `500 Internal Server Error` - Server error

---

### Update Concept

```http
PUT /concepts/:id
Content-Type: application/json

{
  "id": "my_concept",
  "title": "Updated Title",
  "dhatu": "SEEKING",
  "tags": ["tag1", "tag2", "tag3"]
}
```

**Path Parameters:**
- `id` (string) - Concept ID (must match body `id`)

**Response:**
```json
{
  "id": "my_concept",
  "title": "Updated Title",
  "dhatu": "SEEKING",
  "tags": ["tag1", "tag2", "tag3"]
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - ID mismatch
- `500 Internal Server Error` - Server error

---

### Delete Concept

```http
DELETE /concepts/:id
```

**Path Parameters:**
- `id` (string) - Concept ID

**Response:** Empty body

**Status Codes:**
- `204 No Content` - Deleted successfully
- `500 Internal Server Error` - Server error

---

## Relations API

### Get Concept Relations

```http
GET /concepts/:id/relations
```

**Path Parameters:**
- `id` (string) - Source concept ID

**Response:**
```json
[
  {
    "source": "child_concept",
    "relation_type": "is_a",
    "target": "parent_concept",
    "confidence": 0.95,
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Server error

---

### Add Relation

```http
POST /concepts/:id/relations
Content-Type: application/json

{
  "rel_type": "is_a",
  "target": "parent_concept",
  "confidence": 0.95
}
```

**Path Parameters:**
- `id` (string) - Source concept ID

**Body Parameters:**
- `rel_type` (enum) - Relation type (see below)
- `target` (string) - Target concept ID
- `confidence` (float, optional) - Confidence score 0-1 (default: 1.0)

**Relation Types:**
- `is_a` - Taxonomic hierarchy (child is a parent)
- `part_of` - Compositional (part belongs to whole)
- `causes` - Causal (A causes B)
- `contradicts` - Opposition (A contradicts B)
- `supports` - Support (A supports B)
- `derives_from` - Derivation (A derives from B)
- `used_by` - Usage (A is used by B)
- `related_to` - Generic association

**Response:** Empty body

**Status Codes:**
- `201 Created` - Relation created
- `400 Bad Request` - Invalid relation type
- `500 Internal Server Error` - Server error

---

## Error Handling

**Error Response Format:**
```json
{
  "error": "Error description"
}
```

**Common Status Codes:**
- `200 OK` - Request succeeded
- `201 Created` - Resource created
- `204 No Content` - Deleted successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

## Examples

### Complete Workflow

#### 1. Create Parent Concept
```bash
curl -X POST http://localhost:3000/concepts \
  -H "Content-Type: application/json" \
  -d '{
    "id": "animal",
    "title": "Animal",
    "dhatu": "SEEKING"
  }'
```

#### 2. Create Child Concept
```bash
curl -X POST http://localhost:3000/concepts \
  -H "Content-Type: application/json" \
  -d '{
    "id": "dog",
    "title": "Dog",
    "dhatu": "CARE"
  }'
```

#### 3. Add Taxonomic Relation
```bash
curl -X POST http://localhost:3000/concepts/dog/relations \
  -H "Content-Type: application/json" \
  -d '{
    "rel_type": "is_a",
    "target": "animal",
    "confidence": 0.99
  }'
```

#### 4. Get Dog Relations
```bash
curl http://localhost:3000/concepts/dog/relations
```

#### 5. Update Dog Concept
```bash
curl -X PUT http://localhost:3000/concepts/dog \
  -H "Content-Type: application/json" \
  -d '{
    "id": "dog",
    "title": "Dog (Canis familiaris)",
    "dhatu": "CARE",
    "tags": ["mammal", "pet"]
  }'
```

#### 6. List All Concepts
```bash
curl http://localhost:3000/concepts
```

#### 7. Delete Concept
```bash
curl -X DELETE http://localhost:3000/concepts/dog
```

---

### Python Example

```python
import requests

BASE_URL = "http://localhost:3000"

# Create concept
response = requests.post(
    f"{BASE_URL}/concepts",
    json={
        "id": "quantum_computing",
        "title": "Quantum Computing",
        "dhatu": "SEEKING",
        "tags": ["physics", "computer-science"]
    }
)
print(f"Created: {response.status_code}")

# Get concept
response = requests.get(f"{BASE_URL}/concepts/quantum_computing")
concept = response.json()
print(f"Title: {concept['title']}")

# Add relation
response = requests.post(
    f"{BASE_URL}/concepts/quantum_computing/relations",
    json={
        "rel_type": "related_to",
        "target": "classical_computing",
        "confidence": 0.85
    }
)
print(f"Relation added: {response.status_code}")

# List all concepts
response = requests.get(f"{BASE_URL}/concepts")
concepts = response.json()
print(f"Total concepts: {len(concepts)}")
```

---

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:3000';

async function example() {
  // Create concept
  const createRes = await axios.post(`${BASE_URL}/concepts`, {
    id: 'machine_learning',
    title: 'Machine Learning',
    dhatu: 'SEEKING',
    tags: ['ai', 'data-science']
  });
  console.log('Created:', createRes.status);

  // Get concept
  const getRes = await axios.get(`${BASE_URL}/concepts/machine_learning`);
  console.log('Title:', getRes.data.title);

  // Add relation
  await axios.post(`${BASE_URL}/concepts/machine_learning/relations`, {
    rel_type: 'part_of',
    target: 'artificial_intelligence',
    confidence: 0.90
  });

  // Get relations
  const relsRes = await axios.get(`${BASE_URL}/concepts/machine_learning/relations`);
  console.log('Relations:', relsRes.data);
}

example();
```

---

## Health Check

```http
GET /health
```

**Response:** `OK`

**Status Code:** `200 OK`

Use this endpoint for monitoring and readiness checks.

---

## CORS

CORS is enabled with permissive settings for development. All origins are allowed.

**Headers:**
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

---

## Rate Limiting

**Current Version:** No rate limiting

**Future:** 1000 requests/hour per IP

---

## Versioning

**Current:** v2.0.0-alpha  
**Stability:** Alpha (breaking changes possible)  
**Support:** Development only

Production-ready API planned for v2.1.0 with:
- Authentication
- Rate limiting
- Pagination
- Filtering
- Full-text search endpoints

---

## Server Configuration

**Default Port:** 3000  
**Host:** 0.0.0.0 (all interfaces)  
**Max Body Size:** 10 MB  
**Timeout:** 30 seconds

Configure via environment variables (future):
```bash
PANINI_HOST=0.0.0.0
PANINI_PORT=3000
PANINI_TIMEOUT=30
```

---

## Support

- GitHub Issues: https://github.com/yourusername/Panini-FS/issues
- Documentation: https://github.com/yourusername/Panini-FS/docs
- Email: support@panini-fs.dev

---

**Last Updated:** 2025-10-29  
**API Version:** 2.0.0-alpha
