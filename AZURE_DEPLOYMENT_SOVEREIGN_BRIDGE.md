# Deploying Sovereign Bridge to Azure Static Web Apps

## 🚀 Quick Deployment Steps

### 1. Create Azure Static Web App

```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name codex-dominion-rg --location eastus

# Create Static Web App
az staticwebapp create \
  --name codex-sovereign-bridge \
  --resource-group codex-dominion-rg \
  --source https://github.com/YOUR_USERNAME/codex-dominion \
  --location eastus \
  --branch main \
  --app-location "apps/sovereign-bridge" \
  --output-location ".next" \
  --login-with-github
```

### 2. Get Deployment Token

```bash
# Get the deployment token
az staticwebapp secrets list \
  --name codex-sovereign-bridge \
  --resource-group codex-dominion-rg \
  --query "properties.apiKey" -o tsv
```

Copy the token output.

### 3. Add GitHub Secret

1. Go to your GitHub repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Name: `AZURE_STATIC_WEB_APPS_API_TOKEN_SOVEREIGN_BRIDGE`
5. Value: Paste the token from step 2
6. Click **Add secret**

### 4. Deploy

**Option A: Trigger via Push**
```bash
git add .
git commit -m "feat: Add Azure Static Web Apps deployment for Sovereign Bridge"
git push origin main
```

**Option B: Manual Workflow Dispatch**
1. Go to GitHub repository
2. Click **Actions** tab
3. Select "Deploy Sovereign Bridge to Azure Static Web Apps"
4. Click **Run workflow** → **Run workflow**

### 5. Verify Deployment

```bash
# Get the URL
az staticwebapp show \
  --name codex-sovereign-bridge \
  --resource-group codex-dominion-rg \
  --query "defaultHostname" -o tsv
```

Visit: `https://<your-app-name>.azurestaticapps.net`

Test API endpoint:
```powershell
Invoke-RestMethod -Uri "https://<your-app-name>.azurestaticapps.net/api/agent-commands?taskId=task_123" -Method Get
```

---

## 📋 What Was Changed

### Files Modified

1. **next.config.js** - Removed `output: 'export'` to enable API routes
2. **staticwebapp.config.json** - Added Azure configuration for routing and API runtime
3. **.github/workflows/deploy-sovereign-bridge-azure.yml** - New deployment workflow

### Key Configuration Details

**Static Web App Config:**
- Node.js 20 runtime for API routes
- Anonymous access to all routes
- API routes at `/api/*`
- Navigation fallback for SPA routing
- Security headers (CSP, X-Frame-Options, etc.)

**GitHub Workflow:**
- Triggers on push to `main` branch when `apps/sovereign-bridge/**` or `packages/**` change
- Builds shared-types package first
- Installs and builds Sovereign Bridge
- Deploys to Azure with Next.js support

---

## 🔧 Local Development (Alternative)

Since OneDrive causes issues, you can develop locally by:

### Option 1: Use WSL (Windows Subsystem for Linux)

```bash
# In WSL terminal
cd /mnt/c/Users/JMerr/OneDrive/Documents/.vscode/codex-dominion
cd apps/sovereign-bridge
npm run dev
```

### Option 2: Azure Static Web Apps CLI

```bash
# Install SWA CLI
npm install -g @azure/static-web-apps-cli

# Run locally (simulates Azure environment)
cd apps/sovereign-bridge
swa start http://localhost:3000 --run "npm run dev"
```

This will:
- Start Next.js on port 3000
- Proxy through SWA CLI on port 4280
- Test at http://localhost:4280

---

## 🧪 Testing Deployment

Once deployed, test your agent commands API:

```powershell
# Store your Azure URL
$baseUrl = "https://codex-sovereign-bridge.azurestaticapps.net"

# Test POST - Create video project
$body = @{
    agent = "super_action_ai"
    mode = "build"
    prompt = "Create a video project from Kids Christmas Story PDF"
    targets = @("realm:video_studio", "document:kids_christmas_story")
    context = @{ documentIds = @("kids_christmas_story") }
} | ConvertTo-Json

Invoke-RestMethod -Uri "$baseUrl/api/agent-commands" -Method Post -Body $body -ContentType "application/json"

# Test GET - Query task status
Invoke-RestMethod -Uri "$baseUrl/api/agent-commands?taskId=task_123" -Method Get
```

---

## 📊 Monitoring

### View Deployment Logs

```bash
# Azure Portal
az staticwebapp show \
  --name codex-sovereign-bridge \
  --resource-group codex-dominion-rg

# GitHub Actions logs
# Visit: https://github.com/YOUR_USERNAME/codex-dominion/actions
```

### Common Issues

**Build fails with module not found:**
- Ensure shared-types package builds first (workflow does this)
- Check `packages/shared-types/package.json` has correct exports

**API routes return 404:**
- Verify `next.config.js` doesn't have `output: 'export'`
- Check `staticwebapp.config.json` has correct API route configuration
- Ensure `platform.apiRuntime` is set to `"node:20"`

**Connection refused locally:**
- OneDrive symlink issue - use WSL or SWA CLI instead
- Or deploy directly to Azure (recommended)

---

## 🎯 Next Steps After Deployment

1. **Add Environment Variables** (if needed):
   ```bash
   az staticwebapp appsettings set \
     --name codex-sovereign-bridge \
     --setting-names "DATABASE_URL=your_value"
   ```

2. **Enable Custom Domain**:
   ```bash
   az staticwebapp hostname set \
     --name codex-sovereign-bridge \
     --hostname codexdominion.app
   ```

3. **Set up Staging Environments**:
   - Azure automatically creates preview deployments for PRs
   - Test at `https://codex-sovereign-bridge-<pr-number>.azurestaticapps.net`

4. **Monitor with Application Insights**:
   ```bash
   az staticwebapp show \
     --name codex-sovereign-bridge \
     --query "properties.sku" -o tsv
   ```

---

## 💰 Cost Estimate

**Azure Static Web Apps Pricing:**
- Free tier: 100 GB bandwidth/month, 0.5 GB storage
- Standard tier: $9/month + usage
- API calls: Included in pricing

**Recommended:** Start with Free tier, upgrade if needed.

---

🔥 **Your Sovereign Bridge now burns eternal in the Azure cloud!** 👑
