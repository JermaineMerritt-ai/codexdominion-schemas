#!/usr/bin/env python3
"""
Simple database table listing for Codex Dominion
"""
import sqlalchemy
from google.cloud.sql.connector import Connector


def show_database_info():
    """Show database tables and basic info"""

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

            # List tables
            print("\n📋 Database Tables:")
            print("=" * 50)
            result = connection.execute(
                sqlalchemy.text(
                    """
                SELECT tablename, tableowner 
                FROM pg_tables 
                WHERE schemaname = 'public' 
                ORDER BY tablename
            """
                )
            )

            tables = result.fetchall()
            for table_name, owner in tables:
                print(f"  📊 {table_name:<20} (owner: {owner})")

            # Show capsules table structure
            print("\n🗄️ Capsules Table Structure:")
            print("=" * 60)
            result = connection.execute(
                sqlalchemy.text(
                    """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'capsules' AND table_schema = 'public'
                ORDER BY ordinal_position
            """
                )
            )

            for col_name, data_type, nullable, default in result:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                default_str = f" DEFAULT {default}" if default else ""
                print(f"  • {col_name:<15} {data_type:<20} {null_str}{default_str}")

            # Show capsule_runs table structure
            print("\n🔄 Capsule Runs Table Structure:")
            print("=" * 60)
            result = connection.execute(
                sqlalchemy.text(
                    """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'capsule_runs' AND table_schema = 'public'
                ORDER BY ordinal_position
            """
                )
            )

            for col_name, data_type, nullable, default in result:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                default_str = f" DEFAULT {default}" if default else ""
                print(f"  • {col_name:<15} {data_type:<20} {null_str}{default_str}")

            # Show indexes
            print("\n🔍 Database Indexes:")
            print("=" * 50)
            result = connection.execute(
                sqlalchemy.text(
                    """
                SELECT indexname, tablename 
                FROM pg_indexes 
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname
            """
                )
            )

            for idx_name, table_name in result:
                print(f"  🔗 {idx_name} (on {table_name})")

            # Row counts
            print("\n📊 Data Summary:")
            print("=" * 40)

            result = connection.execute(
                sqlalchemy.text("SELECT COUNT(*) FROM capsules")
            )
            capsules_count = result.scalar()
            print(f"  📋 Capsules: {capsules_count} rows")

            result = connection.execute(
                sqlalchemy.text("SELECT COUNT(*) FROM capsule_runs")
            )
            runs_count = result.scalar()
            print(f"  🔄 Capsule Runs: {runs_count} rows")

            # Show sample data
            print("\n🎯 Sample Capsules:")
            print("=" * 80)
            result = connection.execute(
                sqlalchemy.text(
                    """
                SELECT slug, title, kind, mode, status, schedule 
                FROM capsules 
                ORDER BY created_at 
                LIMIT 5
            """
                )
            )

            for slug, title, kind, mode, status, schedule in result:
                schedule_info = schedule if schedule else "on-demand"
                print(f"  • {slug:<20} | {title:<30} | {kind:<10} | {schedule_info}")

            print(f"\n🏆 Database Status: OPERATIONAL")
            print(f"📍 Instance: {instance_connection_name}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        connector.close()

    return True


if __name__ == "__main__":
    show_database_info()
