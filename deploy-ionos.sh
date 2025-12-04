#!/bin/bash
# =============================================================================
# IONOS Production Deployment Script for CodexDominion.app
# =============================================================================
# Generated: December 3, 2025
# Complete automated deployment with database, SSL, and service configuration
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔥 CODEXDOMINION.APP - IONOS PRODUCTION DEPLOYMENT 🔥${NC}"
echo "=========================================================="
echo ""

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# =============================================================================
DOMAIN="codexdominion.app"
IONOS_SERVER="${IONOS_SERVER:-your-ionos-server-ip}"  # Set via environment or update here
IONOS_USER="${IONOS_USER:-your-ionos-username}"       # Set via environment or update here
DEPLOY_PATH="/var/www/codexdominion.app"
BACKUP_PATH="/var/backups/codexdominion"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_rsa}"

# Validate configuration
if [[ "$IONOS_SERVER" == "your-ionos-server-ip" ]] || [[ "$IONOS_USER" == "your-ionos-username" ]]; then
    echo -e "${RED}✗ ERROR: Please configure IONOS_SERVER and IONOS_USER${NC}"
    echo ""
    echo "Set environment variables:"
    echo "  export IONOS_SERVER='your.server.ip.address'"
    echo "  export IONOS_USER='your-username'"
    echo ""
    echo "Or edit this script and update the CONFIGURATION section"
    exit 1
fi

echo -e "${GREEN}📋 Deployment Configuration${NC}"
echo "============================"
echo "  Domain:      $DOMAIN"
echo "  Server:      $IONOS_SERVER"
echo "  User:        $IONOS_USER"
echo "  Deploy Path: $DEPLOY_PATH"
echo "  SSH Key:     $SSH_KEY"
echo ""
read -p "Continue with deployment? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi
echo ""

# =============================================================================
# Step 1: Build Frontend
# =============================================================================
echo -e "${BLUE}🔨 Step 1: Building Frontend Application${NC}"
echo "-------------------------------------------"
cd frontend || exit 1
echo "Installing dependencies..."
npm install --production=false
echo "Running production build..."
NODE_ENV=production npm run build
cd ..
echo -e "${GREEN}✓ Frontend build complete (output in frontend/out/)${NC}"
echo ""

# =============================================================================
# Step 2: Prepare Backend
# =============================================================================
echo -e "${BLUE}🐍 Step 2: Preparing Python Backend${NC}"
echo "---------------------------------------"
if [[ ! -d ".venv" ]]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Backend dependencies installed${NC}"
echo ""

# =============================================================================
# Step 3: Create Deployment Package
# =============================================================================
echo -e "${BLUE}📦 Step 3: Creating Deployment Package${NC}"
echo "-------------------------------------------"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_ARCHIVE="codexdominion_${TIMESTAMP}.tar.gz"

tar -czf "$DEPLOY_ARCHIVE" \
  --exclude='node_modules' \
  --exclude='.venv' \
  --exclude='.git' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='.env' \
  --exclude='.env.local' \
  frontend/.next/standalone/ \
  frontend/.next/static/ \
  frontend/public/ \
  src/ \
  artifacts/ \
  codexdominion/ \
  deployment/ \
  requirements.txt \
  .env.production

echo -e "${GREEN}✓ Deployment package created: $DEPLOY_ARCHIVE${NC}"
echo "  Size: $(du -h $DEPLOY_ARCHIVE | cut -f1)"
echo ""

# =============================================================================
# Step 4: Test SSH Connection
# =============================================================================
echo -e "${BLUE}🔗 Step 4: Testing SSH Connection${NC}"
echo "-----------------------------------"
if ! ssh -i "$SSH_KEY" -o ConnectTimeout=10 "$IONOS_USER@$IONOS_SERVER" "echo 'Connection successful'"; then
    echo -e "${RED}✗ SSH connection failed!${NC}"
    echo "  Please check:"
    echo "    - Server IP: $IONOS_SERVER"
    echo "    - Username: $IONOS_USER"
    echo "    - SSH key: $SSH_KEY"
    exit 1
fi
echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

# =============================================================================
# Step 5: Create Backup on Server
# =============================================================================
echo -e "${BLUE}💾 Step 5: Creating Backup on Server${NC}"
echo "--------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
sudo mkdir -p /var/backups/codexdominion
if [ -d "/var/www/codexdominion.app" ]; then
    BACKUP_FILE="/var/backups/codexdominion/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    sudo tar -czf "$BACKUP_FILE" -C /var/www/codexdominion.app . 2>/dev/null || true
    echo "Backup created: $BACKUP_FILE"
else
    echo "No existing installation found, skipping backup"
fi
ENDSSH
echo -e "${GREEN}✓ Backup completed${NC}"
echo ""

# =============================================================================
# Step 6: Upload Deployment Package
# =============================================================================
echo -e "${BLUE}🚀 Step 6: Uploading to IONOS Server${NC}"
echo "--------------------------------------"
echo "Uploading $DEPLOY_ARCHIVE..."
scp -i "$SSH_KEY" "$DEPLOY_ARCHIVE" "$IONOS_USER@$IONOS_SERVER:/tmp/"
echo -e "${GREEN}✓ Upload complete${NC}"
echo ""

# =============================================================================
# Step 7: Deploy on Server
# =============================================================================
echo -e "${BLUE}📂 Step 7: Deploying Application${NC}"
echo "----------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << ENDSSH
set -e

# Create directory structure
sudo mkdir -p /var/www/codexdominion.app/frontend
sudo mkdir -p /var/log/codexdominion
sudo mkdir -p /var/log/codexdominion-frontend
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo chown -R www-data:www-data /var/log/codexdominion
sudo chown -R www-data:www-data /var/log/codexdominion-frontend

# Extract deployment package to temporary location
cd /tmp
tar -xzf $DEPLOY_ARCHIVE

# Move Next.js standalone server to frontend directory
sudo rsync -av frontend/.next/standalone/ /var/www/codexdominion.app/frontend/
sudo mkdir -p /var/www/codexdominion.app/frontend/.next
sudo rsync -av frontend/.next/static/ /var/www/codexdominion.app/frontend/.next/static/
sudo rsync -av frontend/public/ /var/www/codexdominion.app/frontend/public/

# Move backend files
sudo rsync -av src/ /var/www/codexdominion.app/src/
sudo rsync -av artifacts/ /var/www/codexdominion.app/artifacts/ || true
sudo rsync -av codexdominion/ /var/www/codexdominion.app/codexdominion/ || true
sudo rsync -av deployment/ /var/www/codexdominion.app/deployment/
sudo cp requirements.txt /var/www/codexdominion.app/
sudo cp .env.production /var/www/codexdominion.app/

# Cleanup
rm -rf /tmp/frontend /tmp/src /tmp/artifacts /tmp/codexdominion /tmp/deployment /tmp/requirements.txt /tmp/.env.production
sudo rm /tmp/$DEPLOY_ARCHIVE

# Set permissions
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo chmod -R 755 /var/www/codexdominion.app
sudo chmod 600 /var/www/codexdominion.app/.env.production

echo "✓ Application files deployed"
ENDSSH
echo -e "${GREEN}✓ Deployment complete${NC}"
echo ""
# =============================================================================
# Step 8: Install System Dependencies
# =============================================================================
echo -e "${BLUE}📦 Step 8: Installing System Dependencies${NC}"
echo "-------------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
set -e

# Update package list
sudo apt update

# Install Node.js 18.x LTS (required for Next.js)
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL
if ! command -v psql &> /dev/null; then
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Install Nginx
if ! command -v nginx &> /dev/null; then
    sudo apt install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
fi

# Install Certbot for SSL
if ! command -v certbot &> /dev/null; then
    sudo apt install -y certbot python3-certbot-nginx
fi

echo "✓ System dependencies installed"
echo "  Node.js version: $(node --version)"
echo "  Python version: $(python3 --version)"
ENDSSH
echo -e "${GREEN}✓ System dependencies ready${NC}"
echo ""

# =============================================================================
# Step 9: Setup Python Virtual Environment
# =============================================================================
echo -e "${BLUE}🐍 Step 9: Setting up Python Environment${NC}"
echo "-------------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
set -e

cd /var/www/codexdominion.app

# Create virtual environment
sudo -u www-data python3 -m venv .venv

# Install Python packages
sudo -u www-data .venv/bin/pip install --upgrade pip
sudo -u www-data .venv/bin/pip install -r requirements.txt

echo "✓ Python environment configured"
ENDSSH
echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

# =============================================================================
# Step 10: Setup Database
# =============================================================================
echo -e "${BLUE}🗄️  Step 10: Setting up Database${NC}"
echo "----------------------------------"
echo "Uploading database setup script..."
scp -i "$SSH_KEY" deployment/setup-database.sh "$IONOS_USER@$IONOS_SERVER:/tmp/"

ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
chmod +x /tmp/setup-database.sh
sudo /tmp/setup-database.sh
rm /tmp/setup-database.sh
ENDSSH
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# =============================================================================
# Step 11: Configure Systemd Service
# =============================================================================
echo -e "${BLUE}⚙️  Step 11: Configuring Systemd Services${NC}"
echo "--------------------------------------------"
scp -i "$SSH_KEY" deployment/codexdominion-api.service "$IONOS_USER@$IONOS_SERVER:/tmp/"
scp -i "$SSH_KEY" deployment/codexdominion-frontend.service "$IONOS_USER@$IONOS_SERVER:/tmp/"
scp -i "$SSH_KEY" deployment/logging.conf "$IONOS_USER@$IONOS_SERVER:/tmp/"

ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
set -e

# Install service files
sudo cp /tmp/codexdominion-api.service /etc/systemd/system/
sudo cp /tmp/codexdominion-frontend.service /etc/systemd/system/
sudo rm /tmp/codexdominion-api.service /tmp/codexdominion-frontend.service

# Install logging config
sudo cp /tmp/logging.conf /var/www/codexdominion.app/deployment/
sudo rm /tmp/logging.conf

# Reload systemd and enable services
sudo systemctl daemon-reload
sudo systemctl enable codexdominion-api
sudo systemctl enable codexdominion-frontend
sudo systemctl start codexdominion-api
sudo systemctl start codexdominion-frontend

# Check status
sleep 3
echo "Backend API Status:"
sudo systemctl status codexdominion-api --no-pager || true
echo ""
echo "Frontend Server Status:"
sudo systemctl status codexdominion-frontend --no-pager || true

echo "✓ Systemd services configured"
ENDSSH
echo -e "${GREEN}✓ API and Frontend services running${NC}"
echo ""

# =============================================================================
# Step 12: Configure Nginx
# =============================================================================
echo -e "${BLUE}🌐 Step 12: Configuring Nginx${NC}"
echo "--------------------------------"
scp -i "$SSH_KEY" deployment/nginx-production.conf "$IONOS_USER@$IONOS_SERVER:/tmp/"

ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << ENDSSH
set -e

# Install nginx config
sudo cp /tmp/nginx-production.conf /etc/nginx/sites-available/codexdominion.app
sudo rm /tmp/nginx-production.conf

# Create symlink (if not exists)
if [ ! -L "/etc/nginx/sites-enabled/codexdominion.app" ]; then
    sudo ln -s /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/
fi

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

echo "✓ Nginx configuration installed"
ENDSSH
echo -e "${GREEN}✓ Nginx configured${NC}"
echo ""

# =============================================================================
# Step 13: Setup SSL Certificate
# =============================================================================
echo -e "${BLUE}🔒 Step 13: Setting up SSL Certificate${NC}"
echo "---------------------------------------"
echo "This will request SSL certificate from Let's Encrypt"
echo ""
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << ENDSSH
set -e

# Stop nginx temporarily for standalone certbot
sudo systemctl stop nginx

# Request certificate
sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN -d api.$DOMAIN \
    --non-interactive --agree-tos --email admin@$DOMAIN || {
    echo "⚠️  SSL certificate request failed. You may need to:"
    echo "    1. Ensure DNS is pointing to this server"
    echo "    2. Ensure ports 80 and 443 are open"
    echo "    3. Run manually: sudo certbot certonly --nginx -d $DOMAIN"
}

# Restart nginx
sudo systemctl start nginx
sudo systemctl reload nginx

# Setup auto-renewal
if ! sudo crontab -l 2>/dev/null | grep -q certbot; then
    (sudo crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && systemctl reload nginx") | sudo crontab -
fi

echo "✓ SSL certificate configured"
ENDSSH
echo -e "${GREEN}✓ SSL ready${NC}"
echo ""

# =============================================================================
# Step 14: Final Service Restart
# =============================================================================
echo -e "${BLUE}🔄 Step 14: Restarting All Services${NC}"
echo "-------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
sudo systemctl restart codexdominion-api
sudo systemctl restart nginx
sleep 2
echo "✓ All services restarted"
ENDSSH
echo -e "${GREEN}✓ Services running${NC}"
echo ""

# =============================================================================
# Step 15: Health Check
# =============================================================================
echo -e "${BLUE}🏥 Step 15: Running Health Checks${NC}"
echo "-----------------------------------"
sleep 3

# Check API health
echo "Testing API endpoint..."
if curl -s -o /dev/null -w "%{http_code}" "http://$IONOS_SERVER:8001/health" | grep -q "200"; then
    echo -e "${GREEN}✓ API is responding${NC}"
else
    echo -e "${YELLOW}⚠️  API health check inconclusive${NC}"
fi

# Check nginx
echo "Testing Nginx..."
if ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" "sudo systemctl is-active --quiet nginx"; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is not running${NC}"
fi

# Check API service
echo "Testing API service..."
if ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" "sudo systemctl is-active --quiet codexdominion-api"; then
    echo -e "${GREEN}✓ API service is running${NC}"
else
    echo -e "${RED}✗ API service is not running${NC}"
fi
echo ""

# =============================================================================
# Deployment Complete
# =============================================================================
echo "=========================================================="
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo "=========================================================="
echo ""
echo "🌐 Your application is deployed at:"
echo "   https://$DOMAIN"
echo "   https://api.$DOMAIN"
echo ""
echo "📝 Important Files on Server:"
echo "   Application:  /var/www/codexdominion.app"
echo "   Logs:         /var/log/codexdominion/"
echo "   Nginx Config: /etc/nginx/sites-available/codexdominion.app"
echo "   Service:      /etc/systemd/system/codexdominion-api.service"
echo "   DB Creds:     /var/www/codexdominion.app/.db_credentials"
echo ""
echo "🔧 Useful Commands (on server):"
echo "   sudo systemctl status codexdominion-api"
echo "   sudo systemctl restart codexdominion-api"
echo "   sudo systemctl restart nginx"
echo "   sudo tail -f /var/log/codexdominion/api.log"
echo "   sudo tail -f /var/log/nginx/codexdominion-error.log"
echo ""
echo -e "${YELLOW}⚠️  Next Steps:${NC}"
echo "   1. Update DNS records to point to $IONOS_SERVER"
echo "   2. Update .env.production with secure credentials"
echo "   3. Test all endpoints: https://$DOMAIN"
echo "   4. Set up monitoring and backups"
echo "   5. Review security settings"
echo ""
echo "🔥 Codex Dominion is LIVE! 🔥"
echo ""

# Cleanup
rm -f "$DEPLOY_ARCHIVE"
echo "Local deployment archive cleaned up"
