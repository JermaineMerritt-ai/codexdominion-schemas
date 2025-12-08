#!/bin/bash
# Codex Dominion - Frontend-Only IONOS Deployment
# Backend hosted on Azure App Service
# Generated: 2025-12-06 22:22:44 UTC

set -e

echo "🔥 Codex Dominion - Frontend Deployment to IONOS"
echo "Backend: http://codex-backend.eastus.azurecontainer.io:8001"
echo "=================================================="
echo ""

DOMAIN="CodexDominion.app"
EMAIL="support@jermaineai.com"
AZURE_BACKEND="http://codex-backend.eastus.azurecontainer.io:8001"
APP_DIR="/opt/codex-dominion-frontend"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📦 Step 1: System Update"
echo "------------------------"
apt update && apt upgrade -y
echo -e "${GREEN}✅ System updated${NC}"
echo ""

echo "🐳 Step 2: Install Docker"
echo "-------------------------"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ Docker installed${NC}"
else
    echo -e "${GREEN}✅ Docker already installed${NC}"
fi

if ! docker compose version &> /dev/null; then
    if ! command -v docker-compose &> /dev/null; then
        echo "Installing docker-compose standalone..."
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
        echo -e "${GREEN}✅ Docker Compose installed${NC}"
    else
        echo -e "${GREEN}✅ Docker Compose already installed${NC}"
    fi
else
    echo -e "${GREEN}✅ Docker Compose already installed${NC}"
fi

docker --version
docker-compose --version 2>/dev/null || docker compose version
echo ""

echo "📁 Step 3: Create Application Directory"
echo "----------------------------------------"
mkdir -p $APP_DIR/nginx/logs $APP_DIR/ssl
cd $APP_DIR
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

echo "🌐 Step 4: Create Nginx Configuration"
echo "--------------------------------------"
cat > $APP_DIR/nginx/nginx.conf <<'EOFNGINX'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '\ - \ [\] "\" '
                    '\ \ "\" '
                    '"\"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    client_max_body_size 20M;

    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;

    limit_req_zone \ zone=general_limit:10m rate=30r/s;

    upstream frontend {
        server frontend:3001;
    }

    # HTTP - Redirect to HTTPS
    server {
        listen 80;
        server_name DOMAIN_PLACEHOLDER www.DOMAIN_PLACEHOLDER;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://\System.Management.Automation.Internal.Host.InternalHost\;
        }
    }

    # HTTPS - Frontend
    server {
        listen 443 ssl http2;
        server_name DOMAIN_PLACEHOLDER www.DOMAIN_PLACEHOLDER;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        add_header Strict-Transport-Security "max-age=31536000" always;

        limit_req zone=general_limit burst=20 nodelay;

        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host \System.Management.Automation.Internal.Host.InternalHost;
            proxy_set_header X-Real-IP \;
            proxy_set_header X-Forwarded-For \;
            proxy_set_header X-Forwarded-Proto \;
        }
    }
}
EOFNGINX

sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" $APP_DIR/nginx/nginx.conf
echo -e "${GREEN}✅ Nginx configuration created${NC}"
echo ""

echo "🐳 Step 5: Create Docker Compose Configuration"
echo "-----------------------------------------------"
cat > $APP_DIR/docker-compose.yml <<EOFDOCKER
services:
  frontend:
    image: jmerritt48/codex-dominion-frontend:2.0.0
    container_name: codex-frontend
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=$AZURE_BACKEND
      - NEXT_PUBLIC_SITE_URL=https://$DOMAIN
    ports:
      - "3001:3001"
    networks:
      - codex-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3001"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: codex-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - frontend
    networks:
      - codex-network

networks:
  codex-network:
    driver: bridge
EOFDOCKER

echo -e "${GREEN}✅ Docker Compose configuration created${NC}"
echo ""

echo "🔒 Step 6: Install Certbot and Obtain SSL Certificate"
echo "------------------------------------------------------"
apt install certbot -y

systemctl stop nginx 2>/dev/null || true
docker stop codex-nginx 2>/dev/null || true

certbot certonly --standalone \
    --preferred-challenges http \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $APP_DIR/ssl/
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $APP_DIR/ssl/
chmod 644 $APP_DIR/ssl/fullchain.pem
chmod 600 $APP_DIR/ssl/privkey.pem

echo -e "${GREEN}✅ SSL certificates configured${NC}"
echo ""

echo "🐳 Step 7: Pull Docker Images"
echo "------------------------------"
docker pull jmerritt48/codex-dominion-frontend:2.0.0
docker pull nginx:alpine
echo -e "${GREEN}✅ Docker images pulled${NC}"
echo ""

echo "🚀 Step 8: Start Services"
echo "---------------------------"
cd $APP_DIR
docker-compose up -d 2>/dev/null || docker compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 15

docker compose ps
echo ""

echo "🔄 Step 9: Configure Auto-Renewal"
echo "-----------------------------------"
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $APP_DIR/ssl/ && cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $APP_DIR/ssl/ && docker compose -f $APP_DIR/docker-compose.yml restart nginx") | crontab -

echo -e "${GREEN}✅ Auto-renewal configured${NC}"
echo ""

echo "🔥 Step 10: Configure Firewall"
echo "-------------------------------"
ufw --force enable
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw reload
echo -e "${GREEN}✅ Firewall configured${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}🔥 FRONTEND DEPLOYMENT COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "🌐 Your frontend is LIVE at:"
echo -e "   ${YELLOW}https://$DOMAIN${NC}"
echo ""
echo "🔗 Backend (Azure):"
echo -e "   ${YELLOW}$AZURE_BACKEND${NC}"
echo ""
echo "📊 Service Status:"
docker compose ps
echo ""
echo "📝 View logs:"
echo "   cd $APP_DIR && docker compose logs -f"
echo ""
echo "🔒 SSL auto-renews at 3:00 AM daily"
echo ""
echo "🔥 The frontend reigns on IONOS. Backend eternal in Azure."
