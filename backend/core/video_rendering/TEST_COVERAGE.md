# Test Coverage for Long Song Rendering

## Overview

The test suite in `test_long_song_rendering.py` covers all errors and edge cases we encountered during debugging the 4+ minute song rendering issue.

## Test Cases

### ✅ 1. Subtitle File Generation
**What it tests:** Basic ASS subtitle file creation with proper formatting
- Verifies file is created correctly
- Checks for required ASS format sections (Script Info, Styles, Events)
- Validates lyrics are included
- Tests with problematic timestamp (46.35)
- Includes title and artist

### ✅ 2. Subtitle Filter Building  
**What it tests:** FFmpeg subtitle filter string generation
- Verifies filter syntax is correct
- Checks for proper escaping
- Validates filter parameters

### ✅ 3. Drawtext with Problematic Timestamp
**What it tests:** The exact error that caused failures - timestamp 46.35
- Tests drawtext filter generation with the problematic timestamp
- Verifies timestamp format doesn't break FFmpeg parsing
- Checks quote balancing

### ✅ 4. Apostrophe Handling
**What it tests:** Lyrics with apostrophes (We'll, Don't, It's, etc.)
- Ensures apostrophes don't break filter syntax
- Verifies proper quote escaping
- Tests multiple apostrophes in different lyrics

### ✅ 5. Long Song Detection (20+ Lyrics)
**What it tests:** Automatic switching to subtitle approach
- Creates 25 lyrics (triggers subtitle approach)
- Verifies all lyrics are included in subtitle file
- Checks dialogue entry count

### ✅ 6. Real 4-Minute Song Data
**What it tests:** The actual failing song data
- Uses real lyrics from "(Only) About Love" by grentperez
- 28 lyrics (triggers subtitle approach)
- Includes all problematic timestamps (46.35, 91.22, 245.35)
- Tests with apostrophes (We'll, won't, let's)
- Verifies subtitle file and filter generation

### ✅ 7. FFmpeg Subtitle Parsing
**What it tests:** FFmpeg can parse the generated filter
- Validates filter syntax
- Checks for balanced quotes
- Verifies filter structure

### ✅ 8. Empty Lyrics Handling
**What it tests:** Empty or whitespace-only lyrics
- Filters out empty lyrics
- Handles whitespace-only text
- Only includes valid lyrics

### ✅ 9. Filter Length Scaling
**What it tests:** Efficiency comparison
- Compares drawtext approach (short songs) vs subtitles (long songs)
- Verifies subtitle approach is more efficient for 20+ lyrics
- Shows filter length differences

## Errors Covered

1. **"No such filter: '46.35'"** - Fixed by using subtitle approach for long songs
2. **"No option name near '42:fontcolor..."** - Fixed by avoiding long filter chains
3. **Quote escaping issues** - Fixed by using double quotes and proper escaping
4. **Apostrophe parsing errors** - Fixed by proper text escaping in subtitle files
5. **Very long filter chains** - Fixed by switching to subtitles for 20+ lyrics

## Running the Tests

```bash
python -m backend.core.video_rendering.test_long_song_rendering
```

## Expected Results

All 9 tests should pass. If any fail, it indicates a regression in the fix.

## Key Insights

- **Subtitle approach is more reliable** for songs with 20+ lyrics
- **Drawtext works fine** for shorter songs (<20 lyrics)
- **ASS subtitle format** handles all edge cases (apostrophes, timestamps, etc.)
- **No chunking needed** with subtitle approach - FFmpeg handles it natively

