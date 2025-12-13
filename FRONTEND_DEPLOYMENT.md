# Deploy Frontend to Azure Static Web App

## Static Web App Details
- **Name**: codexdominion-frontend
- **Default URL**: https://happy-hill-0f1fded0f.3.azurestaticapps.net
- **Resource Group**: codex-dominion
- **Deployment Token**: `5c31dcc01f66d750703-f0b50c9a-958f-4a37-93ea-7889a853674300f20130f1fded0f`

## Deployment Options

### Option 1: GitHub Actions (Recommended)
1. Push code to GitHub repository
2. Add deployment token as secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`
3. GitHub Actions workflow will automatically deploy on push
4. Workflow file created at: `.github/workflows/deploy-frontend.yml`

### Option 2: Azure Static Web Apps CLI
```bash
# Install SWA CLI
npm install -g @azure/static-web-apps-cli

# Deploy from static-deploy folder
cd static-deploy
swa deploy --deployment-token 5c31dcc01f66d750703-f0b50c9a-958f-4a37-93ea-7889a853674300f20130f1fded0f
```

### Option 3: VS Code Extension
1. Install "Azure Static Web Apps" extension
2. Right-click on static-deploy folder
3. Select "Deploy to Static Web App"
4. Choose codexdominion-frontend

### Option 4: Azure Portal
1. Go to https://portal.azure.com
2. Navigate to codexdominion-frontend Static Web App
3. Click "Manage deployment token"
4. Use the token with SWA CLI or GitHub Actions

## DNS Configuration

### Update DNS Records:
```bash
# Add/Update CNAME for www (currently points to A record)
az network dns record-set a delete --resource-group codex-dominion --zone-name codexdominion.app --name www --yes
az network dns record-set cname create --resource-group codex-dominion --zone-name codexdominion.app --name www
az network dns record-set cname set-record --resource-group codex-dominion --zone-name codexdominion.app --record-set-name www --cname happy-hill-0f1fded0f.3.azurestaticapps.net

# Configure custom domain in Static Web App
az staticwebapp hostname set --name codexdominion-frontend --resource-group codex-dominion --hostname www.codexdominion.app
```

## Current Status
✅ Static Web App created
✅ Deployment token generated
✅ GitHub Actions workflow configured
✅ Static placeholder site created in `static-deploy/`
⏳ Waiting for deployment (use one of the options above)

## Test URLs
- **Default**: https://happy-hill-0f1fded0f.3.azurestaticapps.net
- **Custom Domain** (after DNS): https://www.codexdominion.app
- **Backend API**: http://codex-api-eastus.eastus.azurecontainer.io:8000

## Next Steps
1. Fix Next.js frontend build errors (useState hooks issues)
2. Deploy using GitHub Actions or SWA CLI
3. Configure custom domain SSL
4. Test end-to-end application flow
