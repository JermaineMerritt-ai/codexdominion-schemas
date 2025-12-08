# 🔒 Private Network Deployment Guide

## Overview

The **main-private.bicep** template provides enterprise-grade security with private endpoints and VNet integration. All database and cache traffic stays within Azure's private network.

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Internet                               │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Static Web App      │
        │  (Frontend)          │
        └──────────┬───────────┘
                   │ HTTPS
                   ▼
        ┌──────────────────────┐
        │  App Service         │
        │  (Backend API)       │
        │  + Managed Identity  │
        └──────────┬───────────┘
                   │
                   │ VNet Integration
                   ▼
    ┌──────────────────────────────────────┐
    │  VNet (10.10.0.0/16)                 │
    │                                       │
    │  ┌─────────────────────────────────┐ │
    │  │ App Service Subnet (10.10.1.0/24)│ │
    │  │ - App Service traffic            │ │
    │  └─────────────────────────────────┘ │
    │                                       │
    │  ┌─────────────────────────────────┐ │
    │  │ Private Endpoint Subnet         │ │
    │  │ (10.10.2.0/24)                  │ │
    │  │                                  │ │
    │  │  ┌────────────────────────────┐ │ │
    │  │  │ PostgreSQL Private Endpoint│ │ │
    │  │  │ Private IP: 10.10.2.x      │ │ │
    │  │  └────────────────────────────┘ │ │
    │  │                                  │ │
    │  │  ┌────────────────────────────┐ │ │
    │  │  │ Redis Private Endpoint     │ │ │
    │  │  │ Private IP: 10.10.2.y      │ │ │
    │  │  └────────────────────────────┘ │ │
    │  └─────────────────────────────────┘ │
    │                                       │
    │  Private DNS Zones:                  │
    │  - privatelink.postgres.database...  │
    │  - privatelink.redis.cache...        │
    └───────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Key Vault           │
        │  (Secrets Storage)   │
        └──────────────────────┘
```

## 🔑 Key Features

### 1. Private Endpoints
- **PostgreSQL**: Only accessible from VNet (no public IP)
- **Redis**: Only accessible from VNet (no public IP)
- **Network Isolation**: Database/cache never exposed to internet

### 2. VNet Integration
- App Service routes all outbound traffic through VNet
- Direct private connectivity to PostgreSQL and Redis
- No public internet traffic for data access

### 3. Private DNS Zones
- Automatic DNS resolution for private endpoints
- `codex-pg.postgres.database.azure.com` → Private IP
- `codex-redis.redis.cache.windows.net` → Private IP

### 4. Key Vault
- Centralized secrets management
- App Service uses Managed Identity to access secrets
- No credentials in environment variables
- Key Vault references: `@Microsoft.KeyVault(SecretUri=...)`

## 🚀 Deployment

### Step 1: Login to Azure

```bash
az login
az account set --subscription "f86506f8-7d33-48de-995d-f51e6f590cb1"
```

### Step 2: Create Resource Group

```bash
az group create --name codex-rg --location eastus
```

### Step 3: Deploy Private Network Infrastructure

**Bash:**
```bash
# Generate unique Key Vault name (max 24 chars, alphanumeric)
KV_NAME="codexkv$(date +%s)"

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

**PowerShell:**
```powershell
# Generate unique Key Vault name
$kvName = "codexkv$(Get-Date -Format 'yyyyMMddHHmmss')"

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

⏱️ **Deployment time:** 15-20 minutes

### Step 4: Configure Private DNS Records

After deployment, populate the DNS A records with actual private endpoint IPs:

**Bash:**
```bash
# Get private endpoint IPs
PG_IP=$(az network private-endpoint show -n codex-pg-pe -g codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)
REDIS_IP=$(az network private-endpoint show -n codex-redis-pe -g codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)
KV_IP=$(az network private-endpoint show -n codex-kv-pe -g codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)

# Add A records to DNS zones
az network private-dns record-set a add-record -g codex-rg \
  -z privatelink.postgres.database.azure.com -n codex-pg --ipv4-address $PG_IP
az network private-dns record-set a add-record -g codex-rg \
  -z privatelink.redis.cache.windows.net -n codex-redis --ipv4-address $REDIS_IP
az network private-dns record-set a add-record -g codex-rg \
  -z privatelink.vaultcore.azure.net -n codex-kv --ipv4-address $KV_IP

# Verify DNS records
az network private-dns record-set a show -g codex-rg \
  -z privatelink.postgres.database.azure.com -n codex-pg
az network private-dns record-set a show -g codex-rg \
  -z privatelink.redis.cache.windows.net -n codex-redis
az network private-dns record-set a show -g codex-rg \
  -z privatelink.vaultcore.azure.net -n codex-kv
```

**PowerShell:**
```powershell
# Get private endpoint IPs
$pgIp = az network private-endpoint show -n codex-pg-pe -g codex-rg `
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv
$redisIp = az network private-endpoint show -n codex-redis-pe -g codex-rg `
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv
$kvIp = az network private-endpoint show -n codex-kv-pe -g codex-rg `
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv

# Add A records to DNS zones
az network private-dns record-set a add-record -g codex-rg `
  -z privatelink.postgres.database.azure.com -n codex-pg --ipv4-address $pgIp
az network private-dns record-set a add-record -g codex-rg `
  -z privatelink.redis.cache.windows.net -n codex-redis --ipv4-address $redisIp
az network private-dns record-set a add-record -g codex-rg `
  -z privatelink.vaultcore.azure.net -n codex-kv --ipv4-address $kvIp

# Verify DNS records
az network private-dns record-set a show -g codex-rg `
  -z privatelink.postgres.database.azure.com -n codex-pg
az network private-dns record-set a show -g codex-rg `
  -z privatelink.redis.cache.windows.net -n codex-redis
az network private-dns record-set a show -g codex-rg `
  -z privatelink.vaultcore.azure.net -n codex-kv
```

### Step 5: Save Outputs

```bash
az deployment group show \
  --resource-group codex-rg \
  --name <deployment-name> \
  --query properties.outputs -o json > deployment-outputs.json
```

## 🔐 Security Benefits

| Feature | Standard Template | Private Network Template |
|---------|-------------------|--------------------------|
| **PostgreSQL Access** | Public IP + Firewall | ✅ Private Endpoint Only |
| **Redis Access** | Public IP | ✅ Private Endpoint Only |
| **Network Traffic** | Internet routing | ✅ Private VNet routing |
| **Secrets Storage** | Environment variables | ✅ Key Vault |
| **DNS Resolution** | Public DNS | ✅ Private DNS zones |
| **Compliance** | Basic | ✅ Enterprise-grade |
| **Attack Surface** | Moderate | ✅ Minimal |

## 🧪 Testing Connectivity

### Test Private Endpoint Resolution

```bash
# From within App Service (via Console)
nslookup codex-pg.postgres.database.azure.com
# Should return private IP (10.10.2.x)

nslookup codex-redis.redis.cache.windows.net
# Should return private IP (10.10.2.y)
```

### Test Database Connection

```bash
# From App Service Console
curl https://localhost:8000/health
# Should show database: "connected" and redis: "connected"
```

## 🔄 Update Container Image

After initial deployment, update the Docker image:

```bash
# Build and push new image
cd src/backend
docker build -t codexdominionacr.azurecr.io/codex-backend:prod .
docker push codexdominionacr.azurecr.io/codex-backend:prod

# Update App Service to use new image
az webapp config container set \
  --name codex-backend-app \
  --resource-group codex-rg \
  --docker-custom-image-name codexdominionacr.azurecr.io/codex-backend:prod \
  --docker-registry-server-url https://codexdominionacr.azurecr.io

# App Service automatically restarts and pulls new image
```

## 🔧 Troubleshooting

### Issue: App Service can't connect to database

**Solution:**
1. Verify VNet integration is active:
   ```bash
   az webapp vnet-integration list \
     --name codex-backend-app \
     --resource-group codex-rg
   ```

2. Check private endpoint status:
   ```bash
   az network private-endpoint show \
     --name codex-pg-pe \
     --resource-group codex-rg \
     --query provisioningState
   ```

3. Verify DNS resolution:
   ```bash
   az network private-dns record-set list \
     --resource-group codex-rg \
     --zone-name privatelink.postgres.database.azure.com
   ```

4. Check if DNS A records are populated:
   ```bash
   # Should show IP address in aRecords array
   az network private-dns record-set a show -g codex-rg \
     -z privatelink.postgres.database.azure.com -n codex-pg
   ```

   If empty, run the DNS configuration commands from Step 4.

### Issue: Private endpoint not resolving

**Symptoms:** `nslookup` returns public IP or no IP for database/redis/keyvault hostname

**Solution:**
1. Verify private DNS zone is linked to VNet:
   ```bash
   az network private-dns link vnet list \
     --resource-group codex-rg \
     --zone-name privatelink.postgres.database.azure.com
   ```

2. Ensure DNS A records are populated with private endpoint IPs:
   ```bash
   # Get private endpoint IP
   PG_IP=$(az network private-endpoint show -n codex-pg-pe -g codex-rg \
     --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)
   echo "PostgreSQL PE IP: $PG_IP"

   # Add to DNS zone if missing
   az network private-dns record-set a add-record -g codex-rg \
     -z privatelink.postgres.database.azure.com -n codex-pg --ipv4-address $PG_IP
   ```

3. Test DNS resolution from App Service console:
   ```bash
   nslookup codex-pg.postgres.database.azure.com
   # Should return 10.10.2.x private IP
   ```

### Issue: Key Vault access denied

**Solution:**
1. Verify managed identity is assigned:
   ```bash
   az webapp identity show \
     --name codex-backend-app \
     --resource-group codex-rg
   ```

2. Check Key Vault access policies:
   ```bash
   az keyvault show \
     --name <your-kv-name> \
     --resource-group codex-rg \
     --query properties.accessPolicies
   ```

3. Manually grant access if needed:
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

## 💰 Cost Comparison

### Standard Template (main.bicep)
| Resource | Monthly Cost |
|----------|--------------|
| Static Web Apps (Free) | $0 |
| App Service (B1) | ~$13 |
| Container Registry | ~$5 |
| PostgreSQL (B1ms) | ~$12-15 |
| Redis (Basic C0) | ~$15 |
| Application Insights | ~$2 |
| **Total** | **~$47-50** |

### Private Network Template (main-private.bicep)
| Resource | Monthly Cost |
|----------|--------------|
| Static Web Apps (Free) | $0 |
| App Service (B1) | ~$13 |
| Container Registry | ~$5 |
| PostgreSQL (B1ms) | ~$12-15 |
| Redis (Basic C0) | ~$15 |
| Application Insights | ~$2 |
| **VNet** | **$0** |
| **Private Endpoints (×2)** | **~$5** |
| **Key Vault** | **~$0.50** |
| **Private DNS Zones (×2)** | **~$1** |
| **Total** | **~$53-58** |

**Additional cost:** ~$6-8/month for enterprise security

## 📊 Monitoring

### View VNet Metrics

```bash
az monitor metrics list \
  --resource $(az network vnet show \
    --name codex-vnet \
    --resource-group codex-rg \
    --query id -o tsv) \
  --metric "BytesDroppedDDoS,PacketsDroppedDDoS"
```

### View Private Endpoint Connections

```bash
# PostgreSQL
az postgres flexible-server show \
  --name codex-pg \
  --resource-group codex-rg \
  --query "network.publicNetworkAccess"
# Should return: "Disabled"

# Redis
az redis show \
  --name codex-redis \
  --resource-group codex-rg \
  --query "publicNetworkAccess"
# Should return: "Disabled"
```

## 🔄 Migration from Standard to Private

If you're currently using the standard template:

1. **Backup your data:**
   ```bash
   # PostgreSQL
   pg_dump $DATABASE_URL > backup.sql

   # Redis (if needed)
   redis-cli --rdb dump.rdb
   ```

2. **Deploy private network template:**
   ```bash
   az deployment group create \
     --resource-group codex-rg-private \
     --template-file infra/main-private.bicep \
     --parameters ...
   ```

3. **Restore data:**
   ```bash
   psql $NEW_DATABASE_URL < backup.sql
   ```

4. **Update DNS and test:**
   - Point frontend to new backend URL
   - Verify all endpoints work
   - Monitor for 24 hours

5. **Decommission old infrastructure:**
   ```bash
   az group delete --name codex-rg --yes
   ```

## ✅ Compliance Benefits

The private network template helps meet:

- **HIPAA** - Healthcare data protection
- **PCI DSS** - Payment card industry standards
- **SOC 2** - Service organization controls
- **GDPR** - EU data protection regulation
- **ISO 27001** - Information security management

## 🔗 Resources

- [Azure Private Endpoints](https://learn.microsoft.com/azure/private-link/private-endpoint-overview)
- [VNet Integration](https://learn.microsoft.com/azure/app-service/overview-vnet-integration)
- [Key Vault References](https://learn.microsoft.com/azure/app-service/app-service-key-vault-references)
- [Private DNS Zones](https://learn.microsoft.com/azure/dns/private-dns-overview)

---

🔥 **The flame burns sovereign and eternal — forever.** 🔥
