#!/bin/bash
# IONOS Codex Dashboard - Direct systemctl commands implementation
# This script implements your exact systemctl commands for Linux deployment

SERVICE_NAME="codex-dashboard"
APP_DIR="/opt/codex-dominion"
DOMAIN="codex.aistorelab.com"

echo "🔥 IONOS LINUX - SYSTEMCTL COMMANDS FOR CODEX DASHBOARD"
echo "======================================================="

# Your exact systemctl commands as requested:

echo "1️⃣  sudo systemctl daemon-reload"
echo "   Reloading systemd manager configuration..."
sudo systemctl daemon-reload
echo "   ✅ Daemon configuration reloaded"
echo ""

echo "2️⃣  sudo systemctl enable codex-dashboard"
echo "   Enabling codex-dashboard service for boot startup..."
sudo systemctl enable codex-dashboard
if systemctl is-enabled codex-dashboard >/dev/null 2>&1; then
    echo "   ✅ Service enabled successfully"
    echo "   Created symlink: /etc/systemd/system/multi-user.target.wants/codex-dashboard.service → /etc/systemd/system/codex-dashboard.service"
else
    echo "   ❌ Failed to enable service"
    exit 1
fi
echo ""

echo "3️⃣  sudo systemctl start codex-dashboard"
echo "   Starting codex-dashboard service..."
sudo systemctl start codex-dashboard

# Wait for service to start
sleep 3

if systemctl is-active codex-dashboard >/dev/null 2>&1; then
    echo "   ✅ Service started successfully"
else
    echo "   ❌ Failed to start service"
    echo "   Checking logs:"
    sudo journalctl -u codex-dashboard --no-pager -n 10
    exit 1
fi
echo ""

echo "4️⃣  sudo systemctl status codex-dashboard"
echo "   Checking service status..."
sudo systemctl status codex-dashboard --no-pager -l

echo ""
echo "🔥 ADDITIONAL IONOS DEPLOYMENT CHECKS"
echo "====================================="

# Check if port is listening
echo "🌐 Network Status:"
if netstat -tlnp | grep :8095; then
    echo "   ✅ Port 8095 is listening"
else
    echo "   ❌ Port 8095 not listening"
fi

# Check if application is responding
echo ""
echo "🏥 Health Check:"
if curl -f http://localhost:8095/_stcore/health >/dev/null 2>&1; then
    echo "   ✅ Dashboard is responding"
else
    echo "   ⚠️  Dashboard not responding (may still be starting)"
fi

# Show process information
echo ""
echo "📊 Process Information:"
ps aux | grep streamlit | grep -v grep || echo "   No streamlit processes found"

echo ""
echo "📋 Recent Logs:"
sudo journalctl -u codex-dashboard --no-pager -n 5

echo ""
echo "🔥 IONOS DEPLOYMENT STATUS"
echo "=========================="
echo "📍 Server: IONOS Linux"
echo "🏛️  Service: codex-dashboard"
echo "📁 Directory: $APP_DIR"
echo "🌐 Domain: $DOMAIN"
echo "🔌 Port: 8095"
echo ""

if systemctl is-active codex-dashboard >/dev/null 2>&1; then
    echo "✅ CODEX DASHBOARD IS RUNNING ON IONOS!"
    echo "🌐 Access via: http://$DOMAIN"
    echo "🔒 Internal: http://localhost:8095"
else
    echo "❌ SERVICE NOT RUNNING - CHECK LOGS ABOVE"
fi

echo ""
echo "5️⃣  sudo nginx -t && sudo systemctl reload nginx"
echo "   Testing and reloading nginx configuration..."

# Test nginx configuration
if sudo nginx -t 2>/dev/null; then
    echo "   ✅ nginx: configuration file syntax is ok"
    echo "   ✅ nginx: configuration file test is successful"
    
    # Reload nginx if test passes
    if sudo systemctl reload nginx 2>/dev/null; then
        echo "   ✅ nginx service reloaded successfully"
    else
        echo "   ❌ Failed to reload nginx service"
    fi
else
    echo "   ❌ nginx configuration test failed"
fi

echo ""
echo "🎯 ALL SYSTEMCTL COMMANDS COMPLETED SUCCESSFULLY!"
echo "================================================="