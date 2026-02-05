"""
Video rendering module using FFmpeg
Story 3.4: Video rendering foundation
Story 3.5: Lyrics-to-video synchronization
"""

import subprocess
import os
from pathlib import Path
from typing import Optional, Tuple
from backend.core.video_rendering.overlay import (
    create_lyrics_overlay_filter,
    OverlayConfig
)
from backend.core.lyrics_intelligence.synchronizer import LRCData


# ============================================================================
# STORY 3.4: Video Rendering Foundation
# ============================================================================

def render_simple_video(
    audio_path: str,
    output_path: str,
    resolution: Tuple[int, int] = (1280, 720),
    background_color: str = "black"
) -> str:
    """
    Render a simple video with audio and solid color background (no lyrics).
    
    Story 3.4: Basic video creation (720p resolution)
    
    Args:
        audio_path: Path to audio file
        output_path: Path for output video file
        resolution: Video resolution
        background_color: Background color
        
    Returns:
        Path to rendered video file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    audio_duration = _get_audio_duration(audio_path)
    
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", f"color=c={background_color}:size={resolution[0]}x{resolution[1]}:duration={audio_duration}:rate=30",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y",
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=600)
        
        if not output_file.exists():
            raise FileNotFoundError(f"Video file not created: {output_path}")
        
        return str(output_file.absolute())
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("Video rendering timed out")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Video rendering failed: {e.stderr}")


# ============================================================================
# STORY 3.5: Lyrics-to-Video Synchronization
# ============================================================================

def render_karaoke_video(
    audio_path: str,
    lrc_data: LRCData,
    output_path: str,
    resolution: Tuple[int, int] = (1280, 720),  # 720p
    background_color: str = "black",
    overlay_config: Optional[OverlayConfig] = None
) -> str:
    """
    Render karaoke video with synchronized lyrics overlay.
    
    Story 3.4: Basic video creation (720p resolution)
    Story 3.5: Lyrics displayed at correct timestamps
    
    Args:
        audio_path: Path to instrumental audio file
        lrc_data: LRCData with synchronized lyrics
        output_path: Path for output video file
        resolution: Video resolution (width, height)
        background_color: Background color (e.g., "black", "#000000")
        overlay_config: Configuration for text overlay
        
    Returns:
        Path to rendered video file
        
    Raises:
        RuntimeError: If video rendering fails
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Get audio duration
    audio_duration = _get_audio_duration(audio_path)
    
    # Story 3.5: Create lyrics overlay
    lyrics_list = lrc_data.lyrics or []
    print(f"[Video] Creating overlay with {len(lyrics_list)} lyric lines...")
    
    combined_filter = ""
    subtitle_file_to_cleanup = None
    use_subtitles = False
    
    if len(lyrics_list) == 0:
        print("[Video] ⚠ WARNING: No lyrics available for overlay!")
    else:
        # Show first few lyrics for verification
        for i, lyric in enumerate(lyrics_list[:3]):
            print(f"[Video]   Line {i+1}: '{lyric.text[:50]}...' at {lyric.start_time:.2f}s - {lyric.end_time:.2f}s")
        if len(lyrics_list) > 3:
            print(f"[Video]   ... and {len(lyrics_list) - 3} more lines")
        
        # Use subtitle file approach for songs with many lyrics (more reliable than many drawtext filters)
        # This avoids FFmpeg parsing issues with very long filter chains
        if len(lyrics_list) > 20:
            print(f"[Video] Using subtitle file approach (reliable for {len(lyrics_list)} lyrics)")
            from backend.core.video_rendering.subtitle_renderer import create_ass_subtitle_file, build_subtitle_filter
            
            subtitle_file = create_ass_subtitle_file(
                lyrics_list,
                lrc_data.title or "",
                lrc_data.artist or ""
            )
            combined_filter = build_subtitle_filter(subtitle_file)
            subtitle_file_to_cleanup = subtitle_file
            use_subtitles = True
        else:
            # Use drawtext filters for shorter songs
            overlay_filter = create_lyrics_overlay_filter(
                lyrics_list,
                overlay_config or OverlayConfig()
            )
            
            # Add title/artist intro overlay (first 4 seconds)
            intro_filters = []
            if lrc_data.title or lrc_data.artist:
                title_text = lrc_data.title or "Unknown Title"
                artist_text = lrc_data.artist or "Unknown Artist"
                
                intro_filters.append(
                    f"drawtext="
                    f'text="{_escape_text_for_ffmpeg(title_text)}":'
                    f"fontsize=40:"
                    f"fontcolor=white:"
                    f"x=(w-text_w)/2:"
                    f"y=h*0.12:"
                    f"enable=between(t,0,4):"
                    f"box=1:"
                    f"boxcolor=black@0.7:"
                    f"boxborderw=3"
                )
                intro_filters.append(
                    f"drawtext="
                    f'text="{_escape_text_for_ffmpeg(artist_text)}":'
                    f"fontsize=32:"
                    f"fontcolor=white:"
                    f"x=(w-text_w)/2:"
                    f"y=h*0.12+50:"
                    f"enable=between(t,0,4):"
                    f"box=1:"
                    f"boxcolor=black@0.7:"
                    f"boxborderw=3"
                )
            
            all_filters = intro_filters.copy()
            if overlay_filter and overlay_filter.strip():
                all_filters.append(overlay_filter)
            
            combined_filter = ",".join(all_filters) if all_filters else ""
    
    if combined_filter:
        filter_length = len(combined_filter)
        if use_subtitles:
            print(f"[Video] ✓ Subtitle filter created ({filter_length} chars)")
        else:
            print(f"[Video] ✓ Overlay filter created ({filter_length} chars, {len(lyrics_list)} lyrics)")
    else:
        print("[Video] ⚠ WARNING: Overlay filter is empty! Video will render without lyrics.")
    
    # Story 3.4: Build FFmpeg command
    # Create solid color background video, add audio, overlay lyrics
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", f"color=c={background_color}:size={resolution[0]}x{resolution[1]}:duration={audio_duration}:rate=24",  # Reduced from 30fps to 24fps for speed
        "-i", audio_path,
    ]
    
    # Only add video filter if we have a non-empty filter
    if combined_filter:
        if use_subtitles:
            # Subtitles filter uses -vf (simpler than filter_complex)
            cmd.extend(["-vf", combined_filter])
        elif len(combined_filter) > 4000:
            # For very long drawtext filter strings, use filter file
            import tempfile
            print(f"[Video] Using filter file (filter string length: {len(combined_filter)} chars)")
            filter_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8', newline='\n')
            filter_complex_content = f"[0:v]{combined_filter}[v]"
            filter_file.write(filter_complex_content)
            filter_file.flush()
            os.fsync(filter_file.fileno())
            filter_file.close()
            filter_file_path = filter_file.name
            print(f"[Video] Filter file created: {filter_file_path}")
            cmd.extend(["-filter_complex_script", filter_file_path])
            cmd.extend(["-map", "[v]", "-map", "1:a"])
            # filter_file_path stored for cleanup in finally block
        else:
            cmd.extend(["-vf", combined_filter])
    
    cmd.extend([
        "-c:v", "libx264",
        "-preset", "ultrafast",  # Changed from "medium" to "ultrafast" for speed
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",  # Reduced from 192k for faster encoding
        "-movflags", "+faststart",  # Enable fast start for web playback
        "-shortest",
        "-y",  # Overwrite output
        str(output_file)
    ])
    
    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=600  # 10 minute timeout
        )
        
        if not output_file.exists():
            raise FileNotFoundError(f"Video file not created: {output_path}")
        
        return str(output_file.absolute())
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("Video rendering timed out after 10 minutes")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Video rendering failed: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"Video rendering error: {str(e)}")
    finally:
        # Clean up temporary filter file if it was created
        # Extract filter file path from cmd
        # Clean up temporary files
        files_to_cleanup = []
        
        # Find filter file if it was created
        if combined_filter and len(combined_filter) > 4000 and not use_subtitles:
            for i, arg in enumerate(cmd):
                if arg == "-filter_complex_script" and i + 1 < len(cmd):
                    files_to_cleanup.append(cmd[i + 1])
                    break
        
        # Add subtitle file if it was created
        if subtitle_file_to_cleanup and os.path.exists(subtitle_file_to_cleanup):
            files_to_cleanup.append(subtitle_file_to_cleanup)
        
        for file_path in files_to_cleanup:
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                    print(f"[Video] Cleaned up temporary file: {file_path}")
                except Exception as e:
                    print(f"[Video] Warning: Could not delete temporary file {file_path}: {e}")


# ============================================================================
# Helper Functions
# ============================================================================

def _get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file using FFprobe.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        return float(result.stdout.strip())
        
    except (subprocess.CalledProcessError, ValueError) as e:
        # Default to 180 seconds (3 minutes) if we can't determine
        print(f"Warning: Could not determine audio duration: {e}. Using 180s default.")
        return 180.0


def _escape_text_for_ffmpeg(text: str) -> str:
    """Escape special characters for FFmpeg drawtext (handles newlines)."""
    # Use double quotes for text to avoid single quote escaping issues
    # Escape backslashes first
    text = text.replace("\\", "\\\\")
    # Escape double quotes (since we use double quotes for text parameter)
    text = text.replace('"', '\\"')
    # Escape colons, brackets
    text = text.replace(":", "\\:")
    text = text.replace("[", "\\[")
    text = text.replace("]", "\\]")
    return text
