# 🚀 Azure Deployment - Complete CLI Guide

## ⚡ Super Quick Start (Private Network - Recommended)

For the **most secure deployment** with private endpoints:

```bash
# 1-4. Login and setup
az login
az account set --subscription "f86506f8-7d33-48de-995d-f51e6f590cb1"
az group create --name codex-rg --location eastus

# 5. Deploy with private network (ONE COMMAND)
KV_NAME="codexkv$(date +%s)"
az deployment group create \
  --resource-group codex-rg \
  --name codex-private-$(date +%Y%m%d-%H%M) \
  --template-file infra/main-private.bicep \
  --parameters \
    location=eastus \
    baseName=codex \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<YOUR_STRONG_PASSWORD>' \
    keyVaultName=$KV_NAME
```

📖 **See [Quick Start Guide](./infra/QUICK_START_PRIVATE.md) for complete private network deployment**

---

## Standard Deployment Commands

```bash
# 1. Login to Azure
az login

# 2. Set subscription
az account set --subscription "f86506f8-7d33-48de-995d-f51e6f590cb1"

# 3. Create resource group
az group create --name codex-rg --location eastus

# 4. Deploy infrastructure (replace <YOUR_PASSWORD>)
az deployment group create \
  --resource-group codex-rg \
  --name codex-infrastructure-$(date +%Y%m%d-%H%M%S) \
  --template-file infra/main.bicep \
  --parameters \
    location="eastus" \
    baseName="codex" \
    environment="prod" \
    acrName="codexdominionacr" \
    dockerImage="codexdominionacr.azurecr.io/codex-backend:latest" \
    pgAdminPassword="<YOUR_STRONG_PASSWORD>" \
    pgAdminUser="codexadmin" \
    pgDbName="codexdb" \
    pgVersion="16" \
    swaSku="Free" \
    appServiceSku="B1" \
    redisSku="Basic" \
    backendPort=8001
```

## 🔒 Architecture Options

You have **two deployment templates** to choose from:

### Option 1: Standard (main.bicep)
- PostgreSQL with firewall rules
- Redis with public access
- Environment variables for secrets
- **Cost:** ~$47-50/month
- **Use case:** Development, testing, simple deployments

### Option 2: Private Network (main-private.bicep) ⭐ RECOMMENDED
- Private endpoints for PostgreSQL and Redis
- VNet integration for App Service
- Azure Key Vault for secrets
- Private DNS zones
- **Cost:** ~$50-55/month
- **Use case:** Production, compliance, enterprise security

**This guide uses the private network template for maximum security.**

---

## 📋 Detailed Step-by-Step Guide

### Prerequisites Check

```bash
# Verify Azure CLI
az version

# Expected: azure-cli version 2.50.0+
```

### Step 1: Authentication

```bash
# Login (opens browser)
az login

# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "f86506f8-7d33-48de-995d-f51e6f590cb1"

# Verify
az account show
```

### Step 2: Generate Secure Password

**Linux/Mac:**
```bash
openssl rand -base64 32
```

**Windows PowerShell:**
```powershell
-join ((33..126) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Save this password securely!** You'll need it for database access.

### Step 3: Deploy Infrastructure

**Bash:**
```bash
# Option 1: Original template (public access with firewall rules)
az deployment group create \
  --resource-group codex-rg \
  --name "codex-infra-$(date +%Y%m%d-%H%M)" \
  --template-file infra/main.bicep \
  --parameters \
    location=eastus \
    baseName=codex \
    environment=prod \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='YourSecurePassword123!' \
    pgDbName=codexdb \
    backendPort=8001 \
    enableAppInsights=true

# Option 2: Private network template (RECOMMENDED - enterprise security)
az deployment group create \
  --resource-group codex-rg \
  --name "codex-infra-private-$(date +%Y%m%d-%H%M)" \
  --template-file infra/main-private.bicep \
  --parameters \
    location=eastus \
    baseName=codex \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='YourSecurePassword123!' \
    pgDbName=codexdb \
    keyVaultName=codexkv$(date +%s) \
    backendPort=8000 \
    allowedOrigins='*'
```

**PowerShell (Original):**
```powershell
az deployment group create `
  --resource-group codex-rg `
  --name "codex-infra-$(Get-Date -Format 'yyyyMMddHHmm')" `
  --template-file infra/main.bicep `
  --parameters `
    location=eastus `
    baseName=codex `
    environment=prod `
    acrName=codexdominionacr `
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest `
    pgAdminPassword='YourSecurePassword123!' `
    pgDbName=codexdb `
    backendPort=8001 `
    enableAppInsights=true
```

**PowerShell (Private Network - RECOMMENDED):**
```powershell
$timestamp = Get-Date -Format 'yyyyMMddHHmmss'
az deployment group create `
  --resource-group codex-rg `
  --name "codex-infra-private-$(Get-Date -Format 'yyyyMMddHHmm')" `
  --template-file infra/main-private.bicep `
  --parameters `
    location=eastus `
    baseName=codex `
    acrName=codexdominionacr `
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest `
    pgAdminPassword='YourSecurePassword123!' `
    pgDbName=codexdb `
    keyVaultName="codexkv$timestamp" `
    backendPort=8000 `
    allowedOrigins='*'
```

⏱️ **Takes 10-15 minutes**

### Step 4: Save Deployment Outputs

```bash
# Get outputs
az deployment group show \
  --resource-group codex-rg \
  --name <deployment-name> \
  --query properties.outputs -o json > deployment-outputs.json

# View outputs
cat deployment-outputs.json | jq
```

**Key outputs:**
- `staticWebAppHostname` - Frontend URL
- `staticWebAppToken` - GitHub deployment token
- `backendUrl` - API URL
- `acrLoginServer` - Container registry
- `postgresFqdn` - Database server

### Step 5: Build & Push Docker Image

```bash
# Login to ACR
az acr login --name codexdominionacr

# Build backend image
cd src/backend
docker build -t codexdominionacr.azurecr.io/codex-backend:latest .
docker build -t codexdominionacr.azurecr.io/codex-backend:prod .

# Push to registry
docker push codexdominionacr.azurecr.io/codex-backend:latest
docker push codexdominionacr.azurecr.io/codex-backend:prod

# Verify
az acr repository list --name codexdominionacr -o table
```

### Step 6: Update Container Configuration

```bash
# Update the container image reference
az webapp config container set \
  --name codex-backend-app \
  --resource-group codex-rg \
  --docker-custom-image-name codexdominionacr.azurecr.io/codex-backend:prod \
  --docker-registry-server-url https://codexdominionacr.azurecr.io
```

### Step 7: Restart App Service

```bash
# Restart to pull new image
az webapp restart \
  --name codex-backend-prod \
  --resource-group codex-rg

# Wait for startup
sleep 30

# Check status
az webapp show \
  --name codex-backend-prod \
  --resource-group codex-rg \
  --query state -o tsv
```

### Step 7: Deploy Frontend

```bash
cd frontend

# Build
npm ci
npm run build

# Get deployment token
export SWA_TOKEN=$(cat ../deployment-outputs.json | jq -r '.staticWebAppToken.value')

# Deploy with SWA CLI
npm install -g @azure/static-web-apps-cli
swa deploy out --deployment-token $SWA_TOKEN --app-name codex-frontend-prod
```

### Step 8: Initialize Database

```bash
# Get connection details
PGHOST=$(cat deployment-outputs.json | jq -r '.postgresFqdn.value')
PGUSER="codexadmin"
PGPASSWORD="YourSecurePassword123!"
PGDB="codexdb"

# Connect
psql "postgresql://${PGUSER}:${PGPASSWORD}@${PGHOST}:5432/${PGDB}?sslmode=require"
```

**Create schema:**
```sql
CREATE TABLE capsules (
    id SERIAL PRIMARY KEY,
    heir_id VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE signals (
    id SERIAL PRIMARY KEY,
    heir_id VARCHAR(255) NOT NULL,
    signal_type VARCHAR(100) NOT NULL,
    payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_signals_heir_id ON signals(heir_id);
CREATE INDEX idx_signals_created_at ON signals(created_at);

CREATE TABLE replays (
    id SERIAL PRIMARY KEY,
    heir_id VARCHAR(255) NOT NULL,
    replay_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_replays_heir_id ON replays(heir_id);

\q
```

### Step 9: Configure GitHub Secrets

**Navigate to:** https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions

**Add these secrets:**

1. **AZURE_STATIC_WEB_APPS_API_TOKEN**
   ```bash
   cat deployment-outputs.json | jq -r '.staticWebAppToken.value'
   ```

2. **AZURE_CREDENTIALS**
   ```bash
   az ad sp create-for-rbac \
     --name "codex-github-actions" \
     --role contributor \
     --scopes /subscriptions/f86506f8-7d33-48de-995d-f51e6f590cb1/resourceGroups/codex-rg \
     --json-auth
   ```
   Copy the entire JSON output

3. **DB_ADMIN_PASSWORD**
   ```
   YourSecurePassword123!
   ```

### Step 10: Update CORS Settings

```bash
# Get Static Web App hostname
FRONTEND_URL=$(cat deployment-outputs.json | jq -r '.staticWebAppHostname.value')

# Update backend CORS
az webapp config appsettings set \
  --name codex-backend-prod \
  --resource-group codex-rg \
  --settings ALLOWED_ORIGINS="https://${FRONTEND_URL}"
```

### Step 11: Test Everything

```bash
# Get URLs
FRONTEND_URL=$(cat deployment-outputs.json | jq -r '.staticWebAppHostname.value')
BACKEND_URL=$(cat deployment-outputs.json | jq -r '.backendUrl.value')

# Test frontend
curl -I https://${FRONTEND_URL}

# Test backend health
curl ${BACKEND_URL}/health | jq

# Test backend API
curl ${BACKEND_URL}/ | jq

# Test database connection
curl ${BACKEND_URL}/health | jq .database

# Test Redis
curl ${BACKEND_URL}/health | jq .redis
```

## 🎯 Quick Reference

### View Logs
```bash
# App Service logs
az webapp log tail --name codex-backend-prod --resource-group codex-rg

# Download logs
az webapp log download --name codex-backend-prod --resource-group codex-rg
```

### Update Container Image
```bash
# Update to a new image version
az webapp config container set \
  --name codex-backend-app \
  --resource-group codex-rg \
  --docker-custom-image-name codexdominionacr.azurecr.io/codex-backend:prod \
  --docker-registry-server-url https://codexdominionacr.azurecr.io

# App Service will automatically pull and restart
```

### Update Environment Variables
```bash
az webapp config appsettings set \
  --name codex-backend-app \
  --resource-group codex-rg \
  --settings \
    NEW_VAR="value" \
    ANOTHER_VAR="another_value"
```

### Restart Services
```bash
# Restart backend
az webapp restart --name codex-backend-prod --resource-group codex-rg

# Restart PostgreSQL
az postgres flexible-server restart --name codex-pg-prod --resource-group codex-rg

# Restart Redis
az redis force-reboot --name codex-redis-prod --resource-group codex-rg --reboot-type AllNodes
```

### List Resources
```bash
# All resources in resource group
az resource list --resource-group codex-rg -o table

# Container images
az acr repository list --name codexdominionacr -o table

# Databases
az postgres flexible-server db list --server-name codex-pg-prod --resource-group codex-rg -o table
```

### Cost Monitoring
```bash
# View resource costs
az consumption usage list \
  --start-date $(date -d '30 days ago' +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --query "[?resourceGroup=='codex-rg']" \
  -o table
```

## 🆘 Troubleshooting

### Deployment Failed
```bash
# View error details
az deployment group show \
  --resource-group codex-rg \
  --name <deployment-name> \
  --query properties.error

# List all deployments
az deployment group list --resource-group codex-rg -o table
```

### App Not Starting
```bash
# Check state
az webapp show --name codex-backend-prod --resource-group codex-rg --query state

# View configuration
az webapp config show --name codex-backend-prod --resource-group codex-rg

# Check container logs
az webapp log tail --name codex-backend-prod --resource-group codex-rg
```

### Database Connection Failed
```bash
# List firewall rules
az postgres flexible-server firewall-rule list \
  --name codex-pg-prod \
  --resource-group codex-rg

# Add your IP
az postgres flexible-server firewall-rule create \
  --resource-group codex-rg \
  --name codex-pg-prod \
  --rule-name allow-my-ip \
  --start-ip-address $(curl -s ifconfig.me) \
  --end-ip-address $(curl -s ifconfig.me)
```

## 📊 Monitoring

### Application Insights
```bash
# Query recent requests
az monitor app-insights query \
  --app codex-insights-prod \
  --analytics-query "requests | where timestamp > ago(1h) | summarize count() by resultCode"
```

### View Metrics
```bash
# App Service metrics
az monitor metrics list \
  --resource $(az webapp show --name codex-backend-prod --resource-group codex-rg --query id -o tsv) \
  --metric "Http4xx,Http5xx,ResponseTime"
```

## 🗑️ Cleanup

### Delete Everything
```bash
# Delete resource group (IRREVERSIBLE!)
az group delete --name codex-rg --yes --no-wait
```

### Delete Specific Resources
```bash
# Delete App Service only
az webapp delete --name codex-backend-prod --resource-group codex-rg

# Delete database only
az postgres flexible-server delete --name codex-pg-prod --resource-group codex-rg --yes
```

## ✅ Deployment Checklist

- [ ] Azure CLI installed
- [ ] Logged in to Azure
- [ ] Subscription selected
- [ ] Resource group created
- [ ] Secure password generated
- [ ] Infrastructure deployed
- [ ] Outputs saved
- [ ] Docker image built
- [ ] Docker image pushed
- [ ] App Service restarted
- [ ] Frontend deployed
- [ ] Database schema initialized
- [ ] GitHub secrets configured
- [ ] CORS settings updated
- [ ] All endpoints tested
- [ ] Monitoring configured

## 💰 Estimated Costs

| Resource | Monthly Cost |
|----------|--------------|
| Static Web Apps (Free) | $0 |
| App Service (B1) | ~$13 |
| Container Registry | ~$5 |
| PostgreSQL (B1ms) | ~$12-15 |
| Redis (Basic) | ~$15 |
| Application Insights | ~$2 |
| **Total** | **~$47-50** |

## 🔗 Resources

- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)
- [App Service Docs](https://learn.microsoft.com/azure/app-service/)
- [Static Web Apps Docs](https://learn.microsoft.com/azure/static-web-apps/)

---

🔥 **The flame burns sovereign and eternal — forever.** 🔥
