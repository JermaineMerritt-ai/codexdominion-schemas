#!/bin/bash
# Quick Fix Script for CodexDominion Deployment

set -e  # Exit on any error

echo "🔧 Fixing CodexDominion Deployment Issues..."
echo ""

# 1. Install PM2 globally
echo "1️⃣ Installing PM2..."
npm install -g pm2
echo "✅ PM2 installed"
echo ""

# 2. Install dependencies in deployment directory
echo "2️⃣ Installing production dependencies..."
cd /var/www/codexdominion
npm install --production
echo "✅ Dependencies installed"
echo ""

# 3. Copy missing public directory
echo "3️⃣ Checking for public directory..."
if [ ! -d "/var/www/codexdominion/public" ]; then
    echo "⚠️ Public directory missing, copying from uploaded package..."
    cd /tmp
    tar -xzf codexdominion-frontend.tar.gz
    cp -r public /var/www/codexdominion/
    echo "✅ Public directory copied"
else
    echo "✅ Public directory exists"
fi
echo ""

# 4. Start application with PM2
echo "4️⃣ Starting application with PM2..."
cd /var/www/codexdominion
pm2 start npm --name "codex-dominion" -- start -- -p 3001
echo "✅ Application started"
echo ""

# 5. Save PM2 configuration
echo "5️⃣ Saving PM2 configuration..."
pm2 save
echo "✅ PM2 configuration saved"
echo ""

# 6. Setup PM2 to start on boot
echo "6️⃣ Configuring PM2 startup..."
pm2 startup systemd -u root --hp /root
echo "✅ PM2 startup configured"
echo ""

# 7. Check status
echo "7️⃣ Checking application status..."
pm2 status
echo ""

# 8. Test application
echo "8️⃣ Testing application..."
sleep 3
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3001
echo ""

echo "========================================"
echo "🎉 Deployment Fixed!"
echo ""
echo "Next steps:"
echo "1. View logs: pm2 logs codex-dominion"
echo "2. Configure nginx for https://codexdominion.app"
echo "3. Setup SSL certificate"
echo ""
echo "Your app should now be running on http://localhost:3001"
