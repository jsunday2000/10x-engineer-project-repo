# PromptLab API Reference

**Complete API Documentation**

Version: 1.0.0  
Base URL: `http://localhost:8000` (local development)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Request/Response Format](#requestresponse-format)
3. [Error Handling](#error-handling)
4. [Health Check Endpoints](#health-check-endpoints)
5. [Prompt Endpoints](#prompt-endpoints)
6. [Collection Endpoints](#collection-endpoints)
7. [Error Response Reference](#error-response-reference)
8. [Status Codes](#status-codes)

---

## Authentication

**Current Status**: No authentication required

All endpoints are publicly accessible without authentication. This is suitable for internal tools and development environments. 

**Future Implementation Note**: For production deployments, consider implementing:
- API Key authentication
- JWT Bearer tokens
- OAuth 2.0
- Rate limiting by client ID

---

## Request/Response Format

### Content-Type Header

All requests and responses use **JSON** format.

**Request:**
```
Content-Type: application/json
```

**Response:**
```
Content-Type: application/json; charset=utf-8
```

### Timestamp Format

All timestamps use **ISO 8601** format with UTC timezone:
```
2024-02-16T10:30:00
```

### UUID Format

Resource IDs are **UUID v4** format:
```
"550e8400-e29b-41d4-a716-446655440000"
```

---

## Error Handling

### Error Response Structure

All error responses follow a consistent format:

```json
{
  "detail": "String describing the error"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful request with no content to return |
| 400 | Bad Request | Invalid request (validation error) |
| 404 | Not Found | Resource does not exist |
| 422 | Unprocessable Entity | Invalid data format or constraints violated |
| 500 | Internal Server Error | Server error |

### Common Error Scenarios

**Validation Error (400):**
```json
{
  "detail": "Collection not found"
}
```

**Resource Not Found (404):**
```json
{
  "detail": "Prompt not found"
}
```

**Validation Constraint (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

## Health Check Endpoints

### GET /health

Check API health and version status.

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Response Fields:**
- `status` (string): API health status. Expected value: `"healthy"`
- `version` (string): Current API version

**Error Responses:**
- None. This endpoint always returns 200 if the API is running.

---

## Prompt Endpoints

### GET /prompts

List all prompts with optional filtering and search.

**Request:**
```bash
curl -X GET "http://localhost:8000/prompts?search=customer&collection_id=col-123"
```

**Query Parameters:**
- `search` (optional, string): Search term for prompt title and description (case-insensitive)
- `collection_id` (optional, string): Filter prompts by collection UUID

**Response (200 OK):**
```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Customer Service Response",
      "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
      "description": "Template for responding to customer inquiries",
      "collection_id": "col-123",
      "created_at": "2024-02-16T10:30:00",
      "updated_at": "2024-02-16T10:30:15"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Email Draft",
      "content": "Draft a professional email in response to {{email_topic}}",
      "description": "Generate professional email drafts",
      "collection_id": "col-123",
      "created_at": "2024-02-16T09:15:00",
      "updated_at": "2024-02-16T09:15:00"
    }
  ],
  "total": 2
}
```

**Response Fields:**
- `prompts` (array): List of prompt objects
  - `id` (string): Unique prompt identifier (UUID)
  - `title` (string): Prompt title (1-200 characters)
  - `content` (string): Main prompt content
  - `description` (string, nullable): Optional description (max 500 characters)
  - `collection_id` (string, nullable): Parent collection UUID, if assigned
  - `created_at` (string): Creation timestamp (ISO 8601)
  - `updated_at` (string): Last update timestamp (ISO 8601)
- `total` (integer): Total number of prompts in result

**Error Responses:**
- None. Returns empty list if no prompts match filters.

**Sorting:**
- Results are always sorted by `created_at` in descending order (newest first)

---

### GET /prompts/{prompt_id}

Retrieve a specific prompt by ID.

**Request:**
```bash
curl -X GET http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt to retrieve

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Customer Service Response",
  "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
  "description": "Template for responding to customer inquiries",
  "collection_id": "col-123",
  "created_at": "2024-02-16T10:30:00",
  "updated_at": "2024-02-16T10:30:15"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

---

### POST /prompts

Create a new prompt.

**Request:**
```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Service Response",
    "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
    "description": "Template for responding to customer inquiries",
    "collection_id": null
  }'
```

**Request Body:**
```json
{
  "title": "Customer Service Response",
  "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
  "description": "Template for responding to customer inquiries",
  "collection_id": null
}
```

**Request Fields:**
- `title` (string, required): Prompt title (1-200 characters)
- `content` (string, required): Main prompt content (at least 1 character)
- `description` (string, optional): Detailed description (max 500 characters)
- `collection_id` (string, optional): UUID of parent collection (must exist if provided)

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Customer Service Response",
  "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
  "description": "Template for responding to customer inquiries",
  "collection_id": null,
  "created_at": "2024-02-16T10:30:00",
  "updated_at": "2024-02-16T10:30:00"
}
```

**Error Responses:**

**400 Bad Request** (collection not found):
```json
{
  "detail": "Collection not found"
}
```

**422 Unprocessable Entity** (validation error):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

### PUT /prompts/{prompt_id}

Replace an entire prompt (full update).

**Request:**
```bash
curl -X PUT http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Customer Service",
    "content": "New prompt content here",
    "description": "Updated description",
    "collection_id": null
  }'
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt to update

**Request Body:**
```json
{
  "title": "Updated Customer Service",
  "content": "New prompt content here",
  "description": "Updated description",
  "collection_id": null
}
```

**Request Fields:**
- `title` (string, optional): Updated title (1-200 characters)
- `content` (string, optional): Updated content
- `description` (string, optional): Updated description (max 500 characters)
- `collection_id` (string, optional): New collection UUID

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Customer Service",
  "content": "New prompt content here",
  "description": "Updated description",
  "collection_id": null,
  "created_at": "2024-02-16T10:30:00",
  "updated_at": "2024-02-16T10:45:30"
}
```

**Response Notes:**
- `created_at` remains unchanged from original
- `updated_at` is set to current timestamp

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

**400 Bad Request** (collection not found):
```json
{
  "detail": "Collection not found"
}
```

---

### PATCH /prompts/{prompt_id}

Partially update a prompt (only provided fields are updated).

**Request:**
```bash
curl -X PATCH http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title Only"
  }'
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt to update

**Request Body:**
```json
{
  "title": "New Title Only"
}
```

**Request Fields (all optional):**
- `title` (string, optional): Update only the title
- `content` (string, optional): Update only the content
- `description` (string, optional): Update only the description
- `collection_id` (string, optional): Reassign to different collection

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "New Title Only",
  "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
  "description": "Template for responding to customer inquiries",
  "collection_id": null,
  "created_at": "2024-02-16T10:30:00",
  "updated_at": "2024-02-16T10:45:30"
}
```

**Response Notes:**
- Only specified fields are updated
- Unchanged fields retain their previous values
- `created_at` remains unchanged
- `updated_at` is updated to current timestamp

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

**400 Bad Request** (collection not found):
```json
{
  "detail": "Collection not found"
}
```

---

### POST /prompts/{prompt_id}/versions

Create an immutable version snapshot from the current prompt state.

**Request:**
```bash
curl -X POST http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt to snapshot

**Response (201 Created):**
```json
{
  "id": "a7f44b5f-4d58-4a8d-9f41-5a2a4da6f0cd",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "version_number": 1,
  "title": "Customer Service Response",
  "content": "You are a helpful customer service agent...",
  "description": "Template for responding to customer inquiries",
  "collection_id": null,
  "created_at": "2024-02-16T11:00:00"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

---

### GET /prompts/{prompt_id}/versions

List all saved versions for a prompt.

**Request:**
```bash
curl -X GET http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt

**Response (200 OK):**
```json
{
  "versions": [
    {
      "id": "a7f44b5f-4d58-4a8d-9f41-5a2a4da6f0cd",
      "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
      "version_number": 1,
      "title": "Original Title",
      "content": "Original Content",
      "description": "Original description",
      "collection_id": null,
      "created_at": "2024-02-16T11:00:00"
    }
  ],
  "total": 1
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

---

### GET /prompts/{prompt_id}/versions/{version_id}

Retrieve a single saved version snapshot for a prompt.

**Request:**
```bash
curl -X GET http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/a7f44b5f-4d58-4a8d-9f41-5a2a4da6f0cd
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt
- `version_id` (string, required): UUID of the saved version snapshot

**Response (200 OK):**
```json
{
  "id": "a7f44b5f-4d58-4a8d-9f41-5a2a4da6f0cd",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "version_number": 1,
  "title": "Original Title",
  "content": "Original Content",
  "description": "Original description",
  "collection_id": null,
  "created_at": "2024-02-16T11:00:00"
}
```

**Error Responses:**

**404 Not Found (prompt):**
```json
{
  "detail": "Prompt not found"
}
```

**404 Not Found (version):**
```json
{
  "detail": "Prompt version not found"
}
```

---

### POST /prompts/{prompt_id}/versions/{version_id}/restore

Restore prompt fields from a specific version snapshot.

**Request:**
```bash
curl -X POST http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/a7f44b5f-4d58-4a8d-9f41-5a2a4da6f0cd/restore
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt to restore
- `version_id` (string, required): UUID of the version to restore from

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Customer Service Response",
  "content": "You are a helpful customer service agent...",
  "description": "Template for responding to customer inquiries",
  "collection_id": null,
  "created_at": "2024-02-16T10:30:00",
  "updated_at": "2024-02-16T11:30:00"
}
```

**Error Responses:**

**404 Not Found (prompt):**
```json
{
  "detail": "Prompt not found"
}
```

**404 Not Found (version):**
```json
{
  "detail": "Prompt version not found"
}
```

---

### DELETE /prompts/{prompt_id}

Delete a prompt permanently.

**Request:**
```bash
curl -X DELETE http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

**Path Parameters:**
- `prompt_id` (string, required): UUID of the prompt to delete

**Response (204 No Content):**
```
(empty body)
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

---

## Collection Endpoints

### GET /collections

List all collections.

**Request:**
```bash
curl -X GET http://localhost:8000/collections
```

**Response (200 OK):**
```json
{
  "collections": [
    {
      "id": "col-123",
      "name": "Customer Service",
      "description": "Prompts for customer service interactions",
      "created_at": "2024-02-15T14:00:00"
    },
    {
      "id": "col-456",
      "name": "Email Templates",
      "description": "Email draft templates",
      "created_at": "2024-02-16T08:30:00"
    }
  ],
  "total": 2
}
```

**Response Fields:**
- `collections` (array): List of collection objects
  - `id` (string): Unique collection identifier (UUID)
  - `name` (string): Collection name (1-100 characters)
  - `description` (string, nullable): Optional description (max 500 characters)
  - `created_at` (string): Creation timestamp (ISO 8601)
- `total` (integer): Total number of collections

**Error Responses:**
- None. Returns empty list if no collections exist.

---

### GET /collections/{collection_id}

Retrieve a specific collection by ID.

**Request:**
```bash
curl -X GET http://localhost:8000/collections/col-123
```

**Path Parameters:**
- `collection_id` (string, required): UUID of the collection to retrieve

**Response (200 OK):**
```json
{
  "id": "col-123",
  "name": "Customer Service",
  "description": "Prompts for customer service interactions",
  "created_at": "2024-02-15T14:00:00"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Collection not found"
}
```

---

### POST /collections

Create a new collection.

**Request:**
```bash
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Service",
    "description": "Prompts for customer service interactions"
  }'
```

**Request Body:**
```json
{
  "name": "Customer Service",
  "description": "Prompts for customer service interactions"
}
```

**Request Fields:**
- `name` (string, required): Collection name (1-100 characters)
- `description` (string, optional): Description (max 500 characters)

**Response (201 Created):**
```json
{
  "id": "col-123",
  "name": "Customer Service",
  "description": "Prompts for customer service interactions",
  "created_at": "2024-02-15T14:00:00"
}
```

**Response Fields:**
- `id` (string): Auto-generated UUID
- `name` (string): Collection name
- `description` (string, nullable): Description (if provided)
- `created_at` (string): Current timestamp

**Error Responses:**

**422 Unprocessable Entity** (validation error):
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

### DELETE /collections/{collection_id}

Delete a collection and all associated prompts.

**Request:**
```bash
curl -X DELETE http://localhost:8000/collections/col-123
```

**Path Parameters:**
- `collection_id` (string, required): UUID of the collection to delete

**Response (204 No Content):**
```
(empty body)
```

**Important Note:**
This operation is **cascading**. All prompts in the collection are permanently deleted. This cannot be undone.

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Collection not found"
}
```

---

## Error Response Reference

### All Possible Error Formats

#### 1. Simple Error Message

```json
{
  "detail": "String describing the error"
}
```

**Occurs with:**
- 404 Not Found
- 400 Bad Request

#### 2. Validation Error Array

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    },
    {
      "loc": ["body", "content"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Occurs with:**
- 422 Unprocessable Entity (validation failures)

**Fields:**
- `loc` (array): Location of the error (section, field name)
- `msg` (string): Human-readable error message
- `type` (string): Machine-readable error type

#### 3. Validation Constraint Error

```json
{
  "detail": "Collection not found"
}
```

**Occurs with:**
- 400 Bad Request (when a referenced resource doesn't exist)

---

## Status Codes

### Success Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| **200** | OK | GET successful, data returned |
| **201** | Created | POST successful, resource created |
| **204** | No Content | DELETE successful, no content to return |

### Error Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| **400** | Bad Request | Validation failed, invalid parameters, or referenced resource not found |
| **404** | Not Found | Resource with given ID doesn't exist |
| **422** | Unprocessable Entity | Request data format is invalid or violates constraints |
| **500** | Internal Server Error | Unexpected server-side error |

---

## Best Practices

### Request Headers

Always include the correct content type:
```
Content-Type: application/json
Accept: application/json
```

### Error Handling

1. Check HTTP status code first
2. Parse the `detail` field for error message
3. For validation errors (422), iterate through error array
4. Implement exponential backoff for retries on 500 errors

### Rate Limiting

Currently not implemented. Production deployments should consider:
- Rate limiting per IP
- Rate limiting per API key (if authentication added)
- Graceful degradation with 429 Too Many Requests

### Pagination

Currently not implemented. For future versions, consider:
- `?page=1&page_size=20` query parameters
- `X-Total-Count` response header
- `Link` header with pagination URLs

---

## OpenAPI/Swagger

Full interactive API documentation is available at:

```
http://localhost:8000/docs
```

Alternative documentation format at:
```
http://localhost:8000/redoc
```

Raw OpenAPI schema:
```
http://localhost:8000/openapi.json
```

---

**Last Updated**: February 2024  
**Version**: 1.0.0  
**Status**: Complete and Stable
