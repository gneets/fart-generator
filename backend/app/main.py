"""
Fart Generator - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Fart Sound Generator API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)

    if settings.APP_ENV == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    return response


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "operational",
        "docs": "/api/docs",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
    }


# API version prefix
@app.get("/api/v1")
async def api_info():
    """API v1 info"""
    return {
        "version": "v1",
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "generations": "/api/v1/generations",
            "shared": "/api/v1/shared",
            "collections": "/api/v1/collections",
            "websocket": "ws://localhost:8000/ws/generate",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
