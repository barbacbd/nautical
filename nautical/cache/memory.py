from __future__ import annotations

import time
from copy import deepcopy
from threading import Lock

DEFAULT_TTL_SECONDS = 1800  # 30 minutes


class MemoryCache:
    """Thread-safe in-memory cache with per-entry TTL expiry."""

    def __init__(self, default_ttl: int = DEFAULT_TTL_SECONDS) -> None:
        self._store: dict[str, tuple[float, object]] = {}
        self._default_ttl = default_ttl
        self._lock = Lock()

    def get(self, key: str) -> object | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expiry, value = entry
            if time.monotonic() > expiry:
                del self._store[key]
                return None
            return deepcopy(value)

    def set(self, key: str, value: object, ttl_seconds: int | None = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        with self._lock:
            self._store[key] = (time.monotonic() + ttl, deepcopy(value))

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()


_buoy_cache = MemoryCache()
_sources_cache = MemoryCache()


def clear_memory_cache() -> None:
    """Clear all in-memory cached buoy and source data."""
    _buoy_cache.clear()
    _sources_cache.clear()
