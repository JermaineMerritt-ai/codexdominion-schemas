from src.backend.models import Capsule, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Use the same database URL as your backend
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)
session = Session(bind=engine)

capsules = [
    Capsule(name="Supermarket", domain="Commerce", status="Active", lineage=["Blueprinted", "Crowned"]),
    Capsule(name="Healthcare", domain="Wellness", status="Pending", lineage=["Blueprinted"]),
    Capsule(name="Genesis", domain="Creation", status="Active", lineage=["Blueprinted", "Crowned"]),
    Capsule(name="Restaurant", domain="Food", status="Active", lineage=["Blueprinted", "Crowned"]),
]

session.add_all(capsules)
session.commit()
session.close()
