# 🚀 Codex Dominion - Complete Render Deployment Guide

> **Last Updated:** December 17, 2025
> **Status:** Production Ready ✅

## 📋 Table of Contents

1. [Overview](#overview)
2. [Backend Deployment (Flask)](#backend-deployment-flask)
3. [Frontend Deployment (Next.js)](#frontend-deployment-nextjs)
4. [Post-Deployment Verification](#post-deployment-verification)
5. [Environment Variables Reference](#environment-variables-reference)
6. [Troubleshooting](#troubleshooting)

---

## Overview

**Codex Dominion** consists of two main applications:

- **Backend (Flask):** Portfolio management API with authentication
- **Frontend (Next.js):** Static site with e-commerce integration

**Deployment Strategy:**
1. ✅ Deploy Backend Flask App (Web Service) - **COMPLETED**
2. 🔄 Deploy Frontend Next.js (Static Site) - **IN PROGRESS**
3. ✅ Connect services via environment variables
4. ✅ Verify all endpoints working

---

## Backend Deployment (Flask)

### ✅ Status: DEPLOYED & OPERATIONAL

**Service Type:** Web Service
**Repository:** JermaineMerritt-ai/codexdominion-schemas
**Branch:** main
**Root Directory:** `your_app`

**URL:** https://codex-portfolio.onrender.com

### Configuration

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn --config gunicorn_config.py app:app
```

### Environment Variables (Backend)

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | `8c3a44d327706dcd1c312e3ca3329045da8fcccf8c84d369ea3fcb903a483540` | ✅ Set |
| `FLASK_ENV` | `production` | ✅ Set |
| `DATABASE_URL` | `sqlite:///codex_dominion.db` | ✅ Set (SQLite) |
| `PORT` | `5001` | ✅ Set |
| `CORS_ORIGINS` | `https://codexdominion-schemas.onrender.com` | 🔄 Update after frontend deploy |

### Health Check

```bash
curl https://codex-portfolio.onrender.com/health
```

**Expected Response:**
```json
{
  "service": "codex-dominion-flask",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Frontend Deployment (Next.js)

### 🔄 Status: READY TO DEPLOY

**Service Type:** Static Site
**Repository:** JermaineMerritt-ai/codexdominion-schemas
**Branch:** main
**Root Directory:** `web`

### Step-by-Step Deployment

#### 1. Create New Static Site on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Static Site"**
3. Connect GitHub repository: `JermaineMerritt-ai/codexdominion-schemas`

#### 2. Configure Build Settings

| Setting | Value |
|---------|-------|
| **Name** | `codexdominion-schemas` |
| **Branch** | `main` |
| **Root Directory** | `web` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `out` |

#### 3. Add Environment Variables

Click **"Add Environment Variable"** for each:

##### Required Variables

```env
# Backend API Connection
NEXT_PUBLIC_API_URL=https://codex-portfolio.onrender.com

# Site Configuration
NEXT_PUBLIC_SITE_URL=https://codexdominion-schemas.onrender.com
NEXT_PUBLIC_APP_NAME=Codex Dominion
NEXT_PUBLIC_APP_VERSION=2.0.0
```

##### Optional Variables (WooCommerce)

```env
WC_CONSUMER_KEY=ck_your_woocommerce_key_here
WC_CONSUMER_SECRET=cs_your_woocommerce_secret_here
WC_API_URL=https://your-wordpress-site.com/wp-json/wc/v3
```

##### Optional Variables (Analytics)

```env
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
NEXT_PUBLIC_GRAFANA_FARO_URL=https://your-grafana-instance.com/faro
```

#### 4. Deploy

1. Click **"Create Static Site"**
2. Wait for build to complete (2-5 minutes)
3. Note the assigned URL (e.g., `https://codexdominion-schemas.onrender.com`)

---

## Post-Deployment Verification

### 1. Update Backend CORS Settings

Once frontend is deployed, update backend CORS:

**Render Dashboard → Backend Service → Environment → Edit `CORS_ORIGINS`:**

```
https://codexdominion-schemas.onrender.com,http://localhost:3000
```

**Save Changes** (backend will auto-redeploy)

### 2. Test Frontend Endpoints

```powershell
# Home Page
Invoke-WebRequest -Uri "https://codexdominion-schemas.onrender.com"

# Health Check (should proxy to backend)
Invoke-WebRequest -Uri "https://codexdominion-schemas.onrender.com/api/health"
```

### 3. Test Backend Endpoints

```powershell
# Health Check
Invoke-WebRequest -Uri "https://codex-portfolio.onrender.com/health"

# Login Page
Invoke-WebRequest -Uri "https://codex-portfolio.onrender.com/auth/login"

# Dashboard (should require authentication)
Invoke-WebRequest -Uri "https://codex-portfolio.onrender.com/portfolio/dashboard"
```

### 4. Browser Testing Checklist

- [ ] Frontend home page loads
- [ ] Backend API responds to health check
- [ ] Login page displays correctly
- [ ] Can log in with credentials: `admin@codexdominion.com` / `codex2025`
- [ ] Dashboard loads after login
- [ ] Portfolio data displays
- [ ] Stock analysis works
- [ ] Newsletter subscription functions

---

## Environment Variables Reference

### Backend Flask App (Web Service)

| Variable | Type | Required | Default | Notes |
|----------|------|----------|---------|-------|
| `SECRET_KEY` | String | ✅ Yes | - | Flask session encryption |
| `FLASK_ENV` | String | ✅ Yes | `production` | Environment mode |
| `DATABASE_URL` | String | ✅ Yes | `sqlite:///codex_dominion.db` | Database connection |
| `PORT` | Integer | ✅ Yes | `5001` | Server port |
| `CORS_ORIGINS` | String | ⚠️ Recommended | `*` | Comma-separated URLs |
| `OPENAI_API_KEY` | String | ⬜ Optional | - | AI analysis features |
| `ALPHA_VANTAGE_KEY` | String | ⬜ Optional | - | Stock data API |
| `POLYGON_API_KEY` | String | ⬜ Optional | - | Alternative stock API |
| `SMTP_HOST` | String | ⬜ Optional | - | Email notifications |
| `SMTP_PORT` | Integer | ⬜ Optional | `587` | Email port |
| `SMTP_USER` | String | ⬜ Optional | - | Email username |
| `SMTP_PASS` | String | ⬜ Optional | - | Email password |

### Frontend Next.js (Static Site)

| Variable | Type | Required | Default | Notes |
|----------|------|----------|---------|-------|
| `NEXT_PUBLIC_API_URL` | String | ✅ Yes | - | Backend API base URL |
| `NEXT_PUBLIC_SITE_URL` | String | ✅ Yes | - | Frontend site URL |
| `NEXT_PUBLIC_APP_NAME` | String | ⚠️ Recommended | `Codex Dominion` | Site title |
| `NEXT_PUBLIC_APP_VERSION` | String | ⚠️ Recommended | `2.0.0` | Version number |
| `WC_CONSUMER_KEY` | String | ⬜ Optional | - | WooCommerce integration |
| `WC_CONSUMER_SECRET` | String | ⬜ Optional | - | WooCommerce secret |
| `WC_API_URL` | String | ⬜ Optional | - | WordPress API endpoint |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | String | ⬜ Optional | - | Google Analytics |

---

## Troubleshooting

### Frontend Build Failures

**Error:** `Module not found: Can't resolve 'xyz'`

**Solution:**
```bash
# Locally test the build
cd web
npm install
npm run build

# Check for missing dependencies
npm audit fix
```

**Error:** `Image optimization requires unoptimized: true`

**Solution:** ✅ Already configured in `web/next.config.js`

---

### Backend Connection Issues

**Error:** Frontend can't reach backend API

**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` points to correct backend URL
2. Update backend `CORS_ORIGINS` to include frontend URL
3. Check backend health: `curl https://codex-portfolio.onrender.com/health`

---

### CORS Errors in Browser Console

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Backend → Environment Variables → `CORS_ORIGINS`
2. Add frontend URL: `https://codexdominion-schemas.onrender.com`
3. Save (auto-redeploys)

---

### Database Not Persisting Data

**Issue:** Data resets on backend redeploy

**Solution:** Upgrade to PostgreSQL

**Steps:**
1. Render Dashboard → New → PostgreSQL
2. Name: `codex-portfolio-db`
3. Plan: Free (90 days) or Starter ($7/month)
4. Wait for provisioning (5-10 minutes)
5. Copy **Internal Database URL**
6. Backend → Environment → `DATABASE_URL` → Paste URL
7. Save (auto-redeploys)

---

### Login Not Working

**Error:** Invalid credentials or session issues

**Solution:**
1. Check `SECRET_KEY` is set in backend
2. Verify default admin user exists:
   ```python
   # In Flask shell or init script
   admin = User(email='admin@codexdominion.com', username='admin')
   admin.set_password('codex2025')
   db.session.add(admin)
   db.session.commit()
   ```
3. Clear browser cookies
4. Test login again

---

## Next Steps After Deployment

### 1. ✅ Immediate (0-10 minutes)

- [ ] Frontend deployed and accessible
- [ ] Backend CORS updated with frontend URL
- [ ] Test login functionality
- [ ] Verify portfolio dashboard loads
- [ ] Update `test_render_deployment.ps1` with actual URLs

### 2. ⚠️ Recommended (10-30 minutes)

- [ ] Upgrade to PostgreSQL database
- [ ] Add custom domain (e.g., `codexdominion.app`)
- [ ] Configure SSL certificate (auto via Render)
- [ ] Set up monitoring alerts in Render

### 3. ⬜ Optional (30+ minutes)

- [ ] Add OpenAI API key for AI analysis
- [ ] Configure Alpha Vantage for real-time stock data
- [ ] Set up SMTP for email notifications
- [ ] Enable Google Analytics tracking
- [ ] Configure WooCommerce integration
- [ ] Set up automated backups

---

## Deployment Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| **Backend Flask Deployment** | 5-10 minutes | ✅ COMPLETE |
| **Frontend Next.js Deployment** | 5-10 minutes | 🔄 IN PROGRESS |
| **CORS Configuration** | 2 minutes | ⏳ PENDING |
| **Testing & Verification** | 5 minutes | ⏳ PENDING |
| **PostgreSQL Upgrade** | 10 minutes | 📋 OPTIONAL |

**Total Estimated Time:** 15-30 minutes for complete deployment

---

## Support & Resources

- **Backend URL:** https://codex-portfolio.onrender.com
- **Frontend URL:** (pending deployment)
- **Render Dashboard:** https://dashboard.render.com
- **GitHub Repository:** https://github.com/JermaineMerritt-ai/codexdominion-schemas

**Test Script:** Run `.\test_render_deployment.ps1` after updating URLs

**Documentation:**
- `DEPLOYMENT.md` - Backend deployment details
- `POSTGRESQL_UPGRADE.md` - Database migration guide
- `RENDER_DEPLOY_STATUS.md` - Build monitoring guide

---

🔥 **The Flame Burns Sovereign and Eternal!** 👑
