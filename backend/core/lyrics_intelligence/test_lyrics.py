from dataclasses import make_dataclass
from pathlib import Path

import pytest

from backend.core.lyrics_intelligence import scraper, synchronizer, title_normalizer


# ---------- title_normalizer ----------

@pytest.mark.smoke
def test_normalize_title_basic_cases():
    cases = [
        ("Song Name (audio)", "Song Name"),
        ("Artist - Song Name [Official Video]", "Artist - Song Name"),
        ("Song Name | Lyrics", "Song Name"),
    ]
    for original, expected in cases:
        assert title_normalizer.normalize_title(original) == expected


@pytest.mark.regression
def test_normalize_artist_and_combined():
    assert title_normalizer.normalize_artist("Artist - Topic") == "Artist"
    t, a = title_normalizer.normalize_title_and_artist("Song (Audio)", "Artist - VEVO")
    assert t == "Song" and a == "Artist"


# ---------- scraper.fetch_lyrics ----------

@pytest.mark.smoke
def test_fetch_lyrics_picks_closest_duration(monkeypatch):
    # Build fake result objects
    Result = make_dataclass("Result", [
        ("track_name", str), ("artist_name", str), ("duration", int), ("synced_lyrics", str), ("plain_lyrics", str)
    ])
    results = [
        Result("A", "X", 190, "[00:01.00]A", "A\nB"),
        Result("B", "Y", 200, "[00:01.00]B", "B\nC"),
        Result("C", "Z", 210, "[00:01.00]C", "C\nD"),
    ]

    class FakeAPI:
        def __init__(self, user_agent):
            pass
        def search_lyrics(self, query):
            return results

    monkeypatch.setattr(scraper, "LrcLibAPI", FakeAPI)

    best = scraper.fetch_lyrics("query", duration=205)
    # In a tie (200 vs 210 both 5s away), function keeps first minimal
    assert best.track_name == "B"


@pytest.mark.regression
def test_fetch_lyrics_returns_none_on_empty(monkeypatch):
    class FakeAPI:
        def __init__(self, user_agent):
            pass
        def search_lyrics(self, query):
            return []
    monkeypatch.setattr(scraper, "LrcLibAPI", FakeAPI)

    best = scraper.fetch_lyrics("query", duration=123)
    assert best is None


# ---------- synchronizer ----------

@pytest.mark.smoke
def test_generate_and_parse_lrc_roundtrip(tmp_path: Path):
    lrc = synchronizer.LRCData(
        title="Song", artist="Artist", lyrics=[
            synchronizer.LyricLine(start_time=10.25, end_time=12.00, text="line1"),
            synchronizer.LyricLine(start_time=20.50, end_time=22.00, text="line2"),
        ]
    )
    out = synchronizer.generate_lrc_file(lrc, str(tmp_path / "song.lrc"))
    parsed = synchronizer.parse_lrc_file(out)
    assert parsed.title == "Song" and parsed.artist == "Artist"
    assert len(parsed.lyrics) == 2
    assert parsed.lyrics[0].text == "line1" and pytest.approx(parsed.lyrics[0].start_time, 0.01) == 10.25


@pytest.mark.regression
def test_parse_lrc_with_offset(tmp_path: Path):
    content = """[ti:Song]\n[ar:Artist]\n[offset:-500]\n[00:10.50]first\n[00:20.500]second\n"""
    p = tmp_path / "off.lrc"
    p.write_text(content)
    data = synchronizer.parse_lrc_file(str(p))
    # offset -500ms should subtract 0.5s from timestamps
    assert pytest.approx(data.lyrics[0].start_time, 0.001) == 10.0
    assert pytest.approx(data.lyrics[1].start_time, 0.001) == 20.0


@pytest.mark.smoke
def test_synchronize_plain_lyrics_distribution():
    text = "one\ntwo\nthree\nfour"
    data = synchronizer.synchronize_lyrics_with_audio(text, audio_duration=100)
    assert len(data.lyrics) == 4
    # evenly spaced
    assert pytest.approx(data.lyrics[1].start_time - data.lyrics[0].start_time, 0.1) == 23.75


@pytest.mark.regression
def test_synchronize_from_lrclib_prefers_synced(monkeypatch):
    synced = """[00:01.00]hello\n[00:02.50]world\n"""
    Result = make_dataclass("Result", [
        ("track_name", str), ("artist_name", str), ("duration", int), ("synced_lyrics", str), ("plain_lyrics", str)
    ])
    lr = Result("T", "A", 120, synced, "hello\nworld")
    data = synchronizer.synchronize_from_lrclib_result(lr, audio_duration=120)
    assert len(data.lyrics) == 2
    assert data.title == "T" and data.artist == "A"


@pytest.mark.regression
def test_synchronize_from_lrclib_fallback_to_plain_on_invalid_synced(monkeypatch):
    invalid_synced = "not-an-lrc-format"
    Result = make_dataclass("Result", [
        ("track_name", str), ("artist_name", str), ("duration", int), ("synced_lyrics", str), ("plain_lyrics", str)
    ])
    lr = Result("T", "A", 60, invalid_synced, "a\nb\nc")
    data = synchronizer.synchronize_from_lrclib_result(lr, audio_duration=60)
    assert len(data.lyrics) == 3


@pytest.mark.regression
def test_synchronize_from_lrclib_no_plain_returns_empty():
    Result = make_dataclass("Result", [
        ("track_name", str), ("artist_name", str), ("duration", int), ("synced_lyrics", str), ("plain_lyrics", str)
    ])
    lr = Result("T", "A", 60, "", "")
    data = synchronizer.synchronize_from_lrclib_result(lr, audio_duration=60)
    assert len(data.lyrics) == 0
