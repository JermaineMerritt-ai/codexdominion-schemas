from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.models import Capsule
from src.backend.db import get_db

router = APIRouter()

@router.get("/count")
def get_capsule_count(db: Session = Depends(get_db)):
    count = db.query(Capsule).count()
    return {"capsule_count": count}

@router.get("/")
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
