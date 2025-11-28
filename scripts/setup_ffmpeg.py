"""
Setup script to install FFmpeg automatically.
Checks for FFmpeg and attempts to install it if missing.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def check_ffmpeg_installed():
    """Check if FFmpeg is already installed."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ FFmpeg is already installed!")
        print(f"  Version: {result.stdout.split(chr(10))[0]}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_ffmpeg_windows():
    """Attempt to install FFmpeg on Windows."""
    print("\nAttempting to install FFmpeg on Windows...")
    
    # Try winget first (Windows 11/Windows 10 with App Installer)
    try:
        print("  Trying winget...")
        print("  (This may take a few minutes - please wait...)")
        result = subprocess.run(
            ["winget", "install", "ffmpeg", "--accept-package-agreements", "--accept-source-agreements"],
            capture_output=True,
            text=True,
            check=True,
            timeout=300  # 5 minute timeout
        )
        print("  ✓ FFmpeg installed via winget!")
        return True
    except subprocess.TimeoutExpired:
        print("  ✗ winget installation timed out (took longer than 5 minutes)")
        print("  You can try running the command manually in PowerShell: winget install ffmpeg")
    except subprocess.CalledProcessError as e:
        print("  ✗ winget installation failed")
        if e.stderr:
            print(f"    Error: {e.stderr[:200]}")
    except FileNotFoundError:
        print("  ✗ winget not found (requires Windows 10/11 with App Installer)")
    except Exception as e:
        print(f"  ✗ Unexpected error with winget: {e}")
    
    # Try chocolatey
    try:
        print("  Trying Chocolatey...")
        print("  (This may take a few minutes - please wait...)")
        result = subprocess.run(
            ["choco", "install", "ffmpeg", "-y"],
            capture_output=True,
            text=True,
            check=True,
            timeout=300  # 5 minute timeout
        )
        print("  ✓ FFmpeg installed via Chocolatey!")
        return True
    except subprocess.TimeoutExpired:
        print("  ✗ Chocolatey installation timed out (took longer than 5 minutes)")
        print("  You can try running manually: choco install ffmpeg -y")
    except subprocess.CalledProcessError as e:
        print("  ✗ Chocolatey installation failed")
        if e.stderr:
            print(f"    Error: {e.stderr[:200]}")
    except FileNotFoundError:
        print("  ✗ Chocolatey not found (install from https://chocolatey.org/)")
    except Exception as e:
        print(f"  ✗ Unexpected error with Chocolatey: {e}")
    
    # If package managers don't work, provide manual instructions
    print("\n" + "=" * 60)
    print("  ✗ Could not install automatically.")
    print("\n  Please install FFmpeg manually:")
    print("    1. Download from: https://www.gyan.dev/ffmpeg/builds/")
    print("       (Download 'ffmpeg-release-essentials.zip')")
    print("    2. Extract to C:\\ffmpeg")
    print("    3. Add C:\\ffmpeg\\bin to your system PATH:")
    print("       - Press Win+R, type: sysdm.cpl")
    print("       - Advanced → Environment Variables")
    print("       - Edit 'Path' → New → Add: C:\\ffmpeg\\bin")
    print("    4. Restart your terminal and verify: ffmpeg -version")
    print("=" * 60)
    return False


def install_ffmpeg_mac():
    """Attempt to install FFmpeg on macOS."""
    print("\nAttempting to install FFmpeg on macOS...")
    
    try:
        print("  Using Homebrew...")
        result = subprocess.run(
            ["brew", "install", "ffmpeg"],
            capture_output=True,
            text=True,
            check=True
        )
        print("  ✓ FFmpeg installed via Homebrew!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n  ✗ Homebrew not found.")
        print("\n  Please install FFmpeg manually:")
        print("    1. Install Homebrew: https://brew.sh/")
        print("    2. Run: brew install ffmpeg")
        return False


def install_ffmpeg_linux():
    """Attempt to install FFmpeg on Linux."""
    print("\nAttempting to install FFmpeg on Linux...")
    
    # Try apt (Debian/Ubuntu)
    try:
        print("  Trying apt...")
        result = subprocess.run(
            ["sudo", "apt", "update"],
            capture_output=True,
            text=True,
            check=True
        )
        result = subprocess.run(
            ["sudo", "apt", "install", "-y", "ffmpeg"],
            capture_output=True,
            text=True,
            check=True
        )
        print("  ✓ FFmpeg installed via apt!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Try yum (RedHat/CentOS)
    try:
        print("  Trying yum...")
        result = subprocess.run(
            ["sudo", "yum", "install", "-y", "ffmpeg"],
            capture_output=True,
            text=True,
            check=True
        )
        print("  ✓ FFmpeg installed via yum!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print("\n  ✗ Could not install automatically.")
    print("\n  Please install FFmpeg manually using your package manager:")
    print("    Debian/Ubuntu: sudo apt install ffmpeg")
    print("    RedHat/CentOS: sudo yum install ffmpeg")
    return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("FFmpeg Setup Script")
    print("=" * 60)
    
    # Check if already installed
    if check_ffmpeg_installed():
        print("\n✓ Setup complete! FFmpeg is ready to use.")
        return 0
    
    print("\n✗ FFmpeg is not installed.")
    
    # Ask user if they want to try automatic installation
    print("\nWould you like to attempt automatic installation?")
    print("  (This requires admin privileges and may take several minutes)")
    response = input("  Try automatic installation? [y/N]: ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("\n" + "=" * 60)
        print("Skipping automatic installation.")
        print("\nPlease install FFmpeg manually:")
        system = platform.system()
        if system == "Windows":
            print("  1. Download from: https://www.gyan.dev/ffmpeg/builds/")
            print("  2. Extract to C:\\ffmpeg")
            print("  3. Add C:\\ffmpeg\\bin to your system PATH")
        elif system == "Darwin":
            print("  Run: brew install ffmpeg")
        elif system == "Linux":
            print("  Run: sudo apt install ffmpeg")
        print("=" * 60)
        return 1
    
    # Detect OS and attempt installation
    system = platform.system()
    
    if system == "Windows":
        success = install_ffmpeg_windows()
    elif system == "Darwin":  # macOS
        success = install_ffmpeg_mac()
    elif system == "Linux":
        success = install_ffmpeg_linux()
    else:
        print(f"\n✗ Unsupported operating system: {system}")
        print("  Please install FFmpeg manually for your specific OS.")
        return 1
    
    if success:
        # Verify installation
        print("\n" + "-" * 60)
        if check_ffmpeg_installed():
            print("\n✓ Setup complete! FFmpeg is ready to use.")
            print("\n⚠️  Please restart your terminal/IDE for changes to take effect and verify the installation.")
            return 0
        else:
            print("\n⚠️  FFmpeg was installed but not found in PATH.")
            print("  Please restart your terminal/IDE and run this script again to verify the installation.")
            return 1
    
    return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

