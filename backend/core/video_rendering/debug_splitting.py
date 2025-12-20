"""
Debug the filter splitting logic to see why it's creating 86 parts instead of 30.
"""

from backend.core.video_rendering.overlay import create_lyrics_overlay_filter, OverlayConfig
from backend.core.lyrics_intelligence.synchronizer import LyricLine, LRCData

# Create simple test
lyrics = [
    LyricLine("Test 1", 1.0, 2.0),
    LyricLine("Test 2", 2.0, 3.0),
]

config = OverlayConfig()
overlay_filter = create_lyrics_overlay_filter(lyrics, config)

print(f"Overlay filter: {overlay_filter}")
print(f"Length: {len(overlay_filter)} chars")

# Test splitting
def split_filters_respecting_quotes(filter_string):
    """Split comma-separated filters, respecting commas inside single or double quotes."""
    parts = []
    current = []
    in_single_quotes = False
    in_double_quotes = False
    i = 0
    while i < len(filter_string):
        char = filter_string[i]
        # Handle single quotes
        if char == "'" and not in_double_quotes and (i == 0 or filter_string[i-1] != '\\'):
            in_single_quotes = not in_single_quotes
            current.append(char)
        # Handle double quotes
        elif char == '"' and not in_single_quotes and (i == 0 or filter_string[i-1] != '\\'):
            in_double_quotes = not in_double_quotes
            current.append(char)
        # Handle commas - only split if not inside any quotes
        elif char == ',' and not in_single_quotes and not in_double_quotes:
            # This comma is a separator
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
        i += 1
    if current:
        parts.append(''.join(current).strip())
    return [p for p in parts if p]  # Remove empty parts

split_parts = split_filters_respecting_quotes(overlay_filter)
print(f"\nSplit into {len(split_parts)} parts:")
for i, part in enumerate(split_parts):
    print(f"  Part {i+1}: {part[:100]}...")

