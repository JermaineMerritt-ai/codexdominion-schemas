from fastapi import FastAPI
heir_registry = {}
# Mapping of avatar titles to image filenames
avatar_images = {
    "Flamekeeper": "flamekeeper.png",
    "Archivist": "archivist.png",
    "Seer": "seer.png",
    "Sentinel": "sentinel.png",
    "Echoist": "echoist.png"
}

# ...existing code...
import csv
from fastapi.responses import StreamingResponse
from io import StringIO

app = FastAPI(
    title="Codex Dominion API",
    description="Ceremonial endpoints for scroll dispatch, replay logging, and capsule adoption",
    version="1.0.0"
)

# ...existing code...


from pydantic import BaseModel, Field

class Heir(BaseModel):
    name: str
    avatar: str
    scroll: str

# Heir registration endpoints
@app.get("/heirs")
def list_all_heirs():
    return list(heir_registry.values())
@app.post("/heirs")
def register_heir(heir: Heir):
    heir_registry[heir.heir_id] = heir.dict()
    return {"status": "registered", "heir_id": heir.heir_id}

# Download ledger as CSV
@app.get("/heirs/ledger")
def download_ledger():
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["heir_id", "name", "codex_right", "origin_cycle", "avatar", "oath"])
    writer.writeheader()
    for heir in heir_registry.values():
        writer.writerow(heir)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=heir_ledger.csv"})

@app.get("/heirs/{heir_id}")
def get_heir(heir_id: str):
    heir = heir_registry.get(heir_id)
    if not heir:
        raise HTTPException(status_code=404, detail="Heir not found")
    avatar_title = heir.get("avatar")
    heir["avatar_image"] = avatar_images.get(avatar_title, "default.png")
    return heir

# ...existing code...

@app.get("/scrolls")
def list_all_scrolls(page: int = 1, page_size: int = 10, query: str = ""):
    scrolls = list(scroll_archive.values())
    if query:
        query_lower = query.lower()
        scrolls = [
            s for s in scrolls
            if query_lower in s["heir_id"].lower() or query in s["cycle"]
        ]
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "scrolls": scrolls[start:end],
        "total": len(scrolls),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(scrolls) + page_size - 1) // page_size
    }


from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.backend.models import Capsule, Base

api_key = os.getenv("MCP_API_KEY")
print("API Key:", api_key)

# Database setup (update connection string as needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)





from src.backend.dispatch import dispatch_router
from src.backend.replay import router as replay_router
from src.backend.capsule import router as capsule_router
from src.backend.signals import router as signals_router



app = FastAPI(
    title="Codex Dominion API",
    description="Ceremonial endpoints for scroll dispatch, replay logging, and capsule adoption",
    version="1.0.0"
)


# Mount routers with clear prefixes
app.include_router(dispatch_router, prefix="/dispatch", tags=["Dispatch"])
app.include_router(replay_router, prefix="/replay", tags=["Replay"])
app.include_router(capsule_router, prefix="/capsules", tags=["Capsules"])
app.include_router(signals_router, prefix="/signals", tags=["Signals"])

from src.backend.db import get_db


@app.get("/")
def read_root():
    return {"message": "Codex Dominion API is running"}

@app.get("/capsule_count")
def get_capsule_count(db: Session = Depends(get_db)):
    count = db.query(Capsule).count()
    return {"capsule_count": count}

# New endpoint to fetch all capsules
@app.get("/capsules")
def get_capsules(db: Session = Depends(get_db)):
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

# Health and readiness endpoints
@app.get("/health")
def health_check():
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
    return {"ready": True}

# Ceremonial scroll dispatch endpoint

from fastapi import HTTPException
from pydantic import BaseModel, Field
import uuid



from fastapi import Path
from datetime import datetime

# In-memory archive for demonstration
scroll_archive = {}

class Pledge(BaseModel):
    heir_id: str = Field(..., min_length=3)
    cycle: str = Field(..., regex=r"^\d{3}\.M\d{2}$")
    pledge: str = Field(..., min_length=10)
    codex_right: str = Field(..., min_length=3)

@app.post("/dominion")
def receive_pledge(data: Pledge):
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
    if scroll_id not in scroll_archive:
        raise HTTPException(status_code=404, detail="Scroll not found.")
    return scroll_archive[scroll_id]
