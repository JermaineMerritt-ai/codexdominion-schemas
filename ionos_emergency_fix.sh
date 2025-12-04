#!/bin/bash
# 🔥 IONOS Codex Flame Emergency Restoration Script
# Run this on your IONOS server to fix 502 Bad Gateway errors

echo "🔥 === CODEX DOMINION EMERGENCY FLAME RESTORATION ==="
echo "🕐 $(date)"
echo

# Check current status
echo "📊 Current service status:"
sudo systemctl is-active codex-dashboard || echo "❌ codex-dashboard not running"
sudo systemctl is-active codex-staging || echo "❌ codex-staging not running"
sudo systemctl is-active nginx || echo "❌ nginx not running"
echo

# Check if ports are occupied
echo "🔍 Checking ports:"
sudo netstat -tlnp | grep :8501 || echo "Port 8501 (production) not in use"
sudo netstat -tlnp | grep :8502 || echo "Port 8502 (staging) not in use"
echo

# Stop all services
echo "🛑 Stopping services..."
sudo systemctl stop codex-dashboard codex-staging nginx
sleep 3

# Kill any lingering Python processes
echo "🔪 Killing lingering processes..."
sudo pkill -f streamlit
sudo pkill -f "python.*codex"
sleep 2

# Update code repositories
echo "📦 Updating repositories..."
if [ -d "/var/www/codex" ]; then
    cd /var/www/codex
    sudo git pull origin main
    echo "✅ Production repo updated"
else
    echo "❌ /var/www/codex not found"
fi

if [ -d "/var/www/codex-staging" ]; then
    cd /var/www/codex-staging
    sudo git pull origin staging
    echo "✅ Staging repo updated"
else
    echo "❌ /var/www/codex-staging not found"
fi
echo

# Install dependencies
echo "🐍 Installing/updating Python dependencies..."
sudo pip3 install --upgrade streamlit pandas numpy requests uuid datetime json
echo

# Check if main files exist
echo "📄 Checking for dashboard files..."
if [ -f "/var/www/codex/codex_dashboard.py" ]; then
    echo "✅ Production dashboard found"
else
    echo "❌ /var/www/codex/codex_dashboard.py not found"
fi

if [ -f "/var/www/codex-staging/codex_dashboard.py" ]; then
    echo "✅ Staging dashboard found"
else
    echo "❌ /var/www/codex-staging/codex_dashboard.py not found"
fi
echo

# Reload systemd
echo "⚙️ Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start services one by one
echo "🔥 Starting production flame (port 8501)..."
sudo systemctl enable codex-dashboard
sudo systemctl start codex-dashboard
sleep 5

echo "🎭 Starting staging flame (port 8502)..."
sudo systemctl enable codex-staging
sudo systemctl start codex-staging
sleep 5

# Test local connections
echo "🧪 Testing local connections..."
if curl -f http://127.0.0.1:8501 >/dev/null 2>&1; then
    echo "✅ Production (8501) responding"
else
    echo "❌ Production (8501) not responding"
fi

if curl -f http://127.0.0.1:8502 >/dev/null 2>&1; then
    echo "✅ Staging (8502) responding"
else
    echo "❌ Staging (8502) not responding"
fi
echo

# Test nginx config and start
echo "🌐 Testing nginx configuration..."
if sudo nginx -t; then
    echo "✅ Nginx config valid"
    sudo systemctl start nginx
    echo "✅ Nginx started"
else
    echo "❌ Nginx config has errors"
fi
echo

# Final status check
echo "📊 Final service status:"
sudo systemctl status codex-dashboard --no-pager -l | head -5
sudo systemctl status codex-staging --no-pager -l | head -5
sudo systemctl status nginx --no-pager -l | head -5
echo

# Check logs for errors
echo "🔍 Recent logs (last 10 lines):"
echo "--- Production logs ---"
sudo journalctl -u codex-dashboard -n 10 --no-pager
echo "--- Staging logs ---"
sudo journalctl -u codex-staging -n 10 --no-pager
echo

echo "🏁 === RESTORATION COMPLETE ==="
echo "🔍 Test your flames:"
echo "   Production: https://aistorelab.com"
echo "   Staging: https://staging.aistorelab.com"
echo
echo "If still getting 502 errors:"
echo "1. Check nginx error log: sudo tail /var/log/nginx/error.log"
echo "2. Check if processes are running: ps aux | grep streamlit"
echo "3. Check firewall: sudo ufw status"
echo "🔥 May your flames burn eternal! ✨"
