"""
API endpoints package.
"""

from .karaoke import router as karaoke_router
from .health import router as health_router

__all__ = ["karaoke_router", "health_router"]
