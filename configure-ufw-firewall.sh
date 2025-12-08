#!/bin/bash
# UFW Firewall Configuration for CodexDominion Server
# Run this script on your server at 74.208.123.158

echo "=================================="
echo "🔥 Configuring UFW Firewall"
echo "=================================="

# Enable UFW (if not already enabled)
echo "📋 Enabling UFW..."
sudo ufw --force enable

# Allow SSH (critical - don't lock yourself out!)
echo "✅ Allowing SSH (port 22)..."
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
echo "✅ Allowing HTTP (port 80)..."
sudo ufw allow 80/tcp

echo "✅ Allowing HTTPS (port 443)..."
sudo ufw allow 443/tcp

# Allow Next.js development server
echo "✅ Allowing Next.js (port 3000)..."
sudo ufw allow 3000/tcp

# Allow Backend API servers
echo "✅ Allowing Backend API (port 8001)..."
sudo ufw allow 8001/tcp

echo "✅ Allowing Alt Backend (port 8080)..."
sudo ufw allow 8080/tcp

# Optional: Database ports (only if accessed externally)
# Uncomment if needed:
# echo "✅ Allowing PostgreSQL (port 5432)..."
# sudo ufw allow 5432/tcp

# echo "✅ Allowing Redis (port 6379)..."
# sudo ufw allow 6379/tcp

# Reload UFW
echo "🔄 Reloading UFW..."
sudo ufw reload

# Show status
echo ""
echo "=================================="
echo "📊 Current UFW Status"
echo "=================================="
sudo ufw status numbered

echo ""
echo "✅ Firewall configuration complete!"
echo "🧪 Test HTTPS now: curl https://74.208.123.158"
