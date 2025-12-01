"""Signals API endpoints for Codex Dominion."""

from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/heartbeat")
def heartbeat() -> dict:
    """Return system heartbeat status."""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@router.get("/status")
def status() -> dict:
    """Return system status overview."""
    # Dummy values for now; can be replaced with real system stats
    return {
        "system_health": "operational",
        "uptime": "72h",
        "capsule_count": 42,
        "scrolls_dispatched": 17,
    }


@router.get("/echo")
def echo() -> dict:
    """Echo endpoint for system check."""
    return {"message": "The Dominion hears you."}
