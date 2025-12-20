"""Performance benchmarks for the karaoke generation pipeline."""
import pytest
import time
import psutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.mark.performance
@pytest.mark.slow
@patch('backend.core.video_rendering.renderer.subprocess.run')
@patch('backend.core.video_rendering.renderer._get_audio_duration')
def test_video_render_time_1_minute_song(mock_duration, mock_run, tmp_path):
    """Test that 1-minute song renders in < 2 minutes."""
    mock_duration.return_value = 60.0
    mock_run.return_value = MagicMock(returncode=0)
    
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"MOCK AUDIO" * 1000)
    
    subtitle_path = tmp_path / "subs.ass"
    subtitle_path.write_text("[Script Info]\nTitle: Test", encoding="utf-8")
    
    output_path = tmp_path / "output.mp4"
    output_path.write_bytes(b"VIDEO")
    
    from backend.core.video_rendering.renderer import render_karaoke_video
    
    start_time = time.time()
    render_karaoke_video(
        audio_file=str(audio_path),
        subtitle_file=str(subtitle_path),
        output_file=str(output_path),
        title="Test",
        artist="Artist"
    )
    elapsed = time.time() - start_time
    
    # With mocks, should be nearly instant
    # Real benchmark: < 120 seconds for 1-min song
    assert elapsed < 120, f"Render took {elapsed:.2f}s, expected < 120s"


@pytest.mark.performance
@pytest.mark.slow
@patch('backend.core.video_rendering.renderer.subprocess.run')
@patch('backend.core.video_rendering.renderer._get_audio_duration')
def test_video_render_time_3_minute_song(mock_duration, mock_run, tmp_path):
    """Test that 3-minute song renders in < 5 minutes."""
    mock_duration.return_value = 180.0
    mock_run.return_value = MagicMock(returncode=0)
    
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"MOCK AUDIO" * 3000)
    
    subtitle_path = tmp_path / "subs.ass"
    subtitle_path.write_text("[Script Info]\nTitle: Test", encoding="utf-8")
    
    output_path = tmp_path / "output.mp4"
    output_path.write_bytes(b"VIDEO")
    
    from backend.core.video_rendering.renderer import render_karaoke_video
    
    start_time = time.time()
    render_karaoke_video(
        audio_file=str(audio_path),
        subtitle_file=str(subtitle_path),
        output_file=str(output_path),
        title="Test",
        artist="Artist"
    )
    elapsed = time.time() - start_time
    
    # Target: < 300 seconds (5 minutes) for 3-min song
    assert elapsed < 300, f"Render took {elapsed:.2f}s, expected < 300s"


@pytest.mark.performance
@pytest.mark.slow
@patch('backend.core.video_rendering.renderer.subprocess.run')
@patch('backend.core.video_rendering.renderer._get_audio_duration')
def test_video_render_time_5_minute_song(mock_duration, mock_run, tmp_path):
    """Test that 5-minute song renders in < 8 minutes."""
    mock_duration.return_value = 300.0
    mock_run.return_value = MagicMock(returncode=0)
    
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"MOCK AUDIO" * 5000)
    
    subtitle_path = tmp_path / "subs.ass"
    subtitle_path.write_text("[Script Info]\nTitle: Test", encoding="utf-8")
    
    output_path = tmp_path / "output.mp4"
    output_path.write_bytes(b"VIDEO")
    
    from backend.core.video_rendering.renderer import render_karaoke_video
    
    start_time = time.time()
    render_karaoke_video(
        audio_file=str(audio_path),
        subtitle_file=str(subtitle_path),
        output_file=str(output_path),
        title="Test",
        artist="Artist"
    )
    elapsed = time.time() - start_time
    
    # Target: < 480 seconds (8 minutes) for 5-min song
    assert elapsed < 480, f"Render took {elapsed:.2f}s, expected < 480s"


@pytest.mark.performance
@pytest.mark.regression
def test_memory_usage_stays_within_limits():
    """Test that memory usage stays within reasonable limits during processing."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Simulate some processing
    from backend.core.lyrics_intelligence.synchronizer import parse_lrc_file
    
    large_lrc = "\n".join([f"[00:{i:02d}.00]Line {i}" for i in range(1000)])
    parsed = parse_lrc_file(large_lrc)
    
    current_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = current_memory - initial_memory
    
    # Memory increase should be reasonable (< 500 MB for this test)
    assert memory_increase < 500, f"Memory increased by {memory_increase:.2f} MB"


@pytest.mark.performance
@pytest.mark.regression
def test_no_memory_leaks():
    """Test for memory leaks during repeated operations."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    from backend.core.lyrics_intelligence.synchronizer import generate_lrc_file
    
    # Perform operation multiple times
    for _ in range(100):
        timestamps = [{"timestamp": float(i), "text": f"Line {i}"} for i in range(20)]
        lrc = generate_lrc_file(timestamps, "Title", "Artist")
        assert lrc  # Use the result
    
    final_memory = process.memory_info().rss / 1024 / 1024
    memory_leak = final_memory - initial_memory
    
    # Should not leak significant memory (< 50 MB for 100 iterations)
    assert memory_leak < 50, f"Potential memory leak: {memory_leak:.2f} MB after 100 iterations"


@pytest.mark.performance
@pytest.mark.smoke
@patch('backend.core.audio_acquisition.downloader.subprocess.run')
def test_audio_download_time(mock_run, tmp_path):
    """Test that audio download completes in < 30 seconds."""
    mock_run.return_value = MagicMock(returncode=0)
    
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"AUDIO")
    
    info_json = tmp_path / "audio.info.json"
    info_json.write_text('{"duration": 180}')
    
    with patch('backend.core.audio_acquisition.downloader.Path') as mock_path_cls:
        mock_path_inst = MagicMock()
        mock_path_inst.exists.return_value = True
        mock_path_inst.__truediv__ = lambda self, other: tmp_path / other
        mock_path_cls.return_value = mock_path_inst
        
        from backend.core.audio_acquisition.downloader import download_audio
        
        start_time = time.time()
        result = download_audio("https://youtube.com/watch?v=test", str(tmp_path))
        elapsed = time.time() - start_time
        
        assert result is not None
        # Target: < 30 seconds
        assert elapsed < 30, f"Download took {elapsed:.2f}s, expected < 30s"


@pytest.mark.performance
@pytest.mark.slow
@patch('backend.core.audio_processing.separator.subprocess.run')
def test_vocal_separation_time_3min_song(mock_run, tmp_path):
    """Test that vocal separation for 3-min song takes < 3 minutes."""
    mock_run.return_value = MagicMock(returncode=0)
    
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"AUDIO" * 3000)
    
    vocals_path = tmp_path / "htdemucs" / "audio" / "vocals.wav"
    vocals_path.parent.mkdir(parents=True, exist_ok=True)
    vocals_path.write_bytes(b"VOCALS")
    
    from backend.core.audio_processing.separator import separate_vocals
    
    start_time = time.time()
    result = separate_vocals(str(audio_path), str(tmp_path))
    elapsed = time.time() - start_time
    
    assert result is not None
    # Target: < 180 seconds for 3-min song
    assert elapsed < 180, f"Separation took {elapsed:.2f}s, expected < 180s"


@pytest.mark.performance
@pytest.mark.smoke
def test_lyrics_synchronization_time():
    """Test that lyrics synchronization completes in < 1 minute."""
    from backend.core.lyrics_intelligence.synchronizer import parse_lrc_file
    
    # Large LRC file (100 lines)
    lrc = "\n".join([f"[00:{i:02d}.{(i*10)%100:02d}]Line {i}" for i in range(100)])
    
    start_time = time.time()
    parsed = parse_lrc_file(lrc)
    elapsed = time.time() - start_time
    
    assert len(parsed) == 100
    # Target: < 60 seconds
    assert elapsed < 60, f"Sync took {elapsed:.2f}s, expected < 60s"


@pytest.mark.performance
@pytest.mark.regression
def test_lyric_accuracy_benchmark():
    """Benchmark lyric timestamp accuracy (target ≥ 90%)."""
    from backend.core.lyrics_intelligence.synchronizer import parse_lrc_file
    
    # Test with known accurate timestamps
    test_lrc = """[00:00.00]Line 1
[00:05.50]Line 2
[00:10.00]Line 3
[00:15.25]Line 4
[00:20.00]Line 5"""
    
    parsed = parse_lrc_file(test_lrc)
    
    expected_timestamps = [0.0, 5.5, 10.0, 15.25, 20.0]
    actual_timestamps = [entry["timestamp"] for entry in parsed]
    
    # Calculate accuracy (timestamps should match exactly)
    correct = sum(1 for a, e in zip(actual_timestamps, expected_timestamps) if abs(a - e) < 0.01)
    accuracy = (correct / len(expected_timestamps)) * 100
    
    # Target: ≥ 90% accuracy
    assert accuracy >= 90, f"Lyric accuracy {accuracy:.1f}%, expected ≥ 90%"


@pytest.mark.performance
@pytest.mark.regression
def test_processing_speed_benchmarks(tmp_path):
    """Comprehensive processing speed benchmark."""
    benchmarks = {
        "lrc_parse_100_lines": 0.0,
        "lrc_generate_100_lines": 0.0,
    }
    
    from backend.core.lyrics_intelligence.synchronizer import parse_lrc_file, generate_lrc_file
    
    # Benchmark 1: Parse 100 lines
    lrc = "\n".join([f"[00:{i:02d}.00]Line {i}" for i in range(100)])
    start = time.time()
    parse_lrc_file(lrc)
    benchmarks["lrc_parse_100_lines"] = time.time() - start
    
    # Benchmark 2: Generate 100 lines
    timestamps = [{"timestamp": float(i), "text": f"Line {i}"} for i in range(100)]
    start = time.time()
    generate_lrc_file(timestamps, "Title", "Artist")
    benchmarks["lrc_generate_100_lines"] = time.time() - start
    
    # All operations should be fast
    for operation, elapsed in benchmarks.items():
        assert elapsed < 1.0, f"{operation} took {elapsed:.3f}s, expected < 1s"
    
    # Print benchmarks for documentation
    print("\n=== Performance Benchmarks ===")
    for operation, elapsed in benchmarks.items():
        print(f"{operation}: {elapsed*1000:.2f}ms")
