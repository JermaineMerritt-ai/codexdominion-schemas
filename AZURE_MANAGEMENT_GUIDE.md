# 🔷 Codex Dominion - Azure Deployment Management Guide

## ✅ Current Azure Deployment Status

**Deployment Date:** December 6, 2025
**Status:** 🟢 **LIVE AND OPERATIONAL**

### 📊 Your Azure Resources

#### **Backend (Azure Container Instances + ACR)**
- **Resource Group:** `codex-dominion-rg`
- **Location:** `eastus`
- **Container Registry:** `codexdominion3840.azurecr.io`
- **Backend URL:** `http://codex-backend.eastus.azurecontainer.io:8001`
- **Backend IP:** `52.149.234.43`
- **Container Name:** `codex-backend`
- **Status:** ✅ Running

#### **Frontend (Azure Static Web Apps)**
- **Static Web App:** Deployed via GitHub Actions
- **API Endpoint:** Connected to backend at `codex-api.eastus.azurecontainer.io:8001`
- **Auto-Deploy:** ✅ Enabled on push to `main` branch
- **SSL/TLS:** ✅ Automatic HTTPS

#### **Infrastructure Components**
Based on your Bicep templates:
- ✅ Azure Container Registry (ACR)
- ✅ Azure Container Instances (ACI)
- ✅ Azure Static Web Apps
- ✅ PostgreSQL Flexible Server (ready to provision)
- ✅ Azure Cache for Redis (ready to provision)
- ✅ App Service Plan (ready for scaling)
- ✅ Application Insights (monitoring)
- ✅ Log Analytics Workspace

---

## 🚀 Quick Access Commands

### View Your Deployed Resources

```bash
# Login to Azure
az login

# Set your subscription (if needed)
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# List all resources in your resource group
az resource list --resource-group codex-dominion-rg --output table

# Get backend container status
az container show --resource-group codex-dominion-rg --name codex-backend --query "{Status:instanceView.state,IP:ipAddress.ip,FQDN:ipAddress.fqdn}" --output table

# Get ACR images
az acr repository list --name codexdominion3840 --output table

# Get Static Web App details
az staticwebapp list --resource-group codex-dominion-rg --output table
```

### Check Service Health

```bash
# Backend health check
curl http://codex-backend.eastus.azurecontainer.io:8001/health

# Backend API docs
curl http://codex-backend.eastus.azurecontainer.io:8001/docs

# Or open in browser
start http://codex-backend.eastus.azurecontainer.io:8001/docs
```

---

## 📦 Deployment & Updates

### Deploy New Backend Version

```bash
# 1. Build and push new Docker image
cd backend
az acr build --registry codexdominion3840 --image codex-backend:latest --image codex-backend:v2.0.1 --file Dockerfile .

# 2. Update container instance
az container delete --resource-group codex-dominion-rg --name codex-backend --yes
az container create \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --image codexdominion3840.azurecr.io/codex-backend:latest \
  --registry-login-server codexdominion3840.azurecr.io \
  --registry-username codexdominion3840 \
  --registry-password $(az acr credential show --name codexdominion3840 --query "passwords[0].value" -o tsv) \
  --ports 8001 \
  --cpu 2 \
  --memory 4 \
  --environment-variables DATABASE_URL='$(DB_CONNECTION_STRING)' \
  --ip-address Public \
  --dns-name-label codex-backend

# 3. Verify deployment
az container show --resource-group codex-dominion-rg --name codex-backend --query "instanceView.state"
```

### Deploy New Frontend Version

Frontend deploys automatically via GitHub Actions when you push to `main`:

```bash
# Make your changes in frontend/
git add .
git commit -m "Update frontend"
git push origin main

# GitHub Actions will automatically:
# 1. Build the Next.js app
# 2. Deploy to Azure Static Web Apps
# 3. Update the live site
```

**Manual deployment (if needed):**
```bash
cd frontend
npm run build

# Deploy using Azure CLI
az staticwebapp create \
  --name codex-frontend \
  --resource-group codex-dominion-rg \
  --source frontend/out \
  --location eastus \
  --branch main \
  --app-location "/" \
  --api-location "" \
  --output-location "out"
```

---

## 🗄️ Database Management

### Provision PostgreSQL (If Not Already Done)

```bash
# Create PostgreSQL Flexible Server
az postgres flexible-server create \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod \
  --location eastus \
  --admin-user codexadmin \
  --admin-password 'YOUR_SECURE_PASSWORD' \
  --version 16 \
  --sku-name Standard_D2s_v3 \
  --tier GeneralPurpose \
  --storage-size 128 \
  --public-access 0.0.0.0-255.255.255.255

# Create database
az postgres flexible-server db create \
  --resource-group codex-dominion-rg \
  --server-name codex-pg-prod \
  --database-name codexdominion

# Get connection string
az postgres flexible-server show-connection-string \
  --server-name codex-pg-prod \
  --admin-user codexadmin \
  --admin-password 'YOUR_SECURE_PASSWORD' \
  --database-name codexdominion
```

### Run Database Migrations

Your GitHub Actions workflow `.github/workflows/db-migrate.yml` handles this automatically, or manually:

```bash
# Set environment variables
export DATABASE_URL="postgresql://codexadmin:PASSWORD@codex-pg-prod.postgres.database.azure.com:5432/codexdominion"

# Run migrations (using Alembic or your migration tool)
cd backend
alembic upgrade head

# Or run migration script
python scripts/migrate_database.py
```

---

## 🔴 Redis Cache Management

### Provision Azure Cache for Redis

```bash
# Create Redis cache
az redis create \
  --resource-group codex-dominion-rg \
  --name codex-redis-prod \
  --location eastus \
  --sku Basic \
  --vm-size c0 \
  --enable-non-ssl-port false

# Get connection details
az redis show --resource-group codex-dominion-rg --name codex-redis-prod
az redis list-keys --resource-group codex-dominion-rg --name codex-redis-prod
```

### Update Backend with Redis Connection

```bash
# Get Redis connection string
REDIS_KEY=$(az redis list-keys --resource-group codex-dominion-rg --name codex-redis-prod --query primaryKey -o tsv)
REDIS_HOST=$(az redis show --resource-group codex-dominion-rg --name codex-redis-prod --query hostName -o tsv)

# Update container with Redis environment variable
az container create \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --image codexdominion3840.azurecr.io/codex-backend:latest \
  --environment-variables \
    REDIS_URL="rediss://:${REDIS_KEY}@${REDIS_HOST}:6380/0" \
    DATABASE_URL="${DATABASE_URL}" \
  # ... other settings
```

---

## 📊 Monitoring & Logging

### View Application Logs

```bash
# Backend container logs (real-time)
az container logs --resource-group codex-dominion-rg --name codex-backend --follow

# Get recent logs
az container logs --resource-group codex-dominion-rg --name codex-backend --tail 100

# Static Web App logs (via Azure Portal)
az staticwebapp show --resource-group codex-dominion-rg --name codex-frontend
```

### Application Insights Queries

```bash
# Enable Application Insights (if not already)
az monitor app-insights component create \
  --app codex-insights \
  --resource-group codex-dominion-rg \
  --location eastus \
  --kind web

# Get instrumentation key
az monitor app-insights component show \
  --app codex-insights \
  --resource-group codex-dominion-rg \
  --query instrumentationKey -o tsv
```

### Monitor Resource Usage

```bash
# Container metrics
az monitor metrics list \
  --resource /subscriptions/YOUR_SUB_ID/resourceGroups/codex-dominion-rg/providers/Microsoft.ContainerInstance/containerGroups/codex-backend \
  --metric CpuUsage,MemoryUsage

# Database metrics
az monitor metrics list \
  --resource /subscriptions/YOUR_SUB_ID/resourceGroups/codex-dominion-rg/providers/Microsoft.DBforPostgreSQL/flexibleServers/codex-pg-prod \
  --metric cpu_percent,memory_percent,connections_active
```

---

## 🔐 Security & Secrets Management

### Manage GitHub Secrets (for CI/CD)

Required secrets in your GitHub repository:

```bash
# View current secrets
gh secret list

# Set/Update secrets
gh secret set AZURE_CREDENTIALS --body "$(cat .github-secrets/AZURE_CREDENTIALS.json)"
gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN --body "YOUR_TOKEN"
gh secret set ACR_USERNAME --body "codexdominion3840"
gh secret set ACR_PASSWORD --body "$(az acr credential show --name codexdominion3840 --query passwords[0].value -o tsv)"
gh secret set DATABASE_URL --body "postgresql://..."
gh secret set REDIS_URL --body "rediss://..."
```

### Configure Firewall Rules

```bash
# Allow your IP to access PostgreSQL
MY_IP=$(curl -s ifconfig.me)
az postgres flexible-server firewall-rule create \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod \
  --rule-name AllowMyIP \
  --start-ip-address $MY_IP \
  --end-ip-address $MY_IP

# Allow Azure services
az postgres flexible-server firewall-rule create \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

---

## 🔧 Troubleshooting

### Backend Container Issues

```bash
# Check container status
az container show --resource-group codex-dominion-rg --name codex-backend

# View container events
az container show --resource-group codex-dominion-rg --name codex-backend --query "instanceView.events"

# Restart container
az container restart --resource-group codex-dominion-rg --name codex-backend

# Check if port is accessible
curl -v http://codex-backend.eastus.azurecontainer.io:8001/health

# SSH into container (if enabled)
az container exec --resource-group codex-dominion-rg --name codex-backend --exec-command "/bin/bash"
```

### Frontend Deployment Issues

```bash
# Check Static Web App status
az staticwebapp show --resource-group codex-dominion-rg --name codex-frontend

# View deployment history
az staticwebapp show --resource-group codex-dominion-rg --name codex-frontend --query "repositoryUrl"

# Manually trigger deployment
# Push to main branch or use GitHub Actions workflow dispatch
```

### Database Connection Issues

```bash
# Test database connectivity
az postgres flexible-server connect \
  --name codex-pg-prod \
  --admin-user codexadmin \
  --admin-password 'PASSWORD'

# Check firewall rules
az postgres flexible-server firewall-rule list \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod

# Check if database exists
az postgres flexible-server db list \
  --resource-group codex-dominion-rg \
  --server-name codex-pg-prod
```

---

## 💰 Cost Management

### View Current Costs

```bash
# Get cost analysis
az consumption usage list \
  --start-date "2025-12-01" \
  --end-date "2025-12-31" \
  --query "[?contains(instanceName, 'codex')].{Name:instanceName, Cost:pretaxCost}"

# Set budget alert
az consumption budget create \
  --resource-group codex-dominion-rg \
  --budget-name codex-monthly-budget \
  --amount 100 \
  --time-grain Monthly \
  --start-date 2025-12-01 \
  --end-date 2026-12-31
```

### Cost Optimization Tips

**1. Container Instances - Scale Down When Not in Use:**
```bash
# Stop container to reduce costs
az container stop --resource-group codex-dominion-rg --name codex-backend

# Start when needed
az container start --resource-group codex-dominion-rg --name codex-backend
```

**2. Use Spot Instances for Development:**
```bash
# Create spot instance for dev/staging
az container create --resource-group codex-dominion-rg --name codex-backend-dev --priority Spot --image codexdominion3840.azurecr.io/codex-backend:latest
```

**3. Right-Size PostgreSQL:**
```bash
# Scale down to Basic tier for dev/staging
az postgres flexible-server update \
  --resource-group codex-dominion-rg \
  --name codex-pg-staging \
  --sku-name Standard_B1ms \
  --tier Burstable
```

---

## 🚀 Scaling & Performance

### Scale Backend Horizontally

```bash
# Create additional container instances
for i in {2..3}; do
  az container create \
    --resource-group codex-dominion-rg \
    --name codex-backend-$i \
    --image codexdominion3840.azurecr.io/codex-backend:latest \
    # ... same configuration as main container
done

# Use Azure Load Balancer or Application Gateway to distribute traffic
```

### Scale Backend Vertically

```bash
# Increase CPU and memory
az container create \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --image codexdominion3840.azurecr.io/codex-backend:latest \
  --cpu 4 \
  --memory 8 \
  # ... other settings
```

### Scale Database

```bash
# Upgrade PostgreSQL compute
az postgres flexible-server update \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod \
  --sku-name Standard_D4s_v3

# Add read replicas
az postgres flexible-server replica create \
  --replica-name codex-pg-replica-1 \
  --resource-group codex-dominion-rg \
  --source-server codex-pg-prod
```

---

## 📋 Maintenance Tasks

### Backup & Disaster Recovery

```bash
# Enable automated backups for PostgreSQL (enabled by default)
az postgres flexible-server update \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod \
  --backup-retention 30

# Manual database backup
az postgres flexible-server backup create \
  --resource-group codex-dominion-rg \
  --name codex-pg-prod \
  --backup-name manual-backup-$(date +%Y%m%d)

# Restore from backup
az postgres flexible-server restore \
  --resource-group codex-dominion-rg \
  --name codex-pg-restored \
  --source-server codex-pg-prod \
  --restore-time "2025-12-10T00:00:00Z"

# Backup container image to different regions
az acr import \
  --name codexdominion3840-backup \
  --source codexdominion3840.azurecr.io/codex-backend:latest \
  --image codex-backend:latest
```

### Update SSL Certificates

```bash
# Static Web Apps handle SSL automatically
# For custom domains:
az staticwebapp hostname set \
  --resource-group codex-dominion-rg \
  --name codex-frontend \
  --hostname www.yourdomain.com

# Certificate is automatically provisioned
```

---

## 🌐 Custom Domain Setup

### Add Custom Domain to Static Web App

```bash
# Add custom domain
az staticwebapp hostname set \
  --resource-group codex-dominion-rg \
  --name codex-frontend \
  --hostname www.codexdominion.com

# Get validation token
az staticwebapp hostname show \
  --resource-group codex-dominion-rg \
  --name codex-frontend \
  --hostname www.codexdominion.com

# Add DNS records:
# Type: CNAME
# Name: www
# Value: [static-web-app-url].azurestaticapps.net
#
# Type: TXT
# Name: _dnsauth.www
# Value: [validation-token]
```

### Add Custom Domain to Backend

```bash
# Option 1: Use Azure Application Gateway
# Option 2: Use Azure Front Door
# Option 3: Use custom DNS with ACI FQDN

# Get ACI FQDN
az container show --resource-group codex-dominion-rg --name codex-backend --query "ipAddress.fqdn"

# Create CNAME record:
# api.codexdominion.com -> codex-backend.eastus.azurecontainer.io
```

---

## 📞 Support & Resources

### Azure Portal Quick Links

- **Resource Group:** https://portal.azure.com/#@/resource/subscriptions/YOUR_SUB/resourceGroups/codex-dominion-rg
- **Container Instances:** https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.ContainerInstance%2FcontainerGroups
- **Static Web Apps:** https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2FStaticSites
- **Container Registry:** https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.ContainerRegistry%2Fregistries

### Azure CLI Documentation

- Azure CLI: https://docs.microsoft.com/cli/azure/
- Container Instances: https://docs.microsoft.com/azure/container-instances/
- Static Web Apps: https://docs.microsoft.com/azure/static-web-apps/
- PostgreSQL: https://docs.microsoft.com/azure/postgresql/

### Quick Health Check Script

Save as `check_azure_health.sh`:

```bash
#!/bin/bash
echo "🔷 Checking Codex Dominion Azure Health..."

# Backend health
echo -e "\n🔧 Backend Status:"
curl -f -s http://codex-backend.eastus.azurecontainer.io:8001/health && echo "✅ Backend healthy" || echo "❌ Backend unhealthy"

# Container status
echo -e "\n📦 Container Status:"
az container show --resource-group codex-dominion-rg --name codex-backend --query "instanceView.state" -o tsv

# Static Web App
echo -e "\n🌐 Frontend Status:"
az staticwebapp show --resource-group codex-dominion-rg --query "[name, defaultHostname]" -o table

echo -e "\n✅ Health check complete!"
```

---

## 🎯 Your Current Setup Summary

✅ **Backend:** Running on Azure Container Instances
✅ **Frontend:** Deployed via Azure Static Web Apps
✅ **Container Registry:** ACR configured
✅ **CI/CD:** GitHub Actions automated deployment
✅ **Location:** East US
✅ **Status:** 🟢 Live and Operational

**Next Recommended Steps:**
1. ✅ Backend is running - Access at: http://codex-backend.eastus.azurecontainer.io:8001
2. ⚠️ Consider provisioning PostgreSQL database for production data
3. ⚠️ Consider adding Redis cache for improved performance
4. ✅ Setup custom domain for professional URLs
5. ✅ Enable Application Insights for monitoring
6. ✅ Configure automated backups
7. ✅ Set cost alerts and budgets

---

**🔥 Your Codex Dominion is LIVE on Azure! 🔥**

*Last Updated: December 10, 2025*
