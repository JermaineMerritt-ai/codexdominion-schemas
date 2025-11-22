# codex_capsules/api.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import os

# Use in-memory storage for now (can be switched to database later)
USE_DATABASE = os.getenv("DATABASE_URL") is not None

if USE_DATABASE:
    try:
        from database import CapsuleDatabase
        db = CapsuleDatabase()
    except ImportError:
        USE_DATABASE = False
        print("Database dependencies not available, using in-memory storage")

app = FastAPI(
    title="Codex Capsules API",
    description="Operational sovereignty tracking for ceremonial and technical operations",
    version="1.0.0"
)

# In-memory storage fallback
CAPSULES = {}
RUNS = []
NEXT_RUN_ID = 1

class Capsule(BaseModel):
    slug: str
    title: str
    kind: str
    mode: str
    version: str = "1.0.0"
    status: str = "active"
    entrypoint: str = ""
    schedule: Optional[str] = None

class CapsuleRun(BaseModel):
    capsule_slug: str
    actor: str
    status: str = "success"
    artifact_uri: Optional[str] = None
    checksum: Optional[str] = None

@app.post("/capsules")
def register_capsule(capsule: Capsule):
    """Register a new capsule or update an existing one"""
    if USE_DATABASE:
        try:
            result = db.register_capsule(capsule.dict())
            return result
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")
    else:
        # In-memory storage
        capsule_data = capsule.dict()
        capsule_data["created_at"] = datetime.utcnow().isoformat() + "Z"
        capsule_data["updated_at"] = capsule_data["created_at"]
        CAPSULES[capsule.slug] = capsule_data
        return capsule_data

@app.get("/capsules")
def list_capsules():
    """List all registered capsules"""
    if USE_DATABASE:
        try:
            return db.list_capsules()
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")
    else:
        return list(CAPSULES.values())

@app.post("/capsules/run")
def record_run(run: CapsuleRun):
    """Record a capsule execution run"""
    global NEXT_RUN_ID
    
    if USE_DATABASE:
        try:
            result = db.record_run(run.dict())
            return result
        except ValueError as e:
            raise HTTPException(404, str(e))
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")
    else:
        # Check if capsule exists
        if run.capsule_slug not in CAPSULES:
            raise HTTPException(404, "Capsule not found")
        
        # In-memory storage
        run_data = run.dict()
        run_data["id"] = NEXT_RUN_ID
        run_data["started_at"] = datetime.utcnow().isoformat() + "Z"
        NEXT_RUN_ID += 1
        RUNS.append(run_data)
        return run_data

@app.get("/capsules/runs")
def list_runs(capsule_slug: Optional[str] = Query(None, description="Filter runs by capsule slug")):
    """List all capsule runs, optionally filtered by capsule"""
    if USE_DATABASE:
        try:
            return db.list_runs(capsule_slug)
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")
    else:
        if capsule_slug:
            return [run for run in RUNS if run["capsule_slug"] == capsule_slug]
        return RUNS

@app.get("/capsules/performance")
def get_performance():
    """Get capsule performance analytics"""
    if USE_DATABASE:
        try:
            return db.get_capsule_performance()
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")
    else:
        # Basic performance calculation from in-memory data
        performance = {}
        for run in RUNS:
            slug = run["capsule_slug"]
            if slug not in performance:
                performance[slug] = {"total_runs": 0, "successful_runs": 0}
            performance[slug]["total_runs"] += 1
            if run["status"] == "success":
                performance[slug]["successful_runs"] += 1
        
        result = []
        for slug, stats in performance.items():
            capsule = CAPSULES.get(slug, {})
            result.append({
                "capsule_slug": slug,
                "capsule_title": capsule.get("title", "Unknown"),
                "total_runs": stats["total_runs"],
                "success_rate": stats["successful_runs"] / stats["total_runs"] if stats["total_runs"] > 0 else 0
            })
        return result

@app.get("/capsules/scheduled")
def get_scheduled():
    """Get scheduled capsules and their next run times"""
    if USE_DATABASE:
        try:
            return db.get_scheduled_capsules()
        except Exception as e:
            raise HTTPException(500, f"Database error: {str(e)}")
    else:
        # Return capsules that have a schedule
        scheduled = []
        for capsule in CAPSULES.values():
            if capsule.get("schedule"):
                scheduled.append({
                    "slug": capsule["slug"],
                    "title": capsule["title"],
                    "schedule": capsule["schedule"],
                    "next_run": "Next run calculation requires database integration"
                })
        return scheduled

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}