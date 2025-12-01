"""
FastAPI application entry point.
Main application setup and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=True  # Enable auto-reload for development
    )

