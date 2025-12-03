# 🚀 CodexDominion.app - Quick Deployment Guide

**One-Page Reference for Multi-Cloud Setup**

---

## 📋 Pre-Flight Checklist

```bash
# Required Accounts & Access
✅ Google Domains account (for CodexDominion.app)
✅ IONOS VPS: 74.208.123.158 (SSH access)
✅ Azure AKS: codex-dominion-aks (kubectl access)
✅ GitHub: JermaineMerritt-ai/codexdominion-schemas
✅ Docker Hub: jmerritt48
```

---

## ⚡ Quick Setup Commands

### 1️⃣ Configure DNS (Google Domains)
```dns
# Root domain - Multi-cloud
@               A       1h      74.208.123.158      # IONOS
@               A       1h      135.237.24.198      # Azure

# AI Systems - Azure
jermaine-ai     A       1h      135.237.24.198
dot300-ai       A       1h      135.237.24.198
avatar          A       1h      135.237.24.198

# Apps - IONOS
dashboard       A       1h      74.208.123.158
api             A       1h      74.208.123.158
stockanalytics  A       1h      74.208.123.158

# WWW redirect
www             CNAME   1h      codexdominion.app.

# Security
@               CAA     1h      0 issue "letsencrypt.org"
```

⏱️ **Wait 1-48 hours for DNS propagation**

---

### 2️⃣ Setup IONOS Server

```bash
# SSH into IONOS
ssh root@74.208.123.158

# Download and run setup script
curl -o setup.sh https://raw.githubusercontent.com/JermaineMerritt-ai/codexdominion-schemas/main/scripts/setup-ionos-server.sh
chmod +x setup.sh
./setup.sh

# Wait for DNS propagation, then get SSL certificates
certbot --nginx -d codexdominion.app \
    -d www.codexdominion.app \
    -d dashboard.codexdominion.app \
    -d api.codexdominion.app \
    -d stockanalytics.codexdominion.app \
    --non-interactive --agree-tos \
    -m your-email@example.com

# Configure environment
cd /var/www/codexdominion
cp .env.template .env
nano .env  # Edit with your credentials

# Deploy
./deploy.sh
```

---

### 3️⃣ Update Azure AKS

```powershell
# On your local machine
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion

# Update ingress for new domain
kubectl apply -f k8s/ai-systems-ingress.yaml

# Verify
kubectl get ingress -n codex-governance
kubectl get certificate -n codex-governance
```

---

### 4️⃣ Setup GitHub Actions

#### Add Secrets
Go to: `https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions`

```bash
# Generate Azure credentials
az ad sp create-for-rbac --name "github-actions-codexdominion" \
    --role contributor \
    --scopes /subscriptions/YOUR_SUB_ID/resourceGroups/codex-dominion-rg \
    --sdk-auth
# Copy output to AZURE_CREDENTIALS secret

# Generate SSH key for IONOS
ssh-keygen -t ed25519 -C "github@codexdominion.app" -f ~/.ssh/ionos_deploy
cat ~/.ssh/ionos_deploy.pub | ssh root@74.208.123.158 "cat >> ~/.ssh/authorized_keys"
cat ~/.ssh/ionos_deploy  # Copy to IONOS_SSH_KEY secret
```

#### Deploy!
```bash
# Automatic on push
git add .
git commit -m "🚀 Deploy CodexDominion.app"
git push origin main

# Or manual via GitHub Actions UI
# Actions > Multi-Cloud Deployment Pipeline > Run workflow
```

---

## 🔍 Verification Commands

### Test DNS
```powershell
nslookup codexdominion.app 8.8.8.8
nslookup jermaine-ai.codexdominion.app 8.8.8.8
```

### Test IONOS
```bash
ssh root@74.208.123.158
docker ps
curl http://localhost:3000/health
systemctl status nginx
```

### Test Azure
```powershell
kubectl get pods -n codex-governance
kubectl get ingress -n codex-governance
kubectl get certificate -n codex-governance
```

### Test URLs (after SSL)
```powershell
curl -I https://codexdominion.app
curl -I https://dashboard.codexdominion.app
curl -I https://jermaine-ai.codexdominion.app
curl -I https://dot300-ai.codexdominion.app
curl -I https://avatar.codexdominion.app
```

---

## 🚨 Common Issues

### DNS Not Resolving
```powershell
# Check propagation status
# Visit: https://www.whatsmydns.net/#A/codexdominion.app
```

### SSL Certificate Failed
```bash
# IONOS - Manual certificate
ssh root@74.208.123.158
certbot renew --force-renewal --nginx

# Azure - Check cert-manager
kubectl describe certificate ai-systems-tls -n codex-governance
```

### GitHub Actions Failed
```powershell
# View logs
gh run list --workflow=multi-cloud-deploy.yml
gh run view --log

# Common fixes:
# - Check secrets are set
# - Verify SSH key format (no password, correct format)
# - Ensure Azure credentials JSON is valid
```

### IONOS Services Not Starting
```bash
ssh root@74.208.123.158
cd /var/www/codexdominion

# View logs
docker-compose -f docker-compose.production.yml logs --tail=100

# Restart
docker-compose -f docker-compose.production.yml restart

# Full rebuild
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --build
```

---

## 📊 Service URLs

| Service | URL | Hosted On |
|---------|-----|-----------|
| Main Site | https://codexdominion.app | IONOS |
| Dashboard | https://dashboard.codexdominion.app | IONOS |
| API Gateway | https://api.codexdominion.app | IONOS |
| Stock Analytics | https://stockanalytics.codexdominion.app | IONOS |
| Jermaine AI | https://jermaine-ai.codexdominion.app | Azure |
| .300 Action AI | https://dot300-ai.codexdominion.app | Azure |
| Avatar System | https://avatar.codexdominion.app | Azure |

---

## 📚 Full Documentation

- **Complete Guide:** `MULTI_CLOUD_DEPLOYMENT_GUIDE.md`
- **DNS Details:** `dns/google-domains-codexdominion-app.md`
- **GitHub Workflow:** `.github/workflows/multi-cloud-deploy.yml`
- **Docker Config:** `docker-compose.production.yml`
- **IONOS Setup:** `scripts/setup-ionos-server.sh`

---

## 🎯 Deployment Flow

```
┌─────────────────────┐
│  Push to GitHub     │
│  (main branch)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  GitHub Actions     │
│  Triggers           │
└──────────┬──────────┘
           │
      ┌────┴────┐
      ▼         ▼
┌──────────┐ ┌──────────┐
│  Build   │ │  Build   │
│  Docker  │ │  Docker  │
│  Images  │ │  Images  │
└────┬─────┘ └─────┬────┘
     │             │
     ▼             ▼
┌──────────┐ ┌──────────┐
│  Deploy  │ │  Deploy  │
│  IONOS   │ │  Azure   │
│  (SSH)   │ │  (kubectl)│
└────┬─────┘ └─────┬────┘
     │             │
     └──────┬──────┘
            ▼
    ┌───────────────┐
    │  Update DNS   │
    │  Verify SSL   │
    │  Run Tests    │
    └───────────────┘
```

---

## ⏱️ Timeline

| Phase | Duration | Can Start |
|-------|----------|-----------|
| DNS Setup | 15 min | Immediately |
| DNS Propagation | 1-48 hrs | After DNS setup |
| IONOS Setup | 45 min | After DNS propagation |
| Azure Update | 20 min | Anytime |
| GitHub Setup | 15 min | Anytime |
| First Deployment | 10 min | After all above |
| **Total Active Time** | **~2 hours** | |
| **Total Calendar Time** | **1-2 days** | (DNS wait) |

---

## 🔥 Quick Deploy Script

Save as `quick-deploy.ps1`:

```powershell
#!/usr/bin/env pwsh

Write-Host "🚀 CodexDominion.app Quick Deploy" -ForegroundColor Cyan

# Check prerequisites
Write-Host "`n✅ Checking prerequisites..." -ForegroundColor Yellow
$checks = @{
    "kubectl" = "kubectl version --client"
    "git" = "git --version"
    "az" = "az --version"
}

foreach ($tool in $checks.Keys) {
    try {
        Invoke-Expression $checks[$tool] | Out-Null
        Write-Host "  ✓ $tool installed" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ $tool missing" -ForegroundColor Red
    }
}

# Update Azure
Write-Host "`n☁️ Updating Azure AKS..." -ForegroundColor Yellow
kubectl apply -f k8s/ai-systems-ingress.yaml
Write-Host "  ✓ Azure ingress updated" -ForegroundColor Green

# Commit and deploy
Write-Host "`n📤 Deploying via GitHub Actions..." -ForegroundColor Yellow
git add .
git commit -m "🚀 Deploy $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main
Write-Host "  ✓ Pushed to GitHub" -ForegroundColor Green

Write-Host "`n🎉 Deployment initiated!" -ForegroundColor Green
Write-Host "   Monitor: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions"
```

---

**Ready to deploy? Follow the steps above!** 🚀

For detailed troubleshooting, see `MULTI_CLOUD_DEPLOYMENT_GUIDE.md`
