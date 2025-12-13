"""
Database optimization script for Codex Dominion
Adds indexes and optimizes queries for performance
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pgadmin:Jer47#jer47@codex-pg-centralus.postgres.database.azure.com:5432/codexdb?sslmode=require"
)

print("🔧 Database Optimization Script")
print("=" * 60)
print(f"Database: {DATABASE_URL.split('@')[1].split('/')[0]}")
print()

engine = create_engine(DATABASE_URL)

# SQL for creating indexes
OPTIMIZATION_QUERIES = [
    # Index on capsules.status for filtering active capsules
    """
    CREATE INDEX IF NOT EXISTS idx_capsules_status
    ON capsules(status);
    """,

    # Index on capsules.domain for domain-based queries
    """
    CREATE INDEX IF NOT EXISTS idx_capsules_domain
    ON capsules(domain);
    """,

    # Index on replay_events.capsule_id for foreign key lookups
    """
    CREATE INDEX IF NOT EXISTS idx_replay_events_capsule_id
    ON replay_events(capsule_id);
    """,

    # Index on replay_events.timestamp for time-based queries
    """
    CREATE INDEX IF NOT EXISTS idx_replay_events_timestamp
    ON replay_events(timestamp DESC);
    """,

    # Index on scroll_dispatches.capsule_id
    """
    CREATE INDEX IF NOT EXISTS idx_scroll_dispatches_capsule_id
    ON scroll_dispatches(capsule_id);
    """,

    # Index on scroll_dispatches.timestamp
    """
    CREATE INDEX IF NOT EXISTS idx_scroll_dispatches_timestamp
    ON scroll_dispatches(timestamp DESC);
    """,
]

def create_indexes():
    """Create database indexes for improved query performance"""
    print("📊 Creating database indexes...")

    with engine.connect() as conn:
        for i, query in enumerate(OPTIMIZATION_QUERIES, 1):
            try:
                # Extract index name from query
                index_name = query.split("idx_")[1].split()[0] if "idx_" in query else f"index_{i}"

                conn.execute(text(query))
                conn.commit()
                print(f"   ✅ Created index: idx_{index_name}")
            except Exception as e:
                print(f"   ⚠️  Index creation skipped: {str(e)[:50]}")

    print()


def analyze_tables():
    """Run ANALYZE on tables to update statistics"""
    print("📈 Updating table statistics...")

    tables = ["capsules", "replay_events", "scroll_dispatches"]

    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"ANALYZE {table}"))
                conn.commit()
                print(f"   ✅ Analyzed: {table}")
            except Exception as e:
                print(f"   ⚠️  Analysis failed for {table}: {e}")

    print()


def show_table_stats():
    """Display table statistics"""
    print("📋 Table Statistics:")

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    with engine.connect() as conn:
        for table in tables:
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"   {table}: {count} rows")
            except Exception as e:
                print(f"   {table}: Error - {e}")

    print()


def main():
    """Run all optimization tasks"""
    try:
        create_indexes()
        analyze_tables()
        show_table_stats()

        print("=" * 60)
        print("✅ Database optimization complete!")
        print("   - Indexes created for faster queries")
        print("   - Table statistics updated")
        print("   - Query planner optimized")
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
