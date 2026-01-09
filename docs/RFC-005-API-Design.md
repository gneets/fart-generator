# RFC-005: API Design

**Status:** Draft
**Created:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal

---

## 1. Overview

This RFC defines the REST and WebSocket API endpoints for the Fart Generator backend.

## 2. Base URL & Versioning

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.fartgenerator.com/api/v1`
- **Version**: `/api/v1` for current version

## 3. Authentication

All authenticated endpoints require JWT token in header:
```
Authorization: Bearer <access_token>
```

## 4. REST API Endpoints

### 4.1 Authentication Endpoints

#### POST /auth/register
Register new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "username": "fartlover99",
  "password": "SecurePassword123!"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "fartlover99",
  "created_at": "2026-01-09T12:00:00Z"
}
```

#### POST /auth/login
Login and receive JWT tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

#### POST /auth/password-reset
Request password reset email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "message": "Password reset email sent if account exists"
}
```

### 4.2 User Profile Endpoints

#### GET /users/me
Get current user's profile.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "fartlover99",
  "is_verified": true,
  "created_at": "2026-01-01T12:00:00Z",
  "last_login_at": "2026-01-09T12:00:00Z"
}
```

#### PATCH /users/me
Update current user's profile.

**Request:**
```json
{
  "username": "newfartlover"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "newfartlover",
  ...
}
```

### 4.3 Generation Endpoints

#### GET /generations
Get user's generation history.

**Query Parameters:**
- `limit` (int, default=50): Number of results
- `offset` (int, default=0): Pagination offset
- `search` (str, optional): Search prompt text
- `favorite` (bool, optional): Filter favorites only

**Response (200):**
```json
{
  "items": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "prompt": "long rumbling fart",
      "duration": 4.5,
      "wetness": 3,
      "pitch": 2,
      "type": "rumbler",
      "audio_url": "https://cdn.fartgen.com/audio/660e8400.wav",
      "is_favorite": false,
      "play_count": 5,
      "created_at": "2026-01-09T11:00:00Z"
    }
  ],
  "total": 142,
  "limit": 50,
  "offset": 0
}
```

#### GET /generations/{generation_id}
Get specific generation details.

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "prompt": "long rumbling fart",
  "duration": 4.5,
  "wetness": 3,
  "pitch": 2,
  "type": "rumbler",
  "confidence": 0.95,
  "audio_url": "https://cdn.fartgen.com/audio/660e8400.wav",
  "audio_format": "wav",
  "file_size_bytes": 397312,
  "is_favorite": false,
  "play_count": 5,
  "created_at": "2026-01-09T11:00:00Z"
}
```

#### DELETE /generations/{generation_id}
Delete a generation.

**Response (204):** No content

#### POST /generations/{generation_id}/favorite
Toggle favorite status.

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "is_favorite": true
}
```

### 4.4 Sharing Endpoints

#### POST /generations/{generation_id}/share
Create shareable link.

**Request:**
```json
{
  "is_public": true,
  "expires_in_days": null
}
```

**Response (201):**
```json
{
  "share_token": "a7b3c9d2",
  "share_url": "https://fartgenerator.com/s/a7b3c9d2",
  "is_public": true,
  "expires_at": null
}
```

#### GET /shared/{share_token}
Get shared sound details (public endpoint).

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "prompt": "long rumbling fart",
  "audio_url": "https://cdn.fartgen.com/audio/660e8400.wav",
  "duration": 4.5,
  "type": "rumbler",
  "created_at": "2026-01-09T11:00:00Z",
  "view_count": 42
}
```

#### GET /shared
Get public shared sounds (discovery feed).

**Query Parameters:**
- `limit` (int, default=50)
- `offset` (int, default=0)
- `sort` (str, default="recent"): "recent", "popular"

**Response (200):**
```json
{
  "items": [...],
  "total": 523,
  "limit": 50,
  "offset": 0
}
```

### 4.5 Collections Endpoints

#### GET /collections
Get user's collections.

**Response (200):**
```json
{
  "items": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "name": "My Favorites",
      "description": "Best farts ever",
      "is_public": false,
      "sound_count": 15,
      "created_at": "2026-01-01T12:00:00Z"
    }
  ],
  "total": 5
}
```

#### POST /collections
Create new collection.

**Request:**
```json
{
  "name": "Epic Farts",
  "description": "My collection of epic sounds",
  "is_public": false
}
```

**Response (201):**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "name": "Epic Farts",
  "description": "My collection of epic sounds",
  "is_public": false,
  "sound_count": 0,
  "created_at": "2026-01-09T12:00:00Z"
}
```

#### POST /collections/{collection_id}/sounds
Add sound to collection.

**Request:**
```json
{
  "generation_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

**Response (201):**
```json
{
  "message": "Sound added to collection"
}
```

## 5. WebSocket API

### 5.1 Connection

**URL:** `wss://api.fartgenerator.com/ws/generate?token=<jwt_token>`

### 5.2 Message Protocol

#### Client → Server: Generation Request

```json
{
  "type": "generate",
  "payload": {
    "prompt": "long rumbling fart",
    "context": {
      "previous_generation": {
        "id": "660e8400-e29b-41d4-a716-446655440000",
        "prompt": "short squeaker",
        "duration": 1.2,
        "wetness": 2,
        "pitch": 8,
        "type": "squeaker"
      }
    }
  }
}
```

#### Server → Client: Status Updates

**Interpreting:**
```json
{
  "type": "status",
  "status": "interpreting",
  "message": "Interpreting your prompt..."
}
```

**Interpreted:**
```json
{
  "type": "interpreted",
  "interpretation": {
    "duration": 4.5,
    "wetness": 3,
    "pitch": 2,
    "type": "rumbler",
    "confidence": 0.95
  },
  "message": "Generating rumbler sound..."
}
```

**Generating:**
```json
{
  "type": "status",
  "status": "generating",
  "progress": 45,
  "message": "Generating audio..."
}
```

**Complete:**
```json
{
  "type": "complete",
  "generation": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "prompt": "long rumbling fart",
    "audio_url": "https://cdn.fartgen.com/audio/660e8400.wav",
    "duration": 4.5,
    "wetness": 3,
    "pitch": 2,
    "type": "rumbler",
    "created_at": "2026-01-09T12:00:00Z"
  }
}
```

**Error:**
```json
{
  "type": "error",
  "error": "generation_failed",
  "message": "Failed to generate audio. Please try again."
}
```

## 6. Error Responses

### 6.1 Standard Error Format

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "constraint": "format"
    }
  }
}
```

### 6.2 HTTP Status Codes

- `200 OK`: Successful GET/PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing/invalid auth token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## 7. Rate Limiting

**Per User:**
- Generations: 50 per hour
- API requests: 1000 per hour

**Per IP (unauthenticated):**
- API requests: 100 per hour

**Headers:**
```
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1673280000
```

## 8. CORS Policy

**Allowed Origins:**
- `https://fartgenerator.com`
- `http://localhost:5173` (development)

**Allowed Methods:** GET, POST, PATCH, DELETE, OPTIONS

**Allowed Headers:** Authorization, Content-Type

---

**Next Steps:**
1. Implement FastAPI routes
2. Add request/response validation with Pydantic
3. Set up rate limiting middleware
4. Test all endpoints
5. Generate OpenAPI documentation
