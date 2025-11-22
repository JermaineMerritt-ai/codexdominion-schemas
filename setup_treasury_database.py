#!/usr/bin/env python3
"""
Codex Database Setup and Migration Script
========================================

Sets up PostgreSQL database for the Codex Treasury system.
Creates tables, indexes, and sample data for testing.
"""

import os
import sys
import json
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    PSYCOPG2_AVAILABLE = True
except ImportError:
    print("❌ psycopg2 not available. Install with:")
    print("   pip install psycopg2-binary")
    PSYCOPG2_AVAILABLE = False

class CodexDatabaseSetup:
    """Database setup and migration manager."""
    
    def __init__(self, config_path="treasury_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self):
        """Load database configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "database": {
                    "dbname": "codex",
                    "user": "codex_user",
                    "password": "codex_pass", 
                    "host": "localhost",
                    "port": 5432
                }
            }
    
    def create_database(self):
        """Create the Codex database if it doesn't exist."""
        if not PSYCOPG2_AVAILABLE:
            print("❌ PostgreSQL support not available")
            return False
            
        try:
            db_config = self.config["database"].copy()
            dbname = db_config.pop("dbname")
            
            # Connect to postgres database to create our database
            db_config["dbname"] = "postgres"
            
            print(f"🔗 Connecting to PostgreSQL server...")
            conn = psycopg2.connect(**db_config)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            cur = conn.cursor()
            
            # Check if database exists
            cur.execute("""
                SELECT 1 FROM pg_database 
                WHERE datname = %s
            """, (dbname,))
            
            if cur.fetchone():
                print(f"✅ Database '{dbname}' already exists")
            else:
                # Create database
                cur.execute(f'CREATE DATABASE "{dbname}"')
                print(f"✅ Database '{dbname}' created successfully")
            
            # Create user if not exists
            user = self.config["database"]["user"]
            password = self.config["database"]["password"]
            
            cur.execute("""
                SELECT 1 FROM pg_user 
                WHERE usename = %s
            """, (user,))
            
            if not cur.fetchone():
                cur.execute(f"""
                    CREATE USER "{user}" WITH PASSWORD '{password}'
                """)
                print(f"✅ User '{user}' created")
            
            # Grant privileges
            cur.execute(f'''
                GRANT ALL PRIVILEGES ON DATABASE "{dbname}" TO "{user}"
            ''')
            
            cur.close()
            conn.close()
            
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Database creation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def create_tables(self):
        """Create all necessary tables and indexes."""
        if not PSYCOPG2_AVAILABLE:
            print("❌ PostgreSQL support not available")
            return False
            
        try:
            print("🏗️  Creating database tables...")
            
            conn = psycopg2.connect(**self.config["database"])
            cur = conn.cursor()
            
            # Create transactions table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id VARCHAR(20) PRIMARY KEY,
                    stream VARCHAR(50) NOT NULL,
                    amount DECIMAL(15,2) NOT NULL,
                    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
                    source VARCHAR(200) NOT NULL,
                    status VARCHAR(50) NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                );
            """)
            
            # Create revenue streams summary table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS revenue_streams (
                    stream VARCHAR(50) PRIMARY KEY,
                    total_amount DECIMAL(15,2) NOT NULL DEFAULT 0,
                    transaction_count INTEGER NOT NULL DEFAULT 0,
                    first_transaction TIMESTAMP WITH TIME ZONE,
                    last_transaction TIMESTAMP WITH TIME ZONE,
                    status VARCHAR(20) NOT NULL DEFAULT 'active',
                    settings JSONB
                );
            """)
            
            # Create portfolios table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS portfolios (
                    id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    owner VARCHAR(100) NOT NULL,
                    risk_tier VARCHAR(20) NOT NULL DEFAULT 'moderate',
                    total_value DECIMAL(15,2) NOT NULL DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    settings JSONB
                );
            """)
            
            # Create positions table  
            cur.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    id VARCHAR(20) PRIMARY KEY,
                    portfolio_id VARCHAR(20) REFERENCES portfolios(id),
                    symbol VARCHAR(20) NOT NULL,
                    quantity DECIMAL(15,4) NOT NULL,
                    avg_price DECIMAL(15,2) NOT NULL,
                    current_value DECIMAL(15,2),
                    pnl DECIMAL(15,2),
                    pnl_percent DECIMAL(8,4),
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                );
            """)
            
            # Create AMM pools table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS amm_pools (
                    id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    token_pair VARCHAR(50) NOT NULL,
                    tvl DECIMAL(15,2) NOT NULL DEFAULT 0,
                    apr DECIMAL(8,4) NOT NULL DEFAULT 0,
                    fee_tier DECIMAL(6,4) NOT NULL DEFAULT 0.003,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                );
            """)
            
            # Create indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_transactions_stream ON transactions(stream);",
                "CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);",
                "CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);",
                "CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount);",
                "CREATE INDEX IF NOT EXISTS idx_positions_portfolio ON positions(portfolio_id);",
                "CREATE INDEX IF NOT EXISTS idx_positions_symbol ON positions(symbol);",
                "CREATE INDEX IF NOT EXISTS idx_amm_pools_pair ON amm_pools(token_pair);"
            ]
            
            for index_sql in indexes:
                cur.execute(index_sql)
            
            conn.commit()
            cur.close()
            conn.close()
            
            print("✅ Database tables created successfully")
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Table creation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def insert_sample_data(self):
        """Insert sample data for testing."""
        if not PSYCOPG2_AVAILABLE:
            print("❌ PostgreSQL support not available")
            return False
            
        try:
            print("📊 Inserting sample data...")
            
            conn = psycopg2.connect(**self.config["database"])
            cur = conn.cursor()
            
            # Sample revenue streams
            revenue_streams = [
                ('affiliate', 2500.00, 15, 'active'),
                ('stock', 15000.00, 25, 'active'), 
                ('amm', 8500.00, 20, 'active'),
                ('consulting', 12000.00, 8, 'active'),
                ('development', 25000.00, 5, 'active')
            ]
            
            for stream, total, count, status in revenue_streams:
                cur.execute("""
                    INSERT INTO revenue_streams (stream, total_amount, transaction_count, status)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (stream) DO UPDATE SET
                        total_amount = EXCLUDED.total_amount,
                        transaction_count = EXCLUDED.transaction_count
                """, (stream, total, count, status))
            
            # Sample portfolio
            cur.execute("""
                INSERT INTO portfolios (id, name, owner, risk_tier, total_value)
                VALUES ('PORT-001', 'Main Portfolio', 'Jermaine Merritt', 'aggressive', 50000.00)
                ON CONFLICT (id) DO NOTHING
            """)
            
            # Sample positions
            positions = [
                ('POS-001', 'PORT-001', 'AAPL', 100, 150.00, 18500.00, 3500.00, 23.33),
                ('POS-002', 'PORT-001', 'MSFT', 50, 300.00, 17500.00, 2500.00, 16.67),
                ('POS-003', 'PORT-001', 'GOOGL', 25, 140.00, 14000.00, 500.00, 3.70)
            ]
            
            for pos_id, port_id, symbol, qty, avg_price, curr_val, pnl, pnl_pct in positions:
                cur.execute("""
                    INSERT INTO positions (
                        id, portfolio_id, symbol, quantity, avg_price, 
                        current_value, pnl, pnl_percent
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (pos_id, port_id, symbol, qty, avg_price, curr_val, pnl, pnl_pct))
            
            # Sample AMM pools
            amm_pools = [
                ('POOL-001', 'ETH-USDC Pool', 'ETH/USDC', 1500000.00, 15.25, 0.003),
                ('POOL-002', 'BTC-ETH Pool', 'BTC/ETH', 2200000.00, 12.80, 0.003),
                ('POOL-003', 'USDC-DAI Pool', 'USDC/DAI', 800000.00, 8.50, 0.001)
            ]
            
            for pool_id, name, pair, tvl, apr, fee in amm_pools:
                cur.execute("""
                    INSERT INTO amm_pools (id, name, token_pair, tvl, apr, fee_tier)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (pool_id, name, pair, tvl, apr, fee))
            
            conn.commit()
            cur.close()
            conn.close()
            
            print("✅ Sample data inserted successfully")
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Sample data insertion failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def test_connection(self):
        """Test database connection and basic operations."""
        if not PSYCOPG2_AVAILABLE:
            print("❌ PostgreSQL support not available")
            return False
            
        try:
            print("🧪 Testing database connection...")
            
            conn = psycopg2.connect(**self.config["database"])
            cur = conn.cursor()
            
            # Test basic query
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"✅ PostgreSQL version: {version}")
            
            # Test transactions table
            cur.execute("SELECT COUNT(*) FROM transactions;")
            txn_count = cur.fetchone()[0]
            print(f"✅ Transactions in database: {txn_count}")
            
            # Test revenue streams
            cur.execute("SELECT COUNT(*) FROM revenue_streams;")
            stream_count = cur.fetchone()[0]
            print(f"✅ Revenue streams configured: {stream_count}")
            
            cur.close()
            conn.close()
            
            print("✅ Database connection test successful")
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Connection test failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

def main():
    """Main setup routine."""
    print("🏛️  Codex Database Setup")
    print("=" * 30)
    
    if not PSYCOPG2_AVAILABLE:
        print("\n❌ PostgreSQL support not available")
        print("To install PostgreSQL support:")
        print("  pip install psycopg2-binary")
        print("\nThe treasury system will work in JSON-only mode without PostgreSQL.")
        return
    
    setup = CodexDatabaseSetup()
    
    print("\n🔧 Setting up Codex Treasury database...")
    
    # Step 1: Create database and user
    if setup.create_database():
        print("✅ Database setup completed")
    else:
        print("❌ Database setup failed")
        return
    
    # Step 2: Create tables
    if setup.create_tables():
        print("✅ Table creation completed")
    else:
        print("❌ Table creation failed")
        return
    
    # Step 3: Insert sample data
    if setup.insert_sample_data():
        print("✅ Sample data insertion completed")
    else:
        print("❌ Sample data insertion failed")
    
    # Step 4: Test connection
    if setup.test_connection():
        print("✅ Database setup verification successful")
    else:
        print("❌ Database setup verification failed")
    
    print("\n🎉 Codex Treasury database is ready!")
    print("\nNext steps:")
    print("1. Run: python codex_treasury_database.py")
    print("2. Test transactions with the treasury system")
    print("3. View data in your PostgreSQL client")

if __name__ == "__main__":
    main()