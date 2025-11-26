# Karaoke Video Generator

An automated system that converts any song into a karaoke video with synchronized lyrics.

## Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd project_team_27
```

### 2. Setup Backend

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install Python dependencies
cd backend
pip install -r requirements.txt
```

### 3. Setup FFmpeg (Required)

**Option A: Automatic Setup (Recommended)**
```bash
# Run the setup script
python scripts/setup_ffmpeg.py
```

**Option B: Manual Setup**
- **Windows:** Download from https://www.gyan.dev/ffmpeg/builds/ and add to PATH
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

See [docs/setup.md](docs/setup.md) for detailed instructions.

### 4. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Run Backend

```bash
cd backend
python main.py
```

Backend will be available at `http://localhost:8000`  
Frontend will be available at `http://localhost:5173`

## Project Structure

```
project_team_27/
├── backend/          # FastAPI backend
├── frontend/         # React + TypeScript frontend
├── docs/            # Documentation
├── scripts/          # Setup and utility scripts
└── tests/           # Test files
```

## Documentation

- [Project Charter](docs/charter.md)
- [Product & Sprint Backlogs](docs/backlog.md)
- [Setup Guide](docs/setup.md)
- [User Stories](docs/user_stories.md)
- [Use Cases](docs/use_cases.md)
- [Domain Model](docs/domain_model.md)

## Requirements

- Python 3.10+
- Node.js 20.19+ or 22.12+
- FFmpeg 6.0+ (see setup instructions above)

## Team

- **Technical Lead:** William Cagas
- **Team Members:** Aruhant Mehta, Mark Rozin, Thomas Zhang, William Cagas



