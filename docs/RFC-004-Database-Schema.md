# RFC-004: Database Schema

**Status:** Draft
**Created:** 2026-01-09
**Authors:** Gurneet Sandhu, Guriqbal Mahal

---

## 1. Overview

This RFC defines the PostgreSQL database schema for storing users, generations, favorites, collections, and shared sounds.

## 2. Schema Design

### 2.1 ER Diagram

```
┌─────────────┐
│    users    │
└──────┬──────┘
       │
       │ 1:N
       ▼
┌──────────────────┐         ┌─────────────────┐
│   generations    │─────────│  shared_sounds  │
└─────────┬────────┘   1:1   └─────────────────┘
          │
          │ M:N
          ▼
┌──────────────────┐
│    favorites     │
└──────────────────┘
          │
          │ M:N
          ▼
┌──────────────────┐         ┌─────────────────┐
│   collections    │─────────│ collection_     │
└──────────────────┘   M:N   │   sounds        │
                              └─────────────────┘
```

### 2.2 Table Definitions

**users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

**generations**
```sql
CREATE TABLE generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- User input
    prompt TEXT NOT NULL,

    -- Audio parameters (from Claude API)
    duration DECIMAL(4,2) NOT NULL CHECK (duration >= 0.5 AND duration <= 10.0),
    wetness INT NOT NULL CHECK (wetness >= 0 AND wetness <= 10),
    pitch INT NOT NULL CHECK (pitch >= 0 AND pitch <= 10),
    type VARCHAR(20) NOT NULL CHECK (type IN ('squeaker', 'rumbler', 'stutterer', 'classic', 'wet')),
    confidence DECIMAL(3,2) CHECK (confidence >= 0.0 AND confidence <= 1.0),

    -- Audio file info
    audio_url TEXT NOT NULL,  -- S3 URL
    audio_format VARCHAR(10) DEFAULT 'wav',
    file_size_bytes INT,

    -- Metadata
    is_favorite BOOLEAN DEFAULT FALSE,
    play_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Additional parameters (JSON for flexibility)
    additional_params JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_generations_user_id ON generations(user_id);
CREATE INDEX idx_generations_created_at ON generations(created_at DESC);
CREATE INDEX idx_generations_is_favorite ON generations(is_favorite) WHERE is_favorite = TRUE;
CREATE INDEX idx_generations_prompt_search ON generations USING gin(to_tsvector('english', prompt));
```

**shared_sounds**
```sql
CREATE TABLE shared_sounds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    generation_id UUID UNIQUE NOT NULL REFERENCES generations(id) ON DELETE CASCADE,
    share_token VARCHAR(32) UNIQUE NOT NULL,  -- Short URL token
    is_public BOOLEAN DEFAULT TRUE,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE  -- NULL = never expires
);

CREATE INDEX idx_shared_sounds_share_token ON shared_sounds(share_token);
CREATE INDEX idx_shared_sounds_created_at ON shared_sounds(created_at DESC);
```

**collections**
```sql
CREATE TABLE collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_user_collection_name UNIQUE(user_id, name)
);

CREATE INDEX idx_collections_user_id ON collections(user_id);
```

**collection_sounds**
```sql
CREATE TABLE collection_sounds (
    collection_id UUID NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    generation_id UUID NOT NULL REFERENCES generations(id) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sort_order INT DEFAULT 0,

    PRIMARY KEY (collection_id, generation_id)
);

CREATE INDEX idx_collection_sounds_collection_id ON collection_sounds(collection_id);
```

## 3. SQLAlchemy Models

```python
from sqlalchemy import Column, String, Boolean, Integer, Float, Text, DateTime, ForeignKey, CheckConstraint, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    generations = relationship("Generation", back_populates="user", cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="user", cascade="all, delete-orphan")


class Generation(Base):
    __tablename__ = "generations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    prompt = Column(Text, nullable=False)

    duration = Column(DECIMAL(4, 2), nullable=False)
    wetness = Column(Integer, CheckConstraint('wetness >= 0 AND wetness <= 10'), nullable=False)
    pitch = Column(Integer, CheckConstraint('pitch >= 0 AND pitch <= 10'), nullable=False)
    type = Column(String(20), nullable=False)
    confidence = Column(DECIMAL(3, 2), nullable=True)

    audio_url = Column(Text, nullable=False)
    audio_format = Column(String(10), default='wav')
    file_size_bytes = Column(Integer, nullable=True)

    is_favorite = Column(Boolean, default=False, index=True)
    play_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    additional_params = Column(JSONB, default={})

    # Relationships
    user = relationship("User", back_populates="generations")
    shared_sound = relationship("SharedSound", back_populates="generation", uselist=False)
    collections = relationship("CollectionSound", back_populates="generation")


class SharedSound(Base):
    __tablename__ = "shared_sounds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"), unique=True, nullable=False)
    share_token = Column(String(32), unique=True, nullable=False, index=True)
    is_public = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    generation = relationship("Generation", back_populates="shared_sound")


class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="collections")
    sounds = relationship("CollectionSound", back_populates="collection", cascade="all, delete-orphan")


class CollectionSound(Base):
    __tablename__ = "collection_sounds"

    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.id"), primary_key=True)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"), primary_key=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    sort_order = Column(Integer, default=0)

    # Relationships
    collection = relationship("Collection", back_populates="sounds")
    generation = relationship("Generation", back_populates="collections")
```

## 4. Migrations (Alembic)

```python
# alembic/versions/001_initial_schema.py

def upgrade():
    # Create extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create users table
    op.create_table('users', ...)

    # Create generations table
    op.create_table('generations', ...)

    # ... (create all tables)

def downgrade():
    op.drop_table('collection_sounds')
    op.drop_table('collections')
    op.drop_table('shared_sounds')
    op.drop_table('generations')
    op.drop_table('users')
```

## 5. Query Patterns

### 5.1 Common Queries

**Get user's recent generations:**
```python
generations = session.query(Generation)
    .filter(Generation.user_id == user_id)
    .order_by(Generation.created_at.desc())
    .limit(50)
    .all()
```

**Search user's history:**
```python
generations = session.query(Generation)
    .filter(
        Generation.user_id == user_id,
        Generation.prompt.ilike(f"%{search_term}%")
    )
    .order_by(Generation.created_at.desc())
    .all()
```

**Get public shared sounds (discovery feed):**
```python
shared = session.query(SharedSound, Generation)
    .join(Generation)
    .filter(SharedSound.is_public == True)
    .order_by(SharedSound.created_at.desc())
    .limit(100)
    .all()
```

## 6. Data Retention & Cleanup

### 6.1 Lifecycle Policies

**Generated Audio Files:**
- Keep for 90 days by default
- Delete from S3 after expiration (S3 lifecycle policy)
- Soft delete: Mark as deleted in DB, actual deletion later

**User Data:**
- Keep indefinitely unless user requests deletion (GDPR)
- Implement user data export functionality
- Cascade delete on user deletion

## 7. Backup & Recovery

- **Daily backups**: RDS automated backups (7-day retention)
- **Weekly snapshots**: Manual snapshots (30-day retention)
- **Point-in-time recovery**: RDS PITR (last 7 days)

---

**Next Steps:**
1. Create initial Alembic migration
2. Implement SQLAlchemy models
3. Test CRUD operations
4. Set up backup procedures
