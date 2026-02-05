<!-- ==============================================================================
SPRINT 4 - THOMAS
Story 4.4: Documentation & Code Quality
- API documentation complete for audio processing module
- Usage examples documented
============================================================================== -->

# Audio Processing Module

Handles vocal separation using Demucs for karaoke generation.

## Usage
```python
from core.audio_processing.vocal_separator import separate_vocals

result = separate_vocals("song.mp3")
print(result["vocals"])        # Path to vocals
print(result["instrumental"])  # Path to instrumental