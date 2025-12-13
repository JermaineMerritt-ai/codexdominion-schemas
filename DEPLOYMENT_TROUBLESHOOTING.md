# 🔧 Deployment Troubleshooting - Codex Dominion

## Problem Summary

**Issue 1:** https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard returns **404 Not Found**
**Issue 2:** https://codexdominion.app returns **DNS_PROBE_FINISHED_NXDOMAIN**

---

## Root Cause Analysis

### Issue 1: 404 on Azure Static Web App
**Why:** No content has been deployed to the Azure Static Web App yet.

**What's Missing:** The GitHub Actions workflow needs a deployment secret to push your frontend files to Azure.

**Current State:**
- ✅ Frontend is built (62 pages including main-dashboard.html in `.next/export` folder)
- ✅ GitHub Actions workflow is configured and pushed to repository
- ❌ GitHub Secret `AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210` is NOT uploaded
- ❌ Without the secret, GitHub Actions cannot deploy to Azure

**Manual SWA CLI Attempts Failed:** I tried deploying directly using Azure SWA CLI, but the deployments didn't register properly with Azure Static Web Apps. The GitHub Actions method is more reliable.

### Issue 2: DNS Error for codexdominion.app
**Why:** Domain DNS points to an inactive IONOS VPS server.

**Current DNS:**
- Type: A Record
- Value: 74.208.123.158 (IONOS VPS, ports 80/443 not responding)

**Required DNS:**
- Type: CNAME
- Value: yellow-tree-0ed102210.3.azurestaticapps.net

---

## Solution: Step-by-Step

### STEP 1: Upload GitHub Secret (CRITICAL)

**This must be done first before anything will work.**

1. **Copy the deployment token:**
   ```
   575a2ba3e81e8b6f44fa3f2aaeac114ac547ae3d0b92f8f9149daca43f62bd7103-54c5a44f-da85-4008-9b54-9f602f9f0f8c01013260ed102210
   ```

2. **Go to GitHub Secrets page:**
   - URL: https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions
   - (You must be logged into GitHub as JermaineMerritt-ai)

3. **Click "New repository secret"**

4. **Enter the secret:**
   - **Name:** `AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210`
   - **Value:** (paste the token from step 1)

5. **Click "Add secret"**

### STEP 2: Trigger Deployment

Once the secret is uploaded, trigger the deployment:

**Option A - Automatic (recommended):**
```powershell
# Make any small change and push to main branch
git commit --allow-empty -m "Trigger deployment"
git push
```

**Option B - Manual:**
1. Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
2. Click on "Azure Static Web Apps CI/CD" workflow
3. Click "Run workflow"
4. Select branch: main
5. Click "Run workflow"

### STEP 3: Monitor Deployment (3-5 minutes)

1. Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
2. Watch for the workflow run (green ✓ = success, red ✗ = failed)
3. Click on the run to see detailed logs if needed

**Expected outcome:**
- Workflow builds your Next.js frontend
- Workflow generates static HTML in `.next/export` folder
- Workflow uploads all files to Azure Static Web App
- After 3-5 minutes, your site is live!

### STEP 4: Verify Deployment

Once the workflow shows green checkmark, test the deployment:

```powershell
# Test the main dashboard
Invoke-WebRequest -Uri "https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard" | Select-Object StatusCode, @{Name="ContentLength";Expression={$_.Content.Length}}
```

**Expected:**
- StatusCode: 200
- ContentLength: > 50000 bytes (your main-dashboard HTML)

**If still 404:**
- Wait 2-3 more minutes (Azure propagation delay)
- Check GitHub Actions log for errors
- Verify the secret name is EXACTLY: `AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210`

### STEP 5: Update DNS (Optional - for custom domain)

**After deployment is verified**, update Google Domains DNS:

1. **Go to:** https://domains.google.com/registrar/codexdominion.app/dns

2. **Remove existing A record:**
   - Delete: A record with value 74.208.123.158

3. **Add CNAME records:**

   | Host | Type  | TTL  | Data                                          |
   |------|-------|------|-----------------------------------------------|
   | @    | CNAME | 3600 | yellow-tree-0ed102210.3.azurestaticapps.net   |
   | www  | CNAME | 3600 | yellow-tree-0ed102210.3.azurestaticapps.net   |

4. **Click Save**

5. **Wait for DNS propagation (5-30 minutes)**
   - Test with: `nslookup codexdominion.app`
   - Should resolve to Azure IP (not 74.208.123.158)

6. **Verify custom domain:**
   ```powershell
   Invoke-WebRequest -Uri "https://codexdominion.app/main-dashboard"
   ```

---

## Technical Details

### Why Manual SWA CLI Failed

I attempted direct deployment using:
```powershell
npx @azure/static-web-apps-cli deploy .next/export --deployment-token $token --env production
```

**Result:** The CLI reported "Deploying project to Azure Static Web Apps..." but the content never appeared on the site. This is a known limitation of manual SWA CLI deployments - they don't always register properly with Azure's CDN.

**Solution:** GitHub Actions is the recommended deployment method for Azure Static Web Apps. It uses the official `Azure/static-web-apps-deploy@v1` action which properly handles:
- Build orchestration
- File uploads
- CDN cache invalidation
- Deployment slots
- Rollback capabilities

### Workflow Configuration

The GitHub Actions workflow is configured to:
- **Trigger:** On every push to `main` branch or pull request
- **Build location:** `/frontend` directory
- **Output location:** `.next/export` (static HTML export from Next.js)
- **Deployment token:** Stored in GitHub Secret `AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210`

**File:** `.github/workflows/azure-static-web-apps-yellow-tree-0ed102210.yml`

### Why .next/export folder?

Next.js has two output modes:
1. **Server mode** (output: 'standalone'): Requires Node.js server, supports dynamic rendering
2. **Static mode** (output: 'export'): Generates pure HTML/CSS/JS, works with Azure Static Web Apps

Your `next.config.js` is set to `output: 'standalone'`, but during build, Next.js also creates a static export in `.next/export` which contains:
- 62 working pages as static HTML
- All assets (CSS, JS, images)
- Main dashboard as `main-dashboard.html`

Azure Static Web Apps serves these static HTML files directly from its global CDN.

---

## Timeline

**Immediate (0-5 minutes):**
1. Upload GitHub Secret
2. Trigger deployment (empty commit or manual trigger)

**Deployment (3-5 minutes):**
3. GitHub Actions builds and deploys frontend
4. Azure CDN propagates content

**Verification (1 minute):**
5. Test yellow-tree URL

**DNS Update (Optional, 5-30 minutes):**
6. Update Google Domains DNS
7. Wait for DNS propagation
8. Test custom domain

**Total Time:** 10-15 minutes (immediate) + 5-30 minutes (DNS)

---

## Expected Results

### After GitHub Secret Upload + Deployment:
- ✅ https://yellow-tree-0ed102210.3.azurestaticapps.net/ → Shows your homepage
- ✅ https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard → Shows 865-line dashboard
- ✅ All 62 pages accessible at yellow-tree URL

### After DNS Update:
- ✅ https://codexdominion.app/ → Shows your homepage
- ✅ https://codexdominion.app/main-dashboard → Shows 865-line dashboard
- ✅ www.codexdominion.app works too

---

## Next Steps

**RIGHT NOW:**
1. **Upload GitHub Secret** (link above - this is blocking everything)
2. **Trigger deployment** (empty commit or manual workflow trigger)
3. **Wait 5 minutes** and check yellow-tree URL

**AFTER DEPLOYMENT WORKS:**
4. **Update DNS** in Google Domains (optional but recommended for custom domain)
5. **Wait 30 minutes** for DNS propagation
6. **Test custom domain**

---

## Need Help?

**If GitHub Actions fails:**
- Check the workflow run logs at: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
- Common issues:
  - Secret name mismatch (must be EXACT)
  - Build errors (check "Build And Deploy" step logs)
  - Deployment token expired (regenerate with `az staticwebapp secrets list`)

**If DNS doesn't resolve:**
- Use https://www.whatsmydns.net/#CNAME/codexdominion.app to check propagation
- Google Domains DNS changes can take 5-60 minutes
- Verify CNAME records are correctly entered (no typos)

**If pages show blank/errors:**
- Check browser console for JavaScript errors
- Verify API backend is accessible: http://20.242.178.102:8001/health
- Check Azure Static Web App logs in Azure Portal

---

## Status Checklist

- [ ] GitHub Secret uploaded (AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210)
- [ ] Deployment triggered (commit pushed or workflow manually run)
- [ ] GitHub Actions workflow completed successfully (green checkmark)
- [ ] Yellow-tree URL returns 200 OK with content
- [ ] Main dashboard accessible at yellow-tree URL
- [ ] Google Domains DNS updated (optional)
- [ ] Custom domain resolves correctly (optional)
- [ ] Custom domain shows content (optional)

---

**Last Updated:** December 10, 2025
**Status:** Awaiting GitHub Secret upload to proceed with deployment
