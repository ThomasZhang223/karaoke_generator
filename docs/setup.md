# Development Environment Setup Guide

**Document Version:** 1.0  
**Last Updated:** November 25, 2025

---

## Overview

This guide covers setting up the development environment for the Karaoke Video Generator project.

---

## Prerequisites

- **Python:** 3.10 or higher
- **Node.js:** 20.19+ or 22.12+ (for Vite)
- **FFmpeg:** Latest stable version
- **yt-dlp:** Latest version
- **Git:** For version control

---

## Backend Setup

### 1. Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Option A: Automatic Setup (Recommended)**
```bash
# From project root
python scripts/setup_ffmpeg.py
```

This script will:
- Check if FFmpeg is already installed
- Attempt to install it automatically using your system's package manager
- Provide manual instructions if automatic installation fails

**Option B: Manual Setup**

**Windows:**
1. Download from https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Restart terminal/IDE

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. Verify FFmpeg Installation

```bash
# Test FFmpeg is accessible
ffmpeg -version

# Test Python can access FFmpeg
cd backend
python -m core.video_rendering.test_basic_video
```

### 5. Install yt-dlp
```bash
# From project root
python scripts/setup_yt_dlp.py
```

'''This script will:
- Check if ffmpeg is installed
- Check if yt-dlp is installed
- If not, install the latest version of yt-dlp'''

---

### 6. Install Demucs (Audio Separation)

Demucs is used for separating vocals from instrumental tracks for karaoke generation.

**Installation:**
```bash
# Ensure virtual environment is activated
# Install compatible versions
pip install torchaudio==2.1.0
pip install "numpy<2"
pip install soundfile
pip install demucs
```

**Verify Installation:**
```bash
demucs --help
```

**Test Audio Separation:**
```bash
# Test with a sample MP3 file
demucs --two-stems=vocals path/to/test-song.mp3

# Output will be in: separated/htdemucs/test-song/
# - vocals.wav (singing only)
# - no_vocals.wav (instrumental/karaoke track)
```

**Troubleshooting:**
- If you get NumPy errors, ensure you have `numpy<2` installed
- If you get torchaudio errors, use version 2.1.0 specifically
- Requires FFmpeg to be installed (see step 3 above)

---

## Frontend Setup

### 1. Install Node.js Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173/`

---

## System Requirements

### Minimum Requirements

- **OS:** Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM:** 8GB minimum (16GB recommended for video processing)
- **Storage:** 5GB free space
- **CPU:** Multi-core processor recommended

### Software Versions

- **Python:** 3.10+
- **Node.js:** 20.19+ or 22.12+
- **FFmpeg:** 6.0+ (latest stable recommended)
- **yt-dlp:** 2025.11.12+
- **pytest:** 9.0.1+
- **FastAPI:** 0.104+
- **React:** 18+
- **Vite:** 7.0+
- **Demucs:** 4.0.1+
- **PyTorch/Torchaudio:** 2.1.0
- **NumPy:** <2.0 (1.x versions)

### FFmpeg Codecs Required

- **Video:** H.264 (libx264)
- **Audio:** AAC or MP3
- **Container:** MP4

---

## Troubleshooting

### FFmpeg Not Found

**Error:** `ffmpeg: command not found`

**Solution:**
- Ensure FFmpeg is installed and in your system PATH
- Windows: Add FFmpeg bin directory to PATH environment variable
- Verify with: `ffmpeg -version`

### Python Cannot Find FFmpeg

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution:**
- Ensure FFmpeg is in system PATH
- Restart terminal/IDE after installing FFmpeg
- Test with: `python -m core.video_rendering.test_basic_video`

### Node.js Version Warning

**Error:** `Vite requires Node.js version 20.19+ or 22.12+`

**Solution:**
- Upgrade Node.js to 20.19+ or 22.12+
- Use `nvm` to manage Node.js versions if needed

---

## Next Steps

After setup is complete:
1. Run backend: `cd backend && python main.py`
2. Run frontend: `cd frontend && npm run dev`
3. Test video rendering: `python -m core.video_rendering.test_basic_video`

---

**Document Owner:** Technical Lead (William Cagas)

