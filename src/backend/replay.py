from fastapi import APIRouter, Depends
from src.backend.models import ReplayEvent
from sqlalchemy.orm import Session
from src.backend.db import get_db

router = APIRouter()

@router.get("/log/{capsule_id}")
def get_replay_events(capsule_id: int, db: Session = Depends(get_db)):
    events = db.query(ReplayEvent).filter(ReplayEvent.capsule_id == capsule_id).all()
    return [
        {
            "id": e.id,
            "capsule_id": e.capsule_id,
            "event_type": e.event_type,
            "timestamp": e.timestamp,
            "actor": e.actor,
            "notes": e.notes
        }
        for e in events
    ]