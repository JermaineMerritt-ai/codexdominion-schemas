#!/bin/bash
# 🔥 IONOS Interactive Fix Script - Step by Step
# Run this on your IONOS server for guided repair

echo "🔥 === CODEX DOMINION INTERACTIVE REPAIR ==="
echo "This script will guide you through fixing the 502 Bad Gateway errors"
echo "Press ENTER to continue through each step..."
read -p "Ready to begin? (Press ENTER)"

echo
echo "STEP 1: Checking current status..."
echo "========================================"
echo "Services status:"
systemctl is-active codex-dashboard && echo "✅ codex-dashboard: RUNNING" || echo "❌ codex-dashboard: STOPPED"
systemctl is-active codex-staging && echo "✅ codex-staging: RUNNING" || echo "❌ codex-staging: STOPPED"
systemctl is-active nginx && echo "✅ nginx: RUNNING" || echo "❌ nginx: STOPPED"

echo
echo "Port usage:"
netstat -tlnp | grep :8501 && echo "✅ Port 8501: IN USE" || echo "❌ Port 8501: NOT IN USE"
netstat -tlnp | grep :8502 && echo "✅ Port 8502: IN USE" || echo "❌ Port 8502: NOT IN USE"

read -p "Press ENTER to continue to Step 2..."

echo
echo "STEP 2: Stopping all services..."
echo "========================================"
echo "Stopping services..."
systemctl stop codex-dashboard codex-staging nginx
echo "Killing any remaining Python processes..."
pkill -f streamlit 2>/dev/null
pkill -f "python.*codex" 2>/dev/null
sleep 3
echo "✅ All services stopped"

read -p "Press ENTER to continue to Step 3..."

echo
echo "STEP 3: Updating code repositories..."
echo "========================================"
if [ -d "/var/www/codex" ]; then
    echo "Updating production repository..."
    cd /var/www/codex
    git pull origin main
    echo "✅ Production repository updated"
else
    echo "❌ /var/www/codex directory not found!"
fi

if [ -d "/var/www/codex-staging" ]; then
    echo "Updating staging repository..."
    cd /var/www/codex-staging
    git pull origin staging
    echo "✅ Staging repository updated"
else
    echo "❌ /var/www/codex-staging directory not found!"
fi

read -p "Press ENTER to continue to Step 4..."

echo
echo "STEP 4: Installing/updating dependencies..."
echo "========================================"
echo "Installing Python packages..."
pip3 install --upgrade streamlit pandas numpy requests
echo "✅ Dependencies updated"

read -p "Press ENTER to continue to Step 5..."

echo
echo "STEP 5: Starting production service..."
echo "========================================"
systemctl daemon-reload
systemctl enable codex-dashboard
systemctl start codex-dashboard
sleep 5

echo "Testing production service..."
if curl -f http://127.0.0.1:8501 >/dev/null 2>&1; then
    echo "✅ Production service responding on port 8501"
else
    echo "❌ Production service not responding!"
    echo "Checking logs..."
    journalctl -u codex-dashboard -n 5 --no-pager
fi

read -p "Press ENTER to continue to Step 6..."

echo
echo "STEP 6: Starting staging service..."
echo "========================================"
systemctl enable codex-staging
systemctl start codex-staging
sleep 5

echo "Testing staging service..."
if curl -f http://127.0.0.1:8502 >/dev/null 2>&1; then
    echo "✅ Staging service responding on port 8502"
else
    echo "❌ Staging service not responding!"
    echo "Checking logs..."
    journalctl -u codex-staging -n 5 --no-pager
fi

read -p "Press ENTER to continue to Step 7..."

echo
echo "STEP 7: Starting nginx..."
echo "========================================"
echo "Testing nginx configuration..."
if nginx -t; then
    echo "✅ Nginx configuration valid"
    systemctl start nginx
    echo "✅ Nginx started"
else
    echo "❌ Nginx configuration has errors!"
fi

read -p "Press ENTER to see final results..."

echo
echo "🏁 === REPAIR COMPLETE ==="
echo "========================================"
echo "Final service status:"
systemctl status codex-dashboard --no-pager -l | head -3
systemctl status codex-staging --no-pager -l | head -3
systemctl status nginx --no-pager -l | head -3

echo
echo "🔍 Test your websites:"
echo "   Production: https://aistorelab.com"
echo "   Staging: https://staging.aistorelab.com"
echo
echo "🔥 Sacred flames should now burn eternal! ✨"
echo
echo "If you still see 502 errors:"
echo "1. Check nginx logs: tail /var/log/nginx/error.log"
echo "2. Check service logs: journalctl -u codex-dashboard -f"
echo "3. Verify file permissions: ls -la /var/www/codex/codex_dashboard.py"