# Filter Chunking Fix Verification Test

This test script verifies that the filter chunking fix works correctly for long songs (4+ minutes) **without requiring a full 5-7 minute video generation**.

## Quick Test

Run from the project root:

```bash
python -m backend.core.video_rendering.test_filter_chunking
```

## What It Tests

1. **Filter Splitting**: Verifies that comma-separated filters are split correctly while respecting commas inside quoted strings (like timestamps in `enable='between(t,46.35,54.22)'`)

2. **Filter Chunking**: Tests that long filter chains (30+ filters) are properly split into labeled chunks using FFmpeg's intermediate outputs format

3. **Filter File Format**: Validates that the generated filter file has the correct format for FFmpeg parsing

4. **Problematic Timestamp**: Specifically tests the timestamp `46.35` that was causing the error

## Expected Results

- ✅ Filter splitting works correctly
- ✅ Filter chunking creates proper labeled intermediate outputs  
- ✅ Filter file format is valid
- ✅ Timestamp 46.35 is handled correctly

If all tests pass, the fix should work for your 4+ minute songs!

## What the Fix Does

For songs longer than 4 minutes (filter strings > 4000 characters), the code now:

1. Splits the filter chain into smaller chunks (8 filters per chunk)
2. Uses labeled intermediate outputs like: `[0:v]filters1,filter2[v0];[v0]filters3,filter4[v1];[v1]filters5,filter6[v]`
3. This prevents FFmpeg from misparsing very long comma-separated filter chains

The fix automatically applies when filter strings exceed 4000 characters, so no configuration is needed.

