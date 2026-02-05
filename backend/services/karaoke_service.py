"""
Karaoke generation service.
Orchestrates audio acquisition, processing, lyrics intelligence, and video rendering.
Story 4.1: End-to-End Integration
"""

import uuid
import asyncio
from pathlib import Path
from typing import Optional
from datetime import datetime

from backend.core.audio_acquisition.downloader import (
    validate_url,
    download_audio,
)
from backend.core.audio_processing.separator import separate_vocals
from backend.core.audio_processing.optimizer import optimize_audio_quality
from backend.core.lyrics_intelligence.scraper import fetch_lyrics
from backend.core.lyrics_intelligence.title_normalizer import normalize_title_and_artist
from backend.core.lyrics_intelligence.synchronizer import (
    synchronize_from_lrclib_result,
    generate_lrc_file,
    LRCData
)
from backend.core.video_rendering.renderer import render_karaoke_video
from backend.core.video_rendering.overlay import OverlayConfig
from backend.models.schemas import JobStatus
from backend.config import settings


class KaraokeService:
    """Service for generating karaoke videos from YouTube URLs."""
    
    def __init__(self):
        """Initialize the karaoke service."""
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory job storage (for MVP - could be replaced with database)
        self.jobs: dict[str, dict] = {}
    
    def create_job(
        self,
        youtube_url: str,
        audio_format: str = "mp3",
        audio_bitrate: int = 192
    ) -> str:
        """Create a new karaoke generation job and return job ID."""
        is_valid, video_id = validate_url(youtube_url)
        if not is_valid:
            raise ValueError(f"Invalid YouTube URL: {youtube_url}")
        
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "job_id": job_id,
            "youtube_url": youtube_url,
            "video_id": video_id,
            "status": JobStatus.PENDING,
            "audio_format": audio_format,
            "audio_bitrate": audio_bitrate,
            "created_at": datetime.now().isoformat(),
            "error": None,
            "video_path": None,
            "progress": 0,
            "stage": "Job queued, waiting to start...",
        }
        print(f"[Service] Created job {job_id}: status={JobStatus.PENDING}, progress=0")
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[dict]:
        """Get the status of a karaoke generation job."""
        return self.jobs.get(job_id)
    
    async def process_job(self, job_id: str) -> dict:
        """
        Process a karaoke generation job asynchronously.
        
        Story 4.1: Complete pipeline working end-to-end
        Orchestrates: download audio → separate vocals → fetch lyrics → 
        synchronize → render video
        """
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        
        try:
            # ====================================================================
            # Step 1: Download audio (Story 2.1 - Thomas)
            # ====================================================================
            job["status"] = JobStatus.DOWNLOADING
            job["progress"] = 10
            job["stage"] = "Downloading audio from YouTube"
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            # Run blocking subprocess in thread pool to avoid blocking event loop
            audio_file = await asyncio.to_thread(
                download_audio,
                url=job["youtube_url"],
                output_dir=self.output_dir / "audio",
                audio_format=job["audio_format"],
                bitrate=job["audio_bitrate"]
            )
            
            if audio_file is None:
                raise Exception("Failed to download audio from YouTube")
            
            # ====================================================================
            # Step 2: Process audio (vocal separation)
            # Story 3.3: Audio Processing Integration (Mark)
            # Uses functions from Story 2.2: Demucs Vocal Separation Pipeline
            # ====================================================================
            job["status"] = JobStatus.PROCESSING_AUDIO
            job["progress"] = 25
            job["stage"] = "Separating vocals from audio (this may take a few minutes)..."
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            separated_dir = self.output_dir / "separated" / job_id
            # Run blocking subprocess in thread pool to avoid blocking event loop
            separated_result = await asyncio.to_thread(
                separate_vocals,
                audio_path=audio_file.file_path,
                output_dir=str(separated_dir),
                use_fallback=False  # Set to True for Story 2.3 (Spleeter fallback)
            )
            
            instrumental_path = separated_result["instrumental"]
            
            # Update progress after separation
            job["progress"] = 40
            job["stage"] = "Optimizing audio quality"
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            # Story 3.3: Audio Processing Integration (Mark)
            # Uses optimize_audio_quality from Story 2.2
            optimized_path = self.output_dir / "audio" / f"{job_id}_optimized.wav"
            # Run blocking subprocess in thread pool to avoid blocking event loop
            await asyncio.to_thread(
                optimize_audio_quality,
                input_path=instrumental_path,
                output_path=str(optimized_path),
                normalize=True,
                denoise=False
            )
            instrumental_path = str(optimized_path)
            
            # ====================================================================
            # Step 3: Fetch lyrics (Story 2.4 - Aruhant)
            # ====================================================================
            job["status"] = JobStatus.FETCHING_LYRICS
            job["progress"] = 50
            job["stage"] = "Fetching lyrics for the song"
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            # Get audio duration for lyrics matching
            audio_duration = audio_file.duration if audio_file.duration else 180
            
            # Search for lyrics using video title and artist
            # Normalize title and artist to remove YouTube video tags like "(audio)", "(video)", etc.
            normalized_title, normalized_artist = normalize_title_and_artist(
                audio_file.title,
                audio_file.artist
            )
            
            # Build search string: prefer "title artist" or just "title"
            search_str = ""
            if normalized_title:
                if normalized_artist:
                    # Try multiple search strategies
                    search_attempts = [
                        f"{normalized_title} {normalized_artist}",  # "Song Artist"
                        f"{normalized_artist} {normalized_title}",  # "Artist Song"
                        normalized_title,  # Just title
                    ]
                else:
                    search_attempts = [normalized_title]
            else:
                # Fallback: try to get title from YouTube URL directly
                # This is a last resort - video ID won't work
                search_attempts = [job["video_id"]]
                print(f"Warning: No title extracted, using video ID as fallback (may not find lyrics)")
            
            # Try multiple search strategies
            lyrics_result = None
            for attempt in search_attempts:
                print(f"Searching lyrics for: '{attempt}'")
                lyrics_result = fetch_lyrics(
                    search_str=attempt,
                    duration=audio_duration
                )
                if lyrics_result is not None:
                    print(f"Found lyrics using search: '{attempt}'")
                    break
            
            if lyrics_result is None:
                # Provide helpful error message and allow graceful degradation
                error_msg = f"Could not find lyrics for this song"
                if normalized_title:
                    error_msg += f" (searched for: '{normalized_title}'"
                    if normalized_artist:
                        error_msg += f" by {normalized_artist}"
                    error_msg += ")"
                    if audio_file.title != normalized_title:
                        error_msg += f" [original title: '{audio_file.title}']"
                else:
                    error_msg += f" (no title available from video metadata - metadata fetch timed out)"
                
                # Option 1: Raise error (current behavior)
                raise Exception(error_msg)
                
                # Option 2: Continue without lyrics (uncomment to enable)
                # print(f"Warning: {error_msg}. Continuing without lyrics - video will have no text overlay.")
                # # Create empty LRC data
                # from backend.core.lyrics_intelligence.synchronizer import LRCData
                # lrc_data = LRCData(
                #     title=audio_file.title or "Unknown",
                #     artist=audio_file.artist or "Unknown",
                #     lyrics=[]
                # )
            
            # ====================================================================
            # Step 4: Synchronize lyrics (Story 3.2 - Aruhant)
            # ====================================================================
            job["status"] = JobStatus.SYNCHRONIZING
            job["progress"] = 70
            job["stage"] = "Synchronizing lyrics with audio timestamps"
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            lrc_data = synchronize_from_lrclib_result(
                lyrics_result,
                audio_duration
            )
            
            # Story 2.5: Generate LRC file (Aruhant)
            lrc_path = self.output_dir / "lyrics" / f"{job_id}.lrc"
            generate_lrc_file(lrc_data, str(lrc_path))
            
            # ====================================================================
            # Step 5: Render video (Story 3.4, 3.5 - William)
            # ====================================================================
            job["status"] = JobStatus.RENDERING_VIDEO
            job["progress"] = 80
            job["stage"] = "Rendering video with lyrics overlay (this may take a few minutes)..."
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            video_path = self.output_dir / "videos" / f"{job_id}.mp4"
            
            overlay_config = OverlayConfig(
                font_size=42,  # Smaller, more karaoke-appropriate size
                font_color="white",
                highlight_color="yellow",
                position="center"
            )
            
            # Run blocking subprocess in thread pool to avoid blocking event loop
            await asyncio.to_thread(
                render_karaoke_video,
                audio_path=instrumental_path,
                lrc_data=lrc_data,
                output_path=str(video_path),
                resolution=(1280, 720),  # 720p
                background_color="black",
                overlay_config=overlay_config
            )
            
            # Update progress after rendering starts (FFmpeg is encoding)
            job["progress"] = 95
            job["stage"] = "Finalizing video..."
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
            # ====================================================================
            # Complete
            # ====================================================================
            job["status"] = JobStatus.COMPLETED
            job["progress"] = 100
            job["stage"] = "Karaoke video generation completed"
            job["video_path"] = str(video_path.absolute())
            print(f"[Service] Job {job_id}: {job['stage']} ({job['progress']}%)")
            
        except Exception as e:
            job["status"] = JobStatus.FAILED
            job["error"] = str(e)
            job["stage"] = f"Error: {str(e)}"
            raise
        
        return job

