"""Capsule API endpoints for Codex Dominion."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.backend.db import get_db
from src.backend.models import Capsule

router = APIRouter()


@router.get("/count")
def get_capsule_count(db: Session = Depends(get_db)) -> dict:
    """Return the total number of capsules."""
    count = db.query(Capsule).count()
    return {"capsule_count": count}


@router.get("/")
def get_capsules(db: Session = Depends(get_db)) -> list:
    """Return a list of all capsules."""
    capsules = db.query(Capsule).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "domain": c.domain,
            "status": c.status,
            "lineage": c.lineage,
        }
        for c in capsules
    ]
