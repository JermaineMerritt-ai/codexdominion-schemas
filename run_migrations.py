#!/usr/bin/env python3
"""Run database migrations for Codex Dominion PostgreSQL"""
import psycopg2
import os

# Database connection from environment
DB_HOST = "codex-pg-centralus2.postgres.database.azure.com"
DB_USER = "pgadmin"
DB_PASS = "Jer47#jer47"
DB_NAME = "codexdb"

print(f"Connecting to {DB_HOST}/{DB_NAME}...")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    sslmode='require'
)

# Read schema file
with open('codexdominion-schemas/schema.sql', 'r') as f:
    schema_sql = f.read()

# Execute schema
cursor = conn.cursor()
try:
    cursor.execute(schema_sql)
    conn.commit()
    print("✅ Schema migration completed successfully!")

    # Verify tables created
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print(f"\n📊 Tables created: {', '.join([t[0] for t in tables])}")

except Exception as e:
    print(f"❌ Migration failed: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
