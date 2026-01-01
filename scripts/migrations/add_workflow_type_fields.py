"""
Add enhanced fields to workflow_types table
- domain (for council routing)
- required_inputs (JSON)
- expected_outputs (JSON)
- estimated_duration_minutes
- estimated_savings_weekly
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import text
from db import engine, SessionLocal

def upgrade():
    """Add new columns to workflow_types table"""
    with engine.connect() as conn:
        # SQLite doesn't support ADD COLUMN IF NOT EXISTS, so we try-catch
        try:
            conn.execute(text("ALTER TABLE workflow_types ADD COLUMN domain VARCHAR"))
            print("✅ Added column: domain")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️  Column 'domain' already exists")
            else:
                raise
        
        try:
            conn.execute(text("ALTER TABLE workflow_types ADD COLUMN required_inputs JSON"))
            print("✅ Added column: required_inputs")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️  Column 'required_inputs' already exists")
            else:
                raise
        
        try:
            conn.execute(text("ALTER TABLE workflow_types ADD COLUMN expected_outputs JSON"))
            print("✅ Added column: expected_outputs")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️  Column 'expected_outputs' already exists")
            else:
                raise
        
        try:
            conn.execute(text("ALTER TABLE workflow_types ADD COLUMN estimated_duration_minutes INTEGER"))
            print("✅ Added column: estimated_duration_minutes")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️  Column 'estimated_duration_minutes' already exists")
            else:
                raise
        
        try:
            conn.execute(text("ALTER TABLE workflow_types ADD COLUMN estimated_savings_weekly REAL"))
            print("✅ Added column: estimated_savings_weekly")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️  Column 'estimated_savings_weekly' already exists")
            else:
                raise
        
        conn.commit()

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Add enhanced fields to workflow_types")
    print("=" * 60)
    upgrade()
    print("✅ Migration complete!")
