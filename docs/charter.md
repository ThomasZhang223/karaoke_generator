# KARAOKE VIDEO GENERATOR — PROJECT CHARTER

**Document Version:** 1.0  
**Date Created:** November 4, 2025  

---

## Title of Project
**Karaoke Video Generator**  
An automated system that converts any song into a karaoke video with synchronized lyrics.

---

## Stakeholders
- **Project Sponsor:** Paul Ward  
- **Technical Lead:** William Cagas  
- **Team Members:** Aruhant Mehta, Mark Rozin, Thomas Zhang, William Cagas  
- **End Users:** Content creators, karaoke enthusiasts, musicians  
- **Advisors:** Course Instructor, TA Mentors  

---

## Scope

**In Scope:**
- YouTube → MP3 conversion  
- AI-based vocal separation  
- Lyrics extraction and timestamping  
- LRC file parsing  
- Synchronized video generation (720p)  

**Out of Scope:**
- User authentication  
- Multi-language support  
- Mobile app  
- Cloud hosting  
- Advanced visual effects  
- Commercial music licensing  

---

## Objective
Automate karaoke video creation by integrating YouTube download, AI-driven vocal removal, lyric synchronization, and FFmpeg-based rendering.

**Success Criteria:**
- ≥ 90% lyric accuracy  
- Video render time < 5 minutes for a 3-minute song  
- Functional MVP delivered by Week 4  

---

## Project Team and Responsibilities

| **Member**  | **Role**            | **Key Responsibilities**                           |
|-------------|---------------------|----------------------------------------------------|
| Thomas      | Audio Acquisition   | YouTube download, MP3 conversion                   |
| Mark        | Audio Processing    | Vocal separation, quality optimization             |
| Aruhant     | Lyrics Intelligence | Lyrics scraping, timestamp sync, LRC generation    |
| William     | Video Rendering     | FFmpeg integration, text overlay rendering         |
| All Members | QA & Integration    | Testing, documentation, and final demo preparation |

---

## Deliverables
- **Weeks 1–2:** Architecture document, YouTube→MP3 conversion, Demucs integration  
- **Week 3:** Lyrics API + timestamp sync, LRC file generation  
- **Week 4:** Video rendering engine, full integration, demo, and documentation  

---

## Risks and Mitigation

| **Risk**                     | **Likelihood / Impact** | **Mitigation Strategy**                     |
|------------------------------|-------------------------|---------------------------------------------|
| Poor vocal separation        | Medium / High           | Use Demucs + Spleeter fallback              |
| Inaccurate lyrics timestamps | Medium / High           | Use QuickLRC AI + manual correction         |
| YouTube API limitations      | Medium                  | Implement fallback libs (yt-dlp, pytube)    |
| Scope creep                  | High                    | Enforce weekly scope reviews                |
| Integration challenges       | Medium                  | Daily standups and early interface planning |

---

## Constraints
- Fixed 4-week timeline (28 days)  
- 4-member team, no external hires  
- Zero budget (open-source tools only)  
- Python-only stack (pytube, Demucs, FFmpeg-Python, LyricsGenius)  
- Educational use only (no commercial licensing)  

---

## Authority and Sign-Off Criteria

**Project completion requires:**
- Functional MVP demo producing karaoke video output  
- Approval of documentation and code quality  
- Sponsor and technical lead sign-off  

**Project Sponsor (Paul Ward):** ____________________  **Date:** ____________  
**Technical Lead (William Cagas):** ______William Cagas________  **Date:** ___11/05/2025___  

---

## Project Summary
This 4-week agile project will deliver an AI-powered Karaoke Video Generator that automatically converts any YouTube song into a synchronized karaoke video with accurate lyrics and clean visuals. The team of four software engineers will complete design, integration, and testing under strict time, cost, and scope constraints.