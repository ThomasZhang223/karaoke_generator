"""
Pydantic schemas for API request/response models.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, HttpUrl


class JobStatus(str, Enum):
    """Status of a karaoke generation job."""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING_AUDIO = "processing_audio"
    FETCHING_LYRICS = "fetching_lyrics"
    SYNCHRONIZING = "synchronizing"
    RENDERING_VIDEO = "rendering_video"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerateKaraokeRequest(BaseModel):
    """Request model for generating a karaoke video."""
    youtube_url: HttpUrl
    audio_format: str = "mp3"
    audio_bitrate: int = 192


class GenerateKaraokeResponse(BaseModel):
    """Response model for karaoke generation request."""
    job_id: str
    status: JobStatus
    message: str
    video_url: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    version: str

