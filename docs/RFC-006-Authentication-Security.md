# RFC-006: Authentication & Security

**Status:** Draft
**Created:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal

---

## 1. Overview

This RFC defines authentication mechanisms, authorization policies, and security best practices for the Fart Generator application.

## 2. Authentication Strategy

### 2.1 JWT-Based Authentication

**Why JWT:**
- Stateless (no server-side session storage)
- Scalable across multiple backend instances
- Self-contained (includes user claims)
- Industry standard

**Token Types:**
1. **Access Token**: Short-lived (15 minutes), used for API requests
2. **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

### 2.2 Token Structure

**Access Token Payload:**
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",  // user_id
  "email": "user@example.com",
  "username": "fartlover99",
  "type": "access",
  "exp": 1673280900,  // 15 minutes from issue
  "iat": 1673280000
}
```

**Refresh Token Payload:**
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "type": "refresh",
  "exp": 1673884800,  // 7 days from issue
  "iat": 1673280000,
  "jti": "unique-token-id"  // For token revocation
}
```

### 2.3 Implementation

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration
SECRET_KEY = "your-secret-key-here"  # From env vars
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: str, email: str, username: str) -> str:
    """Create JWT access token"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_id,
        "email": email,
        "username": username,
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create JWT refresh token"""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())  # Unique token ID
    to_encode = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": jti
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise InvalidTokenError("Invalid or expired token")


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)
```

### 2.4 Authentication Flow

```
┌──────────┐                           ┌──────────┐
│  Client  │                           │  Server  │
└────┬─────┘                           └────┬─────┘
     │                                      │
     │  POST /auth/login                    │
     │  {email, password}                   │
     ├─────────────────────────────────────>│
     │                                      │
     │                        Verify credentials
     │                        Generate tokens
     │                                      │
     │  {access_token, refresh_token}       │
     │<─────────────────────────────────────┤
     │                                      │
     │  GET /generations                    │
     │  Authorization: Bearer <access_token>│
     ├─────────────────────────────────────>│
     │                                      │
     │                        Verify token
     │                        Return data
     │                                      │
     │  {generations: [...]}                │
     │<─────────────────────────────────────┤
     │                                      │
     │  (15 minutes later - token expired)  │
     │                                      │
     │  POST /auth/refresh                  │
     │  {refresh_token}                     │
     ├─────────────────────────────────────>│
     │                                      │
     │                        Verify refresh token
     │                        Generate new access token
     │                                      │
     │  {access_token}                      │
     │<─────────────────────────────────────┤
```

## 3. Password Security

### 3.1 Password Requirements

- Minimum length: 8 characters
- Must contain: uppercase, lowercase, number
- Optional: special character
- Check against common password list (top 10K)

### 3.2 Password Hashing

**Algorithm:** bcrypt with cost factor 12

**Why bcrypt:**
- Adaptive (can increase cost as hardware improves)
- Built-in salt
- Industry standard
- Resistant to rainbow table attacks

```python
# Example usage
hashed = hash_password("MySecurePassword123!")
# $2b$12$KIXxPj3...  (60 chars)

is_valid = verify_password("MySecurePassword123!", hashed)
# True
```

### 3.3 Password Reset Flow

1. User requests reset via email
2. Server generates secure reset token (random 32 bytes, hex encoded)
3. Store token hash in Redis with 1-hour TTL
4. Send reset link: `https://fartgen.com/reset?token=<token>`
5. User clicks link, enters new password
6. Server verifies token, updates password
7. Invalidate all existing refresh tokens for user

## 4. Authorization

### 4.1 FastAPI Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Dependency to get authenticated user"""
    token = credentials.credentials

    try:
        payload = verify_token(token)

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # Fetch user from database
        user = await user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Usage in route
@router.get("/generations")
async def get_generations(
    current_user: User = Depends(get_current_user)
):
    """Get user's generations (authenticated)"""
    return await generation_service.get_user_generations(current_user.id)
```

### 4.2 Resource Authorization

**Rule:** Users can only access their own resources (generations, collections)

```python
async def verify_generation_ownership(
    generation_id: str,
    current_user: User = Depends(get_current_user)
) -> Generation:
    """Verify user owns the generation"""
    generation = await generation_repository.get_by_id(generation_id)

    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation not found"
        )

    if generation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this generation"
        )

    return generation
```

## 5. Security Best Practices

### 5.1 Input Validation

**Use Pydantic for all request bodies:**
```python
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8)

    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
```

### 5.2 SQL Injection Prevention

- **Always use SQLAlchemy ORM** (parameterized queries)
- Never construct raw SQL with string interpolation
- Use ORM filters and query builders

### 5.3 XSS Prevention

- Frontend: Sanitize user input before rendering
- React automatically escapes content in JSX
- Be careful with `dangerouslySetInnerHTML`
- Sanitize prompts before displaying

### 5.4 CSRF Protection

- Not needed for JWT-based API (no cookies)
- If using cookies: CSRF tokens required for state-changing operations

### 5.5 CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fartgenerator.com",
        "http://localhost:5173"  # Dev only
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)
```

### 5.6 Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute per IP
async def login(request: Request, credentials: LoginRequest):
    ...
```

### 5.7 Secrets Management

**Never commit secrets to repository!**

**Use environment variables:**
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    anthropic_api_key: str
    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**Production:** Use AWS Secrets Manager or similar

### 5.8 HTTPS Enforcement

- **All communication over HTTPS in production**
- HTTP Strict Transport Security (HSTS) header
- Redirect HTTP to HTTPS at load balancer level

```python
# HSTS header
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## 6. Logging & Monitoring

### 6.1 Security Events to Log

- Failed login attempts
- Password reset requests
- Token refresh attempts
- Authorization failures (403)
- Rate limit violations
- Unusual activity patterns

### 6.2 What NOT to Log

- Passwords (plain or hashed)
- JWT tokens
- API keys
- Sensitive user data

### 6.3 Log Format

```python
import logging
import json

logger = logging.getLogger(__name__)

def log_security_event(event_type: str, user_id: str = None, details: dict = None):
    logger.info(json.dumps({
        "event": "security",
        "type": event_type,
        "user_id": user_id,
        "details": details,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.client.host
    }))


# Usage
log_security_event("login_failed", user_id=user.id, details={"reason": "invalid_password"})
```

## 7. Compliance & Privacy

### 7.1 GDPR Considerations

- **Right to Access**: Provide user data export
- **Right to Deletion**: Delete all user data on request
- **Data Minimization**: Only collect necessary data
- **Consent**: Terms of service acceptance

### 7.2 Data Retention

- User data: Indefinite (until user requests deletion)
- Generated audio: 90 days
- Access logs: 30 days
- Error logs: 90 days

## 8. Security Checklist

**Pre-Launch:**
- [ ] All secrets in environment variables/secrets manager
- [ ] HTTPS enforced in production
- [ ] Password requirements implemented
- [ ] Rate limiting on all endpoints
- [ ] Input validation with Pydantic
- [ ] SQL injection prevention (ORM only)
- [ ] XSS prevention (React escaping)
- [ ] CORS properly configured
- [ ] Security headers added
- [ ] Error messages don't leak sensitive info
- [ ] Logging configured (without sensitive data)
- [ ] Token expiration tested
- [ ] Password reset flow tested
- [ ] Authorization checks on all protected endpoints

**Ongoing:**
- [ ] Regular security audits
- [ ] Dependency updates (npm audit, pip audit)
- [ ] Monitor for suspicious activity
- [ ] Review access logs
- [ ] Rotate secrets periodically

---

**Next Steps:**
1. Implement authentication system
2. Add rate limiting middleware
3. Configure CORS
4. Set up security logging
5. Security audit before launch
