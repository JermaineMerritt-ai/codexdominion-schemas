"""
Redis Client Utilities
======================
Provides Redis connection management and helper functions.
"""
import os
from typing import Optional

import redis.asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL")
redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> Optional[aioredis.Redis]:
    """
    Get Redis client instance.

    Returns:
        Redis client if configured, None otherwise
    """
    global redis_client
    if REDIS_URL and redis_client is None:
        redis_client = aioredis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client


async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


# Cache decorators and helpers
async def cache_set(key: str, value: str, expire: int = 3600):
    """
    Set a value in Redis cache.

    Args:
        key: Cache key
        value: Value to cache
        expire: Expiration time in seconds (default: 1 hour)
    """
    client = await get_redis()
    if client:
        await client.setex(key, expire, value)


async def cache_get(key: str) -> Optional[str]:
    """
    Get a value from Redis cache.

    Args:
        key: Cache key

    Returns:
        Cached value or None if not found
    """
    client = await get_redis()
    if client:
        return await client.get(key)
    return None


async def cache_delete(key: str):
    """
    Delete a value from Redis cache.

    Args:
        key: Cache key
    """
    client = await get_redis()
    if client:
        await client.delete(key)


async def cache_exists(key: str) -> bool:
    """
    Check if key exists in Redis cache.

    Args:
        key: Cache key

    Returns:
        True if key exists, False otherwise
    """
    client = await get_redis()
    if client:
        return await client.exists(key) > 0
    return False
