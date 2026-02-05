# Test Fixtures

This directory contains sample data for testing:

## Sample YouTube URLs (test_urls.txt)
- Standard YouTube URL
- Short YouTube URL (youtu.be)
- Playlist URL
- Invalid URLs for error testing

## Sample LRC Files
- `valid_lrc.lrc`: Valid LRC with timestamps
- `metadata_lrc.lrc`: LRC with metadata tags
- `missing_timestamps.lrc`: LRC with missing timestamps
- `out_of_order.lrc`: LRC with out-of-order timestamps

## Sample Audio Files (Not included - too large)
For local testing, place small audio files here:
- `short_song.mp3` (1 minute)
- `medium_song.mp3` (3 minutes)
- `long_song.mp3` (5 minutes)

## Notes
- Audio files are excluded from git (.gitignore)
- Tests use mocked data to avoid external dependencies
- Real audio files only needed for manual integration testing
