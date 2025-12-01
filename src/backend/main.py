


@app.get("/ready")
def readiness_check():
    """Readiness check endpoint."""
    return {"ready": True}


@app.post("/dominion")
def receive_pledge(data: Pledge):
    """Receive a pledge and store as a scroll."""
    if "codex" not in data.pledge.lower():
        raise HTTPException(
            status_code=400,
            detail="Pledge must reference the Codex."
        )

    initials = ''.join([c for c in data.heir_id if c.isalpha()])[:3].upper()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    scroll_id = (
        f"SCROLL-{initials}-{data.cycle.replace('.', '')}-{timestamp}"
    )

    rank = "high" if len(data.pledge) > 50 else "standard"

    scroll = {
    capsules = db.query(Capsule).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "domain": c.domain,
            "status": c.status,
            "lineage": c.lineage
        }
        for c in capsules
    ]

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "service": "Super-Codex-AI - Codex Dominion",
        "version": "1.0.0",
        "status": "operational",
        "flame_state": "sovereign",
        "ceremonial_interface": "/dominion",
        "health_check": "/health",
        "readiness_check": "/ready",
        "motto": "The flame burns sovereign and eternal — forever."
    }

@app.get("/ready")
def readiness_check():
    """Readiness check endpoint."""
    return {"ready": True}

@app.post("/dominion")
def receive_pledge(data: Pledge):
    """Receive a pledge and store as a scroll."""
    if "codex" not in data.pledge.lower():
        raise HTTPException(status_code=400, detail="Pledge must reference the Codex.")

    initials = ''.join([c for c in data.heir_id if c.isalpha()])[:3].upper()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    scroll_id = f"SCROLL-{initials}-{data.cycle.replace('.', '')}-{timestamp}"

    rank = "high" if len(data.pledge) > 50 else "standard"

    scroll = {
        "scroll_id": scroll_id,
        "heir_id": data.heir_id,
        "cycle": data.cycle,
        "codex_right": data.codex_right,
        "pledge_rank": rank,
        "timestamp": timestamp,
        "flame_status": "sovereign",
        "motto": "The flame burns sovereign and eternal — forever.",
        "echo": f"Your pledge has been received, {data.heir_id}. The Dominion watches."
    }
    scroll_archive[scroll_id] = scroll
    return scroll

@app.get("/scrolls/{scroll_id}")
def replay_scroll(scroll_id: str = Path(..., min_length=10)):
    """Replay a scroll by its ID."""
    if scroll_id not in scroll_archive:
        raise HTTPException(status_code=404, detail="Scroll not found.")
    return scroll_archive[scroll_id]


load_dotenv()
api_key = os.getenv("MCP_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

heir_registry = {}
scroll_archive = {}
avatar_images = {
    "Flamekeeper": "flamekeeper.png",
    "Archivist": "archivist.png",
    "Seer": "seer.png",
    "Sentinel": "sentinel.png",
    "Echoist": "echoist.png"
}

app = FastAPI(
    title="Codex Dominion API",
    description=(
        "Ceremonial endpoints for scroll dispatch, replay logging, "
        "and capsule adoption"
    ),
    version="1.0.0"
)

app.include_router(dispatch_router, prefix="/dispatch", tags=["Dispatch"])
app.include_router(replay_router, prefix="/replay", tags=["Replay"])
app.include_router(capsule_router, prefix="/capsules", tags=["Capsules"])
app.include_router(signals_router, prefix="/signals", tags=["Signals"])

load_dotenv()
api_key = os.getenv("MCP_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

heir_registry = {}
scroll_archive = {}
avatar_images = {
    "Flamekeeper": "flamekeeper.png",
    "Archivist": "archivist.png",
    "Seer": "seer.png",
    "Sentinel": "sentinel.png",
    "Echoist": "echoist.png"
}

app = FastAPI(
    title="Codex Dominion API",
    description=(
        "Ceremonial endpoints for scroll dispatch, replay logging, "
        "and capsule adoption"
    ),
    version="1.0.0"
)

app.include_router(dispatch_router, prefix="/dispatch", tags=["Dispatch"])
app.include_router(replay_router, prefix="/replay", tags=["Replay"])
app.include_router(capsule_router, prefix="/capsules", tags=["Capsules"])
app.include_router(signals_router, prefix="/signals", tags=["Signals"])
import csv
import os
import uuid
from datetime import datetime
from io import StringIO

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.backend.capsule import router as capsule_router
from src.backend.db import get_db
from src.backend.dispatch import dispatch_router
from src.backend.models import Base, Capsule
from src.backend.replay import router as replay_router
from src.backend.signals import router as signals_router

load_dotenv()
api_key = os.getenv("MCP_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

heir_registry = {}
scroll_archive = {}
avatar_images = {
    "Flamekeeper": "flamekeeper.png",
    "Archivist": "archivist.png",
    "Seer": "seer.png",
    "Sentinel": "sentinel.png",
    "Echoist": "echoist.png"
}

app = FastAPI(
    title="Codex Dominion API",
    description=(
        "Ceremonial endpoints for scroll dispatch, replay logging, "
        "and capsule adoption"
    ),
    version="1.0.0"
)

app.include_router(dispatch_router, prefix="/dispatch", tags=["Dispatch"])
app.include_router(replay_router, prefix="/replay", tags=["Replay"])
app.include_router(capsule_router, prefix="/capsules", tags=["Capsules"])
app.include_router(signals_router, prefix="/signals", tags=["Signals"])
