# ==============================================================================
# ==============================================================================
#                        LYRICS SCRAPER MODULE
# ==============================================================================
# ==============================================================================
#
# Sprint 1 - Story 1.4: Lyrics Intelligence Research & Setup (Aruhant)
# Sprint 2 - Story 2.4: Lyrics Fetching Implementation (Aruhant)
#
# ==============================================================================

from lrclib import LrcLibAPI


# ==============================================================================
# SPRINT 2 - ARUHANT
# Story 2.4: Lyrics Fetching Implementation
# - Lyrics fetching from primary API (LRCLib)
# - Song title and artist matching logic
# - Error handling for missing lyrics, API failures
# - Rate limiting and API usage tracking
# ==============================================================================

# lyrics search fuzzy with respect to duration
def fetch_lyrics(search_str: str, duration: int):
    # Create an instance of the API
    api = LrcLibAPI(user_agent="my-app/0.0.1")

    # Search for tracks by an artist
    results = api.search_lyrics(
        query=search_str,
    )

    # find the result with closest duration, with sync lyrics
    best_match = None
    smallest_duration_diff = float('inf')
    for result in results:
        print(f"Found: {result.track_name} by {result.artist_name}, duration: {result.duration}s, synced: {bool(result.synced_lyrics)}")
        duration_diff = abs(result.duration - duration)
        if duration_diff < smallest_duration_diff:
            smallest_duration_diff = duration_diff
            best_match = result

    return best_match

# ==============================================================================
# END OF SPRINT 2 - ARUHANT
# ==============================================================================
