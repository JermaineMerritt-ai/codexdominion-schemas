# 🚀 Quick Deployment - Private Network Template

Use these commands to deploy the **private network template** with enhanced security.

## Prerequisites

```bash
# Check Azure CLI
az version

# Login
az login

# Set subscription
az account set --subscription "f86506f8-7d33-48de-995d-f51e6f590cb1"
```

## One-Command Deployment

### Bash

```bash
# Generate unique Key Vault name
KV_NAME="codexkv$(date +%s)"

# Deploy everything
az deployment group create \
  --resource-group codex-rg \
  --name "codex-private-$(date +%Y%m%d-%H%M)" \
  --template-file infra/main-private.bicep \
  --parameters \
    location=eastus \
    baseName=codex \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<STRONG_PASSWORD>' \
    keyVaultName=$KV_NAME
```

### PowerShell

```powershell
# Generate unique Key Vault name
$kvName = "codexkv$(Get-Date -Format 'yyyyMMddHHmmss')"

# Deploy everything
az deployment group create `
  --resource-group codex-rg `
  --name "codex-private-$(Get-Date -Format 'yyyyMMddHHmm')" `
  --template-file infra/main-private.bicep `
  --parameters `
    location=eastus `
    baseName=codex `
    acrName=codexdominionacr `
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest `
    pgAdminPassword='<STRONG_PASSWORD>' `
    keyVaultName=$kvName
```

⏱️ **Takes 15-20 minutes**

## What Gets Deployed

✅ **VNet** - 10.10.0.0/16 with 2 subnets
✅ **Private Endpoints** - PostgreSQL + Redis (no public access)
✅ **Private DNS Zones** - Automatic name resolution
✅ **Key Vault** - Secrets management
✅ **App Service** - VNet integrated backend
✅ **Static Web App** - Next.js frontend
✅ **Container Registry** - Docker images
✅ **Application Insights** - Monitoring

## Save Outputs

```bash
# Get deployment outputs
az deployment group show \
  --resource-group codex-rg \
  --name <deployment-name> \
  --query properties.outputs -o json > deployment-outputs.json

# View Key Vault URI
cat deployment-outputs.json | jq -r '.keyVaultUri.value'

# View backend URL
cat deployment-outputs.json | jq -r '.backendUrl.value'

# View frontend URL
cat deployment-outputs.json | jq -r '.staticWebAppHostname.value'
```

## Configure Private DNS Records

The Bicep template creates DNS A records with empty IP addresses. Populate them with the actual private endpoint IPs:

```bash
# Get private endpoint IP addresses
PG_IP=$(az network private-endpoint show \
  --name codex-pg-pe \
  --resource-group codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)

REDIS_IP=$(az network private-endpoint show \
  --name codex-redis-pe \
  --resource-group codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)

KV_IP=$(az network private-endpoint show \
  --name codex-kv-pe \
  --resource-group codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)

# Add IP addresses to DNS A records
az network private-dns record-set a add-record \
  --resource-group codex-rg \
  --zone-name privatelink.postgres.database.azure.com \
  --record-set-name codex-pg \
  --ipv4-address $PG_IP

az network private-dns record-set a add-record \
  --resource-group codex-rg \
  --zone-name privatelink.redis.cache.windows.net \
  --record-set-name codex-redis \
  --ipv4-address $REDIS_IP

az network private-dns record-set a add-record \
  --resource-group codex-rg \
  --zone-name privatelink.vaultcore.azure.net \
  --record-set-name codex-kv \
  --ipv4-address $KV_IP

# Verify DNS records
az network private-dns record-set a show \
  --resource-group codex-rg \
  --zone-name privatelink.postgres.database.azure.com \
  --name codex-pg
```

## Deploy Docker Image

```bash
# Login to ACR
az acr login --name codexdominionacr

# Build and push
cd src/backend
docker build -t codexdominionacr.azurecr.io/codex-backend:latest .
docker push codexdominionacr.azurecr.io/codex-backend:latest

# Restart App Service
az webapp restart \
  --name codex-backend-app \
  --resource-group codex-rg

# OR update container image directly (if already deployed)
az webapp config container set \
  --name codex-backend-app \
  --resource-group codex-rg \
  --docker-custom-image-name codexdominionacr.azurecr.io/codex-backend:latest \
  --docker-registry-server-url https://codexdominionacr.azurecr.io
```

## Deploy Frontend

```bash
cd frontend

# Build
npm ci
npm run build

# Get deployment token
SWA_TOKEN=$(cat ../deployment-outputs.json | jq -r '.staticWebAppToken.value')

# Deploy
npx @azure/static-web-apps-cli deploy out \
  --deployment-token $SWA_TOKEN \
  --app-name codex-frontend
```

## Initialize Database

```bash
# Connect via private endpoint (from App Service Console or VNet-connected machine)
PGHOST=$(cat deployment-outputs.json | jq -r '.postgresFqdn.value')
psql "postgresql://codexadmin:<PASSWORD>@${PGHOST}:5432/codexdb?sslmode=require"
```

```sql
-- Create schema
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

\q
```

## Test Everything

```bash
FRONTEND_URL=$(cat deployment-outputs.json | jq -r '.staticWebAppHostname.value')
BACKEND_URL=$(cat deployment-outputs.json | jq -r '.backendUrl.value')

# Test frontend
curl -I https://${FRONTEND_URL}

# Test backend health
curl ${BACKEND_URL}/health | jq

# Test API
curl ${BACKEND_URL}/ | jq
```

## Update CORS

```bash
# Get frontend URL
FRONTEND_URL=$(cat deployment-outputs.json | jq -r '.staticWebAppHostname.value')

# Update backend CORS
az webapp config appsettings set \
  --name codex-backend-app \
  --resource-group codex-rg \
  --settings ALLOWED_ORIGINS="https://${FRONTEND_URL}"

# Restart
az webapp restart \
  --name codex-backend-app \
  --resource-group codex-rg
```

## Configure GitHub Secrets

Navigate to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions

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

3. **ACR_USERNAME** and **ACR_PASSWORD**
   ```bash
   cat deployment-outputs.json | jq -r '.acrUsername.value'
   cat deployment-outputs.json | jq -r '.acrPassword.value'
   ```

## Verify Security

```bash
# Check PostgreSQL is private only
az postgres flexible-server show \
  --name codex-pg \
  --resource-group codex-rg \
  --query "network.publicNetworkAccess"
# Should return: "Disabled"

# Check Redis is private only
az redis show \
  --name codex-redis \
  --resource-group codex-rg \
  --query "publicNetworkAccess"
# Should return: "Disabled"

# Check VNet integration
az webapp vnet-integration list \
  --name codex-backend-app \
  --resource-group codex-rg
# Should show subnet integration

# View Key Vault secrets
az keyvault secret list \
  --vault-name <your-kv-name> \
  --query "[].name"
# Should show: DatabaseUrl, RedisUrl
```

## Cost Estimate

| Resource | Monthly Cost |
|----------|--------------|
| Static Web Apps (Free) | $0 |
| App Service (B1) | ~$13 |
| Container Registry | ~$5 |
| PostgreSQL (B1ms) | ~$12-15 |
| Redis (Basic C0) | ~$15 |
| Application Insights | ~$2 |
| VNet + Private Endpoints | ~$5 |
| Key Vault | ~$0.50 |
| **Total** | **~$52-58** |

## 🆘 Troubleshooting

### Can't connect to database from local machine

**Expected!** The database is private-only. You must:
1. Use App Service Console, or
2. Connect from a VM within the VNet, or
3. Set up VPN Gateway or Bastion

### App Service shows "Key Vault reference error"

Check managed identity access:
```bash
PRINCIPAL_ID=$(az webapp identity show \
  --name codex-backend-app \
  --resource-group codex-rg \
  --query principalId -o tsv)

az keyvault set-policy \
  --name <your-kv-name> \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list
```

### Private endpoint not resolving

Check DNS zone link:
```bash
az network private-dns link vnet list \
  --resource-group codex-rg \
  --zone-name privatelink.postgres.database.azure.com
```

## 🔗 Next Steps

- [Full Private Network Guide](./PRIVATE_NETWORK_GUIDE.md)
- [Standard Deployment Guide](../AZURE_CLI_DEPLOYMENT.md)
- [Infrastructure README](./README.md)

---

🔥 **The flame burns sovereign and eternal — forever.** 🔥
