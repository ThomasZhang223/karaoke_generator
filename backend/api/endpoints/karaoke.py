"""
Karaoke generation endpoints.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.models.schemas import (
    GenerateKaraokeRequest,
    GenerateKaraokeResponse,
    JobStatus,
)
from backend.services.karaoke_service import KaraokeService

router = APIRouter(prefix="/karaoke", tags=["karaoke"])

# Initialize service
karaoke_service = KaraokeService()


@router.post("/generate", response_model=GenerateKaraokeResponse, status_code=202)
async def generate_karaoke(
    request: GenerateKaraokeRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a karaoke video from a YouTube URL.
    
    Creates an asynchronous job and returns a job ID for tracking progress.
    """
    try:
        job_id = karaoke_service.create_job(
            youtube_url=str(request.youtube_url),
            audio_format=request.audio_format,
            audio_bitrate=request.audio_bitrate
        )
        
        background_tasks.add_task(karaoke_service.process_job, job_id)
        
        return GenerateKaraokeResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            message="Karaoke generation job created successfully",
            video_url=None
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get("/status/{job_id}", response_model=GenerateKaraokeResponse)
async def get_job_status(job_id: str):
    """Get the status of a karaoke generation job."""
    job = karaoke_service.get_job_status(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    video_url = None
    if job["status"] == JobStatus.COMPLETED and job.get("video_path"):
        video_url = f"/api/v1/karaoke/download/{job_id}"
    
    return GenerateKaraokeResponse(
        job_id=job["job_id"],
        status=job["status"],
        message=_get_status_message(job["status"], job.get("error")),
        video_url=video_url
    )


@router.get("/download/{job_id}")
async def download_video(job_id: str):
    """Download the generated karaoke video."""
    job = karaoke_service.get_job_status(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    if job["status"] != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Video is not ready. Current status: {job['status']}"
        )
    
    video_path = job.get("video_path")
    if not video_path:
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # TODO: Return file response when video rendering is implemented
    # from fastapi.responses import FileResponse
    # return FileResponse(path=video_path, media_type="video/mp4", filename=f"karaoke_{job_id}.mp4")
    
    return {"message": "Video download endpoint - to be implemented when video rendering is complete"}


def _get_status_message(status: JobStatus, error: Optional[str] = None) -> str:
    """Get human-readable status message."""
    if error:
        return f"Job failed: {error}"
    
    status_messages = {
        JobStatus.PENDING: "Job is queued and waiting to start",
        JobStatus.DOWNLOADING: "Downloading audio from YouTube",
        JobStatus.PROCESSING_AUDIO: "Processing audio and separating vocals",
        JobStatus.FETCHING_LYRICS: "Fetching lyrics for the song",
        JobStatus.SYNCHRONIZING: "Synchronizing lyrics with audio timestamps",
        JobStatus.RENDERING_VIDEO: "Rendering video with lyrics overlay",
        JobStatus.COMPLETED: "Karaoke video generation completed successfully",
        JobStatus.FAILED: "Job failed during processing",
    }
    
    return status_messages.get(status, "Unknown status")

