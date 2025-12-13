# Codex Dominion - Complete Infrastructure Deployment Readiness

**Status**: ⏳ Ready for Deployment (Pending Quota Approval)
**Created**: December 9, 2025
**Resource Group**: codex-rg
**Region**: West US (Static Web App: East US 2)

---

## ✅ Prerequisites Complete

### 1. Resource Providers Registered
All 7 required Azure resource providers are registered:
- ✅ Microsoft.Web
- ✅ Microsoft.DBforPostgreSQL
- ✅ Microsoft.Cache
- ✅ Microsoft.KeyVault
- ✅ Microsoft.Insights
- ✅ Microsoft.ContainerRegistry
- ✅ microsoft.operationalinsights

### 2. Data Services Deployed
Current production data layer (via `main-private.bicep`):
- ✅ PostgreSQL Flexible Server: `codex-pg-westus.postgres.database.azure.com`
- ✅ Redis Cache: `codex-redis-westus.redis.cache.windows.net:6380`
- ✅ Key Vault: `https://codex-kv-westus.vault.azure.net/`
- ✅ Application Insights: Connection string configured
- ✅ Container Registry: `codexacrwestus.azurecr.io`

### 3. Docker Images Ready
- ✅ Backend: `codexacrwestus.azurecr.io/codex-backend:prod` (637MB)
- ✅ Frontend: `codexacrwestus.azurecr.io/codex-frontend:production` (221MB)

### 4. Deployment Templates Ready
- ✅ `infra/main-complete.bicep` (400 lines, clean)
- ✅ `infra/main-complete.parameters.json` (all 23 parameters)
- ✅ `.github/workflows/deploy-complete-infrastructure.yml` (CI/CD pipeline)

---

## ❌ Blocking Issue: Quota Exhaustion

### Current Quota Status (West US)
```
❌ Free VMs (F1): 0 available (need 1 for Static Web App)
❌ Basic VMs (B1): 0 available (need 1 for App Service)
❌ Dynamic VMs (Y1): 0 available (need 1 for Function App)
```

**Verification Command**:
```powershell
.\test-compute-quotas.ps1
```

### Required Quotas
Based on `QUOTA_REQUEST_JUSTIFICATION.md`, request the following in **West US**:

| Quota Type | Current | Requested | Purpose |
|------------|---------|-----------|---------|
| **BSv2 vCPUs** | 0 | 2 | App Service Plan (B1 = 1 vCPU) |
| **Av2 vCPUs** | 0 | 1 | Function App scaling buffer |
| **Dynamic vCPUs** | 0 | 2 | Function App (Y1 Consumption) |
| **Total Regional vCPUs** | 0 | 10 | Overall subscription limit |

---

## 🚀 Deployment Plan

### Phase 1: Submit Quota Requests (User Action Required)

1. **Navigate to Azure Portal**:
   ```
   https://portal.azure.com/#view/Microsoft_Azure_Capacity/QuotaMenuBlade
   ```

2. **Select Compute Quotas**:
   - Subscription: `f86506f8-7d33-48de-995d-f51e6f590cb1`
   - Region: **West US**

3. **Submit 4 Requests**:
   - **BSv2 vCPUs**: Increase to **2**
   - **Av2 vCPUs**: Increase to **1**
   - **Dynamic vCPUs**: Increase to **2**
   - **Total Regional vCPUs**: Increase to **10**

4. **Justification** (copy from `QUOTA_REQUEST_JUSTIFICATION.md`):
   - Business case: Production deployment of Codex Dominion application
   - Technical architecture: Backend API, serverless functions, frontend SPA
   - Cost commitment: $60-75/month
   - Timeline impact: Critical for production launch

5. **Expected Approval**: 1-2 business days

---

### Phase 2: Verify Quota Approval

Once approved, run validation:

```powershell
# Test compute quota availability
.\test-compute-quotas.ps1

# Expected output:
# ✅ Free Tier (F1): AVAILABLE
# ✅ Basic Tier (B1): AVAILABLE
# ✅ Consumption Tier (Y1): AVAILABLE
```

---

### Phase 3: Deploy Complete Infrastructure

#### Option A: GitHub Actions (Recommended)

1. **Trigger Workflow**:
   - Navigate to: Actions → Deploy Complete Azure Infrastructure
   - Click "Run workflow" → "Run workflow on main"

2. **Monitor Deployment**:
   - Watch workflow logs for progress
   - Validation → What-If → Deploy → Display Outputs
   - Expected duration: 15-20 minutes

3. **Verify Outputs**:
   ```
   webAppUrl: https://codex-backend-app.azurewebsites.net
   functionAppUrl: https://codex-functions.azurewebsites.net
   staticWebAppUrl: https://[generated].azurestaticapps.net
   postgresHost: codex-pg-westus.postgres.database.azure.com
   redisHost: codex-redis-westus.redis.cache.windows.net
   keyVaultUri: https://codex-kv-westus.vault.azure.net/
   acrLoginServer: codexacrwestus.azurecr.io
   ```

#### Option B: Local Deployment

```powershell
# Authenticate
az login
az account set --subscription f86506f8-7d33-48de-995d-f51e6f590cb1

# Validate template
az deployment group validate `
  --resource-group codex-rg `
  --template-file infra/main-complete.bicep `
  --parameters @infra/main-complete.parameters.json `
  --parameters pgAdminPassword="<YOUR_PASSWORD>"

# What-if analysis
az deployment group what-if `
  --resource-group codex-rg `
  --template-file infra/main-complete.bicep `
  --parameters @infra/main-complete.parameters.json `
  --parameters pgAdminPassword="<YOUR_PASSWORD>"

# Deploy
az deployment group create `
  --resource-group codex-rg `
  --template-file infra/main-complete.bicep `
  --parameters @infra/main-complete.parameters.json `
  --parameters pgAdminPassword="<YOUR_PASSWORD>" `
  --verbose
```

---

## 📦 Infrastructure Components

### Complete Stack (After Deployment)

#### Compute Resources (NEW)
- **App Service Plan**: codex-plan (B1/Linux, 1 vCPU, 1.75GB RAM)
- **Web App**: codex-backend-app (Docker container from ACR)
- **Function App**: codex-functions (Y1 Consumption, Python 3.11)
- **Static Web App**: codex-frontend (Free tier, East US 2)
- **Storage Account**: codexfuncstore (for Functions runtime)

#### Data Resources (EXISTING)
- **PostgreSQL**: codex-pg-westus (Standard_B1ms, Burstable, 32GB)
- **Redis Cache**: codex-redis-westus (Basic C0, 250MB)
- **Key Vault**: codex-kv-westus (Standard, soft delete enabled)
- **Application Insights**: codex-insights-westus (30-day retention)
- **Container Registry**: codexacrwestus (Basic, admin enabled)

---

## 🔐 Security Configuration

### Managed Identities
- Web App and Function App have system-assigned identities
- Both identities have Key Vault access policies (get/list secrets)

### Network Security
- All services use HTTPS only
- PostgreSQL: Firewall rule for Azure services (0.0.0.0)
- Redis: Non-SSL port disabled, TLS 1.2+ required
- Key Vault: Soft delete enabled (90-day retention)

### Secrets Management
- PostgreSQL password: GitHub secret `PG_ADMIN_PASSWORD`
- ACR credentials: Retrieved automatically via `acr.listCredentials()`
- Redis keys: Retrieved automatically via `redis.listKeys()`

---

## 🔄 Environment Variables (Web App)

The Web App automatically receives:
```
DOCKER_REGISTRY_SERVER_URL=https://codexacrwestus.azurecr.io
DOCKER_REGISTRY_SERVER_USERNAME=[from ACR]
DOCKER_REGISTRY_SERVER_PASSWORD=[from ACR]
DATABASE_URL=Server=codex-pg-westus.postgres.database.azure.com;Database=codexdb;...
REDIS_HOST=codex-redis-westus.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=[from Redis]
KEY_VAULT_URI=https://codex-kv-westus.vault.azure.net/
ALLOWED_ORIGINS=https://CodexDominion.app
PORT=8080
APPLICATIONINSIGHTS_CONNECTION_STRING=[from App Insights]
```

---

## 💰 Estimated Monthly Costs

| Resource | SKU | Estimated Cost |
|----------|-----|----------------|
| App Service Plan | B1 (1 vCPU, 1.75GB) | ~$13/month |
| Function App | Y1 Consumption | ~$5-10/month |
| Static Web App | Free | $0 |
| PostgreSQL | Standard_B1ms | ~$13/month |
| Redis | Basic C0 | ~$16/month |
| Key Vault | Standard | ~$0.03/month |
| App Insights | 30-day retention | ~$2-5/month |
| Container Registry | Basic | ~$5/month |
| Storage Account | Standard LRS | ~$1/month |
| **Total** | | **~$55-63/month** |

*Note: Actual costs may vary based on usage (data transfer, function executions, etc.)*

---

## ✅ Post-Deployment Verification

After deployment completes:

```powershell
# 1. List all resources
az resource list --resource-group codex-rg --output table

# 2. Check Web App status
az webapp show --name codex-backend-app --resource-group codex-rg --query "state"

# 3. Check Function App status
az functionapp show --name codex-functions --resource-group codex-rg --query "state"

# 4. Test Web App endpoint
curl https://codex-backend-app.azurewebsites.net/health

# 5. Get Static Web App URL
az staticwebapp show --name codex-frontend --resource-group codex-rg --query "defaultHostname"

# 6. Verify container deployment
az webapp config container show --name codex-backend-app --resource-group codex-rg
```

---

## 🐛 Troubleshooting

### If Deployment Fails

1. **Check quota again**:
   ```powershell
   .\test-compute-quotas.ps1
   ```

2. **Review deployment logs**:
   ```powershell
   az deployment group show --resource-group codex-rg --name main-complete
   ```

3. **Check resource provider registration**:
   ```powershell
   .\check-azure-quotas.ps1
   ```

4. **Validate template locally**:
   ```powershell
   az deployment group validate --resource-group codex-rg --template-file infra/main-complete.bicep --parameters @infra/main-complete.parameters.json --parameters pgAdminPassword="test"
   ```

### Common Issues

- **"Quota exceeded"**: Quota request not approved yet, wait 1-2 days
- **"Resource already exists"**: Data services already deployed via main-private.bicep (this is expected)
- **"Image pull failed"**: Check ACR credentials and Docker image tag
- **"PostgreSQL connection failed"**: Verify firewall rules allow Azure services

---

## 📝 Next Steps After Deployment

1. **Update DNS**: Point `CodexDominion.app` to Static Web App URL
2. **Configure Static Web App**: Link GitHub repository for CI/CD
3. **Deploy Function Code**: Push Azure Functions code to Function App
4. **Store Secrets**: Add API keys and secrets to Key Vault
5. **Enable Monitoring**: Configure Application Insights alerts
6. **Scale if Needed**: Upgrade SKUs based on traffic patterns

---

## 📚 Related Files

- `infra/main-complete.bicep` - Complete infrastructure template
- `infra/main-complete.parameters.json` - Parameter values
- `infra/main-private.bicep` - Current data-only deployment (production)
- `.github/workflows/deploy-complete-infrastructure.yml` - CI/CD pipeline
- `QUOTA_REQUEST_JUSTIFICATION.md` - Quota request documentation
- `check-azure-quotas.ps1` - Provider and validation check
- `test-compute-quotas.ps1` - Compute quota verification

---

**Status Summary**:
- ✅ Templates ready
- ✅ Images ready
- ✅ Data services deployed
- ❌ **Quota approval required** ← **BLOCKER**
- ⏳ Ready to deploy once quota approved

**Action Required**: Submit quota requests via Azure Portal, then trigger deployment workflow.
