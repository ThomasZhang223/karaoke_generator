"""
Health check endpoints.
"""

from fastapi import APIRouter
from backend.models.schemas import HealthResponse
from backend.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the API.
    """
    return HealthResponse(
        status="healthy",
        version=settings.api_version
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    
    Verifies that the API is ready to accept requests.
    Can be extended to check dependencies (database, external services, etc.).
    """
    return {
        "status": "ready",
        "version": settings.api_version
    }

