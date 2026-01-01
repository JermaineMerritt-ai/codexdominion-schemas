"""
CODEX DOMINION - COUNCILS MIGRATION
==========================================
Migrate councils from councils.json to PostgreSQL/SQLite database

Usage:
    python scripts/migrations/migrate_councils_from_json.py
"""

import json
import sys
import os
from pathlib import Path
import uuid
from contextlib import contextmanager

# Set SQLite database before any imports
os.environ['DATABASE_URL'] = 'sqlite:///codexdominion.db'

# Add parent directory to path to import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import Base, Council, CouncilMember
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Create SQLite engine directly
engine = create_engine(
    'sqlite:///codexdominion.db',
    echo=False,
    poolclass=StaticPool,
    connect_args={'check_same_thread': False}
)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def load_councils_json(json_path: str = "councils.json"):
    """Load councils from JSON file"""
    json_file = Path(__file__).parent.parent.parent / json_path
    if not json_file.exists():
        print(f"❌ JSON file not found: {json_file}")
        sys.exit(1)
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both array and object with "councils" key
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "councils" in data:
        return data["councils"]
    else:
        print("❌ Unexpected JSON structure. Expected array or object with 'councils' key")
        sys.exit(1)


def migrate_councils():
    """Migrate councils from JSON to Postgres"""
    print("🔄 Starting council migration from JSON to Postgres...")
    
    # Connect to database using centralized session
    Base.metadata.create_all(engine)  # Ensure tables exist
    
    with get_db_session() as session:
        try:
            # Load JSON data
            councils_data = load_councils_json()
            print(f"📋 Found {len(councils_data)} councils in JSON")
            
            # Check existing councils
            existing_count = session.query(Council).count()
            print(f"📊 Database currently has {existing_count} councils")
            
            # Process each council
            inserted = 0
            updated = 0
            skipped = 0
            
            for council_data in councils_data:
                council_id = council_data.get("id")
                if not council_id:
                    print(f"⚠️  Skipping council without ID: {council_data.get('name', 'Unknown')}")
                    skipped += 1
                    continue
                
                # Check if council already exists
                existing = session.query(Council).filter(Council.id == council_id).first()
                
                if existing:
                    # Update existing council (match new models.py structure)
                    existing.name = council_data.get("name") or existing.name
                    existing.description = council_data.get("purpose") or council_data.get("description") or existing.description
                    existing.is_active = council_data.get("status", "active") == "active"
                    if council_data.get("config"):
                        existing.config = council_data.get("config")
                    elif not existing.config:
                        # Migrate old fields to config JSON
                        existing.config = {
                            "domain": council_data.get("domain"),
                            "primary_engines": council_data.get("primary_engines", []),
                            "oversight": council_data.get("oversight", {})
                        }
                    updated += 1
                    print(f"✏️  Updated: {existing.name} ({council_id})")
                else:
                    # Create new council (matching new models.py structure)
                    # Migrate old structure fields to config JSON
                    config = council_data.get("config", {})
                    if not config:
                        config = {
                            "domain": council_data.get("domain"),
                            "primary_engines": council_data.get("primary_engines", []),
                            "oversight": council_data.get("oversight", {})
                        }
                    
                    council = Council(
                        id=council_id,
                        name=council_data.get("name", "Unnamed Council"),
                        description=council_data.get("purpose") or council_data.get("description"),
                        is_active=council_data.get("status", "active") == "active",
                        config=config
                    )
                    session.add(council)
                    inserted += 1
                    print(f"➕ Inserted: {council.name} ({council_id})")
                    
                    # Create council members if present
                    members = council_data.get("members", [])
                    for agent_id in members:
                        member = CouncilMember(
                            id=f"cm_{uuid.uuid4().hex[:12]}",
                            council_id=council_id,
                            agent_id=agent_id,
                            name=agent_id,  # Will be updated when agents are loaded
                            is_active=True
                        )
                        session.add(member)
                    print(f"   Added {len(members)} members")
            
            # Commit transaction
            session.commit()
            
            print("\n" + "=" * 60)
            print("✅ Migration complete!")
            print(f"   Inserted: {inserted}")
            print(f"   Updated:  {updated}")
            print(f"   Skipped:  {skipped}")
            print(f"   Total in DB: {session.query(Council).count()}")
            print("=" * 60)
        
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    migrate_councils()
