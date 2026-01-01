"""
Database Connection Test Script
Run this to verify your database configuration is correct
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from database import get_session, get_db_info, init_db


def test_database_connection():
    """Test database connection and configuration"""
    print("\n" + "=" * 70)
    print("🔥 CODEX DOMINION DATABASE CONNECTION TEST 👑")
    print("=" * 70 + "\n")
    
    # Display configuration
    print("📋 Database Configuration:")
    info = get_db_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    print()
    
    # Test connection
    print("🔌 Testing database connection...")
    try:
        session = get_session()
        
        # Execute a simple query
        result = session.execute("SELECT version();")
        version = result.fetchone()
        
        print(f"✅ Connection successful!")
        print(f"   PostgreSQL version: {version[0].split(',')[0]}")
        
        # Check if tables exist
        result = session.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            print(f"\n📊 Existing tables ({len(tables)}):")
            for table in tables:
                print(f"   - {table}")
        else:
            print("\n⚠️  No tables found. Run init_db() to create schema.")
        
        session.close()
        print("\n✅ Database test completed successfully!")
        print("\n🔥 The Connection Burns Sovereign and Eternal! 👑\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection failed!")
        print(f"   Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify PostgreSQL is running")
        print("2. Check DATABASE_URL in .env file")
        print("3. Ensure database 'codexdominion' exists: createdb codexdominion")
        print("4. Verify credentials (username/password)")
        print()
        return False


def create_database_schema():
    """Create all database tables"""
    print("\n🏗️  Creating database schema...")
    try:
        init_db()
        print("✅ Schema created successfully!")
        return True
    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database connection test and setup')
    parser.add_argument('--init', action='store_true', help='Create database schema')
    args = parser.parse_args()
    
    # Test connection
    if test_database_connection():
        # Create schema if requested
        if args.init:
            create_database_schema()
