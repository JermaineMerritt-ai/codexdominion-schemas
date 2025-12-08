#!/bin/bash
# Commands to run on IONOS server to fix SSL and DNS issues

echo "=== Codex Dominion SSL Fix ==="
echo ""

# 1. Check current nginx configuration
echo "1. Checking nginx configuration..."
sudo nginx -t
echo ""

# 2. Check what SSL certificates exist
echo "2. Checking existing SSL certificates..."
sudo ls -la /etc/letsencrypt/live/
echo ""

# 3. Check systemd service status
echo "3. Checking Codex Dominion service..."
sudo systemctl status codexdominion --no-pager
echo ""

# 4. Check if app is running on port 3000
echo "4. Checking if app is running on port 3000..."
curl -s http://localhost:3000 | head -c 200
echo ""
echo ""

# 5. Check nginx configuration for codexdominion
echo "5. Current nginx site configuration:"
sudo cat /etc/nginx/sites-enabled/codexdominion 2>/dev/null || echo "No codexdominion site config found"
echo ""

# 6. Remove old/conflicting SSL certificates
echo "6. Removing old SSL certificates..."
sudo certbot delete --cert-name codexdominion.app 2>/dev/null || echo "No cert to delete"
sudo certbot delete --cert-name www.codexdominion.app 2>/dev/null || echo "No cert to delete"
echo ""

# 7. Get fresh SSL certificate
echo "7. Getting fresh SSL certificate for both domains..."
echo "   This will take a moment..."
sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app --non-interactive --agree-tos --email admin@codexdominion.app --redirect
echo ""

# 8. Final checks
echo "8. Final verification..."
echo "   Testing HTTPS..."
curl -sk https://codexdominion.app | head -c 100
echo ""
echo ""
echo "   Testing HTTP (should redirect to HTTPS)..."
curl -I http://codexdominion.app 2>&1 | grep -i "location\|http"
echo ""

echo "=== SSL Fix Complete ==="
echo ""
echo "Your site should now be accessible at:"
echo "  - https://codexdominion.app"
echo "  - https://www.codexdominion.app"
echo ""
echo "Check SSL certificate:"
echo "  sudo certbot certificates"
