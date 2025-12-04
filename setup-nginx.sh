#!/bin/bash
# Nginx Setup Script for Codex Dominion Trading Platform

set -e

echo "🚀 Setting up Nginx for Codex Dominion Trading Platform"
echo "=" * 60

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing Nginx..."
    apt update
    apt install -y nginx
else
    echo "✅ Nginx is already installed"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p /etc/nginx/snippets
mkdir -p /var/log/nginx
mkdir -p /srv/codex/static

# Copy configuration files
echo "📋 Setting up Nginx configuration..."

# Copy main configuration
cp nginx/codex-dominion.conf /etc/nginx/sites-available/codex-dominion

# Copy locations snippet
cp nginx/codex-dominion-locations.conf /etc/nginx/snippets/

# Enable the site
if [ ! -L /etc/nginx/sites-enabled/codex-dominion ]; then
    ln -s /etc/nginx/sites-available/codex-dominion /etc/nginx/sites-enabled/
    echo "✅ Enabled Codex Dominion site"
else
    echo "ℹ️  Codex Dominion site already enabled"
fi

# Disable default site if it exists
if [ -L /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
    echo "✅ Disabled default Nginx site"
fi

# Test Nginx configuration
echo "🔍 Testing Nginx configuration..."
if nginx -t; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration has errors"
    exit 1
fi

# Create self-signed SSL certificate for development
if [ ! -f /etc/ssl/certs/codex-dominion.crt ]; then
    echo "🔐 Creating self-signed SSL certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/ssl/private/codex-dominion.key \
        -out /etc/ssl/certs/codex-dominion.crt \
        -subj "/C=US/ST=State/L=City/O=CodexDominion/OU=TradingPlatform/CN=codex-dominion.local"
    echo "✅ SSL certificate created"
else
    echo "ℹ️  SSL certificate already exists"
fi

# Set proper permissions
echo "🔒 Setting permissions..."
chown -R www-data:www-data /srv/codex
chmod -R 755 /srv/codex

# Start and enable Nginx
echo "🔄 Starting Nginx..."
systemctl enable nginx
systemctl restart nginx

if systemctl is-active --quiet nginx; then
    echo "✅ Nginx is running successfully"
else
    echo "❌ Failed to start Nginx"
    systemctl status nginx
    exit 1
fi

echo ""
echo "🎉 Nginx setup completed successfully!"
echo ""
echo "📊 Your Codex Dominion platform is now available at:"
echo "   HTTP:  http://localhost"
echo "   HTTPS: https://localhost (self-signed certificate)"
echo ""
echo "🔗 Service URLs:"
echo "   Main Dashboard:     http://localhost/"
echo "   Portfolio Manager:  http://localhost/portfolio"
echo "   API Backend:        http://localhost/api"
echo "   API Documentation:  http://localhost/docs"
echo "   Health Check:       http://localhost/health"
echo ""
echo "📋 Management commands:"
echo "   sudo systemctl status nginx"
echo "   sudo systemctl restart nginx"
echo "   sudo nginx -t  # Test configuration"
echo "   sudo tail -f /var/log/nginx/codex-dominion.access.log"
echo ""
echo "⚠️  Note: Make sure your Codex services are running:"
echo "   - Main Dashboard on port 8501"
echo "   - Portfolio Dashboard on port 8503"
echo "   - FastAPI Backend on port 8000"
