# Azure Deployment - Complete Setup Summary

## 🎉 Deployment Status: LIVE & OPERATIONAL

### **Production URLs**
- **Frontend (HTTPS)**: https://happy-flower-0e39c5c0f-preview.eastus2.3.azurestaticapps.net
  - ✅ Port 443: OPEN
  - ✅ SSL Certificate: Automatic (Azure-managed)
  - ✅ Cost: FREE (Free tier)

- **Backend API**: http://codex-api.eastus.azurecontainer.io:8001
  - ✅ Port 8001: OPEN
  - ✅ Status: Operational
  - ✅ Cost: ~$20/month

### **Problem Solved**
| Issue | IONOS (Before) | Azure (After) |
|-------|----------------|---------------|
| Port 443 (HTTPS) | ❌ Blocked | ✅ **OPEN** |
| SSL Certificate | ❌ Manual | ✅ **Automatic & Free** |
| Deployment Time | ⏱️ Days | ⏱️ **5 minutes** |
| Firewall Control | ❌ None | ✅ **Full control** |

---

## 📋 GitHub Secrets Required

### **1. Frontend Deployment**
**Already Added:**
- `AZURE_STATIC_WEB_APPS_API_TOKEN`

### **2. Backend Deployment**
**Need to Add:**

Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions

**Secret Name:** `AZURE_CREDENTIALS`

**Secret Value:**
```json
{
  "clientId": "<YOUR_CLIENT_ID>",
  "clientSecret": "<YOUR_CLIENT_SECRET>",
  "subscriptionId": "f86506f8-7d33-48de-995d-f51e6f590cb1",
  "tenantId": "d6fd8270-b2a6-4492-9fd5-79def18a9452"
}
```

> **Note:** The actual `clientId` and `clientSecret` values were provided to you separately. Use those values when creating this secret.

---

## 🚀 CI/CD Workflows

### **Frontend Workflow**
**File:** `.github/workflows/azure-static-web-apps.yml`

**Triggers:**
- Push to `main` branch
- Pull requests to `main`

**What it does:**
1. Checks out code
2. Installs Node.js dependencies
3. Builds Next.js app
4. Deploys to Azure Static Web Apps
5. **Result:** Frontend automatically updates with HTTPS

### **Backend Workflow**
**File:** `.github/workflows/azure-backend-deploy.yml`

**Triggers:**
- Push to `main` branch (only when `src/backend/**` changes)
- Manual workflow dispatch

**What it does:**
1. Authenticates with Azure
2. Builds Docker image
3. Pushes to Azure Container Registry
4. Deploys to Azure Container Instances
5. Verifies health endpoint
6. **Result:** Backend API automatically updates

---

## 🏗️ Azure Resources

### **Resource Group: codex-rg**
Location: East US

| Resource | Type | Purpose | Status |
|----------|------|---------|--------|
| **codex-frontend** | Static Web App | Next.js Frontend | ✅ Running |
| **codex-backend** | Container Instance | FastAPI Backend | ✅ Running |
| **codexdominionacr** | Container Registry | Docker Images | ✅ Active |

### **Cost Breakdown**
- Static Web App (Free): **$0/month**
- Container Instances (1 vCPU, 1GB): **~$20/month**
- Container Registry (Basic): **~$5/month**
- **Total: ~$25/month**

---

## 🔧 Manual Deployment Commands

### **Frontend**
```powershell
# Build
cd frontend
npm run build

# Deploy
npx @azure/static-web-apps-cli deploy out \
  --deployment-token <TOKEN> \
  --app-name codex-frontend
```

### **Backend**
```powershell
# Build Docker image
docker build -t codexdominionacr.azurecr.io/codex-backend:latest \
  -f src/backend/Dockerfile src/backend/

# Login to ACR
az acr login --name codexdominionacr

# Push image
docker push codexdominionacr.azurecr.io/codex-backend:latest

# Redeploy container
.\update-container-env.ps1
```

---

## 🧪 Testing Endpoints

### **Frontend Health Check**
```powershell
Test-NetConnection -ComputerName happy-flower-0e39c5c0f-preview.eastus2.3.azurestaticapps.net -Port 443
# Expected: TcpTestSucceeded = True
```

### **Backend Health Check**
```powershell
curl http://codex-api.eastus.azurecontainer.io:8001/health

# Expected Response:
# {
#   "status": "healthy",
#   "service": "Codex Dominion API",
#   "version": "2.0.0"
# }
```

### **Full API Test**
```powershell
curl http://codex-api.eastus.azurecontainer.io:8001/
# Should return full API info with endpoints
```

---

## 📝 Environment Variables

### **Frontend**
Configured in `next.config.js`:
- `NEXT_PUBLIC_API_URL`: `http://codex-api.eastus.azurecontainer.io:8001` (production)
- `NEXT_PUBLIC_APP_NAME`: `Codex Dominion`
- `NEXT_PUBLIC_APP_VERSION`: `2.0.0`
- `NEXT_PUBLIC_EMPIRE_STATUS`: `Operational`
- `NEXT_PUBLIC_SOVEREIGNTY_LEVEL`: `Maximum`

### **Backend**
Configured in Container Instance:
- `PORT`: `8001`
- `ENVIRONMENT`: `production`
- `PYTHONUNBUFFERED`: `1`
- `ALLOWED_ORIGINS`: `https://happy-flower-0e39c5c0f.3.azurestaticapps.net`
- `CORS_ENABLED`: `true`

To update backend environment variables, edit `update-container-env.ps1` and run it.

---

## 🔐 Security Notes

### **Secrets to Protect**
1. `AZURE_STATIC_WEB_APPS_API_TOKEN` - Frontend deployment token
2. `AZURE_CREDENTIALS` - Azure service principal credentials
3. ACR password (managed automatically by workflows)

### **Network Security**
- Frontend: HTTPS with Azure-managed SSL certificate
- Backend: HTTP on port 8001 (internal API, accessed by frontend)
- CORS: Configured to allow frontend origin only

### **Access Control**
- Azure service principal has **contributor** role scoped to `codex-rg` resource group only
- Container Registry: Admin access enabled for deployment
- Static Web App: Public access with configurable authentication (if needed)

---

## 🔄 Rollback Procedures

### **Frontend Rollback**
Azure Static Web Apps keeps deployment history:
1. Go to Azure Portal → Static Web Apps → codex-frontend
2. Navigate to **Environments** → **Production**
3. Select previous deployment → Click **Promote to production**

### **Backend Rollback**
Redeploy previous Docker image:
```powershell
az container create \
  --resource-group codex-rg \
  --name codex-backend \
  --image codexdominionacr.azurecr.io/codex-backend:<PREVIOUS_SHA> \
  # ... (rest of container config)
```

Or use Git:
```powershell
git revert HEAD  # Revert last commit
git push origin main  # Triggers automatic redeployment
```

---

## 📊 Monitoring

### **View Logs**

**Frontend:**
```powershell
# Via Azure CLI
az staticwebapp show --name codex-frontend --resource-group codex-rg

# Or view in Azure Portal
```

**Backend:**
```powershell
# Container logs
az container logs --resource-group codex-rg --name codex-backend

# Follow logs (live tail)
az container attach --resource-group codex-rg --name codex-backend
```

### **GitHub Actions**
Monitor deployments at:
- https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions

---

## 🎯 Next Steps

### **Optional Enhancements**

1. **Custom Domain**
   - Add `codexdominion.com` to Static Web App
   - Configure DNS records
   - Automatic SSL for custom domain

2. **Database**
   ```powershell
   # Add Azure PostgreSQL Flexible Server
   az postgres flexible-server create \
     --name codex-db \
     --resource-group codex-rg \
     --location eastus \
     --admin-user codexadmin \
     --tier Burstable \
     --sku-name Standard_B1ms
   ```

3. **Redis Cache**
   ```powershell
   # Add Azure Cache for Redis
   az redis create \
     --name codex-redis \
     --resource-group codex-rg \
     --location eastus \
     --sku Basic \
     --vm-size c0
   ```

4. **Application Insights**
   ```powershell
   # Add monitoring
   az monitor app-insights component create \
     --app codex-insights \
     --location eastus \
     --resource-group codex-rg
   ```

5. **Upgrade to App Service** (when quota approved)
   - Submit quota increase request
   - Migrate from Container Instances to App Service
   - Get automatic HTTPS on backend

---

## ✅ Success Criteria Met

- [x] HTTPS working on frontend (port 443)
- [x] Free SSL certificate
- [x] Backend API operational
- [x] No firewall blocking issues
- [x] Automatic deployments via GitHub Actions
- [x] Full control over infrastructure
- [x] ~5 minute deployment time
- [x] Production-ready architecture

---

## 📞 Support Resources

- **Azure Documentation**: https://docs.microsoft.com/azure/
- **Azure Static Web Apps**: https://docs.microsoft.com/azure/static-web-apps/
- **Container Instances**: https://docs.microsoft.com/azure/container-instances/
- **Azure Container Registry**: https://docs.microsoft.com/azure/container-registry/
- **GitHub Actions**: https://docs.github.com/actions

---

**Last Updated**: December 8, 2025
**Deployment Status**: ✅ OPERATIONAL
**HTTPS Issue**: ✅ RESOLVED
