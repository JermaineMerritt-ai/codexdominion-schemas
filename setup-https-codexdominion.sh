#!/bin/bash
# =============================================================================
# CODEX DOMINION - HTTPS/SSL SETUP SCRIPT
# Domain: www.codexdominion.app
# Server: 74.208.123.158 (IONOS)
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="www.codexdominion.app"
EMAIL="admin@codexdominion.app"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   CODEX DOMINION HTTPS SETUP${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# =============================================================================
# Step 1: Check if running as root
# =============================================================================
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   exit 1
fi

# =============================================================================
# Step 2: Install required packages
# =============================================================================
echo -e "${YELLOW}Step 1: Installing required packages...${NC}"
apt-get update
apt-get install -y certbot python3-certbot-nginx nginx

echo -e "${GREEN}✓ Packages installed${NC}"
echo ""

# =============================================================================
# Step 3: Stop nginx temporarily
# =============================================================================
echo -e "${YELLOW}Step 2: Stopping nginx temporarily...${NC}"
systemctl stop nginx

echo -e "${GREEN}✓ Nginx stopped${NC}"
echo ""

# =============================================================================
# Step 4: Remove existing certificates (if any)
# =============================================================================
echo -e "${YELLOW}Step 3: Cleaning up old certificates...${NC}"
certbot delete --cert-name $DOMAIN --non-interactive 2>/dev/null || true

echo -e "${GREEN}✓ Old certificates removed${NC}"
echo ""

# =============================================================================
# Step 5: Request SSL certificate using standalone mode
# =============================================================================
echo -e "${YELLOW}Step 4: Requesting SSL certificate from Let's Encrypt...${NC}"
certbot certonly --standalone \
  -d $DOMAIN \
  --non-interactive \
  --agree-tos \
  --email $EMAIL \
  --preferred-challenges http

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL certificate obtained successfully${NC}"
else
    echo -e "${RED}✗ Failed to obtain SSL certificate${NC}"
    systemctl start nginx
    exit 1
fi
echo ""

# =============================================================================
# Step 6: Create nginx configuration with HTTPS
# =============================================================================
echo -e "${YELLOW}Step 5: Creating nginx configuration...${NC}"

cat > "$NGINX_AVAILABLE/codexdominion.app" << 'NGINXCONF'
# HTTP - Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name www.codexdominion.app;

    # Allow Let's Encrypt challenges
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS - Main site
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name www.codexdominion.app;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/www.codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.codexdominion.app/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Root directory
    root /var/www/codexdominion;
    index index.html index.htm;

    # Serve static files
    location / {
        try_files $uri $uri/ =404;
    }

    # Proxy to backend API if needed
    location /api/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Logs
    access_log /var/log/nginx/codexdominion_access.log;
    error_log /var/log/nginx/codexdominion_error.log;
}
NGINXCONF

echo -e "${GREEN}✓ Nginx configuration created${NC}"
echo ""

# =============================================================================
# Step 7: Enable the site
# =============================================================================
echo -e "${YELLOW}Step 6: Enabling site...${NC}"

# Create symlink if it doesn't exist
if [ ! -L "$NGINX_ENABLED/codexdominion.app" ]; then
    ln -s "$NGINX_AVAILABLE/codexdominion.app" "$NGINX_ENABLED/codexdominion.app"
fi

# Remove default site
rm -f "$NGINX_ENABLED/default"

echo -e "${GREEN}✓ Site enabled${NC}"
echo ""

# =============================================================================
# Step 8: Test nginx configuration
# =============================================================================
echo -e "${YELLOW}Step 7: Testing nginx configuration...${NC}"
nginx -t

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Nginx configuration is valid${NC}"
else
    echo -e "${RED}✗ Nginx configuration has errors${NC}"
    exit 1
fi
echo ""

# =============================================================================
# Step 9: Start nginx
# =============================================================================
echo -e "${YELLOW}Step 8: Starting nginx...${NC}"
systemctl start nginx
systemctl enable nginx

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Nginx started successfully${NC}"
else
    echo -e "${RED}✗ Failed to start nginx${NC}"
    exit 1
fi
echo ""

# =============================================================================
# Step 10: Configure automatic certificate renewal
# =============================================================================
echo -e "${YELLOW}Step 9: Setting up automatic certificate renewal...${NC}"

# Test renewal
certbot renew --dry-run

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Certificate renewal is configured${NC}"
else
    echo -e "${YELLOW}⚠ Certificate renewal test failed (may work in production)${NC}"
fi
echo ""

# =============================================================================
# Step 11: Configure firewall
# =============================================================================
echo -e "${YELLOW}Step 10: Configuring firewall...${NC}"

# Check if UFW is active
if command -v ufw &> /dev/null; then
    ufw allow 'Nginx Full'
    ufw delete allow 'Nginx HTTP' 2>/dev/null || true
    echo -e "${GREEN}✓ Firewall configured (UFW)${NC}"
elif command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
    echo -e "${GREEN}✓ Firewall configured (firewalld)${NC}"
else
    echo -e "${YELLOW}⚠ No firewall detected (UFW/firewalld)${NC}"
fi
echo ""

# =============================================================================
# Step 12: Verification
# =============================================================================
echo -e "${YELLOW}Step 11: Verifying setup...${NC}"
echo ""

# Check if nginx is running
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is not running${NC}"
fi

# Check if certificate exists
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo -e "${GREEN}✓ SSL certificate installed${NC}"

    # Show certificate expiry
    EXPIRY=$(openssl x509 -enddate -noout -in "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" | cut -d= -f2)
    echo -e "${BLUE}   Certificate expires: $EXPIRY${NC}"
else
    echo -e "${RED}✗ SSL certificate not found${NC}"
fi

# Check if port 443 is listening
if ss -tuln | grep -q ':443'; then
    echo -e "${GREEN}✓ Port 443 (HTTPS) is listening${NC}"
else
    echo -e "${RED}✗ Port 443 (HTTPS) is not listening${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   HTTPS SETUP COMPLETE!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Your site should now be accessible at:${NC}"
echo -e "${GREEN}   https://www.codexdominion.app${NC}"
echo ""
echo -e "${YELLOW}Certificate will auto-renew before expiry.${NC}"
echo -e "${YELLOW}Check renewal with: certbot renew --dry-run${NC}"
echo ""
