import time
from os import environ
from os.path import exists
from shutil import rmtree

import pytest

environ["NAUTICAL_CACHE_DIR"] = "nautical_cache_memory_tests"

from nautical.cache.file import (
    NAUTICAL_CACHE_DIR,
    NAUTICAL_CACHE_FILE,
    load_buoy,
    load_sources,
    save_buoy,
    save_sources,
    setup,
)
from nautical.cache.memory import MemoryCache, _buoy_cache, _sources_cache, clear_memory_cache
from nautical.noaa.buoy import Buoy, Source


def _make_test_buoy(station_id="TEST01", valid=True):
    return Buoy.from_json(
        {
            "data": {
                "wdir": "ESE",
                "wspd": 10.2,
                "gst": 15.9,
                "wspd10m": 10.4,
                "wspd20m": 13.4,
                "wvht": 2.5,
                "dpd": 2.5,
                "apd": 2.5,
                "mwd": "E",
                "wwh": 3.5,
                "wwp": 7,
                "wwd": "ESE",
                "swh": 10.0,
                "swp": 1.4,
                "swd": "W",
                "pres": 1.8,
                "ptdy": 1.8,
                "atmp": 76.5,
                "wtmp": 65.3,
                "otmp": 65.3,
                "dewp": 85.0,
                "time": "09:34:00",
                "dd": 10,
                "mm": 1,
                "year": 2020,
            },
            "station": station_id,
            "description": "Test buoy",
            "valid": valid,
            "location": {"latitude": 36.0, "longitude": -75.34},
        }
    )


def _make_test_source(name="TestSource"):
    return Source.from_json(
        {
            "buoys": [
                {
                    "station": "TestBuoy",
                    "data": {
                        "wdir": "ESE",
                        "wspd": 10.2,
                        "gst": 15.9,
                        "wspd10m": 10.4,
                        "wspd20m": 13.4,
                        "wvht": 2.5,
                        "dpd": 2.5,
                        "apd": 2.5,
                        "mwd": "E",
                        "wwh": 3.5,
                        "wwp": 7,
                        "wwd": "ESE",
                        "swh": 10.0,
                        "swp": 1.4,
                        "swd": "W",
                        "pres": 1.8,
                        "ptdy": 1.8,
                        "atmp": 76.5,
                        "wtmp": 65.3,
                        "otmp": 65.3,
                        "dewp": 85.0,
                        "time": "09:34:00",
                        "dd": 10,
                        "mm": 1,
                        "year": 2020,
                    },
                }
            ],
            "name": name,
            "description": "Test source",
        }
    )


class TestMemoryCache:
    """Tests for the in-memory TTL cache."""

    def test_set_and_get(self):
        cache = MemoryCache()
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_missing_key(self):
        cache = MemoryCache()
        assert cache.get("nonexistent") is None

    def test_ttl_expiry(self):
        cache = MemoryCache(default_ttl=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_custom_ttl_per_entry(self):
        cache = MemoryCache(default_ttl=60)
        cache.set("short", "data", ttl_seconds=1)
        cache.set("long", "data", ttl_seconds=60)
        time.sleep(1.1)
        assert cache.get("short") is None
        assert cache.get("long") == "data"

    def test_invalidate(self):
        cache = MemoryCache()
        cache.set("key1", "value1")
        cache.invalidate("key1")
        assert cache.get("key1") is None

    def test_invalidate_missing_key(self):
        cache = MemoryCache()
        cache.invalidate("nonexistent")

    def test_clear(self):
        cache = MemoryCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.get("a") is None
        assert cache.get("b") is None

    def test_deep_copy_isolation(self):
        """Cached values should be independent copies."""
        cache = MemoryCache()
        original = {"key": [1, 2, 3]}
        cache.set("test", original)
        original["key"].append(4)
        retrieved = cache.get("test")
        assert retrieved["key"] == [1, 2, 3]

    def test_overwrite(self):
        cache = MemoryCache()
        cache.set("key1", "old")
        cache.set("key1", "new")
        assert cache.get("key1") == "new"


class TestClearMemoryCache:
    """Tests for clear_memory_cache()."""

    def test_clears_both_caches(self):
        _buoy_cache.set("test_buoy", "data")
        _sources_cache.set("test_source", "data")
        clear_memory_cache()
        assert _buoy_cache.get("test_buoy") is None
        assert _sources_cache.get("test_source") is None


class TestDiskCacheHelpers:
    """Tests for load_buoy/save_buoy/load_sources/save_sources."""

    @pytest.fixture(autouse=True)
    def cleanup(self):
        setup()
        yield
        if exists(NAUTICAL_CACHE_DIR):
            rmtree(NAUTICAL_CACHE_DIR)

    def test_save_and_load_buoy(self):
        buoy = _make_test_buoy("DISK01")
        save_buoy(buoy)
        loaded = load_buoy("DISK01")
        assert loaded is not None
        assert loaded.station == "DISK01"
        assert loaded.valid is True

    def test_load_buoy_not_found(self):
        assert load_buoy("NONEXISTENT") is None

    def test_save_buoy_upsert(self):
        buoy1 = _make_test_buoy("UPSERT01")
        save_buoy(buoy1)
        buoy2 = _make_test_buoy("UPSERT01")
        save_buoy(buoy2)
        loaded = load_buoy("UPSERT01")
        assert loaded is not None
        assert loaded.station == "UPSERT01"

    def test_save_and_load_sources(self):
        source = _make_test_source("DiskSource")
        save_sources({"DiskSource": source})
        loaded = load_sources()
        assert loaded is not None
        assert "DiskSource" in loaded

    def test_load_sources_empty(self):
        assert load_sources() is None
