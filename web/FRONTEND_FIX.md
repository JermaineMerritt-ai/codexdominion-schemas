# Frontend Deployment Fix - Render Static Site

## 🔧 Current Issue
Frontend shows 404 at https://codexdominion-schemas.onrender.com

## ✅ Solution Steps

### Option A: Update Existing Service (Quick Fix)

1. **Go to Render Dashboard:**
   https://dashboard.render.com/static/srv-d51kpgf6s9ss73eokga0

2. **Update Settings → Build & Deploy:**
   - **Build Command:** `npm ci --legacy-peer-deps && npm run build`
   - **Publish Directory:** `out`
   - **Root Directory:** `web`

3. **Add Environment Variables** (if not already set):
   ```
   NEXT_PUBLIC_API_URL=https://codex-portfolio.onrender.com
   NEXT_PUBLIC_SITE_URL=https://codexdominion-schemas.onrender.com
   NEXT_PUBLIC_APP_NAME=Codex Dominion
   NEXT_PUBLIC_APP_VERSION=2.0.0
   ```

4. **Deploy:**
   - Click **"Manual Deploy"** button
   - Select **"Clear build cache & deploy"**
   - Wait 2-3 minutes

5. **Verify:**
   - Visit https://codexdominion-schemas.onrender.com
   - Should see homepage (not 404)

---

### Option B: Create New Static Site (Fresh Start)

1. **Go to:** https://dashboard.render.com
2. **Click:** "New +" → "Static Site"
3. **Connect Repository:** JermaineMerritt-ai/codexdominion-schemas
4. **Configure:**
   - **Name:** codexdominion-frontend
   - **Branch:** main
   - **Root Directory:** web
   - **Build Command:** `npm ci --legacy-peer-deps && npm run build`
   - **Publish Directory:** out

5. **Add Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://codexdominion-backend.onrender.com
   NEXT_PUBLIC_SITE_URL=https://codexdominion-frontend.onrender.com
   NEXT_PUBLIC_APP_NAME=Codex Dominion
   NEXT_PUBLIC_APP_VERSION=2.0.0
   ```

6. **Create Static Site**

---

## 🔍 Common Issues & Fixes

### Issue: Build Command Not Updated
**Symptom:** Build still fails with pnpm errors
**Fix:** Ensure build command is exactly: `npm ci --legacy-peer-deps && npm run build`

### Issue: Wrong Publish Directory
**Symptom:** 404 after successful build
**Fix:** Publish directory must be `out` (not `web`, not `.next`)

### Issue: PostCSS Error
**Symptom:** Build fails with "module is not defined"
**Fix:** Already fixed with `web/postcss.config.mjs` file

### Issue: Missing Environment Variables
**Symptom:** Frontend loads but API calls fail
**Fix:** Add all NEXT_PUBLIC_* variables in Render dashboard

---

## 📋 Verification Checklist

After deployment:
- [ ] Homepage loads at base URL
- [ ] No 404 errors
- [ ] CSS and images display correctly
- [ ] Navigation works between pages
- [ ] Console shows no critical errors (F12)
- [ ] API_URL environment variable is set correctly

---

## 🔄 After Backend Deploys

Once backend is live at `https://codexdominion-backend.onrender.com`:

1. Update frontend environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://codexdominion-backend.onrender.com
   ```

2. Redeploy frontend (manual deploy or git push)

3. Test API integration:
   - Login functionality
   - Portfolio data display
   - Stock picks page

---

## ⏱️ Expected Timeline

- **Configuration update:** 2 minutes
- **Build & deploy:** 2-3 minutes
- **Verification:** 1 minute
- **Total:** ~5-7 minutes

---

## 🎯 Success Criteria

✅ Frontend accessible without 404
✅ All pages load correctly
✅ Static assets serve properly
✅ Ready to connect to backend API

---

🔥 **The Flame Burns Sovereign and Eternal!** 👑
