"""
Debug script to inspect the generated filter file and identify the parsing issue.
"""

import tempfile
import os
from backend.core.video_rendering.overlay import create_lyrics_overlay_filter, OverlayConfig
from backend.core.lyrics_intelligence.synchronizer import LyricLine, LRCData


def create_sample_long_lyrics() -> LRCData:
    """Create sample lyrics with the problematic timestamp."""
    lyrics = []
    base_time = 8.0
    
    lyric_texts = [
        "Take my hand and come with me to another place",
        "In outer space",
        "We can walk around the universe tonight",
        "",
        "And through the doors",
        "Through the passages that lay inside your mind",
        "We'll take a look inside and I'll show you all",  # Line with timestamp 46.35
        "The wonders far and wide",
    ]
    
    for i, text in enumerate(lyric_texts):
        start_time = base_time + (i * 8.0)
        end_time = start_time + 6.0
        
        if i == 6:
            start_time = 46.35
            end_time = 54.22
        
        lyrics.append(LyricLine(
            text=text if text else " ",
            start_time=start_time,
            end_time=end_time
        ))
    
    return LRCData(title="Test Song", artist="Test Artist", lyrics=lyrics)


def main():
    lrc_data = create_sample_long_lyrics()
    config = OverlayConfig()
    
    overlay_filter = create_lyrics_overlay_filter(lrc_data.lyrics, config)
    
    intro_filters = [
        f"drawtext=text='{lrc_data.title}':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h*0.12:enable='between(t,0,4)':box=1:boxcolor=black@0.7:boxborderw=3",
        f"drawtext=text='{lrc_data.artist}':fontsize=32:fontcolor=white:x=(w-text_w)/2:y=h*0.12+50:enable='between(t,0,4)':box=1:boxcolor=black@0.7:boxborderw=3"
    ]
    
    all_filters = intro_filters.copy()
    all_filters.append(overlay_filter)
    combined_filter = ",".join(all_filters)
    
    print(f"Combined filter length: {len(combined_filter)} chars")
    
    # Simulate the splitting logic
    def split_filters_respecting_quotes(filter_string):
        parts = []
        current = []
        in_quotes = False
        i = 0
        while i < len(filter_string):
            char = filter_string[i]
            if char == "'" and (i == 0 or filter_string[i-1] != '\\'):
                in_quotes = not in_quotes
                current.append(char)
            elif char == ',' and not in_quotes:
                parts.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
            i += 1
        if current:
            parts.append(''.join(current).strip())
        return [p for p in parts if p]
    
    filter_parts = []
    for f in intro_filters:
        filter_parts.append(f)
    filter_parts.extend(split_filters_respecting_quotes(overlay_filter))
    
    print(f"\nTotal filter parts: {len(filter_parts)}")
    
    # Find the problematic filter
    for i, part in enumerate(filter_parts):
        if "46.35" in part:
            print(f"\n=== Filter part {i} with timestamp 46.35 ===")
            print(part)
            print(f"\nLength: {len(part)} chars")
            print(f"Has quotes around timestamp: {'between(t,46.35' in part}")
            break
    
    # Create chunked version
    CHUNK_SIZE = 8
    if len(filter_parts) > CHUNK_SIZE:
        filter_chains = []
        for i in range(0, len(filter_parts), CHUNK_SIZE):
            chunk_filters = filter_parts[i:i+CHUNK_SIZE]
            chunk_str = ','.join(chunk_filters)
            
            if i == 0:
                input_label = "[0:v]"
                output_label = f"[v{i//CHUNK_SIZE}]"
            elif i + CHUNK_SIZE >= len(filter_parts):
                input_label = f"[v{(i//CHUNK_SIZE)-1}]"
                output_label = "[v]"
            else:
                input_label = f"[v{(i//CHUNK_SIZE)-1}]"
                output_label = f"[v{i//CHUNK_SIZE}]"
            
            filter_chains.append(f"{input_label}{chunk_str}{output_label}")
        
        filter_complex_content = ';'.join(filter_chains)
        
        # Save to file for inspection
        filter_file_path = "debug_filter.txt"
        with open(filter_file_path, 'w', encoding='utf-8') as f:
            f.write(filter_complex_content)
        
        print(f"\n=== Saved filter file to: {filter_file_path} ===")
        print(f"Total length: {len(filter_complex_content)} chars")
        print(f"Number of chunks: {len(filter_chains)}")
        
        # Show the chunk containing 46.35
        for i, chain in enumerate(filter_chains):
            if "46.35" in chain:
                print(f"\n=== Chunk {i} containing timestamp 46.35 ===")
                print(chain[:500])
                print("...")
                print(chain[-500:])
                break


if __name__ == "__main__":
    main()

