# 🎤 Karaoke Video Generator — Demo Script

**Duration:** 2 minutes  
**Presenter:** [Your Name]  
**Date:** [Demo Date]

---

## Demo Preparation Checklist

- [ ] Pre-generate 3-5 sample karaoke videos
- [ ] Test demo environment (backend running, frontend accessible)
- [ ] Have backup YouTube URLs ready (tested and working)
- [ ] Prepare before/after audio samples
- [ ] Have troubleshooting guide ready
- [ ] Test video playback on presentation screen
- [ ] Practice demo script at least 3 times
- [ ] Have backup plan if live demo fails (pre-recorded video)

---

## Demo Script

### [0:00–0:15 | Hook]

> "Creating karaoke videos is surprisingly manual — you need to extract audio, remove vocals, find lyrics, sync them, and render a video. Our project automates that entire pipeline."

**Visual:** Show slide with problem statement

---

### [0:15–0:35 | What it does]

> "This is the Karaoke Video Generator. Given any YouTube link, our system automatically converts the song into a karaoke video with synchronized lyrics, ready to use or upload."

**Visual:** 
- Switch to application interface
- Show the main form with YouTube URL input
- Highlight the simplicity of the interface

---

### [0:35–1:05 | How it works (high level)]

> "Under the hood, the system is a fully automated pipeline.
> 
> We start by downloading the audio from YouTube and converting it to MP3.
> 
> Next, we use AI-based vocal separation to isolate the instrumental track.
> 
> Then we extract lyrics, generate timestamps, and produce an LRC file.
> 
> Finally, we render a 720p karaoke video using FFmpeg with real-time lyric overlays."

**Visual:**
- Show architecture diagram or pipeline flow
- Highlight each step as you mention it
- Optionally show code snippets or module structure

---

### [1:05–1:30 | Team & architecture]

> "Our team split responsibilities across the pipeline.
> 
> Thomas handled audio acquisition, Mark focused on vocal separation, Aruhant built the lyric intelligence and synchronization, and I handled video rendering and FFmpeg integration.
> 
> Everything is written in Python using open-source tools like Demucs, Lyrics APIs, and FFmpeg."

**Visual:**
- Show team responsibilities slide
- Highlight technology stack
- Show code structure if time permits

---

### [1:30–1:50 | Demo moment]

> "Here's an example output.
> 
> You can see the vocals removed, lyrics perfectly synced, and the video rendered automatically in under five minutes for a three-minute song."

**Visual:**
- **LIVE DEMO (if time allows):**
  1. Paste a YouTube URL into the interface
  2. Click "Generate Karaoke Video"
  3. Show progress indicators updating
  4. Wait for completion (or use pre-generated video if time is tight)
  5. Play the final karaoke video
  6. Highlight synchronized lyrics

- **OR PRE-RECORDED DEMO:**
  1. Play pre-generated karaoke video
  2. Show before/after audio comparison
  3. Highlight synchronized lyrics timing
  4. Show video quality (720p)

**Key Points to Highlight:**
- Clean instrumental track (vocals removed)
- Perfectly synchronized lyrics
- Professional video quality
- Fast processing time

---

### [1:50–2:00 | Wrap-up]

> "In four weeks, we delivered a fully functional MVP that automates karaoke video creation end-to-end, meeting our performance and accuracy goals. Thank you."

**Visual:**
- Return to title slide or summary slide
- Show key metrics (90% accuracy, <5 min render time)
- Thank you slide

---

## Alternative Demo Flow (If Live Demo Fails)

### Backup Plan

1. **Pre-recorded Video Demo:**
   - Show screen recording of full process
   - Highlight key features
   - Show final output

2. **Static Examples:**
   - Show pre-generated karaoke videos
   - Show before/after audio samples
   - Show architecture diagrams

3. **Code Walkthrough:**
   - Show key code snippets
   - Explain integration points
   - Highlight technical achievements

---

## Demo Tips

### Do's ✅
- Practice the script multiple times
- Have backup videos ready
- Test all equipment beforehand
- Speak clearly and confidently
- Make eye contact with audience
- Highlight key achievements
- Show enthusiasm for the project

### Don'ts ❌
- Don't rush through the demo
- Don't apologize for minor issues
- Don't get stuck on technical details
- Don't skip the demo if something minor fails (use backup)
- Don't forget to highlight team contributions

---

## Sample YouTube URLs for Demo

**Pre-tested URLs (have these ready):**
- [Popular song 1] - [URL]
- [Popular song 2] - [URL]
- [Popular song 3] - [URL]

**Notes:**
- Test all URLs before demo
- Ensure they're not region-locked
- Have backups ready

---

## Troubleshooting Guide

### If Backend Fails to Start:
- Check if port is already in use
- Verify all dependencies are installed
- Check environment variables

### If Video Generation Fails:
- Use pre-generated video
- Explain the process verbally
- Show architecture diagram

### If Internet Connection Fails:
- Use pre-generated videos
- Explain the process
- Show code examples

### If Video Playback Fails:
- Have video file ready to play in VLC/Media Player
- Show screenshots of the output
- Explain the visual features

---

## Post-Demo Q&A Preparation

### Anticipated Questions:

**Q: How accurate is the vocal separation?**
A: Demucs provides high-quality separation, with Spleeter as fallback. We achieved clean instrumental tracks for ~90% of tested songs.

**Q: What about copyright issues?**
A: This is an educational project. For commercial use, proper licensing would be required.

**Q: Can it handle different languages?**
A: Currently supports English. Multi-language support is a future enhancement.

**Q: How does it handle songs with multiple vocalists?**
A: The AI model (Demucs) handles multiple vocalists well, separating them from the instrumental track.

**Q: What's the longest song it can process?**
A: Technically unlimited, but processing time scales with song length. We optimized for songs under 5 minutes.

**Q: Can users edit the lyrics?**
A: Not in the current MVP. Manual timestamp adjustment is a planned future feature.

---

## Demo Checklist (Day Of)

- [ ] Backend server running and tested
- [ ] Frontend accessible and tested
- [ ] Sample videos pre-generated
- [ ] Backup videos ready
- [ ] Presentation slides loaded
- [ ] Demo script printed/accessible
- [ ] Troubleshooting guide ready
- [ ] Internet connection stable
- [ ] Audio/video equipment tested
- [ ] Team members briefed on backup plan

---

**Good luck with your demo! 🎤**

