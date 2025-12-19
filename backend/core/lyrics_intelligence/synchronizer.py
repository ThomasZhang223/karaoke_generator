import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass



@dataclass
class LyricLine:
    """Represents a single line of lyrics with timestamp."""
    start_time: float  # in seconds
    end_time: float    # in seconds
    text: str
    line_number: int = 0


@dataclass
class LRCData:
    """Represents LRC file data with metadata and lyrics."""
    title: str = ""
    artist: str = ""
    album: str = ""
    offset: int = 0  # Offset in milliseconds
    lyrics: List[LyricLine] = None
    
    def __post_init__(self):
        if self.lyrics is None:
            self.lyrics = []


def parse_lrc_file(lrc_path: str) -> LRCData:
    """
    Parse an LRC file into structured data.
    
    Story 2.5: LRC file parser implemented
    
    Args:
        lrc_path: Path to LRC file
        
    Returns:
        LRCData object with parsed lyrics and metadata
        
    Raises:
        FileNotFoundError: If LRC file doesn't exist
        ValueError: If LRC file format is invalid
    """
    lrc_file = Path(lrc_path)
    if not lrc_file.exists():
        raise FileNotFoundError(f"LRC file not found: {lrc_path}")
    
    data = LRCData()
    lyrics = []
    
    # Regex patterns for LRC format
    # Support [MM:SS.mm], [MM:SS:mmm], and [MM:SS.mmm] formats
    # Examples: [00:14.43], [01:23:456], [02:45.123]
    # Match either . or : as separator (character class [.:] works, but need to escape .)
    time_tag_pattern = re.compile(r'\[(\d{1,2}):(\d{2})[\.:](\d{2,3})\]')
    metadata_pattern = re.compile(r'\[(\w+):(.+)\]')
    
    lines_processed = 0
    lines_with_timestamps = 0
    
    print(f"[Lyrics] parse_lrc_file: Opening {lrc_file}")
    
    with open(lrc_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
        print(f"[Lyrics] parse_lrc_file: Read {len(file_content)} chars, {len(file_content.splitlines())} lines")
        # Show first few lines
        first_lines = file_content.splitlines()[:5]
        for i, line in enumerate(first_lines):
            print(f"[Lyrics] parse_lrc_file: Line {i+1}: '{line[:60]}'")
    
    with open(lrc_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            original_line = line
            line = line.strip()
            if not line:
                continue
            
            lines_processed += 1
            
            # Check for metadata tags FIRST (but only if it's not a timestamp line)
            # Metadata tags are like [ti:Title] or [ar:Artist], NOT [00:14.43]
            # Timestamp lines start with [MM:SS...] where MM is digits
            # Metadata lines start with [word:...] where word is letters only
            if line.startswith('[') and ':' in line:
                # Check if it looks like a timestamp (starts with digits) vs metadata (starts with letters)
                after_bracket = line[1:].split(':', 1)
                if len(after_bracket) == 2:
                    first_part = after_bracket[0]
                    # If first part is all digits, it's a timestamp, skip metadata check
                    if first_part.isdigit():
                        pass  # It's a timestamp, continue to timestamp parsing
                    else:
                        # It might be metadata, try to match
                        metadata_match = metadata_pattern.match(line)
                        if metadata_match:
                            tag, value = metadata_match.groups()
                            if tag.lower() == 'ti':
                                data.title = value
                            elif tag.lower() == 'ar':
                                data.artist = value
                            elif tag.lower() == 'al':
                                data.album = value
                            elif tag.lower() == 'offset':
                                try:
                                    data.offset = int(value)  # Offset in milliseconds
                                    print(f"[Lyrics] LRC file has offset: {data.offset}ms ({data.offset/1000:.2f}s)")
                                except ValueError:
                                    print(f"[Lyrics] ⚠ Invalid offset value: {value}")
                            continue
            
            # Extract all timestamps from line
            time_matches = list(time_tag_pattern.finditer(line))
            if not time_matches:
                # Debug: show first few non-matching lines to understand format
                if lines_processed <= 10:
                    print(f"[Lyrics] DEBUG: Line {line_num} doesn't match time pattern: '{line[:80]}'")
                    # Test the regex manually
                    test_match = time_tag_pattern.search(line)
                    if test_match:
                        print(f"[Lyrics] DEBUG: But regex.search found: {test_match.groups()}")
                    else:
                        print(f"[Lyrics] DEBUG: Regex pattern: {time_tag_pattern.pattern}")
                continue
            
            lines_with_timestamps += 1
            
            # Get text (everything after last timestamp)
            last_match = time_matches[-1]
            text = line[last_match.end():].strip()
            
            if not text:
                if lines_with_timestamps <= 3:
                    print(f"[Lyrics] DEBUG: Line {line_num} has timestamp but no text: '{line[:80]}'")
                continue
            
            # Debug: show first few parsed lines
            if lines_with_timestamps <= 3:
                first_match = time_matches[0]
                minutes, seconds, milliseconds = first_match.groups()
                # Get the separator from the match string
                match_str = first_match.group(0)
                separator = '.' if '.' in match_str else ':'
                print(f"[Lyrics] DEBUG: Parsed line {line_num}: '{text[:40]}...' at [{minutes}:{seconds}{separator}{milliseconds}]")
            
            # Create lyric line for each timestamp
            for match in time_matches:
                minutes, seconds, milliseconds = match.groups()
                # Get the separator from the match string
                match_str = match.group(0)
                separator = '.' if '.' in match_str else ':'
                
                # Handle both . and : as separator, and 2 or 3 digit milliseconds
                if separator == '.':
                    # [MM:SS.mm] or [MM:SS.mmm] format
                    if len(milliseconds) == 2:
                        # Hundredths of a second (e.g., [00:14.43] = 14.43 seconds)
                        total_seconds = (
                            int(minutes) * 60 + 
                            int(seconds) + 
                            int(milliseconds) / 100.0
                        )
                    else:
                        # Thousandths of a second (e.g., [00:14.430] = 14.430 seconds)
                        total_seconds = (
                            int(minutes) * 60 + 
                            int(seconds) + 
                            int(milliseconds) / 1000.0
                        )
                else:  # separator == ':'
                    # [MM:SS:mmm] format - milliseconds are in thousandths
                    total_seconds = (
                        int(minutes) * 60 + 
                        int(seconds) + 
                        int(milliseconds) / 1000.0
                    )
                
                lyrics.append(LyricLine(
                    start_time=total_seconds,
                    end_time=total_seconds,  # Will be updated by synchronization
                    text=text,
                    line_number=line_num
                ))
    
    
    # Sort by timestamp
    lyrics.sort(key=lambda x: x.start_time)
    
    # Apply offset if present (convert from milliseconds to seconds)
    # Note: LRC offset is usually negative (subtract from timestamps)
    if data.offset != 0:
        offset_seconds = data.offset / 1000.0
        print(f"[Lyrics] LRC file has offset: {data.offset}ms ({offset_seconds:.2f}s)")
        print(f"[Lyrics] Applying offset to {len(lyrics)} lyric lines")
        for lyric in lyrics:
            lyric.start_time += offset_seconds
            lyric.end_time += offset_seconds
    
    # Set end_time to start of next line (or estimate)
    for i in range(len(lyrics) - 1):
        lyrics[i].end_time = lyrics[i + 1].start_time
    
    # Last line: estimate duration (4 seconds or until end)
    if lyrics:
        lyrics[-1].end_time = lyrics[-1].start_time + 4.0
    
    data.lyrics = lyrics
    return data


def generate_lrc_file(
    lrc_data: LRCData,
    output_path: str
) -> str:
    """
    Generate an LRC file from LRCData.
    
    Story 2.5: LRC file generator implemented
    
    Args:
        lrc_data: LRCData object with lyrics and metadata
        output_path: Path where LRC file will be written
        
    Returns:
        Path to generated LRC file
        
    Raises:
        ValueError: If LRC data is invalid
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write metadata
        if lrc_data.title:
            f.write(f"[ti:{lrc_data.title}]\n")
        if lrc_data.artist:
            f.write(f"[ar:{lrc_data.artist}]\n")
        if lrc_data.album:
            f.write(f"[al:{lrc_data.album}]\n")
        if lrc_data.offset != 0:
            f.write(f"[offset:{lrc_data.offset}]\n")
        
        f.write("\n")
        
        # Write lyrics with timestamps
        for lyric in lrc_data.lyrics:
            # Format: [mm:ss.ff] text
            minutes = int(lyric.start_time // 60)
            seconds = int(lyric.start_time % 60)
            centiseconds = int((lyric.start_time % 1) * 100)
            
            timestamp = f"[{minutes:02d}:{seconds:02d}.{centiseconds:02d}]"
            f.write(f"{timestamp}{lyric.text}\n")
    
    return str(output_file.absolute())

