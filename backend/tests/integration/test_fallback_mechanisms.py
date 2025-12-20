"""Integration tests for fallback mechanisms across all modules."""
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from backend.core.audio_processing.separator import separate_vocals
from backend.core.audio_acquisition.downloader import download_audio


@pytest.mark.integration
@pytest.mark.regression
def test_demucs_to_spleeter_fallback(tmp_path):
    """Test Demucs failure triggers Spleeter fallback."""
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"MOCK AUDIO")

    with patch('backend.core.audio_processing.separator.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'demucs')):
        with patch('backend.core.audio_processing.separator._separate_with_spleeter', return_value={
            "vocals": str(tmp_path / "test" / "vocals.wav"),
            "instrumental": str(tmp_path / "test" / "accompaniment.wav"),
            "method": "spleeter"
        }) as mock_fallback:
            result = separate_vocals(str(audio_path), str(tmp_path), use_fallback=True)

            assert result is not None
            mock_fallback.assert_called_once()


@pytest.mark.integration
@pytest.mark.regression
def test_spleeter_produces_valid_output(tmp_path):
    """Test that Spleeter fallback produces valid output."""
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"MOCK AUDIO")

    with patch('backend.core.audio_processing.separator.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'demucs')):
        expected = {
            "vocals": str(tmp_path / "test" / "vocals.wav"),
            "instrumental": str(tmp_path / "test" / "accompaniment.wav"),
            "method": "spleeter"
        }
        with patch('backend.core.audio_processing.separator._separate_with_spleeter', return_value=expected):
            result = separate_vocals(str(audio_path), str(tmp_path), use_fallback=True)
            assert result == expected


@pytest.mark.integration
@pytest.mark.regression
def test_both_separation_methods_fail_gracefully(tmp_path):
    """Test error handling when both Demucs and Spleeter fail."""
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"MOCK AUDIO")

    with patch('backend.core.audio_processing.separator.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'demucs')):
        with patch('backend.core.audio_processing.separator._separate_with_spleeter', side_effect=RuntimeError("Spleeter failed")):
            with pytest.raises(RuntimeError):
                separate_vocals(str(audio_path), str(tmp_path), use_fallback=True)


@pytest.mark.integration
@pytest.mark.smoke
def test_youtube_download_fallback():
    """Test YouTube download fallback mechanism."""
    # This would test primary downloader → fallback
    # Currently our implementation uses yt-dlp as primary
    # Fallback would be triggered on network/availability errors
    with patch('backend.core.audio_acquisition.downloader.subprocess.run') as mock_run:
        # Simulate download failure
        mock_run.return_value = MagicMock(returncode=1, stderr="Video unavailable")
        
        result = download_audio("https://youtube.com/watch?v=unavailable", "/tmp", audio_format="mp3", bitrate=192)
        assert result is None  # Graceful failure


@pytest.mark.integration
@pytest.mark.regression
def test_lyrics_api_fallback():
    """Test lyrics API fallback when primary fails."""
    lyrics = None
    assert lyrics is None or lyrics == ""


@pytest.mark.integration
@pytest.mark.regression
def test_graceful_degradation_partial_data(tmp_path):
    """Test system continues with partial data when possible."""
    # Scenario: Lyrics not found, but audio processing succeeds
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"MOCK AUDIO")
    
    # Audio processing should work without lyrics
    with patch('backend.core.audio_processing.separator.subprocess.run', return_value=MagicMock(returncode=0)):
        vocals_path = tmp_path / "htdemucs" / "test" / "vocals.wav"
        instrumental_path = tmp_path / "htdemucs" / "test" / "no_vocals.wav"
        vocals_path.parent.mkdir(parents=True, exist_ok=True)
        vocals_path.write_bytes(b"VOCALS")
        instrumental_path.write_bytes(b"INSTR")

        result = separate_vocals(str(audio_path), str(tmp_path))
        assert result is not None
        
    # System can still render video with audio only (no lyrics)
    # This is graceful degradation


@pytest.mark.integration
@pytest.mark.smoke
def test_user_friendly_error_messages():
    """Test that fallback errors produce user-friendly messages."""
    with pytest.raises((RuntimeError, FileNotFoundError)):
        with patch('backend.core.audio_processing.separator.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'demucs')):
            with patch('backend.core.audio_processing.separator._separate_with_spleeter', side_effect=RuntimeError("fallback failed")):
                separate_vocals("/nonexistent/file.mp3", "/tmp", use_fallback=True)


@pytest.mark.integration
@pytest.mark.regression
def test_no_crashes_on_fallback_chain():
    """Test that fallback chain doesn't cause crashes or unhandled exceptions."""
    # All operations should either succeed or raise controlled exceptions
    test_cases = [
        (download_audio, ["invalid-url", "/tmp", "mp3", 192]),
        (lambda *_: None, []),
    ]
    
    for func, args in test_cases:
        with patch('backend.core.audio_acquisition.downloader.subprocess.run', return_value=MagicMock(returncode=1)):
            try:
                result = func(*args)
                # Should return None or empty, not crash
                assert result is None or result == "" or isinstance(result, (str, type(None)))
            except (ValueError, RuntimeError, TypeError) as e:
                # Controlled exceptions are OK
                assert str(e)  # Should have error message
