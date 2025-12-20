# KARAOKE VIDEO GENERATOR — USER MANUAL

**Document Version:** 1.0  
**Date Created:** December 2025  
**Last Updated:** December 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [How to Use](#how-to-use)
4. [Understanding the Interface](#understanding-the-interface)
5. [Features](#features)
6. [Troubleshooting](#troubleshooting)
7. [Frequently Asked Questions](#frequently-asked-questions)

---

## Introduction

### What is the Karaoke Video Generator?

The Karaoke Video Generator is an automated web application that converts any YouTube song into a professional karaoke video with synchronized lyrics. Simply provide a YouTube URL, and the system will:

- Download the audio from YouTube
- Remove vocals to create an instrumental track
- Fetch and synchronize lyrics with timestamps
- Generate a 720p karaoke video with lyrics overlay

**Perfect for:**
- Content creators making karaoke videos for social media
- Karaoke enthusiasts creating custom videos
- Musicians needing instrumental tracks for practice

### Key Features

- ✅ **Fully Automated:** No manual editing required
- ✅ **Fast Processing:** Generates videos in under 5 minutes (for 3-minute songs)
- ✅ **High Quality:** 720p video resolution with synchronized lyrics
- ✅ **Accurate Lyrics:** 90%+ accuracy for most popular songs
- ✅ **Easy to Use:** Simple web interface, just paste a URL

---

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Edge, or Safari)
- Internet connection
- A valid YouTube URL for the song you want to convert

### Accessing the Application

1. **Open your web browser**
2. **Navigate to:** `http://localhost:5174/` (if running locally)
   - Or the URL provided by your system administrator
3. **Wait for the page to load** - You should see the Karaoke Video Generator interface

### First Time Setup

If you're running the application locally, ensure:
- The backend server is running on `http://localhost:8000`
- The frontend server is running on `http://localhost:5174`

---

## How to Use

### Step-by-Step Guide

#### Step 1: Enter YouTube URL

1. **Find the YouTube video** you want to convert to karaoke
2. **Copy the URL** from your browser's address bar
   - Example: `https://www.youtube.com/watch?v=VIDEO_ID`
3. **Paste the URL** into the input field on the main page
4. **Click "Generate Karaoke Video"** button

#### Step 2: Wait for Processing

The system will automatically process your request through several stages:

1. **Downloading audio** (0-20%)
   - Downloads the audio from YouTube
   - Converts to the required format

2. **Processing audio** (20-50%)
   - Separates vocals from instrumental track using AI
   - Optimizes audio quality
   - *This may take a few minutes for longer songs*

3. **Fetching lyrics** (50-70%)
   - Searches for lyrics matching the song
   - Normalizes song title and artist name

4. **Synchronizing lyrics** (70-80%)
   - Synchronizes lyrics with audio timestamps
   - Ensures lyrics appear at the correct time

5. **Rendering video** (80-100%)
   - Creates the final karaoke video with lyrics overlay
   - *This may take a few minutes*

**Note:** The entire process typically takes 3-5 minutes for a 3-minute song. Longer songs may take proportionally longer.

#### Step 3: Download Your Video

1. **Wait for completion** - The progress bar will reach 100%
2. **Video preview appears** - You'll see a preview of your karaoke video
3. **Click "Download"** button to save the video to your computer
4. **Video format:** MP4 (720p resolution)

---

## Understanding the Interface

### Main Components

#### 1. URL Input Form
- **Location:** Top left of the page
- **Purpose:** Enter the YouTube URL you want to convert
- **Features:**
  - Validates URL format
  - Shows error messages for invalid URLs

#### 2. Progress Indicator
- **Location:** Below the input form
- **Shows:**
  - Current processing stage
  - Progress percentage (0-100%)
  - Estimated time remaining (when available)

#### 3. Status Messages
- **"Job queued, waiting to start..."** - Request received
- **"Downloading audio from YouTube"** - Downloading audio
- **"Separating vocals from audio (this may take a few minutes)..."** - Processing audio
- **"Optimizing audio quality"** - Audio optimization
- **"Fetching lyrics for the song"** - Searching for lyrics
- **"Synchronizing lyrics with audio timestamps"** - Syncing lyrics
- **"Rendering video with lyrics overlay (this may take a few minutes)..."** - Creating video
- **"Finalizing video..."** - Completing video
- **"Karaoke video generation completed"** - Success!

#### 4. Video Preview
- **Location:** Right side of the page
- **Shows:**
  - Preview of the generated video (when complete)
  - Download button
  - Video player controls

#### 5. Error Messages
- **Location:** Red banner at top of page
- **Shows:** Error details if something goes wrong
- **Can be dismissed:** Click the X button

---

## Features

### Automated Processing Pipeline

The system handles everything automatically:

1. **Audio Acquisition**
   - Downloads audio from YouTube
   - Validates URL format
   - Handles various YouTube URL formats

2. **Vocal Separation**
   - Uses AI (Demucs) to separate vocals from instrumental
   - Creates clean instrumental track
   - Optimizes audio quality

3. **Lyrics Intelligence**
   - Automatically finds lyrics for the song
   - Normalizes song titles (removes "(audio)", "(video)", etc.)
   - Synchronizes lyrics with audio timestamps
   - Achieves 90%+ accuracy for most songs

4. **Video Rendering**
   - Creates 720p video
   - Overlays synchronized lyrics
   - Uses black background with white/yellow text
   - Centers lyrics on screen

### Quality Settings

- **Video Resolution:** 720p (1280x720)
- **Video Format:** MP4
- **Audio Quality:** Maintains original quality after processing
- **Lyric Accuracy:** ≥90% for most popular songs

### Performance

- **Processing Time:** < 5 minutes for 3-minute songs
- **Audio Processing:** < 3 minutes for 3-minute songs
- **Video Rendering:** 1-2 minutes typically

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Unable to connect to the server"

**Possible Causes:**
- Backend server is not running
- Backend server is on a different port
- Network connectivity issues

**Solutions:**
1. Ensure the backend server is running on `http://localhost:8000`
2. Check that both frontend and backend servers are started
3. Verify your internet connection
4. Try refreshing the page

#### Issue: "Invalid YouTube URL"

**Possible Causes:**
- URL format is incorrect
- URL is not a valid YouTube link
- URL contains extra characters

**Solutions:**
1. Copy the URL directly from YouTube (not from a shortened link)
2. Ensure the URL starts with `https://www.youtube.com/watch?v=` or `https://youtu.be/`
3. Remove any extra text or spaces before/after the URL
4. Try the full YouTube URL format: `https://www.youtube.com/watch?v=VIDEO_ID`

#### Issue: "Could not find lyrics for this song"

**Possible Causes:**
- Song is very new or obscure
- Song title/artist doesn't match lyrics database
- Lyrics are not available in the database

**Solutions:**
1. Try a different version of the song (official audio vs. live performance)
2. Ensure the YouTube video has the correct song title and artist
3. Try popular songs that are more likely to be in the lyrics database
4. The system will show what it searched for in the error message

#### Issue: Processing takes too long

**Possible Causes:**
- Song is very long (>5 minutes)
- System is processing multiple requests
- Computer resources are limited

**Solutions:**
1. Be patient - longer songs take proportionally longer
2. A 3-minute song typically takes 3-5 minutes to process
3. A 5-minute song may take 5-8 minutes
4. Close other resource-intensive applications
5. Ensure you have a stable internet connection

#### Issue: Video generation fails

**Possible Causes:**
- FFmpeg not installed or not in PATH
- Insufficient disk space
- Audio processing failed
- Lyrics synchronization failed

**Solutions:**
1. Check the error message for specific details
2. Ensure FFmpeg is installed (if running locally)
3. Check available disk space
4. Try a different song
5. Contact support if the issue persists

#### Issue: Video quality is poor

**Possible Causes:**
- Original YouTube video quality was low
- Audio separation quality issues

**Solutions:**
1. Use high-quality source videos from YouTube
2. Try official audio versions rather than live performances
3. The system maintains original audio quality after processing

#### Issue: Lyrics are not synchronized correctly

**Possible Causes:**
- Song has unusual timing
- Lyrics database has incorrect timestamps
- Song has instrumental sections

**Solutions:**
1. Try a different version of the song
2. The system achieves 90%+ accuracy for most popular songs
3. Some songs may have minor timing discrepancies
4. Instrumental sections will show no lyrics (this is normal)

---

## Frequently Asked Questions

### General Questions

**Q: Is this free to use?**  
A: Yes, the application is free to use. However, ensure you comply with YouTube's terms of service and copyright laws when using downloaded content.

**Q: What video formats are supported?**  
A: The system outputs MP4 format videos in 720p resolution.

**Q: Can I use this for commercial purposes?**  
A: Please review copyright laws and YouTube's terms of service. The application itself is for educational/personal use. Commercial use of generated content may require proper licensing.

**Q: How long does it take to generate a video?**  
A: Typically 3-5 minutes for a 3-minute song. Longer songs take proportionally longer. The system shows progress updates throughout the process.

**Q: Can I process multiple songs at once?**  
A: Currently, the system processes one song at a time. Wait for one video to complete before starting another.

### Technical Questions

**Q: What browsers are supported?**  
A: Modern browsers including Chrome, Firefox, Edge, and Safari. Ensure you're using the latest version.

**Q: Do I need to install anything?**  
A: If you're using the hosted version, no installation is needed. If running locally, follow the setup guide in the documentation.

**Q: Why does vocal separation take so long?**  
A: AI-based vocal separation is computationally intensive. The system uses Demucs, which provides high-quality results but requires processing time.

**Q: Can I customize the video appearance?**  
A: Currently, videos use a black background with white/yellow centered lyrics. Customization options may be added in future versions.

**Q: What happens if the process fails?**  
A: The system will display an error message explaining what went wrong. You can try again with the same or different URL.

### Quality Questions

**Q: How accurate are the lyrics?**  
A: The system achieves 90%+ accuracy for most popular songs. Accuracy may vary for:
- Very new songs
- Obscure songs
- Songs with unusual timing
- Live performances

**Q: Can I edit the lyrics after generation?**  
A: Currently, lyrics cannot be edited after generation. The system uses the lyrics found in the database.

**Q: What if the lyrics are wrong?**  
A: If lyrics are incorrect, try a different version of the song (official audio vs. live). The system searches multiple sources for the best match.

**Q: Why are some parts of the song missing lyrics?**  
A: Instrumental sections, intros, and outros typically don't have lyrics. This is normal and expected behavior.

### Usage Questions

**Q: Can I use any YouTube video?**  
A: Yes, as long as the video contains audio and is accessible. However, ensure you comply with copyright and terms of service.

**Q: What if the song is very long (>10 minutes)?**  
A: Longer songs will take longer to process. Very long songs (>10 minutes) may take 10-15 minutes or more. Be patient and ensure you have a stable connection.

**Q: Can I download the instrumental track separately?**  
A: Currently, only the complete karaoke video is available for download. The instrumental track is embedded in the video.

**Q: How do I share my generated video?**  
A: Download the video and share it like any other video file. The video is in standard MP4 format compatible with most platforms.

---

## Tips for Best Results

### Getting the Best Quality

1. **Use Official Audio Versions**
   - Official audio tracks typically have better quality
   - Lyrics are more likely to be accurate
   - Vocal separation works better

2. **Choose Popular Songs**
   - More likely to have accurate lyrics in the database
   - Better synchronization accuracy
   - Faster processing

3. **Ensure Good Internet Connection**
   - Faster download of audio from YouTube
   - More reliable processing
   - Better overall experience

4. **Be Patient**
   - Processing takes time, especially for longer songs
   - Don't close the browser tab during processing
   - The progress indicator shows you what's happening

5. **Check Song Title and Artist**
   - Ensure YouTube video has correct metadata
   - Helps the system find accurate lyrics
   - Improves synchronization quality

---

## Support

### Getting Help

If you encounter issues not covered in this manual:

1. **Check the Troubleshooting section** above
2. **Review error messages** - they often contain helpful information
3. **Try a different song** to see if the issue is song-specific
4. **Contact support** with:
   - The error message you received
   - The YouTube URL you tried
   - Steps you took before the error occurred

### Reporting Issues

When reporting issues, please include:
- **Error message** (if any)
- **YouTube URL** you tried to use
- **Browser** and version you're using
- **What you expected** to happen
- **What actually happened**

---

## Version Information

**Current Version:** 1.0.0  
**Last Updated:** December 2025  
**Document Version:** 1.0

---

## Legal Notice

**Important:** This application is for educational and personal use. Users are responsible for:
- Complying with YouTube's Terms of Service
- Respecting copyright laws
- Obtaining proper licenses for commercial use of generated content
- Using downloaded content in accordance with applicable laws

The application developers are not responsible for misuse of the generated content.

---

**Document Owner:** Technical Lead (William Cagas)  
**For Technical Support:** See setup documentation or contact the development team

