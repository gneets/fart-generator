# RFC-001: System Architecture

**Status:** Draft
**Created:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal
**Related PRD:** [PRD.md](./PRD.md)

---

## 1. Overview

This RFC defines the overall system architecture for the Fart Generator web application, including component breakdown, technology choices, deployment strategy, and inter-component communication patterns.

## 2. Goals

- Define a scalable, maintainable architecture for the full-stack application
- Establish clear boundaries between frontend, backend, and infrastructure components
- Enable real-time audio generation and streaming
- Support horizontal scaling for production traffic
- Minimize latency for optimal user experience

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              React Frontend (TypeScript)                    │ │
│  │  - UI Components (Tailwind CSS)                            │ │
│  │  - State Management (Context/Zustand)                      │ │
│  │  - Web Audio API (Playback & Visualization)                │ │
│  │  - WebSocket Client                                        │ │
│  │  - REST API Client (fetch/axios)                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS (REST + WebSocket)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Load Balancer / CDN                         │
│                    (CloudFront + ALB)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Python)                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  REST API        │  │  WebSocket       │  │  Background  │  │
│  │  Endpoints       │  │  Handler         │  │  Tasks       │  │
│  │  (Auth, CRUD)    │  │  (Real-time gen) │  │  (Celery)    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  Auth Middleware │  │  Rate Limiter    │  │  Logging     │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
           │                    │                    │
           │                    │                    │
           ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   PostgreSQL     │  │      Redis       │  │   AWS S3         │
│   (User Data,    │  │   (Cache, Rate   │  │  (Audio Files)   │
│    History)      │  │    Limiting)     │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘

           │
           │ API Calls
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                External Services                                 │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │  Anthropic       │  │  SendGrid/SES    │                     │
│  │  Claude API      │  │  (Email)         │                     │
│  └──────────────────┘  └──────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              Audio Generation Pipeline                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Prompt → Claude API → Parameters → Audio Engine → Stream    ││
│  │                                                               ││
│  │  Audio Engine Components:                                    ││
│  │  - Sample Library (10-20 base sounds)                        ││
│  │  - Synthesis Module (NumPy/SciPy)                            ││
│  │  - Effects Processor (filters, pitch shift)                  ││
│  │  - Mixer & Normalizer                                        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 4. Component Breakdown

### 4.1 Frontend (React + TypeScript)

**Technology Stack:**
- React 18+ with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Zustand or Context API for state management
- React Router for navigation
- Web Audio API for audio playback and visualization

**Key Responsibilities:**
- Render UI components and handle user interactions
- Manage client-side state (auth tokens, user data, generation history)
- Establish and maintain WebSocket connection for real-time generation
- Play audio using Web Audio API
- Handle file downloads
- Implement responsive design for mobile/desktop

**Directory Structure:**
```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Generator/       # Main generation interface
│   │   ├── History/         # User history view
│   │   ├── Player/          # Audio player component
│   │   └── Auth/            # Login/signup forms
│   ├── pages/               # Route-level page components
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API clients (REST + WebSocket)
│   ├── stores/              # State management
│   ├── types/               # TypeScript type definitions
│   └── utils/               # Helper functions
├── public/                  # Static assets
└── package.json
```

### 4.2 Backend (FastAPI + Python)

**Technology Stack:**
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0 (async) for ORM
- Alembic for database migrations
- Pydantic for data validation
- python-jose for JWT
- passlib for password hashing
- anthropic SDK for Claude API
- numpy, scipy, pydub for audio processing
- celery + redis for background tasks (optional)

**Key Responsibilities:**
- Handle REST API requests (CRUD operations)
- Manage WebSocket connections for real-time generation
- Authenticate and authorize users (JWT)
- Interpret prompts using Claude API
- Generate audio using synthesis engine
- Store metadata in PostgreSQL
- Upload audio files to S3
- Implement rate limiting
- Log requests and errors

**Directory Structure:**
```
backend/
├── app/
│   ├── api/
│   │   ├── routes/          # API route handlers
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── generation.py # Generation endpoints
│   │   │   ├── history.py   # History endpoints
│   │   │   └── websocket.py # WebSocket handler
│   │   └── deps.py          # Dependency injection
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── security.py      # Auth utilities
│   │   └── database.py      # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/
│   │   ├── audio_engine.py  # Audio generation
│   │   ├── claude_service.py # LLM integration
│   │   └── storage.py       # S3 integration
│   └── main.py              # FastAPI app entry point
├── alembic/                 # Database migrations
├── tests/                   # Unit and integration tests
└── requirements.txt
```

### 4.3 Database (PostgreSQL)

**Purpose:**
- Store user accounts and authentication data
- Store generation history and metadata
- Store favorites and collections
- Store shared sound metadata

**Why PostgreSQL:**
- ACID compliance for user data integrity
- Rich querying capabilities for search/filter
- JSON support for flexible metadata storage
- Mature ecosystem and tooling
- Strong SQLAlchemy support

### 4.4 Cache Layer (Redis)

**Purpose:**
- Cache Claude API responses for common prompts
- Store rate limiting counters
- Session management (optional)
- Task queue for Celery (optional)

**Why Redis:**
- Fast in-memory operations
- Built-in data structures (strings, sets, sorted sets)
- TTL support for automatic expiration
- Pub/sub for real-time features

### 4.5 Object Storage (AWS S3)

**Purpose:**
- Store generated audio files (.wav, .mp3)
- Serve files via CloudFront CDN
- Lifecycle policies for automatic cleanup

**Why S3:**
- Highly durable and available
- Cost-effective for large file storage
- Seamless CloudFront integration
- Supports presigned URLs for secure access

### 4.6 External Services

**Claude API (Anthropic):**
- Interpret natural language prompts
- Extract audio generation parameters
- Handle conversational follow-ups ("make it wetter")

**SendGrid/SES:**
- Password reset emails
- Account verification emails
- Notification emails (optional)

## 5. Communication Patterns

### 5.1 REST API (HTTP/HTTPS)

**Used for:**
- User authentication (login, register, password reset)
- CRUD operations (history, favorites, collections)
- Metadata queries (fetch history, search sounds)
- File downloads (presigned S3 URLs)

**Protocol:** HTTP/1.1 or HTTP/2 over TLS
**Format:** JSON request/response bodies
**Authentication:** JWT Bearer tokens in Authorization header

### 5.2 WebSocket

**Used for:**
- Real-time audio generation streaming
- Progress updates during generation
- Bidirectional communication for interactive generation

**Flow:**
1. Client establishes WebSocket connection (with JWT token)
2. Client sends generation request: `{prompt: "long rumbler", parameters: {...}}`
3. Server interprets prompt via Claude API
4. Server generates audio in chunks
5. Server streams progress updates: `{status: "generating", progress: 45%}`
6. Server streams final audio data: `{status: "complete", audio_url: "..."}`
7. Client plays audio or downloads file

**Protocol:** WebSocket over TLS (wss://)
**Format:** JSON messages

### 5.3 Database Access

**Pattern:** Repository pattern with async SQLAlchemy
- All database access through repository classes
- Connection pooling for efficiency
- Read replicas for scaling (future)

### 5.4 File Storage Access

**Pattern:** Service layer abstraction
- Backend generates presigned S3 URLs
- Frontend downloads directly from S3 (bypass backend)
- CloudFront CDN for global delivery

## 6. Deployment Architecture

### 6.1 Development Environment

```
Local Machine:
- Frontend: npm run dev (Vite dev server on :5173)
- Backend: uvicorn app.main:app --reload (on :8000)
- PostgreSQL: Docker container (on :5432)
- Redis: Docker container (on :6379)
- MinIO: Docker container (S3-compatible, on :9000)
```

**Setup:**
- Use Docker Compose for local infrastructure
- Environment variables in `.env` files
- Hot reload for both frontend and backend

### 6.2 Production Environment (AWS)

```
AWS Architecture:
┌─────────────────────────────────────────────────────────────┐
│                      CloudFront CDN                          │
│  - Frontend static files (S3 bucket)                        │
│  - Audio file delivery (S3 bucket)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Load Balancer (ALB)                 │
│  - SSL/TLS termination                                      │
│  - WebSocket upgrade support                                │
│  - Health checks                                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            ECS/EC2 Auto Scaling Group                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Backend   │  │   Backend   │  │   Backend   │         │
│  │  Container  │  │  Container  │  │  Container  │         │
│  │  (FastAPI)  │  │  (FastAPI)  │  │  (FastAPI)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
           │                    │
           ▼                    ▼
┌──────────────────┐  ┌──────────────────┐
│   RDS PostgreSQL │  │  ElastiCache     │
│   (Multi-AZ)     │  │  Redis           │
└──────────────────┘  └──────────────────┘
```

**Components:**
- **Frontend**: S3 + CloudFront for static hosting
- **Backend**: ECS Fargate or EC2 with auto-scaling (2-10 instances)
- **Database**: RDS PostgreSQL (Multi-AZ for HA)
- **Cache**: ElastiCache Redis (cluster mode)
- **Storage**: S3 with lifecycle policies
- **Monitoring**: CloudWatch + Sentry
- **CI/CD**: GitHub Actions → ECR → ECS

### 6.3 Scaling Strategy

**Horizontal Scaling:**
- Backend: Auto-scale based on CPU/memory (2-10 instances)
- Database: Read replicas for read-heavy operations
- Redis: Cluster mode for high throughput

**Vertical Scaling:**
- Database: Upgrade instance type as needed
- Backend: Increase container memory for audio processing

**Cost Optimization:**
- CloudFront caching for audio files (reduce bandwidth)
- S3 lifecycle policies (delete old generations after 30 days)
- Reserved instances for base load (if cost-effective)
- Cache Claude API responses to reduce API costs

## 7. Security Considerations

### 7.1 Authentication & Authorization
- JWT tokens with short expiry (15 min access, 7 day refresh)
- Password hashing with bcrypt/argon2
- Rate limiting on authentication endpoints

### 7.2 API Security
- CORS policy restricting origins
- CSRF protection for state-changing operations
- Input validation with Pydantic schemas
- SQL injection prevention via ORM

### 7.3 Data Protection
- TLS/SSL for all communication (HTTPS/WSS)
- Database encryption at rest (RDS)
- S3 bucket encryption
- Secure environment variable management (AWS Secrets Manager)

### 7.4 Rate Limiting
- Per-user limits: 50 generations/hour
- Per-IP limits: 100 requests/minute
- Progressive backoff for repeat offenders

## 8. Observability

### 8.1 Logging
- Structured JSON logs (timestamp, level, message, context)
- Log aggregation: CloudWatch Logs or ELK stack
- Retention: 30 days for debugging

### 8.2 Monitoring
- Application metrics: Request rate, latency, error rate
- System metrics: CPU, memory, disk, network
- Custom metrics: Generation time, Claude API calls, cache hit rate
- Dashboards: Grafana or CloudWatch

### 8.3 Error Tracking
- Sentry for exception tracking
- Alerts for critical errors (Slack/email)
- User context for debugging

### 8.4 Performance Monitoring
- APM: Track slow endpoints and bottlenecks
- Real User Monitoring (RUM) for frontend performance
- Distributed tracing for request flows

## 9. Development Workflow

### 9.1 Version Control
- Git with feature branch workflow
- Branch naming: `feature/`, `bugfix/`, `hotfix/`
- Pull requests required for main branch
- Code review by at least one team member

### 9.2 CI/CD Pipeline

**On Pull Request:**
1. Run linters (ESLint, Pylint)
2. Run type checks (TypeScript, mypy)
3. Run unit tests
4. Run integration tests
5. Build Docker images
6. Security scanning

**On Merge to Main:**
1. Build production images
2. Push to ECR
3. Deploy to staging environment
4. Run smoke tests
5. Manual approval
6. Deploy to production
7. Monitor for errors

### 9.3 Testing Strategy
- **Unit Tests**: Backend business logic, frontend components
- **Integration Tests**: API endpoints, database operations
- **E2E Tests**: Critical user flows (Playwright/Cypress)
- **Load Tests**: Performance under expected traffic (Locust/k6)

## 10. Open Questions

1. **ECS vs EC2**: Should we use ECS Fargate (simpler) or EC2 with ECS (more control)?
2. **Celery**: Do we need Celery for background tasks, or can we handle everything in request handlers?
3. **Multi-region**: Should we deploy to multiple AWS regions for global latency?
4. **WebSocket sticky sessions**: How do we handle WebSocket connections with multiple backend instances?
5. **Database connection pooling**: What pool size for async SQLAlchemy?
6. **Audio format**: Should we generate WAV and convert to MP3, or generate MP3 directly?

## 11. Alternatives Considered

### 11.1 Backend Framework
- **Django**: More batteries-included, but slower and synchronous
- **Flask**: Lighter than Django, but lacks async and modern features
- **Node.js/Express**: JS everywhere, but Python better for audio processing
- **Decision**: FastAPI for async support, performance, and Python ecosystem

### 11.2 Database
- **MySQL**: Similar to PostgreSQL, but weaker JSON support
- **MongoDB**: Flexible schema, but loses ACID guarantees
- **Decision**: PostgreSQL for reliability and rich querying

### 11.3 Hosting
- **Heroku**: Easy but expensive at scale
- **Google Cloud**: Good but team less familiar
- **Self-hosted**: Maximum control but high operational burden
- **Decision**: AWS for ecosystem maturity and flexibility

## 12. References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Best Practices](https://react.dev/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [12-Factor App Methodology](https://12factor.net/)

---

**Next Steps:**
1. Review and approve this architecture
2. Set up development environment
3. Implement MVP components (Phase 1)
4. Create detailed RFCs for audio engine, database schema, API design
