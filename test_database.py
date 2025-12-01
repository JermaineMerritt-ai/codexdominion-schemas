#!/usr/bin/env python3
"""Database Connection Test Script"""
import os
import sqlite3
import sys


def test_database_connection():
    """Test SQLite database connection and basic operations"""
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")

        # Connect to database
        conn = sqlite3.connect("data/codex_empire.db")
        cursor = conn.cursor()

        # Create test table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS test_connection (
                id INTEGER PRIMARY KEY,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Insert test data
        cursor.execute(
            'INSERT OR REPLACE INTO test_connection (id, status) VALUES (1, "connected")'
        )

        # Verify connection
        result = cursor.execute(
            "SELECT status FROM test_connection WHERE id=1"
        ).fetchone()

        conn.commit()
        conn.close()

        if result and result[0] == "connected":
            print("✅ Database connection: SUCCESS")
            return True
        else:
            print("❌ Database connection: FAILED - No result")
            return False

    except Exception as e:
        print(f"❌ Database connection: ERROR - {str(e)}")
        return False


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
