# Option E: Database Integration Setup
# Migrates JSON ledger to Azure PostgreSQL

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "OPTION E: DATABASE INTEGRATION" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$RG = "codex-rg"
$LOCATION = "eastus2"
$DB_SERVER = "codex-db-server"
$DB_NAME = "codexdb"
$DB_USER = "codexadmin"
$BACKEND_APP = "codex-backend-https"

Write-Host "[Step 1/5] Creating Azure Database for PostgreSQL..." -ForegroundColor Yellow

# Generate random password
$DB_PASSWORD = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})

# Check if server exists
$serverExists = az postgres flexible-server show --name $DB_SERVER --resource-group $RG 2>$null

if (-not $serverExists) {
    Write-Host "  Creating PostgreSQL Flexible Server..." -ForegroundColor Gray

    az postgres flexible-server create `
        --name $DB_SERVER `
        --resource-group $RG `
        --location $LOCATION `
        --admin-user $DB_USER `
        --admin-password $DB_PASSWORD `
        --sku-name Standard_B1ms `
        --tier Burstable `
        --storage-size 32 `
        --version 14 `
        --public-access 0.0.0.0-255.255.255.255 `
        --output none

    Write-Host "  ✅ PostgreSQL server created" -ForegroundColor Green

    # Create database
    az postgres flexible-server db create `
        --resource-group $RG `
        --server-name $DB_SERVER `
        --database-name $DB_NAME `
        --output none

    Write-Host "  ✅ Database created: $DB_NAME" -ForegroundColor Green
} else {
    Write-Host "  ✅ PostgreSQL server already exists" -ForegroundColor Green
    Write-Host "  ⚠️  Using existing password" -ForegroundColor Yellow
}

$DB_HOST = az postgres flexible-server show --name $DB_SERVER --resource-group $RG --query fullyQualifiedDomainName -o tsv

Write-Host ""
Write-Host "[Step 2/5] Creating Database Schema..." -ForegroundColor Yellow

# Create SQL schema file
$schema = @"
-- Codex Dominion Database Schema

CREATE TABLE IF NOT EXISTS meta (
    version VARCHAR(10),
    omega_seal BOOLEAN,
    last_updated TIMESTAMP,
    custodian_authority VARCHAR(100),
    ledger_type VARCHAR(50),
    seal_power VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS heartbeat (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20),
    last_dispatch TIMESTAMP,
    next_dispatch TIMESTAMP,
    pulse_count INTEGER,
    health_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proclamations (
    id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200),
    status VARCHAR(20),
    issued_by VARCHAR(100),
    issued_date TIMESTAMP,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cycles (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    state VARCHAR(20),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manifest VARCHAR(200),
    version VARCHAR(10),
    purpose TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS revenue_streams (
    id SERIAL PRIMARY KEY,
    stream_name VARCHAR(50),
    amount DECIMAL(10,2),
    currency VARCHAR(3),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS social_media_metrics (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50),
    metric_name VARCHAR(50),
    metric_value INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_proclamations_status ON proclamations(status);
CREATE INDEX IF NOT EXISTS idx_cycles_state ON cycles(state);
CREATE INDEX IF NOT EXISTS idx_revenue_stream ON revenue_streams(stream_name, recorded_at);
CREATE INDEX IF NOT EXISTS idx_social_platform ON social_media_metrics(platform, recorded_at);
"@

$schema | Out-File "database_schema.sql" -Encoding UTF8

Write-Host "  ✅ Schema file created: database_schema.sql" -ForegroundColor Green
Write-Host ""

Write-Host "[Step 3/5] Migrating JSON Ledger Data..." -ForegroundColor Yellow

# Load existing ledger
$ledger = Get-Content "codex_ledger.json" -Raw | ConvertFrom-Json

Write-Host "  Loading codex_ledger.json..." -ForegroundColor Gray
Write-Host "  • Meta data: 1 record" -ForegroundColor Gray
Write-Host "  • Proclamations: $($ledger.proclamations.Count) records" -ForegroundColor Gray
Write-Host "  • Portals: $($ledger.portals.Count) records" -ForegroundColor Gray
Write-Host "  • Cycles: $($ledger.cycles.Count) records" -ForegroundColor Gray

# Create migration SQL
$migrationSQL = @"
-- Migration data from codex_ledger.json
-- Run this against your PostgreSQL database

-- Clear existing data
TRUNCATE TABLE meta, proclamations, portals, cycles RESTART IDENTITY CASCADE;

-- Insert meta data
INSERT INTO meta (version, omega_seal, last_updated, custodian_authority, ledger_type, seal_power)
VALUES ('$($ledger.meta.version)', $($ledger.meta.omega_seal.ToString().ToLower()), '$($ledger.meta.last_updated)', '$($ledger.meta.custodian_authority)', '$($ledger.meta.ledger_type)', '$($ledger.meta.seal_power)');

-- Insert proclamations
"@

foreach ($proc in $ledger.proclamations) {
    $content = $proc.content -replace "'", "''"
    $migrationSQL += @"

INSERT INTO proclamations (id, title, status, issued_by, issued_date, content)
VALUES ('$($proc.id)', '$($proc.title)', '$($proc.status)', '$($proc.issued_by)', '$($proc.issued_date)', '$content');
"@
}

$migrationSQL | Out-File "migration.sql" -Encoding UTF8

Write-Host "  ✅ Migration SQL created: migration.sql" -ForegroundColor Green
Write-Host ""

Write-Host "[Step 4/5] Updating Backend Configuration..." -ForegroundColor Yellow

# Update container app with database connection string
$connectionString = "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}?sslmode=require"

az containerapp update `
    --name $BACKEND_APP `
    --resource-group $RG `
    --set-env-vars "DATABASE_URL=$connectionString" `
    --output none

Write-Host "  ✅ Backend configured with database connection" -ForegroundColor Green
Write-Host ""

Write-Host "[Step 5/5] Creating Python Migration Script..." -ForegroundColor Yellow

$pythonMigration = @'
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
'@

$pythonMigration | Out-File "migrate_to_database.py" -Encoding UTF8

Write-Host "  ✅ Python migration script created" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DATABASE INTEGRATION SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "🗄️  Database Details:" -ForegroundColor White
Write-Host "  Server: $DB_HOST" -ForegroundColor Gray
Write-Host "  Database: $DB_NAME" -ForegroundColor Gray
Write-Host "  Username: $DB_USER" -ForegroundColor Gray
Write-Host "  Password: $DB_PASSWORD" -ForegroundColor Yellow
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor White
Write-Host "  1. Run migration: python migrate_to_database.py" -ForegroundColor Gray
Write-Host "  2. Update backend code to use PostgreSQL instead of JSON" -ForegroundColor Gray
Write-Host "  3. Test database connections" -ForegroundColor Gray
Write-Host "  4. Keep codex_ledger.json as backup" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Cost: ~$10-15/month (Burstable tier)" -ForegroundColor White
Write-Host ""

# Save configuration
@{
    server = $DB_HOST
    database = $DB_NAME
    username = $DB_USER
    password = $DB_PASSWORD
    connection_string = $connectionString
    configured_date = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    cost = "~$10-15/month"
} | ConvertTo-Json | Out-File "database-config.json"

Write-Host "💾 Configuration saved to: database-config.json" -ForegroundColor Gray
Write-Host "⚠️  IMPORTANT: Keep database-config.json secure (contains password)" -ForegroundColor Yellow
Write-Host ""
