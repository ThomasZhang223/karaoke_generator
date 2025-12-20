# KARAOKE VIDEO GENERATOR — TEST PLAN

**Document Version:** 1.0  
**Date Created:** November 25, 2025  
**Last Updated:** November 25, 2025

---

## Overview

This document outlines the comprehensive test plan for the Karaoke Video Generator project, based on the requirements specified in the product backlog. The plan covers unit tests, integration tests, end-to-end tests, and performance benchmarks.

**Testing Framework Recommendations:**
- **Backend (Python):** `pytest` with `pytest-asyncio` for async tests
- **Frontend (TypeScript/React):** `Vitest` (comes with Vite) or `Jest` + `React Testing Library`
- **API Testing:** `pytest` with `httpx` or `TestClient` from FastAPI
- **Performance Testing:** Custom benchmarks using `time` module

---

## Test Categories

### 1. Unit Tests
Test individual functions and classes in isolation.

### 2. Integration Tests
Test interactions between modules (e.g., audio acquisition → audio processing).

### 3. End-to-End Tests
Test complete user flows from YouTube URL to video output.

### 4. Performance Tests
Verify performance benchmarks (render time < 5 min, lyric accuracy ≥ 90%).

### 5. Error Handling Tests
Test fallback mechanisms and error scenarios.

---

## Test Requirements by Module

### Module 1: Audio Acquisition (`backend/core/audio_acquisition/`)

**Story:** 2.1 - YouTube to MP3 Conversion Implementation  
**Assignee:** Thomas

#### Unit Tests Required:

1. **URL Validation Tests** (`test_downloader.py`)
   - [ ] Valid YouTube URL formats (standard, short, playlist, with parameters)
   - [ ] Invalid URL formats (non-YouTube URLs, malformed URLs)
   - [ ] Video ID extraction from various URL formats
   - [ ] Edge cases (empty string, None, special characters)

2. **Download Function Tests**
   - [ ] Successful download with valid URL
   - [ ] MP3 conversion with different bitrates (128, 192, 256)
   - [ ] Different sample rates (44.1kHz, 48kHz)
   - [ ] Error handling for network failures
   - [ ] Error handling for unavailable/private videos
   - [ ] Error handling for age-restricted content
   - [ ] Output file format validation
   - [ ] File size and duration validation

3. **Fallback Mechanism Tests**
   - [ ] Primary library failure triggers fallback
   - [ ] Fallback library succeeds when primary fails
   - [ ] Both libraries fail gracefully

4. **AudioFile Data Class Tests**
   - [ ] Correct metadata extraction (duration, bitrate, file_size)
   - [ ] Status enum transitions
   - [ ] Created timestamp accuracy

**Test File:** `backend/core/audio_acquisition/test_downloader.py`

---

### Module 2: Audio Processing (`backend/core/audio_processing/`)

**Stories:** 2.2 - Demucs Pipeline, 2.3 - Spleeter Fallback  
**Assignee:** Mark

#### Unit Tests Required:

1. **Vocal Separation Tests** (`test_separator.py`)
   - [ ] Demucs separation produces valid output files
   - [ ] Instrumental track is generated correctly
   - [ ] Output audio format matches input format
   - [ ] Processing handles different audio formats (MP3, WAV)
   - [ ] Error handling for corrupted audio files
   - [ ] Error handling for unsupported formats

2. **Audio Optimization Tests** (`test_optimizer.py`)
   - [ ] Normalization function works correctly
   - [ ] Noise reduction improves audio quality
   - [ ] Quality metrics are calculated accurately
   - [ ] Optimization doesn't break audio file

3. **Fallback Mechanism Tests** (`test_separator.py`)
   - [ ] Spleeter fallback activates when Demucs fails
   - [ ] Spleeter produces valid output when used
   - [ ] Quality comparison between Demucs and Spleeter
   - [ ] Error handling when both methods fail

4. **Performance Benchmarks**
   - [ ] Processing time for 1-minute song
   - [ ] Processing time for 3-minute song
   - [ ] Processing time for 5-minute song
   - [ ] Memory usage during processing

**Test Files:**
- `backend/core/audio_processing/test_separator.py`
- `backend/core/audio_processing/test_optimizer.py`

#### Integration Tests Required:

1. **Audio Acquisition → Processing Integration**
   - [ ] MP3 from downloader works with separator
   - [ ] File format compatibility
   - [ ] Error propagation from downloader to processor

**Test File:** `backend/tests/integration/test_audio_pipeline.py`

---

### Module 3: Lyrics Intelligence (`backend/core/lyrics_intelligence/`)

**Stories:** 2.4 - Lyrics Fetching, 2.5 - LRC Generation, 3.2 - Timestamp Synchronization  
**Assignee:** Aruhant

#### Unit Tests Required:

1. **Lyrics Fetching Tests** (`test_scraper.py`)
   - [ ] Successful lyrics fetch from primary API
   - [ ] Fallback to secondary API when primary fails
   - [ ] Song title and artist matching logic
   - [ ] Handling of missing lyrics
   - [ ] API rate limiting handling
   - [ ] Error handling for API failures (network, 404, 500)
   - [ ] Special characters in lyrics (unicode, emojis)
   - [ ] Multiple verses and sections

2. **LRC File Parsing Tests** (`test_synchronizer.py`)
   - [ ] Valid LRC file parsing
   - [ ] Timestamp format validation ([mm:ss.ff])
   - [ ] Multiple timestamp formats handled
   - [ ] Empty lines and metadata tags
   - [ ] Invalid timestamp formats rejected
   - [ ] Edge cases (missing timestamps, out-of-order timestamps)

3. **LRC File Generation Tests** (`test_synchronizer.py`)
   - [ ] LRC file generation from lyrics and timestamps
   - [ ] Correct timestamp formatting
   - [ ] File encoding (UTF-8)
   - [ ] Metadata tags included correctly

4. **Timestamp Synchronization Tests** (`test_synchronizer.py`)
   - [ ] Synchronization algorithm accuracy (≥ 90%)
   - [ ] Integration with QuickLRC AI (if used)
   - [ ] Manual correction tools work correctly
   - [ ] Timestamps align with audio correctly
   - [ ] Edge cases (instrumental sections, spoken parts)

**Test Files:**
- `backend/core/lyrics_intelligence/test_scraper.py`
- `backend/core/lyrics_intelligence/test_synchronizer.py`

#### Integration Tests Required:

1. **Lyrics → Synchronization Integration**
   - [ ] Fetched lyrics work with synchronizer
   - [ ] LRC file generation from fetched lyrics
   - [ ] Integration test with actual audio files

**Test File:** `backend/tests/integration/test_lyrics_pipeline.py`

---

### Module 4: Video Rendering (`backend/core/video_rendering/`)

**Stories:** 3.4 - Video Rendering Foundation, 3.5 - Lyrics-to-Video Synchronization  
**Assignee:** William

#### Unit Tests Required:

1. **FFmpeg Integration Tests** (`test_renderer.py`)
   - [ ] FFmpeg is accessible from Python
   - [ ] Basic video creation (720p resolution)
   - [ ] Video format validation (MP4, codec)
   - [ ] Error handling when FFmpeg is not installed

2. **Text Overlay Tests** (`test_overlay.py`)
   - [ ] Text overlay functionality
   - [ ] Font size and color customization
   - [ ] Text positioning (center, left, right)
   - [ ] Multi-line text handling
   - [ ] Special characters in text

3. **Background/Image Support Tests** (`test_renderer.py`)
   - [ ] Solid color backgrounds
   - [ ] Image backgrounds
   - [ ] Background scaling and positioning

4. **Lyrics Synchronization Tests** (`test_renderer.py`)
   - [ ] Lyrics displayed at correct timestamps
   - [ ] Text highlighting/color changes for current line
   - [ ] Smooth transitions between lines
   - [ ] Multiple lines displayed correctly
   - [ ] Edge cases (no lyrics, missing timestamps)

**Test Files:**
- `backend/core/video_rendering/test_renderer.py`
- `backend/core/video_rendering/test_overlay.py`

#### Integration Tests Required:

1. **LRC → Video Integration**
   - [ ] LRC file parsing integrated correctly
   - [ ] Lyrics appear at correct times in video
   - [ ] Integration test with Aruhant's LRC files

**Test File:** `backend/tests/integration/test_video_pipeline.py`

---

### Module 5: Backend API (`backend/api/` and `backend/main.py`)

**Stories:** 2.6 - FastAPI Setup, 3.6 - Frontend-Backend Integration  
**Assignee:** William

#### Unit Tests Required:

1. **API Endpoint Tests** (`test_api.py`)
   - [ ] Health check endpoint (`/health`)
   - [ ] Root endpoint (`/`)
   - [ ] CORS middleware configured correctly
   - [ ] Error handling middleware works
   - [ ] API documentation accessible (Swagger)

2. **Karaoke Generation Endpoint Tests** (`test_api.py`)
   - [ ] POST endpoint accepts YouTube URL
   - [ ] Request validation (URL format)
   - [ ] Async job handling
   - [ ] Progress updates endpoint
   - [ ] Video download endpoint
   - [ ] Error responses (400, 500)

**Test File:** `backend/tests/test_api.py`

#### Integration Tests Required:

1. **End-to-End API Tests**
   - [ ] Complete flow: URL → Video generation → Download
   - [ ] Progress updates work correctly
   - [ ] Error handling across all endpoints

**Test File:** `backend/tests/integration/test_e2e_api.py`

---

### Module 6: Frontend (`frontend/src/`)

**Story:** 3.1 - Frontend UI Implementation  
**Assignee:** William

#### Unit Tests Required:

1. **Component Tests** (using React Testing Library)
   - [ ] `UrlForm` component renders correctly
   - [ ] URL input validation
   - [ ] Form submission
   - [ ] Error message display
   - [ ] `GenerationProgress` component displays progress
   - [ ] `VideoResult` component displays video
   - [ ] `ErrorBanner` component displays errors

2. **API Client Tests** (`test_apiClient.ts`)
   - [ ] API client makes correct requests
   - [ ] Error handling for API failures
   - [ ] Progress polling works
   - [ ] Video download functionality

**Test Files:**
- `frontend/src/components/karaoke/__tests__/UrlForm.test.tsx`
- `frontend/src/components/karaoke/__tests__/GenerationProgress.test.tsx`
- `frontend/src/components/karaoke/__tests__/VideoResult.test.tsx`
- `frontend/src/lib/__tests__/apiClient.test.ts`

#### Integration Tests Required:

1. **Frontend-Backend Integration**
   - [ ] Frontend successfully calls backend
   - [ ] Progress updates displayed in real-time
   - [ ] Video download works
   - [ ] Error handling across communication

**Test File:** `frontend/src/__tests__/integration.test.tsx`

---

## End-to-End Tests

**Story:** 4.1 - End-to-End Integration  
**Assignee:** William

### Complete Pipeline Tests

1. **Happy Path Test**
   - [ ] YouTube URL → MP3 → Vocal Separation → Lyrics + Timestamps → Video
   - [ ] All modules work together
   - [ ] Output video is valid and playable
   - [ ] Video contains synchronized lyrics

2. **Error Scenarios**
   - [ ] Invalid YouTube URL
   - [ ] Unavailable video
   - [ ] Lyrics not found
   - [ ] Audio processing failure
   - [ ] Video rendering failure

**Test File:** `backend/tests/e2e/test_complete_pipeline.py`

---

## Performance Tests

**Story:** 4.2 - Bug Fixes & Performance Optimization  
**Assignee:** Mark

### Performance Benchmarks

1. **Video Render Time**
   - [ ] 3-minute song renders in < 5 minutes
   - [ ] 1-minute song renders in < 2 minutes
   - [ ] 5-minute song renders in < 8 minutes

2. **Lyric Accuracy**
   - [ ] ≥ 90% accuracy for test songs (10-15 diverse songs)
   - [ ] Test across different genres (pop, rock, hip-hop, etc.)

3. **Memory Usage**
   - [ ] Memory usage stays within reasonable limits
   - [ ] No memory leaks during processing

4. **Processing Speed**
   - [ ] Audio download time < 30 seconds
   - [ ] Vocal separation time < 3 minutes for 3-minute song
   - [ ] Lyrics synchronization time < 1 minute

**Test File:** `backend/tests/performance/test_benchmarks.py`

---

## Error Handling & Fallback Tests

**Story:** 4.3 - Fallback Logic & Error Handling  
**Assignee:** Aruhant

### Fallback Mechanism Tests

1. **Demucs → Spleeter Fallback**
   - [ ] Demucs failure triggers Spleeter
   - [ ] Spleeter produces valid output
   - [ ] User receives appropriate error message

2. **YouTube Download Fallback**
   - [ ] Primary download method failure triggers fallback
   - [ ] Fallback method succeeds
   - [ ] Both methods fail gracefully

3. **Lyrics API Fallback**
   - [ ] Primary API failure triggers secondary API
   - [ ] Secondary API succeeds
   - [ ] Both APIs fail gracefully

4. **Graceful Degradation**
   - [ ] System continues with partial data when possible
   - [ ] User-friendly error messages
   - [ ] No crashes or unhandled exceptions

**Test File:** `backend/tests/integration/test_fallback_mechanisms.py`

---

## Quality Assurance Tests

**Story:** 4.6 - Final QA & Testing  
**Assignee:** Thomas

### Comprehensive Test Suite

1. **Test Coverage**
   - [ ] All major features covered
   - [ ] Edge cases tested
   - [ ] Code coverage ≥ 80% (target)

2. **Test Cases Documentation**
   - [ ] Test cases documented for all features
   - [ ] Test data prepared (sample audio files, LRC files)
   - [ ] Test environment setup documented

3. **Test Report**
   - [ ] All tests passing
   - [ ] Performance benchmarks documented
   - [ ] Known issues documented
   - [ ] Test report generated

**Test Files:** All test files listed above

---

## Test Data Requirements

### Sample Audio Files
- Short song (1 minute)
- Medium song (3 minutes)
- Long song (5 minutes)
- Different genres (pop, rock, hip-hop, classical)
- Different audio qualities (128kbps, 192kbps, 256kbps)

### Sample LRC Files
- Valid LRC with timestamps
- LRC with metadata tags
- LRC with missing timestamps
- LRC with out-of-order timestamps

### Sample YouTube URLs
- Standard YouTube URL
- Short YouTube URL (youtu.be)
- Playlist URL
- Invalid URLs for error testing

---

## Test Execution Strategy

### Development Phase
- Run unit tests before committing code
- Run integration tests before merging PRs
- Run relevant tests for the module being worked on

### Pre-Release Phase
- Run full test suite
- Run performance benchmarks
- Run end-to-end tests
- Generate test coverage report

### Continuous Integration (if set up)
- Run all tests on every push
- Run tests on multiple Python versions
- Run tests on different operating systems

---

## Test Environment Setup

### Backend Testing
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=backend --cov-report=html

# Run specific test file
pytest backend/core/audio_acquisition/test_downloader.py
```

### Frontend Testing
```bash
# Install test dependencies (if using Vitest)
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Run tests
npm run test

# Run with coverage
npm run test:coverage
```

---

## Success Criteria

Based on backlog requirements:

1. **All Unit Tests Passing**
   - [ ] All unit tests for core functions pass
   - [ ] Code coverage ≥ 80%

2. **All Integration Tests Passing**
   - [ ] Integration tests between modules pass
   - [ ] End-to-end pipeline test passes

3. **Performance Benchmarks Met**
   - [ ] Video render time < 5 minutes for 3-minute song
   - [ ] Lyric accuracy ≥ 90%

4. **Error Handling Verified**
   - [ ] All fallback mechanisms tested
   - [ ] Error messages are user-friendly

5. **Test Report Generated**
   - [ ] Test report documents all test results
   - [ ] Performance benchmarks documented

---

## Test Files Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_api.py                    # API endpoint tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_audio_pipeline.py      # Audio acquisition → processing
│   │   ├── test_lyrics_pipeline.py     # Lyrics → synchronization
│   │   ├── test_video_pipeline.py     # LRC → video rendering
│   │   ├── test_e2e_api.py            # Frontend-backend integration
│   │   └── test_fallback_mechanisms.py # Fallback logic tests
│   ├── e2e/
│   │   ├── __init__.py
│   │   └── test_complete_pipeline.py   # Complete end-to-end test
│   └── performance/
│       ├── __init__.py
│       └── test_benchmarks.py         # Performance benchmarks
│
├── core/
│   ├── audio_acquisition/
│   │   └── test_downloader.py         # Unit tests for downloader
│   ├── audio_processing/
│   │   ├── test_separator.py          # Unit tests for separator
│   │   └── test_optimizer.py          # Unit tests for optimizer
│   ├── lyrics_intelligence/
│   │   ├── test_scraper.py            # Unit tests for scraper
│   │   └── test_synchronizer.py       # Unit tests for synchronizer
│   └── video_rendering/
│       ├── test_renderer.py           # Unit tests for renderer
│       └── test_overlay.py            # Unit tests for overlay

frontend/
├── src/
│   ├── __tests__/
│   │   └── integration.test.tsx       # Frontend integration tests
│   ├── components/
│   │   └── karaoke/
│   │       └── __tests__/
│   │           ├── UrlForm.test.tsx
│   │           ├── GenerationProgress.test.tsx
│   │           └── VideoResult.test.tsx
│   └── lib/
│       └── __tests__/
│           └── apiClient.test.ts
```

---

## Notes

- **Mocking External Services:** Use mocks for YouTube downloads, lyrics APIs, and AI models in unit tests to avoid external dependencies and speed up tests.
- **Test Data:** Store test audio files, LRC files, and sample URLs in `backend/tests/fixtures/` directory.
- **CI/CD:** Consider setting up GitHub Actions or GitLab CI to run tests automatically.
- **Test Maintenance:** Update tests when requirements change or bugs are fixed.

---

**Document Owner:** William Cagas (Technical Lead)  
**Review Date:** Weekly during sprint planning





