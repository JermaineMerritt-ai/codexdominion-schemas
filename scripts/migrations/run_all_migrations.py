"""
Master migration runner - Executes all JSON → Postgres migrations in correct order
Run this script to migrate all data: councils → agents → workflows
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import individual migration modules
from scripts.migrations.migrate_councils_from_json import migrate_councils
from scripts.migrations.migrate_agents_from_json import migrate_agents
from scripts.migrations.migrate_workflows_from_json import migrate_workflows


def run_all_migrations():
    """Run all migrations in correct order"""
    print("\n" + "=" * 70)
    print("🔥 CODEXDOMINION JSON → POSTGRES MIGRATION SUITE 👑")
    print("=" * 70 + "\n")
    
    try:
        # Step 1: Migrate councils (no dependencies)
        print("Step 1/3: Migrating councils...")
        migrate_councils()
        print("✅ Councils migration complete\n")
        
        # Step 2: Migrate agents (no dependencies on councils yet)
        print("Step 2/3: Migrating agents...")
        migrate_agents()
        print("✅ Agents migration complete\n")
        
        # Step 3: Migrate workflows (depends on agents and councils)
        print("Step 3/3: Migrating workflows...")
        migrate_workflows()
        print("✅ Workflows migration complete\n")
        
        print("=" * 70)
        print("🎉 ALL MIGRATIONS COMPLETE!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Verify data in Postgres: psql -U postgres -d codexdominion")
        print("2. Update Flask endpoints to read from Postgres")
        print("3. Test frontend with Postgres backend")
        print("4. Move JSON files to backups/ directory")
        print("\n🔥 The Data Burns Sovereign and Eternal! 👑\n")
        
    except Exception as e:
        print(f"\n❌ Migration suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_migrations()
