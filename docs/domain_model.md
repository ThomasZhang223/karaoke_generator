# KARAOKE VIDEO GENERATOR — DOMAIN MODEL

**Document Version:** 1.0  
**Date Created:** November 25, 2025  
**Last Updated:** November 25, 2025

---

## Overview

This document describes the domain model for the Karaoke Video Generator system. It defines the key entities, their attributes, relationships, and behaviors within the problem domain.

---

## Domain Entities

### AudioFile
Represents an audio file downloaded or processed by the system.

**Attributes:**
- `id` (String): Unique identifier
- `source_url` (String): Original YouTube URL
- `file_path` (String): Local file system path
- `format` (String): Audio format (MP3, WAV, etc.)
- `duration` (Float): Duration in seconds
- `sample_rate` (Integer): Audio sample rate
- `bitrate` (Integer): Audio bitrate
- `file_size` (Integer): File size in bytes
- `created_at` (DateTime): Timestamp of creation
- `status` (Enum): Processing status (downloaded, processing, processed, failed)

**Relationships:**
- Has one `InstrumentalTrack`
- Has one `OriginalTrack`
- Has many `LyricLine` (through synchronization)

**Behaviors:**
- `download()`: Downloads audio from YouTube
- `validate()`: Validates audio file integrity
- `convert()`: Converts audio to required format

---

### InstrumentalTrack
Represents the vocal-separated instrumental version of an audio file.

**Attributes:**
- `id` (String): Unique identifier
- `audio_file_id` (String): Reference to source AudioFile
- `file_path` (String): Local file system path
- `separation_method` (String): Method used (Demucs, Spleeter)
- `quality_score` (Float): Separation quality metric (0-1)
- `created_at` (DateTime): Timestamp of creation
- `status` (Enum): Status (processing, completed, failed)

**Relationships:**
- Belongs to `AudioFile`
- Used by `Video`

**Behaviors:**
- `separate_vocals()`: Performs vocal separation
- `validate_quality()`: Checks separation quality
- `export()`: Exports instrumental track

---

### Lyrics
Represents the lyrics for a song with synchronization information.

**Attributes:**
- `id` (String): Unique identifier
- `song_title` (String): Song title
- `artist` (String): Artist name
- `source` (String): Source API (LyricsGenius, etc.)
- `raw_text` (String): Plain text lyrics
- `language` (String): Language code
- `created_at` (DateTime): Timestamp of creation
- `accuracy_score` (Float): Estimated accuracy (0-1)

**Relationships:**
- Has many `LyricLine`
- Synchronized with `AudioFile`

**Behaviors:**
- `fetch()`: Fetches lyrics from API
- `parse()`: Parses lyrics into lines
- `validate()`: Validates lyrics completeness

---

### LyricLine
Represents a single line of lyrics with timestamp information.

**Attributes:**
- `id` (String): Unique identifier
- `lyrics_id` (String): Reference to parent Lyrics
- `line_number` (Integer): Sequential line number
- `text` (String): Lyric line text
- `start_time` (Float): Start timestamp in seconds
- `end_time` (Float): End timestamp in seconds
- `duration` (Float): Duration in seconds
- `highlight_color` (String): Color for video display

**Relationships:**
- Belongs to `Lyrics`
- Synchronized with `AudioFile`

**Behaviors:**
- `synchronize()`: Synchronizes timestamp with audio
- `validate_timing()`: Validates timestamp accuracy

---

### LRCFile
Represents a Lyrics Record Container (LRC) file with timestamped lyrics.

**Attributes:**
- `id` (String): Unique identifier
- `lyrics_id` (String): Reference to source Lyrics
- `audio_file_id` (String): Reference to synchronized AudioFile
- `file_path` (String): Local file system path
- `format_version` (String): LRC format version
- `created_at` (DateTime): Timestamp of creation
- `line_count` (Integer): Number of lyric lines

**Relationships:**
- Belongs to `Lyrics`
- Belongs to `AudioFile`
- Used by `Video`

**Behaviors:**
- `generate()`: Generates LRC file from Lyrics and AudioFile
- `parse()`: Parses LRC file format
- `validate()`: Validates LRC file structure

---

### Video
Represents the final karaoke video output.

**Attributes:**
- `id` (String): Unique identifier
- `job_id` (String): Generation job identifier
- `instrumental_track_id` (String): Reference to InstrumentalTrack
- `lrc_file_id` (String): Reference to LRCFile
- `file_path` (String): Local file system path
- `resolution` (String): Video resolution (720p, 1080p)
- `duration` (Float): Video duration in seconds
- `file_size` (Integer): File size in bytes
- `format` (String): Video format (MP4)
- `created_at` (DateTime): Timestamp of creation
- `status` (Enum): Status (rendering, completed, failed)
- `render_time` (Float): Time taken to render in seconds

**Relationships:**
- Uses `InstrumentalTrack`
- Uses `LRCFile`
- Generated from `AudioFile`

**Behaviors:**
- `render()`: Renders video with audio and lyrics overlay
- `validate()`: Validates video file integrity
- `export()`: Exports video for download

---

### GenerationJob
Represents a karaoke video generation request and its progress.

**Attributes:**
- `id` (String): Unique job identifier
- `user_id` (String): User identifier (if authentication added)
- `youtube_url` (String): Source YouTube URL
- `status` (Enum): Job status (queued, processing, completed, failed)
- `progress` (Float): Progress percentage (0-100)
- `current_stage` (String): Current processing stage
- `error_message` (String): Error message if failed
- `created_at` (DateTime): Job creation timestamp
- `started_at` (DateTime): Processing start timestamp
- `completed_at` (DateTime): Completion timestamp
- `estimated_time_remaining` (Float): Estimated seconds remaining

**Relationships:**
- Has one `AudioFile`
- Has one `Video` (when completed)

**Behaviors:**
- `start()`: Starts the generation process
- `update_progress()`: Updates progress percentage
- `complete()`: Marks job as completed
- `fail()`: Marks job as failed with error

---

## Domain Relationships

```
GenerationJob
    ├── creates → AudioFile
    │               ├── generates → InstrumentalTrack
    │               └── synchronizes → Lyrics
    │                                   └── contains → LyricLine
    │
    ├── uses → Lyrics + AudioFile
    │           └── generates → LRCFile
    │
    └── produces → Video
                    ├── uses → InstrumentalTrack
                    └── uses → LRCFile
```

---

## Domain Services

### AudioAcquisitionService
Handles downloading and conversion of audio files.

**Responsibilities:**
- Download audio from YouTube
- Validate audio URLs
- Convert audio formats
- Handle download failures

---

### AudioProcessingService
Handles vocal separation and audio quality optimization.

**Responsibilities:**
- Separate vocals from instrumental
- Optimize audio quality
- Validate separation quality
- Handle processing failures

---

### LyricsIntelligenceService
Handles lyrics fetching, parsing, and synchronization.

**Responsibilities:**
- Fetch lyrics from APIs
- Parse lyrics into structured format
- Synchronize lyrics with audio timestamps
- Generate LRC files

---

### VideoRenderingService
Handles video generation with lyrics overlay.

**Responsibilities:**
- Render video with audio track
- Overlay synchronized lyrics
- Apply visual styling
- Export final video

---

### PipelineOrchestrationService
Coordinates the entire karaoke generation pipeline.

**Responsibilities:**
- Orchestrate all services
- Manage job lifecycle
- Handle errors and retries
- Track progress

---

## Domain Events

### AudioDownloaded
Triggered when audio file is successfully downloaded.

**Payload:**
- `audio_file_id`
- `source_url`
- `file_path`

---

### VocalSeparationCompleted
Triggered when vocal separation is complete.

**Payload:**
- `instrumental_track_id`
- `audio_file_id`
- `quality_score`

---

### LyricsSynchronized
Triggered when lyrics are synchronized with audio.

**Payload:**
- `lrc_file_id`
- `lyrics_id`
- `audio_file_id`
- `accuracy_score`

---

### VideoRendered
Triggered when video rendering is complete.

**Payload:**
- `video_id`
- `job_id`
- `file_path`
- `render_time`

---

## Domain Constraints

### Business Rules
1. Audio files must be valid MP3 or WAV format
2. Video resolution must be at least 720p
3. Lyric accuracy must be ≥ 90% for acceptable quality
4. Video generation must complete in < 5 minutes for 3-minute song
5. Only one generation job per YouTube URL at a time (prevent duplicates)

### Validation Rules
1. YouTube URLs must match valid YouTube URL pattern
2. Audio files must have minimum duration (e.g., 10 seconds)
3. Lyrics must have at least one line
4. LRC files must have valid timestamp format
5. Video files must be valid MP4 format

---

## Traceability

### Backlog Traceability
- **AudioFile, AudioAcquisitionService** → Stories 1.2, 2.1
- **InstrumentalTrack, AudioProcessingService** → Stories 1.3, 2.2, 2.3
- **Lyrics, LyricLine, LRCFile, LyricsIntelligenceService** → Stories 1.4, 2.4, 2.5, 3.1
- **Video, VideoRenderingService** → Stories 1.5, 3.3, 3.4
- **GenerationJob, PipelineOrchestrationService** → Story 4.1

### User Stories Traceability
- **AudioFile** → US-1
- **InstrumentalTrack** → US-2
- **Lyrics, LRCFile** → US-3
- **Video** → US-4, US-6
- **GenerationJob** → US-5

---

**Document Owner:** Technical Lead (William Cagas)  
**Review Frequency:** As domain understanding evolves

