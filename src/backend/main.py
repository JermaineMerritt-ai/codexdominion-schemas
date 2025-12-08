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
from typing import List, Optional

import redis.asyncio as aioredis
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, Path, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# Import from local modules (absolute imports work in Docker)
from capsule import router as capsule_router
from db import engine, get_db
from dispatch import dispatch_router
from models import Capsule
from replay import router as replay_router
from signals import router as signals_router

# =============================================================================
# Application Configuration
# =============================================================================
load_dotenv()

# Environment variables
API_KEY = os.getenv("MCP_API_KEY")
ENVIRONMENT = os.getenv("NODE_ENV", "development")

# Redis connection
redis_url = os.getenv("REDIS_URL")
redis = None
if redis_url:
    redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)

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
# Lifecycle Events
# =============================================================================
@app.on_event("startup")
async def startup_event():
    """Initialize connections and application on startup"""
    global redis
    if redis_url and redis is None:
        redis = aioredis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True
        )
    print("🔥 Codex Dominion API is starting...")
    print(f"   Environment: {ENVIRONMENT}")
    print(f"   Database: {engine.url}")
    if redis:
        print(f"   Redis: Connected")
    print("   The flame burns sovereign and eternal — forever.")


@app.on_event("shutdown")
async def shutdown_event():
    """Close connections and cleanup on shutdown"""
    global redis
    if redis:
        await redis.close()
        print("   Redis: Disconnected")
    print("🔥 Codex Dominion API is shutting down...")
    print("   The flame endures...")


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


# =============================================================================
# AI Chat & Document Processing Endpoints
# =============================================================================
class ChatMessage(BaseModel):
    """Model for AI chat messages"""
    message: str = Field(..., description="User message to AI")
    context: Optional[str] = Field(None, description="Additional context")


class ChatResponse(BaseModel):
    """Model for AI chat response"""
    response: str
    timestamp: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(data: ChatMessage):
    """
    Process AI chat messages from Jermaine Super Action AI

    Args:
        data: User message and optional context

    Returns:
        AI response with timestamp
    """
    # TODO: Integrate with actual AI model (OpenAI, Anthropic, etc.)
    responses = [
        f"I've received your message: '{data.message}'. How can I assist you with Codex Dominion?",
        f"Processing your request about '{data.message}'. The sovereign systems are ready.",
        f"Acknowledged: '{data.message}'. All engines operating at optimal capacity.",
        f"Your inquiry regarding '{data.message}' has been logged. What would you like to create today?"
    ]

    import random
    response_text = random.choice(responses)

    return ChatResponse(
        response=response_text,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Handle document uploads (PDF, DOCX, TXT, MD)

    Args:
        file: Uploaded file from user

    Returns:
        Upload confirmation with file details
    """
    # Read file content
    content = await file.read()
    file_size = len(content)

    # Store in upload directory
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    saved_path = os.path.join(upload_dir, f"{file_id}{file_ext}")

    with open(saved_path, "wb") as f:
        f.write(content)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": file_size,
        "path": saved_path,
        "uploaded_at": datetime.utcnow().isoformat(),
        "status": "success"
    }


class RevenueData(BaseModel):
    """Model for revenue tracking"""
    platform: str
    amount: float
    currency: str = "USD"


@app.get("/api/revenue")
async def get_revenue_data():
    """
    Get real-time revenue data across all platforms

    Returns:
        Revenue breakdown by platform
    """
    # TODO: Integrate with actual payment processors
    return {
        "total": 76600.00,
        "currency": "USD",
        "stores": {
            "woocommerce": 28500.00,
            "shopify": 15200.00,
            "total": 43700.00
        },
        "channels": {
            "youtube": 12300.00,
            "tiktok": 8400.00,
            "twitch": 3200.00,
            "total": 23900.00
        },
        "websites": {
            "codexdominion": 5800.00,
            "other": 1200.00,
            "total": 7000.00
        },
        "apps": {
            "mobile": 1500.00,
            "desktop": 500.00,
            "total": 2000.00
        },
        "updated_at": datetime.utcnow().isoformat()
    }


# =============================================================================
# Scroll Management Endpoints
# =============================================================================
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
