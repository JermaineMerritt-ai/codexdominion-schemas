#!/bin/bash
# CodexDominion.app - Complete VPS Deployment Script
# Run this on your IONOS VPS after SSH connection

set -e

echo "🔥 CODEXDOMINION.APP VPS DEPLOYMENT 🔥"
echo "========================================"
echo ""

# Configuration
DOMAIN="codexdominion.app"
APP_DIR="/var/www/codexdominion.app"
REPO_URL="https://github.com/JermaineMerritt-ai/codexdominion-schemas.git"

echo "📋 System Information"
echo "--------------------"
echo "Domain: $DOMAIN"
echo "App Directory: $APP_DIR"
echo "Repository: $REPO_URL"
echo ""

# Step 1: Update system
echo "🔄 Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install required packages
echo "📦 Step 2: Installing required packages..."
sudo apt install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    nginx \
    certbot \
    python3-certbot-nginx \
    postgresql \
    postgresql-contrib \
    unzip

# Install Node 18+ if needed
echo "📦 Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

echo "✅ Installed versions:"
python3 --version
node --version
npm --version
git --version
echo ""

# Step 3: Clone repository
echo "📥 Step 3: Cloning repository..."
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR
cd $APP_DIR
git clone $REPO_URL .

echo "✅ Repository cloned"
echo ""

# Step 4: Set up Python backend
echo "🐍 Step 4: Setting up Python backend..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python dependencies installed"
echo ""

# Step 5: Set up database
echo "🗄️ Step 5: Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
CREATE DATABASE codexdominion;
CREATE USER codexdominion_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE codexdominion TO codexdominion_user;
\q
EOF

echo "✅ Database created"
echo ""

# Step 6: Create environment file
echo "⚙️ Step 6: Creating environment configuration..."
cat > $APP_DIR/.env.production << EOF
# Database
DATABASE_URL=postgresql://codexdominion_user:CHANGE_THIS_PASSWORD@localhost/codexdominion

# Application
NODE_ENV=production
PYTHON_ENV=production
API_BASE_URL=https://api.$DOMAIN
FRONTEND_URL=https://$DOMAIN

# Security
JWT_SECRET=$(openssl rand -hex 32)
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN,https://api.$DOMAIN

# Logging
LOG_LEVEL=INFO
LOG_DIR=/var/log/codexdominion
EOF

sudo mkdir -p /var/log/codexdominion
sudo chown -R $USER:$USER /var/log/codexdominion

echo "✅ Environment configured"
echo ""

# Step 7: Install systemd service
echo "🔧 Step 7: Installing systemd service..."
sudo cp $APP_DIR/codexdominion-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable codexdominion-api
sudo systemctl start codexdominion-api

echo "✅ Backend service started"
echo ""

# Step 8: Configure Nginx
echo "🌐 Step 8: Configuring Nginx..."
sudo cp $APP_DIR/nginx-codexdominion.conf /etc/nginx/sites-available/codexdominion.app
sudo ln -sf /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "✅ Nginx configured"
echo ""

# Step 9: SSL Certificate
echo "🔒 Step 9: Installing SSL certificate..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN -d api.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

echo "✅ SSL certificate installed"
echo ""

# Step 10: Verify deployment
echo "🔍 Step 10: Verifying deployment..."
echo ""
echo "Backend API status:"
sudo systemctl status codexdominion-api --no-pager
echo ""
echo "Nginx status:"
sudo systemctl status nginx --no-pager
echo ""

# Final status
echo "======================================"
echo "🔥 DEPLOYMENT COMPLETE! 🔥"
echo "======================================"
echo ""
echo "✅ Application deployed to: $APP_DIR"
echo "✅ Backend API running on port 8000"
echo "✅ Nginx configured and running"
echo "✅ SSL certificates installed"
echo ""
echo "🌐 Your sites:"
echo "   Frontend: https://$DOMAIN"
echo "   API: https://api.$DOMAIN"
echo ""
echo "📝 Next steps:"
echo "   1. Update DNS records to point to this server"
echo "   2. Edit .env.production to change database password"
echo "   3. Run database migrations if needed"
echo ""
echo "📊 Check logs:"
echo "   Backend: sudo journalctl -u codexdominion-api -f"
echo "   Nginx: sudo tail -f /var/log/nginx/codexdominion-*.log"
echo ""
echo "🔄 Restart services:"
echo "   Backend: sudo systemctl restart codexdominion-api"
echo "   Nginx: sudo systemctl restart nginx"
echo ""
echo "✨ CodexDominion.app is now LIVE! ✨"
