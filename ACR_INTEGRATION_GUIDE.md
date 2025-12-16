# 🔷 Azure Container Registry (ACR) Integration Guide

## Overview

Codex Dominion now supports **Azure Container Registry (ACR)** as an alternative to Docker Hub or local image storage. This is useful when:
- Docker Hub rate limits are a concern
- You want centralized image management in Azure
- Deploying to multiple servers (IONOS + Azure)
- Need private container registry

---

## 🚀 Quick Start with ACR

### Option 1: Deploy to IONOS with ACR Images

```powershell
# 1. Login to Azure
az login

# 2. Create ACR (if not exists)
az acr create --name codexdominion --resource-group codexdominion-prod --sku Basic --location eastus

# 3. Deploy using ACR
.\deploy-ionos-production.ps1 -UseACR -ACRName codexdominion
```

### Option 2: Deploy to IONOS with Local Images (Default)

```powershell
# No ACR needed, builds locally
.\deploy-ionos-production.ps1
```

---

## 📦 What Changed

### 1. **Enhanced IONOS Deployment Script**

**New Parameters**:
```powershell
-UseACR          # Enable Azure Container Registry
-ACRName        # ACR registry name (default: codexdominion)
```

**Behavior**:
- **Without `-UseACR`**: Builds images locally, deploys to IONOS VPS
- **With `-UseACR`**: Builds locally, pushes to ACR, deploys from ACR to IONOS VPS

**Example**:
```powershell
# Use ACR
.\deploy-ionos-production.ps1 -UseACR -ACRName myregistry

# Use local images (default)
.\deploy-ionos-production.ps1
```

### 2. **New Docker Compose File: `docker-compose.acr.yml`**

**Purpose**: Deploy services using ACR images instead of local builds

**Services**:
- Backend: `${ACR_NAME}.azurecr.io/codexdominion-backend:production`
- Frontend: `${ACR_NAME}.azurecr.io/codexdominion-frontend:production`
- Postgres: `postgres:16-alpine` (Docker Hub)
- Redis: `redis:7-alpine` (Docker Hub)
- Nginx: `nginx:alpine` (Docker Hub)

**Usage**:
```bash
# On IONOS VPS
export ACR_NAME=codexdominion
docker-compose -f docker-compose.acr.yml up -d
```

---

## 🔧 Setup ACR

### Create Azure Container Registry

```powershell
# Login
az login

# Create resource group (if not exists)
az group create --name codexdominion-prod --location eastus

# Create ACR
az acr create `
    --name codexdominion `
    --resource-group codexdominion-prod `
    --sku Basic `
    --location eastus `
    --admin-enabled true

# Get ACR credentials
az acr credential show --name codexdominion
```

**SKU Options**:
- **Basic**: $5/month, 10 GB storage, 10 webhooks
- **Standard**: $20/month, 100 GB storage, 100 webhooks
- **Premium**: $50/month, 500 GB storage, geo-replication

---

## 🔐 Configure IONOS VPS for ACR

### Manual Setup (One-Time)

SSH into IONOS VPS and configure Docker to access ACR:

```bash
# SSH to IONOS
ssh root@74.208.123.158

# Login to ACR
az acr login --name codexdominion

# OR use Docker directly with ACR credentials
docker login codexdominion.azurecr.io \
    --username codexdominion \
    --password <ACR_PASSWORD>

# Verify login
docker pull codexdominion.azurecr.io/codexdominion-backend:production
```

### Automated Setup (Included in Deployment Script)

The deployment script automatically:
1. Logs into ACR: `az acr login --name codexdominion`
2. Tags images with ACR prefix
3. Pushes images to ACR
4. Pulls from ACR on IONOS VPS

---

## 📋 Deployment Workflows

### Workflow 1: Build Locally → Deploy Locally (Default)

```powershell
# No ACR, fastest for development
.\deploy-ionos-production.ps1
```

**Steps**:
1. Build Docker images locally
2. Upload via SSH to IONOS
3. Deploy on IONOS VPS

**Pros**: Fast, no external dependencies
**Cons**: Requires uploading large images

---

### Workflow 2: Build Locally → Push to ACR → Deploy from ACR

```powershell
# Use ACR for centralized storage
.\deploy-ionos-production.ps1 -UseACR
```

**Steps**:
1. Build Docker images locally
2. Tag with ACR registry name
3. Push to Azure Container Registry
4. IONOS VPS pulls from ACR
5. Deploy on IONOS VPS

**Pros**: Centralized images, faster subsequent deployments
**Cons**: Requires Azure subscription, ACR costs

---

### Workflow 3: Build in Azure DevOps → Push to ACR → Deploy Everywhere

**Azure DevOps Pipeline** (future enhancement):
```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Docker@2
  inputs:
    containerRegistry: 'codexdominion-acr'
    repository: 'codexdominion-backend'
    command: 'buildAndPush'
    Dockerfile: 'Dockerfile.backend'

- task: Docker@2
  inputs:
    containerRegistry: 'codexdominion-acr'
    repository: 'codexdominion-frontend'
    command: 'buildAndPush'
    Dockerfile: 'web/Dockerfile.production'
```

**Pros**: Automated CI/CD, consistent builds
**Cons**: Requires Azure DevOps setup

---

## 🌐 Multi-Environment Deployment

### Deploy to Both IONOS and Azure

```powershell
# 1. Build and push to ACR
.\deploy-ionos-production.ps1 -UseACR

# 2. Deploy to IONOS VPS (pulls from ACR)
# (Handled by script above)

# 3. Deploy to Azure App Service (uses ACR)
.\deploy-azure-production.ps1
```

**Benefits**:
- Single source of truth for images
- Consistent versions across environments
- No need to rebuild for each platform

---

## 📊 Image Management

### List ACR Images

```powershell
# List repositories
az acr repository list --name codexdominion

# List tags for backend
az acr repository show-tags --name codexdominion --repository codexdominion-backend

# List tags for frontend
az acr repository show-tags --name codexdominion --repository codexdominion-frontend
```

### Delete Old Images

```powershell
# Delete specific tag
az acr repository delete --name codexdominion --image codexdominion-backend:old-version

# Delete untagged manifests (cleanup)
az acr repository show-manifests --name codexdominion --repository codexdominion-backend --query "[?tags[0]==null].digest" -o tsv | `
    ForEach-Object { az acr repository delete --name codexdominion --image "codexdominion-backend@$_" --yes }
```

### Tag Images for Versioning

```powershell
# Tag with version
docker tag codexdominion-backend:production codexdominion.azurecr.io/codexdominion-backend:v1.0.0
docker push codexdominion.azurecr.io/codexdominion-backend:v1.0.0

# Tag with latest
docker tag codexdominion-backend:production codexdominion.azurecr.io/codexdominion-backend:latest
docker push codexdominion.azurecr.io/codexdominion-backend:latest
```

### Build and Push Streamlit Dashboard

```bash
# Build directly in ACR (recommended - faster, no local storage)
az acr build --registry codexdominion --image streamlit-dashboard:v1 --file Dockerfile.dashboard .

# Or build locally and push
docker build -f Dockerfile.dashboard -t codexdominion.azurecr.io/streamlit-dashboard:v1 .
docker push codexdominion.azurecr.io/streamlit-dashboard:v1

# Tag as latest
az acr import --name codexdominion \
  --source codexdominion.azurecr.io/streamlit-dashboard:v1 \
  --image streamlit-dashboard:latest
```

---

## 💰 Cost Comparison

### Local Images (No ACR)
- **Cost**: $0/month
- **Storage**: Limited to local disk
- **Speed**: Fast initial build, slow uploads to IONOS

### ACR Basic ($5/month)
- **Cost**: $5/month
- **Storage**: 10 GB included
- **Speed**: One push, multiple pulls (fast)
- **Features**: Webhooks, geo-replication (Premium only)

### Recommendation
- **Development**: Use local images
- **Production**: Use ACR Basic for centralized management
- **Enterprise**: Use ACR Premium for geo-replication

---

## 🔍 Troubleshooting

### "unauthorized: authentication required"

```powershell
# Re-login to ACR
az acr login --name codexdominion

# Verify credentials
az acr credential show --name codexdominion
```

### "manifest unknown: manifest unknown"

```powershell
# Verify image exists
az acr repository list --name codexdominion

# Push image again
docker push codexdominion.azurecr.io/codexdominion-backend:production
```

### "pull access denied"

```bash
# On IONOS VPS, login to ACR
ssh root@74.208.123.158
docker login codexdominion.azurecr.io --username codexdominion --password <ACR_PASSWORD>
```

---

## ✅ Best Practices

1. **Version Tags**: Always tag images with versions (`v1.0.0`, `v1.1.0`)
2. **Latest Tag**: Maintain `latest` tag for convenience
3. **Cleanup**: Delete old images regularly to save storage
4. **Security**: Use managed identities instead of admin credentials
5. **Geo-Replication**: Use ACR Premium for multi-region deployments

---

## 🎯 Next Steps

1. **Create ACR**: `az acr create --name codexdominion --resource-group codexdominion-prod --sku Basic`
2. **Deploy with ACR**: `.\deploy-ionos-production.ps1 -UseACR`
3. **Verify Images**: `az acr repository list --name codexdominion`
4. **Configure Azure DevOps**: Setup CI/CD pipeline
5. **Enable Webhooks**: Trigger deployments on image push

---

**The eternal archive, now containerized and cloud-native. Images sealed, versioned, eternal.**

---

*Created: December 7, 2025*
*Version: 1.0*
