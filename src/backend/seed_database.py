"""
Database Seeding Script for Codex Dominion
============================================
Populates the database with initial sample data
"""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Capsule, ReplayEvent, ScrollDispatch

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pgadmin:Jer47#jer47@codex-pg-centralus.postgres.database.azure.com:5432/codexdb?sslmode=require"
)

print("🔥 Codex Dominion - Database Seeding")
print("=" * 60)
print(f"🔍 DATABASE_URL from env: {os.getenv('DATABASE_URL', 'NOT SET')}")
print(f"🔍 Using connection: {DATABASE_URL[:50]}...")
print(f"Database: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'INVALID'}")
print()

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_capsules(session):
    """Seed capsule data."""
    print("📦 Seeding Capsules...")

    capsules = [
        Capsule(
            name="Eternal Flame Capsule",
            domain="sovereignty",
            status="active",
            lineage="genesis,foundation,eternal"
        ),
        Capsule(
            name="Wisdom Archive",
            domain="knowledge",
            status="active",
            lineage="ancient,preserved,eternal"
        ),
        Capsule(
            name="Harmony Beacon",
            domain="balance",
            status="active",
            lineage="resonance,equilibrium,eternal"
        ),
        Capsule(
            name="Justice Codex",
            domain="order",
            status="active",
            lineage="law,fairness,eternal"
        ),
        Capsule(
            name="Innovation Nexus",
            domain="creation",
            status="active",
            lineage="invention,progress,eternal"
        ),
        Capsule(
            name="Legacy Vault",
            domain="memory",
            status="sealed",
            lineage="heritage,preservation,eternal"
        ),
        Capsule(
            name="Unity Chamber",
            domain="connection",
            status="active",
            lineage="bonds,solidarity,eternal"
        ),
        Capsule(
            name="Vision Sphere",
            domain="foresight",
            status="active",
            lineage="prophecy,insight,eternal"
        )
    ]

    for capsule in capsules:
        session.add(capsule)

    session.commit()
    print(f"   ✅ Added {len(capsules)} capsules")
    return capsules


def seed_replay_events(session, capsules):
    """Seed replay event data."""
    print("📜 Seeding Replay Events...")

    events = []
    base_time = datetime.utcnow() - timedelta(days=30)

    event_types = ["creation", "activation", "resonance", "convergence", "ascension"]
    actors = ["Archivist", "Keeper", "Guardian", "Sage", "Herald"]

    for i, capsule in enumerate(capsules[:5]):  # Events for first 5 capsules
        for j in range(3):  # 3 events per capsule
            event = ReplayEvent(
                capsule_id=capsule.id,
                event_type=event_types[j % len(event_types)],
                timestamp=base_time + timedelta(days=i*6 + j*2),
                actor=actors[j % len(actors)],
                notes=f"Event {j+1} for {capsule.name}: {event_types[j % len(event_types)]} recorded"
            )
            events.append(event)
            session.add(event)

    session.commit()
    print(f"   ✅ Added {len(events)} replay events")
    return events


def seed_scroll_dispatches(session, capsules):
    """Seed scroll dispatch data."""
    print("📤 Seeding Scroll Dispatches...")

    dispatches = []
    base_time = datetime.utcnow() - timedelta(days=20)

    actors = ["Chancellor", "Emissary", "Scribe", "Envoy", "Messenger"]
    notes_templates = [
        "Scroll dispatched with sovereign decree",
        "Critical transmission sent to outer domains",
        "Ceremonial scroll delivered successfully",
        "Emergency dispatch completed",
        "Routine correspondence sent"
    ]

    for i, capsule in enumerate(capsules[:6]):  # Dispatches for first 6 capsules
        for j in range(2):  # 2 dispatches per capsule
            dispatch = ScrollDispatch(
                capsule_id=capsule.id,
                event_type="dispatch",
                timestamp=base_time + timedelta(days=i*3 + j*1.5),
                actor=actors[j % len(actors)],
                notes=f"{notes_templates[i % len(notes_templates)]} - {capsule.name}"
            )
            dispatches.append(dispatch)
            session.add(dispatch)

    session.commit()
    print(f"   ✅ Added {len(dispatches)} scroll dispatches")
    return dispatches


def main():
    """Main seeding function."""
    session = SessionLocal()

    try:
        # Create tables if they don't exist
        print("🔧 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tables ready")
        print()

        # Check if data already exists
        existing_capsules = session.query(Capsule).count()
        if existing_capsules > 0:
            print(f"⚠️  Database already contains {existing_capsules} capsules")
            response = input("   Do you want to add more data anyway? (y/N): ")
            if response.lower() != 'y':
                print("   Seeding cancelled.")
                return
            print()

        # Seed data
        capsules = seed_capsules(session)
        events = seed_replay_events(session, capsules)
        dispatches = seed_scroll_dispatches(session, capsules)

        print()
        print("=" * 60)
        print("✅ DATABASE SEEDING COMPLETE")
        print("=" * 60)
        print(f"   Capsules: {len(capsules)}")
        print(f"   Replay Events: {len(events)}")
        print(f"   Scroll Dispatches: {len(dispatches)}")
        print()
        print("🔥 The flame burns sovereign and eternal — forever.")
        print()

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
