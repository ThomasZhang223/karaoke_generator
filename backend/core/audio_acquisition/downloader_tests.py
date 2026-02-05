# ==============================================================================
# ==============================================================================
#                        DOWNLOADER UNIT TESTS
# ==============================================================================
# ==============================================================================
#
# Sprint 4 - Story 4.4: Documentation & Code Quality (Thomas)
# Sprint 4 - Story 4.6: Final QA & Testing (Thomas)
#
# ==============================================================================

"""
Unit Tests for YouTube Audio Downloader

Run with: python downloader_tests.py
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil

from downloader import download_audio, validate_url, AudioFile, Status


# ==============================================================================
# SPRINT 4 - THOMAS
# Story 4.4: Documentation & Code Quality
# Story 4.6: Final QA & Testing
# - Unit tests for audio acquisition module
# - Test cases cover all major features
# - Edge cases tested
# ==============================================================================


class TestValidateUrl:
    """Tests for URL validation."""
    
    def test_valid_urls(self):
        """Test valid YouTube URL formats."""
        valid_urls = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?v=abc123XYZ_-&list=PLtest", "abc123XYZ_-"),
        ]
        for url, expected_id in valid_urls:
            valid, video_id = validate_url(url)
            assert valid is True
            assert video_id == expected_id
    
    def test_invalid_urls(self):
        """Test invalid URLs return False."""
        invalid_urls = ["https://vimeo.com/123", "not a url", ""]
        for url in invalid_urls:
            valid, video_id = validate_url(url)
            assert valid is False
            assert video_id is None


class TestDownloadAudio:
    """Tests for download_audio function."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temp directory, cleanup after test."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp, ignore_errors=True)
    
    def test_invalid_url_returns_none(self, temp_dir):
        """Invalid URL should return None."""
        result = download_audio("https://invalid.com/video", temp_dir, "mp3", 128)
        assert result is None
    
    @patch("downloader.subprocess.run")
    def test_successful_download(self, mock_run, temp_dir):
        """Test successful download returns AudioFile."""
        video_id = "dQw4w9WgXcQ"
        
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=json.dumps({
                "duration_string": "3:32",
                "filesize_approx": 5000000,
            })),
            MagicMock(returncode=0),
        ]
        
        # Create fake downloaded file
        Path(temp_dir, f"{video_id}.mp3").write_text("fake")
        
        result = download_audio(
            f"https://www.youtube.com/watch?v={video_id}",
            temp_dir, "mp3", 128
        )
        
        assert result is not None
        assert result.id == video_id
        assert result.duration == 212  # 3*60 + 32
        assert result.status == Status.DOWNLOADED
    
    @patch("downloader.subprocess.run")
    def test_download_failure_returns_none(self, mock_run, temp_dir):
        """Failed download should return None."""
        mock_run.return_value = MagicMock(returncode=1, stderr="Error")
        
        result = download_audio(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            temp_dir, "mp3", 128
        )
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ==============================================================================
# END OF SPRINT 4 - THOMAS
# ==============================================================================