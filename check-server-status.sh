#!/bin/bash
# Server Status Diagnostic Script for CodexDominion

echo "🔍 CodexDominion Server Diagnostic Check"
echo "========================================"
echo ""

# 1. Check if Node.js is installed
echo "1️⃣ Node.js Version:"
node --version 2>/dev/null || echo "❌ Node.js NOT installed"
echo ""

# 2. Check npm version
echo "2️⃣ NPM Version:"
npm --version 2>/dev/null || echo "❌ NPM NOT installed"
echo ""

# 3. Check if PM2 is installed
echo "3️⃣ PM2 Status:"
pm2 --version 2>/dev/null || echo "❌ PM2 NOT installed"
echo ""

# 4. Check if deployment directory exists
echo "4️⃣ Deployment Directory:"
if [ -d "/var/www/codexdominion" ]; then
    echo "✅ /var/www/codexdominion exists"
    ls -lah /var/www/codexdominion/
else
    echo "❌ /var/www/codexdominion does NOT exist"
fi
echo ""

# 5. Check if tar package exists
echo "5️⃣ Uploaded Package:"
if [ -f "/tmp/codexdominion-frontend.tar.gz" ]; then
    echo "✅ Package found"
    ls -lh /tmp/codexdominion-frontend.tar.gz
else
    echo "❌ Package NOT found in /tmp/"
fi
echo ""

# 6. Check port 3001
echo "6️⃣ Port 3001 Status:"
netstat -tulpn | grep :3001 || echo "⚪ Port 3001 is free"
echo ""

# 7. Check PM2 processes
echo "7️⃣ PM2 Processes:"
pm2 list 2>/dev/null || echo "⚪ No PM2 processes running"
echo ""

# 8. Check nginx
echo "8️⃣ Nginx Status:"
systemctl status nginx --no-pager -l 2>/dev/null || echo "⚪ Nginx not installed or not running"
echo ""

# 9. Test localhost:3001
echo "9️⃣ Application Response:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3001 2>/dev/null || echo "❌ Cannot reach localhost:3001"
echo ""

# 10. Check disk space
echo "🔟 Disk Space:"
df -h /var/www 2>/dev/null || df -h /
echo ""

echo "========================================"
echo "✅ Diagnostic Complete"
