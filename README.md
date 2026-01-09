# Fart Generator 💨

An AI-powered web application that generates realistic, customizable flatulence sound effects based on natural language prompts.

## Overview

The Fart Generator uses Claude AI to interpret your descriptions ("a long, rumbling fart") and synthesizes authentic audio in real-time. It features a full studio experience with user accounts, generation history, favorites, and sound sharing capabilities.

## Project Status

🚀 **Development Environment Setup Complete**

- ✅ Product Requirements Document (PRD) completed
- ✅ 6 comprehensive Technical RFCs completed
- ✅ Development environment configured
- ⏳ Ready for Phase 1 (MVP) implementation

## Contributors

- Gurneet Sandhu
- Guriqbal Mahal

## Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Zustand (state management)
- Web Audio API

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL + SQLAlchemy
- Redis
- Anthropic Claude API
- NumPy/SciPy (audio processing)

**Infrastructure:**
- Docker Compose (local dev)
- AWS S3 (file storage)
- MinIO (local S3-compatible storage)

## Project Structure

```
fart-generator/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API clients
│   │   └── stores/      # State management
│   └── package.json
├── docs/                # Documentation
│   ├── PRD.md          # Product Requirements
│   └── RFC-*.md        # Technical RFCs
├── assets/             # Audio samples
├── docker-compose.yml  # Local infrastructure
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop (for local infrastructure)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gneets/fart-generator.git
   cd fart-generator
   ```

2. **Start local infrastructure**
   ```bash
   docker-compose up -d
   ```
   This starts PostgreSQL, Redis, and MinIO (S3-compatible storage).

3. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Anthropic API key
   ```

4. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

5. **Run backend** (in backend directory)
   ```bash
   python -m app.main
   ```
   Backend runs at http://localhost:8000
   API docs at http://localhost:8000/api/docs

6. **Run frontend** (in frontend directory, separate terminal)
   ```bash
   npm run dev
   ```
   Frontend runs at http://localhost:5173

### Quick Test

Visit http://localhost:5173 to see the frontend.
Visit http://localhost:8000/health to check backend status.
Visit http://localhost:9001 for MinIO console (minioadmin/minioadmin).

## Development

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for detailed development instructions.

## Documentation

- [PRD (Product Requirements Document)](docs/PRD.md)
- [RFC-001: System Architecture](docs/RFC-001-System-Architecture.md)
- [RFC-002: Audio Generation Engine](docs/RFC-002-Audio-Generation-Engine.md)
- [RFC-003: AI/LLM Integration](docs/RFC-003-AI-LLM-Integration.md)
- [RFC-004: Database Schema](docs/RFC-004-Database-Schema.md)
- [RFC-005: API Design](docs/RFC-005-API-Design.md)
- [RFC-006: Authentication & Security](docs/RFC-006-Authentication-Security.md)

## Roadmap

### Phase 1: Foundation & Core Generation (v0.1 - MVP)
- [x] Project setup and documentation
- [x] Development environment configuration
- [ ] Audio generation engine implementation
- [ ] Claude API integration
- [ ] Basic WebSocket generation flow
- [ ] Simple frontend UI

### Phase 2: User Accounts & History (v0.5)
- [ ] User authentication system
- [ ] Database integration
- [ ] Generation history storage
- [ ] User profiles

### Phase 3: Full Studio Experience (v1.0 - Launch)
- [ ] Favorites and collections
- [ ] Sound sharing system
- [ ] Discovery feed
- [ ] Production deployment

## Contributing

This is a personal project by Gurneet Sandhu and Guriqbal Mahal. Contributions are welcome once we reach v1.0!

## License

TBD
