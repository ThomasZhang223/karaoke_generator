"""
Text overlay module for synchronized lyrics display
Story 3.4: Text overlay functionality
Story 3.5: Synchronized lyrics display
"""

from typing import List, Tuple
from dataclasses import dataclass
from backend.core.lyrics_intelligence.synchronizer import LyricLine


# ============================================================================
# STORY 3.4: Text Overlay Functionality
# ============================================================================

@dataclass
class OverlayConfig:
    """Configuration for text overlay rendering."""
    font_size: int = 60
    font_color: str = "white"
    highlight_color: str = "yellow"
    position: str = "center"  # center, bottom
    background_color: str = "black@0.5"  # black with 50% opacity
    stroke_color: str = "black"
    stroke_width: int = 2


def create_simple_overlay_filter(
    text: str,
    start_time: float,
    end_time: float,
    config: OverlayConfig = None
) -> str:
    """
    Create a simple text overlay filter for a single text segment.
    
    Story 3.4: Text overlay functionality
    
    Args:
        text: Text to display
        start_time: Start time in seconds
        end_time: End time in seconds
        config: Overlay configuration
        
    Returns:
        FFmpeg drawtext filter string
    """
    if config is None:
        config = OverlayConfig()
    
    x_expr = "(w-text_w)/2"
    y_expr = f"h-th-{config.font_size}"
    
    return (
        f"drawtext="
        f"text='{_escape_text(text)}':"
        f"fontsize={config.font_size}:"
        f"fontcolor={config.font_color}:"
        f"x={x_expr}:"
        f"y={y_expr}:"
        f"enable='between(t,{start_time},{end_time})':"
        f"box=1:"
        f"boxcolor={config.background_color}:"
        f"boxborderw=5"
    )


# ============================================================================
# STORY 3.5: Synchronized Lyrics Display
# ============================================================================

def create_lyrics_overlay_filter(
    lyrics: List[LyricLine],
    config: OverlayConfig = None
) -> str:
    """
    Create FFmpeg filter_complex string for synchronized lyrics overlay.
    
    Story 3.5: Lyrics displayed at correct timestamps
    
    Args:
        lyrics: List of LyricLine objects with timestamps
        config: Overlay configuration
        
    Returns:
        FFmpeg filter_complex string for drawtext filters
    """
    if config is None:
        config = OverlayConfig()
    
    filters = []
    
    # Filter out empty lyrics and skip very short gaps to reduce filter count
    # This helps prevent FFmpeg parsing issues with too many filters
    filtered_lyrics = [lyric for lyric in lyrics if lyric.text and lyric.text.strip()]
    
    # Create drawtext filters for each lyric line
    for i, lyric in enumerate(filtered_lyrics):
        # Calculate position (perfectly centered)
        x_expr = "(w-text_w)/2"  # Center horizontally
        y_expr = "(h-text_h)/2"  # Center vertically (true center)
        
        # Format timestamps to avoid precision issues that could break FFmpeg parsing
        start_time = f"{lyric.start_time:.3f}".rstrip('0').rstrip('.')
        end_time = f"{lyric.end_time:.3f}".rstrip('0').rstrip('.')
        
        # Create drawtext filter for this time range
        # Note: Multiple drawtext filters are comma-separated in FFmpeg
        # Escape text and use double quotes to avoid single quote escaping issues
        escaped_text = _escape_text(lyric.text)
        drawtext_filter = (
            f"drawtext="
            f'text="{escaped_text}":'
            f"fontsize={config.font_size}:"
            f"fontcolor={config.font_color}:"
            f"x={x_expr}:"
            f"y={y_expr}:"
            f"enable=between(t,{start_time},{end_time}):"
            f"box=1:"
            f"boxcolor={config.background_color}:"
            f"boxborderw=5:"
            f"borderw={config.stroke_width}:"
            f"bordercolor={config.stroke_color}"
        )
        
        filters.append(drawtext_filter)
    
    # Combine all filters with commas (FFmpeg supports multiple drawtext filters comma-separated)
    # Each filter must be properly formatted and escaped
    filter_string = ",".join(filters)
    
    # Debug: Log a sample of the filter string to help diagnose issues
    if len(filter_string) > 1000:
        print(f"[Overlay] Filter string length: {len(filter_string)} chars")
        print(f"[Overlay] First 200 chars: {filter_string[:200]}")
        print(f"[Overlay] Last 200 chars: {filter_string[-200:]}")
    
    return filter_string


def _escape_text(text: str) -> str:
    """Escape special characters for FFmpeg drawtext."""
    # Escape backslashes first
    text = text.replace("\\", "\\\\")
    # Escape double quotes (we'll use double quotes to avoid single quote issues)
    text = text.replace('"', '\\"')
    # Escape colons, brackets (single quotes handled by using double quotes for text)
    text = text.replace(":", "\\:")
    text = text.replace("[", "\\[")
    text = text.replace("]", "\\]")
    return text
