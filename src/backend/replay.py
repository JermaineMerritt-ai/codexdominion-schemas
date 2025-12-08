"""Replay API endpoints for Codex Dominion."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import ReplayEvent

router = APIRouter()


@router.get("/log/{capsule_id}")
def get_replay_events(capsule_id: int, db: Session = Depends(get_db)) -> list:
    """Return replay events for a given capsule."""
    events = db.query(ReplayEvent).filter(ReplayEvent.capsule_id == capsule_id).all()
    return [
        {
            "id": e.id,
            "capsule_id": e.capsule_id,
            "event_type": e.event_type,
            "timestamp": e.timestamp,
            "actor": e.actor,
            "notes": e.notes,
        }
        for e in events
    ]
