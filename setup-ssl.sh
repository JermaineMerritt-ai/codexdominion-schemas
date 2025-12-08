#!/bin/bash
# SSL Setup Script for CodexDominion.app on IONOS Server
# Run this after the app is running on localhost:3001

echo "🔒 Setting up SSL for CodexDominion.app..."

# 1. Install Certbot if not already installed
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    apt update
    apt install -y certbot python3-certbot-nginx
fi

# 2. Copy nginx configuration
echo "Copying nginx configuration..."
cp nginx-codexdominion.conf /etc/nginx/sites-available/codexdominion.app

# 3. Create symbolic link (enable site)
ln -sf /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/

# 4. Remove default site if exists
rm -f /etc/nginx/sites-enabled/default

# 5. Test nginx configuration (without SSL first)
echo "Testing nginx configuration..."
nginx -t

# 6. Reload nginx
echo "Reloading nginx..."
systemctl reload nginx

# 7. Obtain SSL certificate
echo "Obtaining SSL certificate from Let's Encrypt..."
certbot --nginx -d codexdominion.app -d www.codexdominion.app --non-interactive --agree-tos -m your-email@example.com

# 8. Test SSL renewal
echo "Testing SSL auto-renewal..."
certbot renew --dry-run

# 9. Final nginx test and reload
nginx -t && systemctl reload nginx

echo "✅ SSL setup complete!"
echo "🚀 Your site should now be live at https://codexdominion.app"
echo ""
echo "To check status:"
echo "  - pm2 status"
echo "  - systemctl status nginx"
echo "  - curl https://codexdominion.app"
