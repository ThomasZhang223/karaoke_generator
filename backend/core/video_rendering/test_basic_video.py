"""
Basic video creation test for Story 1.5.
Tests that FFmpeg is installed and can create a simple video with audio and text.
"""

import subprocess
import os
import sys
from pathlib import Path


def find_ffmpeg():
    """
    Find FFmpeg executable path.
    Checks: ffmpeg-python library, virtual environment, then system PATH.
    """
    # Try using ffmpeg-python library to find FFmpeg
    try:
        import ffmpeg
        # ffmpeg-python can help us find the binary
        # Try to probe it - if it works, FFmpeg is accessible
        try:
            ffmpeg.probe('dummy')  # This will fail but checks if FFmpeg is accessible
        except:
            pass  # Expected to fail, but means ffmpeg binary might be accessible
        
        # Check if ffmpeg-python can find the binary
        # The library uses subprocess to call ffmpeg, so if it's in PATH it should work
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                check=True
            )
            return "ffmpeg"  # Found via ffmpeg-python/system PATH
        except:
            pass
    except ImportError:
        pass  # ffmpeg-python not installed, continue with other methods
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment
        venv_base = Path(sys.prefix)
        if os.name == 'nt':  # Windows
            ffmpeg_path = venv_base / "Scripts" / "ffmpeg.exe"
        else:  # Mac/Linux
            ffmpeg_path = venv_base / "bin" / "ffmpeg"
        
        if ffmpeg_path.exists():
            return str(ffmpeg_path)
    
    # Check system PATH
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        return "ffmpeg"  # Found in PATH
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return None


def test_ffmpeg_installed():
    """Test that FFmpeg is installed and accessible."""
    ffmpeg_path = find_ffmpeg()
    
    if ffmpeg_path is None:
        print("✗ FFmpeg binary is not installed or not accessible")
        print("\n  Note: You have 'ffmpeg-python' package installed, but you also need the FFmpeg binary.")
        print("  'ffmpeg-python' is just a Python wrapper - it requires the actual FFmpeg executable.")
        print("\n  Please install FFmpeg binary:")
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            venv_base = Path(sys.prefix)
            if os.name == 'nt':  # Windows
                venv_ffmpeg = venv_base / "Scripts" / "ffmpeg.exe"
            else:
                venv_ffmpeg = venv_base / "bin" / "ffmpeg"
            print(f"    Option 1: Copy FFmpeg to virtual environment: {venv_ffmpeg.parent}")
        print("    Option 2: Install FFmpeg system-wide:")
        print("      Windows: Download from https://ffmpeg.org/download.html and add to PATH")
        print("      Mac: brew install ffmpeg")
        print("      Linux: sudo apt install ffmpeg")
        print("\n  After installing, make sure 'ffmpeg' command works in your terminal.")
        return None
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ FFmpeg is installed and accessible")
        print(f"  Location: {ffmpeg_path}")
        print(f"  Version: {result.stdout.split(chr(10))[0]}")
        return ffmpeg_path
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"✗ Error accessing FFmpeg at {ffmpeg_path}: {e}")
        return None


def test_basic_video_creation(ffmpeg_path):
    """
    Create a basic test video:
    - 5 second duration
    - Solid color background
    - Text overlay saying "Test Video"
    - Optional: Add a test audio file if available
    """
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "test_video.mp4"
    
    # FFmpeg command to create a simple test video
    # -f lavfi: use libavfilter virtual input
    # color=c=red: create a red background
    # drawtext: add text overlay
    ffmpeg_cmd = [
        ffmpeg_path,
        "-f", "lavfi",
        "-i", "color=c=red:size=1280x720:duration=5",
        "-vf", "drawtext=text='Last Christmas - Wham!':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y",  # Overwrite output file
        str(output_file)
    ]
    
    try:
        print(f"\nCreating test video: {output_file}")
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if output_file.exists():
            file_size = output_file.stat().st_size
            print(f"✓ Test video created successfully!")
            print(f"  File: {output_file}")
            print(f"  Size: {file_size / 1024:.2f} KB")
            return True
        else:
            print("✗ Video file was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating video:")
        print(f"  {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Video Rendering Basic Test (Story 1.5)")
    print("=" * 50)
    
    # Test 1: FFmpeg installation
    ffmpeg_path = test_ffmpeg_installed()
    if ffmpeg_path is None:
        print("\n" + "=" * 50)
        exit(1)
    
    # Test 2: Basic video creation
    print("\n" + "-" * 50)
    success = test_basic_video_creation(ffmpeg_path)
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed!")
        print(f"  Check output/test_video.mp4 to verify the video")
    else:
        print("✗ Tests failed - check errors above")
    print("=" * 50)

