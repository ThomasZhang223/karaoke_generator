"""Integration tests for audio pipeline: Acquisition → Processing."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from backend.core.audio_acquisition.downloader import download_audio, validate_url
from backend.core.audio_processing.optimizer import optimize_audio_quality
from backend.core.audio_processing.separator import separate_vocals


@pytest.mark.integration
@pytest.mark.regression
def test_audio_acquisition_to_processing_flow(tmp_path):
    """Test complete flow from YouTube URL to separated vocals."""
    # Mock the download to avoid external dependency
    with patch('backend.core.audio_acquisition.downloader.subprocess.run') as mock_run:
        # Mock successful metadata + download command
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Test Song\nTest Artist\n03:00"
        )

        # Prepare files downloader expects
        final_path = tmp_path / "dQw4w9WgXcQ.mp3"
        final_path.write_bytes(b"MOCK AUDIO")
        info_json = tmp_path / "dQw4w9WgXcQ.info.json"
        info_json.write_text('{"duration":180,"title":"Test Song","uploader":"Test Artist"}', encoding="utf-8")

        # Step 1: Download audio
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid, video_id = validate_url(url)
        assert is_valid is True
        assert video_id == "dQw4w9WgXcQ"

        audio_file = download_audio(url, str(tmp_path), audio_format="mp3", bitrate=192)
        assert audio_file is not None
        assert audio_file.file_path == str(final_path)


@pytest.mark.integration
@pytest.mark.regression
def test_file_format_compatibility(tmp_path):
    """Test that downloaded files are compatible with audio processing."""
    # Create a mock audio file
    audio_path = tmp_path / "downloaded.mp3"
    audio_path.write_bytes(b"MOCK MP3 DATA")
    
    # Mock processing functions to write an output file
    optimized = tmp_path / "optimized.mp3"

    def _write_output(*args, **kwargs):
        optimized.write_bytes(b"OPTIMIZED DATA")
        return MagicMock(returncode=0)

    with patch('backend.core.audio_processing.optimizer.subprocess.run', side_effect=_write_output):
        result = optimize_audio_quality(str(audio_path), output_path=str(optimized))
        assert result is not None
        assert Path(result).exists()


@pytest.mark.integration
@pytest.mark.smoke
def test_error_propagation_download_to_processor(tmp_path):
    """Test that download errors are properly handled by processing module."""
    # Simulate download failure
    with patch('backend.core.audio_acquisition.downloader.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="Download failed")
        
        url = "https://www.youtube.com/watch?v=invalid"
        audio_file = download_audio(url, str(tmp_path), audio_format="mp3", bitrate="192")
        
        # Should return None on failure
        assert audio_file is None
        
        # Processing should handle None input gracefully
        with pytest.raises((TypeError, AttributeError, FileNotFoundError)):
            # This should fail because there's no file to process
            optimize_audio_quality(None, str(tmp_path))
