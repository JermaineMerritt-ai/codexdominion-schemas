# ⚠️ DNS CONFIGURATION REQUIRED

## Current Issue
**Error:** `DNS_PROBE_FINISHED_NXDOMAIN`
**Meaning:** The domain `api.CodexDominion.app` doesn't exist in DNS yet.

You **must configure DNS first** before the deployment will work!

---

## 🔧 Fix: Add DNS Records in IONOS

### Step-by-Step:

1. **Login to IONOS:**
   - Go to: https://my.ionos.com
   - Login with your credentials

2. **Navigate to DNS Settings:**
   - Click: **Domains**
   - Select: **CodexDominion.app**
   - Click: **DNS** or **DNS Settings**

3. **Add These 3 A Records:**

   | Type | Host/Subdomain | Points to IP | TTL |
   |------|----------------|--------------|-----|
   | A | @ (root) | 74.208.123.158 | 3600 |
   | A | www | 74.208.123.158 | 3600 |
   | A | api | 74.208.123.158 | 3600 |

   **What each record does:**
   - `@` → Makes `CodexDominion.app` work
   - `www` → Makes `www.CodexDominion.app` work
   - `api` → Makes `api.CodexDominion.app` work

4. **Save Changes**

5. **Wait for DNS Propagation:**
   - Usually takes: 5-30 minutes
   - Can take up to: 24 hours (rare)

---

## ✅ Verify DNS is Working

Open PowerShell and run:

```powershell
nslookup CodexDominion.app
nslookup www.CodexDominion.app
nslookup api.CodexDominion.app
```

**Expected output for each:**
```
Server:  ...
Address: ...

Non-authoritative answer:
Name:    CodexDominion.app
Address: 74.208.123.158
```

If you see `74.208.123.158` - DNS is working! ✅

---

## 🚫 What NOT to Do

**DON'T run the deployment script yet!**

The deployment script (`ionos-vps-deploy.sh`) will fail at the Let's Encrypt SSL certificate step if DNS isn't configured first.

Let's Encrypt needs to verify domain ownership by accessing:
- `http://CodexDominion.app/.well-known/acme-challenge/`

If DNS doesn't point to your server, verification fails.

---

## ⏰ Timeline

1. **Now:** Configure DNS in IONOS (5 minutes)
2. **Wait:** 5-30 minutes for propagation
3. **Verify:** Use `nslookup` to confirm
4. **Then:** Run deployment script

---

## 📋 Once DNS is Working

After DNS verification succeeds, run these commands:

```powershell
# Upload deployment script to VPS
scp ionos-vps-deploy.sh root@74.208.123.158:/root/

# SSH to VPS
ssh root@74.208.123.158

# Run deployment (on VPS)
chmod +x /root/ionos-vps-deploy.sh
/root/ionos-vps-deploy.sh
```

The script will automatically:
- Install Docker
- Obtain SSL certificates (requires working DNS!)
- Configure nginx
- Start all services

---

## 🆘 Need Help with IONOS DNS?

If you can't find the DNS settings:

1. IONOS Control Panel → **Domains & SSL**
2. Click your domain **CodexDominion.app**
3. Look for tabs: **DNS**, **DNS Settings**, or **Manage DNS**
4. Click **Add Record** or **New Record**
5. Select record type: **A**
6. Enter values from table above

---

## ✨ Current Status

- ❌ DNS not configured
- ✅ Deployment script ready
- ✅ Docker images built
- ✅ Local stack working (localhost:3001, localhost:8001)

**Next action:** Configure DNS, then wait for propagation, then deploy.

---

**🔥 Once DNS propagates, the empire goes live. The eternal flame awaits.**
