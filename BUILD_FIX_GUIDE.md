# ⚠️ Build Failed - pnpm Lockfile Issue

## Problem

Render Static Site deployment failing with:
```
ERR_PNPM_OUTDATED_LOCKFILE  Cannot install with "frozen-lockfile"
because pnpm-lock.yaml is not up to date with package.json
```

## Root Cause

- Render auto-detected root-level `pnpm-lock.yaml` file
- Trying to use pnpm instead of npm
- Lockfile is out of sync with `apps/api/package.json` changes
- Your `web/` directory uses npm, not pnpm

## Quick Fix Options

### Option 1: Force npm (Recommended - Fastest)

Update Render build settings to explicitly use npm:

**Build Command (change to):**
```bash
npm install --legacy-peer-deps && npm run build
```

**Steps:**
1. Render Dashboard → Static Site → Settings
2. Find "Build Command"
3. Replace with: `npm install --legacy-peer-deps && npm run build`
4. Click "Save Changes"
5. Manual Deploy → "Clear build cache & deploy"

---

### Option 2: Delete Root pnpm-lock.yaml

Remove the pnpm lockfile so Render uses npm:

```bash
# In repository root
git rm pnpm-lock.yaml
git commit -m "Remove pnpm-lock.yaml to use npm for deployments"
git push origin main
```

Then redeploy on Render.

---

### Option 3: Add .npmrc to web/ directory

Force npm usage in web directory:

**Create `web/.npmrc`:**
```
package-lock=true
legacy-peer-deps=true
```

Then commit and push.

---

## Recommended Solution (Fastest)

**Update Build Command in Render Dashboard:**

Current:
```bash
npm install && npm run build
```

Change to:
```bash
cd web && npm ci --legacy-peer-deps && npm run build
```

**Why this works:**
- `npm ci` uses package-lock.json and ignores pnpm
- `--legacy-peer-deps` handles peer dependency conflicts
- Explicit `cd web` ensures correct directory

---

## Alternative: Update Build Settings

If you want to keep build command simple, configure these in Render:

**Environment Variables (Add):**
```
NPM_CONFIG_LEGACY_PEER_DEPS=true
NPM_USE_PRODUCTION=false
```

**Build Command:**
```
npm install && npm run build
```

This tells npm to handle peer deps gracefully.

---

## Testing Locally First

Before deploying, test the build locally:

```powershell
# Navigate to web directory
cd web

# Clean install
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item package-lock.json -ErrorAction SilentlyContinue

# Install with legacy peer deps
npm install --legacy-peer-deps

# Build
npm run build

# Verify out/ directory created
ls out
```

If this succeeds, the updated build command will work on Render.

---

## Render Configuration Summary

**Current Settings:**
- Name: codexdominion-schemas
- Branch: main
- Root Directory: web
- Build Command: ~~npm install && npm run build~~
- Publish Directory: out

**Updated Settings:**
- Name: codexdominion-schemas
- Branch: main
- Root Directory: web
- Build Command: **npm ci --legacy-peer-deps && npm run build**
- Publish Directory: out

**Environment Variables (add these):**
```
NEXT_PUBLIC_API_URL=https://codex-portfolio.onrender.com
NEXT_PUBLIC_SITE_URL=https://codexdominion-schemas.onrender.com
NEXT_PUBLIC_APP_NAME=Codex Dominion
NEXT_PUBLIC_APP_VERSION=2.0.0
NPM_CONFIG_LEGACY_PEER_DEPS=true
```

---

## Step-by-Step Fix (2 Minutes)

1. **Go to Render Dashboard**
   - https://dashboard.render.com
   - Click "codexdominion-schemas" static site

2. **Update Build Command**
   - Settings → Build & Deploy
   - Build Command: `npm ci --legacy-peer-deps && npm run build`
   - Click "Save Changes"

3. **Clear Cache & Deploy**
   - Manual Deploy → "Clear build cache & deploy"
   - Wait 2-5 minutes

4. **Verify Success**
   - Check logs for "Build successful"
   - Visit https://codexdominion-schemas.onrender.com

---

## Why This Happened

Your monorepo has:
- Root-level `pnpm-lock.yaml` (for monorepo workspace)
- `web/package-lock.json` (for Next.js app)
- `apps/api/package.json` (updated with new dependencies)

Render detected pnpm first and tried to use it, but the pnpm lockfile doesn't reflect recent changes to `apps/api/package.json`.

**Solution:** Explicitly tell Render to use npm for the `web/` subdirectory.

---

🔥 **Fix this in 2 minutes by updating the Build Command!** 👑
