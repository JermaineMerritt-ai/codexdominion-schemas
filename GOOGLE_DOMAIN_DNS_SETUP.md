# 🌐 Codex Dominion - Google Domains DNS Configuration

**Your Azure Static Web App:** `kind-sky-0a658cf0f.3.azurestaticapps.net`
**Your Domain:** `codexdominion.app`

---

## 🚀 Step 1: Configure Custom Domain in Azure (1 minute)

Run this command to add your Google Domain to Azure:

```powershell
az staticwebapp hostname set `
  --name codexdominion-frontend `
  --resource-group codex-dominion-rg `
  --hostname codexdominion.app
```

Azure will give you a TXT record for verification.

---

## 🔧 Step 2: Update Google Domains DNS (5 minutes)

Go to: https://domains.google.com/registrar/codexdominion.app/dns

### Add These DNS Records:

#### 1. CNAME Record (for www)
```
Type: CNAME
Name: www
Data: kind-sky-0a658cf0f.3.azurestaticapps.net
TTL: 1 hour
```

#### 2. CNAME Record (for root domain)
**Option A - Using CNAME flattening (if supported):**
```
Type: CNAME
Name: @
Data: kind-sky-0a658cf0f.3.azurestaticapps.net
TTL: 1 hour
```

**Option B - Using A records (if CNAME @ not supported):**
```
Type: A
Name: @
Data: [Azure will provide IP addresses after you run the hostname command above]
TTL: 1 hour
```

#### 3. Verification TXT Record (Azure will provide this)
```
Type: TXT
Name: @
Data: [Provided by Azure after running hostname command]
TTL: 1 hour
```

---

## 📊 Step 3: Test Your Dashboard

After DNS propagation (5-30 minutes):

- **Main Dashboard:** https://codexdominion.app/main-dashboard
- **Home Page:** https://codexdominion.app
- **Backend Health:** http://20.242.178.102:8001/health

---

## ⚡ FASTEST PATH - Deploy Frontend NOW

Your Azure Static Web App exists but needs content uploaded:

```powershell
# 1. Get deployment token
cd c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion
$token = az staticwebapp secrets list `
  --name codexdominion-frontend `
  --resource-group codex-dominion-rg `
  --query "properties.apiKey" -o tsv

# 2. Build frontend
cd frontend
npm install
npm run build

# 3. Install SWA CLI
npm install -g @azure/static-web-apps-cli

# 4. Deploy
swa deploy .next --deployment-token $token --env production

# 5. Test
Write-Host "🌐 Your dashboard: https://kind-sky-0a658cf0f.3.azurestaticapps.net/main-dashboard"
```

---

## 🎯 Current Status

✅ **Backend:** Running at 20.242.178.102:8001
✅ **Azure Static Web App:** Created (kind-sky-0a658cf0f.3.azurestaticapps.net)
⏳ **Frontend Build:** Ready to deploy
⏳ **Custom Domain:** Needs Google Domains DNS update

---

## 📞 Google Domains Direct Link

**Manage DNS:** https://domains.google.com/registrar/codexdominion.app/dns

---

**Total Time: 10-15 minutes to go live! 🚀**
