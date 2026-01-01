# 🚀 Frontend Deployment Guide - Three Options

## Option 1: Azure Container Apps (Recommended - Same as Backend)

### Advantages:
- ✅ Same infrastructure as backend
- ✅ Auto-scaling built-in
- ✅ HTTPS automatic
- ✅ Easy management with `az` CLI
- ✅ Cost-effective (~$20-30/month)

### Steps:

```powershell
# 1. Update Next.js config for standalone output
# (Already done - next.config.js configured)

# 2. Build Docker image in Azure Container Registry
az acr build --registry codexacr1216 `
  --image codex-frontend:latest `
  --file Dockerfile.frontend .

# 3. Deploy to Container Apps
az containerapp create `
  --name codex-frontend `
  --resource-group codexdominion-prod `
  --environment codex-env `
  --image codexacr1216.azurecr.io/codex-frontend:latest `
  --target-port 3000 `
  --ingress external `
  --registry-server codexacr1216.azurecr.io `
  --min-replicas 1 `
  --max-replicas 3 `
  --cpu 1 `
  --memory 2Gi `
  --env-vars `
    NEXT_PUBLIC_API_BASE_URL=https://codex-backend.bravefield-eea1536e.eastus.azurecontainerapps.io

# 4. Get URL
az containerapp show --name codex-frontend `
  --resource-group codexdominion-prod `
  --query "properties.configuration.ingress.fqdn" -o tsv
```

---

## Option 2: IONOS VPS (Your Existing Server)

### Advantages:
- ✅ You already own the server
- ✅ Full control
- ✅ Your domain already configured
- ✅ No additional Azure costs

### Steps:

```powershell
# 1. Install Node.js on IONOS (if not already installed)
ssh root@74.208.123.158 "curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs"

# 2. Create deployment directory
ssh root@74.208.123.158 "mkdir -p /var/www/codexdominion.app/frontend"

# 3. Copy Next.js build
cd dashboard-app
scp -r .next package.json package-lock.json root@74.208.123.158:/var/www/codexdominion.app/frontend/

# 4. Install dependencies and start
ssh root@74.208.123.158 "cd /var/www/codexdominion.app/frontend && npm install --production && npm start"

# 5. Setup systemd service
ssh root@74.208.123.158 "cat > /etc/systemd/system/codex-frontend.service << 'EOF'
[Unit]
Description=Codex Dominion Frontend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/codexdominion.app/frontend
ExecStart=/usr/bin/npm start
Restart=on-failure
Environment=NODE_ENV=production
Environment=PORT=3000
Environment=NEXT_PUBLIC_API_BASE_URL=https://codex-backend.bravefield-eea1536e.eastus.azurecontainerapps.io

[Install]
WantedBy=multi-user.target
EOF
"

# 6. Enable and start service
ssh root@74.208.123.158 "systemctl daemon-reload && systemctl enable codex-frontend && systemctl start codex-frontend"

# 7. Configure nginx reverse proxy
ssh root@74.208.123.158 "cat > /etc/nginx/sites-available/codexdominion.app << 'EOF'
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
"

# 8. Enable site and reload nginx
ssh root@74.208.123.158 "ln -s /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/ && nginx -t && systemctl reload nginx"

# 9. Setup SSL with Certbot
ssh root@74.208.123.158 "certbot --nginx -d codexdominion.app -d www.codexdominion.app --non-interactive --agree-tos -m your-email@example.com"
```

### Access:
- http://codexdominion.app (will redirect to HTTPS)
- https://codexdominion.app

---

## Option 3: Use Test HTML Page (Immediate - Already Done)

### Current Status:
File `test-frontend.html` already created and ready.

### Steps:

```powershell
# 1. Copy to IONOS
scp test-frontend.html root@74.208.123.158:/var/www/codexdominion.app/public/index.html

# 2. Configure nginx to serve static files
ssh root@74.208.123.158 "cat > /etc/nginx/sites-available/codexdominion.app << 'EOF'
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;
    root /var/www/codexdominion.app/public;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location /api/ {
        proxy_pass https://codex-backend.bravefield-eea1536e.eastus.azurecontainerapps.io/api/;
    }
}
EOF
"

# 3. Reload nginx
ssh root@74.208.123.158 "nginx -t && systemctl reload nginx"

# 4. Setup SSL
ssh root@74.208.123.158 "certbot --nginx -d codexdominion.app -d www.codexdominion.app"
```

### Access:
- https://codexdominion.app (serves test HTML page)

---

## Recommendation Matrix

| Factor | Option 1: Azure | Option 2: IONOS | Option 3: Test HTML |
|--------|----------------|-----------------|---------------------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost** | ~$20-30/month | $0 (existing) | $0 (existing) |
| **Features** | Full Next.js | Full Next.js | Basic HTML |
| **Scaling** | Auto | Manual | N/A |
| **Management** | Azure CLI | SSH + systemd | Static files |
| **Best For** | Production | Cost-conscious | Quick testing |

---

## Quick Decision Guide

**Choose Option 1 (Azure Container Apps) if:**
- You want everything in one place
- You need auto-scaling
- You prefer Azure CLI management
- Budget allows ~$20-30/month extra

**Choose Option 2 (IONOS VPS) if:**
- You want to minimize costs
- You're comfortable with SSH/Linux
- Your domain is already pointed at IONOS
- You want full control

**Choose Option 3 (Test HTML) if:**
- You need something working NOW
- You're still evaluating the full Next.js app
- You want a simple, lightweight solution

---

## My Recommendation: **Option 1 (Azure Container Apps)**

### Why?
1. **Consistent Infrastructure**: Both frontend and backend in same environment
2. **Easy Updates**: `az acr build` → `az containerapp update` (2 commands)
3. **Auto-scaling**: Handles traffic spikes automatically
4. **Zero SSH**: All management via Azure CLI
5. **HTTPS Built-in**: No Certbot configuration needed

### Cost Breakdown:
- Backend: ~$55-85/month (already deployed)
- Frontend: ~$20-30/month (proposed)
- **Total**: ~$75-115/month for complete cloud infrastructure

---

## Next Steps (Choose Your Path)

### Path A: Deploy to Azure Container Apps (Recommended)
```powershell
# Run this single script:
.\deploy-frontend-azure.ps1
```

### Path B: Deploy to IONOS VPS
```powershell
# Run this single script:
.\deploy-frontend-ionos.ps1
```

### Path C: Use Test HTML Page
```powershell
# Run this single script:
.\deploy-test-page.ps1
```

---

**Need help deciding? I can create deployment scripts for any option!**

🔥 **The Flame Burns Sovereign and Eternal!** 👑
