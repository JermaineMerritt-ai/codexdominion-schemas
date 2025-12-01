#!/bin/bash
# 🔒 IONOS SSL CERTIFICATE DEPLOYMENT SCRIPT
# Deploy and verify SSL certificates for Codex Dominion on IONOS server

set -e  # Exit on any error

echo "🔒 IONOS SSL CERTIFICATE DEPLOYMENT"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="aistorelab.com"
EMAIL="admin@aistorelab.com"
NGINX_CONF_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"

echo -e "${BLUE}🌟 Starting SSL certificate deployment for $DOMAIN on IONOS server...${NC}"

# Function to check if running as root or with sudo
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${GREEN}✅ Running with root privileges${NC}"
    elif sudo -n true 2>/dev/null; then
        echo -e "${GREEN}✅ Sudo access available${NC}"
    else
        echo -e "${RED}❌ This script requires sudo privileges${NC}"
        exit 1
    fi
}

# Function to install required packages
install_dependencies() {
    echo -e "${YELLOW}📦 Installing SSL certificate dependencies...${NC}"

    # Update package list
    sudo apt update

    # Install required packages
    sudo apt install -y \
        nginx \
        certbot \
        python3-certbot-nginx \
        openssl \
        curl \
        cron

    echo -e "${GREEN}✅ Dependencies installed${NC}"
}

# Function to setup nginx configuration
setup_nginx() {
    echo -e "${YELLOW}🌐 Setting up Nginx configuration...${NC}"

    # Create nginx config for domain
    sudo tee "$NGINX_CONF_DIR/aistorelab.com" > /dev/null << 'EOF'
# HTTP server for Let's Encrypt verification
server {
    listen 80;
    server_name aistorelab.com www.aistorelab.com;

    # Let's Encrypt challenge location
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect all other requests to HTTPS (will be added by certbot)
    location / {
        return 301 https://aistorelab.com$request_uri;
    }
}
EOF

    # Enable the site
    sudo ln -sf "$NGINX_CONF_DIR/aistorelab.com" "$NGINX_ENABLED_DIR/"

    # Create web root directory
    sudo mkdir -p /var/www/html
    sudo chown -R www-data:www-data /var/www/html

    # Test nginx configuration
    if sudo nginx -t; then
        echo -e "${GREEN}✅ Nginx configuration is valid${NC}"
        sudo systemctl reload nginx
    else
        echo -e "${RED}❌ Nginx configuration error${NC}"
        exit 1
    fi
}

# Function to obtain SSL certificates
obtain_certificates() {
    echo -e "${YELLOW}🔒 Obtaining SSL certificates...${NC}"

    # Check if certificates already exist
    if sudo certbot certificates 2>/dev/null | grep -q "$DOMAIN"; then
        echo -e "${YELLOW}⚠️ Certificates for $DOMAIN already exist${NC}"

        # Show existing certificates
        echo -e "${BLUE}📋 Current certificates:${NC}"
        sudo certbot certificates

        # Test renewal
        echo -e "${YELLOW}🧪 Testing certificate renewal...${NC}"
        if sudo certbot renew --dry-run; then
            echo -e "${GREEN}✅ Certificate renewal test passed${NC}"
        else
            echo -e "${RED}❌ Certificate renewal test failed${NC}"
        fi
    else
        echo -e "${YELLOW}🆕 Obtaining new SSL certificates...${NC}"

        # Obtain certificates using nginx plugin
        sudo certbot --nginx \
            -d "$DOMAIN" \
            -d "www.$DOMAIN" \
            --email "$EMAIL" \
            --agree-tos \
            --no-eff-email \
            --redirect \
            --non-interactive

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ SSL certificates obtained successfully!${NC}"
        else
            echo -e "${RED}❌ Failed to obtain SSL certificates${NC}"
            exit 1
        fi
    fi
}

# Function to setup automatic renewal
setup_auto_renewal() {
    echo -e "${YELLOW}🔄 Setting up automatic certificate renewal...${NC}"

    # Enable and start certbot timer (systemd)
    sudo systemctl enable certbot.timer
    sudo systemctl start certbot.timer

    # Verify timer is active
    if systemctl is-active --quiet certbot.timer; then
        echo -e "${GREEN}✅ Certbot timer is active${NC}"

        # Show next renewal time
        echo -e "${CYAN}📅 Next renewal check:${NC}"
        systemctl list-timers certbot.timer --no-pager | grep certbot.timer
    else
        echo -e "${RED}❌ Failed to activate certbot timer${NC}"
    fi

    # Create renewal hook for nginx reload
    sudo mkdir -p /etc/letsencrypt/renewal-hooks/post

    sudo tee /etc/letsencrypt/renewal-hooks/post/nginx-reload.sh > /dev/null << 'EOF'
#!/bin/bash
# Reload Nginx after certificate renewal
systemctl reload nginx
echo "$(date): 🔒 Nginx reloaded after SSL certificate renewal" >> /var/log/certbot-renewal.log
EOF

    sudo chmod +x /etc/letsencrypt/renewal-hooks/post/nginx-reload.sh
    echo -e "${GREEN}✅ Renewal hooks configured${NC}"
}

# Function to create cosmic-ssl-status monitoring command
create_ssl_monitor() {
    echo -e "${YELLOW}📊 Creating SSL monitoring tools...${NC}"

    sudo tee /usr/local/bin/cosmic-ssl-status > /dev/null << 'EOF'
#!/bin/bash
# 🔒 COSMIC DOMINION SSL STATUS MONITOR 🔒

echo "🔒 COSMIC DOMINION SSL STATUS"
echo "============================="
echo ""

# Check certificate details
echo "📋 Certificate Information:"
if sudo certbot certificates 2>/dev/null | grep -q "Certificate Name"; then
    sudo certbot certificates | while IFS= read -r line; do
        if [[ $line == *"Certificate Name"* ]] || [[ $line == *"Domains"* ]] || [[ $line == *"Expiry Date"* ]] || [[ $line == *"Certificate Path"* ]]; then
            echo "   $line"
        fi
    done
else
    echo "   ⚠️ No certificates found"
fi

echo ""

# Check renewal timer status
echo "🔄 Auto-renewal Status:"
if systemctl is-active --quiet certbot.timer; then
    echo "   ✅ Certbot timer: ACTIVE"
    next_run=$(systemctl list-timers certbot.timer --no-pager 2>/dev/null | grep certbot.timer | awk '{print $1, $2}')
    if [ -n "$next_run" ]; then
        echo "   📅 Next check: $next_run"
    fi
else
    echo "   ❌ Certbot timer: INACTIVE"
fi

echo ""

# Check nginx SSL configuration
echo "🌐 Nginx SSL Status:"
if nginx -t 2>/dev/null; then
    echo "   ✅ Nginx configuration: VALID"
else
    echo "   ❌ Nginx configuration: ERROR"
fi

if systemctl is-active --quiet nginx; then
    echo "   ✅ Nginx service: RUNNING"
else
    echo "   ❌ Nginx service: STOPPED"
fi

echo ""

# Test HTTPS connectivity
echo "🔍 HTTPS Connectivity Test:"
for domain in "aistorelab.com" "www.aistorelab.com"; do
    if curl -s -I "https://$domain" | grep -q "HTTP/"; then
        echo "   ✅ https://$domain: ACCESSIBLE"
    else
        echo "   ❌ https://$domain: FAILED"
    fi
done

echo ""

# Show certificate expiry details
echo "📅 Certificate Expiry Details:"
if [ -f "/etc/letsencrypt/live/aistorelab.com/fullchain.pem" ]; then
    expiry_date=$(openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -noout -enddate | cut -d= -f2)
    days_until=$(( ($(date -d "$expiry_date" +%s) - $(date +%s)) / 86400 ))

    echo "   📆 Expires: $expiry_date"
    echo "   ⏰ Days remaining: $days_until"

    if [ $days_until -lt 30 ]; then
        echo "   ⚠️  Certificate expires soon!"
    elif [ $days_until -lt 7 ]; then
        echo "   🚨 Certificate expires very soon - check renewal!"
    else
        echo "   ✅ Certificate expiry is healthy"
    fi
else
    echo "   ⚠️ Certificate file not found"
fi

echo ""
echo "🔧 SSL Management Commands:"
echo "   View certificate details: sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -text -noout"
echo "   Test renewal: sudo certbot renew --dry-run"
echo "   Force renewal: sudo certbot renew --force-renewal"
echo "   List certificates: sudo certbot certificates"
echo "   Check nginx config: sudo nginx -t"
echo ""
echo "🔥 DIGITAL SOVEREIGNTY SSL STATUS COMPLETE! 🔥"
EOF

    sudo chmod +x /usr/local/bin/cosmic-ssl-status
    echo -e "${GREEN}✅ cosmic-ssl-status command created${NC}"
}

# Function to test all SSL commands
test_ssl_commands() {
    echo -e "${YELLOW}🧪 Testing SSL certificate commands...${NC}"

    echo -e "${CYAN}1. Testing certificate details:${NC}"
    if sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -text -noout > /dev/null 2>&1; then
        echo -e "${GREEN}   ✅ Certificate details command: WORKING${NC}"
    else
        echo -e "${RED}   ❌ Certificate details command: FAILED${NC}"
    fi

    echo -e "${CYAN}2. Testing renewal dry run:${NC}"
    if sudo certbot renew --dry-run > /dev/null 2>&1; then
        echo -e "${GREEN}   ✅ Certificate renewal test: PASSED${NC}"
    else
        echo -e "${YELLOW}   ⚠️ Certificate renewal test: Check configuration${NC}"
    fi

    echo -e "${CYAN}3. Testing certificate listing:${NC}"
    if sudo certbot certificates > /dev/null 2>&1; then
        echo -e "${GREEN}   ✅ Certificate listing: WORKING${NC}"
    else
        echo -e "${RED}   ❌ Certificate listing: FAILED${NC}"
    fi

    echo -e "${CYAN}4. Testing cosmic-ssl-status:${NC}"
    if cosmic-ssl-status > /dev/null 2>&1; then
        echo -e "${GREEN}   ✅ cosmic-ssl-status: WORKING${NC}"
    else
        echo -e "${RED}   ❌ cosmic-ssl-status: FAILED${NC}"
    fi
}

# Function to display final status
show_final_status() {
    echo ""
    echo -e "${GREEN}✨ IONOS SSL DEPLOYMENT COMPLETE! ✨${NC}"
    echo ""

    echo -e "${PURPLE}🔒 Available SSL Commands:${NC}"
    echo -e "${CYAN}   # View certificate details${NC}"
    echo -e "${WHITE}   sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -text -noout${NC}"
    echo ""
    echo -e "${CYAN}   # Test certificate renewal${NC}"
    echo -e "${WHITE}   sudo certbot renew --dry-run${NC}"
    echo ""
    echo -e "${CYAN}   # List all certificates${NC}"
    echo -e "${WHITE}   sudo certbot certificates${NC}"
    echo ""
    echo -e "${CYAN}   # Custom SSL status monitor${NC}"
    echo -e "${WHITE}   cosmic-ssl-status${NC}"
    echo ""

    echo -e "${BLUE}🌍 Your domains are now SSL secured:${NC}"
    echo -e "${GREEN}   🔒 https://aistorelab.com${NC}"
    echo -e "${GREEN}   🔒 https://www.aistorelab.com${NC}"
    echo ""

    # Run the status monitor
    echo -e "${YELLOW}📊 Current SSL Status:${NC}"
    cosmic-ssl-status
}

# Main execution flow
main() {
    check_sudo
    install_dependencies
    setup_nginx
    obtain_certificates
    setup_auto_renewal
    create_ssl_monitor
    test_ssl_commands
    show_final_status
}

# Execute main function
main "$@"