#!/usr/bin/env python3
"""
Deploy Codex Dominion database schema to Cloud SQL
"""
import os
import psycopg2
from google.cloud.sql.connector import Connector

def create_connection():
    """Create a connection to Cloud SQL PostgreSQL instance"""
    connector = Connector()
    
    def getconn():
        conn = connector.connect(
            "codex-dominion-prod:us-central1:codex-ledger",
            "pg8000",
            user="codex_user",
            password="codex_pass",
            db="codex"
        )
        return conn
    
    return getconn()

def execute_schema():
    """Execute the database schema"""
    schema_sql = """
-- Codex Dominion Database Schema
-- Capsules system for operational sovereignty tracking

-- Capsules table: indexes ceremonial + technical capsules
CREATE TABLE IF NOT EXISTS capsules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,   -- e.g., 'festival', 'signals-daily'
    title VARCHAR(200) NOT NULL,
    kind VARCHAR(50) NOT NULL,           -- 'ceremony' | 'engine' | 'dispatch' | 'treasury' | 'education'
    mode VARCHAR(50) NOT NULL,           -- 'custodian' | 'heir' | 'customer' | 'public'
    version VARCHAR(50) DEFAULT '1.0.0',
    status VARCHAR(50) DEFAULT 'active', -- 'active' | 'archived'
    entrypoint TEXT,                     -- command, URL, or script path
    schedule VARCHAR(50),                -- cron-like '0 6 * * *' or null
    created_at TIMESTAMP DEFAULT NOW()
);

-- Capsule runs table: records executions, audits, lineage
CREATE TABLE IF NOT EXISTS capsule_runs (
    id SERIAL PRIMARY KEY,
    capsule_slug VARCHAR(120) NOT NULL REFERENCES capsules(slug) ON DELETE CASCADE,
    actor VARCHAR(120) NOT NULL,         -- 'custodian' | service account
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'success',-- 'success' | 'error'
    artifact_uri TEXT,                   -- Cloud Storage path or URL to snapshot/bulletin
    checksum TEXT                        -- integrity hash for idempotency
);

-- Indexes for fast lookup (only create if they don't exist)
CREATE INDEX IF NOT EXISTS idx_capsules_slug ON capsules(slug);
CREATE INDEX IF NOT EXISTS idx_runs_capsule_slug ON capsule_runs(capsule_slug);
CREATE INDEX IF NOT EXISTS idx_runs_started_at ON capsule_runs(started_at);
    """
    
    initial_data = """
-- Insert initial capsules for Codex Dominion system
INSERT INTO capsules (slug, title, kind, mode, entrypoint, schedule) VALUES
('signals-daily', 'Daily Signals Dispatch', 'engine', 'custodian', '/api/signals/daily', '0 6 * * *'),
('dawn-dispatch', 'Dawn Proclamation Capsule', 'dispatch', 'custodian', '/api/capsules/dawn-dispatch', '0 6 * * *'),
('sovereignty-bulletin', 'Operational Sovereignty Bulletin', 'ceremony', 'public', '/api/bulletins/generate', null),
('treasury-audit', 'Treasury Compliance Audit', 'treasury', 'custodian', '/api/treasury/audit', '0 0 1 * *'),
('education-matrix', 'Educational Content Matrix', 'education', 'public', '/api/education/matrix', null)
ON CONFLICT (slug) DO NOTHING;
    """
    
    try:
        # Create connection
        conn = create_connection()
        cursor = conn.cursor()
        
        print("🗄️ Creating Codex Dominion database schema...")
        
        # Execute schema creation
        cursor.execute(schema_sql)
        print("✅ Tables and indexes created successfully")
        
        # Insert initial data
        cursor.execute(initial_data)
        print("✅ Initial capsules data inserted")
        
        # Commit changes
        conn.commit()
        
        # Verify the setup
        cursor.execute("SELECT COUNT(*) FROM capsules")
        count = cursor.fetchone()[0]
        print(f"📊 Total capsules in database: {count}")
        
        cursor.execute("SELECT slug, title, kind FROM capsules ORDER BY created_at")
        capsules = cursor.fetchall()
        print("\n🎯 Deployed Capsules:")
        for slug, title, kind in capsules:
            print(f"  - {slug}: {title} ({kind})")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Codex Dominion database schema deployed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error deploying schema: {e}")
        return False

if __name__ == "__main__":
    execute_schema()