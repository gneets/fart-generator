# Fart Generator - Backend

FastAPI backend for the Fart Generator application.

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Start infrastructure (from project root)

```bash
cd ..
docker-compose up -d
```

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Start development server

```bash
python -m app.main
```

Or with uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Development

### Run tests

```bash
pytest
```

### Code formatting

```bash
black app/
ruff check app/
```

### Type checking

```bash
mypy app/
```

## Project Structure

```
backend/
├── app/
│   ├── api/            # API routes and endpoints
│   │   ├── routes/     # Route handlers
│   │   └── deps.py     # Dependencies
│   ├── core/           # Core configuration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   └── main.py         # FastAPI app entry point
├── alembic/            # Database migrations
├── tests/              # Test files
└── requirements.txt    # Python dependencies
```
