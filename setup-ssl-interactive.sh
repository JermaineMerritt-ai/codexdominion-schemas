#!/bin/bash
# Complete SSL Setup for CodexDominion.app

echo "🔒 SSL Setup for CodexDominion.app"
echo "===================================="
echo ""

# 1. Check DNS
echo "1️⃣ Checking DNS configuration..."
DOMAIN_IP=$(dig +short codexdominion.app | tail -1)
SERVER_IP=$(curl -s ifconfig.me)

echo "Domain points to: $DOMAIN_IP"
echo "Server IP is: $SERVER_IP"

if [ "$DOMAIN_IP" != "$SERVER_IP" ]; then
    echo "⚠️  WARNING: DNS mismatch!"
    echo "Please configure your DNS:"
    echo "  A record: codexdominion.app → $SERVER_IP"
    echo "  A record: www.codexdominion.app → $SERVER_IP"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# 2. Install certbot if needed
echo "2️⃣ Checking certbot installation..."
if ! command -v certbot &> /dev/null; then
    echo "Installing certbot..."
    apt update
    apt install -y certbot python3-certbot-nginx
    echo "✅ Certbot installed"
else
    echo "✅ Certbot already installed"
fi
echo ""

# 3. Get email
echo "3️⃣ Email for SSL certificate:"
read -p "Enter your email (for urgent renewal and security notices): " EMAIL

if [ -z "$EMAIL" ]; then
    echo "❌ Email is required!"
    exit 1
fi
echo ""

# 4. Obtain certificate
echo "4️⃣ Obtaining SSL certificate..."
certbot --nginx \
    -d codexdominion.app \
    -d www.codexdominion.app \
    --non-interactive \
    --agree-tos \
    -m "$EMAIL" \
    --redirect

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate obtained and configured!"
else
    echo "❌ Failed to obtain SSL certificate"
    echo ""
    echo "Common issues:"
    echo "1. DNS not pointing to this server"
    echo "2. Port 80/443 blocked by firewall"
    echo "3. Domain not yet propagated"
    exit 1
fi
echo ""

# 5. Test renewal
echo "5️⃣ Testing SSL auto-renewal..."
certbot renew --dry-run
echo ""

# 6. Final test
echo "6️⃣ Testing HTTPS access..."
curl -I https://codexdominion.app 2>&1 | head -10
echo ""

echo "===================================="
echo "🎉 SSL SETUP COMPLETE!"
echo ""
echo "Your site is now live at:"
echo "  🔒 https://codexdominion.app"
echo "  🔒 https://www.codexdominion.app"
echo ""
echo "Certificate will auto-renew every 60 days"
echo "===================================="
