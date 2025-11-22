#!/bin/bash
# 🔥 IONOS Quick Fix - Copy and paste this entire script into your IONOS server terminal

echo "🔥 === CODEX DOMINION QUICK FIX ==="
echo "🕐 $(date)"

# Quick diagnosis
echo "📊 Quick Status Check:"
systemctl is-active codex-dashboard >/dev/null && echo "✅ codex-dashboard running" || echo "❌ codex-dashboard not running"
systemctl is-active codex-staging >/dev/null && echo "✅ codex-staging running" || echo "❌ codex-staging not running"
systemctl is-active nginx >/dev/null && echo "✅ nginx running" || echo "❌ nginx not running"

echo "🔍 Port Check:"
netstat -tlnp | grep :8501 >/dev/null && echo "✅ Port 8501 in use" || echo "❌ Port 8501 not in use"
netstat -tlnp | grep :8502 >/dev/null && echo "✅ Port 8502 in use" || echo "❌ Port 8502 not in use"

echo
echo "🛠️ Starting Emergency Restoration..."

# Stop everything
echo "🛑 Stopping all services..."
systemctl stop codex-dashboard codex-staging nginx 2>/dev/null
pkill -f streamlit 2>/dev/null
pkill -f "python.*codex" 2>/dev/null
sleep 3

# Quick repository update
echo "📦 Updating repositories..."
if [ -d "/var/www/codex" ]; then
    cd /var/www/codex && git pull origin main 2>/dev/null && echo "✅ Production updated"
fi
if [ -d "/var/www/codex-staging" ]; then
    cd /var/www/codex-staging && git pull origin staging 2>/dev/null && echo "✅ Staging updated"  
fi

# Install dependencies
echo "🐍 Installing dependencies..."
pip3 install --upgrade streamlit pandas numpy requests 2>/dev/null

# Start services
echo "🔥 Starting services..."
systemctl daemon-reload
systemctl enable codex-dashboard codex-staging 2>/dev/null

systemctl start codex-dashboard
sleep 5
systemctl start codex-staging
sleep 5

# Test connections
echo "🧪 Testing connections..."
curl -f http://127.0.0.1:8501 >/dev/null 2>&1 && echo "✅ Production responding" || echo "❌ Production not responding"
curl -f http://127.0.0.1:8502 >/dev/null 2>&1 && echo "✅ Staging responding" || echo "❌ Staging not responding"

# Start nginx
echo "🌐 Starting nginx..."
nginx -t && systemctl start nginx && echo "✅ Nginx started" || echo "❌ Nginx failed"

echo
echo "🏁 === QUICK FIX COMPLETE ==="
echo "🔍 Test your sites:"
echo "   https://aistorelab.com"
echo "   https://staging.aistorelab.com"
echo
echo "📊 Final Status:"
systemctl is-active codex-dashboard nginx codex-staging
echo "🔥 Flames should be restored! ✨"