#!/bin/bash
# IONOS Production Deployment Script for CodexDominion.app
# Generated: December 3, 2025

set -e

echo "🔥 CODEXDOMINION.APP - IONOS PRODUCTION DEPLOYMENT 🔥"
echo "=================================================="

# Configuration
DOMAIN="codexdominion.app"
IONOS_SERVER="your-ionos-server-ip"  # Update with actual IP
IONOS_USER="your-ionos-username"     # Update with actual username
DEPLOY_PATH="/var/www/codexdominion.app"
BACKUP_PATH="/var/backups/codexdominion"

echo ""
echo "📋 Pre-Deployment Checklist"
echo "=========================="
echo "✅ Domain: $DOMAIN"
echo "✅ Server: $IONOS_SERVER"
echo "✅ Deploy Path: $DEPLOY_PATH"
echo ""

# Step 1: Build Frontend
echo "🔨 Step 1: Building Frontend Applications..."
echo "-------------------------------------------"
cd frontend || exit 1
npm install --production
npm run build
cd ..

echo "✅ Frontend build complete"
echo ""

# Step 2: Build Backend Assets
echo "🐍 Step 2: Preparing Python Backend..."
echo "---------------------------------------"
source .venv/Scripts/activate 2>/dev/null || python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt --quiet
echo "✅ Backend dependencies installed"
echo ""

# Step 3: Create deployment package
echo "📦 Step 3: Creating Deployment Package..."
echo "-------------------------------------------"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_ARCHIVE="codexdominion_${TIMESTAMP}.tar.gz"

tar -czf "$DEPLOY_ARCHIVE" \
  --exclude='node_modules' \
  --exclude='.venv' \
  --exclude='.git' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  frontend/out/ \
  src/ \
  artifacts/ \
  codexdominion/ \
  requirements.txt \
  package.json

echo "✅ Deployment package created: $DEPLOY_ARCHIVE"
echo ""

# Step 4: Upload to IONOS
echo "🚀 Step 4: Uploading to IONOS..."
echo "---------------------------------"
echo "Run these commands on IONOS server:"
echo ""
echo "# 1. Create backup"
echo "ssh $IONOS_USER@$IONOS_SERVER 'mkdir -p $BACKUP_PATH && tar -czf $BACKUP_PATH/backup_${TIMESTAMP}.tar.gz -C $DEPLOY_PATH .'"
echo ""
echo "# 2. Upload new version"
echo "scp $DEPLOY_ARCHIVE $IONOS_USER@$IONOS_SERVER:/tmp/"
echo ""
echo "# 3. Extract on server"
echo "ssh $IONOS_USER@$IONOS_SERVER 'cd $DEPLOY_PATH && tar -xzf /tmp/$DEPLOY_ARCHIVE && rm /tmp/$DEPLOY_ARCHIVE'"
echo ""
echo "# 4. Restart services"
echo "ssh $IONOS_USER@$IONOS_SERVER 'systemctl restart codexdominion-api && systemctl restart nginx'"
echo ""

# Step 5: Display next steps
echo "📝 Step 5: Manual Configuration Required"
echo "==========================================="
echo ""
echo "On IONOS server, create/update these files:"
echo ""
echo "1. /etc/systemd/system/codexdominion-api.service"
echo "2. /etc/nginx/sites-available/codexdominion.app"
echo "3. .env.production with environment variables"
echo ""
echo "See IONOS_DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "🔥 Deployment package ready! 🔥"
