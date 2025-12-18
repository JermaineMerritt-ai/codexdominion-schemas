#!/usr/bin/env python3
"""
Database Migration Script
Migrates codex_ledger.json to PostgreSQL
"""

import json
import psycopg2
from datetime import datetime
import os

# Load database connection from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL environment variable not set")
    exit(1)

print("Connecting to database...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("✅ Connected successfully")

# Load JSON ledger
with open("codex_ledger.json", "r") as f:
    ledger = json.load(f)

print(f"\nMigrating data:")
print(f"  • Proclamations: {len(ledger['proclamations'])}")
print(f"  • Portals: {len(ledger['portals'])}")

# Execute schema
with open("database_schema.sql", "r") as f:
    cursor.execute(f.read())

print("✅ Schema created")

# Migrate data (execute migration.sql)
with open("migration.sql", "r") as f:
    cursor.execute(f.read())

conn.commit()
print("✅ Data migrated successfully")

# Verify
cursor.execute("SELECT COUNT(*) FROM proclamations")
count = cursor.fetchone()[0]
print(f"\n✅ Verification: {count} proclamations in database")

cursor.close()
conn.close()
print("\n🎉 Migration complete!")
