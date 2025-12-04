#!/bin/bash
# =============================================================================
# CODEX DOMINION - DATABASE INITIALIZATION SCRIPT
# =============================================================================
# Purpose: Initialize PostgreSQL database for production deployment
# Generated: 2025-12-03
# =============================================================================

set -e

echo "🔥 CODEX DOMINION - DATABASE SETUP 🔥"
echo "======================================"
echo ""

# Configuration
DB_NAME="codexdominion_prod"
DB_USER="codex_user"
DB_PASSWORD="${DB_PASSWORD:-$(openssl rand -base64 32)}"
DB_HOST="localhost"
DB_PORT="5432"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# =============================================================================
# Step 1: Check PostgreSQL Installation
# =============================================================================
echo "📋 Step 1: Checking PostgreSQL installation..."
if ! command -v psql &> /dev/null; then
    echo -e "${RED}✗ PostgreSQL is not installed!${NC}"
    echo "Installing PostgreSQL..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    echo -e "${GREEN}✓ PostgreSQL installed successfully${NC}"
else
    echo -e "${GREEN}✓ PostgreSQL is installed${NC}"
fi
echo ""

# =============================================================================
# Step 2: Create Database User
# =============================================================================
echo "👤 Step 2: Creating database user..."
sudo -u postgres psql -c "SELECT 1 FROM pg_user WHERE usename = '$DB_USER'" | grep -q 1 || \
sudo -u postgres psql << EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER USER $DB_USER WITH CREATEDB;
EOF
echo -e "${GREEN}✓ Database user '$DB_USER' created/verified${NC}"
echo ""

# =============================================================================
# Step 3: Create Database
# =============================================================================
echo "🗄️  Step 3: Creating database..."
sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME || \
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF
echo -e "${GREEN}✓ Database '$DB_NAME' created/verified${NC}"
echo ""

# =============================================================================
# Step 4: Initialize Database Schema
# =============================================================================
echo "🏗️  Step 4: Initializing database schema..."

# Create tables SQL
sudo -u postgres psql -d $DB_NAME << 'EOF'
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Capsules Table
CREATE TABLE IF NOT EXISTS capsules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    lineage VARCHAR(255),
    description TEXT,
    schedule VARCHAR(100),
    archive_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scrolls Table
CREATE TABLE IF NOT EXISTS scrolls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scroll_id VARCHAR(255) UNIQUE NOT NULL,
    heir_id VARCHAR(255) NOT NULL,
    cycle VARCHAR(50),
    codex_right VARCHAR(255),
    pledge TEXT,
    pledge_rank VARCHAR(50),
    flame_status VARCHAR(50) DEFAULT 'sovereign',
    timestamp VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Artifacts Table
CREATE TABLE IF NOT EXISTS artifacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    capsule_slug VARCHAR(255) REFERENCES capsules(slug),
    title VARCHAR(255) NOT NULL,
    generated_at TIMESTAMP,
    execution_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'complete',
    tier_counts JSONB,
    picks JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Signals Table
CREATE TABLE IF NOT EXISTS signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    signal_type VARCHAR(100) NOT NULL,
    source VARCHAR(255),
    data JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Heirs Registry Table
CREATE TABLE IF NOT EXISTS heirs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    heir_id VARCHAR(255) UNIQUE NOT NULL,
    avatar VARCHAR(100),
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes
CREATE INDEX IF NOT EXISTS idx_capsules_slug ON capsules(slug);
CREATE INDEX IF NOT EXISTS idx_capsules_status ON capsules(status);
CREATE INDEX IF NOT EXISTS idx_scrolls_heir_id ON scrolls(heir_id);
CREATE INDEX IF NOT EXISTS idx_scrolls_timestamp ON scrolls(timestamp);
CREATE INDEX IF NOT EXISTS idx_artifacts_capsule ON artifacts(capsule_slug);
CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_signals_created ON signals(created_at);
CREATE INDEX IF NOT EXISTS idx_heirs_heir_id ON heirs(heir_id);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO codex_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO codex_user;

EOF

echo -e "${GREEN}✓ Database schema initialized${NC}"
echo ""

# =============================================================================
# Step 5: Insert Sample Data (Optional)
# =============================================================================
echo "📝 Step 5: Inserting sample data..."
sudo -u postgres psql -d $DB_NAME << 'EOF'
-- Sample Capsules
INSERT INTO capsules (name, slug, domain, status, description, schedule)
VALUES
    ('Eternal Flame', 'eternal-flame', 'sovereignty', 'active', 'The eternal flame of the Codex', 'continuous'),
    ('Cosmic Archive', 'cosmic-archive', 'archive', 'active', 'Archive of cosmic knowledge', 'daily'),
    ('Sacred Dispatch', 'sacred-dispatch', 'communication', 'active', 'Sacred message dispatch system', 'real-time')
ON CONFLICT (slug) DO NOTHING;

EOF
echo -e "${GREEN}✓ Sample data inserted${NC}"
echo ""

# =============================================================================
# Step 6: Save Database Credentials
# =============================================================================
echo "🔐 Step 6: Saving database credentials..."
CREDENTIALS_FILE="/var/www/codexdominion.app/.db_credentials"
sudo mkdir -p /var/www/codexdominion.app
sudo bash -c "cat > $CREDENTIALS_FILE" << EOF
# Database Credentials - Generated $(date)
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT

# Connection String
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME
EOF
sudo chmod 600 $CREDENTIALS_FILE
echo -e "${GREEN}✓ Credentials saved to $CREDENTIALS_FILE${NC}"
echo ""

# =============================================================================
# Step 7: Configure PostgreSQL for Remote Access (Optional)
# =============================================================================
echo "🌐 Step 7: Configuring PostgreSQL access..."
PG_VERSION=$(psql --version | grep -oP '\d+' | head -1)
PG_HBA_FILE="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_CONF_FILE="/etc/postgresql/$PG_VERSION/main/postgresql.conf"

# Backup original files
sudo cp $PG_HBA_FILE ${PG_HBA_FILE}.backup 2>/dev/null || true
sudo cp $PG_CONF_FILE ${PG_CONF_FILE}.backup 2>/dev/null || true

# Update pg_hba.conf for local connections
if ! sudo grep -q "host.*$DB_NAME.*$DB_USER" $PG_HBA_FILE; then
    sudo bash -c "echo 'host    $DB_NAME    $DB_USER    127.0.0.1/32    md5' >> $PG_HBA_FILE"
fi

# Restart PostgreSQL
sudo systemctl restart postgresql
echo -e "${GREEN}✓ PostgreSQL configured${NC}"
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "======================================"
echo -e "${GREEN}🎉 DATABASE SETUP COMPLETE!${NC}"
echo "======================================"
echo ""
echo "Database Details:"
echo "  Name:     $DB_NAME"
echo "  User:     $DB_USER"
echo "  Password: $DB_PASSWORD"
echo "  Host:     $DB_HOST"
echo "  Port:     $DB_PORT"
echo ""
echo "Connection String:"
echo "  postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Save these credentials securely!${NC}"
echo "  Credentials file: $CREDENTIALS_FILE"
echo ""
echo "Next Steps:"
echo "  1. Update .env.production with DATABASE_URL"
echo "  2. Test connection: psql -h $DB_HOST -U $DB_USER -d $DB_NAME"
echo "  3. Run application migrations if needed"
echo ""
