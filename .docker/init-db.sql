-- Initialize PostgreSQL database for Fart Generator

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable full-text search extension
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database user (already created by POSTGRES_USER env var, but good to have for reference)
-- CREATE USER fartgen WITH PASSWORD 'dev_password_change_in_prod';
-- GRANT ALL PRIVILEGES ON DATABASE fartgen_dev TO fartgen;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Fart Generator database initialized successfully!';
END $$;
