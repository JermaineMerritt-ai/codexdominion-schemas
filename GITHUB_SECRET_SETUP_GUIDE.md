# 🔐 GitHub Secret Setup Guide - Deploy to Azure Static Web App

## ⚡ Quick Start (5 minutes)

Your frontend is built and ready to deploy. This guide will help you upload the deployment token so GitHub Actions can automatically deploy your site.

---

## 📋 Prerequisites

✅ GitHub account with access to repository
✅ Azure Static Web App created (`yellow-tree-0ed102210`)
✅ Deployment token available (see below)

---

## 🚀 Step-by-Step Instructions

### Step 1: Copy Your Deployment Token

```
575a2ba3e81e8b6f44fa3f2aaeac114ac547ae3d0b92f8f9149daca43f62bd7103-54c5a44f-da85-4008-9b54-9f602f9f0f8c01013260ed102210
```

**⚠️ Important:** Keep this token secure! It grants deployment access to your Azure Static Web App.

---

### Step 2: Navigate to GitHub Secrets Page

Open your browser and go to:
```
https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions
```

**Alternative Navigation:**
1. Go to your repository: https://github.com/JermaineMerritt-ai/codexdominion-schemas
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)

---

### Step 3: Create New Repository Secret

1. Click the green **"New repository secret"** button (top right)

2. Fill in the form:
   - **Name:** 
     ```
     AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210
     ```
   - **Secret:** (Paste the token from Step 1)
     ```
     575a2ba3e81e8b6f44fa3f2aaeac114ac547ae3d0b92f8f9149daca43f62bd7103-54c5a44f-da85-4008-9b54-9f602f9f0f8c01013260ed102210
     ```

3. Click **"Add secret"** (green button at bottom)

✅ **Success!** You should see the secret listed with a green checkmark.

---

### Step 4: Trigger Deployment

Now that the secret is configured, trigger a deployment:

#### Option A: Push a Change (Recommended)
```powershell
# From your codex-dominion directory
cd c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion

# Create empty commit to trigger deployment
git commit --allow-empty -m "🚀 Deploy frontend to Azure Static Web App"

# Push to GitHub (triggers workflow)
git push origin main
```

#### Option B: Manual Workflow Trigger
1. Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
2. Click **"Azure Static Web Apps CI/CD"** workflow
3. Click **"Run workflow"** dropdown
4. Click green **"Run workflow"** button

---

### Step 5: Monitor Deployment (3-5 minutes)

1. **Watch Progress:**
   - Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
   - You'll see a workflow run named **"Deploy frontend to Azure Static Web App"**
   - Click on it to see real-time logs

2. **Deployment Stages:**
   - ✅ Checkout code
   - ✅ Setup Node.js
   - ✅ Install dependencies
   - ✅ Build Next.js (62 pages)
   - ✅ Deploy to Azure Static Web App
   - ✅ **Complete** (green checkmark)

3. **Typical Timeline:**
   - Build: 2-3 minutes
   - Deploy: 1-2 minutes
   - **Total: 3-5 minutes**

---

### Step 6: Verify Deployment

Once the workflow shows a green checkmark ✅:

#### Test Azure Static Web App URL:
```
https://yellow-tree-0ed102210.3.azurestaticapps.net
https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard
```

#### Expected Results:
- ✅ Homepage loads (no 404 error)
- ✅ Main dashboard visible (865-line dashboard)
- ✅ All 62 pages accessible
- ✅ API proxy working (`/api/*` → Flask backend)

---

## 🌐 OPTIONAL: Configure Custom Domain

After deployment is verified, point your domain to Azure:

### Update DNS Records

1. **Go to Google Domains:**
   - https://domains.google.com/registrar/codexdominion.app/dns

2. **Delete old A record:**
   - Remove: `74.208.123.158` (inactive IONOS server)

3. **Add CNAME records:**

| Name | Type  | TTL  | Data                                          |
|------|-------|------|-----------------------------------------------|
| @    | CNAME | 3600 | yellow-tree-0ed102210.3.azurestaticapps.net   |
| www  | CNAME | 3600 | yellow-tree-0ed102210.3.azurestaticapps.net   |

4. **Save changes**

### Wait for DNS Propagation (15-30 minutes)

Test DNS propagation:
```powershell
# Windows PowerShell
nslookup codexdominion.app

# Should resolve to Azure Static Web App IP
```

### Verify Custom Domain

After DNS propagates:
```
https://codexdominion.app
https://www.codexdominion.app
https://codexdominion.app/main-dashboard
```

---

## 🐛 Troubleshooting

### Issue: "Secret not found" error in workflow

**Solution:** Verify secret name matches exactly:
```
AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210
```
- Check for typos
- Ensure underscores (not hyphens)
- Name is CASE-SENSITIVE

---

### Issue: Workflow doesn't trigger

**Solution:** Check `.github/workflows/azure-static-web-apps-yellow-tree-0ed102210.yml` exists
```powershell
# Verify workflow file exists
ls .github/workflows/azure-static-web-apps-yellow-tree-0ed102210.yml

# If missing, it should be committed to repo
git add .github/workflows/azure-static-web-apps-yellow-tree-0ed102210.yml
git commit -m "Add Azure Static Web Apps workflow"
git push
```

---

### Issue: 404 error persists after deployment

**Possible Causes:**
1. ❌ Deployment failed (check workflow logs)
2. ❌ Wrong output directory configured
3. ❌ DNS not updated (still pointing to old server)

**Solution:**
```powershell
# Check workflow logs for errors
# Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions

# Verify build output directory in workflow:
# Should be: dashboard-app/out (Next.js static export)
```

---

### Issue: API calls fail (500 errors)

**Solution:** Ensure backend is running and accessible
```powershell
# Test backend health
curl http://20.242.178.102:8001/health

# If backend is down, restart it:
docker start codex-backend
# OR
az container start --name codex-backend --resource-group codex-rg
```

---

## ✅ Success Checklist

After completing all steps, verify:

- [ ] GitHub secret created with correct name
- [ ] Workflow triggered successfully
- [ ] Deployment completed (green checkmark)
- [ ] Azure Static Web App URL loads (no 404)
- [ ] Main dashboard visible and functional
- [ ] API calls working (`/api/*` routes)
- [ ] DNS updated (if using custom domain)
- [ ] HTTPS working (Azure auto-managed SSL)

---

## 📞 Support

If you encounter issues:

1. **Check workflow logs:** https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
2. **Verify Azure resources:** https://portal.azure.com → Resource Group `codex-rg`
3. **Test backend health:** http://20.242.178.102:8001/health

---

## 🎯 Next Steps After Deployment

Once frontend is live:

1. ✅ **Database Migration** - Run `migrate_json_to_postgresql.py`
2. ✅ **WordPress Setup** - Run `setup-wordpress-automation.ps1`
3. ✅ **Monitoring** - Configure Grafana dashboards
4. ✅ **SSL Certificate** - Azure auto-manages after DNS update

---

**🔥 Your Digital Sovereignty Awaits in the Cloud!** 👑

**Status:** Ready to Deploy
**Time Required:** 5 minutes
**Next Action:** Copy token → Create secret → Push commit → Go live!
