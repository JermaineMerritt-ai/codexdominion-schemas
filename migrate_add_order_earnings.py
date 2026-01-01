"""
🔥 DATABASE MIGRATION - ADD ORDER EARNINGS TRACKING 🔥
========================================================
Adds order ID and earnings split fields to purchases table

Run: python migrate_add_order_earnings.py
"""

import sys
from sqlalchemy import create_engine, inspect, text
from config import Config

def migrate():
    """Add order earnings fields to purchases table"""
    print("🔥 CODEX DOMINION - ORDER EARNINGS MIGRATION")
    print("=" * 50)
    print()
    
    database_url = Config.get_database_url()
    print(f"🔄 Starting migration...")
    print(f"Database: {database_url}")
    print()
    
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    # Check if purchases table exists
    existing_tables = inspector.get_table_names()
    if 'purchases' not in existing_tables:
        print("❌ Purchases table does not exist. Run migrate_add_purchases.py first.")
        return False
    
    print("1. Checking existing columns...")
    columns = inspector.get_columns('purchases')
    column_names = [col['name'] for col in columns]
    print(f"   Current columns: {', '.join(column_names)}")
    print()
    
    # Check if columns already exist
    new_columns = ['order_id', 'creator_earning', 'referrer_earning']
    existing_new_cols = [col for col in new_columns if col in column_names]
    
    if existing_new_cols:
        print(f"⚠️  Columns already exist: {', '.join(existing_new_cols)}")
        response = input("Do you want to continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return False
        print()
    
    print("2. Adding new columns...")
    
    with engine.connect() as conn:
        # Add order_id column (nullable for backward compatibility)
        if 'order_id' not in column_names:
            conn.execute(text("""
                ALTER TABLE purchases ADD COLUMN order_id VARCHAR
            """))
            print("   ✅ Added order_id column")
        
        # Add creator_earning column (defaults to full amount for existing records)
        if 'creator_earning' not in column_names:
            conn.execute(text("""
                ALTER TABLE purchases ADD COLUMN creator_earning FLOAT DEFAULT 0
            """))
            print("   ✅ Added creator_earning column")
        
        # Add referrer_earning column (defaults to 0 for existing records)
        if 'referrer_earning' not in column_names:
            conn.execute(text("""
                ALTER TABLE purchases ADD COLUMN referrer_earning FLOAT DEFAULT 0
            """))
            print("   ✅ Added referrer_earning column")
        
        # Update existing records to set creator_earning = amount (for records without earnings)
        conn.execute(text("""
            UPDATE purchases 
            SET creator_earning = amount 
            WHERE creator_earning = 0 OR creator_earning IS NULL
        """))
        print("   ✅ Updated existing records with earnings")
        
        # Add index on order_id for fast lookups
        if 'order_id' not in column_names:
            conn.execute(text("""
                CREATE INDEX idx_purchases_order_id ON purchases(order_id)
            """))
            print("   ✅ Created index on order_id")
        
        conn.commit()
    
    print()
    print("3. Verifying updated table structure...")
    inspector = inspect(engine)
    columns = inspector.get_columns('purchases')
    
    print("   Updated Columns:")
    for col in columns:
        print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
    
    print()
    print("✅ Migration completed successfully!")
    print()
    print("📊 New Fields:")
    print("   - order_id: VARCHAR - External order/transaction ID")
    print("   - creator_earning: FLOAT - Amount earned by product creator")
    print("   - referrer_earning: FLOAT - Commission earned by referrer")
    print()
    print("💰 Revenue Split Calculation:")
    print("   - No referrer: creator_earning = 100% of amount")
    print("   - With referrer: creator_earning = 80%, referrer_earning = 20%")
    print("   - Configurable via commission rate")
    print()
    
    return True


def rollback():
    """Remove order earnings columns"""
    print("🔥 CODEX DOMINION - ROLLBACK ORDER EARNINGS")
    print("=" * 50)
    print()
    
    database_url = Config.get_database_url()
    print(f"🔄 Rolling back migration...")
    print(f"Database: {database_url}")
    print()
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # SQLite doesn't support DROP COLUMN easily, so we skip for SQLite
        if not database_url.startswith('sqlite'):
            conn.execute(text("ALTER TABLE purchases DROP COLUMN order_id"))
            conn.execute(text("ALTER TABLE purchases DROP COLUMN creator_earning"))
            conn.execute(text("ALTER TABLE purchases DROP COLUMN referrer_earning"))
            conn.commit()
            print("✅ Columns dropped successfully")
        else:
            print("⚠️  SQLite doesn't support DROP COLUMN easily")
            print("   To rollback, drop and recreate the purchases table")
    
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback()
    else:
        migrate()
