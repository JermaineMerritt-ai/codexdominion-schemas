# 🚀 GitHub Actions Auto-Deployment Setup

## ✅ COMPLETED

1. **GitHub Actions Workflow Created**
   - File: `.github/workflows/azure-static-web-apps.yml`
   - Target: yellow-tree-0ed102210.3.azurestaticapps.net
   - Trigger: Automatic on push to main branch

## 📋 NEXT STEP: Add GitHub Secret

### Get Your Deployment Token:

Run this command:
```powershell
az staticwebapp secrets list --name codex-frontend-centralus --resource-group codex-rg --query "properties.apiKey" -o tsv
```

### Add to GitHub:

1. **Go to Repository Secrets:**
   https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions

2. **Click:** "New repository secret"

3. **Name:** `AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE`

4. **Value:** Paste the token from the command above

5. **Click:** "Add secret"

## 🔄 Deploy Your Dashboard

Once the secret is added:

```bash
git add .github/workflows/azure-static-web-apps.yml
git commit -m "Setup auto-deployment to yellow-tree"
git push
```

GitHub Actions will automatically:
- Build your Next.js frontend
- Deploy to yellow-tree-0ed102210.3.azurestaticapps.net
- Take 3-5 minutes to complete

## 🌐 Update Google Domains DNS

While deployment runs, update your DNS:

**Go to:** https://domains.google.com/registrar/codexdominion.app/dns

**Add CNAME Records:**

```
Type: CNAME
Name: @
Value: yellow-tree-0ed102210.3.azurestaticapps.net
TTL: 1 hour
```

```
Type: CNAME
Name: www
Value: yellow-tree-0ed102210.3.azurestaticapps.net
TTL: 1 hour
```

**Remove:** A record pointing to 74.208.123.158

## 📊 Your URLs

After deployment completes:

- **Temporary:** https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard
- **Custom Domain (after DNS):** https://codexdominion.app/main-dashboard
- **Backend:** http://20.242.178.102:8001

## ✅ System Status

- ✅ Backend: Running with Stripe configured
- ✅ Frontend Code: 69 pages ready
- ✅ Azure Static Web App: Created (yellow-tree)
- ✅ GitHub Actions Workflow: Configured
- ⏳ GitHub Secret: Needs manual upload
- ⏳ DNS: Needs Google Domains update

---

**Total Time to Live:** 10-15 minutes after adding the secret! 🚀
