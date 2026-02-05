# ==============================================================================
# ==============================================================================
#                        TITLE NORMALIZER UNIT TESTS
# ==============================================================================
# ==============================================================================
#
# Sprint 4 - Story 4.3: Fallback Logic & Error Handling (Aruhant)
#           Tests for lyrics title and artist normalization
#
# ==============================================================================

"""
Tests for title normalization to ensure lyrics search works with YouTube video titles.
"""

from backend.core.lyrics_intelligence.title_normalizer import (
    normalize_title,
    normalize_artist,
    normalize_title_and_artist
)


# ==============================================================================
# SPRINT 4 - ARUHANT
# Story 4.3: Fallback Logic & Error Handling
# - Unit tests for title normalization
# - Test cases cover all major features
# - Edge cases tested
# ==============================================================================


def test_common_video_tags():
    """Test that common YouTube video tags are removed."""
    test_cases = [
        ("Song Name (audio)", "Song Name"),
        ("Song Name (Audio)", "Song Name"),
        ("Song Name (AUDIO)", "Song Name"),
        ("Song Name (video)", "Song Name"),
        ("Song Name (Video)", "Song Name"),
        ("Song Name (official audio)", "Song Name"),
        ("Song Name (Official Audio)", "Song Name"),
        ("Song Name (lyric video)", "Song Name"),
        ("Song Name (Lyric Video)", "Song Name"),
        ("Song Name (lyrics)", "Song Name"),
        ("Song Name (Lyrics)", "Song Name"),
        ("Song Name (with lyrics)", "Song Name"),
    ]
    
    print("Testing common video tags:")
    all_passed = True
    for original, expected in test_cases:
        result = normalize_title(original)
        passed = result == expected
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} '{original}' -> '{result}'")
        if not passed:
            all_passed = False
            print(f"      Expected: '{expected}'")
    
    return all_passed


def test_bracket_formats():
    """Test that bracket formats are also removed."""
    test_cases = [
        ("Song Name [audio]", "Song Name"),
        ("Song Name [Audio]", "Song Name"),
        ("Song Name [official video]", "Song Name"),
        ("Song Name [Official Video]", "Song Name"),
        ("[Audio] Song Name", "Song Name"),
        ("[Lyrics] Song Name", "Song Name"),
    ]
    
    print("\nTesting bracket formats:")
    all_passed = True
    for original, expected in test_cases:
        result = normalize_title(original)
        passed = result == expected
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} '{original}' -> '{result}'")
        if not passed:
            all_passed = False
            print(f"      Expected: '{expected}'")
    
    return all_passed


def test_complex_cases():
    """Test complex real-world examples."""
    test_cases = [
        ("Artist - Song Name (audio)", "Artist - Song Name"),
        ("Artist - Song Name [Official Video]", "Artist - Song Name"),
        ("Song Name - Official Video", "Song Name"),
        ("Song Name | Lyrics", "Song Name"),
        ("Song Name HD", "Song Name"),
        ("Song Name 4K", "Song Name"),
        ("Song Name HQ", "Song Name"),
    ]
    
    print("\nTesting complex cases:")
    all_passed = True
    for original, expected in test_cases:
        result = normalize_title(original)
        passed = result == expected
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} '{original}' -> '{result}'")
        if not passed:
            all_passed = False
            print(f"      Expected: '{expected}'")
    
    return all_passed


def test_artist_normalization():
    """Test artist name normalization."""
    test_cases = [
        ("Artist Name - Topic", "Artist Name"),
        ("Artist Name - VEVO", "Artist Name"),
        ("Artist Name", "Artist Name"),
    ]
    
    print("\nTesting artist normalization:")
    all_passed = True
    for original, expected in test_cases:
        result = normalize_artist(original)
        passed = result == expected
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} '{original}' -> '{result}'")
        if not passed:
            all_passed = False
            print(f"      Expected: '{expected}'")
    
    return all_passed


def test_combined_normalization():
    """Test normalizing title and artist together."""
    test_cases = [
        (("Song Name (audio)", "Artist Name"), ("Song Name", "Artist Name")),
        (("Song Name (Official Video)", "Artist - Topic"), ("Song Name", "Artist")),
        (("Song Name", None), ("Song Name", "")),
        (("Song Name (audio)", None), ("Song Name", "")),
    ]
    
    print("\nTesting combined normalization:")
    all_passed = True
    for (original_title, original_artist), (expected_title, expected_artist) in test_cases:
        result_title, result_artist = normalize_title_and_artist(original_title, original_artist)
        passed = result_title == expected_title and result_artist == expected_artist
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} Title: '{original_title}', Artist: '{original_artist}'")
        print(f"      -> Title: '{result_title}', Artist: '{result_artist}'")
        if not passed:
            all_passed = False
            print(f"      Expected: Title: '{expected_title}', Artist: '{expected_artist}'")
    
    return all_passed


def run_all_tests():
    """Run all tests."""
    print("="*70)
    print("TITLE NORMALIZER TESTS")
    print("="*70)
    
    results = []
    results.append(("Common video tags", test_common_video_tags()))
    results.append(("Bracket formats", test_bracket_formats()))
    results.append(("Complex cases", test_complex_cases()))
    results.append(("Artist normalization", test_artist_normalization()))
    results.append(("Combined normalization", test_combined_normalization()))
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {test_name}")
    
    print(f"\n  Total: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n  [SUCCESS] All tests passed!")
        return True
    else:
        print(f"\n  [WARNING] {total - passed} test suite(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

# ==============================================================================
# END OF SPRINT 4 - ARUHANT
# ==============================================================================

