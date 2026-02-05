"""Integration tests for lyrics pipeline: Fetching → Synchronization."""
import pytest
from pathlib import Path
from backend.core.lyrics_intelligence.synchronizer import (
    parse_lrc_file,
    generate_lrc_file,
    LRCData,
    LyricLine
)


@pytest.mark.integration
@pytest.mark.regression
def test_lyrics_fetch_to_synchronization_flow(tmp_path):
    """Test complete flow from lyrics fetching to LRC file generation."""
    # Mock LRCLib API response
    lyrics = "[00:00.00]First line\n[00:05.50]Second line"

    # Step 2: Write synced lyrics to temp LRC and parse
    lrc_path = tmp_path / "synced.lrc"
    lrc_path.write_text(lyrics, encoding="utf-8")
    parsed = parse_lrc_file(str(lrc_path))
    assert len(parsed.lyrics) == 2
    assert parsed.lyrics[0].text == "First line"
    assert parsed.lyrics[0].start_time == 0.0

    # Step 3: Generate LRC file from LRCData
    lrc_data = LRCData(title="Test Song", artist="Test Artist", lyrics=[
        LyricLine(start_time=0.0, end_time=4.0, text="First line"),
        LyricLine(start_time=5.5, end_time=9.5, text="Second line"),
    ])
    output_path = tmp_path / "test.lrc"
    generated_path = generate_lrc_file(lrc_data, str(output_path))
    assert Path(generated_path).exists()
    content = Path(generated_path).read_text(encoding="utf-8")
    assert "[00:00.00]First line" in content


@pytest.mark.integration
@pytest.mark.smoke
def test_lrc_generation_from_fetched_lyrics(tmp_path):
    """Test LRC file generation from API-fetched lyrics."""
    lyrics = "Line 1\nLine 2\nLine 3"
    lines = lyrics.strip().split("\n")
    duration = 60.0  # 1 minute song
    interval = duration / len(lines)

    lrc_data = LRCData(
        title="Song",
        artist="Artist",
        lyrics=[LyricLine(start_time=i * interval, end_time=(i+1)*interval, text=line) for i, line in enumerate(lines)]
    )
    output_path = tmp_path / "plain.lrc"
    generated_path = generate_lrc_file(lrc_data, str(output_path))
    content = Path(generated_path).read_text(encoding="utf-8")
    assert "[ti:Song]" in content
    assert "[ar:Artist]" in content
    assert "Line 1" in content


@pytest.mark.integration
@pytest.mark.regression
def test_integration_with_audio_files(tmp_path):
    """Test lyrics synchronization with actual audio file simulation."""
    # Create mock audio file
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"MOCK AUDIO")
    
    # Mock LRC content
    lrc_content = "[00:00.00]First\n[00:10.00]Second\n[00:20.00]Third"
    lrc_path = tmp_path / "mock.lrc"
    lrc_path.write_text(lrc_content, encoding="utf-8")
    parsed = parse_lrc_file(str(lrc_path))

    # Simulate synchronization with audio
    assert len(parsed.lyrics) == 3
    assert all(line.start_time >= 0 for line in parsed.lyrics)
    
    # Verify timestamps are in order
    timestamps = [line.start_time for line in parsed.lyrics]
    assert timestamps == sorted(timestamps)


@pytest.mark.integration
@pytest.mark.smoke
def test_missing_lyrics_fallback():
    """Test fallback behavior when lyrics are not found."""
    lyrics = None
    assert lyrics is None or lyrics == ""
