# Development Environment Setup Guide

**Document Version:** 1.1  
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

**Key Dependencies:**
- FastAPI: Web framework for building the API
- Uvicorn: ASGI server for running FastAPI
- Pydantic: Data validation and settings management
- yt-dlp: YouTube audio download
- ffmpeg-python: Video processing

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

This script will:
- Check if ffmpeg is installed
- Check if yt-dlp is installed
- If not, install the latest version of yt-dlp

### 6. Run FastAPI Backend Server

**Option A: Using Python directly**
```bash
cd backend
python main.py
```

**Option B: Using Uvicorn directly**
```bash
cd backend
uvicorn main:app --reload
```

The backend server will start on `http://localhost:8000`

**API Endpoints:**
- Root: `http://localhost:8000/`
- Health Check: `http://localhost:8000/api/v1/health`
- API Documentation (Swagger): `http://localhost:8000/docs`
- API Documentation (ReDoc): `http://localhost:8000/redoc`
- Generate Karaoke: `POST http://localhost:8000/api/v1/karaoke/generate`
- Job Status: `GET http://localhost:8000/api/v1/karaoke/status/{job_id}`

### 7. Backend Structure

The backend follows a clean architecture pattern:

```
backend/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── api/
│   ├── endpoints/       # API route handlers
│   │   ├── health.py   # Health check endpoints
│   │   └── karaoke.py  # Karaoke generation endpoints
│   └── middleware.py    # Error handling middleware
├── services/            # Business logic layer
│   └── karaoke_service.py  # Orchestrates core modules
├── models/              # Data models
│   └── schemas.py       # Pydantic request/response models
└── core/                # Core functionality modules
    ├── audio_acquisition/
    ├── audio_processing/
    ├── lyrics_intelligence/
    └── video_rendering/
```

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
- **FastAPI:** 0.104+
- **React:** 18+
- **Vite:** 7.0+

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

### FastAPI Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
- Ensure virtual environment is activated
- Install dependencies: `pip install -r backend/requirements.txt`
- Verify installation: `pip list | grep fastapi`

### Backend Server Won't Start

**Error:** `Address already in use` or port conflicts

**Solution:**
- Check if port 8000 is already in use: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)
- Kill the process using the port or change the port in `backend/config.py`
- Alternatively, specify a different port: `uvicorn main:app --port 8001`

---

## Next Steps

After setup is complete:
1. **Run backend:** `cd backend && python main.py`
   - Backend will be available at `http://localhost:8000`
   - API documentation at `http://localhost:8000/docs`
2. **Run frontend:** `cd frontend && npm run dev`
   - Frontend will be available at `http://localhost:5173`
3. **Test the API:**
   - Visit `http://localhost:8000/docs` to access interactive API documentation
   - Test health endpoint: `curl http://localhost:8000/api/v1/health`
   - Test karaoke generation: Use the Swagger UI or send POST request to `/api/v1/karaoke/generate`
4. **Test video rendering:** `python -m core.video_rendering.test_basic_video`

## Testing the Backend API

### Using Swagger UI (Recommended)
1. Start the backend server
2. Navigate to `http://localhost:8000/docs`
3. Use the interactive interface to test endpoints
4. Click "Try it out" on any endpoint to test it

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
```

**Generate Karaoke (example):**
```bash
curl -X POST "http://localhost:8000/api/v1/karaoke/generate" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

**Check Job Status:**
```bash
curl http://localhost:8000/api/v1/karaoke/status/{job_id}
```

---

**Document Owner:** Technical Lead (William Cagas)

