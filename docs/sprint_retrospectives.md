# KARAOKE VIDEO GENERATOR — SPRINT RETROSPECTIVES

**Document Version:** 1.0  
**Date Created:** November 25, 2025  
**Last Updated:** December 19, 2025

---

## Overview

This document contains retrospective reflections for each sprint, focusing on process improvements, team dynamics, technical challenges, and lessons learned.

**Retrospective Format:**
- **What Went Well:** Successes, achievements, and positive observations
- **What Didn't Go Well:** Challenges, blockers, and areas for improvement
- **Action Items:** Concrete steps to improve in the next sprint
- **Metrics:** Velocity, completion rate, and other relevant metrics (optional)

---

## SPRINT 1: Foundation & Research (Week 1)
**Sprint Dates:** November 4 - November 11, 2025  
**Retrospective Date:** November 11, 2025  
**Participants:** All Team Members

### What Went Well
- Successfully set up the project repository and established coding conventions
- Research on lyrics synchronization APIs was comprehensive; identified Genius API and LRCLIB as viable options
- Team communication was strong—daily standups kept everyone aligned
- Completed the domain model ahead of schedule
- Everyone contributed to the project charter and felt invested in the vision

### What Didn't Go Well
- Underestimated the complexity of audio downloading due to YouTube rate limiting
- Initial environment setup took longer than expected (dependency conflicts with FFmpeg)
- Some confusion around Git branching strategy in the first few days
- Documentation was scattered across multiple locations initially

### Action Items
- [x] Consolidate all documentation into the /docs folder
- [x] Create a shared troubleshooting guide for environment setup
- [x] Establish clear Git workflow guidelines

### Metrics (Optional)
- **Story Points Planned:** 21
- **Story Points Completed:** 18
- **Velocity:** 18
- **Completion Rate:** 86%

### Notes
- Discovered that yt-dlp is more reliable than pytube for audio extraction
- Learned that synchronized lyrics (LRC format) are essential for karaoke timing accuracy
- Team decided to use Python for backend due to familiarity and library availability

---

## SPRINT 2: Core Implementation (Week 2)
**Sprint Dates:** November 11 - November 18, 2025  
**Retrospective Date:** November 18, 2025  
**Participants:** All Team Members

### What Went Well
- Audio downloader module completed with robust error handling
- Lyrics scraper successfully integrated with Genius API
- Title normalization system handles edge cases well (featuring artists, remix tags, etc.)
- Code reviews helped catch several bugs before they became issues
- Pair programming sessions accelerated knowledge sharing

### What Didn't Go Well
- Lyrics synchronization proved more challenging than anticipated—timestamp accuracy varied wildly
- Some API rate limits forced us to implement caching earlier than planned
- One team member was sick for 2 days, causing minor delays on the UI mockups
- Test coverage was lower than desired for the scraper module

### Action Items
- [x] Implement request caching to reduce API calls
- [x] Add unit tests for lyrics parsing edge cases
- [x] Create fallback mechanisms when primary lyrics source fails

### Metrics (Optional)
- **Story Points Planned:** 26
- **Story Points Completed:** 22
- **Velocity:** 22
- **Completion Rate:** 85%

### Notes
- WhisperX proved to be incredibly useful for generating timestamps when LRC files aren't available
- Realized we need a hybrid approach: use pre-synced lyrics when available, fall back to Whisper-based alignment
- Team morale is high despite the synchronization challenges

---

## SPRINT 3: Integration & Synchronization (Week 3)
**Sprint Dates:** November 18 - November 25, 2025  
**Retrospective Date:** November 25, 2025  
**Participants:** All Team Members

### What Went Well
- Successfully integrated all core modules (downloader, scraper, synchronizer)
- Video generation pipeline produces clean karaoke-style output
- The confidence scoring system for lyrics matching works better than expected
- Frontend design is coming together nicely with a modern, clean aesthetic
- Team handled the Thanksgiving break scheduling well

### What Didn't Go Well
- Integration revealed some interface mismatches between modules that required refactoring
- Video rendering is slower than desired (~2x the song duration)
- Some songs with unusual structures (bridges, ad-libs) don't synchronize well
- Had to pivot from our original lyrics highlighting approach due to performance issues

### Action Items
- [x] Optimize video rendering with hardware acceleration where available
- [x] Add manual timestamp adjustment option for edge cases
- [ ] Implement progress indicators for long-running operations

### Metrics (Optional)
- **Story Points Planned:** 28
- **Story Points Completed:** 25
- **Velocity:** 25
- **Completion Rate:** 89%

### Notes
- Learned that MoviePy can be slow for real-time text overlays; considering FFmpeg direct calls for performance
- The synchronization accuracy is around 85-90% for most pop songs, which is acceptable for MVP
- Team is feeling the time pressure but staying focused on core functionality

---

## SPRINT 4: Integration, Testing & Demo (Week 4)
**Sprint Dates:** November 25 - December 2, 2025  
**Retrospective Date:** December 2, 2025  
**Participants:** All Team Members

### What Went Well
- Demo went smoothly! Professors were impressed with the real-time lyrics highlighting
- End-to-end testing caught critical bugs before the demo
- Successfully implemented batch processing for multiple songs
- The UI polish in the final days made a big difference in presentation
- Team pulled together under pressure and delivered a working product

### What Didn't Go Well
- Last-minute bug with certain Unicode characters in lyrics caused some stress
- Didn't have time to implement the "karaoke mode" color transition we originally wanted
- Some edge cases with instrumental sections still cause timing drift
- Documentation could have been more thorough throughout the project

### Action Items
- [x] Create demo video showcasing the application
- [x] Write final project report
- [ ] Consider open-sourcing the project after course completion

### Metrics (Optional)
- **Story Points Planned:** 24
- **Story Points Completed:** 23
- **Velocity:** 23
- **Completion Rate:** 96%

### Notes
- The project successfully generates karaoke videos for approximately 90% of tested songs
- Performance optimization made rendering 40% faster than Sprint 3
- Received positive feedback from TAs during the demo session
- Proud of what the team accomplished in just 4 weeks!

---

## Project-Wide Retrospective

**Date:** December 5, 2025  
**Participants:** All Team Members

### Overall Project Reflection
This project was an ambitious undertaking that pushed us to learn new technologies and work effectively as a team under tight deadlines. Building a karaoke video generator from scratch required integrating multiple complex systems: audio processing, lyrics fetching, natural language processing for synchronization, and video generation. Despite the challenges, we delivered a functional product that we're all proud of. The experience reinforced the importance of iterative development and adapting to discoveries made along the way.

### Key Learnings
- **Technical:** Audio/video processing is computationally expensive—always consider performance early
- **Technical:** API rate limits are a real constraint; caching strategies are essential
- **Technical:** Machine learning models (like Whisper) are powerful but require careful tuning
- **Process:** Daily standups and regular communication prevent misunderstandings
- **Process:** Code reviews are worth the time investment—they catch bugs and spread knowledge
- **Team:** Playing to individual strengths leads to better outcomes

### What We'd Do Differently
- Start with a simpler MVP and iterate (we tried to do too much initially)
- Allocate more time for integration testing between sprints
- Set up CI/CD pipeline from day one instead of Sprint 3
- Have clearer API contracts between modules before implementation
- Schedule regular pair programming sessions instead of ad-hoc

### Recommendations for Future Projects
1. **Spike early:** When dealing with unfamiliar technology, do a quick proof-of-concept before committing
2. **Embrace modularity:** Well-defined interfaces make integration smoother
3. **Test on real data:** Synthetic test cases don't capture real-world complexity
4. **Document as you go:** Retrofitting documentation is painful and often incomplete
5. **Celebrate small wins:** Team morale matters, especially during crunch time

---

## Retrospective Guidelines

### When to Conduct Retrospectives
- **Sprint Retrospectives:** End of each sprint (1 hour)
- **Project Retrospective:** After project completion (2 hours)

### Retrospective Format Options

#### Option 1: Start/Stop/Continue
- **Start:** What should we start doing?
- **Stop:** What should we stop doing?
- **Continue:** What should we continue doing?

#### Option 2: Mad/Sad/Glad
- **Mad:** What frustrated us?
- **Sad:** What disappointed us?
- **Glad:** What made us happy?

#### Option 3: 4Ls (Liked/Learned/Lacked/Longed For)
- **Liked:** What did we like?
- **Learned:** What did we learn?
- **Lacked:** What did we lack?
- **Longed For:** What did we wish we had?

### Best Practices
- Be honest and constructive
- Focus on process, not people
- Generate actionable items
- Follow up on action items from previous sprints
- Document decisions and rationale

---

**Document Owner:** Technical Lead (William Cagas)  
**Review Frequency:** After each sprint retrospective

