"""
🔥 DATABASE MIGRATION - ADD PURCHASES TRACKING 🔥
===================================================
Adds purchases table to track product sales and referrals

Run: python migrate_add_purchases.py
"""

import sys
from sqlalchemy import create_engine, inspect, text
from config import Config

def migrate():
    """Add purchases table to database"""
    print("🔥 CODEX DOMINION - PURCHASES MIGRATION")
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
    
    if 'purchases' in existing_tables:
        print("⚠️  Purchases table already exists!")
        response = input("Do you want to recreate it? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return False
        
        # Drop existing table
        print("🗑️  Dropping existing purchases table...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS purchases"))
            conn.commit()
        print("   ✅ Table dropped")
        print()
    
    # Create purchases table
    print("2. Creating purchases table...")
    
    # SQL for SQLite
    if database_url.startswith('sqlite'):
        create_table_sql = """
        CREATE TABLE purchases (
            id VARCHAR PRIMARY KEY,
            product_id VARCHAR NOT NULL,
            buyer_id VARCHAR,
            referrer_id VARCHAR,
            payment_method VARCHAR NOT NULL,
            amount FLOAT NOT NULL,
            status VARCHAR DEFAULT 'completed',
            purchased_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (buyer_id) REFERENCES users(id),
            FOREIGN KEY (referrer_id) REFERENCES users(id)
        )
        """
        
        # Create indexes
        create_index_sql = """
        CREATE INDEX idx_purchases_product_id ON purchases(product_id);
        CREATE INDEX idx_purchases_buyer_id ON purchases(buyer_id);
        CREATE INDEX idx_purchases_referrer_id ON purchases(referrer_id);
        CREATE INDEX idx_purchases_status ON purchases(status);
        CREATE INDEX idx_purchases_purchased_at ON purchases(purchased_at);
        """
    else:
        # PostgreSQL
        create_table_sql = """
        CREATE TABLE purchases (
            id VARCHAR PRIMARY KEY,
            product_id VARCHAR NOT NULL,
            buyer_id VARCHAR,
            referrer_id VARCHAR,
            payment_method VARCHAR NOT NULL,
            amount FLOAT NOT NULL,
            status VARCHAR DEFAULT 'completed',
            purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (buyer_id) REFERENCES users(id),
            FOREIGN KEY (referrer_id) REFERENCES users(id)
        )
        """
        
        create_index_sql = """
        CREATE INDEX idx_purchases_product_id ON purchases(product_id);
        CREATE INDEX idx_purchases_buyer_id ON purchases(buyer_id);
        CREATE INDEX idx_purchases_referrer_id ON purchases(referrer_id);
        CREATE INDEX idx_purchases_status ON purchases(status);
        CREATE INDEX idx_purchases_purchased_at ON purchases(purchased_at);
        """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        
        # Create indexes
        for index_sql in create_index_sql.strip().split(';'):
            if index_sql.strip():
                conn.execute(text(index_sql))
        
        conn.commit()
    
    print("   ✅ Purchases table created")
    print("   ✅ Indexes created for performance")
    print()
    
    # Verify table structure
    print("3. Verifying table structure...")
    inspector = inspect(engine)
    columns = inspector.get_columns('purchases')
    
    print("   New Columns:")
    for col in columns:
        print(f"   - {col['name']}: {col['type']} (nullable: {col['nullable']})")
    
    print()
    print("✅ Migration completed successfully!")
    print()
    print("📊 Purchases Table Schema:")
    print("   - id: VARCHAR (primary key) - Unique purchase identifier")
    print("   - product_id: VARCHAR - ID of product purchased")
    print("   - buyer_id: VARCHAR (nullable) - ID of buyer (can be guest)")
    print("   - referrer_id: VARCHAR (nullable) - ID of referrer for affiliate tracking")
    print("   - payment_method: VARCHAR - Payment method used")
    print("   - amount: FLOAT - Purchase amount")
    print("   - status: VARCHAR - Purchase status (completed, pending, refunded)")
    print("   - purchased_at: DATETIME - When purchase was made")
    print()
    print("📈 Indexes created:")
    print("   - idx_purchases_product_id - Fast lookup by product")
    print("   - idx_purchases_buyer_id - Fast lookup by buyer")
    print("   - idx_purchases_referrer_id - Fast affiliate tracking")
    print("   - idx_purchases_status - Fast status filtering")
    print("   - idx_purchases_purchased_at - Fast date range queries")
    print()
    
    return True


def rollback():
    """Remove purchases table"""
    print("🔥 CODEX DOMINION - ROLLBACK PURCHASES")
    print("=" * 50)
    print()
    
    database_url = Config.get_database_url()
    print(f"🔄 Rolling back migration...")
    print(f"Database: {database_url}")
    print()
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS purchases"))
        conn.commit()
    
    print("✅ Purchases table dropped successfully")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback()
    else:
        migrate()
