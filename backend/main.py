"""
FastAPI application entry point.
Main application setup and configuration.
"""

import sys
from pathlib import Path

# Add project root to Python path to allow imports
# This allows running from either project root or backend directory
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import settings
from backend.api.endpoints import health_router, karaoke_router

# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    description="API for generating karaoke videos from YouTube URLs",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Request logging middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"[Middleware] {request.method} {request.url.path} - Request received")
        response = await call_next(request)
        print(f"[Middleware] {request.method} {request.url.path} - Response sent: {response.status_code}")
        return response

app.add_middleware(RequestLoggingMiddleware)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(karaoke_router, prefix="/api/v1")

# Story 3.6: Add frontend-compatible routes (without /v1 prefix)
# Frontend expects /api/generate-karaoke and /api/jobs/{jobId}
from backend.api.endpoints.karaoke import (
    generate_karaoke_for_frontend,
    get_job_status_for_frontend
)
from fastapi import APIRouter

# Create a compatibility router for frontend
frontend_router = APIRouter()
frontend_router.add_api_route("/generate-karaoke", generate_karaoke_for_frontend, methods=["POST"])
frontend_router.add_api_route("/jobs/{job_id}", get_job_status_for_frontend, methods=["GET"])

app.include_router(frontend_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Karaoke Video Generator API",
        "status": "running",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    # Use import string for reload to work properly
    uvicorn.run(
        "backend.main:app",  # Import string format
        host=settings.api_host,
        port=settings.api_port,
        reload=True  # Enable auto-reload for development
    )

