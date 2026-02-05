"""
Debug script to inspect the actual filter file content and find the issue.
"""

import tempfile
import os
from backend.core.video_rendering.overlay import create_lyrics_overlay_filter, OverlayConfig
from backend.core.lyrics_intelligence.synchronizer import LyricLine, LRCData


def create_realistic_long_song_lyrics() -> LRCData:
    """Create lyrics similar to the actual 4+ minute song that was failing."""
    lyrics = []
    
    lyric_data = [
        (8.04, 16.52, "Take my hand and come with me to another place"),
        (16.52, 21.12, "In outer space"),
        (91.22, 98.97, "And we'll dance along the Milky Way"),  # Around the error point
        (98.97, 105.69, "I hope that you feel the same"),
    ]
    
    for start, end, text in lyric_data:
        lyrics.append(LyricLine(text=text, start_time=start, end_time=end))
    
    return LRCData(title="Test Song", artist="Test Artist", lyrics=lyrics)


def main():
    lrc_data = create_realistic_long_song_lyrics()
    config = OverlayConfig(font_size=42)
    
    overlay_filter = create_lyrics_overlay_filter(lrc_data.lyrics, config)
    
    intro_filters = [
        f'drawtext=text="{lrc_data.title}":fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h*0.12:enable=\'between(t,0,4)\':box=1:boxcolor=black@0.7:boxborderw=3',
    ]
    
    all_filters = intro_filters.copy()
    all_filters.append(overlay_filter)
    combined_filter = ",".join(all_filters)
    
    filter_complex_content = f"[0:v]{combined_filter}[v]"
    
    # Save to file for inspection
    filter_file_path = "debug_filter_content.txt"
    with open(filter_file_path, 'w', encoding='utf-8') as f:
        f.write(filter_complex_content)
    
    print(f"Filter file saved to: {filter_file_path}")
    print(f"Length: {len(filter_complex_content)} chars")
    print("\nFirst 500 chars:")
    print(filter_complex_content[:500])
    print("\nAround the problematic area (near 91.22):")
    if "91.22" in filter_complex_content:
        idx = filter_complex_content.find("91.22")
        print(filter_complex_content[max(0, idx-200):idx+300])
    
    # Count filters
    filter_count = combined_filter.count("drawtext=")
    print(f"\nTotal drawtext filters: {filter_count}")
    
    # Check for broken patterns
    if "fontsize=42:fontcolor" in filter_complex_content:
        print("\nWARNING: Found 'fontsize=42:fontcolor' pattern - might indicate broken filter")


if __name__ == "__main__":
    main()

