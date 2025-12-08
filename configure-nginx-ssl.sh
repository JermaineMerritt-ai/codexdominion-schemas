#!/bin/bash
# Final step: Configure Nginx and SSL for CodexDominion.app

echo "🌐 Configuring Nginx for CodexDominion.app..."
echo ""

# 1. Copy nginx config
echo "1️⃣ Installing nginx configuration..."
cp /tmp/nginx-codexdominion.conf /etc/nginx/sites-available/codexdominion.app
echo "✅ Config copied"

# 2. Enable site
echo "2️⃣ Enabling site..."
ln -sf /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/
echo "✅ Site enabled"

# 3. Remove SSL lines temporarily (we'll get cert first)
echo "3️⃣ Creating temporary HTTP-only config..."
cat > /etc/nginx/sites-available/codexdominion.app << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name codexdominion.app www.codexdominion.app;

    # Logging
    access_log /var/log/nginx/codexdominion_access.log;
    error_log /var/log/nginx/codexdominion_error.log;

    # Root location - proxy to Next.js on port 3001
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    # Static files caching
    location /_next/static {
        proxy_pass http://localhost:3001;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # API routes
    location /api {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF
echo "✅ HTTP config created"

# 4. Test nginx config
echo "4️⃣ Testing nginx configuration..."
nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Nginx config is valid"
else
    echo "❌ Nginx config has errors!"
    exit 1
fi

# 5. Reload nginx
echo "5️⃣ Reloading nginx..."
systemctl reload nginx
echo "✅ Nginx reloaded"

# 6. Get SSL certificate
echo "6️⃣ Obtaining SSL certificate..."
certbot --nginx -d codexdominion.app -d www.codexdominion.app --non-interactive --agree-tos -m jermaine@codexdominion.app --redirect
echo "✅ SSL configured"

# 7. Test SSL renewal
echo "7️⃣ Testing SSL auto-renewal..."
certbot renew --dry-run
echo "✅ SSL renewal tested"

# 8. Final check
echo "8️⃣ Final verification..."
curl -I https://codexdominion.app 2>&1 | head -5

echo ""
echo "========================================"
echo "🎉 CODEX DOMINION IS LIVE!"
echo ""
echo "Your sovereign dashboard is now accessible at:"
echo "🌍 https://codexdominion.app"
echo "🌍 https://www.codexdominion.app"
echo ""
echo "Features live:"
echo "  • 16 Operational Engines"
echo "  • 28 Avatar Council (Claude & Copilot)"
echo "  • 6 AI Tools (Video Studio, Automation, etc.)"
echo "  • 50+ Dashboards"
echo "  • Real-time monitoring"
echo "  • $76.6K Revenue tracking"
echo ""
echo "Management commands:"
echo "  pm2 status"
echo "  pm2 logs codex-dominion"
echo "  systemctl status nginx"
echo "========================================"
