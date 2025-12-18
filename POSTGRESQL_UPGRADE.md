# 🔄 PostgreSQL Upgrade Guide

## Step 1: Create PostgreSQL Database in Render

1. Go to Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   ```
   Name: codex-portfolio-db
   Database: codex_portfolio
   User: codex_admin
   Region: Oregon (US West) - SAME as web service
   Plan: Free ($0 for 90 days) or Starter ($7/month)
   ```
4. Click **"Create Database"**
5. Wait for database to provision (30-60 seconds)

---

## Step 2: Get Database Connection String

1. In the PostgreSQL database page, find **"Internal Database URL"**
2. Copy the entire URL (starts with `postgresql://`)
3. It looks like:
   ```
   postgresql://codex_admin:PASSWORD@dpg-xxxxx-a.oregon-postgres.render.com/codex_portfolio
   ```

---

## Step 3: Update Web Service Environment Variable

1. Go to your web service: **codex-portfolio**
2. Click **"Environment"** tab
3. Find `DATABASE_URL` variable
4. Click **"Edit"**
5. Paste the PostgreSQL Internal Database URL
6. Click **"Save Changes"**

**Result:** Render automatically redeploys with PostgreSQL!

---

## Step 4: Initialize Database

After redeployment completes:

### Option A: Manual SSH (Render Shell)
```bash
# In Render Shell (Connect tab)
python init_db.py
```

### Option B: Add Initialization to Dockerfile
Already handled! The app will auto-create tables on first run.

---

## Step 5: Verify PostgreSQL Connection

Run test script locally:

```powershell
# Update APP_URL in test script first
.\test_render_deployment.ps1
```

Or manually test:
```powershell
$APP_URL = "https://your-app.onrender.com"
curl "$APP_URL/health"
```

---

## 🔄 Migration Checklist

- [ ] Create PostgreSQL database in Render
- [ ] Copy Internal Database URL
- [ ] Update DATABASE_URL environment variable
- [ ] Wait for auto-redeploy (2-3 minutes)
- [ ] Test health endpoint
- [ ] Verify data persists after restart

---

## 💡 Benefits of PostgreSQL

✅ **Persistent Data** - Survives container restarts
✅ **Concurrent Users** - Better performance under load
✅ **Automatic Backups** - Daily backups included
✅ **Connection Pooling** - Better resource management
✅ **Production Ready** - Industry standard

---

## 💰 Cost Comparison

| Option | Storage | Backups | Cost |
|--------|---------|---------|------|
| **SQLite** | Ephemeral | None | Free |
| **PostgreSQL (Free)** | 1 GB | Daily | $0 (90 days) |
| **PostgreSQL (Starter)** | 10 GB | Daily | $7/month |

---

## 🚨 Rollback to SQLite

If PostgreSQL has issues:

1. Go to web service → **Environment**
2. Change `DATABASE_URL` back to: `sqlite:///codex_dominion.db`
3. Save → Auto-redeploys with SQLite

---

## 🔥 Ready to Upgrade!

Once your SQLite deployment is tested and working, follow steps 1-5 above.

**Estimated Time:** 5-10 minutes
