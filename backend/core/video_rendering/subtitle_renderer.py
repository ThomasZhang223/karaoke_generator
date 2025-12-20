"""
Subtitle-based rendering for lyrics - more reliable than drawtext for many lyrics.
This uses FFmpeg's subtitles filter which is designed for this exact use case.
"""

import tempfile
from pathlib import Path
from typing import List
from backend.core.lyrics_intelligence.synchronizer import LyricLine


def create_ass_subtitle_file(lyrics: List[LyricLine], title: str = "", artist: str = "") -> str:
    """
    Create an ASS (Advanced SubStation Alpha) subtitle file from lyrics.
    ASS format supports styling and is ideal for karaoke videos.
    
    Returns:
        Path to the temporary ASS subtitle file
    """
    subtitle_file = tempfile.NamedTemporaryFile(mode='w', suffix='.ass', delete=False, encoding='utf-8')
    
    # Write ASS header
    subtitle_file.write("[Script Info]\n")
    subtitle_file.write("Title: Karaoke Video\n")
    subtitle_file.write("ScriptType: v4.00+\n")
    subtitle_file.write("\n")
    
    # Write V4+ Styles section
    subtitle_file.write("[V4+ Styles]\n")
    subtitle_file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
    subtitle_file.write("Style: Default,Arial,42,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,0,5,10,10,10,1\n")
    subtitle_file.write("\n")
    
    # Write Events section
    subtitle_file.write("[Events]\n")
    subtitle_file.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    
    # Add title/artist at the start (first 4 seconds)
    if title or artist:
        subtitle_file.write(f"Dialogue: 0,0:00:00.00,0:00:04.00,Default,,0,0,0,,{{\\an5}}{title}\n")
        if artist:
            subtitle_file.write(f"Dialogue: 0,0:00:00.00,0:00:04.00,Default,,0,0,0,,{{\\an5\\fs32}}\\N{artist}\n")
    
    # Add lyrics
    for lyric in lyrics:
        # Check if text exists and is not empty
        if not hasattr(lyric, 'text') or not lyric.text:
            continue
        if isinstance(lyric.text, str) and not lyric.text.strip():
            continue
        
        # Convert seconds to ASS time format (H:MM:SS.cc)
        def format_time(seconds: float) -> str:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hours}:{int(minutes):02d}:{secs:05.2f}"
        
        start_time = format_time(lyric.start_time)
        end_time = format_time(lyric.end_time)
        
        # Escape text for ASS format
        text = lyric.text.replace("\\", "\\\\").replace("{", "{{").replace("}", "}}")
        
        # Center-aligned text with styling
        subtitle_file.write(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{{\\an5}}{text}\n")
    
    subtitle_file.close()
    return subtitle_file.name


def build_subtitle_filter(subtitle_file_path: str) -> str:
    """
    Build FFmpeg filter string to burn subtitles into video.
    
    Returns:
        FFmpeg filter_complex string
    """
    # Escape the path for Windows
    escaped_path = subtitle_file_path.replace("\\", "\\\\").replace(":", "\\:")
    return f"subtitles='{escaped_path}':force_style='Alignment=5,Fontsize=42,OutlineColour=&H80000000,BackColour=&H80000000,Outline=2'"

