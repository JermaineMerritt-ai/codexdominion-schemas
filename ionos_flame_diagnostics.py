#!/usr/bin/env python3
"""
🔥 IONOS Flame Diagnostics - 502 Bad Gateway Resolution
Diagnoses and fixes nginx 502 errors for Codex Dominion deployment
"""

import datetime
import json
import subprocess
import time

import requests


def check_flame_health():
    """Check current flame status"""
    print("🔥 === IONOS FLAME DIAGNOSTICS ===")
    print(f"🕐 Ceremony Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check main domain
    print("🌐 Checking aistorelab.com flame...")
    try:
        response = requests.get("https://aistorelab.com", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 502:
            print("   ⚠️  502 Bad Gateway detected!")
        elif response.status_code == 200:
            print("   ✅ Flame burns bright!")
        else:
            print(f"   ⚡ Unexpected status: {response.status_code}")
    except requests.exceptions.Timeout:
        print("   ⏰ Timeout - Server may be down")
    except requests.exceptions.ConnectionError:
        print("   🔌 Connection Error - DNS or network issue")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    print()

    # Check staging
    print("🎭 Checking staging.aistorelab.com flame...")
    try:
        response = requests.get("https://staging.aistorelab.com", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 502:
            print("   ⚠️  502 Bad Gateway detected!")
        elif response.status_code == 200:
            print("   ✅ Staging flame burns bright!")
        else:
            print(f"   ⚡ Unexpected status: {response.status_code}")
    except requests.exceptions.Timeout:
        print("   ⏰ Timeout - Server may be down")
    except requests.exceptions.ConnectionError:
        print("   🔌 Connection Error - DNS or network issue")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def generate_fix_commands():
    """Generate SSH commands to fix 502 issues"""
    print("\n🛠️  === 502 BAD GATEWAY FIX COMMANDS ===")
    print("Copy and run these commands on your IONOS server:")
    print()

    print("# 1. Check if Streamlit services are running")
    print("sudo systemctl status codex-dashboard")
    print("sudo systemctl status codex-staging")
    print()

    print("# 2. Check if processes are listening on correct ports")
    print("sudo netstat -tlnp | grep 8501  # Production port")
    print("sudo netstat -tlnp | grep 8502  # Staging port")
    print()

    print("# 3. Check nginx configuration")
    print("sudo nginx -t")
    print("sudo systemctl status nginx")
    print()

    print("# 4. Check application logs")
    print("sudo journalctl -u codex-dashboard -n 50")
    print("sudo journalctl -u codex-staging -n 50")
    print()

    print("# 5. Restart services (if needed)")
    print("sudo systemctl restart codex-dashboard")
    print("sudo systemctl restart codex-staging")
    print("sudo systemctl reload nginx")
    print()

    print("# 6. Check nginx error logs")
    print("sudo tail -f /var/log/nginx/error.log")
    print()


def generate_nginx_config():
    """Generate proper nginx configuration"""
    print("\n🌐 === NGINX CONFIGURATION ===")
    print("Save this as /etc/nginx/sites-available/aistorelab.com:")
    print()

    nginx_config = """# Codex Dominion - aistorelab.com
server {
    listen 80;
    server_name aistorelab.com www.aistorelab.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name aistorelab.com www.aistorelab.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/aistorelab.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/aistorelab.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;

    # Reverse proxy to Streamlit
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
}

# Staging subdomain
server {
    listen 80;
    server_name staging.aistorelab.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name staging.aistorelab.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/aistorelab.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/aistorelab.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;

    # Reverse proxy to Staging Streamlit
    location / {
        proxy_pass http://127.0.0.1:8502;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
}"""

    print(nginx_config)


def generate_systemd_services():
    """Generate updated systemd service files"""
    print("\n⚙️  === SYSTEMD SERVICE FILES ===")

    print("Save as /etc/systemd/system/codex-dashboard.service:")
    production_service = """[Unit]
Description=Codex Dashboard - Production Flame
After=network.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/var/www/codex
ExecStart=/usr/local/bin/streamlit run codex_dashboard.py --server.port=8501 --server.address=127.0.0.1 --server.headless=true
Restart=always
RestartSec=10
User=www-data
Group=www-data

# Environment
Environment=PYTHONPATH=/var/www/codex
Environment=STREAMLIT_SERVER_HEADLESS=true
Environment=STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=codex-dashboard

[Install]
WantedBy=multi-user.target"""
    print(production_service)
    print()

    print("Save as /etc/systemd/system/codex-staging.service:")
    staging_service = """[Unit]
Description=Codex Dashboard - Staging Flame  
After=network.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/var/www/codex-staging
ExecStart=/usr/local/bin/streamlit run codex_dashboard.py --server.port=8502 --server.address=127.0.0.1 --server.headless=true
Restart=always
RestartSec=10
User=www-data
Group=www-data

# Environment
Environment=PYTHONPATH=/var/www/codex-staging
Environment=STREAMLIT_SERVER_HEADLESS=true
Environment=STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=codex-staging

[Install]
WantedBy=multi-user.target"""
    print(staging_service)


def generate_deployment_script():
    """Generate complete deployment script"""
    print("\n🚀 === COMPLETE DEPLOYMENT SCRIPT ===")
    print("Run this script on your IONOS server to fix everything:")
    print()

    script = """#!/bin/bash
# Codex Dominion 502 Fix - Complete Deployment Script

echo "🔥 Starting Codex Dominion flame restoration..."

# Stop services
echo "🛑 Stopping services..."
sudo systemctl stop codex-dashboard codex-staging nginx

# Update repositories
echo "📦 Updating code repositories..."
cd /var/www/codex && sudo git pull origin main
cd /var/www/codex-staging && sudo git pull origin staging

# Install/update Python dependencies
echo "🐍 Installing Python dependencies..."
sudo pip3 install streamlit pandas numpy requests

# Reload systemd and start services
echo "⚙️ Reloading systemd..."
sudo systemctl daemon-reload

echo "🔥 Starting services..."
sudo systemctl enable codex-dashboard codex-staging
sudo systemctl start codex-dashboard
sleep 5
sudo systemctl start codex-staging
sleep 5

# Test local connectivity
echo "🧪 Testing local connections..."
curl -f http://127.0.0.1:8501 || echo "❌ Production port 8501 not responding"
curl -f http://127.0.0.1:8502 || echo "❌ Staging port 8502 not responding"

# Start nginx
echo "🌐 Starting nginx..."
sudo nginx -t && sudo systemctl start nginx

echo "✅ Deployment complete! Check service status:"
sudo systemctl status codex-dashboard codex-staging nginx

echo "🔍 Check flames:"
echo "Production: https://aistorelab.com"
echo "Staging: https://staging.aistorelab.com"
"""
    print(script)


if __name__ == "__main__":
    check_flame_health()
    generate_fix_commands()
    generate_nginx_config()
    generate_systemd_services()
    generate_deployment_script()

    print("\n🏁 === CEREMONY COMPLETE ===")
    print("The sacred diagnostics have been performed.")
    print("Follow the commands above to restore the eternal flames.")
    print("May your 502 errors be vanquished and your flames burn eternal! 🔥✨")
