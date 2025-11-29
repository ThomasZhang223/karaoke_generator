import json
import subprocess
import re
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
    
    # Fetch metadata from video
    metadata_cmd = ["yt-dlp", "-J", "--skip-download", url]
    metadata_success = False
    
    try:
        result = subprocess.run(metadata_cmd, capture_output=True, text=True,timeout=30)
        
        if result.returncode !=0:
            print(f'Failed to fetch video info: {result.stderr}')
            return None
        
        metadata = json.loads(result.stdout)
        
        # Duration string is given in Minutes:Seconds
        duration_str = metadata.get('duration_string', '0:0')
        time = duration_str.split(':') 
        duration = int(time[0])*60 + int(time[1]) if len(time) >= 2 else 0
        
        filesize = metadata.get('filesize_approx', 0)
        metadata_success = True
        #print(metadata)
        
    except subprocess.TimeoutExpired:
        print("Timeout fetching video metadata")
    except KeyError as e:
        print(f'No data exists for field: {e}')
        
    output_template = str(output_dir / f"{video_id}.%(ext)s")
    download_cmd = ['yt-dlp', url, '-x', '--audio-format', audio_format, '--audio-quality', f'{bitrate}K', '--no-playlist', '-o', output_template]
    
    # Download video audio
    try:
        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=600)
        if result.returncode !=0:
            print(f'Failed to fetch video audio: {result.stderr}')
            return None
    except subprocess.TimeoutExpired:
        print("Download timed out")
        return None
    except RuntimeError as e:
        print(f'Error occured while fetching video metadata: {e}')
        
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
    
    return AudioFile(
        id = video_id,
        source_url=url,
        file_path=str(final_path.absolute()),
        format=audio_format,
        duration=  duration if metadata_success else None,
        bitrate=bitrate,
        file_size=filesize if metadata_success else None,
        created_at=datetime.now(),
        status=Status.DOWNLOADED
    )
    