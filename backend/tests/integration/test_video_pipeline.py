"""Integration tests for video rendering pipeline: LRC → Video."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from backend.core.lyrics_intelligence.synchronizer import parse_lrc_file, LRCData, LyricLine
from backend.core.video_rendering.renderer import render_karaoke_video
from backend.core.video_rendering.subtitle_renderer import create_ass_subtitle_file


@pytest.mark.integration
@pytest.mark.regression
def test_lrc_to_video_integration(tmp_path):
    """Test complete flow from LRC parsing to video rendering."""
    # Create mock LRC file
    lrc_content = """[ti:Test Song]
[ar:Test Artist]
[00:00.00]First line of lyrics
[00:05.50]Second line here
[00:10.00]Third line now
"""
    lrc_path = tmp_path / "test.lrc"
    lrc_path.write_text(lrc_content, encoding="utf-8")
    
    # Parse LRC
    lrc_path = tmp_path / "test.lrc"
    lrc_path.write_text(lrc_content, encoding="utf-8")
    parsed_data = parse_lrc_file(str(lrc_path))
    assert len(parsed_data.lyrics) == 3
    
    # Create ASS subtitle file
    ass_path = tmp_path / "subtitles.ass"
    ass_generated = create_ass_subtitle_file(parsed_data.lyrics, "Test Song", "Test Artist")
    Path(ass_generated).rename(ass_path)
    assert ass_path.exists()
    
    # Verify ASS content
    ass_content = ass_path.read_text(encoding="utf-8")
    assert "[Script Info]" in ass_content
    assert "First line of lyrics" in ass_content


@pytest.mark.integration
@pytest.mark.smoke  
def test_lyrics_appear_at_correct_times(tmp_path):
    """Verify timestamps are correctly converted for video rendering."""
    # LRC with specific timestamps
    lyrics = [
        LyricLine(start_time=0.0, end_time=4.0, text="Start"),
        LyricLine(start_time=10.5, end_time=14.5, text="Middle"),
        LyricLine(start_time=20.0, end_time=24.0, text="End"),
    ]
    ass_path = tmp_path / "timing.ass"
    ass_generated = create_ass_subtitle_file(lyrics, "Song", "Artist")
    Path(ass_generated).rename(ass_path)
    content = ass_path.read_text(encoding="utf-8")
    
    # Check that timestamps are formatted correctly (HH:MM:SS.cs)
    assert "0:00:00.00" in content  # Start at 0
    assert "0:00:10.50" in content  # Middle at 10.5s
    assert "0:00:20.00" in content  # End at 20s


@pytest.mark.integration
@pytest.mark.regression
@patch('backend.core.video_rendering.renderer.subprocess.run')
def test_video_rendering_with_subtitles(mock_run, tmp_path):
    """Test video rendering with subtitle file integration."""
    mock_run.return_value = MagicMock(returncode=0)
    
    # Create mock audio file
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"MOCK AUDIO")
    
    # Create subtitle file data
    lyrics = [
        LyricLine(start_time=0.0, end_time=3.0, text="Line 1"),
        LyricLine(start_time=5.0, end_time=8.0, text="Line 2"),
    ]
    lrc_data = LRCData(title="Title", artist="Artist", lyrics=lyrics)
    
    output_path = tmp_path / "output.mp4"
    
    def _fake_render(cmd, *args, **kwargs):
        output_path.write_bytes(b"VIDEO")
        return MagicMock(returncode=0)

    mock_run.side_effect = _fake_render

    with patch('backend.core.video_rendering.renderer._get_audio_duration', return_value=30.0):
        # Render video with subtitles using LRCData
        result = render_karaoke_video(
            audio_path=str(audio_path),
            lrc_data=lrc_data,
            output_path=str(output_path)
        )
        
        assert mock_run.called
        # Verify ffmpeg command constructed and output path returned
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "ffmpeg"
        assert result == str(output_path)


@pytest.mark.integration
@pytest.mark.regression
def test_special_characters_in_lyrics(tmp_path):
    """Test that special characters in lyrics are properly escaped for video."""
    lyrics_with_special_chars = [
        LyricLine(start_time=0.0, end_time=3.0, text="It's a quote: 'Hello'"),
        LyricLine(start_time=5.0, end_time=8.0, text="Symbols: @#$%"),
        LyricLine(start_time=10.0, end_time=14.0, text="Unicode: 你好"),
    ]
    
    ass_generated = create_ass_subtitle_file(lyrics_with_special_chars, "Test", "Artist")
    ass_path = tmp_path / "special.ass"
    Path(ass_generated).rename(ass_path)
    
    content = ass_path.read_text(encoding="utf-8")
    # All text should be present in some form
    assert "Hello" in content
    assert "Symbols" in content
    assert "你好" in content
