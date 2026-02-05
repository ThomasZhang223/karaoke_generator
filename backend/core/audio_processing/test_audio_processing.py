from pathlib import Path
from unittest.mock import MagicMock
import subprocess

import pytest

from backend.core.audio_processing import optimizer, separator


# ----------------------- optimizer tests -----------------------

@pytest.mark.smoke
def test_normalize_audio_success(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "in.wav"
    input_file.write_bytes(b"data")
    output_file = tmp_path / "out.wav"

    def fake_run(cmd, capture_output, text, check):
        output_file.write_bytes(b"normalized")
        return MagicMock(returncode=0)

    monkeypatch.setattr(optimizer.subprocess, "run", fake_run)

    result = optimizer.normalize_audio(str(input_file), str(output_file))

    assert Path(result) == output_file
    assert output_file.exists()


@pytest.mark.regression
def test_normalize_audio_failure(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "in.wav"
    input_file.write_bytes(b"data")
    output_file = tmp_path / "out.wav"

    def fake_run(cmd, capture_output, text, check):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="boom")

    monkeypatch.setattr(optimizer.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError):
        optimizer.normalize_audio(str(input_file), str(output_file))


@pytest.mark.smoke
def test_reduce_noise_success(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "in.wav"
    input_file.write_bytes(b"data")
    output_file = tmp_path / "out.wav"

    def fake_run(cmd, capture_output, text, check):
        output_file.write_bytes(b"denoised")
        return MagicMock(returncode=0)

    monkeypatch.setattr(optimizer.subprocess, "run", fake_run)

    result = optimizer.reduce_noise(str(input_file), str(output_file), noise_reduction=0.5)

    assert Path(result) == output_file
    assert output_file.exists()


@pytest.mark.regression
def test_reduce_noise_failure(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "in.wav"
    input_file.write_bytes(b"data")
    output_file = tmp_path / "out.wav"

    def fake_run(cmd, capture_output, text, check):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="nope")

    monkeypatch.setattr(optimizer.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError):
        optimizer.reduce_noise(str(input_file), str(output_file))


@pytest.mark.regression
def test_optimize_audio_quality_calls_normalize_and_denoise(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "in.wav"
    input_file.write_bytes(b"data")
    out_file = tmp_path / "in_optimized.wav"
    temp_file = tmp_path / "in_optimized_temp.wav"

    calls = {"normalize": 0, "denoise": 0}

    def fake_normalize(inp, outp, target_lufs=-23.0):
        calls["normalize"] += 1
        Path(outp).write_bytes(b"norm")
        return str(outp)

    def fake_denoise(inp, outp, noise_reduction=0.3):
        calls["denoise"] += 1
        Path(outp).write_bytes(b"denoise")
        return str(outp)

    monkeypatch.setattr(optimizer, "normalize_audio", fake_normalize)
    monkeypatch.setattr(optimizer, "reduce_noise", fake_denoise)

    result = optimizer.optimize_audio_quality(str(input_file), normalize=True, denoise=True)

    assert calls == {"normalize": 1, "denoise": 1}
    assert out_file.exists()
    # Function returns temp path even though file is moved; ensure final file exists
    assert Path(result).name.endswith("_temp.wav")


@pytest.mark.smoke
def test_optimize_audio_quality_denoise_only(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "in.wav"
    input_file.write_bytes(b"data")
    out_file = tmp_path / "in_optimized.wav"

    calls = {"normalize": 0, "denoise": 0}

    def fake_denoise(inp, outp, noise_reduction=0.3):
        calls["denoise"] += 1
        Path(outp).write_bytes(b"denoise")
        return str(outp)

    monkeypatch.setattr(optimizer, "reduce_noise", fake_denoise)

    result = optimizer.optimize_audio_quality(str(input_file), normalize=False, denoise=True)

    assert calls == {"normalize": 0, "denoise": 1}
    assert Path(result) == out_file
    assert out_file.exists()


# ----------------------- separator tests -----------------------

def _write_demucs_outputs(base: Path):
    vocals = base / "vocals.wav"
    instrumental = base / "no_vocals.wav"
    base.mkdir(parents=True, exist_ok=True)
    vocals.write_bytes(b"v")
    instrumental.write_bytes(b"i")


@pytest.mark.regression
def test_separate_vocals_demucs_success(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "song.wav"
    input_file.write_bytes(b"audio")
    demucs_base = tmp_path / "out" / "htdemucs" / "song"

    def fake_run(cmd, capture_output, text, check, timeout, env):
        _write_demucs_outputs(demucs_base)
        return MagicMock(returncode=0, stdout="")

    monkeypatch.setattr(separator.subprocess, "run", fake_run)

    result = separator.separate_vocals(str(input_file), output_dir=str(tmp_path / "out"))

    assert result["method"] == "demucs"
    assert Path(result["vocals"]).exists()
    assert Path(result["instrumental"]).exists()


@pytest.mark.regression
def test_separate_vocals_demucs_failure_no_fallback(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "song.wav"
    input_file.write_bytes(b"audio")

    def fake_run(cmd, capture_output, text, check, timeout, env):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="fail")

    monkeypatch.setattr(separator.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError):
        separator.separate_vocals(str(input_file), output_dir=str(tmp_path / "out"), use_fallback=False)


@pytest.mark.regression
def test_separate_vocals_demucs_failure_with_fallback(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "song.wav"
    input_file.write_bytes(b"audio")

    def fake_run(cmd, capture_output, text, check, timeout, env):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="fail")

    monkeypatch.setattr(separator.subprocess, "run", fake_run)
    monkeypatch.setattr(separator, "_separate_with_spleeter", lambda audio_path, output_dir: {"vocals": "v", "instrumental": "i", "method": "spleeter"})

    result = separator.separate_vocals(str(input_file), output_dir=str(tmp_path / "out"), use_fallback=True)

    assert result["method"] == "spleeter"


@pytest.mark.regression
def test_separate_vocals_missing_outputs_triggers_fallback(monkeypatch, tmp_path: Path):
    input_file = tmp_path / "song.wav"
    input_file.write_bytes(b"audio")

    def fake_run(cmd, capture_output, text, check, timeout, env):
        return MagicMock(returncode=0, stdout="")

    monkeypatch.setattr(separator.subprocess, "run", fake_run)
    monkeypatch.setattr(separator, "_separate_with_spleeter", lambda audio_path, output_dir: {"vocals": "v", "instrumental": "i", "method": "spleeter"})

    result = separator.separate_vocals(str(input_file), output_dir=str(tmp_path / "out"), use_fallback=True)

    assert result["method"] == "spleeter"
