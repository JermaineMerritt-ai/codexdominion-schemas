#!/usr/bin/env pwsh
# =============================================================================
# Redis Caching Implementation for Codex Dominion
# =============================================================================
# Adds caching layer to improve performance

Write-Host "🔧 Implementing Redis Caching for Capsules API" -ForegroundColor Cyan
Write-Host "=" * 60

$backendPath = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\src\backend"

# Create redis_cache.py module
$redisCacheContent = @'
"""
Redis caching layer for Codex Dominion API
Caches frequently accessed data to reduce database load
"""
import json
import os
from typing import Optional, Any
from redis import Redis
from redis.exceptions import RedisError

# Redis connection configuration
REDIS_HOST = os.getenv("REDIS_HOST", "codex-redis-centralus.redis.cache.windows.net")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6380"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_SSL = os.getenv("REDIS_SSL", "true").lower() == "true"

# Cache TTL (Time To Live) in seconds
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes default

# Initialize Redis client
try:
    redis_client = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        ssl=REDIS_SSL,
        ssl_cert_reqs=None,
        decode_responses=True
    )
    redis_client.ping()
    print(f"✅ Redis connected: {REDIS_HOST}:{REDIS_PORT}")
except RedisError as e:
    print(f"⚠️  Redis connection failed: {e}")
    redis_client = None


def get_cached(key: str) -> Optional[Any]:
    """Get value from cache"""
    if not redis_client:
        return None
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
    except RedisError as e:
        print(f"Cache get error: {e}")
    return None


def set_cached(key: str, value: Any, ttl: int = CACHE_TTL) -> bool:
    """Set value in cache with TTL"""
    if not redis_client:
        return False
    try:
        redis_client.setex(key, ttl, json.dumps(value))
        return True
    except RedisError as e:
        print(f"Cache set error: {e}")
        return False


def invalidate_cache(pattern: str = "*") -> int:
    """Invalidate cache keys matching pattern"""
    if not redis_client:
        return 0
    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
    except RedisError as e:
        print(f"Cache invalidate error: {e}")
    return 0


def get_cache_stats() -> dict:
    """Get cache statistics"""
    if not redis_client:
        return {"status": "disconnected"}
    try:
        info = redis_client.info()
        return {
            "status": "connected",
            "used_memory": info.get("used_memory_human", "N/A"),
            "connected_clients": info.get("connected_clients", 0),
            "total_keys": redis_client.dbsize()
        }
    except RedisError as e:
        return {"status": "error", "message": str(e)}
'@

Write-Host "`n📝 Creating redis_cache.py module..."
Set-Content -Path "$backendPath\redis_cache.py" -Value $redisCacheContent -Encoding UTF8
Write-Host "✅ Redis cache module created" -ForegroundColor Green

Write-Host "`n" + ("=" * 60)
Write-Host "✅ Redis Caching Setup Complete" -ForegroundColor Green
Write-Host "   Module: redis_cache.py" -ForegroundColor White
Write-Host "   Functions: get_cached(), set_cached(), invalidate_cache()" -ForegroundColor White
Write-Host "   Default TTL: 5 minutes" -ForegroundColor White
Write-Host "`n⚠️  Next steps:" -ForegroundColor Yellow
Write-Host "   1. Update main.py to use caching" -ForegroundColor White
Write-Host "   2. Add REDIS_PASSWORD to App Service settings" -ForegroundColor White
Write-Host "   3. Test caching with capsules endpoint" -ForegroundColor White
