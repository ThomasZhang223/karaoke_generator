# KARAOKE VIDEO GENERATOR — USE CASES

**Document Version:** 1.0  
**Date Created:** November 25, 2025  
**Last Updated:** November 25, 2025

---

## Overview

This document describes the use cases for the Karaoke Video Generator system. Each use case includes actors, preconditions, main flow, alternative flows, and postconditions.

---

## Actors

- **User:** End user who wants to generate a karaoke video
- **System:** The Karaoke Video Generator application
- **YouTube:** External service for audio source
- **Lyrics API:** External service for lyrics retrieval (e.g., LyricsGenius)
- **AI Model:** Vocal separation model (Demucs/Spleeter)

---

## Use Cases

### UC-1: Generate Karaoke Video from YouTube URL

**Actor:** User  
**Preconditions:**
- User has access to the web application
- User has a valid YouTube URL for a song
- System is operational and all services are available

**Main Flow:**
1. User navigates to the application
2. User enters a YouTube URL in the input field
3. User clicks "Generate Karaoke Video" button
4. System validates the YouTube URL
5. System downloads audio from YouTube
6. System processes audio to separate vocals (creates instrumental track)
7. System fetches lyrics for the song
8. System synchronizes lyrics with audio timestamps
9. System generates LRC file with timestamps
10. System renders video with instrumental audio and synchronized lyrics overlay
11. System displays the completed video
12. User can download the video file

**Alternative Flows:**

**3a. Invalid YouTube URL:**
- 3a.1. System displays error message: "Invalid YouTube URL. Please check and try again."
- 3a.2. Use case ends

**5a. YouTube download fails:**
- 5a.1. System attempts fallback download method
- 5a.2. If fallback succeeds, continue to step 6
- 5a.3. If fallback fails, display error: "Unable to download audio. Please try a different URL."
- 5a.4. Use case ends

**6a. Vocal separation fails:**
- 6a.1. System attempts fallback separation method (Spleeter if Demucs fails)
- 6a.2. If fallback succeeds, continue to step 7
- 6a.3. If fallback fails, display error: "Audio processing failed. Please try again."
- 6a.4. Use case ends

**7a. Lyrics not found:**
- 7a.1. System attempts fallback lyrics API
- 7a.2. If fallback succeeds, continue to step 8
- 7a.3. If fallback fails, display error: "Lyrics not available for this song."
- 7a.4. Use case ends

**8a. Lyric synchronization fails:**
- 8a.1. System uses basic timestamp estimation
- 8a.2. Continue to step 9 with estimated timestamps
- 8a.3. Display warning: "Lyrics may not be perfectly synchronized"

**Postconditions:**
- Karaoke video is generated and available for download
- Video file is stored temporarily on the server
- User has access to download the video

**Priority:** P0 (Critical)

---

### UC-2: View Generation Progress

**Actor:** User  
**Preconditions:**
- User has initiated a karaoke video generation (UC-1)
- Generation process is in progress

**Main Flow:**
1. User views the progress page
2. System displays current stage of generation:
   - "Downloading audio..." (0-20%)
   - "Processing audio..." (20-50%)
   - "Fetching lyrics..." (50-70%)
   - "Rendering video..." (70-100%)
3. System updates progress percentage in real-time
4. User can see estimated time remaining
5. When complete, system redirects to video display page

**Alternative Flows:**

**2a. Generation fails:**
- 2a.1. System displays error message with details
- 2a.2. User can retry or return to home page

**Postconditions:**
- User is aware of generation progress
- User can see when video is ready

**Priority:** P1 (High)

---

### UC-3: Download Generated Video

**Actor:** User  
**Preconditions:**
- Video generation is complete (UC-1)
- Video file is available on the server

**Main Flow:**
1. User views the completed video
2. User clicks "Download" button
3. System initiates video file download
4. Video file downloads to user's device

**Alternative Flows:**

**2a. Video file not found:**
- 2a.1. System displays error: "Video file not available. Please regenerate."
- 2a.2. Use case ends

**Postconditions:**
- Video file is downloaded to user's device
- User can use the video file

**Priority:** P0 (Critical)

---

### UC-4: Handle Error Scenarios

**Actor:** User, System  
**Preconditions:**
- User is interacting with the system
- An error condition occurs

**Main Flow:**
1. System detects an error condition
2. System logs the error for debugging
3. System displays user-friendly error message
4. System provides actionable next steps (retry, contact support, etc.)
5. User can retry the operation or navigate away

**Error Types:**
- Invalid YouTube URL
- Network connectivity issues
- Audio processing failures
- Lyrics API failures
- Video rendering failures
- Server errors

**Postconditions:**
- Error is logged
- User is informed of the issue
- System remains stable

**Priority:** P0 (Critical)

---

## Use Case Diagram Relationships

```
User --(initiates)--> UC-1: Generate Karaoke Video
User --(monitors)--> UC-2: View Generation Progress
User --(downloads)--> UC-3: Download Generated Video
System --(handles)--> UC-4: Handle Error Scenarios

UC-1 --(includes)--> UC-2
UC-1 --(extends)--> UC-4
UC-1 --(precedes)--> UC-3
```

---

## Traceability

### Backlog Traceability
- **UC-1** → Stories 1.2, 2.1, 2.2, 2.4, 3.1, 3.3, 3.4, 4.1
- **UC-2** → Story 4.1 (Integration)
- **UC-3** → Story 4.1 (Integration)
- **UC-4** → Stories 2.1, 2.2, 2.4, 4.2, 4.3

### User Stories Traceability
- **UC-1** → US-1, US-2, US-3, US-4
- **UC-2** → US-5
- **UC-3** → US-6
- **UC-4** → All user stories (error handling)

---

**Document Owner:** Technical Lead (William Cagas)  
**Review Frequency:** As requirements evolve
