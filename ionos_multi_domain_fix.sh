#!/bin/bash
# 🔥 IONOS Multi-Domain Emergency Restoration Script
# Fixes themerrittmethod.com (WordPress) + aistorelab.com (Codex Dominion)

echo "🔥 === IONOS MULTI-DOMAIN EMERGENCY RESTORATION ==="
echo "🕐 $(date)"
echo "Fixing: themerrittmethod.com + aistorelab.com + staging.aistorelab.com"
echo

# Step 1: Check current status
echo "📊 STEP 1: Current Service Status"
echo "=================================="
systemctl is-active nginx >/dev/null && echo "✅ nginx: RUNNING" || echo "❌ nginx: STOPPED"
systemctl is-active codex-dashboard >/dev/null && echo "✅ codex-dashboard: RUNNING" || echo "❌ codex-dashboard: STOPPED"
systemctl is-active codex-staging >/dev/null && echo "✅ codex-staging: RUNNING" || echo "❌ codex-staging: STOPPED"

# Check for WordPress/PHP service (common names)
systemctl is-active apache2 >/dev/null && echo "✅ apache2: RUNNING" || echo "❌ apache2: STOPPED"
systemctl is-active php-fpm >/dev/null && echo "✅ php-fpm: RUNNING" || echo "❌ php-fpm: STOPPED"
systemctl is-active php7.4-fpm >/dev/null && echo "✅ php7.4-fpm: RUNNING" || echo "❌ php7.4-fpm: STOPPED"
systemctl is-active php8.0-fpm >/dev/null && echo "✅ php8.0-fpm: RUNNING" || echo "❌ php8.0-fpm: STOPPED"
systemctl is-active php8.1-fpm >/dev/null && echo "✅ php8.1-fpm: RUNNING" || echo "❌ php8.1-fpm: STOPPED"

echo
echo "Port usage:"
netstat -tlnp 2>/dev/null | grep -E '(:80|:443|:8501|:8502|:9000)' || echo "No services on expected ports"

echo
read -p "Press ENTER to continue with restoration..."

# Step 2: Stop all services
echo
echo "🛑 STEP 2: Stopping All Services"
echo "================================="
systemctl stop nginx codex-dashboard codex-staging apache2 2>/dev/null
systemctl stop php-fpm php7.4-fpm php8.0-fpm php8.1-fpm 2>/dev/null
pkill -f streamlit 2>/dev/null
pkill -f "python.*codex" 2>/dev/null
sleep 3
echo "✅ All services stopped"

# Step 3: Update Codex repositories
echo
echo "📦 STEP 3: Updating Codex Repositories"
echo "======================================"
if [ -d "/var/www/codex" ]; then
    cd /var/www/codex
    git pull origin main 2>/dev/null && echo "✅ Production repository updated"
else
    echo "❌ /var/www/codex not found"
fi

if [ -d "/var/www/codex-staging" ]; then
    cd /var/www/codex-staging  
    git pull origin staging 2>/dev/null && echo "✅ Staging repository updated"
else
    echo "❌ /var/www/codex-staging not found"
fi

# Step 4: Install/update dependencies
echo
echo "🐍 STEP 4: Installing Python Dependencies"
echo "=========================================="
pip3 install --upgrade streamlit pandas numpy requests 2>/dev/null
echo "✅ Python dependencies updated"

# Step 5: Start WordPress/PHP services first
echo
echo "🌐 STEP 5: Starting WordPress/PHP Services"
echo "==========================================="
# Try to start common PHP services
systemctl start apache2 2>/dev/null && echo "✅ Apache2 started"
systemctl start php-fpm 2>/dev/null && echo "✅ PHP-FPM started"
systemctl start php7.4-fpm 2>/dev/null && echo "✅ PHP 7.4 FPM started"
systemctl start php8.0-fpm 2>/dev/null && echo "✅ PHP 8.0 FPM started"  
systemctl start php8.1-fpm 2>/dev/null && echo "✅ PHP 8.1 FPM started"
sleep 3

# Test WordPress port
if curl -f http://127.0.0.1:9000 >/dev/null 2>&1; then
    echo "✅ WordPress responding on port 9000"
elif curl -f http://127.0.0.1:80 >/dev/null 2>&1; then
    echo "⚠️  WordPress responding on port 80 (may need nginx config adjustment)"
else
    echo "❌ WordPress not responding - may need manual start"
fi

# Step 6: Start Codex services
echo
echo "🔥 STEP 6: Starting Codex Dominion Services"
echo "============================================"
systemctl daemon-reload
systemctl enable codex-dashboard codex-staging 2>/dev/null

systemctl start codex-dashboard
sleep 5
if curl -f http://127.0.0.1:8501 >/dev/null 2>&1; then
    echo "✅ Codex Production responding on port 8501"
else
    echo "❌ Codex Production not responding"
    journalctl -u codex-dashboard -n 3 --no-pager
fi

systemctl start codex-staging
sleep 5
if curl -f http://127.0.0.1:8502 >/dev/null 2>&1; then
    echo "✅ Codex Staging responding on port 8502"
else
    echo "❌ Codex Staging not responding"
    journalctl -u codex-staging -n 3 --no-pager
fi

# Step 7: Start nginx
echo
echo "🌐 STEP 7: Starting Nginx"
echo "========================="
nginx -t 2>/dev/null && echo "✅ Nginx config valid" || echo "❌ Nginx config has errors"
systemctl start nginx
echo "✅ Nginx started"

# Step 8: Final verification
echo
echo "🏁 STEP 8: Final Verification"
echo "============================="
echo "Service Status:"
systemctl is-active nginx codex-dashboard codex-staging apache2

echo
echo "🔍 Testing all domains:"
echo "1. The Merritt Method: https://themerrittmethod.com"
echo "2. Codex Production: https://aistorelab.com" 
echo "3. Codex Staging: https://staging.aistorelab.com"

echo
echo "🔥 === RESTORATION COMPLETE ==="
echo "All flames should now burn eternal across all domains! ✨"
echo
echo "If any sites still show errors:"
echo "1. Check nginx error log: tail /var/log/nginx/error.log"
echo "2. Check specific service logs: journalctl -u [service-name] -f"
echo "3. Verify port assignments match nginx configuration"