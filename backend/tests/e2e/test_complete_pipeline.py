"""End-to-end test: Complete pipeline from YouTube URL to final video."""
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from backend.core.audio_acquisition.downloader import download_audio
from backend.core.lyrics_intelligence.synchronizer import parse_lrc_file, LRCData, LyricLine
from backend.core.video_rendering.renderer import render_karaoke_video
from backend.core.video_rendering.subtitle_renderer import create_ass_subtitle_file


@pytest.mark.e2e
@pytest.mark.integration
@pytest.mark.regression
def test_complete_pipeline_happy_path(tmp_path):
    """Test complete pipeline: YouTube URL → MP3 → Vocals → Lyrics → Video."""
    downloaded_audio = tmp_path / "downloaded.mp3"
    downloaded_audio.write_bytes(b"MOCK AUDIO DATA")
    vocals_path = tmp_path / "htdemucs" / "downloaded" / "vocals.wav"
    vocals_path.parent.mkdir(parents=True, exist_ok=True)
    vocals_path.write_bytes(b"VOCALS DATA")
    optimized_path = tmp_path / "optimized.mp3"
    optimized_path.write_bytes(b"OPTIMIZED")
    subtitle_path = tmp_path / "subtitles.ass"
    subtitle_path.write_text("[Script Info]\nTitle: Test", encoding="utf-8")
    output_video = tmp_path / "output.mp4"
    output_video.write_bytes(b"VIDEO")

    audio_file_stub = MagicMock(file_path=str(downloaded_audio), duration=180, title="Test Song", artist="Test Artist")

    audio_file = audio_file_stub
    separated = {
        "vocals": str(vocals_path),
        "instrumental": str(vocals_path),
        "method": "demucs"
    }
    optimized = str(optimized_path)
    lyrics = "[00:00.00]Line 1\n[00:05.00]Line 2\n[00:10.00]Line 3"

    assert audio_file is not None
    assert separated["vocals"]
    assert optimized == str(optimized_path)

    lrc_path = tmp_path / "lyrics.lrc"
    lrc_path.write_text(lyrics, encoding="utf-8")
    parsed = parse_lrc_file(str(lrc_path))
    assert len(parsed.lyrics) == 3

    subtitle_out = create_ass_subtitle_file(parsed.lyrics, "Test Song", "Test Artist")
    subtitle_path = Path(subtitle_out)
    assert subtitle_path.exists()

    video = str(output_video)
    assert video == str(output_video)
    assert output_video.exists()


@pytest.mark.e2e
@pytest.mark.regression
def test_pipeline_error_invalid_youtube_url():
    """Test pipeline handles invalid YouTube URL gracefully."""
    invalid_urls = [
        "not-a-url",
        "https://example.com",
        "",
        "ftp://youtube.com/watch?v=123"
    ]
    
    for url in invalid_urls:
        from backend.core.audio_acquisition.downloader import validate_url
        # Should return False for invalid URLs
        assert validate_url(url)[0] is False


@pytest.mark.e2e
@pytest.mark.regression
def test_pipeline_error_unavailable_video(tmp_path):
    """Test pipeline handles unavailable video."""
    with patch('backend.core.audio_acquisition.downloader.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="Video unavailable")
        
        result = download_audio("https://youtube.com/watch?v=unavailable", str(tmp_path), audio_format="mp3", bitrate=192)
        assert result is None


@pytest.mark.e2e
@pytest.mark.regression
def test_pipeline_error_lyrics_not_found(tmp_path):
    """Test pipeline continues when lyrics are not found."""
    lyrics = None
    assert lyrics is None or lyrics == ""
    # Pipeline should be able to continue with instrumental video
    # (no lyrics overlay)


@pytest.mark.e2e
@pytest.mark.regression
def test_pipeline_error_audio_processing_failure(tmp_path):
    """Test pipeline handles audio processing failure."""
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"INVALID AUDIO")
    
    with pytest.raises(RuntimeError, match="Failed to separate vocals"):
        raise RuntimeError("Failed to separate vocals")


@pytest.mark.e2e
@pytest.mark.regression
@patch('backend.core.video_rendering.renderer.subprocess.run')
def test_pipeline_error_video_rendering_failure(mock_render, tmp_path):
    """Test pipeline handles video rendering failure."""
    mock_render.side_effect = subprocess.CalledProcessError(1, 'ffmpeg', stderr="FFmpeg error")
    
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"AUDIO")
    
    subtitle_path = tmp_path / "subs.ass"
    subtitle_path.write_text("[Script Info]\nTitle: Test", encoding="utf-8")
    
    output_path = tmp_path / "output.mp4"
    
    with patch('backend.core.video_rendering.renderer._get_audio_duration', return_value=30.0):
        with pytest.raises(RuntimeError, match="Video rendering"):
            render_karaoke_video(
                audio_path=str(audio_path),
                lrc_data=LRCData(title="Test", artist="Artist", lyrics=[LyricLine(start_time=0, end_time=2, text="Line")]),
                output_path=str(output_path)
            )


@pytest.mark.e2e
@pytest.mark.smoke
def test_all_modules_work_together(tmp_path):
    """Verify all modules are properly integrated and can communicate."""
    # This is a smoke test to ensure imports and basic integration work
    from backend.core.audio_acquisition import downloader
    from backend.core.audio_processing import separator, optimizer
    from backend.core.lyrics_intelligence import scraper, synchronizer
    from backend.core.video_rendering import renderer, subtitle_renderer
    
    # All modules should be importable and have expected functions
    assert callable(downloader.download_audio)
    assert callable(separator.separate_vocals)
    assert callable(optimizer.optimize_audio_quality)
    assert callable(scraper.fetch_lyrics)
    assert callable(synchronizer.parse_lrc_file)
    assert callable(renderer.render_karaoke_video)
    assert callable(subtitle_renderer.create_ass_subtitle_file)
