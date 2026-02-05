# ==============================================================================
# ==============================================================================
#                        AUDIO ACQUISITION MODULE
# ==============================================================================
# ==============================================================================
#
# Sprint 1 - Story 1.2: YouTube Audio Download Research & Setup (Thomas)
# Sprint 2 - Story 2.1: YouTube to MP3 Conversion Implementation (Thomas)
#
# ==============================================================================

import json
import subprocess
import re
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ==============================================================================
# SPRINT 1 - THOMAS
# Story 1.2: YouTube Audio Download Research & Setup
# - Research completed on pytube, yt-dlp, and alternatives
# - Python environment configured with required dependencies
# - Module structure created
# ==============================================================================

class Status(Enum):
    DOWNLOADED = 1
    PROCESSING = 2
    PROCESSED = 3
    FAILED = 4

@dataclass
class AudioFile:
    id: str
    source_url: str
    file_path: str
    format: str
    duration: int
    bitrate: int
    file_size: int
    created_at: datetime
    status: Status
    title: str = ""  # Video title from YouTube
    artist: str = ""  # Artist name (extracted from title if available)

# ==============================================================================
# END OF SPRINT 1 - THOMAS
# ==============================================================================


# ==============================================================================
# SPRINT 2 - THOMAS
# Story 2.1: YouTube to MP3 Conversion Implementation
# - YouTube URL validation and parsing
# - Audio download functionality
# - MP3 conversion with configurable quality (bitrate, sample rate)
# - Error handling for network issues, invalid URLs, unavailable videos
# - Fallback mechanism if primary library fails
# ==============================================================================
        
def validate_url(url):
    """
    Validate if the URL is a valid YouTube URL
        
    Returns (is_valid, video_id) where is_valid is bool and video_id is str or None
    """
    pattern = r'^(?:https?://|//)?(?:www\.|m\.)?(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?.+&v=))([\w-]{11})(?![\w-])'
    
    match = re.match(pattern, url)
    if match:
        video_id = match.group(1)
        return True, video_id
    return False, None
    
    
def download_audio(url, output_dir, audio_format, bitrate):
    """
    Download youtube video according to given params
    """
    
    valid, video_id = validate_url(url)
    if not valid:
        return None # None return indicates failure
        
    # Convert output_dir to Path if it's a string
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch metadata from video - try fast method first, then full JSON
    metadata_success = False
    title = ""
    artist = ""
    duration = 0
    filesize = 0
    
    # Strategy 1: Fast metadata fetch using --print (much faster than -J)
    try:
        print("Fetching video metadata (fast method)...")
        quick_cmd = ["yt-dlp", "--print", "title", "--print", "uploader", "--print", "duration_string", "--skip-download", url]
        quick_result = subprocess.run(quick_cmd, capture_output=True, text=True, timeout=10)
        if quick_result.returncode == 0 and quick_result.stdout:
            lines = [line.strip() for line in quick_result.stdout.strip().split('\n') if line.strip()]
            if len(lines) >= 1 and lines[0]:
                title = lines[0]
            if len(lines) >= 2 and lines[1]:
                artist = lines[1]
            if len(lines) >= 3 and lines[2]:
                # Parse duration
                duration_str = lines[2]
                time = duration_str.split(':')
                if len(time) >= 2:
                    try:
                        duration = int(time[0])*60 + int(time[1])
                    except ValueError:
                        pass
                elif len(time) == 1:
                    try:
                        duration = int(time[0])
                    except ValueError:
                        pass
            if title:
                print(f"✓ Got metadata (fast): title='{title}', artist='{artist or '(none)'}'")
                metadata_success = True
            else:
                print(f"⚠ Fast method returned empty title")
        else:
            print(f"⚠ Fast method failed: returncode={quick_result.returncode}, stderr={quick_result.stderr[:100]}")
    except subprocess.TimeoutExpired:
        print("⚠ Fast metadata fetch timed out (10s) - trying full metadata fetch...")
    except Exception as e:
        print(f"⚠ Fast metadata fetch failed: {e} - trying full metadata fetch...")
    
    # Strategy 2: Full JSON metadata fetch (slower but more complete)
    if not metadata_success:
        try:
            print("Fetching full video metadata...")
            metadata_cmd = ["yt-dlp", "-J", "--skip-download", url]
            result = subprocess.run(metadata_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f'Failed to fetch video info: {result.stderr}')
            else:
                metadata = json.loads(result.stdout)
                
                # Duration string is given in Minutes:Seconds
                duration_str = metadata.get('duration_string', '0:0')
                time = duration_str.split(':') 
                if len(time) >= 2:
                    duration = int(time[0])*60 + int(time[1])
                elif len(time) == 1:
                    duration = int(time[0])
                
                filesize = metadata.get('filesize_approx', 0)
                
                # Extract title and artist for lyrics search
                if not title:  # Only set if not already set from fast method
                    title = metadata.get('title', '')
                if not artist:  # Only set if not already set from fast method
                    artist = metadata.get('artist', '') or metadata.get('uploader', '')
                
                metadata_success = True
                print(f"Got full metadata: title='{title}', artist='{artist}'")
        
        except subprocess.TimeoutExpired:
            print("Timeout fetching full video metadata")
        except json.JSONDecodeError as e:
            print(f'Failed to parse metadata JSON: {e}')
        except KeyError as e:
            print(f'No data exists for field: {e}')
        except Exception as e:
            print(f'Error fetching metadata: {e} - continuing with download')
    
    # Try to extract artist from title if format is "Song - Artist" or "Artist - Song"
    if not artist and title:
        # Common patterns: "Song - Artist", "Artist - Song", "Song by Artist"
        if ' - ' in title:
            parts = title.split(' - ', 1)
            artist = parts[1] if len(parts) > 1 else ''
        elif ' by ' in title.lower():
            parts = title.lower().split(' by ', 1)
            if len(parts) > 1:
                artist = parts[1]
        
    output_template = str(output_dir / f"{video_id}.%(ext)s")
    
    # Use --write-info-json to save metadata during download (more reliable than separate fetch)
    info_json_path = output_dir / f"{video_id}.info.json"
    download_cmd = [
        'yt-dlp', url, 
        '-x', '--audio-format', audio_format, 
        '--audio-quality', f'{bitrate}K', 
        '--no-playlist', 
        '--write-info-json',  # Save metadata to JSON file during download
        '-o', output_template
    ]
    
    # Download video audio
    try:
        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=600)
        if result.returncode !=0:
            print(f'Failed to fetch video audio: {result.stderr}')
            return None
        
        # Extract metadata from info.json (most reliable - saved during download)
        if info_json_path.exists():
            try:
                print("Extracting metadata from info.json file...")
                with open(info_json_path, 'r', encoding='utf-8') as f:
                    info_data = json.load(f)
                    # Always use info.json data (it's the most complete)
                    title = info_data.get('title', title)  # Use info.json title, fallback to existing
                    artist = info_data.get('artist', '') or info_data.get('uploader', artist)
                    if 'duration' in info_data:
                        duration = int(info_data['duration'])
                    if 'filesize_approx' in info_data:
                        filesize = info_data.get('filesize_approx', filesize)
                    print(f"✓ Extracted from info.json: title='{title}', artist='{artist or '(none)'}'")
                    metadata_success = True
            except Exception as e:
                print(f"⚠ Failed to read info.json: {e}")
        else:
            print(f"⚠ info.json not found at {info_json_path}")
        
        # Also try to parse title from download output (yt-dlp sometimes prints it)
        if not title and result.stdout:
            # Look for patterns like "[download] Destination: ..." or title in output
            for line in result.stdout.split('\n'):
                if 'title' in line.lower() and not title:
                    # Try to extract title from various output formats
                    pass  # yt-dlp output format varies, so we rely on info.json instead
        
    except subprocess.TimeoutExpired:
        print("Download timed out")
        return None
    except RuntimeError as e:
        print(f'Error occurred while downloading: {e}')
        
     # Step 3: Find the downloaded file
    final_path = output_dir / f"{video_id}.{audio_format}"
    print(f'FINAL PATH: {final_path}')
    
    if not final_path.exists():
        # Try finding file with different naming
        matches = list(output_dir.glob(f"{video_id}*.{audio_format}"))
        if matches:
            final_path = matches[0]
        else:
            print(f"Downloaded file not found: {final_path}")
            return None
    
    # Final check: print what we have
    if not title:
        print(f"⚠ WARNING: No title extracted after all attempts for video {video_id}")
    else:
        print(f"✓ Final metadata: title='{title}', artist='{artist or '(none)'}'")
    
    return AudioFile(
        id = video_id,
        source_url=url,
        file_path=str(final_path.absolute()),
        format=audio_format,
        duration=  duration if metadata_success else None,
        bitrate=bitrate,
        file_size=filesize if metadata_success else None,
        created_at=datetime.now(),
        status=Status.DOWNLOADED,
        title=title,  # Use title even if metadata_success is False (might have gotten from fallback)
        artist=artist  # Use artist even if metadata_success is False (might have gotten from fallback)
    )

# ==============================================================================
# END OF SPRINT 2 - THOMAS
# ==============================================================================