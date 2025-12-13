"""
Redis caching service for Codex Dominion API
Implements caching layer for export endpoints and API responses
"""
import redis
import json
import os
from typing import Optional, Any
from datetime import timedelta

class RedisService:
    """Redis caching service with connection pooling"""

    def __init__(self):
        """Initialize Redis connection from environment variables"""
        redis_host = os.getenv('REDIS_HOST', 'codexdominion-redis.redis.cache.windows.net')
        redis_port = int(os.getenv('REDIS_PORT', '6380'))
        redis_password = os.getenv('REDIS_PASSWORD', '')

        self.redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=True,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )

        # Test connection
        try:
            self.redis_client.ping()
            self.available = True
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.available = False

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.available:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> bool:
        """
        Set value in cache with TTL

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl_seconds: Time to live in seconds (default: 5 minutes)

        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            return False

        try:
            serialized = json.dumps(value)
            self.redis_client.setex(key, ttl_seconds, serialized)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete key from cache

        Args:
            key: Cache key to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            return False

        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    def build_export_key(self, format: str, cycle: Optional[str] = None,
                         engine: Optional[str] = None, role: Optional[str] = None) -> str:
        """
        Build cache key for export endpoints

        Args:
            format: Export format (yaml, markdown, pdf)
            cycle: Cycle filter (daily, seasonal, epochal, millennial)
            engine: Engine filter
            role: Role filter

        Returns:
            Cache key string
        """
        parts = [f"export:{format}"]
        if cycle:
            parts.append(f"cycle:{cycle}")
        if engine:
            parts.append(f"engine:{engine}")
        if role:
            parts.append(f"role:{role}")
        return ":".join(parts)

    def clear_export_cache(self) -> int:
        """
        Clear all export-related cache keys

        Returns:
            Number of keys deleted
        """
        if not self.available:
            return 0

        try:
            keys = self.redis_client.keys("export:*")
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Redis clear cache error: {e}")
            return 0

    def get_stats(self) -> dict:
        """
        Get Redis cache statistics

        Returns:
            Dictionary with cache stats
        """
        if not self.available:
            return {"available": False}

        try:
            info = self.redis_client.info('stats')
            return {
                "available": True,
                "total_commands_processed": info.get('total_commands_processed', 0),
                "keyspace_hits": info.get('keyspace_hits', 0),
                "keyspace_misses": info.get('keyspace_misses', 0),
                "hit_rate": round(
                    info.get('keyspace_hits', 0) /
                    max(info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0), 1) * 100,
                    2
                )
            }
        except Exception as e:
            print(f"Redis stats error: {e}")
            return {"available": False, "error": str(e)}


# Singleton instance
_redis_service = None

def get_redis_service() -> RedisService:
    """Get or create Redis service singleton"""
    global _redis_service
    if _redis_service is None:
        _redis_service = RedisService()
    return _redis_service
