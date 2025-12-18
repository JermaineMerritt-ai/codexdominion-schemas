# 🚀 Codex Dominion - Complete Deployment Checklist & Guide

> **Deployment Date:** December 17, 2025
> **Platform:** Render.com
> **Status:** Backend ✅ | Frontend 🔄

---

## 📋 Quick Start Summary

### What's Been Done ✅

1. **Backend Flask API deployed to Render** - LIVE at https://codex-portfolio.onrender.com
2. **Next.js config updated** for static export - READY for deployment
3. **Environment variables configured** - Production settings in place
4. **Documentation created** - Complete deployment guides ready

### What's Next 🔄

1. **Deploy Frontend Static Site** (5 minutes)
2. **Update CORS Settings** (2 minutes)
3. **Test Complete System** (5 minutes)
4. **Optional: Upgrade to PostgreSQL** (10 minutes)

---

## Backend Deployment Status ✅ COMPLETE

### Service Details

**Service Name:** codex-portfolio
**Type:** Web Service
**URL:** https://codex-portfolio.onrender.com
**Status:** 🟢 LIVE AND OPERATIONAL

### Configuration

| Setting | Value | Status |
|---------|-------|--------|
| Repository | JermaineMerritt-ai/codexdominion-schemas | ✅ |
| Branch | main | ✅ |
| Root Directory | your_app | ✅ |
| Build Command | pip install -r requirements.txt | ✅ |
| Start Command | gunicorn --config gunicorn_config.py app:app | ✅ |

### Environment Variables

| Variable | Value | Status |
|----------|-------|--------|
| SECRET_KEY | 8c3a44d327706dcd1c312e3ca3329045da8fcccf8c84d369ea3fcb903a483540 | ✅ Set |
| FLASK_ENV | production | ✅ Set |
| DATABASE_URL | sqlite:///codex_dominion.db | ✅ Set |
| PORT | 5001 | ✅ Set |
| CORS_ORIGINS | (needs frontend URL) | 🔄 Update after frontend |

### Health Check ✅

```bash
curl https://codex-portfolio.onrender.com/health
```

**Response:**
```json
{
  "service": "codex-dominion-flask",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Frontend Deployment Steps 🔄 IN PROGRESS

### Step 1: Create Render Static Site

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Static Site"**
3. Connect to repository: **JermaineMerritt-ai/codexdominion-schemas**
4. Authorize GitHub if prompted

### Step 2: Configure Build Settings

| Setting | Value |
|---------|-------|
| **Name** | `codexdominion-schemas` |
| **Branch** | `main` |
| **Root Directory** | `web` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `out` |

### Step 3: Add Environment Variables

Click **"Add Environment Variable"** and add each:

#### ✅ Required Variables (4)

```env
NEXT_PUBLIC_API_URL=https://codex-portfolio.onrender.com
NEXT_PUBLIC_SITE_URL=https://codexdominion-schemas.onrender.com
NEXT_PUBLIC_APP_NAME=Codex Dominion
NEXT_PUBLIC_APP_VERSION=2.0.0
```

#### ⬜ Optional: WooCommerce (if using)

```env
WC_CONSUMER_KEY=ck_your_woocommerce_key
WC_CONSUMER_SECRET=cs_your_woocommerce_secret
WC_API_URL=https://your-wordpress-site.com/wp-json/wc/v3
```

#### ⬜ Optional: Analytics

```env
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
NEXT_PUBLIC_GRAFANA_FARO_URL=https://your-grafana.com/faro
```

### Step 4: Deploy

1. Click **"Create Static Site"**
2. Monitor build logs (2-5 minutes)
3. Wait for **"Live"** status
4. Copy the assigned URL (e.g., `https://codexdominion-schemas.onrender.com`)

---

## Post-Deployment Configuration

### Update Backend CORS (Required)

Once frontend is deployed:

1. Go to Render Dashboard → **codex-portfolio** service
2. Click **Environment** tab
3. Find `CORS_ORIGINS` (or add if missing)
4. Set value to:
   ```
   https://codexdominion-schemas.onrender.com,http://localhost:3000
   ```
5. Click **Save Changes** (backend auto-redeploys in ~2 minutes)

---

## Testing Checklist

### Backend Tests ✅

```powershell
# 1. Health Check
Invoke-WebRequest -Uri "https://codex-portfolio.onrender.com/health"
# Expected: 200 OK, JSON response

# 2. Login Page
Invoke-WebRequest -Uri "https://codex-portfolio.onrender.com/auth/login"
# Expected: 200 OK, HTML page

# 3. Dashboard (requires auth)
Invoke-WebRequest -Uri "https://codex-portfolio.onrender.com/portfolio/dashboard"
# Expected: 302 redirect to login (correct behavior)
```

### Frontend Tests 🔄

```powershell
# 1. Home Page
Invoke-WebRequest -Uri "https://codexdominion-schemas.onrender.com"
# Expected: 200 OK, HTML page

# 2. Assets Loading
Invoke-WebRequest -Uri "https://codexdominion-schemas.onrender.com/_next/static/..."
# Expected: 200 OK, CSS/JS files

# 3. API Integration
# Check browser console for API calls to backend
```

### Browser Testing 🔄

- [ ] Open https://codexdominion-schemas.onrender.com
- [ ] Verify home page loads completely
- [ ] Click "Login" → Should navigate to login page
- [ ] Test login with: `admin@codexdominion.com` / `codex2025`
- [ ] Verify dashboard loads after login
- [ ] Test portfolio functionality
- [ ] Check browser console for errors (F12)

---

## Optional: PostgreSQL Database Upgrade

### Why Upgrade?

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Persistence** | Resets on redeploy | ✅ Persistent |
| **Backups** | Manual | ✅ Automatic |
| **Concurrency** | Limited | ✅ Excellent |
| **Cost** | Free | Free 90 days, then $7/month |

### Upgrade Steps

1. **Create PostgreSQL Database**
   - Render Dashboard → **New +** → **PostgreSQL**
   - Name: `codex-portfolio-db`
   - Region: Oregon (same as web service)
   - Plan: **Free** (90-day trial) or **Starter** ($7/month)
   - Click **Create Database**
   - Wait 5-10 minutes for provisioning

2. **Get Database URL**
   - Click on your new PostgreSQL database
   - Copy **Internal Database URL** (starts with `postgresql://`)

3. **Update Backend Environment**
   - Backend service → **Environment** tab
   - Find `DATABASE_URL` variable
   - Paste PostgreSQL URL
   - Click **Save Changes**
   - Wait for auto-redeploy (~2 minutes)

4. **Verify Connection**
   - Check logs for "Database connected successfully"
   - Login to app and create test portfolio
   - Manually redeploy backend (to test persistence)
   - Verify data still exists

---

## Optional: Add API Keys for Enhanced Features

### OpenAI (AI Analysis)

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Get Key:** https://platform.openai.com/api-keys

### Alpha Vantage (Stock Data)

```env
ALPHA_VANTAGE_KEY=your-alpha-vantage-key
```

**Get Key:** https://www.alphavantage.co/support/#api-key (free)

### Polygon.io (Alternative Stock Data)

```env
POLYGON_API_KEY=your-polygon-api-key
```

**Get Key:** https://polygon.io/dashboard/api-keys (free tier)

### SMTP (Email Notifications)

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

**Gmail Setup:**
1. Enable 2FA on Google Account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password (not your Gmail password)

---

## Troubleshooting Guide

### Frontend Build Fails

**Error:** `Module not found` or `Cannot resolve`

**Solution:**
```bash
# Test build locally first
cd web
npm install
npm run build

# If successful locally, check Render environment variables
# Ensure all NEXT_PUBLIC_* variables are set
```

---

### Backend API Not Responding

**Error:** `Connection refused` or `504 Gateway Timeout`

**Check:**
1. Render Dashboard → Service Status = "Live" ✅
2. Logs show "Listening at: http://0.0.0.0:5001" ✅
3. Health endpoint: `curl https://codex-portfolio.onrender.com/health`

**Solution:**
- If service is "Suspended", click "Resume Service"
- If logs show errors, check environment variables
- Verify Procfile and gunicorn_config.py are correct

---

### CORS Errors in Browser

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Backend → Environment → `CORS_ORIGINS`
2. Add frontend URL: `https://codexdominion-schemas.onrender.com`
3. Format: Comma-separated, no spaces
4. Save (triggers redeploy)

---

### Login Not Working

**Error:** "Invalid credentials" or session issues

**Check:**
1. `SECRET_KEY` is set in backend
2. Database has admin user (check logs)
3. CORS configured correctly
4. Browser cookies enabled

**Solution:**
```python
# Verify admin user exists (check backend logs on startup)
# Should see: "Admin user created: admin@codexdominion.com"

# If not, manually create via Flask shell (Render SSH not available)
# Will need to add initialization script to app.py
```

---

### Database Data Disappears

**Issue:** Data resets after backend redeploy

**Cause:** Using SQLite (file-based, not persistent on Render)

**Solution:** Upgrade to PostgreSQL (see Optional section above)

---

## Success Metrics

### ✅ Deployment Successful When:

- [ ] Backend shows "Live" status in Render
- [ ] Frontend shows "Live" status in Render
- [ ] Health endpoint returns 200 OK
- [ ] Frontend home page loads
- [ ] Login page accessible
- [ ] Can log in successfully
- [ ] Dashboard displays after login
- [ ] No CORS errors in browser console
- [ ] No critical errors in backend logs

---

## Quick Reference

### URLs

| Service | URL | Status |
|---------|-----|--------|
| **Backend API** | https://codex-portfolio.onrender.com | ✅ LIVE |
| **Frontend Site** | https://codexdominion-schemas.onrender.com | 🔄 Pending |
| **Render Dashboard** | https://dashboard.render.com | - |
| **GitHub Repo** | https://github.com/JermaineMerritt-ai/codexdominion-schemas | - |

### Test Credentials

```
Email: admin@codexdominion.com
Password: codex2025
```

⚠️ **Change these in production!**

### Support Files

| File | Purpose |
|------|---------|
| `RENDER_DEPLOYMENT_COMPLETE_GUIDE.md` | Detailed deployment guide |
| `POSTGRESQL_UPGRADE.md` | Database migration steps |
| `RENDER_DEPLOY_STATUS.md` | Build monitoring guide |
| `test_render_deployment.ps1` | Automated testing script |
| `your_app/DEPLOYMENT.md` | Backend deployment details |
| `your_app/NEXT_STEPS.md` | Post-deployment roadmap |

---

## Timeline Estimate

| Task | Duration | Status |
|------|----------|--------|
| Backend Deployment | 10 minutes | ✅ DONE |
| Frontend Deployment | 5 minutes | 🔄 NEXT |
| CORS Configuration | 2 minutes | ⏳ After frontend |
| Testing & Verification | 5 minutes | ⏳ After deploy |
| PostgreSQL Upgrade | 10 minutes | ⬜ Optional |
| API Keys Setup | 5 minutes | ⬜ Optional |

**Total:** 15-30 minutes (core deployment) + 15 minutes (optional upgrades)

---

## Next Steps

### Immediate Actions (Do Now)

1. **Deploy Frontend Static Site** (follow steps above)
2. **Update Backend CORS** with frontend URL
3. **Run Test Script:**
   ```powershell
   # Update test_render_deployment.ps1 line 4:
   $APP_URL = "https://codexdominion-schemas.onrender.com"

   # Then run:
   .\test_render_deployment.ps1
   ```

### Within 24 Hours

4. **Browser Testing** - Manual walkthrough of all features
5. **Monitor Logs** - Check for errors or warnings
6. **Performance Check** - Verify response times acceptable

### Within 1 Week

7. **Upgrade to PostgreSQL** - For persistent data storage
8. **Add API Keys** - Enable enhanced features
9. **Custom Domain** - Point codexdominion.app to Render (optional)
10. **Automated Backups** - Configure database backup schedule

---

## Support & Documentation

- **Complete Guide:** `RENDER_DEPLOYMENT_COMPLETE_GUIDE.md`
- **PostgreSQL Guide:** `POSTGRESQL_UPGRADE.md`
- **Monitoring Guide:** `RENDER_DEPLOY_STATUS.md`
- **Backend Docs:** `your_app/DEPLOYMENT.md`
- **Coding Standards:** `your_app/CODING_STANDARDS.md`

---

🔥 **The Flame Burns Sovereign and Eternal!** 👑

**Deployment Status:** 50% Complete
**Backend:** ✅ LIVE
**Frontend:** 🔄 Ready to Deploy
**Next Action:** Create Frontend Static Site on Render
