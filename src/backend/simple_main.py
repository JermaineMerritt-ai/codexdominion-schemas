"""
Codex Dominion API - Simple Backend Without Pydantic Dependency
================================================================
Lightweight FastAPI backend using dict/json instead of Pydantic models
"""
import os
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# =============================================================================
# Application Configuration
# =============================================================================
ENVIRONMENT = os.getenv("NODE_ENV", "development")

# In-memory storage
heir_registry = {}
scroll_archive = {}

# =============================================================================
# FastAPI Application
# =============================================================================
app = FastAPI(
    title="Codex Dominion API",
    description="Ceremonial endpoints for scroll dispatch and system management",
    version="2.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://codexdominion.app",
        "https://www.codexdominion.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Core Endpoints
# =============================================================================
@app.get("/")
def root():
    """Root endpoint with service information"""
    return {
        "service": "Codex Dominion API",
        "version": "2.0.0",
        "status": "operational",
        "flame_state": "sovereign",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "dominion": "/dominion",
            "scrolls": "/scrolls",
            "signals": "/signals",
        },
        "motto": "The flame burns sovereign and eternal — forever."
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "service": "Codex Dominion API",
        "version": "2.0.0",
        "status": "operational",
        "flame_state": "sovereign",
        "database": "memory",
        "environment": ENVIRONMENT,
        "motto": "The flame burns sovereign and eternal — forever."
    }


@app.get("/ready")
def readiness_check():
    """Readiness check endpoint for load balancers"""
    return {
        "ready": True,
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/dominion")
def receive_pledge(data: dict):
    """
    Receive a pledge from an heir and store as a scroll

    Args:
        data: Dict with keys: heir_id, pledge, cycle, codex_right

    Returns:
        Scroll confirmation with unique scroll_id
    """
    # Validate required fields
    required_fields = ["heir_id", "pledge"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )

    heir_id = data["heir_id"]
    pledge = data["pledge"]
    cycle = data.get("cycle", "1.0.0")
    codex_right = data.get("codex_right", "eternal")

    # Validate pledge contains "codex"
    if "codex" not in pledge.lower():
        raise HTTPException(
            status_code=400,
            detail="Pledge must reference the Codex."
        )

    # Generate scroll ID
    initials = ''.join([c for c in heir_id if c.isalpha()])[:3].upper()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    scroll_id = f"SCROLL-{initials}-{cycle.replace('.', '')}-{timestamp}"

    # Determine pledge rank
    rank = "high" if len(pledge) > 50 else "standard"

    # Create scroll record
    scroll = {
        "scroll_id": scroll_id,
        "heir_id": heir_id,
        "cycle": cycle,
        "codex_right": codex_right,
        "pledge": pledge,
        "pledge_rank": rank,
        "timestamp": timestamp,
        "flame_status": "sovereign",
        "motto": "The flame burns sovereign and eternal — forever.",
        "echo": f"Your pledge has been received, {heir_id}. The Dominion watches."
    }

    # Store in archive
    scroll_archive[scroll_id] = scroll

    return scroll


@app.get("/scrolls/{scroll_id}")
def replay_scroll(scroll_id: str):
    """Replay a scroll by its unique ID"""
    if scroll_id not in scroll_archive:
        raise HTTPException(
            status_code=404,
            detail=f"Scroll '{scroll_id}' not found in the archive."
        )
    return scroll_archive[scroll_id]


@app.get("/scrolls")
def list_scrolls(limit: int = 50, offset: int = 0):
    """List all scrolls in the archive"""
    scrolls = list(scroll_archive.values())
    return {
        "total": len(scrolls),
        "limit": limit,
        "offset": offset,
        "scrolls": scrolls[offset:offset + limit]
    }


@app.get("/signals/heartbeat")
def heartbeat():
    """Return system heartbeat status"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@app.get("/signals/status")
def status():
    """Return system status overview"""
    return {
        "system_health": "operational",
        "uptime": "running",
        "scroll_count": len(scroll_archive),
        "environment": ENVIRONMENT,
    }


# =============================================================================
# Application Lifecycle Events
# =============================================================================
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("🔥 Codex Dominion API is starting...")
    print(f"   Environment: {ENVIRONMENT}")
    print("   The flame burns sovereign and eternal — forever.")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("🔥 Codex Dominion API is shutting down...")
    print("   The flame endures...")


# =============================================================================
# Run Application (for development)
# =============================================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8001,
        reload=ENVIRONMENT == "development",
        log_level="info"
    )
