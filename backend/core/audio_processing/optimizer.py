# ==============================================================================
# ==============================================================================
#                        AUDIO OPTIMIZER MODULE
# ==============================================================================
# ==============================================================================
#
# Sprint 2 - Story 2.2: Demucs Vocal Separation Pipeline (Mark)
#           Audio quality optimization functions (normalization, noise reduction)
# Sprint 4 - Story 4.2: Bug Fixes & Performance Optimization (Mark)
#
# ==============================================================================

"""
Audio quality optimization
Story 2.2: Audio quality optimization functions
"""

import subprocess
from pathlib import Path
from typing import Optional


# ==============================================================================
# SPRINT 2 - MARK
# Story 2.2: Audio Quality Optimization Functions
# - Normalize audio to target LUFS level using FFmpeg
# - Reduce background noise from audio using FFmpeg
# - Apply audio quality optimizations (normalize, denoise)
# ==============================================================================

def normalize_audio(
    input_path: str,
    output_path: str,
    target_lufs: float = -23.0
) -> str:
    """
    Normalize audio to target LUFS level using FFmpeg.
    
    Story 2.2: Audio quality optimization functions
    
    Args:
        input_path: Path to input audio file
        output_path: Path for output normalized file
        target_lufs: Target loudness in LUFS (default -23.0, broadcast standard)
        
    Returns:
        Path to normalized audio file
        
    Raises:
        RuntimeError: If normalization fails
    """
    try:
        # Use FFmpeg loudnorm filter for LUFS normalization
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_path,
                "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
                "-y",  # Overwrite output file
                output_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not Path(output_path).exists():
            raise FileNotFoundError(f"Normalized file not created: {output_path}")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Audio normalization failed: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"Audio normalization error: {str(e)}")


def reduce_noise(
    input_path: str,
    output_path: str,
    noise_reduction: float = 0.3
) -> str:
    """
    Reduce background noise from audio using FFmpeg.
    
    Story 2.2: Audio quality optimization functions
    
    Args:
        input_path: Path to input audio file
        output_path: Path for output denoised file
        noise_reduction: Noise reduction strength (0.0-1.0)
        
    Returns:
        Path to denoised audio file
        
    Raises:
        RuntimeError: If noise reduction fails
    """
    try:
        # Use FFmpeg highpass and lowpass filters to reduce noise
        # This is a simple approach; more advanced would use spectral subtraction
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_path,
                "-af", f"highpass=f=80,lowpass=f=15000,afftdn=nr={noise_reduction}",
                "-y",
                output_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not Path(output_path).exists():
            raise FileNotFoundError(f"Denoised file not created: {output_path}")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Noise reduction failed: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"Noise reduction error: {str(e)}")


def optimize_audio_quality(
    input_path: str,
    output_path: Optional[str] = None,
    normalize: bool = True,
    denoise: bool = False
) -> str:
    """
    Apply audio quality optimizations.
    
    Story 2.2: Audio quality optimization functions
    
    Args:
        input_path: Path to input audio file
        output_path: Optional output path (defaults to input_path with _optimized suffix)
        normalize: Whether to normalize audio levels
        denoise: Whether to reduce background noise
        
    Returns:
        Path to optimized audio file
    """
    input_file = Path(input_path)
    
    if output_path is None:
        output_path = str(input_file.parent / f"{input_file.stem}_optimized{input_file.suffix}")
    
    current_path = input_path
    
    # Apply normalization if requested
    if normalize:
        current_path = normalize_audio(current_path, output_path)
        if denoise:
            # If both, create intermediate file
            temp_path = str(Path(output_path).parent / f"{Path(output_path).stem}_temp{Path(output_path).suffix}")
            current_path = reduce_noise(current_path, temp_path)
            # Move temp to final output
            Path(temp_path).replace(output_path)
    elif denoise:
        current_path = reduce_noise(current_path, output_path)
    
    return current_path

# ==============================================================================
# END OF SPRINT 2 - MARK
# ==============================================================================

