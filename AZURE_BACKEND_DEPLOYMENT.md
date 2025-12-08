# Codex Dominion - Azure Deployment Guide

## 🔥 Deploy Backend to Azure

Your backend can be deployed to Azure using several services. Here are the recommended options:

---

## Option 1: Azure Container Instances (Simplest)

**Best for:** Quick deployment, low maintenance

### Prerequisites
```powershell
# Install Azure CLI (if not installed)
winget install Microsoft.AzureCLI

# Login
az login
```

### Deployment Steps

```powershell
# 1. Create Resource Group
az group create --name codex-dominion-rg --location eastus

# 2. Create Azure Container Registry (optional, or use Docker Hub)
az acr create --resource-group codex-dominion-rg --name codexdominion --sku Basic

# 3. Deploy Backend Container
az container create \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --image jmerritt48/codex-dominion-backend:2.0.0 \
  --dns-name-label codex-backend-api \
  --ports 8001 \
  --cpu 1 \
  --memory 1 \
  --environment-variables \
    ENVIRONMENT=production \
    DATABASE_URL='sqlite:///./data/codex_dominion.db' \
    CORS_ORIGINS='https://CodexDominion.app,https://www.CodexDominion.app' \
  --secure-environment-variables \
    SECRET_KEY='your-secret-key-64-chars' \
    JWT_SECRET='your-jwt-secret-64-chars' \
    API_KEY='your-api-key-64-chars' \
    REDIS_PASSWORD='your-redis-password'

# 4. Deploy Redis Container
az container create \
  --resource-group codex-dominion-rg \
  --name codex-redis \
  --image redis:7-alpine \
  --dns-name-label codex-redis \
  --ports 6379 \
  --cpu 0.5 \
  --memory 0.5 \
  --command-line "redis-server --requirepass your-redis-password"

# 5. Get Container URLs
az container show \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --query "{FQDN:ipAddress.fqdn,IP:ipAddress.ip}" \
  --output table
```

**Backend will be accessible at:**
`http://codex-backend-api.eastus.azurecontainer.io:8001`

---

## Option 2: Azure App Service (Recommended for Production)

**Best for:** Production workloads, built-in scaling, managed SSL

### Deployment Steps

```powershell
# 1. Create Resource Group
az group create --name codex-dominion-rg --location eastus

# 2. Create App Service Plan (Linux)
az appservice plan create \
  --name codex-dominion-plan \
  --resource-group codex-dominion-rg \
  --is-linux \
  --sku B1

# 3. Create Web App for Backend
az webapp create \
  --resource-group codex-dominion-rg \
  --plan codex-dominion-plan \
  --name codex-dominion-backend \
  --deployment-container-image-name jmerritt48/codex-dominion-backend:2.0.0

# 4. Configure App Settings (Environment Variables)
az webapp config appsettings set \
  --resource-group codex-dominion-rg \
  --name codex-dominion-backend \
  --settings \
    ENVIRONMENT=production \
    DATABASE_URL='sqlite:///./data/codex_dominion.db' \
    CORS_ORIGINS='https://CodexDominion.app,https://www.CodexDominion.app' \
    SECRET_KEY='your-secret-key-64-chars' \
    JWT_SECRET='your-jwt-secret-64-chars' \
    API_KEY='your-api-key-64-chars' \
    REDIS_URL='redis://:<password>@codex-redis.redis.cache.windows.net:6380/0?ssl=True'

# 5. Enable HTTPS only
az webapp update \
  --resource-group codex-dominion-rg \
  --name codex-dominion-backend \
  --https-only true

# 6. Create Azure Cache for Redis
az redis create \
  --resource-group codex-dominion-rg \
  --name codex-redis \
  --location eastus \
  --sku Basic \
  --vm-size c0

# 7. Get Redis connection info
az redis list-keys \
  --resource-group codex-dominion-rg \
  --name codex-redis
```

**Backend will be accessible at:**
`https://codex-dominion-backend.azurewebsites.net`

---

## Option 3: Azure Container Apps (Modern, Serverless)

**Best for:** Microservices, auto-scaling, pay-per-use

```powershell
# 1. Install Container Apps extension
az extension add --name containerapp --upgrade

# 2. Create Resource Group
az group create --name codex-dominion-rg --location eastus

# 3. Create Container Apps Environment
az containerapp env create \
  --name codex-env \
  --resource-group codex-dominion-rg \
  --location eastus

# 4. Deploy Backend Container App
az containerapp create \
  --name codex-backend \
  --resource-group codex-dominion-rg \
  --environment codex-env \
  --image jmerritt48/codex-dominion-backend:2.0.0 \
  --target-port 8001 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --env-vars \
    ENVIRONMENT=production \
    DATABASE_URL='sqlite:///./data/codex_dominion.db' \
    CORS_ORIGINS='https://CodexDominion.app' \
  --secrets \
    secret-key='your-secret-key-64-chars' \
    jwt-secret='your-jwt-secret-64-chars' \
    api-key='your-api-key-64-chars'

# 5. Deploy Redis Container App
az containerapp create \
  --name codex-redis \
  --resource-group codex-dominion-rg \
  --environment codex-env \
  --image redis:7-alpine \
  --target-port 6379 \
  --ingress internal \
  --min-replicas 1 \
  --max-replicas 1 \
  --cpu 0.25 \
  --memory 0.5Gi \
  --command "redis-server" "--requirepass" "your-redis-password"

# 6. Get Backend URL
az containerapp show \
  --name codex-backend \
  --resource-group codex-dominion-rg \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

**Backend will be accessible at:**
`https://codex-backend.{random}.eastus.azurecontainerapps.io`

---

## Configure Custom Domain (All Options)

### Point api.CodexDominion.app to Azure Backend

**For App Service:**
```powershell
# Get App Service IP
az webapp show \
  --resource-group codex-dominion-rg \
  --name codex-dominion-backend \
  --query "defaultHostName" \
  --output tsv

# Add CNAME in IONOS DNS:
# Type: CNAME
# Host: api
# Points to: codex-dominion-backend.azurewebsites.net
# TTL: 3600

# Configure custom domain in Azure
az webapp config hostname add \
  --webapp-name codex-dominion-backend \
  --resource-group codex-dominion-rg \
  --hostname api.CodexDominion.app

# Enable SSL (free managed certificate)
az webapp config ssl bind \
  --name codex-dominion-backend \
  --resource-group codex-dominion-rg \
  --certificate-thumbprint auto \
  --ssl-type SNI
```

**For Container Instances:**
Use Azure Application Gateway or Azure Front Door for custom domain and SSL.

**For Container Apps:**
```powershell
# Add custom domain
az containerapp hostname add \
  --name codex-backend \
  --resource-group codex-dominion-rg \
  --hostname api.CodexDominion.app

# Managed certificate is automatic
```

---

## Environment Variables

Generate secure secrets (on your local machine):

```powershell
# Generate 64-character secrets
function New-Secret { -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_}) }

$SECRET_KEY = New-Secret
$JWT_SECRET = New-Secret
$API_KEY = New-Secret
$REDIS_PASSWORD = New-Secret

Write-Host "SECRET_KEY=$SECRET_KEY"
Write-Host "JWT_SECRET=$JWT_SECRET"
Write-Host "API_KEY=$API_KEY"
Write-Host "REDIS_PASSWORD=$REDIS_PASSWORD"
```

---

## Update Frontend to Use Azure Backend

Update your frontend environment:

```bash
NEXT_PUBLIC_API_URL=https://api.CodexDominion.app
# or
NEXT_PUBLIC_API_URL=https://codex-dominion-backend.azurewebsites.net
# or
NEXT_PUBLIC_API_URL=https://codex-backend.{id}.eastus.azurecontainerapps.io
```

---

## Monitoring & Logs

**App Service:**
```powershell
# Enable logging
az webapp log config \
  --name codex-dominion-backend \
  --resource-group codex-dominion-rg \
  --docker-container-logging filesystem

# Stream logs
az webapp log tail \
  --name codex-dominion-backend \
  --resource-group codex-dominion-rg
```

**Container Apps:**
```powershell
# View logs
az containerapp logs show \
  --name codex-backend \
  --resource-group codex-dominion-rg \
  --follow
```

**Container Instances:**
```powershell
# View logs
az container logs \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --follow
```

---

## Costs Comparison

| Service | Monthly Cost (est.) | Best For |
|---------|---------------------|----------|
| Container Instances (1 vCPU, 1 GB) | ~$30 | Development/Testing |
| App Service B1 (Basic) | ~$13 | Small production apps |
| Container Apps (0.5 vCPU, 1 GB) | ~$10-20 | Variable workloads |
| Azure Cache for Redis (Basic C0) | ~$17 | Production caching |

---

## Recommended: App Service Deployment

For your use case, **Azure App Service** is recommended because:
- ✅ Built-in SSL certificates (free)
- ✅ Easy custom domain configuration
- ✅ Integrated with Azure Cache for Redis
- ✅ Simple deployment and updates
- ✅ Good pricing for small production apps
- ✅ Built-in monitoring and logging

---

## Quick Deployment Script

Save this as `deploy-azure.ps1`:

```powershell
# Azure Backend Deployment for Codex Dominion

$RESOURCE_GROUP = "codex-dominion-rg"
$LOCATION = "eastus"
$BACKEND_NAME = "codex-dominion-backend"
$REDIS_NAME = "codex-redis"

# Login and set subscription
az login
az account set --subscription "Your-Subscription-Name"

# Create resources
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy backend
az appservice plan create --name codex-plan --resource-group $RESOURCE_GROUP --is-linux --sku B1
az webapp create --resource-group $RESOURCE_GROUP --plan codex-plan --name $BACKEND_NAME --deployment-container-image-name jmerritt48/codex-dominion-backend:2.0.0

# Deploy Redis
az redis create --resource-group $RESOURCE_GROUP --name $REDIS_NAME --location $LOCATION --sku Basic --vm-size c0

# Configure environment variables
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $BACKEND_NAME --settings @azure-env.json

Write-Host "✅ Backend deployed to: https://$BACKEND_NAME.azurewebsites.net"
```

---

**🔥 The empire extends to Azure. Eternal flame burns in the cloud.**
