

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ReplayEvent(Base):
    __tablename__ = "replay_events"
    id = Column(Integer, primary_key=True)
    capsule_id = Column(Integer)
    event_type = Column(String)
    timestamp = Column(DateTime)
    actor = Column(String)
    notes = Column(String)


class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    domain = Column(String)
    status = Column(String)
    lineage = Column(String)  # Store as comma-separated string

class ScrollDispatch(Base):
    __tablename__ = "scroll_dispatches"
    id = Column(Integer, primary_key=True, index=True)
    capsule_id = Column(Integer, nullable=False)
    event_type = Column(String, default="dispatch")
    timestamp = Column(DateTime, default=datetime.utcnow)
    actor = Column(String, nullable=False)
    notes = Column(String, nullable=True)
