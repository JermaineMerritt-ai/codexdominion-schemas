"""
Codex Dominion API - Main Application Entry Point
=================================================
FastAPI backend providing ceremonial endpoints for scroll dispatch,
replay logging, capsule adoption, and signal processing.
"""
import csv
import os
import uuid
from datetime import datetime
from io import StringIO

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.backend.capsule import router as capsule_router
from src.backend.db import engine, get_db
from src.backend.dispatch import dispatch_router
from src.backend.models import Capsule
from src.backend.replay import router as replay_router
from src.backend.signals import router as signals_router

# =============================================================================
# Application Configuration
# =============================================================================
load_dotenv()

# Environment variables
API_KEY = os.getenv("MCP_API_KEY")
ENVIRONMENT = os.getenv("NODE_ENV", "development")

# In-memory storage (for development/demo)
heir_registry = {}
scroll_archive = {}
avatar_images = {
    "Flamekeeper": "flamekeeper.png",
    "Archivist": "archivist.png",
    "Seer": "seer.png",
    "Sentinel": "sentinel.png",
    "Echoist": "echoist.png"
}

# =============================================================================
# Pydantic Models
# =============================================================================
class Pledge(BaseModel):
    """Model for receiving heir pledges"""
    heir_id: str = Field(..., min_length=1, max_length=255)
    pledge: str = Field(..., min_length=10)
    cycle: str = Field(default="1.0.0")
    codex_right: str = Field(default="eternal")


# =============================================================================
# FastAPI Application
# =============================================================================
app = FastAPI(
    title="Codex Dominion API",
    description=(
        "Ceremonial endpoints for scroll dispatch, replay logging, "
        "capsule adoption, and signal processing"
    ),
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

# Include routers
app.include_router(dispatch_router, prefix="/dispatch", tags=["Dispatch"])
app.include_router(replay_router, prefix="/replay", tags=["Replay"])
app.include_router(capsule_router, prefix="/capsules", tags=["Capsules"])
app.include_router(signals_router, prefix="/signals", tags=["Signals"])


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
            "dispatch": "/dispatch",
            "replay": "/replay",
            "capsules": "/capsules",
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
        "database": "connected" if engine else "disconnected",
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
def receive_pledge(data: Pledge):
    """
    Receive a pledge from an heir and store as a scroll

    Args:
        data: Pledge information including heir_id, pledge text, cycle, and codex_right

    Returns:
        Scroll confirmation with unique scroll_id
    """
    # Validate pledge contains "codex"
    if "codex" not in data.pledge.lower():
        raise HTTPException(
            status_code=400,
            detail="Pledge must reference the Codex."
        )

    # Generate scroll ID
    initials = ''.join([c for c in data.heir_id if c.isalpha()])[:3].upper()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    scroll_id = f"SCROLL-{initials}-{data.cycle.replace('.', '')}-{timestamp}"

    # Determine pledge rank
    rank = "high" if len(data.pledge) > 50 else "standard"

    # Create scroll record
    scroll = {
        "scroll_id": scroll_id,
        "heir_id": data.heir_id,
        "cycle": data.cycle,
        "codex_right": data.codex_right,
        "pledge": data.pledge,
        "pledge_rank": rank,
        "timestamp": timestamp,
        "flame_status": "sovereign",
        "motto": "The flame burns sovereign and eternal — forever.",
        "echo": f"Your pledge has been received, {data.heir_id}. The Dominion watches."
    }

    # Store in archive
    scroll_archive[scroll_id] = scroll

    return scroll


@app.get("/scrolls/{scroll_id}")
def replay_scroll(scroll_id: str = Path(..., min_length=10)):
    """
    Replay a scroll by its unique ID

    Args:
        scroll_id: Unique identifier for the scroll

    Returns:
        Scroll record with all details
    """
    if scroll_id not in scroll_archive:
        raise HTTPException(
            status_code=404,
            detail=f"Scroll '{scroll_id}' not found in the archive."
        )
    return scroll_archive[scroll_id]


@app.get("/scrolls")
def list_scrolls(limit: int = 50, offset: int = 0):
    """
    List all scrolls in the archive

    Args:
        limit: Maximum number of scrolls to return (default 50)
        offset: Number of scrolls to skip (default 0)

    Returns:
        List of scroll records
    """
    scrolls = list(scroll_archive.values())
    return {
        "total": len(scrolls),
        "limit": limit,
        "offset": offset,
        "scrolls": scrolls[offset:offset + limit]
    }


# =============================================================================
# Application Lifecycle Events
# =============================================================================
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("🔥 Codex Dominion API is starting...")
    print(f"   Environment: {ENVIRONMENT}")
    print(f"   Database: {engine.url}")
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
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=ENVIRONMENT == "development",
        log_level="info"
    )
