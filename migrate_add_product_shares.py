"""
🔥 DATABASE MIGRATION - ADD PRODUCT SHARES TRACKING 🔥
=======================================================
Adds product_shares table to track social media sharing

Run: python migrate_add_product_shares.py
"""

import sys
from sqlalchemy import create_engine, inspect, text
from config import Config

def migrate():
    """Add product_shares table to database"""
    print("🔥 CODEX DOMINION - PRODUCT SHARES MIGRATION")
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
    
    print("1. Checking existing tables...")
    print(f"   Found tables: {len(existing_tables)} tables")
    print()
    
    if 'product_shares' in existing_tables:
        print("⚠️  Product shares table already exists!")
        response = input("Do you want to recreate it? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return False
        
        # Drop existing table
        print("🗑️  Dropping existing product_shares table...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS product_shares"))
            conn.commit()
        print("   ✅ Table dropped")
        print()
    
    # Create product_shares table
    print("2. Creating product_shares table...")
    
    # SQL for SQLite
    if database_url.startswith('sqlite'):
        create_table_sql = """
        CREATE TABLE product_shares (
            id VARCHAR PRIMARY KEY,
            user_id VARCHAR NOT NULL,
            product_id VARCHAR NOT NULL,
            channel VARCHAR NOT NULL,
            shared_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
        """
        
        # Create index for faster queries
        create_index_sql = """
        CREATE INDEX idx_product_shares_product_id ON product_shares(product_id);
        CREATE INDEX idx_product_shares_user_id ON product_shares(user_id);
        CREATE INDEX idx_product_shares_channel ON product_shares(channel);
        """
    else:
        # PostgreSQL
        create_table_sql = """
        CREATE TABLE product_shares (
            id VARCHAR PRIMARY KEY,
            user_id VARCHAR NOT NULL,
            product_id VARCHAR NOT NULL,
            channel VARCHAR NOT NULL,
            shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
        """
        
        create_index_sql = """
        CREATE INDEX idx_product_shares_product_id ON product_shares(product_id);
        CREATE INDEX idx_product_shares_user_id ON product_shares(user_id);
        CREATE INDEX idx_product_shares_channel ON product_shares(channel);
        """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        
        # Create indexes
        for index_sql in create_index_sql.strip().split(';'):
            if index_sql.strip():
                conn.execute(text(index_sql))
        
        conn.commit()
    
    print("   ✅ Product shares table created")
    print("   ✅ Indexes created for performance")
    print()
    
    # Verify table structure
    print("3. Verifying table structure...")
    inspector = inspect(engine)
    columns = inspector.get_columns('product_shares')
    
    print("   New Columns:")
    for col in columns:
        print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
    
    print()
    print("✅ Migration completed successfully!")
    print()
    print("📊 Product Shares Table Schema:")
    print("   - id: VARCHAR (primary key) - Unique share record identifier")
    print("   - user_id: VARCHAR - ID of user who shared")
    print("   - product_id: VARCHAR - ID of product shared")
    print("   - channel: VARCHAR - Social channel (whatsapp, instagram, tiktok, other)")
    print("   - shared_at: DATETIME - When product was shared")
    print()
    print("📈 Indexes created:")
    print("   - idx_product_shares_product_id - Fast lookup by product")
    print("   - idx_product_shares_user_id - Fast lookup by user")
    print("   - idx_product_shares_channel - Fast analytics by channel")
    print()
    
    return True


def rollback():
    """Remove product_shares table"""
    print("🔥 CODEX DOMINION - ROLLBACK PRODUCT SHARES")
    print("=" * 50)
    print()
    
    database_url = Config.get_database_url()
    print(f"🔄 Rolling back migration...")
    print(f"Database: {database_url}")
    print()
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS product_shares"))
        conn.commit()
    
    print("✅ Product shares table dropped successfully")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback()
    else:
        migrate()
