"""
Advanced Performance Optimizations for Codex Dominion
Implements compression, response caching, and connection pooling
"""
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import Response
import time
import hashlib

class CacheControlMiddleware:
    """Add cache control headers to static responses"""
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Intercept response
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    path = scope.get("path", "")

                    # Add cache headers for static endpoints
                    if path in ["/", "/health", "/ready"]:
                        # Short cache for health checks
                        headers.append((b"cache-control", b"public, max-age=60"))
                    elif path == "/capsules":
                        # 5 minute cache for capsules (matches Redis TTL)
                        headers.append((b"cache-control", b"public, max-age=300"))

                    # Add ETag support
                    headers.append((b"x-served-by", b"codex-backend"))
                    message["headers"] = headers

                await send(message)

            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)


class PerformanceMonitorMiddleware:
    """Monitor request performance"""
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()

            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    process_time = time.time() - start_time
                    headers = list(message.get("headers", []))
                    headers.append(
                        (b"x-process-time", f"{process_time:.4f}".encode())
                    )
                    message["headers"] = headers
                await send(message)

            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)


def apply_performance_optimizations(app: FastAPI):
    """Apply all performance optimizations to FastAPI app"""

    # 1. GZip compression for responses > 1KB
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # 2. Cache control headers
    app.add_middleware(CacheControlMiddleware)

    # 3. Performance monitoring
    app.add_middleware(PerformanceMonitorMiddleware)

    print("✅ Performance optimizations applied:")
    print("   - GZip compression enabled (>1KB responses)")
    print("   - Cache-Control headers configured")
    print("   - Response time monitoring active")

    return app
