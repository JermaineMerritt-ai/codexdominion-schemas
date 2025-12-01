"""Cache System for Codex Dominion"""

import time
from typing import Any, Dict, Optional


class CodexCache:
    """Simple cache implementation"""

    def __init__(self):
        self.cache = {}
        self.timestamps = {}

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set a cached value with TTL"""
        self.cache[key] = value
        self.timestamps[key] = time.time() + ttl

    def get(self, key: str) -> Optional[Any]:
        """Get a cached value"""
        if key in self.cache:
            if time.time() < self.timestamps.get(key, 0):
                return self.cache[key]
            else:
                # Expired
                self.cache.pop(key, None)
                self.timestamps.pop(key, None)
        return None

    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()


codex_cache = CodexCache()
