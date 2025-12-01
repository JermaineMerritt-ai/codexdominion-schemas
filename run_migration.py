"""
Database Migration Runner for Codex Dominion Trading Platform
Handles PostgreSQL database setup and migrations
"""

import asyncio
import logging
import os
from pathlib import Path

import psycopg2
import psycopg2.extras

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "codex_dominion"),
    "user": os.getenv("DB_USER", "codex_admin"),
    "password": os.getenv("DB_PASSWORD", "your_secure_password"),
}


class DatabaseMigrator:
    """Handle database migrations and setup"""

    def __init__(self):
        self.connection = None

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            # Try to connect to the specific database
            self.connection = psycopg2.connect(**DB_CONFIG)
            logger.info(f"✅ Connected to database: {DB_CONFIG['database']}")
            return True
        except psycopg2.OperationalError as e:
            if "does not exist" in str(e):
                # Database doesn't exist, connect to postgres to create it
                logger.info(
                    f"Database {DB_CONFIG['database']} doesn't exist, creating..."
                )
                self.create_database()
                return self.connect()
            else:
                logger.error(f"❌ Database connection failed: {e}")
                return False
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False

    def create_database(self):
        """Create the database if it doesn't exist"""
        try:
            # Connect to postgres database to create new database
            postgres_config = DB_CONFIG.copy()
            postgres_config["database"] = "postgres"

            conn = psycopg2.connect(**postgres_config)
            conn.autocommit = True  # Required for CREATE DATABASE
            cursor = conn.cursor()

            # Create database
            cursor.execute(f'CREATE DATABASE "{DB_CONFIG["database"]}"')
            logger.info(f"✅ Database {DB_CONFIG['database']} created successfully")

            cursor.close()
            conn.close()

        except psycopg2.errors.DuplicateDatabase:
            logger.info(f"Database {DB_CONFIG['database']} already exists")
        except Exception as e:
            logger.error(f"❌ Failed to create database: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("🔌 Database connection closed")

    async def run_migration(self, sql_file_path: str):
        """Run SQL migration from file"""
        try:
            # Read SQL file
            with open(sql_file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()

            # Split by semicolon and execute each statement
            statements = [
                stmt.strip() for stmt in sql_content.split(";") if stmt.strip()
            ]

            logger.info(f"📄 Running migration: {sql_file_path}")
            logger.info(f"🔄 Executing {len(statements)} SQL statements...")

            for i, statement in enumerate(statements, 1):
                try:
                    # Skip comments and empty statements
                    if statement.startswith("--") or not statement.strip():
                        continue

                    await self.connection.execute(statement)
                    logger.debug(f"✅ Statement {i}/{len(statements)} executed")

                except Exception as e:
                    logger.error(f"❌ Error in statement {i}: {e}")
                    logger.error(f"Statement: {statement[:100]}...")
                    raise

            logger.info(f"✅ Migration completed successfully: {sql_file_path}")

        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise

    async def verify_tables(self):
        """Verify that all expected tables were created"""
        expected_tables = [
            "portfolios",
            "positions",
            "daily_picks",
            "affiliate_metrics",
            "amm_pools",
            "amm_events",
        ]

        logger.info("🔍 Verifying database tables...")

        for table in expected_tables:
            try:
                result = await self.connection.fetchval(
                    """
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_name = $1 AND table_schema = 'public'
                """,
                    table,
                )

                if result > 0:
                    logger.info(f"✅ Table '{table}' exists")

                    # Get row count
                    count = await self.connection.fetchval(
                        f"SELECT COUNT(*) FROM {table}"
                    )
                    logger.info(f"   📊 Contains {count} records")
                else:
                    logger.error(f"❌ Table '{table}' missing!")

            except Exception as e:
                logger.error(f"❌ Error checking table '{table}': {e}")

    async def verify_indexes(self):
        """Verify that indexes were created"""
        logger.info("🔍 Verifying database indexes...")

        result = await self.connection.fetch(
            """
            SELECT schemaname, tablename, indexname 
            FROM pg_indexes 
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname
        """
        )

        if result:
            logger.info(f"✅ Found {len(result)} indexes:")
            for row in result:
                logger.info(f"   📇 {row['tablename']}.{row['indexname']}")
        else:
            logger.warning("⚠️ No custom indexes found")

    async def get_database_stats(self):
        """Get database statistics"""
        logger.info("📊 Database Statistics:")

        # Table sizes
        stats = await self.connection.fetch(
            """
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """
        )

        for stat in stats:
            logger.info(f"   📊 {stat['tablename']}: {stat['size']}")

        # Total database size
        db_size = await self.connection.fetchval(
            """
            SELECT pg_size_pretty(pg_database_size($1))
        """,
            DB_CONFIG["database"],
        )

        logger.info(f"💾 Total database size: {db_size}")


async def main():
    """Main migration runner"""
    migrator = DatabaseMigrator()

    try:
        # Connect to database
        if not await migrator.connect():
            logger.error("Failed to connect to database")
            return False

        # Run migration
        migration_file = Path(__file__).parent / "database_migration.sql"
        if migration_file.exists():
            await migrator.run_migration(str(migration_file))
        else:
            logger.error(f"Migration file not found: {migration_file}")
            return False

        # Verify setup
        await migrator.verify_tables()
        await migrator.verify_indexes()
        await migrator.get_database_stats()

        logger.info("🎉 Database migration completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False

    finally:
        await migrator.disconnect()


def run_migration():
    """Sync wrapper for migration"""
    return asyncio.run(main())


if __name__ == "__main__":
    success = run_migration()
    exit(0 if success else 1)
