# 🌐 Multi-Cloud Deployment Guide
# CodexDominion.app: IONOS + Azure + GitHub Automation

**Status:** Production-Ready Configuration
**Domain:** CodexDominion.app (Google Domains)
**Infrastructure:** IONOS Primary + Azure Secondary
**Automation:** GitHub Actions Push-Button Deployment

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CodexDominion.app                         │
│                  (Google Domains DNS)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────┐            ┌─────▼────┐
   │  IONOS   │            │  Azure   │
   │ Primary  │            │Secondary │
   └────┬─────┘            └─────┬────┘
        │                         │
   ┌────▼──────────┐    ┌────────▼────────┐
   │  Dashboard    │    │   AI Systems    │
   │  Analytics    │    │  Jermaine AI    │
   │  Stock Data   │    │  .300 Action    │
   │  API Gateway  │    │  Avatar System  │
   │               │    │  16 Engines     │
   └───────────────┘    └─────────────────┘
         │                       │
         └───────┬───────────────┘
                 │
        ┌────────▼────────┐
        │  GitHub Actions │
        │  Auto-Deploy    │
        └─────────────────┘
```

## 🔧 Prerequisites

### 1. IONOS Account Setup
- [x] IONOS VPS Server: `74.208.123.158`
- [x] Ubuntu 24.04 LTS installed
- [ ] SSH access configured
- [ ] Docker & Docker Compose installed
- [ ] Nginx installed

### 2. Azure Account Setup
- [x] AKS Cluster: `codex-dominion-aks`
- [x] Resource Group: `codex-dominion-rg`
- [x] LoadBalancer IP: `135.237.24.198`
- [x] kubectl configured
- [x] 16 engines running
- [x] AI trinity deployed

### 3. GitHub Repository
- [x] Repository: `JermaineMerritt-ai/codexdominion-schemas`
- [ ] GitHub Actions enabled
- [ ] Secrets configured
- [ ] Container registry access

### 4. Google Domains
- [ ] Domain: `CodexDominion.app` purchased
- [ ] DNS management access
- [ ] Nameservers configured

## 📋 Step-by-Step Setup

### Phase 1: DNS Configuration (Google Domains)

**Time: 15 minutes + 1-48 hours propagation**

1. **Login to Google Domains**
   - Go to https://domains.google.com
   - Select `CodexDominion.app`

2. **Configure DNS Records**
   ```dns
   # Root domain (multi-cloud)
   @               A       1h      74.208.123.158      # IONOS
   @               A       1h      135.237.24.198      # Azure

   # WWW redirect
   www             CNAME   1h      codexdominion.app.

   # AI Systems (Azure)
   jermaine-ai     A       1h      135.237.24.198
   dot300-ai       A       1h      135.237.24.198
   avatar          A       1h      135.237.24.198

   # Dashboard & Apps (IONOS)
   dashboard       A       1h      74.208.123.158
   api             A       1h      74.208.123.158
   stockanalytics  A       1h      74.208.123.158
   analytics       A       1h      74.208.123.158

   # Security
   @               CAA     1h      0 issue "letsencrypt.org"
   ```

3. **Save & Wait for Propagation**
   ```powershell
   # Test propagation
   nslookup codexdominion.app 8.8.8.8
   ```

📄 **Full DNS Guide:** `dns/google-domains-codexdominion-app.md`

---

### Phase 2: IONOS Server Configuration

**Time: 30-45 minutes**

#### 2.1 Initial Server Setup

```bash
# SSH into IONOS server
ssh root@74.208.123.158

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Install Nginx
apt install nginx -y

# Install Certbot for SSL
apt install certbot python3-certbot-nginx -y
```

#### 2.2 Directory Structure

```bash
# Create application directory
mkdir -p /var/www/codexdominion
cd /var/www/codexdominion

# Create required directories
mkdir -p {logs,backups,data,ssl}
```

#### 2.3 Docker Compose Configuration

Create `/var/www/codexdominion/docker-compose.production.yml`:

```yaml
version: '3.8'

services:
  dashboard:
    image: jmerritt48/codex-dashboard:latest
    container_name: codex-dashboard
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DOMAIN=codexdominion.app
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs

  api-gateway:
    image: jmerritt48/codex-api:latest
    container_name: codex-api
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - API_KEY=${API_KEY}
      - AZURE_ENDPOINT=https://jermaine-ai.codexdominion.app

  stockanalytics:
    image: jmerritt48/stock-analytics:latest
    container_name: stock-analytics
    restart: unless-stopped
    ports:
      - "8515:8515"
    volumes:
      - ./data/stocks:/app/data

networks:
  default:
    name: codex-network
```

#### 2.4 Nginx Configuration

Create `/etc/nginx/sites-available/codexdominion`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;
    return 301 https://codexdominion.app$request_uri;
}

# Main site
server {
    listen 443 ssl http2;
    server_name codexdominion.app www.codexdominion.app;

    ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Dashboard
server {
    listen 443 ssl http2;
    server_name dashboard.codexdominion.app;

    ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# API Gateway
server {
    listen 443 ssl http2;
    server_name api.codexdominion.app;

    ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }
}

# Stock Analytics
server {
    listen 443 ssl http2;
    server_name stockanalytics.codexdominion.app;

    ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;

    location / {
        proxy_pass http://localhost:8515;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### 2.5 Enable & Get SSL Certificates

```bash
# Enable site
ln -s /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/

# Test configuration
nginx -t

# Get SSL certificates (wait for DNS propagation first!)
certbot --nginx -d codexdominion.app \
    -d www.codexdominion.app \
    -d dashboard.codexdominion.app \
    -d api.codexdominion.app \
    -d stockanalytics.codexdominion.app \
    --non-interactive --agree-tos \
    -m your-email@example.com

# Reload nginx
systemctl reload nginx

# Start Docker services
docker compose -f docker-compose.production.yml up -d
```

---

### Phase 3: Azure AKS Configuration

**Time: 20 minutes**

#### 3.1 Update Ingress for New Domain

```powershell
# On your local machine
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion
```

Edit `k8s/ai-systems-ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ai-systems-ingress
  namespace: codex-governance
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - jermaine-ai.codexdominion.app
    - dot300-ai.codexdominion.app
    - avatar.codexdominion.app
    secretName: ai-systems-tls
  rules:
  - host: jermaine-ai.codexdominion.app
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: jermaine-super-action-ai
            port:
              number: 80
  - host: dot300-ai.codexdominion.app
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: dot300-action-ai
            port:
              number: 8501
  - host: avatar.codexdominion.app
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: avatar-system
            port:
              number: 8502
```

#### 3.2 Apply Updated Configuration

```powershell
# Apply ingress update
kubectl apply -f k8s/ai-systems-ingress.yaml

# Check cert-manager
kubectl get certificate -n codex-governance

# Verify ingress
kubectl describe ingress ai-systems-ingress -n codex-governance
```

---

### Phase 4: GitHub Actions Setup

**Time: 15 minutes**

#### 4.1 Configure Repository Secrets

Go to: `https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions`

Add these secrets:

| Secret Name | Value | Purpose |
|------------|-------|---------|
| `IONOS_SSH_KEY` | [Your IONOS private key] | SSH access to IONOS server |
| `AZURE_CREDENTIALS` | [Azure service principal JSON] | Azure deployment access |
| `DOCKERHUB_USERNAME` | `jmerritt48` | Docker Hub push access |
| `DOCKERHUB_TOKEN` | [Docker Hub access token] | Docker Hub authentication |

#### 4.2 Get Azure Credentials

```powershell
# Create service principal for GitHub Actions
az ad sp create-for-rbac `
    --name "github-actions-codexdominion" `
    --role contributor `
    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/codex-dominion-rg `
    --sdk-auth

# Copy the entire JSON output to AZURE_CREDENTIALS secret
```

#### 4.3 Get IONOS SSH Key

```powershell
# On your local machine, create SSH key if not exists
ssh-keygen -t ed25519 -C "github-actions@codexdominion.app" -f ~/.ssh/ionos_deploy

# Copy public key to IONOS server
cat ~/.ssh/ionos_deploy.pub | ssh root@74.208.123.158 "cat >> ~/.ssh/authorized_keys"

# Copy PRIVATE key to GitHub secret IONOS_SSH_KEY
cat ~/.ssh/ionos_deploy
```

#### 4.4 Enable Workflow

The workflow `.github/workflows/multi-cloud-deploy.yml` is already created!

**Trigger deployment:**
```bash
# Commit and push to trigger automatic deployment
git add .
git commit -m "🚀 Enable multi-cloud deployment"
git push origin main
```

Or use manual dispatch:
1. Go to **Actions** tab in GitHub
2. Select **Multi-Cloud Deployment Pipeline**
3. Click **Run workflow**
4. Choose target: `all`, `ionos`, or `azure`
5. Click **Run workflow**

---

## 🎛️ Push-Button Deployment

### Automatic Deployment (on push to main)

```bash
# Any push to main triggers full deployment
git add .
git commit -m "feat: new feature"
git push origin main

# GitHub Actions will automatically:
# ✅ Build Docker images
# ✅ Push to registries
# ✅ Deploy to IONOS
# ✅ Deploy to Azure
# ✅ Run health checks
```

### Manual Deployment

```powershell
# Via GitHub CLI
gh workflow run multi-cloud-deploy.yml \
    -f target=all \
    -f environment=production

# Or via GitHub web interface
# Actions > Multi-Cloud Deployment Pipeline > Run workflow
```

### Selective Deployment

```bash
# Deploy only to IONOS
gh workflow run multi-cloud-deploy.yml -f target=ionos

# Deploy only to Azure
gh workflow run multi-cloud-deploy.yml -f target=azure

# Deploy to staging
gh workflow run multi-cloud-deploy.yml -f environment=staging
```

---

## 🔍 Monitoring & Verification

### Check Deployment Status

```powershell
# IONOS - SSH and check
ssh root@74.208.123.158 "docker ps"

# Azure - Check pods
kubectl get pods -A

# GitHub Actions - Check workflow
gh run list --workflow=multi-cloud-deploy.yml
```

### Health Check URLs

```powershell
# Test all endpoints
$endpoints = @(
    "https://codexdominion.app",
    "https://dashboard.codexdominion.app",
    "https://jermaine-ai.codexdominion.app",
    "https://dot300-ai.codexdominion.app",
    "https://avatar.codexdominion.app",
    "https://api.codexdominion.app/health",
    "https://stockanalytics.codexdominion.app"
)

foreach ($url in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10
        Write-Host "✅ $url - $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "❌ $url - Failed" -ForegroundColor Red
    }
}
```

---

## 🚨 Troubleshooting

### DNS Not Resolving

```powershell
# Check DNS propagation
nslookup codexdominion.app 8.8.8.8

# Check from multiple locations
# Visit: https://www.whatsmydns.net/#A/codexdominion.app
```

### SSL Certificate Issues

```bash
# IONOS - Renew certificates
ssh root@74.208.123.158
certbot renew --force-renewal --nginx

# Azure - Check cert-manager
kubectl get certificate -n codex-governance
kubectl describe certificate ai-systems-tls -n codex-governance
```

### GitHub Actions Failing

```powershell
# Check workflow logs
gh run list --workflow=multi-cloud-deploy.yml
gh run view [RUN_ID] --log

# Common issues:
# - Missing secrets
# - SSH key permissions
# - Docker image not found
# - Kubernetes context not set
```

### IONOS Deployment Failed

```bash
# Check logs
ssh root@74.208.123.158
cd /var/www/codexdominion
docker-compose -f docker-compose.production.yml logs --tail=100

# Restart services
docker-compose -f docker-compose.production.yml restart

# Check Nginx
nginx -t
systemctl status nginx
```

### Azure Deployment Failed

```powershell
# Check pod status
kubectl get pods -n codex-governance
kubectl describe pod [POD_NAME] -n codex-governance
kubectl logs [POD_NAME] -n codex-governance

# Check events
kubectl get events -n codex-governance --sort-by='.lastTimestamp'

# Restart deployment
kubectl rollout restart deployment/jermaine-super-action-ai -n codex-governance
```

---

## 📊 Architecture Details

### Traffic Routing

```
User Request → codexdominion.app
    ↓
DNS Resolution (Google Domains)
    ↓
Round-Robin: 74.208.123.158 OR 135.237.24.198
    ↓
┌─────────────────┬─────────────────┐
│  IONOS          │  Azure          │
├─────────────────┼─────────────────┤
│ Dashboard       │ Jermaine AI     │
│ Stock Analytics │ .300 Action AI  │
│ API Gateway     │ Avatar System   │
│ Admin Portal    │ 16 Engines      │
└─────────────────┴─────────────────┘
```

### Load Distribution

- **IONOS (74.208.123.158):**
  - Public-facing dashboard
  - Stock analytics platform
  - Business applications
  - API gateway

- **Azure (135.237.24.198):**
  - AI Trinity (Jermaine, .300 Action, Avatar)
  - 16 computational engines
  - Backend processing
  - Internal services

### Failover Strategy

1. **DNS-Level:** Multiple A records for automatic failover
2. **API Gateway:** Routes to healthy backends
3. **Health Checks:** GitHub Actions monitors endpoints
4. **Auto-Recovery:** Docker restart policies + Kubernetes self-healing

---

## 🎯 Next Steps

### Immediate (Before Go-Live)
- [ ] Purchase `CodexDominion.app` domain
- [ ] Configure DNS records in Google Domains
- [ ] Wait 24-48 hours for DNS propagation
- [ ] Add GitHub secrets
- [ ] Run test deployment to staging
- [ ] Verify SSL certificates
- [ ] Test all endpoints

### Phase 2 (Week 2)
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure automated backups
- [ ] Add CloudFlare CDN
- [ ] Implement rate limiting
- [ ] Set up logging aggregation

### Phase 3 (Month 1)
- [ ] Add geographic load balancing
- [ ] Implement blue-green deployments
- [ ] Add chaos engineering tests
- [ ] Optimize Docker images
- [ ] Add A/B testing capability

---

## 📚 Documentation Files

- **DNS Configuration:** `dns/google-domains-codexdominion-app.md`
- **GitHub Workflow:** `.github/workflows/multi-cloud-deploy.yml`
- **IONOS Setup:** `docs/ionos-server-setup.md` (to be created)
- **Azure Setup:** `docs/azure-aks-setup.md` (to be created)
- **Deployment Guide:** This file

---

## 🔥 Quick Start Checklist

```
🎯 Multi-Cloud Deployment - Quick Start

Prerequisites:
[ ] Domain purchased: CodexDominion.app
[ ] IONOS VPS accessible: 74.208.123.158
[ ] Azure AKS running: codex-dominion-aks
[ ] GitHub repository configured
[ ] Docker Hub account: jmerritt48

Phase 1 - DNS (15 min):
[ ] Login to Google Domains
[ ] Add A records for IONOS & Azure
[ ] Add subdomain records
[ ] Add CAA records for SSL
[ ] Wait 1-48 hours for propagation

Phase 2 - IONOS (45 min):
[ ] SSH into server
[ ] Install Docker + Nginx
[ ] Create directory structure
[ ] Deploy docker-compose.yml
[ ] Configure Nginx
[ ] Get SSL certificates
[ ] Start services

Phase 3 - Azure (20 min):
[ ] Update ingress hostnames
[ ] Apply Kubernetes manifests
[ ] Verify cert-manager
[ ] Check pod status
[ ] Test LoadBalancer

Phase 4 - GitHub (15 min):
[ ] Add IONOS_SSH_KEY secret
[ ] Add AZURE_CREDENTIALS secret
[ ] Add DOCKERHUB secrets
[ ] Enable workflow
[ ] Test deployment

Phase 5 - Verification:
[ ] Test all HTTPS endpoints
[ ] Verify SSL certificates
[ ] Check GitHub Actions logs
[ ] Monitor health endpoints
[ ] Document any issues

🎉 Go Live!
[ ] Switch production traffic
[ ] Monitor for 24 hours
[ ] Celebrate! 🚀
```

---

**Deployment Status:** Configuration Complete - Ready for Domain Purchase
**Next Action:** Purchase CodexDominion.app and configure DNS
**Estimated Total Setup Time:** 2-3 hours + DNS propagation
**Support Contact:** GitHub Issues or jmerritt48@codexdominion.app
