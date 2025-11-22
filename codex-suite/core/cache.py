#!/usr/bin/env python3
"""
Redis Cache Integration
======================

High-performance caching layer for the Codex Dominion Suite.
Provides fast data access and improved system performance.
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib

# Optional Redis import
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not available - using in-memory cache fallback")

from .settings import CODEX_CONFIG

class CodexCache:
    """High-performance caching system with Redis backend"""
    
    def __init__(self):
        self.redis_config = CODEX_CONFIG.get("redis", {})
        self.redis_client = None
        self.fallback_cache = {}  # In-memory fallback
        
        # Initialize Redis connection if available and enabled
        if REDIS_AVAILABLE and self.redis_config.get("enabled", False):
            self._initialize_redis()
        else:
            print("📦 Using in-memory cache fallback")
    
    def _initialize_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host=self.redis_config.get("host", "127.0.0.1"),
                port=self.redis_config.get("port", 6379),
                db=self.redis_config.get("db", 0),
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test connection
            self.redis_client.ping()
            print(f"✅ Redis connected: {self.redis_config['host']}:{self.redis_config['port']}")
            
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            self.redis_client = None
    
    def _generate_key(self, namespace: str, key: str) -> str:
        """Generate cache key with namespace"""
        return f"codex:{namespace}:{key}"
    
    def set(self, namespace: str, key: str, value: Any, ttl: int = None) -> bool:
        """Set cache value with optional TTL"""
        try:
            cache_key = self._generate_key(namespace, key)
            serialized_value = json.dumps(value)
            
            if self.redis_client:
                ttl = ttl or self.redis_config.get("cache_ttl", 3600)
                result = self.redis_client.setex(cache_key, ttl, serialized_value)
                return bool(result)
            else:
                # Fallback to in-memory cache
                self.fallback_cache[cache_key] = {
                    "value": serialized_value,
                    "expires": datetime.now() + timedelta(seconds=ttl or 3600)
                }
                return True
                
        except Exception as e:
            print(f"⚠️  Cache set failed: {e}")
            return False
    
    def get(self, namespace: str, key: str) -> Optional[Any]:
        """Get cache value"""
        try:
            cache_key = self._generate_key(namespace, key)
            
            if self.redis_client:
                value = self.redis_client.get(cache_key)
                if value:
                    return json.loads(value)
            else:
                # Check fallback cache
                if cache_key in self.fallback_cache:
                    cached_item = self.fallback_cache[cache_key]
                    if datetime.now() < cached_item["expires"]:
                        return json.loads(cached_item["value"])
                    else:
                        # Expired, remove from cache
                        del self.fallback_cache[cache_key]
            
            return None
            
        except Exception as e:
            print(f"⚠️  Cache get failed: {e}")
            return None
    
    def delete(self, namespace: str, key: str) -> bool:
        """Delete cache value"""
        try:
            cache_key = self._generate_key(namespace, key)
            
            if self.redis_client:
                result = self.redis_client.delete(cache_key)
                return bool(result)
            else:
                if cache_key in self.fallback_cache:
                    del self.fallback_cache[cache_key]
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Cache delete failed: {e}")
            return False
    
    def exists(self, namespace: str, key: str) -> bool:
        """Check if cache key exists"""
        try:
            cache_key = self._generate_key(namespace, key)
            
            if self.redis_client:
                return bool(self.redis_client.exists(cache_key))
            else:
                if cache_key in self.fallback_cache:
                    return datetime.now() < self.fallback_cache[cache_key]["expires"]
            
            return False
            
        except Exception as e:
            print(f"⚠️  Cache exists check failed: {e}")
            return False
    
    def clear_namespace(self, namespace: str) -> int:
        """Clear all keys in namespace"""
        try:
            pattern = self._generate_key(namespace, "*")
            
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
            else:
                # Clear from fallback cache
                to_delete = [k for k in self.fallback_cache.keys() if k.startswith(f"codex:{namespace}:")]
                for key in to_delete:
                    del self.fallback_cache[key]
                return len(to_delete)
            
            return 0
            
        except Exception as e:
            print(f"⚠️  Cache namespace clear failed: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        stats = {
            "backend": "redis" if self.redis_client else "memory",
            "connected": bool(self.redis_client),
            "total_keys": 0,
            "memory_usage": 0,
            "hit_rate": 0.0
        }
        
        try:
            if self.redis_client:
                info = self.redis_client.info()
                stats.update({
                    "total_keys": info.get("db0", {}).get("keys", 0),
                    "memory_usage": info.get("used_memory", 0),
                    "hit_rate": info.get("keyspace_hit_rate", 0.0)
                })
            else:
                # Fallback cache stats
                valid_keys = [
                    k for k, v in self.fallback_cache.items()
                    if datetime.now() < v["expires"]
                ]
                stats["total_keys"] = len(valid_keys)
                stats["memory_usage"] = sum(
                    len(str(v["value"])) for v in self.fallback_cache.values()
                )
                
        except Exception as e:
            print(f"⚠️  Cache stats failed: {e}")
        
        return stats

class CachedMemorySystem:
    """Memory system with intelligent caching"""
    
    def __init__(self, memory_system, cache_system):
        self.memory = memory_system
        self.cache = cache_system
    
    def get_cached_search(self, query: str, **kwargs) -> List[Dict]:
        """Perform cached memory search"""
        # Generate cache key from query and parameters
        cache_key = hashlib.md5(f"{query}{str(sorted(kwargs.items()))}".encode()).hexdigest()
        
        # Try cache first
        cached_result = self.cache.get("memory_search", cache_key)
        if cached_result is not None:
            return cached_result
        
        # Perform actual search
        if hasattr(self.memory, 'semantic_search') and kwargs.get('use_semantic', True):
            results = [(mem, score) for mem, score in self.memory.semantic_search(query, **kwargs)]
            results = [mem for mem, score in results]  # Extract just memories
        else:
            results = self.memory.search_memories(query, **kwargs)
        
        # Cache the results for 5 minutes
        self.cache.set("memory_search", cache_key, results, ttl=300)
        
        return results
    
    def get_cached_analytics(self) -> Dict[str, Any]:
        """Get cached analytics"""
        cached_analytics = self.cache.get("system", "analytics")
        if cached_analytics is not None:
            return cached_analytics
        
        # Generate fresh analytics
        if hasattr(self.memory, 'get_enhanced_analytics'):
            analytics = self.memory.get_enhanced_analytics()
        else:
            analytics = self.memory.get_memory_analytics()
        
        # Cache for 10 minutes
        self.cache.set("system", "analytics", analytics, ttl=600)
        
        return analytics
    
    def invalidate_search_cache(self):
        """Invalidate search cache when memories are added/modified"""
        self.cache.clear_namespace("memory_search")
    
    def store_memory_with_cache_invalidation(self, **kwargs):
        """Store memory and invalidate relevant caches"""
        result = self.memory.store_memory(**kwargs)
        self.invalidate_search_cache()
        self.cache.delete("system", "analytics")  # Invalidate analytics cache
        return result

class PerformanceMonitor:
    """Monitor system performance and cache effectiveness"""
    
    def __init__(self, cache_system):
        self.cache = cache_system
        self.metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "search_times": [],
            "memory_operations": 0
        }
    
    def record_cache_hit(self):
        """Record a cache hit"""
        self.metrics["cache_hits"] += 1
    
    def record_cache_miss(self):
        """Record a cache miss"""
        self.metrics["cache_misses"] += 1
    
    def record_search_time(self, duration: float):
        """Record search operation time"""
        self.metrics["search_times"].append(duration)
        # Keep only last 100 measurements
        if len(self.metrics["search_times"]) > 100:
            self.metrics["search_times"] = self.metrics["search_times"][-100:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        total_requests = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        hit_rate = (self.metrics["cache_hits"] / total_requests * 100) if total_requests > 0 else 0
        
        avg_search_time = (
            sum(self.metrics["search_times"]) / len(self.metrics["search_times"])
            if self.metrics["search_times"] else 0
        )
        
        cache_stats = self.cache.get_stats()
        
        return {
            "cache_hit_rate": hit_rate,
            "total_requests": total_requests,
            "average_search_time_ms": avg_search_time * 1000,
            "memory_operations": self.metrics["memory_operations"],
            "cache_backend": cache_stats["backend"],
            "cache_connected": cache_stats["connected"],
            "recommendations": self._generate_recommendations(hit_rate, avg_search_time)
        }
    
    def _generate_recommendations(self, hit_rate: float, avg_time: float) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if hit_rate < 50:
            recommendations.append("🔄 Consider increasing cache TTL for better hit rates")
        
        if avg_time > 0.5:  # 500ms
            recommendations.append("⚡ Search times are high - consider optimizing queries")
        
        if not self.cache.redis_client:
            recommendations.append("🚀 Enable Redis for better performance")
        
        return recommendations

# Global instances
codex_cache = CodexCache()
performance_monitor = PerformanceMonitor(codex_cache)

# Create cached memory system if enhanced memory is available
try:
    from .enhanced_memory import enhanced_codex_memory
    if enhanced_codex_memory:
        cached_memory = CachedMemorySystem(enhanced_codex_memory, codex_cache)
    else:
        cached_memory = None
except ImportError:
    cached_memory = None

if __name__ == "__main__":
    print("🚀 Redis Cache Integration initialized")
    
    # Test cache functionality
    test_success = codex_cache.set("test", "key1", {"message": "Hello Codex!"})
    if test_success:
        retrieved = codex_cache.get("test", "key1")
        print(f"Cache test: {retrieved}")
    
    # Show cache stats
    stats = codex_cache.get_stats()
    print(f"Cache backend: {stats['backend']}")
    print(f"Connected: {stats['connected']}")
    
    if cached_memory:
        print("✅ Cached memory system available")
    else:
        print("⚠️  Cached memory system not available")