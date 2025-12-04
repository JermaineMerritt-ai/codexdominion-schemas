#!/bin/bash
"""
CODEX DOMINION - NGINX DEPLOYMENT SCRIPT
Deploy Codex Dominion behind Nginx reverse proxy with SSL
"""

# Configuration variables
DOMAIN="aistorelab.com"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled"
CODEX_PATH="/srv/codex"

echo "🔥 CODEX DOMINION - NGINX DEPLOYMENT 🔥"
echo "======================================"

# Function to check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo "❌ This script must be run as root"
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    echo "📦 Installing dependencies..."
    apt-get update
    apt-get install -y nginx certbot python3-certbot-nginx
    echo "✅ Dependencies installed"
}

# Function to create Nginx configuration
deploy_nginx_config() {
    echo "⚙️ Deploying Nginx configuration..."

    # Copy our configuration
    cp nginx-aistorelab.conf "$NGINX_SITES_AVAILABLE/$DOMAIN"

    # Create symlink to enable site
    ln -sf "$NGINX_SITES_AVAILABLE/$DOMAIN" "$NGINX_SITES_ENABLED/$DOMAIN"

    # Remove default site if it exists
    if [[ -f "$NGINX_SITES_ENABLED/default" ]]; then
        rm "$NGINX_SITES_ENABLED/default"
        echo "🗑️ Removed default Nginx site"
    fi

    echo "✅ Nginx configuration deployed"
}

# Function to obtain SSL certificates
setup_ssl() {
    echo "🔒 Setting up SSL certificates..."

    # Test Nginx configuration first
    nginx -t
    if [[ $? -ne 0 ]]; then
        echo "❌ Nginx configuration test failed"
        exit 1
    fi

    # Reload Nginx
    systemctl reload nginx

    # Obtain SSL certificate
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

    if [[ $? -eq 0 ]]; then
        echo "✅ SSL certificates obtained and configured"
    else
        echo "⚠️ SSL setup failed, but continuing with HTTP"
    fi
}

# Function to configure firewall
setup_firewall() {
    echo "🛡️ Configuring firewall..."

    # Allow HTTP and HTTPS
    ufw allow 'Nginx Full'
    ufw allow OpenSSH

    # Enable firewall if not already enabled
    ufw --force enable

    echo "✅ Firewall configured"
}

# Function to create systemd service for auto-renewal
setup_cert_renewal() {
    echo "🔄 Setting up automatic SSL renewal..."

    # Create systemd timer for certificate renewal
    cat > /etc/systemd/system/certbot-renewal.service << 'EOF'
[Unit]
Description=Certbot Renewal
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/certbot renew --quiet --no-self-upgrade
ExecStartPost=/bin/systemctl reload nginx
EOF

    cat > /etc/systemd/system/certbot-renewal.timer << 'EOF'
[Unit]
Description=Run certbot twice daily
Requires=certbot-renewal.service

[Timer]
OnCalendar=*-*-* 00,12:00:00
RandomizedDelaySec=3600
Persistent=true

[Install]
WantedBy=timers.target
EOF

    # Enable and start the timer
    systemctl daemon-reload
    systemctl enable certbot-renewal.timer
    systemctl start certbot-renewal.timer

    echo "✅ Automatic SSL renewal configured"
}

# Function to create monitoring script
create_monitoring() {
    echo "📊 Creating monitoring script..."

    cat > /usr/local/bin/codex-monitor.sh << 'EOF'
#!/bin/bash
# Codex Dominion Service Monitor

check_service() {
    local service=$1
    local port=$2

    if curl -f -s http://localhost:$port/ > /dev/null; then
        echo "✅ $service (port $port): Running"
        return 0
    else
        echo "❌ $service (port $port): Failed"
        return 1
    fi
}

echo "🔥 Codex Dominion Service Status:"
echo "================================"

check_service "Main Dashboard" 8080
check_service "Contributions" 8083
check_service "Council Oversight" 8086
check_service "Contributions Viewer" 8090

echo ""
echo "🌐 Nginx Status:"
systemctl is-active nginx

echo ""
echo "🔒 SSL Certificate Status:"
certbot certificates | grep -A 1 aistorelab.com
EOF

    chmod +x /usr/local/bin/codex-monitor.sh
    echo "✅ Monitoring script created at /usr/local/bin/codex-monitor.sh"
}

# Function to display access information
show_access_info() {
    echo ""
    echo "🔥 CODEX DOMINION - DEPLOYMENT COMPLETE 🔥"
    echo "=========================================="
    echo ""
    echo "🌐 Access URLs:"
    echo "   Main Dashboard:     https://$DOMAIN/"
    echo "   Community Submit:   https://$DOMAIN/contribute/"
    echo "   Council Oversight:  https://$DOMAIN/council/"
    echo "   Public Viewer:      https://$DOMAIN/viewer/"
    echo "   Legacy Summary:     https://$DOMAIN/summary/"
    echo ""
    echo "🔧 Management Commands:"
    echo "   Check Status:       /usr/local/bin/codex-monitor.sh"
    echo "   Restart Nginx:      systemctl restart nginx"
    echo "   Check Logs:         tail -f /var/log/nginx/access.log"
    echo "   SSL Renewal:        certbot renew --dry-run"
    echo ""
    echo "📊 Service Ports (Internal):"
    echo "   8080 - Main Dashboard"
    echo "   8083 - Community Contributions"
    echo "   8086 - Council Oversight"
    echo "   8090 - Contributions Viewer"
    echo ""
}

# Main deployment process
main() {
    check_root

    echo "🚀 Starting Codex Dominion Nginx deployment..."
    echo ""

    install_dependencies
    deploy_nginx_config
    setup_ssl
    setup_firewall
    setup_cert_renewal
    create_monitoring

    # Final nginx reload
    systemctl reload nginx

    show_access_info
}

# Execute main function
main "$@"
