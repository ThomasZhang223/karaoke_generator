from pathlib import Path
from unittest.mock import MagicMock
import subprocess

import pytest

from backend.core.video_rendering import overlay, renderer, subtitle_renderer
from backend.core.lyrics_intelligence.synchronizer import LyricLine, LRCData


# ---------- overlay tests ----------

@pytest.mark.smoke
def test_create_simple_overlay_filter_contains_expected_fields():
    f = overlay.create_simple_overlay_filter("Hello", 1.0, 2.0)
    assert "drawtext" in f
    assert "enable='between(t,1.0,2.0)'" in f
    assert "boxcolor" in f


@pytest.mark.regression
def test_create_lyrics_overlay_filter_escapes_text_and_times():
    lyrics = [
        LyricLine(start_time=10.1234, end_time=12.5, text='He said "[Hi]: now"'),
        LyricLine(start_time=13.0, end_time=14.0, text='Next line'),
    ]
    flt = overlay.create_lyrics_overlay_filter(lyrics)
    # Times formatted to 3 decimals trimmed
    assert "between(t,10.123,12.5)" in flt
    # Text escaped (brackets and colon escaped)
    assert 'text="He said \\\"\\[Hi\\]\\: now\\\""' in flt


# ---------- subtitle renderer tests ----------

@pytest.mark.smoke
def test_create_ass_subtitle_file_and_build_filter(tmp_path: Path):
    lyrics = [
        LyricLine(start_time=0.0, end_time=4.0, text="start"),
        LyricLine(start_time=10.0, end_time=12.0, text="middle"),
    ]
    p = subtitle_renderer.create_ass_subtitle_file(lyrics, title="Song", artist="Artist")
    content = Path(p).read_text()
    assert "[Script Info]" in content and "[Events]" in content
    assert "Dialogue:" in content
    filt = subtitle_renderer.build_subtitle_filter(p)
    assert "subtitles='" in filt and "force_style='" in filt


# ---------- renderer tests ----------

@pytest.mark.smoke
def test_render_simple_video_mocks_ffmpeg(monkeypatch, tmp_path: Path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"data")
    out = tmp_path / "out.mp4"

    monkeypatch.setattr(renderer, "_get_audio_duration", lambda p: 2.0)

    def fake_run(cmd, capture_output, text, check, timeout):
        out.write_bytes(b"video")
        return MagicMock(returncode=0)

    monkeypatch.setattr(renderer.subprocess, "run", fake_run)

    result = renderer.render_simple_video(str(audio), str(out))
    assert Path(result) == out and out.exists()


@pytest.mark.smoke
def test_render_karaoke_video_overlay_path(monkeypatch, tmp_path: Path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"data")
    out = tmp_path / "karaoke.mp4"

    lyrics = [LyricLine(start_time=0.0, end_time=1.0, text="one"), LyricLine(start_time=1.0, end_time=2.0, text="two")]
    lrc = LRCData(title="Song", artist="Artist", lyrics=lyrics)

    monkeypatch.setattr(renderer, "_get_audio_duration", lambda p: 2.0)

    def fake_run(cmd, capture_output, text, check, timeout):
        out.write_bytes(b"video")
        return MagicMock(returncode=0)

    monkeypatch.setattr(renderer.subprocess, "run", fake_run)

    result = renderer.render_karaoke_video(str(audio), lrc, str(out))
    assert Path(result) == out and out.exists()


@pytest.mark.regression
def test_render_karaoke_video_uses_subtitles_for_many_lyrics(monkeypatch, tmp_path: Path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"data")
    out = tmp_path / "karaoke_subs.mp4"

    lyrics = [LyricLine(start_time=i, end_time=i+0.5, text=f"line {i}") for i in range(25)]
    lrc = LRCData(title="Song", artist="Artist", lyrics=lyrics)

    monkeypatch.setattr(renderer, "_get_audio_duration", lambda p: 10.0)

    # Mock subtitle file creation & filter
    def fake_create_ass(lyrics, title, artist):
        p = tmp_path / "subs.ass"
        p.write_text("[Script Info]\n[Events]\n")
        return str(p)

    monkeypatch.setattr(subtitle_renderer, "create_ass_subtitle_file", fake_create_ass)
    monkeypatch.setattr(subtitle_renderer, "build_subtitle_filter", lambda p: "subtitles='x.ass'")

    def fake_run(cmd, capture_output, text, check, timeout):
        out.write_bytes(b"video")
        return MagicMock(returncode=0)

    monkeypatch.setattr(renderer.subprocess, "run", fake_run)

    result = renderer.render_karaoke_video(str(audio), lrc, str(out))
    assert Path(result) == out and out.exists()


@pytest.mark.regression
def test_render_karaoke_video_timeout(monkeypatch, tmp_path: Path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"data")
    out = tmp_path / "karaoke_timeout.mp4"
    lrc = LRCData(lyrics=[LyricLine(start_time=0.0, end_time=1.0, text="one")])

    monkeypatch.setattr(renderer, "_get_audio_duration", lambda p: 2.0)

    def fake_run(cmd, capture_output, text, check, timeout):
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)

    monkeypatch.setattr(renderer.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError):
        renderer.render_karaoke_video(str(audio), lrc, str(out))


@pytest.mark.regression
def test_render_karaoke_video_failure(monkeypatch, tmp_path: Path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"data")
    out = tmp_path / "karaoke_fail.mp4"
    lrc = LRCData(lyrics=[LyricLine(start_time=0.0, end_time=1.0, text="one")])

    monkeypatch.setattr(renderer, "_get_audio_duration", lambda p: 2.0)

    def fake_run(cmd, capture_output, text, check, timeout):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="boom")

    monkeypatch.setattr(renderer.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError):
        renderer.render_karaoke_video(str(audio), lrc, str(out))
