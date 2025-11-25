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

### Story 1.1: Project Architecture & Setup
**Type:** Task  
**Assignee:** All Members  
**Story Points:** 8  
**Priority:** P0  
**Labels:** `setup`, `architecture`, `documentation`, `frontend`, `backend`

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

**Tasks:**
- [ ] Create architecture document template
- [ ] Design system architecture diagram
- [ ] Define module interfaces and contracts
- [ ] Set up monorepo Git repository structure
- [ ] Create `frontend/` folder and initialize Vite + React + TypeScript
- [ ] Create `backend/` folder with FastAPI structure (api/, services/, models/)
- [ ] Set up shadcn-ui in frontend
- [ ] Update `.gitignore` for Python (__pycache__, venv, etc.) and Node.js (node_modules, dist, etc.)
- [ ] Create development environment setup guide (frontend and backend)
- [ ] Establish code review process

---

### Story 1.2: YouTube Audio Download Research & Setup
**Type:** Feature  
**Assignee:** Thomas  
**Story Points:** 8  
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

**Tasks:**
- [ ] Research pytube, yt-dlp, and other YouTube download libraries
- [ ] Compare features, reliability, and maintenance status
- [ ] Set up Python virtual environment
- [ ] Install and test primary library (pytube or yt-dlp)
- [ ] Test download with various YouTube URLs
- [ ] Create `src/audio-acquisition/` module structure
- [ ] Document installation and setup process
- [ ] Implement basic URL validation
- [ ] Coordinate with Mark on audio format requirements

---

### Story 1.3: Audio Processing Research & Setup
**Type:** Feature  
**Assignee:** Mark  
**Story Points:** 8  
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

**Tasks:**
- [ ] Research and compare vocal separation libraries (Demucs, Spleeter, others)
- [ ] Set up Python environment with required dependencies
- [ ] Install and test Demucs locally with sample audio files
- [ ] Document installation process and system requirements
- [ ] Run baseline tests on different song genres to assess separation quality
- [ ] Coordinate with Thomas on audio file format requirements (sample rate, bitrate, format)
- [ ] Create initial audio processing module structure

---

### Story 1.4: Lyrics Intelligence Research & Setup
**Type:** Feature  
**Assignee:** Aruhant  
**Story Points:** 8  
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

**Tasks:**
- [ ] Research lyrics APIs (LyricsGenius, Musixmatch, Genius API)
- [ ] Research timestamping solutions (QuickLRC AI, manual sync tools)
- [ ] Set up Python environment with required dependencies
- [ ] Test lyrics fetching with sample songs
- [ ] Create `src/lyrics-intelligence/` module structure
- [ ] Document API keys setup and rate limits
- [ ] Coordinate with team on lyrics format requirements

---

### Story 1.5: Video Rendering Research & Setup
**Type:** Feature  
**Assignee:** William  
**Story Points:** 8  
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

**Tasks:**
- [ ] Research FFmpeg-Python, moviepy, and other video libraries
- [ ] Install FFmpeg on development machine
- [ ] Set up Python environment with required dependencies
- [ ] Test basic video creation with FFmpeg
- [ ] Create `src/video-rendering/` module structure
- [ ] Document FFmpeg installation process
- [ ] Coordinate with team on video format requirements (720p, codec, etc.)

---

## SPRINT 2: Core Implementation (Week 2)
**Sprint Goal:** Implement core functionality for audio acquisition and processing modules, begin lyrics intelligence development.

**Sprint Dates:** November 11 - November 18, 2025

---

### Story 2.1: YouTube to MP3 Conversion Implementation
**Type:** Feature  
**Assignee:** Thomas  
**Story Points:** 13  
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

**Tasks:**
- [ ] Implement YouTube URL validation
- [ ] Implement audio download function
- [ ] Implement MP3 conversion with quality options
- [ ] Add error handling for common failure cases
- [ ] Implement fallback to secondary library (yt-dlp if using pytube)
- [ ] Write unit tests
- [ ] Test with various YouTube URLs and formats
- [ ] Document API and usage examples

---

### Story 2.2: Demucs Vocal Separation Pipeline
**Type:** Feature  
**Assignee:** Mark  
**Story Points:** 13  
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

**Tasks:**
- [ ] Implement Demucs vocal separation pipeline
- [ ] Build audio quality optimization functions (normalization, noise reduction)
- [ ] Create functions to export separated instrumental track
- [ ] Test separation quality across multiple song types (pop, rock, rap, classical)
- [ ] Document processing time benchmarks for different song lengths
- [ ] Begin integration testing with Thomas's MP3 output
- [ ] Write unit tests

---

### Story 2.3: Spleeter Fallback Implementation
**Type:** Feature  
**Assignee:** Mark  
**Story Points:** 8  
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

**Tasks:**
- [ ] Install and configure Spleeter
- [ ] Implement Spleeter separation function
- [ ] Create fallback logic to switch between Demucs and Spleeter
- [ ] Compare quality between both methods
- [ ] Implement error handling
- [ ] Write unit tests

---

### Story 2.4: Lyrics Fetching Implementation
**Type:** Feature  
**Assignee:** Aruhant  
**Story Points:** 13  
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

**Tasks:**
- [ ] Implement lyrics fetching from primary API
- [ ] Implement fallback to secondary API
- [ ] Create song matching logic (fuzzy matching for titles/artists)
- [ ] Add error handling for API failures
- [ ] Implement rate limiting
- [ ] Write unit tests
- [ ] Document API usage and rate limits

---

### Story 2.5: LRC File Generation Foundation
**Type:** Feature  
**Assignee:** Aruhant  
**Story Points:** 8  
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

**Tasks:**
- [ ] Research LRC file format specification
- [ ] Implement LRC file parser
- [ ] Implement LRC file generator
- [ ] Add timestamp format validation
- [ ] Write unit tests
- [ ] Document LRC format and usage

---

## SPRINT 3: Integration & Synchronization (Week 3)
**Sprint Goal:** Complete lyrics timestamping, integrate all modules, and begin video rendering implementation.

**Sprint Dates:** November 18 - November 25, 2025

---

### Story 3.1: Lyrics Timestamp Synchronization
**Type:** Feature  
**Assignee:** Aruhant  
**Story Points:** 13  
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

**Tasks:**
- [ ] Research and integrate QuickLRC AI or timestamping solution
- [ ] Implement timestamp synchronization algorithm
- [ ] Create manual correction interface/tools
- [ ] Test accuracy on diverse song set
- [ ] Optimize for speed and accuracy
- [ ] Write unit tests
- [ ] Document synchronization process

---

### Story 3.2: Audio Processing Integration
**Type:** Feature  
**Assignee:** Mark  
**Story Points:** 8  
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

**Tasks:**
- [ ] Integrate audio processing module with Thomas's audio acquisition system
- [ ] Optimize processing speed (parallel processing, batch operations if needed)
- [ ] Implement error handling for edge cases (corrupted files, unsupported formats)
- [ ] Work with William on audio format requirements for video rendering
- [ ] Conduct quality assurance testing on 10-15 diverse songs
- [ ] Fine-tune separation parameters for best quality/speed balance
- [ ] Begin documentation of API and usage examples

---

### Story 3.3: Video Rendering Foundation
**Type:** Feature  
**Assignee:** William  
**Story Points:** 13  
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

**Tasks:**
- [ ] Implement FFmpeg wrapper functions
- [ ] Create video rendering pipeline
- [ ] Implement text overlay rendering
- [ ] Add background/image support
- [ ] Test with sample audio files
- [ ] Write unit tests
- [ ] Document rendering API

---

### Story 3.4: Lyrics-to-Video Synchronization
**Type:** Feature  
**Assignee:** William  
**Story Points:** 13  
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

**Tasks:**
- [ ] Integrate LRC file parsing
- [ ] Implement timestamp-based lyric display
- [ ] Add text highlighting for current line
- [ ] Implement smooth transitions
- [ ] Test with various LRC files
- [ ] Write unit tests
- [ ] Coordinate with Aruhant on LRC format

---

## SPRINT 4: Integration, Testing & Demo (Week 4)
**Sprint Goal:** Complete end-to-end integration, fix bugs, optimize performance, and prepare for demo.

**Sprint Dates:** November 25 - December 2, 2025

---

### Story 4.1: End-to-End Integration
**Type:** Feature  
**Assignee:** All Members  
**Story Points:** 21  
**Priority:** P0  
**Labels:** `integration`, `core`, `critical`

**Description:**
Integrate all modules into a complete pipeline from YouTube URL to karaoke video output.

**Acceptance Criteria:**
- [ ] Complete pipeline working end-to-end
- [ ] YouTube URL → MP3 → Vocal Separation → Lyrics + Timestamps → Video
- [ ] Error handling across all integration points
- [ ] Integration tests passing
- [ ] Sample output videos generated successfully
- [ ] Performance meets success criteria (< 5 min for 3-min song)

**Tasks:**
- [ ] Integrate audio acquisition with audio processing
- [ ] Integrate audio processing with lyrics intelligence
- [ ] Integrate lyrics intelligence with video rendering
- [ ] Create main pipeline orchestrator
- [ ] Implement comprehensive error handling
- [ ] Write integration tests
- [ ] Test with multiple sample songs
- [ ] Performance benchmarking

---

### Story 4.2: Bug Fixes & Performance Optimization
**Type:** Bug  
**Assignee:** All Members  
**Story Points:** 13  
**Priority:** P0  
**Labels:** `bug-fix`, `optimization`, `qa`

**Description:**
Fix identified bugs and optimize performance to meet success criteria.

**Acceptance Criteria:**
- [ ] All critical bugs fixed
- [ ] Video render time < 5 minutes for 3-minute song
- [ ] Lyric accuracy ≥ 90%
- [ ] Memory usage optimized
- [ ] Error messages clear and actionable

**Tasks:**
- [ ] Identify and prioritize bugs
- [ ] Fix critical bugs
- [ ] Optimize video rendering speed
- [ ] Optimize audio processing speed
- [ ] Improve lyric accuracy
- [ ] Optimize memory usage
- [ ] Improve error messages

---

### Story 4.3: Fallback Logic & Error Handling
**Type:** Feature  
**Assignee:** All Members  
**Story Points:** 8  
**Priority:** P1  
**Labels:** `error-handling`, `fallback`, `reliability`

**Description:**
Implement comprehensive fallback logic for all failure scenarios.

**Acceptance Criteria:**
- [ ] Fallback logic for Demucs failures (Spleeter)
- [ ] Fallback logic for YouTube download failures
- [ ] Fallback logic for lyrics API failures
- [ ] Graceful degradation when components fail
- [ ] User-friendly error messages

**Tasks:**
- [ ] Create fallback logic if Demucs fails
- [ ] Implement YouTube download fallback
- [ ] Implement lyrics API fallback
- [ ] Add graceful error handling
- [ ] Test all failure scenarios
- [ ] Document error handling behavior

---

### Story 4.4: Documentation & Code Quality
**Type:** Task  
**Assignee:** All Members  
**Story Points:** 8  
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

**Tasks:**
- [ ] Finalize technical documentation and code comments
- [ ] Create comprehensive README
- [ ] Document API for each module
- [ ] Add usage examples
- [ ] Complete architecture document
- [ ] Code review and cleanup
- [ ] Finalize repository organization

---

### Story 4.5: Demo Preparation
**Type:** Task  
**Assignee:** All Members  
**Story Points:** 8  
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

**Tasks:**
- [ ] Prepare audio processing demonstration examples
- [ ] Generate sample karaoke videos
- [ ] Create before/after audio samples showcasing vocal separation
- [ ] Prepare demo script
- [ ] Create presentation slides
- [ ] Test demo environment
- [ ] Prepare troubleshooting guide
- [ ] Practice demo run-through

---

### Story 4.6: Final QA & Testing
**Type:** Task  
**Assignee:** All Members  
**Story Points:** 13  
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

**Tasks:**
- [ ] Participate in full system testing and QA
- [ ] Test with diverse song genres
- [ ] Test edge cases (very short songs, very long songs, instrumental-only)
- [ ] Performance testing
- [ ] User acceptance testing
- [ ] Generate test report
- [ ] Fix any remaining issues

---

## Backlog Summary

### Total Story Points by Sprint
- **Sprint 1:** 40 points
- **Sprint 2:** 55 points
- **Sprint 3:** 47 points
- **Sprint 4:** 71 points
- **Total:** 213 points

### Stories by Priority
- **P0 (Critical):** 15 stories
- **P1 (High):** 1 story

---

## GitLab Issue Board Configuration

### Labels to Create
- `audio-acquisition`
- `audio-processing`
- `lyrics-intelligence`
- `video-rendering`
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
- `documentation`
- `demo`
- `critical`
- `lrc`
- `frontend`
- `backend`

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

1. Create all labels using `namespace::value` format (e.g., `type::story`, `priority::high`, `sprint::1`)
2. Create all milestones (Sprint 1-4) with correct dates
3. Create issues for each story (1.1 through 4.6)
4. Assign issues to appropriate team members
5. Assign issues to correct milestones
6. Set story points using GitLab's weight system
7. Add acceptance criteria as task checklists in issue descriptions
8. Set up Issue Boards:
   - Product Backlog board (label: `backlog`)
   - One board per sprint using Milestones
9. Tag final release: `git tag v1.0 && git push origin v1.0`

---

**Document Owner:** William Cagas (Technical Lead)  
**Review Date:** Weekly during sprint planning

