# Commands to run on IONOS server (via SSH: ssh root@74.208.123.158)

# 1. Stop nginx temporarily
sudo systemctl stop nginx

# 2. Delete any existing certificates for this domain
sudo certbot delete --cert-name codexdominion.app 2>/dev/null
sudo certbot delete --cert-name www.codexdominion.app 2>/dev/null

# 3. Get a fresh certificate using standalone mode (since nginx is stopped)
sudo certbot certonly --standalone -d www.codexdominion.app --non-interactive --agree-tos --email admin@codexdominion.app

# 4. Update nginx configuration to use the new certificate
sudo tee /etc/nginx/sites-available/codexdominion > /dev/null << 'EOF'
server {
    listen 80;
    server_name www.codexdominion.app;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.codexdominion.app;

    ssl_certificate /etc/letsencrypt/live/www.codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.codexdominion.app/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# 5. Test nginx configuration
sudo nginx -t

# 6. Start nginx
sudo systemctl start nginx

# 7. Check certificate
sudo certbot certificates

# 8. Test the site
curl -I https://www.codexdominion.app

echo ""
echo "✅ SSL should now be working!"
echo "Visit: https://www.codexdominion.app"
