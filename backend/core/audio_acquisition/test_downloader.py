import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from backend.core.audio_acquisition import downloader
from backend.core.audio_acquisition.downloader import Status


@pytest.fixture()
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.mark.smoke
def test_validate_url_accepts_youtube_formats():
    valid_urls = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=abc123XYZ_-&list=PLtest", "abc123XYZ_-"),
    ]
    for url, expected in valid_urls:
        ok, video_id = downloader.validate_url(url)
        assert ok is True
        assert video_id == expected


@pytest.mark.smoke
def test_validate_url_rejects_non_youtube():
    for url in ["https://vimeo.com/123", "not a url", ""]:
        ok, video_id = downloader.validate_url(url)
        assert ok is False
        assert video_id is None


@pytest.mark.smoke
def test_download_audio_success(monkeypatch, temp_dir: Path):
    video_id = "dQw4w9WgXcQ"
    audio_path = temp_dir / f"{video_id}.mp3"
    audio_path.write_bytes(b"audio")

    info_json_path = temp_dir / f"{video_id}.info.json"
    info_json_path.write_text(
        json.dumps({"title": "Best Song", "artist": "Artist", "duration": 212, "filesize_approx": 5_000_000})
    )

    quick_result = MagicMock(returncode=0, stdout="Best Song\nArtist\n3:32\n", stderr="")
    download_result = MagicMock(returncode=0, stdout="", stderr="")

    calls = {"count": 0}

    def fake_run(*args, **kwargs):
        calls["count"] += 1
        return quick_result if calls["count"] == 1 else download_result

    monkeypatch.setattr(downloader.subprocess, "run", fake_run)

    result = downloader.download_audio(
        f"https://www.youtube.com/watch?v={video_id}",
        temp_dir,
        "mp3",
        192,
    )

    assert result is not None
    assert result.id == video_id
    assert result.status == Status.DOWNLOADED
    assert result.duration == 212
    assert result.title == "Best Song"
    assert result.artist == "Artist"
    assert Path(result.file_path).exists()


@pytest.mark.regression
def test_download_audio_fails_on_download_error(monkeypatch, temp_dir: Path):
    video_id = "dQw4w9WgXcQ"

    quick_result = MagicMock(returncode=0, stdout="Title\nArtist\n3:32\n", stderr="")
    download_result = MagicMock(returncode=1, stdout="", stderr="boom")

    calls = {"count": 0}

    def fake_run(*args, **kwargs):
        calls["count"] += 1
        return quick_result if calls["count"] == 1 else download_result

    monkeypatch.setattr(downloader.subprocess, "run", fake_run)

    result = downloader.download_audio(
        f"https://www.youtube.com/watch?v={video_id}",
        temp_dir,
        "mp3",
        192,
    )

    assert result is None
