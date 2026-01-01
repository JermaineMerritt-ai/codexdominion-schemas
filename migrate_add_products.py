"""
🔥 DATABASE MIGRATION - ADD PRODUCTS TABLE 🔥
==============================================
Adds products table to support digital marketplace

Run: python migrate_add_products.py
"""

import sys
from sqlalchemy import create_engine, inspect, text, Column, String, Text, Float, Boolean, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker
from config import Config

def migrate():
    """Add products table to database"""
    print("🔥 CODEX DOMINION - PRODUCTS TABLE MIGRATION")
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
    
    # Check if products table already exists
    existing_tables = inspector.get_table_names()
    print(f"1. Checking existing tables...")
    print(f"   Found tables: {', '.join(existing_tables)}")
    print()
    
    if 'products' in existing_tables:
        print("⚠️  Products table already exists!")
        response = input("Do you want to recreate it? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return False
        
        # Drop existing table
        print("🗑️  Dropping existing products table...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS products"))
            conn.commit()
        print("   ✅ Table dropped")
        print()
    
    # Create products table
    print("2. Creating products table...")
    
    # SQL for SQLite
    if database_url.startswith('sqlite'):
        create_table_sql = """
        CREATE TABLE products (
            id VARCHAR PRIMARY KEY,
            title VARCHAR NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR NOT NULL,
            price FLOAT NOT NULL,
            file_url VARCHAR NOT NULL,
            creator_id VARCHAR NOT NULL,
            is_active INTEGER DEFAULT 1,
            downloads_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id)
        )
        """
    else:
        # PostgreSQL
        create_table_sql = """
        CREATE TABLE products (
            id VARCHAR PRIMARY KEY,
            title VARCHAR NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR NOT NULL,
            price FLOAT NOT NULL,
            file_url VARCHAR NOT NULL,
            creator_id VARCHAR NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            downloads_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id)
        )
        """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
    
    print("   ✅ Products table created")
    print()
    
    # Verify table structure
    print("3. Verifying table structure...")
    inspector = inspect(engine)
    columns = inspector.get_columns('products')
    
    print("   New Columns:")
    for col in columns:
        print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
    
    print()
    print("✅ Migration completed successfully!")
    print()
    print("📊 Products Table Schema:")
    print("   - id: VARCHAR (primary key) - Unique product identifier")
    print("   - title: VARCHAR - Product title")
    print("   - description: TEXT - Product description")
    print("   - category: VARCHAR - Product category (ebook, template, course, preset, pack, other)")
    print("   - price: FLOAT - Product price")
    print("   - file_url: VARCHAR - URL to product file")
    print("   - creator_id: VARCHAR - ID of user who created product")
    print("   - is_active: BOOLEAN - Whether product is active")
    print("   - downloads_count: INTEGER - Number of downloads")
    print("   - created_at: DATETIME - Creation timestamp")
    print("   - updated_at: DATETIME - Last update timestamp")
    print()
    
    return True


def rollback():
    """Remove products table"""
    print("🔥 CODEX DOMINION - ROLLBACK PRODUCTS TABLE")
    print("=" * 50)
    print()
    
    database_url = Config.get_database_url()
    print(f"🔄 Rolling back migration...")
    print(f"Database: {database_url}")
    print()
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS products"))
        conn.commit()
    
    print("✅ Products table dropped successfully")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback()
    else:
        migrate()
