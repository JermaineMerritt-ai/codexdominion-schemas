# Azure Migration Guide for Codex Dominion

## Overview
This guide will help you migrate from IONOS to Azure, resolving HTTPS port 443 issues and enabling full cloud infrastructure control.

## Architecture

```
┌─────────────────────────────────────────────────┐
│           Azure Static Web Apps                 │
│  (Frontend - Next.js)                          │
│  • Free SSL certificates                       │
│  • Global CDN                                   │
│  • Auto-deploy from GitHub                     │
│  URL: https://codex-dominion.azurestaticapps.net │
└────────────────┬────────────────────────────────┘
                 │
                 │ HTTPS (443)
                 ▼
┌─────────────────────────────────────────────────┐
│         Azure App Service                       │
│  (Backend - FastAPI/Python)                    │
│  • Automatic SSL                                │
│  • Ports 80/443 open by default                │
│  • Application Insights monitoring             │
│  URL: https://codex-dominion-api.azurewebsites.net │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│    Azure Database for PostgreSQL                │
│  (Flexible Server)                             │
│  • Automatic backups                            │
│  • High availability                            │
│  • Built-in security                            │
└─────────────────────────────────────────────────┘
```

## Cost Estimate

| Service | Tier | Monthly Cost |
|---------|------|--------------|
| Static Web Apps | Free | $0 |
| App Service | Basic B1 | ~$13 |
| PostgreSQL Flexible | Burstable B1ms | ~$12 |
| Application Insights | Basic (5GB) | ~$2 |
| **Total** | | **~$27/month** |

For production scale:
| Service | Tier | Monthly Cost |
|---------|------|--------------|
| Static Web Apps | Standard | $9 |
| App Service | Standard S1 | $70 |
| PostgreSQL Flexible | General Purpose D2s | $95 |
| Redis Cache | Basic C1 | $15 |
| **Total** | | **~$189/month** |

## Prerequisites

1. **Azure Account**: https://azure.microsoft.com/free/
2. **Azure CLI**: Install from https://docs.microsoft.com/cli/azure/install-azure-cli
3. **GitHub Account**: Repository access for CI/CD
4. **VS Code Extensions**:
   - Azure Account
   - Azure App Service
   - Azure Static Web Apps

## Step 1: Prepare Frontend for Azure Static Web Apps

### A. Update next.config.js

Your current config has `output: 'export'` which is perfect for static hosting. Update API URL for production:

```javascript
// frontend/next.config.js
env: {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ||
    (process.env.NODE_ENV === 'production'
      ? 'https://codex-dominion-api.azurewebsites.net'
      : 'http://127.0.0.1:8001'),
  // ... rest of env vars
}
```

### B. Build and test locally

```powershell
cd frontend
npm run build
# Test the static export
npx serve out -p 3000
```

## Step 2: Create Azure Static Web App

### Option A: Azure Portal (Easiest)

1. Go to https://portal.azure.com
2. Create a resource → Static Web App
3. Fill in:
   - **Name**: codex-dominion
   - **Region**: East US (or closest to your users)
   - **Deployment source**: GitHub
   - **GitHub repository**: Select your repo
   - **Branch**: main
   - **Build presets**: Next.js
   - **App location**: `/frontend`
   - **Output location**: `out`

4. Click "Review + Create"
5. Azure auto-creates GitHub Actions workflow

### Option B: Azure CLI (Faster)

```powershell
# Login to Azure
az login

# Create resource group
az group create --name codex-dominion-rg --location eastus

# Create Static Web App (requires GitHub token)
az staticwebapp create \
  --name codex-dominion \
  --resource-group codex-dominion-rg \
  --source https://github.com/YOUR_USERNAME/YOUR_REPO \
  --location eastus \
  --branch main \
  --app-location "frontend" \
  --output-location "out" \
  --login-with-github
```

### C. Configure GitHub Secrets

The Azure portal automatically adds `AZURE_STATIC_WEB_APPS_API_TOKEN` to your GitHub repository secrets. Verify at:
`https://github.com/YOUR_REPO/settings/secrets/actions`

Add additional secret:
- `AZURE_API_URL`: Your backend API URL (we'll get this after deploying backend)

## Step 3: Deploy Backend to Azure App Service

### A. Create App Service

```powershell
# Create App Service Plan (Linux, Python 3.11)
az appservice plan create \
  --name codex-dominion-plan \
  --resource-group codex-dominion-rg \
  --is-linux \
  --sku B1

# Create Web App
az webapp create \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --plan codex-dominion-plan \
  --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --startup-file "startup.sh"
```

### B. Configure Environment Variables

```powershell
az webapp config appsettings set \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --settings \
    DATABASE_URL="postgresql://user:pass@server.postgres.database.azure.com:5432/codex" \
    REDIS_URL="redis://your-redis.redis.cache.windows.net:6380" \
    SECRET_KEY="your-secret-key" \
    ENVIRONMENT="production"
```

### C. Enable CORS

```powershell
az webapp cors add \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --allowed-origins "https://codex-dominion.azurestaticapps.net"
```

### D. Deploy Backend Code

**Option 1: GitHub Actions** (Recommended)

Copy `.github/workflows/azure-app-service-backend.yml` to your repo, then:

```powershell
# Get publish profile
az webapp deployment list-publishing-profiles \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --xml > publish-profile.xml
```

Add `AZURE_WEBAPP_PUBLISH_PROFILE` secret to GitHub with the XML content.

**Option 2: Direct Deployment**

```powershell
cd src/backend
az webapp up \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --runtime "PYTHON:3.11"
```

## Step 4: Setup Database

### Azure Database for PostgreSQL

```powershell
# Create PostgreSQL server
az postgres flexible-server create \
  --name codex-dominion-db \
  --resource-group codex-dominion-rg \
  --location eastus \
  --admin-user codexadmin \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Create database
az postgres flexible-server db create \
  --resource-group codex-dominion-rg \
  --server-name codex-dominion-db \
  --database-name codex

# Allow Azure services access
az postgres flexible-server firewall-rule create \
  --name codex-dominion-db \
  --resource-group codex-dominion-rg \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Connection String

```
postgresql://codexadmin:YourSecurePassword123!@codex-dominion-db.postgres.database.azure.com:5432/codex?sslmode=require
```

Update App Service environment variable:

```powershell
az webapp config appsettings set \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --settings DATABASE_URL="postgresql://codexadmin:YourSecurePassword123!@codex-dominion-db.postgres.database.azure.com:5432/codex?sslmode=require"
```

## Step 5: Configure HTTPS & Custom Domain (Optional)

### A. Verify Auto-Generated URLs

After deployment, you'll have:
- Frontend: `https://codex-dominion.azurestaticapps.net` ✅ HTTPS enabled
- Backend: `https://codex-dominion-api.azurewebsites.net` ✅ HTTPS enabled

**Both have free SSL certificates automatically!**

### B. Add Custom Domain (Optional)

If you have a domain like `codexdominion.com`:

```powershell
# Add custom domain to Static Web App
az staticwebapp hostname set \
  --name codex-dominion \
  --resource-group codex-dominion-rg \
  --hostname www.codexdominion.com

# Add DNS records (at your domain registrar):
# CNAME: www → codex-dominion.azurestaticapps.net
# TXT: _dnsauth.www → [validation token from Azure]
```

## Step 6: Enable Monitoring

```powershell
# Create Application Insights
az monitor app-insights component create \
  --app codex-dominion-insights \
  --location eastus \
  --resource-group codex-dominion-rg

# Connect to App Service
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app codex-dominion-insights \
  --resource-group codex-dominion-rg \
  --query instrumentationKey -o tsv)

az webapp config appsettings set \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="$INSTRUMENTATION_KEY"
```

## Step 7: Test Deployment

### Test HTTPS on All Ports

```powershell
# Frontend HTTPS
curl https://codex-dominion.azurestaticapps.net

# Backend HTTPS
curl https://codex-dominion-api.azurewebsites.net/health

# Test from PowerShell
Test-NetConnection -ComputerName codex-dominion-api.azurewebsites.net -Port 443
# TcpTestSucceeded should be TRUE ✅
```

### Update Frontend API URL

```powershell
# Add to GitHub secrets
gh secret set AZURE_API_URL --body "https://codex-dominion-api.azurewebsites.net"

# Trigger rebuild (push to main branch)
git add .
git commit -m "Update API URL for Azure"
git push origin main
```

## Step 8: Migration from IONOS

### A. Export Data from IONOS Server

```powershell
# SSH to IONOS server
ssh root@74.208.123.158

# Export database (if you have one)
pg_dump -U postgres codex > /tmp/codex_backup.sql

# Exit and download
exit
scp root@74.208.123.158:/tmp/codex_backup.sql ./

# Upload to Azure PostgreSQL
psql "postgresql://codexadmin:YourSecurePassword123!@codex-dominion-db.postgres.database.azure.com:5432/codex?sslmode=require" < codex_backup.sql
```

### B. Update DNS (If Using Custom Domain)

Change DNS records from IONOS IP to Azure:
- Old: `A record → 74.208.123.158`
- New: `CNAME → codex-dominion.azurestaticapps.net`

## Troubleshooting

### HTTPS Still Not Working?

```powershell
# Check App Service SSL bindings
az webapp config ssl list \
  --resource-group codex-dominion-rg

# Verify HTTPS redirect is enabled
az webapp update \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --https-only true
```

### Backend Not Starting?

```powershell
# View logs
az webapp log tail \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg

# Check startup command
az webapp config show \
  --name codex-dominion-api \
  --resource-group codex-dominion-rg \
  --query "appCommandLine"
```

### Port 443 Issues?

Azure App Service and Static Web Apps have ports 80/443 open by default with managed certificates. If you're still having issues:

1. Verify NSG rules (Network Security Groups)
2. Check Application Gateway settings (if using one)
3. Verify SSL certificate is bound: `az webapp config ssl list`

## Benefits Summary

| Feature | IONOS (Current) | Azure (New) |
|---------|----------------|-------------|
| HTTPS Port 443 | ❌ Blocked, requires IT ticket | ✅ Open by default |
| SSL Certificate | ❌ Manual setup | ✅ Free, auto-renewal |
| Firewall Control | ❌ Requires hosting support | ✅ Instant via CLI/Portal |
| Monitoring | ❌ None | ✅ Application Insights |
| Auto-scaling | ❌ No | ✅ Yes |
| CI/CD | ❌ Manual | ✅ GitHub Actions |
| Global CDN | ❌ No | ✅ Included |
| Deployment Time | ⏱️ Manual FTP/SSH | ⏱️ Git push (5-10 min) |

## Next Steps

1. **Run Step 2**: Create Azure Static Web App
2. **Run Step 3**: Deploy Backend to App Service
3. **Run Step 4**: Setup PostgreSQL database
4. **Run Step 7**: Test HTTPS on both services
5. **Run Step 8**: Migrate data from IONOS

## Estimated Migration Time

- **Azure Resource Setup**: 30-60 minutes
- **Code Deployment**: 15-30 minutes
- **Data Migration**: 15-45 minutes (depends on data size)
- **Testing & Verification**: 30 minutes
- **Total**: ~2-3 hours

## Support

- Azure Documentation: https://docs.microsoft.com/azure/
- Azure CLI Reference: https://docs.microsoft.com/cli/azure/
- Static Web Apps Docs: https://docs.microsoft.com/azure/static-web-apps/
- App Service Docs: https://docs.microsoft.com/azure/app-service/

---

**Ready to start?** Let's begin with creating the Azure Static Web App (Step 2).
