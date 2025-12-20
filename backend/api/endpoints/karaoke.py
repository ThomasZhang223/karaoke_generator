"""
Karaoke generation endpoints.
Story 3.6: Frontend-Backend Integration
Story 4.1: End-to-End Integration
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
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
    """
    Download the generated karaoke video.
    
    Story 4.1: Video download functionality working
    """
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
    
    # Story 4.1: Return file response with proper MIME type
    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=f"karaoke_{job_id}.mp4"
    )


# ============================================================================
# STORY 3.6: Frontend-Backend Integration
# ============================================================================

@router.post("/generate-karaoke", response_model=dict, status_code=202)
async def generate_karaoke_for_frontend(
    request: dict,  # Frontend sends { youtubeUrl, style?, quality? }
    background_tasks: BackgroundTasks
):
    """
    Generate karaoke video - endpoint matching frontend expectations.
    Story 3.6: Frontend successfully calls backend API endpoints
    
    Frontend sends: { youtubeUrl, style?, quality? }
    Returns: { jobId }
    """
    try:
        youtube_url = request.get("youtubeUrl")
        if not youtube_url:
            raise HTTPException(status_code=400, detail="youtubeUrl is required")
        
        # Map frontend quality to backend settings
        quality = request.get("quality", "standard")
        audio_bitrate = 256 if quality == "high" else 192
        
        job_id = karaoke_service.create_job(
            youtube_url=youtube_url,
            audio_format="mp3",
            audio_bitrate=audio_bitrate
        )
        
        background_tasks.add_task(karaoke_service.process_job, job_id)
        
        return {"jobId": job_id}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get("/jobs/{job_id}", response_model=dict)
async def get_job_status_for_frontend(job_id: str):
    """
    Get job status in format expected by frontend.
    Story 3.6: Progress updates displayed in real-time
    
    Frontend expects: { jobId, status, progress, stage, videoUrl, errorMessage }
    """
    print(f"[API] GET /jobs/{job_id}: Request received")
    job = karaoke_service.get_job_status(job_id)
    print(f"[API] GET /jobs/{job_id}: Job found: {job is not None}")
    
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    # Map backend status to frontend status
    status_map = {
        JobStatus.PENDING: "queued",
        JobStatus.DOWNLOADING: "processing",
        JobStatus.PROCESSING_AUDIO: "processing",
        JobStatus.FETCHING_LYRICS: "processing",
        JobStatus.SYNCHRONIZING: "processing",
        JobStatus.RENDERING_VIDEO: "rendering",
        JobStatus.COMPLETED: "completed",
        JobStatus.FAILED: "failed",
    }
    
    frontend_status = status_map.get(job["status"], "processing")
    
    video_url = None
    if job["status"] == JobStatus.COMPLETED and job.get("video_path"):
        video_url = f"/api/v1/karaoke/download/{job_id}"
    
    # Debug: Print what we're returning
    print(f"[API] GET /jobs/{job_id}: status={frontend_status}, progress={job.get('progress', 0)}, stage={job.get('stage')}")
    
    return {
        "jobId": job["job_id"],
        "status": frontend_status,
        "progress": job.get("progress", 0),
        "stage": job.get("stage"),
        "videoUrl": video_url,
        "errorMessage": job.get("error")
    }


# ============================================================================
# Helper Functions
# ============================================================================

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

