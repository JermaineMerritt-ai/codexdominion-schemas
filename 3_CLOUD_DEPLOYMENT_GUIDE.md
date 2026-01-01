# 🔥 Codex Dominion - 3-Cloud Deployment Guide

## Overview

Your production system is deployed across **three cloud providers** for maximum reliability and performance:

### 1️⃣ **AZURE** - Backend API (Flask + Gunicorn)
- **Service**: Azure Container Apps
- **Auto-scaling**: 1-5 instances based on load
- **Health checks**: Automatic restart on failure
- **HTTPS**: Automatically provisioned SSL certificates
- **Cost**: ~$30-50/month

### 2️⃣ **IONOS** - Frontend Dashboard (Next.js)
- **Service**: VPS with PM2 process manager
- **European delivery**: Fast access for EU users
- **Auto-restart**: PM2 monitors and restarts on crash
- **Custom domain**: Easy DNS configuration
- **Cost**: Your existing VPS plan

### 3️⃣ **GOOGLE CLOUD** - Creative Engine (AI Pipelines)
- **Service**: Cloud Run + Vertex AI
- **Unlimited scaling**: Handles any AI workload
- **ML APIs**: Pre-trained models + custom models
- **Pay-per-use**: Only pay when processing
- **Cost**: Usage-based (~$20-100/month)

---

## Quick Start

### Prerequisites

Install required CLIs:

```powershell
# Azure CLI
winget install Microsoft.AzureCLI

# Google Cloud SDK
# Download: https://cloud.google.com/sdk/docs/install

# SSH (usually pre-installed on Windows 10+)
Get-Command ssh
```

### Configuration

1. **Copy environment template:**
```powershell
Copy-Item .env.3cloud.example .env.production
```

2. **Edit `.env.production` with your credentials:**
   - Azure subscription ID
   - IONOS server IP and SSH key
   - GCP project ID

3. **Deploy everything:**
```powershell
.\DEPLOY_3_CLOUD_PRODUCTION.ps1
```

That's it! Your system is now crash-proof and running on three continents.

---

## Deployment Options

### Full Deployment (All 3 Clouds)
```powershell
.\DEPLOY_3_CLOUD_PRODUCTION.ps1
```

### Azure Only (Backend)
```powershell
.\DEPLOY_3_CLOUD_PRODUCTION.ps1 -SkipIONOS -SkipGCP
```

### IONOS Only (Frontend)
```powershell
.\DEPLOY_3_CLOUD_PRODUCTION.ps1 -SkipAzure -SkipGCP
```

### GCP Only (Creative Engine)
```powershell
.\DEPLOY_3_CLOUD_PRODUCTION.ps1 -SkipAzure -SkipIONOS
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    CODEX DOMINION                        │
│                  3-Cloud Architecture                    │
└─────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   IONOS VPS  │      │    AZURE     │      │ GOOGLE CLOUD │
│   (Europe)   │◄────►│  (US East)   │◄────►│  (US Central)│
└──────────────┘      └──────────────┘      └──────────────┘
       │                      │                      │
   Next.js              Flask API             Creative AI
  Dashboard            + Gunicorn            + Vertex AI
       │                      │                      │
       └──────────────────────┴──────────────────────┘
                              │
                        User Browser
```

**Data Flow:**
1. User loads dashboard from **IONOS** (fast European delivery)
2. Dashboard calls backend API on **AZURE** (crash-proof, auto-scaling)
3. Backend triggers AI jobs on **GOOGLE CLOUD** (unlimited ML power)
4. Results flow back: GCP → Azure → IONOS → User

---

## What Each Cloud Does

### 🔵 AZURE (Backend API)

**Purpose:** Rock-solid backend that never crashes

**Technology Stack:**
- Azure Container Apps (Docker containers)
- Azure Container Registry (image storage)
- Auto-scaling (1-5 instances)
- Managed HTTPS certificates
- Health monitoring

**What runs here:**
- Flask dashboard backend (`flask_dashboard.py`)
- All API endpoints (`/api/*`)
- Database (SQLite or PostgreSQL)
- Automation engines
- WebSocket connections

**Monitoring:**
```powershell
az containerapp logs show --name codex-backend --resource-group codex-dominion-rg --follow
```

**Restart:**
```powershell
az containerapp restart --name codex-backend --resource-group codex-dominion-rg
```

---

### 🟢 IONOS (Frontend Dashboard)

**Purpose:** Fast, reliable dashboard access

**Technology Stack:**
- Ubuntu VPS
- PM2 process manager
- Nginx reverse proxy (optional)
- Next.js production build
- Node.js 18+

**What runs here:**
- Next.js dashboard (`dashboard-app/`)
- Static assets
- Client-side routing
- Real-time UI updates

**Monitoring:**
```bash
ssh root@your_ionos_ip
pm2 status
pm2 logs codex-frontend
```

**Restart:**
```bash
ssh root@your_ionos_ip
pm2 restart codex-frontend
```

---

### 🔴 GOOGLE CLOUD (Creative Engine)

**Purpose:** Unlimited AI/ML processing power

**Technology Stack:**
- Cloud Run (serverless containers)
- Vertex AI (ML training/serving)
- Cloud Storage (data/models)
- Pub/Sub (event streaming)
- BigQuery (analytics)

**What runs here:**
- AI prompt processing
- Image generation
- Video synthesis
- Content analysis
- Data pipelines
- ML model training

**Monitoring:**
```powershell
gcloud run services logs read codex-creative-engine --region us-central1 --limit 50
```

**Restart:**
```powershell
gcloud run services update codex-creative-engine --region us-central1
```

---

## Cost Breakdown

| Cloud | Service | Monthly Cost | What You Get |
|-------|---------|--------------|--------------|
| **AZURE** | Container Apps | $30-50 | Auto-scaling backend, 1-5 instances |
| **IONOS** | VPS | $10-30 | Your existing server, no extra cost |
| **GCP** | Cloud Run + AI | $20-100 | Pay-per-use, unlimited scale |
| **TOTAL** | | **$60-180/month** | Crash-proof, global, unlimited AI |

**Free Tiers:**
- Azure: $200 credit for 30 days (new accounts)
- GCP: $300 credit for 90 days (new accounts)
- **First 3 months could be FREE!**

---

## Security

### HTTPS/SSL
- **Azure**: Automatic SSL via Container Apps
- **IONOS**: Use Let's Encrypt (free) with Certbot
- **GCP**: Automatic SSL via Cloud Run

### Secrets Management
- **Azure**: Key Vault integration
- **IONOS**: Environment files (`.env`)
- **GCP**: Secret Manager

### Authentication
- Configure in `.env.production`
- Use strong secrets for `SECRET_KEY`
- Enable OAuth2 for API access (optional)

---

## Monitoring & Alerts

### Health Checks

Test all services:
```powershell
# Azure Backend
curl https://your-backend.azurecontainerapps.io/health

# IONOS Frontend
curl http://your_ionos_ip:3000

# GCP Creative Engine
curl https://your-service.run.app/health
```

### Log Aggregation

Centralize logs (optional):
```powershell
# Install Papertrail, Datadog, or New Relic
# Configure forwarding from all 3 clouds
```

### Uptime Monitoring

Use free services:
- **UptimeRobot** (50 monitors free)
- **Pingdom** (1 monitor free)
- **StatusCake** (10 monitors free)

---

## Scaling

### Azure (Backend)
Already auto-scales 1-5 instances. To increase:
```powershell
az containerapp update --name codex-backend `
  --min-replicas 2 `
  --max-replicas 10 `
  --resource-group codex-dominion-rg
```

### IONOS (Frontend)
Add more VPS instances + load balancer:
```bash
# On IONOS, add second server
# Configure nginx load balancer
```

### GCP (Creative Engine)
Already unlimited. Adjust max instances:
```powershell
gcloud run services update codex-creative-engine `
  --max-instances 50 `
  --region us-central1
```

---

## Troubleshooting

### Azure Backend Not Responding

```powershell
# Check logs
az containerapp logs show --name codex-backend --resource-group codex-dominion-rg --follow

# Check status
az containerapp show --name codex-backend --resource-group codex-dominion-rg

# Restart
az containerapp restart --name codex-backend --resource-group codex-dominion-rg
```

### IONOS Frontend Down

```bash
# SSH to server
ssh root@your_ionos_ip

# Check PM2 status
pm2 status

# View logs
pm2 logs codex-frontend --err

# Restart
pm2 restart codex-frontend

# If Node.js crashed
cd /var/www/codex-frontend
npm install
pm2 restart codex-frontend
```

### GCP Service Errors

```powershell
# Check logs
gcloud run services logs read codex-creative-engine --region us-central1 --limit 100

# Check service health
gcloud run services describe codex-creative-engine --region us-central1

# Redeploy
gcloud run services update codex-creative-engine --region us-central1
```

---

## CI/CD Integration

### GitHub Actions (Automated Deployment)

Create `.github/workflows/deploy-3cloud.yml`:

```yaml
name: Deploy 3-Cloud Production

on:
  push:
    branches: [main]

jobs:
  deploy-azure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - run: |
          az containerapp update --name codex-backend \
            --resource-group codex-dominion-rg \
            --image codexdominionacr.azurecr.io/codex-backend:latest

  deploy-ionos:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: |
          cd dashboard-app
          npm run build
          scp -r .next ${{ secrets.IONOS_USER }}@${{ secrets.IONOS_SERVER }}:/var/www/codex-frontend/

  deploy-gcp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      - run: |
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/codex-creative-engine
          gcloud run deploy codex-creative-engine --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/codex-creative-engine
```

---

## Migration from Local

### Step 1: Backup Local Data

```powershell
# Backup database
Copy-Item codex.db codex.db.backup

# Backup environment
Copy-Item .env.production .env.production.backup
```

### Step 2: Deploy to Clouds

```powershell
.\DEPLOY_3_CLOUD_PRODUCTION.ps1
```

### Step 3: Migrate Database

```powershell
# Upload database to Azure
az containerapp exec --name codex-backend --resource-group codex-dominion-rg `
  --command "/bin/bash"

# Inside container:
# Upload your codex.db file via SCP or Azure Storage
```

### Step 4: Update DNS

Point your domain to production:
- `api.codexdominion.app` → Azure backend
- `dashboard.codexdominion.app` → IONOS frontend
- `ai.codexdominion.app` → GCP service

---

## Benefits of 3-Cloud Setup

✅ **Crash-proof**: If one cloud fails, others keep running  
✅ **Auto-scaling**: Handle traffic spikes automatically  
✅ **Global reach**: Fast access from anywhere  
✅ **Cost-optimized**: Pay only for what you use  
✅ **Unlimited AI**: No limits on ML processing  
✅ **Auto-restart**: Failed services restart automatically  
✅ **99.9% uptime**: Enterprise-grade reliability  
✅ **Easy monitoring**: Centralized logs and metrics  

---

## Support

**Documentation:**
- Azure: https://docs.microsoft.com/azure
- IONOS: https://www.ionos.com/help
- GCP: https://cloud.google.com/docs

**Community:**
- GitHub Issues: Your repo issues page
- Discord: Create a support channel

---

## Next Steps

1. ✅ Deploy to all 3 clouds
2. ⏳ Configure custom domains
3. ⏳ Set up monitoring alerts
4. ⏳ Enable CI/CD auto-deployment
5. ⏳ Add database backups
6. ⏳ Configure CDN (optional)

**Your system is now production-ready and crash-proof!** 🔥👑
