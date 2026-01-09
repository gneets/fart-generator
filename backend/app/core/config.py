"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Fart Generator"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Anthropic Claude API
    ANTHROPIC_API_KEY: str

    # AWS S3 / MinIO
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_S3_REGION: str = "us-east-1"
    AWS_S3_ENDPOINT_URL: str | None = None
    AWS_S3_USE_SSL: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    GENERATION_LIMIT_PER_HOUR: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
