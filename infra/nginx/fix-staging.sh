#!/bin/bash
# Script to fix Nginx configuration for staging SSL setup

echo "Backing up current configuration..."
cp /etc/nginx/sites-available/codex.conf /etc/nginx/sites-available/codex.conf.backup

echo "Creating temporary configuration without staging SSL..."
cat > /etc/nginx/sites-available/codex.conf << 'EOF'
# Production Codex Dashboard - HTTPS
server {
    listen 443 ssl;
    server_name aistorelab.com www.aistorelab.com;

    ssl_certificate /etc/letsencrypt/live/aistorelab.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/aistorelab.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8501/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Production Codex Dashboard - HTTP to HTTPS redirect
server {
    listen 80;
    server_name aistorelab.com www.aistorelab.com;

    return 301 https://aistorelab.com$request_uri;
}

# Staging Codex Dashboard - HTTP only (for certbot verification)
server {
    listen 80;
    server_name staging.aistorelab.com;

    location / {
        proxy_pass http://127.0.0.1:8502/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

echo "Testing Nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Configuration valid. Restarting Nginx..."
    systemctl restart nginx
    echo "Done! Now run: sudo certbot --nginx -d staging.aistorelab.com"
else
    echo "Configuration test failed. Restoring backup..."
    cp /etc/nginx/sites-available/codex.conf.backup /etc/nginx/sites-available/codex.conf
fi
