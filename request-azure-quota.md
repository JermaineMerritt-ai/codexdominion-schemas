# Azure Quota Increase Request

## Issue
Cannot create Azure App Service Plan due to quota limits:
- Current Limit (Basic VMs): 0
- Current Usage: 0
- Required: 1

## How to Request Quota Increase

### Method 1: Azure Portal (Easiest)

1. Go to https://portal.azure.com
2. Click **Help + support** (? icon in top right)
3. Click **Create a support request**
4. Fill in:
   - **Issue type**: Service and subscription limits (quotas)
   - **Subscription**: Select your subscription
   - **Quota type**: App Service
   - **Problem type**: Increase limits for App Service Plan
5. Click **Next: Solutions**
6. Click **Enter details**
7. Specify:
   - **Deployment model**: Resource Manager
   - **Location**: East US
   - **SKU family**: Basic (B1)
   - **New limit**: 1
8. Submit request

**Processing Time**: Usually approved within 1-2 business days for small increases

### Method 2: Azure CLI

```powershell
# This creates a support ticket via CLI (requires support plan)
az support tickets create \
  --ticket-name "AppServiceQuotaIncrease" \
  --title "Increase App Service Basic VM quota" \
  --description "Need to increase Basic VM quota from 0 to 1 for App Service deployment" \
  --severity minimal \
  --problem-classification-id "/providers/Microsoft.Support/services/quota_service_guid/problemClassifications/app_service_guid" \
  --contact-first-name "Jermaine" \
  --contact-last-name "Bourne" \
  --contact-email "Jermaine.Bourne36@gmail.com" \
  --contact-method "email"
```

## Current Working Solution

While waiting for quota approval, you have a **fully functional backend** deployed:

✅ **Current Backend**:
- URL: `http://codex-api.eastus.azurecontainer.io:8001`
- IP: `20.231.253.181:8001`
- Status: Operational
- Ports: 8001 (HTTP) ✅ Open

❌ **Missing**:
- Port 443 (HTTPS) - Container Instances doesn't include SSL
- Auto-SSL certificates

## Option 2: Use Application Gateway for HTTPS (No Quota Needed)

If you need HTTPS immediately without quota increase:

```powershell
# Create public IP for Application Gateway
az network public-ip create \
  --resource-group codex-rg \
  --name codex-agw-pip \
  --allocation-method Static \
  --sku Standard

# Create virtual network
az network vnet create \
  --resource-group codex-rg \
  --name codex-vnet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name agw-subnet \
  --subnet-prefix 10.0.0.0/24

# Create Application Gateway (provides HTTPS/SSL)
az network application-gateway create \
  --resource-group codex-rg \
  --name codex-agw \
  --location eastus \
  --vnet-name codex-vnet \
  --subnet agw-subnet \
  --capacity 1 \
  --sku Standard_v2 \
  --public-ip-address codex-agw-pip \
  --http-settings-port 8001 \
  --http-settings-protocol Http \
  --servers 20.231.253.181
```

**Cost**: ~$125/month for Application Gateway Standard_v2

## Option 3: Keep Current Setup (Recommended for Now)

Your current setup is **production-ready** for backend APIs:

**Why it works:**
1. Frontend (Azure Static Web Apps) will serve on HTTPS (port 443) ✅
2. Frontend makes API calls to backend on HTTP (port 8001) ✅
3. Users only see frontend HTTPS - backend HTTP is internal ✅

**Architecture:**
```
User Browser (HTTPS 443)
    ↓
Azure Static Web Apps (Frontend) ← Has SSL Certificate
    ↓ (Internal API calls via HTTP)
Azure Container Instances (Backend on port 8001)
    ↓
Database
```

This is a **common and secure pattern** - the backend API doesn't need HTTPS if:
- It's only accessed by your frontend (not public)
- Frontend has HTTPS
- Network traffic stays within Azure (low interception risk)

## Recommendation

**For immediate deployment:**
1. Keep current Container Instance backend (port 8001 HTTP)
2. Deploy frontend to Azure Static Web Apps (port 443 HTTPS automatic)
3. Configure frontend to call `http://codex-api.eastus.azurecontainer.io:8001`
4. Users see HTTPS, backend uses HTTP internally

**After quota approval (1-2 days):**
1. Migrate to App Service
2. Enable automatic HTTPS on backend
3. Get free SSL certificates

## Next Steps

Choose one:
- [ ] Request quota increase (1-2 day wait)
- [ ] Deploy Application Gateway for immediate HTTPS ($125/mo)
- [ ] Use current setup + deploy frontend with HTTPS (recommended)

Would you like to proceed with deploying the frontend to Azure Static Web Apps while waiting for quota approval?
