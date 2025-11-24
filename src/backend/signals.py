from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/heartbeat")
def heartbeat():
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}

@router.get("/status")
def status():
    # Dummy values for now; can be replaced with real system stats
    return {
        "system_health": "operational",
        "uptime": "72h",
        "capsule_count": 42,
        "scrolls_dispatched": 17
    }

@router.get("/echo")
def echo():
    return {"message": "The Dominion hears you."}
