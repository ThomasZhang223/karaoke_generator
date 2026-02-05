# ==============================================================================
# ==============================================================================
#                        TITLE NORMALIZER MODULE
# ==============================================================================
# ==============================================================================
#
# Sprint 2 - Story 2.4: Lyrics Fetching Implementation (Aruhant)
#           Song title and artist matching logic
#
# ==============================================================================

"""
Title normalization utility for lyrics search.
Removes common YouTube video tags and suffixes that interfere with lyrics search.

Examples:
- "Song Name (audio)" -> "Song Name"
- "Song Name (Official Video)" -> "Song Name"
- "Song Name [Lyric Video]" -> "Song Name"
- "Artist - Song Name (Lyrics)" -> "Song Name"
"""

import re
from typing import Tuple, Optional


# ==============================================================================
# SPRINT 2 - ARUHANT
# Story 2.4: Lyrics Fetching Implementation
# - Song title and artist matching logic
# - Clean and normalize YouTube video titles for lyrics search
# ==============================================================================

# Common patterns to remove from YouTube video titles
# These are often added to video titles but shouldn't be in lyrics searches
COMMON_VIDEO_TAGS = [
    r'\(audio\)',
    r'\(Audio\)',
    r'\(AUDIO\)',
    r'\(video\)',
    r'\(Video\)',
    r'\(VIDEO\)',
    r'\(official audio\)',
    r'\(Official Audio\)',
    r'\(OFFICIAL AUDIO\)',
    r'\(official video\)',
    r'\(Official Video\)',
    r'\(OFFICIAL VIDEO\)',
    r'\(lyric video\)',
    r'\(Lyric Video\)',
    r'\(LYRIC VIDEO\)',
    r'\(lyrics\)',
    r'\(Lyrics\)',
    r'\(LYRICS\)',
    r'\(with lyrics\)',
    r'\(With Lyrics\)',
    r'\(WITH LYRICS\)',
    r'\[audio\]',
    r'\[Audio\]',
    r'\[AUDIO\]',
    r'\[video\]',
    r'\[Video\]',
    r'\[VIDEO\]',
    r'\[official audio\]',
    r'\[Official Audio\]',
    r'\[OFFICIAL AUDIO\]',
    r'\[official video\]',
    r'\[Official Video\]',
    r'\[OFFICIAL VIDEO\]',
    r'\[lyric video\]',
    r'\[Lyric Video\]',
    r'\[LYRIC VIDEO\]',
    r'\[lyrics\]',
    r'\[Lyrics\]',
    r'\[LYRICS\]',
    r'\[with lyrics\]',
    r'\[With Lyrics\]',
    r'\[WITH LYRICS\]',
    # Remove common separators and extra info
    r' - (Official|Lyrics|Audio|Video).*$',  # "Song - Official Video"
    r' \| (Official|Lyrics|Audio|Video).*$',  # "Song | Official Video"
    r' HD$',  # "Song HD"
    r' 4K$',  # "Song 4K"
    r' HQ$',  # "Song HQ"
]


def normalize_title(title: str) -> str:
    """
    Clean and normalize a YouTube video title for lyrics search.
    
    Removes common video tags, suffixes, and formatting that interfere
    with finding the actual song lyrics.
    
    Args:
        title: Raw video title from YouTube
        
    Returns:
        Cleaned title suitable for lyrics search
        
    Examples:
        >>> normalize_title("Song Name (audio)")
        'Song Name'
        >>> normalize_title("Artist - Song Name [Official Video]")
        'Artist - Song Name'
        >>> normalize_title("Song Name (Official Audio)")
        'Song Name'
    """
    if not title:
        return ""
    
    cleaned = title.strip()
    
    # Remove common video tags (case-insensitive)
    for pattern in COMMON_VIDEO_TAGS:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single space
    cleaned = cleaned.strip()
    
    # Remove trailing/leading punctuation that might be left behind
    cleaned = re.sub(r'^[\s\-|:]+|[\s\-|:]+$', '', cleaned)
    
    return cleaned.strip()


def normalize_artist(artist: str) -> str:
    """
    Clean and normalize artist name.
    
    Removes common prefixes/suffixes that might interfere with search.
    
    Args:
        artist: Raw artist name
        
    Returns:
        Cleaned artist name
    """
    if not artist:
        return ""
    
    cleaned = artist.strip()
    
    # Remove common prefixes/suffixes
    # "Artist - Topic" -> "Artist"
    cleaned = re.sub(r'\s*-\s*Topic\s*$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s*-\s*VEVO\s*$', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()


def normalize_title_and_artist(title: Optional[str], artist: Optional[str]) -> Tuple[str, str]:
    """
    Normalize both title and artist for lyrics search.
    
    Args:
        title: Raw video title
        artist: Raw artist name
        
    Returns:
        Tuple of (normalized_title, normalized_artist)
    """
    normalized_title = normalize_title(title or "")
    normalized_artist = normalize_artist(artist or "")
    
    return normalized_title, normalized_artist


# Test the function if run directly
if __name__ == "__main__":
    test_cases = [
        ("Song Name (audio)", "Song Name"),
        ("Song Name (Official Video)", "Song Name"),
        ("Artist - Song Name [Lyric Video]", "Artist - Song Name"),
        ("Song Name (Official Audio)", "Song Name"),
        ("Song Name - Official Video", "Song Name"),
        ("Song Name | Lyrics", "Song Name"),
        ("Song Name HD", "Song Name"),
        ("Artist - Song Name (audio)", "Artist - Song Name"),
        ("[Audio] Song Name", "Song Name"),
        ("Song Name (with lyrics)", "Song Name"),
    ]
    
    print("Testing title normalization:")
    for original, expected in test_cases:
        result = normalize_title(original)
        status = "[PASS]" if result == expected else "[FAIL]"
        print(f"  {status} '{original}' -> '{result}' (expected: '{expected}')")

# ==============================================================================
# END OF SPRINT 2 - ARUHANT
# ==============================================================================

