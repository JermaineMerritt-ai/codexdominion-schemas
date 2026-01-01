"""
Database Migration: Add User Onboarding Fields
===============================================
Adds user_type and onboarding_completed fields to users table

Run this script to update your database schema:
    python migrate_add_onboarding.py
"""

from sqlalchemy import create_engine, text
from config import Config
import sys

def migrate():
    """Add onboarding fields to users table"""
    
    database_url = Config.get_database_url()
    engine = create_engine(database_url)
    
    print("🔄 Starting database migration...")
    print(f"Database: {database_url.split('@')[-1] if '@' in database_url else database_url}")
    
    try:
        with engine.connect() as conn:
            # Check if columns already exist
            print("\n1. Checking existing columns...")
            
            # For PostgreSQL
            if 'postgresql' in database_url:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name IN ('user_type', 'onboarding_completed')
                """))
                existing_columns = [row[0] for row in result]
            
            # For SQLite
            else:
                result = conn.execute(text("PRAGMA table_info(users)"))
                existing_columns = [row[1] for row in result if row[1] in ['user_type', 'onboarding_completed']]
            
            print(f"   Existing onboarding columns: {existing_columns if existing_columns else 'None'}")
            
            # Add user_type column if it doesn't exist
            if 'user_type' not in existing_columns:
                print("\n2. Adding user_type column...")
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN user_type VARCHAR(20)
                """))
                conn.commit()
                print("   ✅ user_type column added")
            else:
                print("\n2. user_type column already exists, skipping...")
            
            # Add onboarding_completed column if it doesn't exist
            if 'onboarding_completed' not in existing_columns:
                print("\n3. Adding onboarding_completed column...")
                
                if 'postgresql' in database_url:
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE
                    """))
                else:  # SQLite
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN onboarding_completed INTEGER DEFAULT 0
                    """))
                
                conn.commit()
                print("   ✅ onboarding_completed column added")
            else:
                print("\n3. onboarding_completed column already exists, skipping...")
            
            # Verify migration
            print("\n4. Verifying migration...")
            
            if 'postgresql' in database_url:
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name IN ('user_type', 'onboarding_completed')
                    ORDER BY column_name
                """))
                
                print("\n   New Columns:")
                for row in result:
                    print(f"   - {row[0]}: {row[1]} (nullable: {row[2]})")
            
            else:  # SQLite
                result = conn.execute(text("PRAGMA table_info(users)"))
                print("\n   New Columns:")
                for row in result:
                    if row[1] in ['user_type', 'onboarding_completed']:
                        print(f"   - {row[1]}: {row[2]} (nullable: {row[3] == 0})")
            
            print("\n✅ Migration completed successfully!")
            print("\n📊 Summary:")
            print("   - user_type: VARCHAR(20) - stores 'creator', 'youth', or 'both'")
            print("   - onboarding_completed: BOOLEAN - tracks if user completed onboarding")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        print("\nPossible causes:")
        print("  1. Database connection error")
        print("  2. Insufficient permissions")
        print("  3. Table 'users' doesn't exist")
        print("\nTroubleshooting:")
        print("  - Check DATABASE_URL in .env or config.py")
        print("  - Ensure database is running")
        print("  - Run: python -c 'from models import Base; from db import engine; Base.metadata.create_all(bind=engine)'")
        sys.exit(1)
    
    finally:
        engine.dispose()

def rollback():
    """Remove onboarding fields from users table"""
    
    database_url = Config.get_database_url()
    engine = create_engine(database_url)
    
    print("🔄 Rolling back migration...")
    
    try:
        with engine.connect() as conn:
            print("\n1. Dropping user_type column...")
            try:
                conn.execute(text("ALTER TABLE users DROP COLUMN user_type"))
                conn.commit()
                print("   ✅ user_type column dropped")
            except Exception as e:
                print(f"   ⚠️  Could not drop user_type: {str(e)}")
            
            print("\n2. Dropping onboarding_completed column...")
            try:
                conn.execute(text("ALTER TABLE users DROP COLUMN onboarding_completed"))
                conn.commit()
                print("   ✅ onboarding_completed column dropped")
            except Exception as e:
                print(f"   ⚠️  Could not drop onboarding_completed: {str(e)}")
            
            print("\n✅ Rollback completed!")
    
    except Exception as e:
        print(f"\n❌ Rollback failed: {str(e)}")
        sys.exit(1)
    
    finally:
        engine.dispose()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate database for user onboarding")
    parser.add_argument('--rollback', action='store_true', help='Rollback migration')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔥 CODEX DOMINION - DATABASE MIGRATION")
    print("=" * 60)
    
    if args.rollback:
        print("\n⚠️  WARNING: This will remove onboarding columns!")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() == 'yes':
            rollback()
        else:
            print("Rollback cancelled.")
    else:
        migrate()
    
    print("\n" + "=" * 60)
