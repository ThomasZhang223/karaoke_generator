"""
Inspect the actual filter file being generated to debug the FFmpeg parsing error.
"""

import tempfile
import os
from backend.core.video_rendering.overlay import create_lyrics_overlay_filter, OverlayConfig
from backend.core.lyrics_intelligence.synchronizer import LyricLine, LRCData

# Create the same lyrics as the failing test
lyrics = []
lyric_data = [
    (91.22, 98.97, "And we'll dance along the Milky Way"),
    (98.97, 105.69, "I hope that you feel the same"),
]

for start, end, text in lyric_data:
    lyrics.append(LyricLine(text=text, start_time=start, end_time=end))

lrc_data = LRCData(title="Test", artist="Test", lyrics=lyrics)
config = OverlayConfig(font_size=42)
overlay_filter = create_lyrics_overlay_filter(lyrics, config)

intro_filters = [
    f'drawtext=text="Test":fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h*0.12:enable=\'between(t,0,4)\':box=1:boxcolor=black@0.7:boxborderw=3',
]

all_filters = intro_filters.copy()
all_filters.append(overlay_filter)
combined_filter = ",".join(all_filters)

# Split filters
def split_filters_respecting_quotes(filter_string):
    parts = []
    current = []
    in_single_quotes = False
    in_double_quotes = False
    i = 0
    while i < len(filter_string):
        char = filter_string[i]
        if char == "'" and not in_double_quotes and (i == 0 or filter_string[i-1] != '\\'):
            in_single_quotes = not in_single_quotes
            current.append(char)
        elif char == '"' and not in_single_quotes and (i == 0 or filter_string[i-1] != '\\'):
            in_double_quotes = not in_double_quotes
            current.append(char)
        elif char == ',' and not in_single_quotes and not in_double_quotes:
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

print(f"Filter parts: {len(filter_parts)}")
for i, part in enumerate(filter_parts):
    print(f"\nPart {i+1}: {part[:150]}...")
    if "91.22" in part or "98.97" in part:
        print(f"  FULL: {part}")

# Create chunked version
MAX_FILTERS_PER_CHUNK = 15
if len(filter_parts) > MAX_FILTERS_PER_CHUNK:
    filter_chains = []
    chunk_num = 0
    for i in range(0, len(filter_parts), MAX_FILTERS_PER_CHUNK):
        chunk = filter_parts[i:i+MAX_FILTERS_PER_CHUNK]
        chunk_filter_str = ','.join(chunk)
        if i == 0:
            input_label = "[0:v]"
            output_label = f"[v{chunk_num}]"
        elif i + MAX_FILTERS_PER_CHUNK >= len(filter_parts):
            input_label = f"[v{chunk_num-1}]"
            output_label = "[v]"
        else:
            input_label = f"[v{chunk_num-1}]"
            output_label = f"[v{chunk_num}]"
        filter_chains.append(f"{input_label}{chunk_filter_str}{output_label}")
        chunk_num += 1
        print(f"\nChunk {chunk_num}:")
        print(f"  Input: {input_label}, Output: {output_label}")
        print(f"  Content: {chunk_filter_str[:200]}...")
    filter_complex_content = ';'.join(filter_chains)
else:
    filter_complex_content = f"[0:v]{combined_filter}[v]"

print(f"\n\nFinal filter complex:")
print(filter_complex_content)

