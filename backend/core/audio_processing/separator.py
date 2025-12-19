def separate_vocals(
    audio_path: str, 
    output_dir: str = "separated",
    use_fallback: bool = False
) -> Dict[str, str]:
    """
    Separate vocals from audio file using Demucs.
    
    Story 2.2: Demucs Vocal Separation Pipeline
    Story 2.3: Spleeter Fallback Implementation (if Demucs fails)
    
    Args:
        audio_path: Path to input audio file
        output_dir: Directory for output files
        use_fallback: If True, use Spleeter if Demucs fails
        
    Returns:
        dict with paths to vocals and instrumental tracks
        
    Raises:
        RuntimeError: If separation fails
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # STORY 2.2: Try Demucs first
    # ========================================================================
    # Try direct command first, then fallback to python -m demucs
    # Use sys.executable to ensure we use the venv Python, not system Python
    # Set environment to use soundfile instead of torchaudio to avoid torchcodec issues
    env = os.environ.copy()
    # Force Demucs to use soundfile backend to avoid torchcodec/FFmpeg DLL issues
    env["DEMUCS_AUDIO_BACKEND"] = "soundfile"
    # Also set torchaudio backend to soundfile if possible
    env["TORCHAUDIO_USE_SOUNDFILE"] = "1"
    
    # Use faster model variant if available (htdemucs is default, but we can specify)
    # Add --shifts 0 to disable time shifting (faster but slightly less accurate)
    demucs_commands = [
        ["demucs", "--two-stems=vocals", "--shifts", "0", "-o", str(output_path), audio_path],
        [sys.executable, "-m", "demucs", "--two-stems=vocals", "--shifts", "0", "-o", str(output_path), audio_path]
    ]
    
    last_error = None
    for cmd in demucs_commands:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=600,  # 10 minute timeout
                env=env  # Use environment with soundfile backend
            )
            break  # Success, exit loop
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            last_error = e
            continue  # Try next command
    
    # If we got here and last_error exists, all commands failed
    if last_error:
        error_msg = last_error.stderr if hasattr(last_error, 'stderr') and last_error.stderr else str(last_error)
        error_details = f"Demucs failed: {error_msg}"
        
        if use_fallback:
            try:
                return _separate_with_spleeter(audio_path, output_dir)
            except Exception as fallback_error:
                raise RuntimeError(
                    f"Both Demucs and Spleeter failed. "
                    f"Demucs error: {error_details}, Spleeter error: {str(fallback_error)}"
                )
        else:
            raise RuntimeError(f"Demucs vocal separation failed: {error_details}")
    


    # Get output paths (only reached if Demucs succeeded)
    filename = Path(audio_path).stem
    base_path = output_path / "htdemucs" / filename
    
    vocals_path = base_path / "vocals.wav"
    instrumental_path = base_path / "no_vocals.wav"
    
    # Verify files exist
    if not vocals_path.exists() or not instrumental_path.exists():
        error_msg = f"Demucs output files not found. Expected: {vocals_path} and {instrumental_path}"
        
        if use_fallback:
            try:
                return _separate_with_spleeter(audio_path, output_dir)
            except Exception as fallback_error:
                raise RuntimeError(
                    f"Both Demucs and Spleeter failed. "
                    f"Demucs error: {error_msg}, Spleeter error: {str(fallback_error)}"
                )
        else:
            raise FileNotFoundError(error_msg)
        
    return {
        "vocals": str(vocals_path.absolute()),
        "instrumental": str(instrumental_path.absolute()),
        "method": "demucs"
    }

def _separate_with_spleeter(audio_path: str, output_dir: str) -> Dict[str, str]:
    """
    Story 2.3: Spleeter Fallback Implementation
    
    Separate vocals using Spleeter as fallback when Demucs fails.
    """
    try:
        from spleeter.separator import Separator
        
        separator = Separator('spleeter:2stems-16kHz')
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Spleeter expects directory, not file
        separator.separate_to_file(
            audio_path,
            str(output_path)
        )
        
        # Spleeter output structure: output_dir/track_name/vocals.wav and accompaniment.wav
        filename = Path(audio_path).stem
        base_path = output_path / filename
        
        vocals_path = base_path / "vocals.wav"
        instrumental_path = base_path / "accompaniment.wav"
        
        if not vocals_path.exists() or not instrumental_path.exists():
            raise FileNotFoundError("Spleeter output files not found")
        
        return {
            "vocals": str(vocals_path.absolute()),
            "instrumental": str(instrumental_path.absolute()),
            "method": "spleeter"
        }
        
    except ImportError:
        raise RuntimeError("Spleeter not installed. Install with: pip install spleeter")
    except Exception as e:
        raise RuntimeError(f"Spleeter separation failed: {str(e)}")