"""
Save the actual filter file from the test so we can inspect it.
"""

import tempfile
import os
from backend.core.video_rendering.overlay import create_lyrics_overlay_filter, OverlayConfig
from backend.core.lyrics_intelligence.synchronizer import LyricLine, LRCData

# Create the same lyrics
lyrics = []
lyric_data = [
    (8.04, 16.52, "Take my hand and come with me to another place"),
    (16.52, 21.12, "In outer space"),
    (21.12, 37.47, "We can walk around the universe tonight"),
    (37.47, 39.87, ""),
    (39.87, 46.35, "Through the passages that lay inside your mind"),
    (46.35, 54.22, "We'll take a look inside and I'll show you all"),
    (54.22, 61.37, "The wonders far and wide"),
    (61.37, 69.12, "So let's fly up to the moon and see"),
    (69.12, 75.69, "The stars from high above"),
    (75.69, 83.94, "With no rain, and no clouds"),
    (83.94, 91.22, "Only love, oh"),
    (91.22, 98.97, "And we'll dance along the Milky Way"),
    (98.97, 105.69, "I hope that you feel the same"),
    (105.69, 150.21, "About me, about us, about love"),
    (150.21, 154.92, "Won't you just come on over"),
    (154.92, 160.82, "And let's share the blankets on my bed"),
    (160.82, 165.03, "Lay here instead"),
    (165.03, 179.21, "We won't need to do much thinking in our dreams"),
    (179.21, 187.49, "So let's fly up to the moon and see"),
    (187.49, 194.47, "The stars from high above"),
    (194.47, 201.66, "With no rain, and no clouds"),
    (201.66, 208.85, "Only love, oh"),
    (208.85, 217.01, "And we'll dance along the Milky Way"),
    (217.01, 223.97, "I hope that you feel the same"),
    (223.97, 231.42, "About me, about us"),
    (231.42, 238.72, "About me, about us"),
    (238.72, 245.35, "About me, about us"),
    (245.35, 249.35, "No, about love"),
]

for start, end, text in lyric_data:
    lyrics.append(LyricLine(text=text if text else " ", start_time=start, end_time=end))

lrc_data = LRCData(title="(Only) About Love", artist="grentperez", lyrics=lyrics)
config = OverlayConfig(font_size=42)
overlay_filter = create_lyrics_overlay_filter(lyrics, config)

intro_filters = [
    f'drawtext=text="{lrc_data.title}":fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h*0.12:enable=\'between(t,0,4)\':box=1:boxcolor=black@0.7:boxborderw=3',
    f'drawtext=text="{lrc_data.artist}":fontsize=32:fontcolor=white:x=(w-text_w)/2:y=h*0.12+50:enable=\'between(t,0,4)\':box=1:boxcolor=black@0.7:boxborderw=3'
]

all_filters = intro_filters.copy()
all_filters.append(overlay_filter)
combined_filter = ",".join(all_filters)

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

MAX_FILTERS_PER_CHUNK = 5
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
    filter_complex_content = ';'.join(filter_chains)
else:
    filter_complex_content = f"[0:v]{combined_filter}[v]"

# Save to file for inspection
output_file = "saved_filter_file.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(filter_complex_content)

print(f"Saved filter file to: {output_file}")
print(f"Length: {len(filter_complex_content)} chars")
print(f"Number of chunks: {filter_complex_content.count(';') + 1}")

# Find the problematic area around the error
if "91.22" in filter_complex_content:
    idx = filter_complex_content.find("91.22")
    print(f"\n=== Around error location (91.22) ===")
    print(filter_complex_content[max(0, idx-300):idx+500])

