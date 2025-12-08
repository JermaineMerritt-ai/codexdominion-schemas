# Codex Dominion - IONOS VPS Deployment Generator
# This script generates the deployment configuration for your IONOS VPS

Write-Host "🔥 Codex Dominion - IONOS VPS Deployment Generator" -ForegroundColor Cyan
Write-Host "====================================================`n" -ForegroundColor Cyan

# Get configuration from user
$DOMAIN = Read-Host "Enter your domain name (e.g., codex-dominion.com)"
$EMAIL = Read-Host "Enter your email for Let's Encrypt SSL notifications"
$SERVER_IP = Read-Host "Enter your IONOS VPS IP address"

if ([string]::IsNullOrWhiteSpace($DOMAIN) -or [string]::IsNullOrWhiteSpace($EMAIL) -or [string]::IsNullOrWhiteSpace($SERVER_IP)) {
    Write-Host "❌ All fields are required!" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Domain: $DOMAIN" -ForegroundColor Gray
Write-Host "   API Domain: api.$DOMAIN" -ForegroundColor Gray
Write-Host "   Email: $EMAIL" -ForegroundColor Gray
Write-Host "   Server IP: $SERVER_IP" -ForegroundColor Gray
Write-Host ""

$confirm = Read-Host "Generate deployment script? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Cancelled" -ForegroundColor Red
    exit
}

# Generate the deployment script for the VPS
$deployScript = @"
#!/bin/bash
# Codex Dominion - IONOS VPS Deployment Script
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC")
# Domain: $DOMAIN
# Server: $SERVER_IP

set -e  # Exit on any error

echo "🔥 Codex Dominion - Production Deployment"
echo "=========================================="
echo ""

# Configuration
DOMAIN="$DOMAIN"
EMAIL="$EMAIL"
APP_DIR="/opt/codex-dominion"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "📦 Step 1: System Update"
echo "------------------------"
apt update && apt upgrade -y
echo -e "`${GREEN}✅ System updated`${NC}"
echo ""

echo "🐳 Step 2: Install Docker"
echo "-------------------------"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo -e "`${GREEN}✅ Docker installed`${NC}"
else
    echo -e "`${GREEN}✅ Docker already installed`${NC}"
fi

if ! docker compose version &> /dev/null; then
    apt install docker-compose-plugin -y
    echo -e "`${GREEN}✅ Docker Compose installed`${NC}"
else
    echo -e "`${GREEN}✅ Docker Compose already installed`${NC}"
fi

docker --version
docker compose version
echo ""

echo "📁 Step 3: Create Application Directory"
echo "----------------------------------------"
mkdir -p `$APP_DIR
cd `$APP_DIR
mkdir -p ssl nginx/logs data logs backups
echo -e "`${GREEN}✅ Directories created`${NC}"
echo ""

echo "🔐 Step 4: Generate Security Secrets"
echo "-------------------------------------"
SECRET_KEY=\$(openssl rand -hex 32)
JWT_SECRET=\$(openssl rand -hex 32)
API_KEY=\$(openssl rand -hex 32)
REDIS_PASSWORD=\$(openssl rand -hex 16)
echo -e "`${GREEN}✅ Secrets generated`${NC}"
echo ""

echo "📝 Step 5: Create Environment Configuration"
echo "--------------------------------------------"
cat > `$APP_DIR/.env <<EOFENV
# Codex Dominion Production Environment
# Generated: \$(date)

NODE_ENV=production
ENVIRONMENT=production

# API Configuration
NEXT_PUBLIC_API_URL=https://api.`$DOMAIN

# Database (SQLite - upgrade to PostgreSQL for production scale)
DATABASE_URL=sqlite:///./data/codex_dominion.db

# Redis Configuration
REDIS_URL=redis://:`\${REDIS_PASSWORD}@redis:6379/0
REDIS_PASSWORD=`\${REDIS_PASSWORD}

# Security Keys
SECRET_KEY=`\${SECRET_KEY}
JWT_SECRET=`\${JWT_SECRET}
API_KEY=`\${API_KEY}

# JWT Configuration
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=https://`$DOMAIN,https://www.`$DOMAIN

# SSL Configuration
SSL_CERT_PATH=/etc/nginx/ssl/fullchain.pem
SSL_KEY_PATH=/etc/nginx/ssl/privkey.pem
EOFENV

chmod 600 `$APP_DIR/.env
echo -e "`${GREEN}✅ Environment file created`${NC}"
echo ""

echo "🌐 Step 6: Create Nginx Configuration"
echo "--------------------------------------"
cat > `$APP_DIR/nginx/nginx.conf <<'EOFNGINX'
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

    log_format main '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                    '\$status \$body_bytes_sent "\$http_referer" '
                    '"\$http_user_agent"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    client_max_body_size 20M;

    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;

    limit_req_zone \$binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone \$binary_remote_addr zone=general_limit:10m rate=30r/s;

    upstream frontend {
        server frontend:3001;
    }

    upstream backend {
        server backend:8001;
    }

    # HTTP - Redirect to HTTPS
    server {
        listen 80;
        server_name DOMAIN_PLACEHOLDER www.DOMAIN_PLACEHOLDER api.DOMAIN_PLACEHOLDER;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://\$host\$request_uri;
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
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }

    # HTTPS - Backend API
    server {
        listen 443 ssl http2;
        server_name api.DOMAIN_PLACEHOLDER;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header Access-Control-Allow-Origin "https://DOMAIN_PLACEHOLDER" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;

        limit_req zone=api_limit burst=5 nodelay;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOFNGINX

# Replace domain placeholder
sed -i "s/DOMAIN_PLACEHOLDER/`$DOMAIN/g" `$APP_DIR/nginx/nginx.conf
echo -e "`${GREEN}✅ Nginx configuration created`${NC}"
echo ""

echo "🐳 Step 7: Create Docker Compose Configuration"
echo "-----------------------------------------------"
cat > `$APP_DIR/docker-compose.yml <<'EOFDOCKER'
services:
  frontend:
    image: jmerritt48/codex-dominion-frontend:2.0.0
    container_name: codex-frontend
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=https://api.DOMAIN_PLACEHOLDER
    ports:
      - "3001:3001"
    networks:
      - codex-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3001"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    image: jmerritt48/codex-dominion-backend:2.0.0
    container_name: codex-backend
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8001:8001"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - codex-network
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: codex-redis
    restart: unless-stopped
    command: redis-server --requirepass \${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - codex-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

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
      - backend
    networks:
      - codex-network

networks:
  codex-network:
    driver: bridge

volumes:
  redis-data:
EOFDOCKER

sed -i "s/DOMAIN_PLACEHOLDER/`$DOMAIN/g" `$APP_DIR/docker-compose.yml
echo -e "`${GREEN}✅ Docker Compose configuration created`${NC}"
echo ""

echo "🔒 Step 8: Install Certbot and Obtain SSL Certificate"
echo "------------------------------------------------------"
apt install certbot -y

# Stop nginx if running
systemctl stop nginx 2>/dev/null || true
docker stop codex-nginx 2>/dev/null || true

# Obtain certificate
certbot certonly --standalone \
    --preferred-challenges http \
    --email `$EMAIL \
    --agree-tos \
    --no-eff-email \
    -d `$DOMAIN \
    -d www.`$DOMAIN \
    -d api.`$DOMAIN

# Copy certificates
cp /etc/letsencrypt/live/`$DOMAIN/fullchain.pem `$APP_DIR/ssl/
cp /etc/letsencrypt/live/`$DOMAIN/privkey.pem `$APP_DIR/ssl/
chmod 644 `$APP_DIR/ssl/fullchain.pem
chmod 600 `$APP_DIR/ssl/privkey.pem

echo -e "`${GREEN}✅ SSL certificates obtained and configured`${NC}"
echo ""

echo "🐳 Step 9: Pull Docker Images"
echo "------------------------------"
docker pull jmerritt48/codex-dominion-frontend:2.0.0
docker pull jmerritt48/codex-dominion-backend:2.0.0
docker pull redis:7-alpine
docker pull nginx:alpine
echo -e "`${GREEN}✅ Docker images pulled`${NC}"
echo ""

echo "🚀 Step 10: Start Services"
echo "---------------------------"
cd `$APP_DIR
docker compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 15

docker compose ps
echo ""

echo "🔄 Step 11: Configure Auto-Renewal"
echo "-----------------------------------"
# SSL renewal cron
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/`$DOMAIN/fullchain.pem `$APP_DIR/ssl/ && cp /etc/letsencrypt/live/`$DOMAIN/privkey.pem `$APP_DIR/ssl/ && docker compose -f `$APP_DIR/docker-compose.yml restart nginx") | crontab -

# Backup script
cat > `$APP_DIR/backup.sh <<'EOFBACKUP'
#!/bin/bash
BACKUP_DIR="/opt/codex-dominion/backups"
DATE=\$(date +%Y%m%d_%H%M%S)
mkdir -p \$BACKUP_DIR
docker exec codex-backend cp /app/data/codex_dominion.db /app/data/backup_\$DATE.db 2>/dev/null || true
find `$APP_DIR/data -name "backup_*.db" -mtime +7 -delete
echo "Backup completed: \$DATE"
EOFBACKUP

chmod +x `$APP_DIR/backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * `$APP_DIR/backup.sh >> `$APP_DIR/logs/backup.log 2>&1") | crontab -

echo -e "`${GREEN}✅ Auto-renewal configured`${NC}"
echo ""

echo "🔥 Step 12: Configure Firewall"
echo "-------------------------------"
ufw --force enable
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw reload
echo -e "`${GREEN}✅ Firewall configured`${NC}"
echo ""

echo "=========================================="
echo -e "`${GREEN}🔥 DEPLOYMENT COMPLETE!`${NC}"
echo "=========================================="
echo ""
echo "🌐 Your Codex Dominion is LIVE at:"
echo -e "   `${YELLOW}https://`$DOMAIN`${NC}"
echo -e "   `${YELLOW}https://api.`$DOMAIN`${NC}"
echo ""
echo "📊 Check service status:"
echo "   cd `$APP_DIR && docker compose ps"
echo ""
echo "📝 View logs:"
echo "   docker compose logs -f"
echo ""
echo "🔐 Secrets stored in: `$APP_DIR/.env"
echo "💾 Daily backups at 2:00 AM"
echo "🔄 SSL auto-renews at 3:00 AM"
echo ""
echo "🔥 The flame burns eternal. Codex Dominion reigns supreme."
"@

# Save the deployment script
$scriptPath = "ionos-vps-deploy.sh"
$deployScript | Out-File -FilePath $scriptPath -Encoding UTF8

# Convert line endings to Unix (LF)
(Get-Content $scriptPath -Raw) -replace "`r`n", "`n" | Set-Content $scriptPath -NoNewline

Write-Host "`n✅ Deployment script generated: $scriptPath" -ForegroundColor Green
Write-Host ""

# Display instructions
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📋 DEPLOYMENT INSTRUCTIONS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "⚠️  CRITICAL: Configure DNS FIRST (before running script)" -ForegroundColor Yellow
Write-Host "--------------------------------------------------------" -ForegroundColor Gray
Write-Host "Login to IONOS Domain Control Panel and add:" -ForegroundColor White
Write-Host ""
Write-Host "  Type    Host    Value           TTL" -ForegroundColor Gray
Write-Host "  ----    ----    -----           ---" -ForegroundColor Gray
Write-Host "  A       @       $SERVER_IP      3600" -ForegroundColor Cyan
Write-Host "  A       www     $SERVER_IP      3600" -ForegroundColor Cyan
Write-Host "  A       api     $SERVER_IP      3600" -ForegroundColor Cyan
Write-Host ""
Write-Host "Wait 5-30 minutes for DNS propagation, verify with:" -ForegroundColor Yellow
Write-Host "  nslookup $DOMAIN" -ForegroundColor Gray
Write-Host "  nslookup api.$DOMAIN`n" -ForegroundColor Gray

Write-Host "Step 1: Copy script to VPS" -ForegroundColor Yellow
Write-Host "----------------------------" -ForegroundColor Gray
Write-Host "  scp ionos-vps-deploy.sh root@${SERVER_IP}:/root/`n" -ForegroundColor Cyan

Write-Host "Step 2: SSH to VPS" -ForegroundColor Yellow
Write-Host "-------------------" -ForegroundColor Gray
Write-Host "  ssh root@$SERVER_IP`n" -ForegroundColor Cyan

Write-Host "Step 3: Run deployment" -ForegroundColor Yellow
Write-Host "----------------------" -ForegroundColor Gray
Write-Host "  chmod +x /root/ionos-vps-deploy.sh" -ForegroundColor Cyan
Write-Host "  /root/ionos-vps-deploy.sh`n" -ForegroundColor Cyan

Write-Host "Step 4: Verify" -ForegroundColor Yellow
Write-Host "--------------" -ForegroundColor Gray
Write-Host "  https://$DOMAIN" -ForegroundColor Cyan
Write-Host "  https://api.$DOMAIN/health`n" -ForegroundColor Cyan

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔥 The empire deploys. Eternal flame ignites." -ForegroundColor Magenta
