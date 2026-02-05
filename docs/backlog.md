# KARAOKE VIDEO GENERATOR — PRODUCT & SPRINT BACKLOGS

**Document Version:** 1.1  
**Date Created:** November 5, 2025  
**Last Updated:** November 25, 2025

---

## Product Backlog Overview

This document contains the prioritized product backlog and sprint breakdowns for the Karaoke Video Generator project. All items are formatted for GitLab Issue Boards with labels, assignees, and acceptance criteria.

**Sprint Duration:** 1 week  
**Total Sprints:** 4  
**Project Timeline:** November 4 - December 2, 2025

---


## SPRINT 1: Foundation & Research (Week 1)
**Sprint Goal:** Establish project architecture, set up development environments, and complete initial research for all core components.

**Sprint Dates:** November 4 - November 11, 2025

---

### Story 1.0: Requirements & Design Documentation
**Type:** Task  
**Assignee:** William  
**Priority:** P0  
**Labels:** `documentation`, `requirements`, `design`, `setup`

**Description:**
Create comprehensive requirements and design documentation including user stories, use cases, and domain model to establish clear, traceable user needs and system structure.

**Acceptance Criteria:**
- [ ] User stories document created (`docs/user_stories.md`)
- [ ] Use cases document created (`docs/use_cases.md`)
- [ ] Domain model document created (`docs/domain_model.md`)
- [ ] All documents include traceability to backlog items
- [ ] User needs clearly defined and documented
- [ ] System structure and relationships documented

---

### Story 1.1: Project Architecture & Setup
**Type:** Task  
**Assignee:** William
**Priority:** P0  
**Labels:** `frontend`, `backend`, `setup`, `architecture`

**Description:**
Create comprehensive architecture document outlining system design, module interfaces, data flow, and integration points. Establish monorepo structure with frontend (React + TypeScript + Vite) and backend (FastAPI) folders.

**Acceptance Criteria:**
- [ ] Architecture document created with system diagram
- [ ] Module interfaces defined (input/output contracts)
- [ ] Data flow diagram completed
- [ ] Development environment setup guide documented
- [ ] Monorepo repository structure established
- [ ] Frontend folder structure created (Vite + React + TypeScript ready)
- [ ] Backend folder structure created (FastAPI structure)
- [ ] `.gitignore` updated for both Python and Node.js
- [ ] Code style guidelines defined

---

### Story 1.2: YouTube Audio Download Research & Setup
**Type:** Issue  
**Assignee:** Thomas  
**Priority:** P0  
**Labels:** `audio-acquisition`, `research`, `setup`

**Description:**
Research and evaluate YouTube download libraries, set up Python environment, and create initial module structure for audio acquisition.

**Acceptance Criteria:**
- [ ] Research completed on pytube, yt-dlp, and alternatives
- [ ] Python environment configured with required dependencies
- [ ] Successfully download sample audio from YouTube
- [ ] Module structure created in `src/audio-acquisition/`
- [ ] Installation process documented
- [ ] Error handling for invalid URLs implemented

---

### Story 1.3: Audio Processing Research & Setup
**Type:** Issue  
**Assignee:** Mark  
**Priority:** P0  
**Labels:** `audio-processing`, `research`, `setup`

**Description:**
Research and compare vocal separation libraries (Demucs, Spleeter, others), set up Python environment, and test baseline separation quality.

**Acceptance Criteria:**
- [ ] Research completed on Demucs, Spleeter, and alternatives
- [ ] Python environment configured with required dependencies
- [ ] Demucs installed and tested locally with sample audio files
- [ ] Installation process and system requirements documented
- [ ] Baseline tests run on different song genres
- [ ] Module structure created in `src/audio-processing/`
- [ ] Audio format requirements coordinated with Thomas

---

### Story 1.4: Lyrics Intelligence Research & Setup
**Type:** Issue  
**Assignee:** Aruhant  
**Priority:** P0  
**Labels:** `lyrics-intelligence`, `research`, `setup`

**Description:**
Research lyrics APIs and timestamping solutions, set up Python environment, and create initial module structure for lyrics intelligence.

**Acceptance Criteria:**
- [ ] Research completed on LyricsGenius, QuickLRC AI, and alternatives
- [ ] Python environment configured with required dependencies
- [ ] Successfully fetch lyrics for sample songs
- [ ] Module structure created in `src/lyrics-intelligence/`
- [ ] Installation process documented
- [ ] API rate limits and usage constraints documented

---

### Story 1.5: Video Rendering Research & Setup
**Type:** Issue  
**Assignee:** William  
**Priority:** P0  
**Labels:** `video-rendering`, `research`, `setup`

**Description:**
Research FFmpeg integration options, set up Python environment, and create initial module structure for video rendering.

**Acceptance Criteria:**
- [ ] Research completed on FFmpeg-Python, moviepy, and alternatives
- [ ] FFmpeg installed and accessible from Python
- [ ] Python environment configured with required dependencies
- [ ] Basic video creation test completed
- [ ] Module structure created in `src/video-rendering/`
- [ ] Installation process documented
- [ ] System requirements documented

---

## SPRINT 2: Core Implementation (Week 2)
**Sprint Goal:** Implement core functionality for audio acquisition and processing modules, begin lyrics intelligence development.

**Sprint Dates:** November 11 - November 18, 2025

---

### Story 2.1: YouTube to MP3 Conversion Implementation
**Type:** Issue  
**Assignee:** Thomas  
**Priority:** P0  
**Labels:** `audio-acquisition`, `implementation`, `core`

**Description:**
Implement complete YouTube download and MP3 conversion pipeline with error handling and quality options.

**Acceptance Criteria:**
- [ ] YouTube URL validation and parsing
- [ ] Audio download functionality working
- [ ] MP3 conversion with configurable quality (bitrate, sample rate)
- [ ] Error handling for network issues, invalid URLs, unavailable videos
- [ ] Fallback mechanism if primary library fails
- [ ] Unit tests for core functions
- [ ] Output format matches Mark's requirements

---

### Story 2.2: Demucs Vocal Separation Pipeline
**Type:** Issue  
**Assignee:** Mark  
**Priority:** P0  
**Labels:** `audio-processing`, `implementation`, `core`

**Description:**
Implement complete Demucs vocal separation pipeline with quality optimization and export functionality.

**Acceptance Criteria:**
- [ ] Demucs vocal separation pipeline implemented
- [ ] Audio quality optimization functions (normalization, noise reduction)
- [ ] Functions to export separated instrumental track
- [ ] Processing time benchmarks documented for different song lengths
- [ ] Unit tests for core functions
- [ ] Integration test with Thomas's MP3 output

---

### Story 2.3: Spleeter Fallback Implementation
**Type:** Issue  
**Assignee:** Mark  
**Priority:** P1  
**Labels:** `audio-processing`, `implementation`, `fallback`

**Description:**
Set up Spleeter as backup/fallback option for vocal separation when Demucs fails or produces poor results.

**Acceptance Criteria:**
- [ ] Spleeter installed and configured
- [ ] Fallback logic implemented to switch to Spleeter
- [ ] Quality comparison documented between Demucs and Spleeter
- [ ] Error handling for Spleeter failures
- [ ] Unit tests for fallback mechanism

---

### Story 2.4: Lyrics Fetching Implementation
**Type:** Issue  
**Assignee:** Aruhant  
**Priority:** P0  
**Labels:** `lyrics-intelligence`, `implementation`, `core`

**Description:**
Implement lyrics fetching from APIs with fallback options and error handling.

**Acceptance Criteria:**
- [ ] Lyrics fetching from primary API (LyricsGenius or similar)
- [ ] Fallback to secondary API if primary fails
- [ ] Song title and artist matching logic
- [ ] Error handling for missing lyrics, API failures
- [ ] Unit tests for core functions
- [ ] Rate limiting and API usage tracking

---

### Story 2.5: LRC File Generation Foundation
**Type:** Issue  
**Assignee:** Aruhant  
**Priority:** P0  
**Labels:** `lyrics-intelligence`, `implementation`, `lrc`

**Description:**
Create LRC file parsing and generation utilities with basic timestamp support.

**Acceptance Criteria:**
- [ ] LRC file parser implemented
- [ ] LRC file generator implemented
- [ ] Basic timestamp format validation
- [ ] Unit tests for LRC parsing and generation
- [ ] Documentation of LRC format requirements

---

### Story 2.6: FastAPI Backend API Setup
**Type:** Task  
**Assignee:** William  
**Priority:** P0  
**Labels:** `backend`, `setup`, `api`

**Description:**
Set up FastAPI backend with API endpoints, CORS configuration, and basic service structure to orchestrate core modules.

**Acceptance Criteria:**
- [ ] FastAPI application initialized with proper structure
- [ ] CORS middleware configured for frontend
- [ ] Basic API endpoints created (health check, generate karaoke)
- [ ] Service layer structure created (api/, services/, models/)
- [ ] Error handling middleware implemented
- [ ] API documentation accessible (Swagger/OpenAPI)
- [ ] Backend can be run locally and tested

---

## SPRINT 3: Integration & Synchronization (Week 3)
**Sprint Goal:** Complete lyrics timestamping, integrate all modules, and begin video rendering implementation.

**Sprint Dates:** November 18 - November 25, 2025

---

### Story 3.1: Frontend UI Implementation
**Type:** Issue  
**Assignee:** William  
**Priority:** P0  
**Labels:** `frontend`, `implementation`, `ui`

**Description:**
Implement React frontend with TypeScript, shadcn-ui components, and API integration for karaoke video generation.

**Acceptance Criteria:**
- [ ] React + TypeScript + Vite setup complete
- [ ] shadcn-ui installed and configured
- [ ] Main form component for YouTube URL input
- [ ] API client service for backend communication
- [ ] Progress indicator component for generation status
- [ ] Video player component for displaying results
- [ ] Error handling and user feedback
- [ ] Responsive design implemented

---

### Story 3.2: Lyrics Timestamp Synchronization
**Type:** Issue  
**Assignee:** Aruhant  
**Priority:** P0  
**Labels:** `lyrics-intelligence`, `implementation`, `synchronization`

**Description:**
Implement lyrics timestamp synchronization using QuickLRC AI or manual alignment algorithms.

**Acceptance Criteria:**
- [ ] Timestamp synchronization algorithm implemented
- [ ] Integration with QuickLRC AI or alternative
- [ ] Manual correction tools for inaccurate timestamps
- [ ] Accuracy ≥ 90% for test songs
- [ ] Unit tests for synchronization functions
- [ ] Integration test with audio files

---

### Story 3.3: Audio Processing Integration
**Type:** Issue  
**Assignee:** Mark  
**Priority:** P0  
**Labels:** `audio-processing`, `integration`, `optimization`

**Description:**
Integrate audio processing module with audio acquisition system and optimize performance.

**Acceptance Criteria:**
- [ ] Integration with Thomas's audio acquisition module complete
- [ ] Processing speed optimized (parallel processing if needed)
- [ ] Error handling for edge cases (corrupted files, unsupported formats)
- [ ] Audio format requirements coordinated with William
- [ ] Quality assurance testing on 10-15 diverse songs
- [ ] API documentation completed

---

### Story 3.4: Video Rendering Foundation
**Type:** Issue  
**Assignee:** William  
**Priority:** P0  
**Labels:** `video-rendering`, `implementation`, `core`

**Description:**
Implement basic video rendering engine with FFmpeg integration and text overlay capabilities.

**Acceptance Criteria:**
- [ ] FFmpeg integration working from Python
- [ ] Basic video creation (720p resolution)
- [ ] Text overlay functionality implemented
- [ ] Background/image support for video
- [ ] Unit tests for core rendering functions
- [ ] Integration test with sample audio and lyrics

---

### Story 3.5: Lyrics-to-Video Synchronization
**Type:** Issue  
**Assignee:** William  
**Priority:** P0  
**Labels:** `video-rendering`, `implementation`, `synchronization`

**Description:**
Implement synchronized lyrics display in video using LRC timestamps.

**Acceptance Criteria:**
- [ ] LRC file parsing integrated
- [ ] Lyrics displayed at correct timestamps
- [ ] Text highlighting/color changes for current line
- [ ] Smooth transitions between lines
- [ ] Integration test with Aruhant's LRC files
- [ ] Unit tests for synchronization logic

---

### Story 3.6: Frontend-Backend Integration
**Type:** Issue  
**Assignee:** William  
**Priority:** P0  
**Labels:** `frontend`, `backend`, `integration`, `implementation`

**Description:**
Integrate frontend React application with FastAPI backend, implement async job handling, and complete end-to-end user flow.

**Acceptance Criteria:**
- [ ] Frontend successfully calls backend API endpoints
- [ ] Async job handling implemented for long-running video generation
- [ ] Progress updates displayed in real-time
- [ ] Video download functionality working
- [ ] Error handling across frontend-backend communication
- [ ] End-to-end flow tested (URL input → video download)
- [ ] CORS properly configured

---

## SPRINT 4: Integration, Testing & Demo (Week 4)
**Sprint Goal:** Complete end-to-end integration, fix bugs, optimize performance, and prepare for demo.

**Sprint Dates:** November 25 - December 2, 2025

---

### Story 4.1: End-to-End Integration
**Type:** Issue  
**Assignee:** William  
**Priority:** P0  
**Labels:** `integration`, `implementation`, `core`

**Description:**
Integrate all modules into a complete pipeline from YouTube URL to karaoke video output.

**Acceptance Criteria:**
- [ ] Complete pipeline working end-to-end
- [ ] YouTube URL → MP3 → Vocal Separation → Lyrics + Timestamps → Video
- [ ] Error handling across all integration points
- [ ] Integration tests passing
- [ ] Sample output videos generated successfully
- [ ] Performance meets success criteria (< 5 min for 3-min song)

---

### Story 4.2: Bug Fixes & Performance Optimization
**Type:** Incident  
**Assignee:** Mark  
**Priority:** P0  
**Labels:** `bug-fix`, `optimization`, `qa`, `implementation`

**Description:**
Fix identified bugs and optimize performance to meet success criteria.

**Acceptance Criteria:**
- [ ] All critical bugs fixed
- [ ] Video render time < 5 minutes for 3-minute song
- [ ] Lyric accuracy ≥ 90%
- [ ] Memory usage optimized
- [ ] Error messages clear and actionable

---

### Story 4.3: Fallback Logic & Error Handling
**Type:** Issue  
**Assignee:** Aruhant  
**Priority:** P1  
**Labels:** `integration`, `error-handling`, `fallback`

**Description:**
Implement comprehensive fallback logic for all failure scenarios.

**Acceptance Criteria:**
- [ ] Fallback logic for Demucs failures (Spleeter)
- [ ] Fallback logic for YouTube download failures
- [ ] Fallback logic for lyrics API failures
- [ ] Graceful degradation when components fail
- [ ] User-friendly error messages

---

### Story 4.4: Documentation & Code Quality
**Type:** Task  
**Assignee:** Thomas  
**Priority:** P0  
**Labels:** `documentation`, `code-quality`, `final`

**Description:**
Complete all technical documentation, code comments, and ensure code quality standards.

**Acceptance Criteria:**
- [ ] API documentation complete for all modules
- [ ] Usage examples documented
- [ ] Code comments added to all functions
- [ ] README with setup and usage instructions
- [ ] Architecture document finalized
- [ ] Code review completed

---

### Story 4.5: Demo Preparation
**Type:** Task  
**Assignee:** William  
**Priority:** P0  
**Labels:** `demo`, `presentation`, `final`

**Description:**
Prepare demonstration materials and examples showcasing the complete system.

**Acceptance Criteria:**
- [ ] Demo script prepared
- [ ] Sample karaoke videos generated (3-5 examples)
- [ ] Before/after audio samples for vocal separation
- [ ] Presentation slides created
- [ ] Demo environment tested and ready
- [ ] Troubleshooting guide for demo

---

### Story 4.6: Final QA & Testing
**Type:** Task  
**Assignee:** Thomas  
**Priority:** P0  
**Labels:** `qa`, `testing`, `final`

**Description:**
Conduct comprehensive quality assurance testing across all functionality.

**Acceptance Criteria:**
- [ ] Full system testing completed
- [ ] Test cases cover all major features
- [ ] Edge cases tested
- [ ] Performance benchmarks documented
- [ ] All tests passing
- [ ] Test report generated

---

## Backlog Summary

### Stories by Priority
- **P0 (Critical):** 22 stories
- **P1 (High):** 1 story
- **Total:** 23 stories

---

## GitLab Issue Board Configuration

### Labels to Create
- `audio-acquisition`
- `audio-processing`
- `lyrics-intelligence`
- `video-rendering`
- `frontend`
- `backend`
- `integration`
- `setup`
- `research`
- `implementation`
- `core`
- `fallback`
- `synchronization`
- `optimization`
- `bug-fix`
- `qa`
- `testing`
- `documentation`
- `code-quality`
- `demo`
- `presentation`
- `api`
- `ui`
- `error-handling`
- `lrc`
- `architecture`
- `final`

### Milestones to Create
- **Sprint 1:** Foundation & Research (Nov 4 - Nov 11)
- **Sprint 2:** Core Implementation (Nov 11 - Nov 18)
- **Sprint 3:** Integration & Synchronization (Nov 18 - Nov 25)
- **Sprint 4:** Integration, Testing & Demo (Nov 25 - Dec 2)

### Board Columns
1. **Backlog** - Unassigned stories
2. **To Do** - Assigned, not started
3. **In Progress** - Currently being worked on
4. **Review** - Code review or testing
5. **Done** - Completed and verified

---

## Notes for GitLab Import

### Important GitLab Limitations & Workarounds

1. **Multiple Assignees:** GitLab doesn't support multiple assignees in free tier
   - **Solution:** Assign one person as main assignee, mention others in description: `@username1 @username2`
   - Or use labels like `team::all` to indicate team stories

2. **Acceptance Criteria:** Not a separate field - add in issue description
   - **Format:** Use markdown checklists: `- [ ] Criterion 1`
   - **Location:** Add in the issue description under "## Acceptance Criteria"

### Setup Steps

1. Create all labels (simple format: `audio-acquisition`, `frontend`, `backend`, `setup`, etc.)
2. Create all milestones (Sprint 1-4) with correct dates
3. Create issues for each story (1.0 through 4.6)
4. **For "All Members" stories:** Assign one person, mention others in description
5. Assign issues to correct milestones
6. Add acceptance criteria as markdown checklists in issue descriptions
8. Set up Issue Boards:
   - Product Backlog board (label: `backlog`)
   - One board per sprint using Milestones
9. Tag final release: `git tag v1.0 && git push origin v1.0`

---

**Document Owner:** William Cagas (Technical Lead)  
**Review Date:** Weekly during sprint planning

