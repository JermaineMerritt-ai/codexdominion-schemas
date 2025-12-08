# Azure CI/CD Architecture - Codex Dominion

## 🏗️ Complete Deployment Pipeline

```
GitHub Repository (main branch)
        │
        │
        ├─────────────────────────────────────────────────────────────┐
        │                                                               │
        ▼                                                               ▼
┌─────────────────────┐                                   ┌─────────────────────┐
│  Frontend Workflow  │                                   │  Backend Workflow   │
│  (Auto-trigger)     │                                   │  (Auto-trigger)     │
└─────────────────────┘                                   └─────────────────────┘
        │                                                               │
        │ Trigger: Push to main                                        │ Trigger: Push to main
        │ Path: any file                                               │ Path: src/backend/**
        │                                                               │
        ├──► 1. Checkout code                                         ├──► 1. Checkout code
        ├──► 2. Setup Node.js 18                                      ├──► 2. Azure Login
        ├──► 3. npm ci                                                ├──► 3. ACR Login
        ├──► 4. npm run build                                         ├──► 4. Docker Build
        ├──► 5. Deploy to Static Web Apps                             │      └─► codexdominionacr.azurecr.io/
        │                                                               │          codex-backend:$SHA
        │                                                               │          codex-backend:latest
        ▼                                                               │
┌─────────────────────┐                                               ├──► 5. Push to ACR
│ Azure Static Web    │                                               ├──► 6. Delete old Container Instance
│ Apps (Free Tier)    │                                               ├──► 7. Create new Container Instance
├─────────────────────┤                                               ├──► 8. Health Check Verification
│ ✅ HTTPS Automatic   │                                               │
│ ✅ Global CDN        │                                               ▼
│ ✅ Custom Domain     │                                   ┌─────────────────────┐
│ ✅ $0/month          │                                   │ Azure Container     │
│                      │                                   │ Instances           │
│ URL:                 │                                   ├─────────────────────┤
│ happy-flower-...     │                                   │ ✅ FastAPI Backend   │
│ eastus2.3.azure...   │                                   │ ✅ 1 vCPU, 1GB RAM   │
└─────────────────────┘                                   │ ✅ ~$20/month        │
                                                            │                      │
                                                            │ URL:                 │
                                                            │ codex-api.eastus...  │
                                                            │ azurecontainer.io    │
                                                            └─────────────────────┘


        ┌─────────────────────────────────────────────────────────────┐
        │                                                               │
        ▼                                                               ▼
┌─────────────────────┐                                   ┌─────────────────────┐
│ Database Workflow   │                                   │  Redis Workflow     │
│ (Manual Trigger)    │                                   │ (Manual Trigger)    │
└─────────────────────┘                                   └─────────────────────┘
        │                                                               │
        │ Trigger: workflow_dispatch                                   │ Trigger: workflow_dispatch
        │                                                               │
        ├──► 1. Check if server exists                                ├──► 1. Create Azure Redis Cache
        ├──► 2. Create PostgreSQL Server                              │      └─► Name: codex-redis
        │      └─► Name: codex-db-server                               │      └─► SKU: Basic C0
        │      └─► SKU: Standard_B1ms                                  │      └─► Location: eastus
        │      └─► Version: 16                                         │
        │      └─► Location: eastus                                    ├──► 2. Enable TLS/SSL
        │                                                               ├──► 3. Get connection string
        ├──► 3. Configure firewall rules                               ├──► 4. Update Container Instance
        │      └─► Allow Azure services                                │      └─► Add REDIS_URL env var
        │                                                               │
        ├──► 4. Initialize database schema                             ├──► 5. Verify Redis connection
        │      └─► Create tables:                                      │
        │          - capsules                                           ▼
        │          - signals                                 ┌─────────────────────┐
        │          - replays                                 │ Azure Cache         │
        │                                                    │ for Redis           │
        ├──► 5. Create indexes                              ├─────────────────────┤
        ├──► 6. Get connection string                       │ ✅ Session Store     │
        ├──► 7. Update Container Instance                   │ ✅ API Caching       │
        │      └─► Add DATABASE_URL env var                 │ ✅ Rate Limiting     │
        │                                                    │ ✅ ~$15/month        │
        ├──► 8. Verify database connection                  │                      │
        │                                                    │ Connection:          │
        ▼                                                    │ SSL/TLS Port 6380    │
┌─────────────────────┐                                   └─────────────────────┘
│ Azure PostgreSQL    │
│ Flexible Server     │
├─────────────────────┤
│ ✅ PostgreSQL 16     │
│ ✅ Burstable Tier    │
│ ✅ 32GB Storage      │
│ ✅ ~$12-15/month     │
│                      │
│ Host:                │
│ codex-db-server...   │
│ postgres.database... │
└─────────────────────┘
```

---

## 📊 Resource Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│                     Azure Resource Group                        │
│                        codex-rg (eastus)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │   ACR    │    │  Static  │    │Container │
        │  Basic   │    │ Web Apps │    │ Instance │
        │  $5/mo   │    │  Free    │    │  $20/mo  │
        └──────────┘    └──────────┘    └──────────┘
             │                                  │
             │                                  │
             └──────────┐              ┌────────┘
                        │              │
                        ▼              ▼
                ┌─────────────────────────┐
                │    Backend Container    │
                │   (pulls from ACR)      │
                └─────────────────────────┘
                        │              │
                ┌───────┴───────┐      │
                │               │      │
                ▼               ▼      ▼
        ┌──────────┐    ┌──────────┐  ┌──────────┐
        │PostgreSQL│    │  Redis   │  │  Logs    │
        │ Optional │    │ Optional │  │Container │
        │ $12/mo   │    │ $15/mo   │  │ Insights │
        └──────────┘    └──────────┘  └──────────┘
```

---

## 🔄 CI/CD Workflow Matrix

| Workflow | Trigger | Frequency | Duration | Cost Impact |
|----------|---------|-----------|----------|-------------|
| **Frontend** | `push main` | Every commit | ~2 min | $0 |
| **Backend** | `push main` (src/backend/**) | On backend changes | ~5 min | $0.01/build |
| **Database** | Manual `workflow_dispatch` | One-time | ~10 min | +$12-15/mo |
| **Redis** | Manual `workflow_dispatch` | One-time | ~5 min | +$15/mo |

---

## 🎯 Deployment Sequence (First Time)

```
Step 1: Initial Setup (Manual)
├─► Create Azure Resource Group
├─► Create ACR (Container Registry)
├─► Create Service Principal
└─► Add GitHub Secrets

Step 2: First Deploy (Automated)
├─► Push to main branch
├─► Frontend workflow runs → Static Web App deployed
├─► Backend workflow runs → Container Instance deployed
└─► Both services operational

Step 3: Database Setup (Manual Trigger)
├─► Run "Provision Azure PostgreSQL Database" workflow
├─► Wait ~10 minutes
└─► Backend automatically connects to database

Step 4: Redis Setup (Manual Trigger - Optional)
├─► Run "Provision Azure Redis Cache" workflow
├─► Wait ~5 minutes
└─► Backend automatically connects to Redis

Step 5: Verification
├─► Test frontend: https://happy-flower-...azurestaticapps.net
├─► Test backend: http://codex-api.eastus.azurecontainer.io:8001/health
├─► Test database: Backend /health shows DB connection
└─► Test Redis: Backend /health shows Redis connection
```

---

## 📝 Workflow Files

### Automated Workflows
1. **`.github/workflows/azure-static-web-apps.yml`**
   - **Triggers**: `push`, `pull_request` on `main`
   - **Actions**: Build Next.js → Deploy to Static Web Apps
   - **Secrets Required**: `AZURE_STATIC_WEB_APPS_API_TOKEN`

2. **`.github/workflows/azure-backend-deploy.yml`**
   - **Triggers**: `push` on `main` (paths: `src/backend/**`)
   - **Actions**: Docker build → ACR push → Container Instance deploy
   - **Secrets Required**: `AZURE_CREDENTIALS`

### Manual Workflows
3. **`.github/workflows/azure-database-provision.yml`**
   - **Trigger**: `workflow_dispatch` (manual)
   - **Actions**: Create PostgreSQL → Initialize schema → Update backend
   - **Secrets Required**: `AZURE_CREDENTIALS`, `DB_ADMIN_PASSWORD`

4. **`.github/workflows/azure-redis-provision.yml`** *(To be created)*
   - **Trigger**: `workflow_dispatch` (manual)
   - **Actions**: Create Redis → Configure → Update backend
   - **Secrets Required**: `AZURE_CREDENTIALS`

---

## 🔐 Required GitHub Secrets

| Secret Name | Purpose | Workflow |
|-------------|---------|----------|
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Frontend deployment | Static Web Apps |
| `AZURE_CREDENTIALS` | Azure authentication | Backend, Database, Redis |
| `DB_ADMIN_PASSWORD` | PostgreSQL admin password | Database |

---

## 💰 Cost Breakdown

| Service | Tier | Monthly Cost | Annual Cost |
|---------|------|--------------|-------------|
| Static Web Apps | Free | $0 | $0 |
| Container Registry | Basic | $5 | $60 |
| Container Instances | 1 vCPU, 1GB | $20 | $240 |
| PostgreSQL (optional) | Standard_B1ms | $12-15 | $144-180 |
| Redis (optional) | Basic C0 | $15 | $180 |
| **Total (Base)** | | **$25/mo** | **$300/yr** |
| **Total (Full)** | | **$52-55/mo** | **$624-660/yr** |

---

## 🚀 Environment Variables Flow

```
GitHub Secrets
      │
      ├──► Frontend Build
      │     └──► NEXT_PUBLIC_API_URL
      │
      └──► Backend Deployment
            ├──► PORT=8001
            ├──► ENVIRONMENT=production
            ├──► ALLOWED_ORIGINS=https://...
            ├──► CORS_ENABLED=true
            ├──► DATABASE_URL=postgresql://... (if database provisioned)
            └──► REDIS_URL=redis://... (if Redis provisioned)
```

---

## 📈 Scaling Strategy

### Current Architecture (MVP)
- Frontend: Auto-scales via CDN
- Backend: 1 container (1 vCPU, 1GB)
- Database: None (in-memory)
- Cache: None

### With Database (Production-Ready)
- Frontend: Auto-scales via CDN
- Backend: 1 container
- Database: PostgreSQL Flexible Server
- Cache: None

### Full Stack (High Performance)
- Frontend: Auto-scales via CDN + Custom Domain
- Backend: App Service (2+ instances with auto-scale)
- Database: PostgreSQL (General Purpose tier)
- Cache: Redis (Standard tier with replication)

---

## ✅ Health Check Matrix

| Endpoint | Purpose | Expected Response | Check Frequency |
|----------|---------|-------------------|-----------------|
| Frontend `/` | Static files | 200 OK | GitHub Actions |
| Backend `/` | API info | JSON with version | GitHub Actions |
| Backend `/health` | Health status | `{"status":"healthy"}` | Container health check |
| Backend `/ready` | Readiness probe | 200 OK when ready | Kubernetes-style |
| Database Connection | DB connectivity | Included in `/health` | On startup |
| Redis Connection | Cache connectivity | Included in `/health` | On startup |

---

## 🔧 Manual Operations

### Update Backend Environment Variables
```powershell
# Edit update-container-env.ps1
# Add/modify environment variables
# Run:
.\update-container-env.ps1
```

### Redeploy Backend Manually
```powershell
# Build and push
docker build -t codexdominionacr.azurecr.io/codex-backend:latest src/backend/
docker push codexdominionacr.azurecr.io/codex-backend:latest

# Update container
.\update-container-env.ps1
```

### Database Backup
```powershell
# Backup PostgreSQL
az postgres flexible-server backup create \
  --name codex-db-server \
  --resource-group codex-rg \
  --backup-name daily-backup-$(Get-Date -Format 'yyyyMMdd')
```

### Redis Cache Clear
```powershell
# Clear all Redis keys
az redis force-reboot \
  --name codex-redis \
  --resource-group codex-rg \
  --reboot-type AllNodes
```

---

## 🎯 Success Metrics

### Deployment Success Criteria
- ✅ Frontend HTTPS accessible (port 443)
- ✅ Backend API responding (port 8001)
- ✅ Health checks passing
- ✅ Database connected (if provisioned)
- ✅ Redis connected (if provisioned)
- ✅ CI/CD pipelines green
- ✅ Zero downtime deployments

### Performance Targets
- Frontend: < 2s page load
- Backend API: < 200ms response time
- Database queries: < 100ms average
- Redis cache: < 10ms hit time
- Deployment time: < 5 minutes

---

**Last Updated**: December 8, 2025
**Architecture Version**: 2.0
**Status**: ✅ Operational
