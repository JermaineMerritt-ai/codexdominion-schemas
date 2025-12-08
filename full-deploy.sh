# CodexDominion Full System Deployment Script
# Run this script after adding DNS records for subdomains
# Usage: ./full-deploy.sh

#!/bin/bash
set -e

echo "========================================="
echo "  CodexDominion Full System Deployment"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
DOMAIN="codexdominion.app"
SERVER_IP="74.208.123.158"
DEPLOY_DIR="/var/www/codexdominion.app"
API_PORT=8000
DASHBOARD_PORT=8501
MONITORING_PORT=9090
FRONTEND_PORT=3000

echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Check DNS records
echo -e "${YELLOW}Step 1: Verifying DNS configuration...${NC}"
SUBDOMAINS=("api" "dashboard" "monitoring")
DNS_OK=true

for sub in "${SUBDOMAINS[@]}"; do
    if host $sub.$DOMAIN > /dev/null 2>&1; then
        echo -e "${GREEN}✓ $sub.$DOMAIN DNS configured${NC}"
    else
        echo -e "${RED}✗ $sub.$DOMAIN DNS not found${NC}"
        DNS_OK=false
    fi
done

if [ "$DNS_OK" = false ]; then
    echo ""
    echo -e "${RED}ERROR: Not all DNS records are configured!${NC}"
    echo "Please add the following A records and wait 10-15 minutes:"
    echo "  api.$DOMAIN        -> $SERVER_IP"
    echo "  dashboard.$DOMAIN  -> $SERVER_IP"
    echo "  monitoring.$DOMAIN -> $SERVER_IP"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Installing dependencies...${NC}"

# Update system
apt update -qq

# Install required packages
PACKAGES=("python3" "python3-pip" "python3-venv" "nodejs" "npm" "certbot" "python3-certbot-nginx" "nginx")
for pkg in "${PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $pkg "; then
        echo "Installing $pkg..."
        apt install -y $pkg -qq
    fi
done

echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""
echo -e "${YELLOW}Step 3: Creating nginx configurations...${NC}"

# API subdomain
cat > /etc/nginx/sites-available/api.$DOMAIN << 'EOFAPI'
server {
    listen 80;
    server_name api.codexdominion.app;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # CORS
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
    }
}
EOFAPI

# Dashboard subdomain
cat > /etc/nginx/sites-available/dashboard.$DOMAIN << 'EOFDASH'
server {
    listen 80;
    server_name dashboard.codexdominion.app;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOFDASH

# Monitoring subdomain
cat > /etc/nginx/sites-available/monitoring.$DOMAIN << 'EOFMON'
server {
    listen 80;
    server_name monitoring.codexdominion.app;

    location / {
        proxy_pass http://localhost:9090;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOFMON

# Enable sites
ln -sf /etc/nginx/sites-available/api.$DOMAIN /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/dashboard.$DOMAIN /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/monitoring.$DOMAIN /etc/nginx/sites-enabled/

echo -e "${GREEN}✓ Nginx configurations created${NC}"

echo ""
echo -e "${YELLOW}Step 4: Testing nginx configuration...${NC}"
if nginx -t; then
    echo -e "${GREEN}✓ Nginx configuration valid${NC}"
    systemctl reload nginx
else
    echo -e "${RED}✗ Nginx configuration error${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 5: Obtaining SSL certificates...${NC}"
certbot --nginx \
    -d api.$DOMAIN \
    -d dashboard.$DOMAIN \
    -d monitoring.$DOMAIN \
    --non-interactive \
    --agree-tos \
    --email admin@$DOMAIN \
    --redirect

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL certificates configured${NC}"
else
    echo -e "${YELLOW}⚠ SSL setup had issues - may need manual intervention${NC}"
fi

echo ""
echo -e "${YELLOW}Step 6: Setting up application directory...${NC}"
mkdir -p $DEPLOY_DIR/{api,frontend,dashboard,monitoring,logs}
chown -R www-data:www-data $DEPLOY_DIR
echo -e "${GREEN}✓ Directory structure created${NC}"

echo ""
echo -e "${YELLOW}Step 7: Setting up Python environment for API...${NC}"
cd $DEPLOY_DIR/api
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    echo -e "${GREEN}✓ Python virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Python virtual environment exists${NC}"
fi

echo ""
echo -e "${YELLOW}Step 8: Creating systemd services...${NC}"

# API Service
cat > /etc/systemd/system/codex-api.service << EOFSERVICE
[Unit]
Description=CodexDominion API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$DEPLOY_DIR/api
Environment="PATH=$DEPLOY_DIR/api/venv/bin"
ExecStart=$DEPLOY_DIR/api/venv/bin/uvicorn main:app --host 127.0.0.1 --port $API_PORT --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOFSERVICE

# Frontend Service
cat > /etc/systemd/system/codex-frontend.service << EOFSERVICE
[Unit]
Description=CodexDominion Frontend Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$DEPLOY_DIR/frontend
Environment="NODE_ENV=production"
Environment="PORT=$FRONTEND_PORT"
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOFSERVICE

systemctl daemon-reload
echo -e "${GREEN}✓ Systemd services created${NC}"

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Your CodexDominion system is configured:"
echo ""
echo "  🌐 Main Site:    https://$DOMAIN"
echo "  🌐 WWW:          https://www.$DOMAIN"
echo "  🔌 API:          https://api.$DOMAIN"
echo "  📊 Dashboard:    https://dashboard.$DOMAIN"
echo "  📈 Monitoring:   https://monitoring.$DOMAIN"
echo ""
echo "SSL certificates expire on: $(date -d '+90 days' +'%B %d, %Y')"
echo "Auto-renewal is configured via certbot timer"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Deploy your API code to $DEPLOY_DIR/api/"
echo "  2. Install API requirements: source $DEPLOY_DIR/api/venv/bin/activate && pip install -r requirements.txt"
echo "  3. Deploy your frontend build to $DEPLOY_DIR/frontend/"
echo "  4. Start services:"
echo "     systemctl start codex-api"
echo "     systemctl enable codex-api"
echo "     systemctl start codex-frontend"
echo "     systemctl enable codex-frontend"
echo "  5. Check service status:"
echo "     systemctl status codex-api"
echo "     systemctl status codex-frontend"
echo ""
echo "  View logs:"
echo "     journalctl -u codex-api -f"
echo "     journalctl -u codex-frontend -f"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
