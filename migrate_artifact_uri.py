#!/usr/bin/env python3
"""
Database migration: Add artifact_uri column to capsule_runs table
"""
import sqlalchemy
from google.cloud.sql.connector import Connector


def run_migration():
    """Add artifact_uri column to capsule_runs table"""

    # Database connection details
    instance_connection_name = "codex-dominion-prod:us-central1:codex-ledger"
    db_user = "codex_user"
    db_pass = "codex_pass"
    db_name = "codex"

    print("🔗 Connecting to Cloud SQL database...")

    # Initialize Connector object
    connector = Connector()

    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)

    try:
        with engine.connect() as connection:
            print("✅ Connected to Cloud SQL successfully!")

            # Check if column already exists
            check_column_sql = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'capsule_runs' 
            AND column_name = 'artifact_uri' 
            AND table_schema = 'public';
            """

            result = connection.execute(sqlalchemy.text(check_column_sql))
            existing_column = result.fetchone()

            if existing_column:
                print("⚠️ Column 'artifact_uri' already exists in capsule_runs table")
                print("✅ Migration already applied - no action needed")
            else:
                # Add the column
                migration_sql = """
                ALTER TABLE capsule_runs 
                ADD COLUMN artifact_uri TEXT;
                """

                print("📋 Adding artifact_uri column to capsule_runs table...")
                connection.execute(sqlalchemy.text(migration_sql))
                connection.commit()
                print("✅ Column added successfully!")

            # Verify the column structure
            print("\n🔍 Verifying capsule_runs table structure:")
            print("=" * 60)

            structure_sql = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'capsule_runs' AND table_schema = 'public'
            ORDER BY ordinal_position;
            """

            result = connection.execute(sqlalchemy.text(structure_sql))
            columns = result.fetchall()

            for col_name, data_type, nullable, default in columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                default_str = f" DEFAULT {default}" if default else ""
                status = "🆕" if col_name == "artifact_uri" else "  "
                print(
                    f"{status} {col_name:<15} {data_type:<20} {null_str}{default_str}"
                )

            print(f"\n🎯 Migration Summary:")
            print(f"   📊 Table: capsule_runs")
            print(f"   📋 Total Columns: {len(columns)}")
            print(f"   🆕 Added: artifact_uri (TEXT, NULL)")
            print(
                f"   📍 Purpose: Store Cloud Storage paths to JSON/Markdown artifacts"
            )

            print(f"\n🏆 Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    finally:
        connector.close()

    return True


if __name__ == "__main__":
    run_migration()
