**Research Report: Comparative Analysis of Lyric Fetching APIs**

**Date:** October 26, 2023
**Subject:** Evaluation of Genius, AILRCGenerator, QuickLRC, Lyrics.ovh, and LRCLib for Lyric Retrieval.

### 1. Executive Summary
Retrieving song lyrics via API is a complex landscape due to international copyright laws. Most "official" providers charge high enterprise fees, while free providers rely on crowd-sourced data or web scraping. This report compares five specific tools ranging from metadata giants (Genius) to open-source synced lyric projects (LRCLib) and AI generation tools.

---

### 2. API Analysis

#### A. Genius API
Genius is the world’s biggest database of musical knowledge.
*   **Type:** Metadata & Annotation Database.
*   **Mechanism:** REST API.
*   **The Catch:** The official Genius API **does not** provide the actual lyrics text in the JSON response due to licensing restrictions. It provides metadata (artist, title, album) and a URL to the lyrics page.
*   **Workaround:** Developers usually fetch the URL provided by the API and use a web scraper (like BeautifulSoup) to extract the text. *Note: This technically violates their Terms of Service.*
*   **Pros:** Unmatched database size, highly accurate metadata, rich media info.
*   **Cons:** No direct lyrics text; high overhead (requires scraping); no synced lyrics (LRC).

#### B. LRCLib
An open-source, community-driven instance rapidly gaining popularity among open-source music players.
*   **Type:** Synced Lyrics Database.
*   **Mechanism:** Public REST API.
*   **Pros:** **Best current option for synced lyrics.** It is free, open-source, requires no API key, and provides lyrics in specific time-synced formats (.lrc) which allows for "karaoke-style" scrolling.
*   **Cons:** Database is smaller than Genius (community reliant); slightly lower coverage for very obscure or brand-new pop releases compared to major commercial databases.

#### C. Lyrics.ovh
A long-standing, simple solution for hobbyists.
*   **Type:** Simple Text Scraper/Database.
*   **Mechanism:** REST API.
*   **Pros:** Extremely simple to use (Endpoint: `/v1/artist/title`), no API key required, free.
*   **Cons:** **Reliability.** The service experiences frequent downtime and timeouts. It provides plain text only (no time-sync/LRC). The database is static and often misses newer songs.
*   **Verdict:** Good for "Hello World" projects, not reliable enough for production apps.

#### D. AILRCGenerator (and similar AI tools)
This represents a new category of "Generation" rather than "Retrieval."
*   **Type:** AI Audio-to-Lyrics Generator.
*   **Mechanism:** Usually involves uploading an audio file or YouTube link, processed by models (like OpenAI Whisper) to generate text and timestamps.
*   **Pros:** Can generate synced lyrics for songs that **do not exist** in any database (indie tracks, unreleased demos, local files).
*   **Cons:** Slow (requires processing time); computation often costs money (credits system); accuracy depends on the clarity of the vocals in the audio file.

#### E. QuickLRC (Contextual Note)
*QuickLRC is often associated with tools for **creating** .lrc files manually or via scripts, rather than a robust public database API like Genius.*
*   **Type:** Tooling / Scraper Wrapper.
*   **Pros:** Useful for users building their own local library of .lrc files.
*   **Cons:** Lacks a centralized, high-availability server for application integration. It is generally a tool for validaters/creators rather than a fetch-API for end-users.

---

### 3. Feature Comparison Matrix

| Feature | Genius | LRCLib | Lyrics.ovh | AILRCGenerator |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Use** | Metadata / Annotations | Music Players (Synced) | Simple Text Display | Generating Missing Lyrics |
| **Lyrics in Response** | No (URL only) | Yes | Yes | Yes (Generated) |
| **Time-Synced (LRC)** | No | **Yes** | No | **Yes** |
| **Reliability** | High | High | Low/Medium | Variable (AI dependent) |
| **Cost** | Free Tier | Free | Free | Usually Paid/Credits |
| **Auth Required** | Yes (OAuth2) | No | No | Yes |

---

### 4. Recommendations

For our Karaoke Video Generator project, we recommend integrating **LRCLib** as the primary lyric source due to its synced lyric capabilities, supplemented by **AILRCGenerator** for any tracks not found in the LRCLib database.

### 5. Conclusion
There is no "perfect" API because lyric rights are expensive. **Genius** remains the database king but is hostile to developers wanting raw text. **Lyrics.ovh** is too unstable for commercial use. **LRCLib** has emerged as the clear winner for developers needing free, synced lyrics, provided the community database covers the requested songs.