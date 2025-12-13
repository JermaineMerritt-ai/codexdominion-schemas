# IONOS DNS Update Guide - Switch to Azure Static Web App

## Current Situation
- **Domain:** www.codexdominion.app
- **Currently Points To:** 74.208.123.158 (IONOS VPS Server)
- **Need To Point To:** yellow-tree-0ed102210.3.azurestaticapps.net (Azure Static Web App)

## Step-by-Step Instructions

### Step 1: Log into IONOS
1. Go to https://www.ionos.com
2. Click **Login** (top right)
3. Enter your IONOS credentials

### Step 2: Navigate to DNS Settings
1. Click **Domains & SSL** in the left menu
2. Find **codexdominion.app** in your domain list
3. Click the **⚙️ (gear icon)** or **Manage** button next to it
4. Click **DNS** or **DNS Settings**

### Step 3: Delete the Old A Record
Look for this record in your DNS table:

```
Type: A
Hostname: www
Points to: 74.208.123.158
```

1. Find this record
2. Click the **🗑️ (trash/delete icon)** or **Delete** button
3. Confirm deletion

### Step 4: Add New CNAME Record
1. Click **Add Record** or **+ Add DNS Record**
2. Fill in the following:
   - **Type:** Select **CNAME** from dropdown
   - **Hostname:** `www` (just "www", not "www.codexdominion.app")
   - **Points to / Value:** `yellow-tree-0ed102210.3.azurestaticapps.net`
   - **TTL:** 3600 (or leave as default)
3. Click **Save** or **Add Record**

### Step 5: Save All Changes
1. Look for a **Save Changes** or **Activate Changes** button at the top/bottom
2. Click it to apply your DNS changes

### Step 6: Wait for DNS Propagation
DNS changes can take 5-30 minutes to propagate globally. Usually it's faster (5-10 minutes).

### Step 7: Verify DNS Change (After 10 minutes)
Open PowerShell and run:

```powershell
# Flush local DNS cache
ipconfig /flushdns

# Check DNS against Google's DNS servers
nslookup www.codexdominion.app 8.8.8.8
```

**Expected Result:**
```
Server:  dns.google
Address:  8.8.8.8

Non-authoritative answer:
Name:    yellow-tree-0ed102210.3.azurestaticapps.net
Address:  [some IP address]
Aliases:  www.codexdominion.app
```

### Step 8: Configure Custom Domain in Azure
Once DNS propagation is complete, run:

```powershell
az staticwebapp hostname set --name codex-frontend-centralus --resource-group codex-rg --hostname www.codexdominion.app
```

This should now succeed and Azure will automatically provision an SSL certificate.

---

## Troubleshooting

### "CNAME Record is invalid" Error
- This means the CNAME record hasn't propagated yet
- Wait 5-10 more minutes
- Verify with: `nslookup www.codexdominion.app 8.8.8.8`

### DNS Still Shows Old IP Address
- Changes not saved in IONOS
- IONOS may require clicking "Activate" or "Apply Changes"
- Some IONOS interfaces have a separate "Save" step

### Can't Find DNS Settings
- IONOS interface varies by region
- Try: Account → Domains → codexdominion.app → DNS
- Or: Home → Domain & SSL → Manage Domain → DNS Settings

---

## What This Changes

**Before:**
```
www.codexdominion.app → 74.208.123.158 (IONOS Docker containers)
```

**After:**
```
www.codexdominion.app → Azure Static Web App (with automatic HTTPS)
```

**Impact:**
- ✅ Azure Static Web App will serve your site
- ✅ Automatic HTTPS/SSL certificate from Azure
- ✅ Global CDN for faster performance
- ❌ Docker containers on IONOS server will no longer be accessible via www.codexdominion.app
- ℹ️ You can still access IONOS server directly at 74.208.123.158
