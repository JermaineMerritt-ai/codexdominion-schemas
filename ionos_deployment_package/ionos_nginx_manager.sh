#!/bin/bash
# IONOS Nginx Management Script for Codex Dashboard
# Provides nginx configuration testing, reloading, and management

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

NGINX_CONFIG="/etc/nginx/sites-available/codex-dashboard"
DOMAIN="codex.aistorelab.com"

print_status() {
    echo -e "${CYAN}📊 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

function test_nginx_config() {
    print_status "Testing nginx configuration..."
    
    if sudo nginx -t; then
        print_success "Nginx configuration syntax is valid"
        return 0
    else
        print_error "Nginx configuration has syntax errors"
        return 1
    fi
}

function reload_nginx() {
    print_status "Reloading nginx service..."
    
    if sudo systemctl reload nginx; then
        print_success "Nginx reloaded successfully"
        return 0
    else
        print_error "Failed to reload nginx"
        return 1
    fi
}

function test_and_reload() {
    echo "🔥 NGINX TEST AND RELOAD - CODEX DASHBOARD"
    echo "=========================================="
    
    print_status "Executing: sudo nginx -t && sudo systemctl reload nginx"
    echo ""
    
    if test_nginx_config; then
        echo ""
        if reload_nginx; then
            echo ""
            print_success "Configuration test and reload completed successfully!"
            check_service_status
        else
            print_error "Reload failed - check nginx logs"
            return 1
        fi
    else
        print_error "Configuration test failed - reload skipped"
        show_config_errors
        return 1
    fi
}

function check_service_status() {
    print_status "Checking nginx service status..."
    
    if systemctl is-active nginx >/dev/null 2>&1; then
        print_success "Nginx service is active and running"
        
        # Check if our site is enabled
        if [ -L "/etc/nginx/sites-enabled/codex-dashboard" ]; then
            print_success "Codex Dashboard site is enabled"
        else
            print_warning "Codex Dashboard site not enabled"
        fi
        
        # Check if domain is responding
        if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|301\|302"; then
            print_success "Nginx is responding to HTTP requests"
        else
            print_warning "Nginx not responding properly"
        fi
        
    else
        print_error "Nginx service is not running"
        return 1
    fi
}

function show_config_errors() {
    print_status "Recent nginx error logs:"
    sudo tail -n 10 /var/log/nginx/error.log 2>/dev/null || echo "No error log available"
}

function show_status() {
    echo "🔥 NGINX STATUS - CODEX DASHBOARD"
    echo "================================"
    
    print_status "Service Status:"
    sudo systemctl status nginx --no-pager -l
    
    echo ""
    print_status "Configuration Files:"
    if [ -f "$NGINX_CONFIG" ]; then
        echo "   ✅ Main config: $NGINX_CONFIG"
    else
        echo "   ❌ Main config: $NGINX_CONFIG (missing)"
    fi
    
    if [ -L "/etc/nginx/sites-enabled/codex-dashboard" ]; then
        echo "   ✅ Site enabled: codex-dashboard"
    else
        echo "   ❌ Site enabled: codex-dashboard (not linked)"
    fi
    
    echo ""
    print_status "Network Status:"
    netstat -tlnp | grep nginx | head -5
    
    echo ""
    print_status "Recent Access Logs:"
    sudo tail -n 5 /var/log/nginx/codex-dashboard.access.log 2>/dev/null || echo "No access log available"
}

function restart_nginx() {
    print_status "Restarting nginx service..."
    
    if sudo systemctl restart nginx; then
        print_success "Nginx restarted successfully"
        check_service_status
    else
        print_error "Failed to restart nginx"
        show_config_errors
        return 1
    fi
}

function enable_site() {
    print_status "Enabling Codex Dashboard site..."
    
    if [ ! -f "$NGINX_CONFIG" ]; then
        print_error "Configuration file not found: $NGINX_CONFIG"
        return 1
    fi
    
    sudo ln -sf "$NGINX_CONFIG" /etc/nginx/sites-enabled/codex-dashboard
    print_success "Site enabled"
    
    test_and_reload
}

function setup_ssl() {
    print_status "Setting up SSL certificate for $DOMAIN..."
    
    if command -v certbot >/dev/null 2>&1; then
        sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email admin@aistorelab.com || {
            print_warning "SSL setup failed - may need manual DNS configuration"
            return 1
        }
        print_success "SSL certificate configured"
    else
        print_error "Certbot not installed"
        return 1
    fi
}

# Main command handling
case "${1:-test-and-reload}" in
    "test"|"-t")
        test_nginx_config
        ;;
    "reload"|"-r")
        reload_nginx
        ;;
    "test-and-reload"|"tar")
        test_and_reload
        ;;
    "status"|"-s")
        show_status
        ;;
    "restart")
        restart_nginx
        ;;
    "enable")
        enable_site
        ;;
    "ssl")
        setup_ssl
        ;;
    "errors")
        show_config_errors
        ;;
    *)
        echo "Usage: $0 {test|reload|test-and-reload|status|restart|enable|ssl|errors}"
        echo ""
        echo "Commands:"
        echo "  test             - Test nginx configuration (nginx -t)"
        echo "  reload           - Reload nginx service"
        echo "  test-and-reload  - Test config then reload (default)"
        echo "  status           - Show nginx and site status"
        echo "  restart          - Restart nginx service"
        echo "  enable           - Enable Codex Dashboard site"
        echo "  ssl              - Setup SSL certificate"
        echo "  errors           - Show recent error logs"
        echo ""
        echo "Examples:"
        echo "  $0 test-and-reload    # sudo nginx -t && sudo systemctl reload nginx"
        echo "  $0 status             # Show detailed nginx status"
        exit 1
        ;;
esac

echo ""
echo "🔥 Nginx management completed!"