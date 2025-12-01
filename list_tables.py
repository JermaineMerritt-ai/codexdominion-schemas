#!/usr/bin/env python3
"""
Query Codex Dominion database to show table structure (equivalent to \dt in psql)
"""
import sqlalchemy
from google.cloud.sql.connector import Connector


def list_tables():
    """List all tables in the database like \dt command"""

    # Database connection details
    instance_connection_name = "codex-dominion-prod:us-central1:codex-ledger"
    db_user = "codex_user"
    db_pass = "codex_pass"
    db_name = "codex"

    print("🔗 Connecting to Cloud SQL database...")

    # Initialize Connector object
    connector = Connector()

    # Function to return the database connection
    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    # Create connection pool
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    try:
        with engine.connect() as connection:
            print("✅ Connected to Cloud SQL successfully!")

            # Query to list all tables (equivalent to \dt)
            tables_query = """
            SELECT 
                schemaname as "Schema",
                tablename as "Name", 
                tableowner as "Owner"
            FROM pg_tables 
            WHERE schemaname = 'public' 
            ORDER BY tablename;
            """

            print("\n📋 Database Tables (\\dt equivalent):")
            print("=" * 60)
            result = connection.execute(sqlalchemy.text(tables_query))
            tables = result.fetchall()

            if tables:
                print(f"{'Schema':<10} | {'Name':<20} | {'Owner':<15}")
                print("-" * 60)
                for row in tables:
                    schema, name, owner = row
                    print(f"{schema:<10} | {name:<20} | {owner:<15}")
            else:
                print("No tables found.")

            # Get table descriptions
            print(f"\n🗄️ Table Details:")
            print("=" * 60)

            for row in tables:
                schema, table_name, owner = row

                print(f"\n📊 Table: {table_name}")

                # Get column information
                columns_query = """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
                """

                col_result = connection.execute(
                    sqlalchemy.text(columns_query), (table_name,)
                )
                columns = col_result.fetchall()

                print(f"   Columns ({len(columns)} total):")
                for col in columns:
                    col_name, data_type, nullable, default = col
                    null_info = "NULL" if nullable == "YES" else "NOT NULL"
                    default_info = f"DEFAULT {default}" if default else ""
                    print(
                        f"     • {col_name:<20} {data_type:<15} {null_info:<8} {default_info}"
                    )

                # Get indexes
                indexes_query = """
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = %s AND schemaname = 'public';
                """

                idx_result = connection.execute(
                    sqlalchemy.text(indexes_query), (table_name,)
                )
                indexes = idx_result.fetchall()

                if indexes:
                    print(f"   Indexes ({len(indexes)} total):")
                    for idx in indexes:
                        idx_name, idx_def = idx
                        print(f"     • {idx_name}")

            # Show row counts
            print(f"\n📈 Table Row Counts:")
            print("=" * 40)
            for row in tables:
                schema, table_name, owner = row
                count_result = connection.execute(
                    sqlalchemy.text(f"SELECT COUNT(*) FROM {table_name}")
                )
                count = count_result.scalar()
                print(f"   {table_name:<20}: {count:>8} rows")

            print(f"\n🎯 Database Summary:")
            print(f"   📍 Instance: {instance_connection_name}")
            print(f"   🗄️ Database: {db_name}")
            print(f"   📋 Total Tables: {len(tables)}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        connector.close()

    return True


if __name__ == "__main__":
    list_tables()
