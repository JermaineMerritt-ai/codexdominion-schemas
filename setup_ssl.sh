#!/bin/bash
# 🔒 COSMIC DOMINION - SSL CERTIFICATE SETUP 🔒
# Automated SSL certificate management for aistorelab.com

echo "🔒 COSMIC DOMINION SSL SETUP 🔒"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="aistorelab.com"
EMAIL="admin@aistorelab.com"  # Change this to your email

echo -e "${BLUE}🌟 Starting SSL certificate setup for $DOMAIN...${NC}"

# 1. Install Certbot if not already installed
echo -e "${YELLOW}📦 Checking Certbot installation...${NC}"
if ! command -v certbot &> /dev/null; then
    echo -e "${YELLOW}⚙️ Installing Certbot...${NC}"
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
else
    echo -e "${GREEN}✅ Certbot is already installed${NC}"
fi

# 2. Check if Nginx is running
echo -e "${YELLOW}🌐 Checking Nginx status...${NC}"
if ! systemctl is-active --quiet nginx; then
    echo -e "${RED}❌ Nginx is not running. Starting Nginx...${NC}"
    sudo systemctl start nginx
    sudo systemctl enable nginx
else
    echo -e "${GREEN}✅ Nginx is running${NC}"
fi

# 3. Test Nginx configuration
echo -e "${YELLOW}🔧 Testing Nginx configuration...${NC}"
if sudo nginx -t; then
    echo -e "${GREEN}✅ Nginx configuration is valid${NC}"
else
    echo -e "${RED}❌ Nginx configuration has errors. Please fix before continuing.${NC}"
    exit 1
fi

# 4. Check if certificates already exist
echo -e "${YELLOW}🔍 Checking existing certificates...${NC}"
if sudo certbot certificates | grep -q "$DOMAIN"; then
    echo -e "${YELLOW}⚠️ Certificates for $DOMAIN already exist${NC}"
    echo -e "${BLUE}📋 Current certificate status:${NC}"
    sudo certbot certificates | grep -A 5 "$DOMAIN"

    read -p "Do you want to renew the certificates? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🔄 Renewing certificates...${NC}"
        sudo certbot renew --nginx
    fi
else
    echo -e "${YELLOW}🆕 No existing certificates found. Creating new ones...${NC}"

    # 5. Obtain SSL certificates
    echo -e "${YELLOW}🔒 Obtaining SSL certificates for $DOMAIN and www.$DOMAIN...${NC}"

    # Interactive certificate request
    sudo certbot --nginx \
        -d "$DOMAIN" \
        -d "www.$DOMAIN" \
        --email "$EMAIL" \
        --agree-tos \
        --no-eff-email \
        --redirect

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SSL certificates obtained successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to obtain SSL certificates${NC}"
        exit 1
    fi
fi

# 6. Set up automatic renewal
echo -e "${YELLOW}🔄 Setting up automatic certificate renewal...${NC}"

# Enable and start certbot timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Check timer status
if systemctl is-active --quiet certbot.timer; then
    echo -e "${GREEN}✅ Certbot timer is active${NC}"
else
    echo -e "${RED}❌ Failed to start certbot timer${NC}"
fi

# 7. Create renewal test
echo -e "${YELLOW}🧪 Testing certificate renewal process...${NC}"
sudo certbot renew --dry-run

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Certificate renewal test passed${NC}"
else
    echo -e "${YELLOW}⚠️ Certificate renewal test failed - check configuration${NC}"
fi

# 8. Set up renewal hook for Nginx reload
echo -e "${YELLOW}🔧 Setting up Nginx reload hook...${NC}"
sudo mkdir -p /etc/letsencrypt/renewal-hooks/post

cat << EOF | sudo tee /etc/letsencrypt/renewal-hooks/post/nginx-reload.sh
#!/bin/bash
# Reload Nginx after certificate renewal
systemctl reload nginx
echo "🔒 Nginx reloaded after SSL certificate renewal"
EOF

sudo chmod +x /etc/letsencrypt/renewal-hooks/post/nginx-reload.sh

# 9. Display certificate information
echo -e "${BLUE}📋 Certificate Information:${NC}"
sudo certbot certificates

# 10. Test HTTPS
echo -e "${YELLOW}🔍 Testing HTTPS connectivity...${NC}"
if curl -s -I "https://$DOMAIN" | grep -q "HTTP"; then
    echo -e "${GREEN}✅ HTTPS is working for $DOMAIN${NC}"
else
    echo -e "${YELLOW}⚠️ HTTPS test failed for $DOMAIN${NC}"
fi

if curl -s -I "https://www.$DOMAIN" | grep -q "HTTP"; then
    echo -e "${GREEN}✅ HTTPS is working for www.$DOMAIN${NC}"
else
    echo -e "${YELLOW}⚠️ HTTPS test failed for www.$DOMAIN${NC}"
fi

# 11. Create SSL monitoring script
echo -e "${YELLOW}📊 Creating SSL monitoring script...${NC}"
cat << 'EOF' | sudo tee /usr/local/bin/cosmic-ssl-status
#!/bin/bash
echo "🔒 COSMIC DOMINION SSL STATUS 🔒"
echo "================================"
echo ""

# Check certificate expiry
echo "📅 Certificate Expiry Status:"
sudo certbot certificates | grep -E "(Certificate Name|Expiry Date)" | while read line; do
    echo "   $line"
done

echo ""

# Check timer status
echo "🔄 Auto-renewal Status:"
if systemctl is-active --quiet certbot.timer; then
    echo "   ✅ Certbot timer: ACTIVE"
    echo "   📅 Next run: $(systemctl list-timers certbot.timer --no-pager | grep certbot.timer | awk '{print $1, $2}')"
else
    echo "   ❌ Certbot timer: INACTIVE"
fi

echo ""

# Check SSL grades (requires external tool)
echo "🏆 SSL Test Results:"
echo "   🌐 Test manually at: https://www.ssllabs.com/ssltest/analyze.html?d=aistorelab.com"

echo ""
echo "🔧 Management Commands:"
echo "   Renew: sudo certbot renew"
echo "   Test renewal: sudo certbot renew --dry-run"
echo "   List certificates: sudo certbot certificates"
EOF

sudo chmod +x /usr/local/bin/cosmic-ssl-status

# 12. Final status display
echo ""
echo -e "${GREEN}✨ COSMIC DOMINION SSL SETUP COMPLETE! ✨${NC}"
echo ""
echo -e "${PURPLE}🔒 SSL Certificate Status:${NC}"
/usr/local/bin/cosmic-ssl-status

echo ""
echo -e "${BLUE}🌍 Your Cosmic Domain is now secured with SSL:${NC}"
echo -e "${GREEN}   🔒 https://$DOMAIN${NC}"
echo -e "${GREEN}   🔒 https://www.$DOMAIN${NC}"
echo ""
echo -e "${YELLOW}⚙️ SSL Management Commands:${NC}"
echo -e "   Check status: ${GREEN}cosmic-ssl-status${NC}"
echo -e "   Manual renewal: ${GREEN}sudo certbot renew${NC}"
echo -e "   Test renewal: ${GREEN}sudo certbot renew --dry-run${NC}"
echo ""
echo -e "${RED}🔥 DIGITAL SOVEREIGNTY IS NOW ENCRYPTED! 🔥${NC}"
