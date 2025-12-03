#!/bin/bash

# ============================================
# IONOS Server Setup Script
# CodexDominion.app Production Environment
# ============================================

set -e  # Exit on error

echo "🚀 Starting IONOS Server Setup for CodexDominion.app"
echo "=================================================="

# ============================================
# 1. System Update
# ============================================
echo ""
echo "📦 Step 1: Updating system packages..."
apt update
apt upgrade -y

# ============================================
# 2. Install Essential Tools
# ============================================
echo ""
echo "🔧 Step 2: Installing essential tools..."
apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    ufw \
    fail2ban \
    certbot \
    python3-certbot-nginx

# ============================================
# 3. Install Docker
# ============================================
echo ""
echo "🐳 Step 3: Installing Docker..."

# Remove old versions
apt remove -y docker docker-engine docker.io containerd runc || true

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Install Docker Compose
apt install -y docker-compose-plugin

# Start Docker service
systemctl start docker
systemctl enable docker

# Test Docker
docker --version
docker compose version

echo "✅ Docker installed successfully"

# ============================================
# 4. Install Nginx
# ============================================
echo ""
echo "🌐 Step 4: Installing Nginx..."

apt install -y nginx

# Start Nginx
systemctl start nginx
systemctl enable nginx

# Test Nginx
nginx -v

echo "✅ Nginx installed successfully"

# ============================================
# 5. Configure Firewall
# ============================================
echo ""
echo "🔥 Step 5: Configuring firewall..."

# Enable UFW
ufw --force enable

# Allow SSH (important!)
ufw allow 22/tcp

# Allow HTTP & HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Show status
ufw status verbose

echo "✅ Firewall configured"

# ============================================
# 6. Create Application Directory
# ============================================
echo ""
echo "📁 Step 6: Creating application directories..."

# Main application directory
mkdir -p /var/www/codexdominion
cd /var/www/codexdominion

# Create subdirectories
mkdir -p {data,logs,backups,ssl,nginx,scripts}
mkdir -p data/{dashboard,api,stocks,analytics}
mkdir -p logs/{dashboard,api,stockanalytics,analytics,nginx}

# Set permissions
chown -R www-data:www-data /var/www/codexdominion
chmod -R 755 /var/www/codexdominion

echo "✅ Directories created"

# ============================================
# 7. Configure Nginx
# ============================================
echo ""
echo "⚙️ Step 7: Configuring Nginx..."

# Backup default config
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

# Create CodexDominion config
cat > /etc/nginx/sites-available/codexdominion << 'NGINX_CONFIG'
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;
    return 301 https://codexdominion.app$request_uri;
}

# Main site
server {
    listen 443 ssl http2;
    server_name codexdominion.app www.codexdominion.app;
    
    # SSL certificates (will be added by certbot)
    # ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logs
    access_log /var/www/codexdominion/logs/nginx/access.log;
    error_log /var/www/codexdominion/logs/nginx/error.log;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}

# Dashboard
server {
    listen 443 ssl http2;
    server_name dashboard.codexdominion.app;
    
    # SSL certificates
    # ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# API Gateway
server {
    listen 443 ssl http2;
    server_name api.codexdominion.app;
    
    # SSL certificates
    # ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Stock Analytics
server {
    listen 443 ssl http2;
    server_name stockanalytics.codexdominion.app;
    
    # SSL certificates
    # ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8515;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGINX_CONFIG

# Enable site
ln -sf /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/

# Test configuration
nginx -t

echo "✅ Nginx configured"

# ============================================
# 8. Create Environment File Template
# ============================================
echo ""
echo "📝 Step 8: Creating environment file..."

cat > /var/www/codexdominion/.env.template << 'ENV_TEMPLATE'
# ============================================
# CodexDominion Production Environment
# ============================================

# API Keys
API_KEY=your-secure-api-key-here
ALPHA_VANTAGE_KEY=your-alphavantage-key
POLYGON_API_KEY=your-polygon-key

# Database
DATABASE_URL=postgresql://codex:PASSWORD@database:5432/codexdominion
DATABASE_PASSWORD=your-secure-database-password

# Redis
REDIS_PASSWORD=your-secure-redis-password

# Domain
DOMAIN=codexdominion.app

# Azure Integration
AZURE_AI_ENDPOINT=https://jermaine-ai.codexdominion.app
ENV_TEMPLATE

echo "⚠️  IMPORTANT: Edit /var/www/codexdominion/.env with your actual credentials"
echo "   cp .env.template .env"
echo "   vi .env"

# ============================================
# 9. Create Deployment Script
# ============================================
echo ""
echo "📜 Step 9: Creating deployment script..."

cat > /var/www/codexdominion/deploy.sh << 'DEPLOY_SCRIPT'
#!/bin/bash

echo "🚀 Deploying CodexDominion..."

cd /var/www/codexdominion

# Pull latest code (if using git)
if [ -d ".git" ]; then
    echo "📥 Pulling latest code..."
    git fetch --all
    git reset --hard origin/main
fi

# Pull latest Docker images
echo "🐳 Pulling Docker images..."
docker compose -f docker-compose.production.yml pull

# Stop services
echo "⏸️ Stopping services..."
docker compose -f docker-compose.production.yml down

# Start services
echo "▶️ Starting services..."
docker compose -f docker-compose.production.yml up -d

# Wait for services to start
echo "⏳ Waiting for services..."
sleep 10

# Show status
echo "📊 Service status:"
docker compose -f docker-compose.production.yml ps

# Cleanup
echo "🧹 Cleaning up..."
docker system prune -af --volumes

echo "✅ Deployment complete!"
DEPLOY_SCRIPT

chmod +x /var/www/codexdominion/deploy.sh

echo "✅ Deployment script created"

# ============================================
# 10. Create Backup Script
# ============================================
echo ""
echo "💾 Step 10: Creating backup script..."

cat > /var/www/codexdominion/backup.sh << 'BACKUP_SCRIPT'
#!/bin/bash

BACKUP_DIR="/var/www/codexdominion/backups"
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="backup-${DATE}.tar.gz"

echo "💾 Creating backup: ${BACKUP_FILE}"

# Create backup
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" \
    --exclude='backups' \
    --exclude='logs/*.log' \
    --exclude='node_modules' \
    /var/www/codexdominion

# Keep only last 7 backups
cd "${BACKUP_DIR}"
ls -t | tail -n +8 | xargs -r rm

echo "✅ Backup complete: ${BACKUP_FILE}"
BACKUP_SCRIPT

chmod +x /var/www/codexdominion/backup.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /var/www/codexdominion/backup.sh") | crontab -

echo "✅ Backup script created (runs daily at 2 AM)"

# ============================================
# Summary
# ============================================
echo ""
echo "=================================================="
echo "🎉 IONOS Server Setup Complete!"
echo "=================================================="
echo ""
echo "✅ Installed:"
echo "   - Docker & Docker Compose"
echo "   - Nginx web server"
echo "   - Certbot for SSL"
echo "   - Firewall (UFW)"
echo "   - Fail2ban"
echo ""
echo "📁 Application directory: /var/www/codexdominion"
echo ""
echo "🔥 Next steps:"
echo "   1. Configure DNS in Google Domains (wait for propagation)"
echo "   2. Edit .env file: cp .env.template .env && vi .env"
echo "   3. Get SSL certificates:"
echo "      certbot --nginx -d codexdominion.app -d www.codexdominion.app -d dashboard.codexdominion.app -d api.codexdominion.app -d stockanalytics.codexdominion.app"
echo "   4. Deploy application:"
echo "      cd /var/www/codexdominion"
echo "      ./deploy.sh"
echo ""
echo "📊 Useful commands:"
echo "   - View logs: docker compose -f docker-compose.production.yml logs -f"
echo "   - Restart: docker compose -f docker-compose.production.yml restart"
echo "   - Status: docker compose -f docker-compose.production.yml ps"
echo ""
echo "🔒 Security notes:"
echo "   - SSH access: Port 22 (consider changing)"
echo "   - Firewall enabled with UFW"
echo "   - Fail2ban configured"
echo "   - Update .env with strong passwords!"
echo ""
echo "=================================================="
