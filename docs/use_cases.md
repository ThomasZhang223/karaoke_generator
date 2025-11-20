# USE CASES — KARAOKE VIDEO GENERATOR

**Document Version:** 1.0  
**Date Created:** November 5, 2025  
**Project:** Karaoke Video Generator

---

## Overview

This document describes the primary use cases for the Karaoke Video Generator system. Each use case outlines the interactions between users and the system to achieve specific goals.

---

## Use Case 1: Generate Karaoke Video from YouTube URL

**ID:** UC-001  
**Priority:** High  
**Actors:** End User (Content Creator, Karaoke Enthusiast, Musician)

### Description
A user provides a YouTube URL for a song, and the system automatically generates a karaoke video with synchronized lyrics, vocal-separated audio, and visual text overlays.

### Preconditions
- User has a valid YouTube URL for a song
- System has internet connectivity
- Required dependencies (Demucs, FFmpeg, etc.) are installed

### Main Success Scenario
1. User launches the application
2. User provides a YouTube URL as input
3. System validates the URL format
4. System downloads the video/audio from YouTube
5. System converts the media to MP3 format
6. System performs AI-based vocal separation (Demucs)
7. System extracts lyrics from the song (using LyricsGenius or similar)
8. System synchronizes lyrics with audio timestamps
9. System generates an LRC file with timing information
10. System renders a 720p video with synchronized lyrics overlay
11. System saves the output karaoke video file
12. System notifies user of successful completion

### Alternative Flows

**3a. Invalid YouTube URL**
- 3a.1. System displays error message
- 3a.2. Use case terminates

**4a. YouTube download fails**
- 4a.1. System attempts fallback method (yt-dlp or pytube)
- 4a.2. If all methods fail, system displays error and terminates

**6a. Vocal separation quality is poor**
- 6a.1. System attempts fallback method (Spleeter)
- 6a.2. If quality remains poor, system continues with best available result

**7a. Lyrics not found**
- 7a.1. System attempts alternative lyrics sources
- 7a.2. If no lyrics found, system displays warning and continues without lyrics

**8a. Timestamp synchronization fails**
- 8a.1. System uses QuickLRC AI for timestamp estimation
- 8a.2. If estimation fails, system uses manual correction or default timing

**10a. Video rendering fails**
- 10a.1. System logs error details
- 10a.2. System displays error message to user
- 10a.3. Use case terminates

### Postconditions
- Karaoke video file is generated and saved (on success)
- User receives notification of completion status
- Temporary files are cleaned up

### Success Criteria
- Video render time < 5 minutes for a 3-minute song
- ≥ 90% lyric accuracy
- Output video is 720p resolution
- Lyrics are synchronized with audio

---

## Use Case 2: Process Audio File (MP3) for Karaoke

**ID:** UC-002  
**Priority:** Medium  
**Actors:** End User

### Description
A user provides an existing MP3 audio file, and the system processes it to create a karaoke video without requiring YouTube download.

### Preconditions
- User has a valid MP3 audio file
- File is accessible to the system

### Main Success Scenario
1. User launches the application
2. User selects "Process Audio File" option
3. User provides path to MP3 file
4. System validates file format and accessibility
5. System performs AI-based vocal separation
6. System extracts lyrics (using song metadata or manual input)
7. System synchronizes lyrics with audio timestamps
8. System generates LRC file
9. System renders 720p karaoke video
10. System saves output file
11. System notifies user of completion

### Alternative Flows

**4a. Invalid or inaccessible file**
- 4a.1. System displays error message
- 4a.2. Use case terminates

**6a. Lyrics cannot be extracted automatically**
- 6a.1. System prompts user to provide lyrics manually
- 6a.2. User provides lyrics text
- 6a.3. System continues with manual lyrics

### Postconditions
- Karaoke video is generated from audio file
- Original audio file remains unchanged

---

## Use Case 3: Generate LRC File from Song

**ID:** UC-003  
**Priority:** Medium  
**Actors:** End User

### Description
A user requests generation of an LRC (Lyrics with timestamps) file for a song without generating the full video.

### Preconditions
- User has audio file or YouTube URL
- Song has available lyrics

### Main Success Scenario
1. User launches the application
2. User selects "Generate LRC File" option
3. User provides audio source (URL or file path)
4. System processes audio to extract timing information
5. System retrieves lyrics
6. System synchronizes lyrics with audio timestamps
7. System generates LRC file
8. System saves LRC file to disk
9. System notifies user of completion

### Alternative Flows

**5a. Lyrics not found**
- 5a.1. System prompts for manual lyrics input
- 5a.2. User provides lyrics
- 5a.3. System continues with manual lyrics

**6a. Synchronization fails**
- 6a.1. System uses QuickLRC AI for estimation
- 6a.2. System generates LRC with estimated timestamps

### Postconditions
- LRC file is generated and saved
- File can be used for future video generation

---

## Use Case 4: Perform Vocal Separation Only

**ID:** UC-004  
**Priority:** Low  
**Actors:** End User, Musician

### Description
A user requests only the vocal separation functionality to extract instrumental or vocal-only tracks from a song.

### Preconditions
- User has audio file or YouTube URL

### Main Success Scenario
1. User launches the application
2. User selects "Vocal Separation" option
3. User provides audio source
4. System downloads/converts audio if needed
5. System performs AI-based vocal separation (Demucs)
6. System generates separate audio tracks (instrumental, vocals)
7. System saves separated audio files
8. System notifies user of completion

### Alternative Flows

**5a. Demucs separation fails**
- 5a.1. System attempts Spleeter fallback
- 5a.2. If both fail, system displays error

### Postconditions
- Instrumental and vocal tracks are saved as separate files
- Original audio remains unchanged

---

## Use Case 5: Batch Process Multiple Songs

**ID:** UC-005  
**Priority:** Low  
**Actors:** Content Creator

### Description
A user provides multiple YouTube URLs or audio files, and the system processes them sequentially to generate multiple karaoke videos.

### Preconditions
- User has list of valid URLs or file paths
- System has sufficient storage space

### Main Success Scenario
1. User launches the application
2. User selects "Batch Process" option
3. User provides list of URLs or file paths
4. System validates all inputs
5. For each item in the list:
   - System processes the song (UC-001 or UC-002)
   - System saves output with unique filename
   - System logs progress
6. System generates summary report
7. System notifies user of batch completion

### Alternative Flows

**4a. Some inputs are invalid**
- 4a.1. System skips invalid inputs
- 4a.2. System logs skipped items
- 4a.3. System continues with valid inputs

**5a. Processing fails for one item**
- 5a.1. System logs error for that item
- 5a.2. System continues with next item

### Postconditions
- All successfully processed videos are saved
- Summary report shows success/failure counts

---

## Use Case 6: Customize Video Output Settings

**ID:** UC-006  
**Priority:** Low  
**Actors:** Content Creator

### Description
A user customizes video rendering settings such as resolution, text styling, or background before generating the karaoke video.

### Preconditions
- User is in the process of generating a karaoke video

### Main Success Scenario
1. User initiates video generation (UC-001 or UC-002)
2. System presents customization options
3. User selects desired settings:
   - Resolution (default: 720p)
   - Text color, font, size
   - Background style
4. User confirms settings
5. System proceeds with video generation using custom settings
6. System saves output with custom styling

### Alternative Flows

**3a. User selects invalid settings**
- 3a.1. System validates and corrects to nearest valid option
- 3a.2. System notifies user of correction

### Postconditions
- Video is generated with user-specified customizations

---

## Use Case 7: View Processing Status and Logs

**ID:** UC-007  
**Priority:** Low  
**Actors:** End User

### Description
A user monitors the progress of a karaoke video generation process and views detailed logs.

### Preconditions
- A video generation process is running

### Main Success Scenario
1. User initiates video generation
2. System displays progress indicator
3. System shows current processing stage:
   - Downloading
   - Converting
   - Separating vocals
   - Extracting lyrics
   - Synchronizing
   - Rendering video
4. System updates progress percentage
5. User can view detailed logs if needed
6. System completes and shows final status

### Postconditions
- User is informed of processing status throughout
- Logs are available for troubleshooting

---

## Use Case 8: Handle Processing Errors Gracefully

**ID:** UC-008  
**Priority:** High  
**Actors:** System, End User

### Description
The system detects and handles various error conditions during processing, providing clear feedback to the user.

### Preconditions
- System is processing a request

### Main Success Scenario
1. System encounters an error during processing
2. System identifies error type:
   - Network error (YouTube download)
   - File I/O error
   - Processing failure (Demucs, FFmpeg)
   - API error (lyrics service)
3. System attempts automatic recovery (fallback methods)
4. If recovery succeeds, system continues processing
5. If recovery fails, system logs error details
6. System displays user-friendly error message
7. System provides suggestions for resolution
8. System cleans up temporary files

### Alternative Flows

**3a. No recovery method available**
- 3a.1. System immediately proceeds to error handling
- 3a.2. System displays error and terminates gracefully

### Postconditions
- User receives clear error information
- System state is clean (no orphaned files)
- User can retry or modify input

---

## Non-Functional Requirements

### Performance
- Video render time < 5 minutes for 3-minute song
- Vocal separation completes within reasonable time
- System handles concurrent requests (if applicable)

### Reliability
- System handles network failures gracefully
- Fallback methods for critical operations
- Error recovery mechanisms

### Usability
- Clear progress indicators
- User-friendly error messages
- Simple command-line or GUI interface

### Accuracy
- ≥ 90% lyric accuracy
- Synchronized timing between lyrics and audio
- High-quality vocal separation

---

## Use Case Relationships

- **UC-001** (Generate from YouTube) is the primary use case
- **UC-002** (Process Audio File) is an alternative entry point
- **UC-003** (Generate LRC) can be a step in UC-001 and UC-002
- **UC-004** (Vocal Separation) is a component of UC-001 and UC-002
- **UC-005** (Batch Process) extends UC-001 and UC-002
- **UC-006** (Customize Settings) enhances UC-001 and UC-002
- **UC-007** (View Status) supports all processing use cases
- **UC-008** (Handle Errors) is applicable to all use cases

---

## Notes

- All use cases assume the system runs in a local environment (no cloud hosting)
- User authentication is out of scope
- Multi-language support is out of scope
- Commercial music licensing is not handled by the system


