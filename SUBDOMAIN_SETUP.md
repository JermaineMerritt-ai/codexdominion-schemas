# Subdomain Setup Guide for CodexDominion.app

## Quick Setup Instructions

### Step 1: Add DNS A Records

Go to your DNS provider and add these A records:

| Type | Name       | Value           | TTL  |
|------|------------|-----------------|------|
| A    | api        | 74.208.123.158  | 3600 |
| A    | dashboard  | 74.208.123.158  | 3600 |
| A    | monitoring | 74.208.123.158  | 3600 |

**DNS Providers:**
- **Google Domains**: https://domains.google.com → Select codexdominion.app → DNS
- **Cloudflare**: https://dash.cloudflare.com → Select codexdominion.app → DNS → Records

### Step 2: Wait for DNS Propagation (5-15 minutes)

Verify DNS is working:
```bash
nslookup api.codexdominion.app 8.8.8.8
nslookup dashboard.codexdominion.app 8.8.8.8
nslookup monitoring.codexdominion.app 8.8.8.8
```

### Step 3: Run Deployment Script on Server

```bash
# SSH into your server
ssh root@74.208.123.158

# Upload and run the deployment script
chmod +x deploy-subdomains.sh
./deploy-subdomains.sh
```

## What Each Subdomain Will Do

### api.codexdominion.app
- **Purpose**: Backend API endpoints
- **Proxies to**: localhost:8000
- **Use for**: REST API, GraphQL, webhooks

### dashboard.codexdominion.app
- **Purpose**: Admin/analytics dashboard
- **Proxies to**: localhost:8501
- **Use for**: Streamlit dashboard, admin panel

### monitoring.codexdominion.app
- **Purpose**: System monitoring and metrics
- **Proxies to**: localhost:9090
- **Use for**: Prometheus, Grafana, health checks

## Manual Setup (if script fails)

### Create nginx configs manually:

```bash
# API subdomain
cat > /etc/nginx/sites-available/api.codexdominion.app << 'EOF'
server {
    listen 80;
    server_name api.codexdominion.app;
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/api.codexdominion.app /etc/nginx/sites-enabled/
```

### Get SSL certificates:

```bash
certbot --nginx -d api.codexdominion.app
certbot --nginx -d dashboard.codexdominion.app
certbot --nginx -d monitoring.codexdominion.app
```

## Troubleshooting

### DNS not resolving
- Wait 15 minutes for propagation
- Clear DNS cache: `ipconfig /flushdns` (Windows) or `sudo systemd-resolve --flush-caches` (Linux)
- Check with multiple DNS servers: `nslookup subdomain.codexdominion.app 1.1.1.1`

### Nginx configuration errors
- Test config: `nginx -t`
- Check logs: `tail -f /var/log/nginx/error.log`
- Verify port isn't already in use: `netstat -tlnp | grep :8000`

### SSL certificate issues
- Ensure DNS is fully propagated first
- Check Let's Encrypt rate limits: https://letsencrypt.org/docs/rate-limits/
- Try certbot in staging mode first: `certbot --nginx -d api.codexdominion.app --staging`

## Verification Commands

```bash
# Check DNS
nslookup api.codexdominion.app

# Check nginx config
nginx -t

# Check if services are running
curl http://localhost:8000
curl http://localhost:8501
curl http://localhost:9090

# Test HTTPS
curl -I https://api.codexdominion.app
curl -I https://dashboard.codexdominion.app
curl -I https://monitoring.codexdominion.app
```
