#!/usr/bin/env python3
"""
Connect to Cloud SQL and deploy schema using Python and cloud-sql-python-connector
"""
import sqlalchemy
from google.cloud.sql.connector import Connector


def deploy_schema():
    """Deploy the Codex Dominion schema to Cloud SQL"""

    # Database connection details
    instance_connection_name = "codex-dominion-prod:us-central1:codex-ledger"
    db_user = "codex_user"
    db_pass = "codex_pass"
    db_name = "codex"

    print("🔗 Connecting to Cloud SQL database...")

    # Initialize Connector object
    connector = Connector()

    # Function to return the database connection
    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    # Create connection pool
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    # Schema SQL
    schema_sql = """
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

-- Indexes for fast lookup
CREATE INDEX IF NOT EXISTS idx_capsules_slug ON capsules(slug);
CREATE INDEX IF NOT EXISTS idx_runs_capsule_slug ON capsule_runs(capsule_slug);
CREATE INDEX IF NOT EXISTS idx_runs_started_at ON capsule_runs(started_at);
"""

    initial_data_sql = """
-- Insert initial capsules for Codex Dominion system
INSERT INTO capsules (slug, title, kind, mode, entrypoint, schedule) VALUES
('signals-daily', 'Daily Signals Dispatch', 'engine', 'custodian', '/api/signals/daily', '0 6 * * *'),
('dawn-dispatch', 'Dawn Proclamation Capsule', 'dispatch', 'custodian', '/api/capsules/dawn-dispatch', '0 6 * * *'),
('sovereignty-bulletin', 'Operational Sovereignty Bulletin', 'ceremony', 'public', '/api/bulletins/generate', null),
('treasury-audit', 'Treasury Compliance Audit', 'treasury', 'custodian', '/api/treasury/audit', '0 0 1 * *'),
('education-matrix', 'Educational Content Matrix', 'education', 'public', '/api/education/matrix', null)
ON CONFLICT (slug) DO UPDATE SET
    title = EXCLUDED.title,
    kind = EXCLUDED.kind,
    mode = EXCLUDED.mode,
    entrypoint = EXCLUDED.entrypoint,
    schedule = EXCLUDED.schedule;
"""

    try:
        with engine.connect() as connection:
            print("✅ Connected to Cloud SQL successfully!")

            # Execute schema creation
            print("📋 Creating tables and indexes...")
            connection.execute(sqlalchemy.text(schema_sql))
            connection.commit()
            print("✅ Tables and indexes created")

            # Insert initial data
            print("📊 Inserting initial capsules...")
            connection.execute(sqlalchemy.text(initial_data_sql))
            connection.commit()
            print("✅ Initial data inserted")

            # Verify the deployment
            result = connection.execute(
                sqlalchemy.text("SELECT COUNT(*) FROM capsules")
            )
            count = result.scalar()
            print(f"📈 Total capsules: {count}")

            # List all capsules
            result = connection.execute(
                sqlalchemy.text(
                    "SELECT slug, title, kind, schedule FROM capsules ORDER BY created_at"
                )
            )
            capsules = result.fetchall()

            print("\n🎯 Deployed Capsules:")
            for row in capsules:
                slug, title, kind, schedule = row
                schedule_info = (
                    f" (scheduled: {schedule})" if schedule else " (on-demand)"
                )
                print(f"  ✅ {slug}: {title} ({kind}){schedule_info}")

            print(f"\n🎉 Schema deployment completed successfully!")
            print(f"🗄️ Database: {db_name}")
            print(f"📍 Instance: {instance_connection_name}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        connector.close()

    return True


if __name__ == "__main__":
    deploy_schema()
