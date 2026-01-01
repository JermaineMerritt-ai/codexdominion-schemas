"""
🔥 DATABASE MIGRATION - ADD PRODUCT STATUS FIELD 🔥
====================================================
Adds status field to products table for publication workflow

Run: python migrate_add_product_status.py
"""

import sys
from sqlalchemy import create_engine, inspect, text
from config import Config

def migrate():
    """Add status field to products table"""
    print("🔥 CODEX DOMINION - PRODUCT STATUS MIGRATION")
    print("=" * 50)
    print()
    
    # Get database URL
    database_url = Config.get_database_url()
    print(f"🔄 Starting migration...")
    print(f"Database: {database_url}")
    print()
    
    # Create engine
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    # Check if products table exists
    existing_tables = inspector.get_table_names()
    if 'products' not in existing_tables:
        print("❌ Products table does not exist. Run migrate_add_products.py first.")
        return False
    
    print("1. Checking existing columns...")
    columns = inspector.get_columns('products')
    column_names = [col['name'] for col in columns]
    print(f"   Existing columns: {', '.join(column_names)}")
    print()
    
    if 'status' in column_names:
        print("⚠️  Status column already exists!")
        response = input("Do you want to recreate it? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return False
        
        # Drop existing column
        print("🗑️  Dropping existing status column...")
        if database_url.startswith('sqlite'):
            print("   ⚠️  SQLite doesn't support DROP COLUMN. Skipping...")
        else:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE products DROP COLUMN status"))
                conn.commit()
        print()
    
    # Add status column
    print("2. Adding status column...")
    
    if database_url.startswith('sqlite'):
        # SQLite
        add_column_sql = """
        ALTER TABLE products 
        ADD COLUMN status VARCHAR DEFAULT 'pending'
        """
    else:
        # PostgreSQL
        add_column_sql = """
        ALTER TABLE products 
        ADD COLUMN status VARCHAR DEFAULT 'pending'
        """
    
    with engine.connect() as conn:
        conn.execute(text(add_column_sql))
        conn.commit()
    
    print("   ✅ status column added")
    print()
    
    # Verify column
    print("3. Verifying migration...")
    inspector = inspect(engine)
    columns = inspector.get_columns('products')
    
    status_col = next((col for col in columns if col['name'] == 'status'), None)
    if status_col:
        print(f"   New Column:")
        print(f"   - status: {status_col['type']} (nullable: {status_col['nullable']}, default: 'pending')")
    
    print()
    print("✅ Migration completed successfully!")
    print()
    print("📊 Status Field Details:")
    print("   - status: VARCHAR - Product publication status")
    print("   - Valid values: 'published' | 'pending'")
    print("   - Default: 'pending'")
    print()
    
    return True


def rollback():
    """Remove status field from products table"""
    print("🔥 CODEX DOMINION - ROLLBACK PRODUCT STATUS")
    print("=" * 50)
    print()
    
    database_url = Config.get_database_url()
    print(f"🔄 Rolling back migration...")
    print(f"Database: {database_url}")
    print()
    
    if database_url.startswith('sqlite'):
        print("⚠️  SQLite doesn't support DROP COLUMN easily.")
        print("   You'll need to manually recreate the table without status column.")
        return False
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE products DROP COLUMN IF EXISTS status"))
        conn.commit()
    
    print("✅ Status column dropped successfully")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback()
    else:
        migrate()
