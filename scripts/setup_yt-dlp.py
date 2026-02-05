"""
Installation Script for Audio Acquisition Dependencies

Installs yt-dlp and verifies FFmpeg is available.

Usage:
    python install.py
"""

import subprocess
import shutil
import sys
import setup_ffmpeg 

def verify_ffmpeg():
   return setup_ffmpeg.check_ffmpeg_installed()


def install_ytdlp():
    """Install yt-dlp using pip."""
    print("[INSTALL] yt-dlp...")
    try:
        # Try standard install first
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default]"]
        )
        print("yt-dlp installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        print("Try manually: python3 -m pip install -U \"yt-dlp[default]\"")
        return False

def verify_ytdlp():
    """Verify yt-dlp is importable."""
    print("[VERIFY] yt-dlp import...")
    try:
        import yt_dlp
        print(f"yt-dlp version {yt_dlp.version.__version__}")
        return True
    except ImportError:
        print("Cannot import yt-dlp")
        return False

def main():
    """Run installation and verification."""
    print("=" * 50)
    print("Audio Acquisition - Dependency Installation")
    print("=" * 50)
    print()
    
    results = []
    
    # Check FFmpeg
    results.append(verify_ffmpeg())
    
    # Install yt-dlp
    results.append(install_ytdlp())
    
    # Verify yt-dlp
    results.append(verify_ytdlp())

    
    # Summary
    print("=" * 50)
    if all(results):
        print("All dependencies installed successfully!")
        return 0
    else:
        print("Some dependencies are missing. See above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())