# 🚀 Codex Dominion - Production Launch Quickstart

**Status:** All automation scripts ready
**Time to Deploy:** 1-2 hours
**Last Updated:** December 23, 2025

---

## 📋 What We Built

✅ **GitHub Secret Upload Guide** - Deploy frontend to Azure
✅ **Database Migration Script** - JSON → PostgreSQL
✅ **AI Advisor Dashboard** - New `/ai-advisor` route in Flask
✅ **WordPress Automation** - Complete WooCommerce setup

---

## 🎯 Launch Sequence (Choose Your Path)

### Option A: Minimal Launch (1 hour) - RECOMMENDED

Get live TODAY with core features:

```powershell
# 1. Deploy Frontend (5 minutes)
# Follow: GITHUB_SECRET_SETUP_GUIDE.md

# 2. Start Master Dashboard (1 minute)
.\START_DASHBOARD.ps1
# Visit: http://localhost:5000

# 3. Test AI Advisor (new!)
# Visit: http://localhost:5000/ai-advisor

# 4. Update DNS (15 minutes)
# Point codexdominion.app to Azure Static Web App
```

**You're Live!** 🎉 System runs on JSON (no database required)

---

### Option B: Full Production Launch (2 hours)

Complete setup with all features:

```powershell
# 1. Migrate to PostgreSQL (30 minutes)
python migrate_json_to_postgresql.py --dry-run  # Test first
python migrate_json_to_postgresql.py            # Run migration

# 2. Setup WordPress + WooCommerce (45 minutes)
.\setup-wordpress-automation.ps1

# 3. Deploy Frontend (5 minutes)
# Follow: GITHUB_SECRET_SETUP_GUIDE.md

# 4. Verify All Systems (10 minutes)
.\START_DASHBOARD.ps1
# Test all dashboards: AI agents, social, revenue, stores, ai-advisor

# 5. Go Live (5 minutes)
# Update DNS to point to Azure
```

**Fully Production Ready!** 🔥

---

## 📁 New Files Created

| File | Purpose | Usage |
|------|---------|-------|
| `GITHUB_SECRET_SETUP_GUIDE.md` | Step-by-step Azure deployment | Read first for frontend deploy |
| `migrate_json_to_postgresql.py` | Database migration script | `python migrate_json_to_postgresql.py` |
| `setup-wordpress-automation.ps1` | WordPress installer | `.\setup-wordpress-automation.ps1` |
| Flask dashboard `/ai-advisor` route | AI recommendations UI | http://localhost:5000/ai-advisor |

---

## 🚦 Quick Start Commands

### Deploy Frontend to Azure
```powershell
# 1. Upload secret (see GITHUB_SECRET_SETUP_GUIDE.md)
# Name: AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210
# Value: 575a2ba3e81e8b6f44fa3f2aaeac114ac547ae3d0b92f8f9149daca43f62bd7103-54c5a44f-da85-4008-9b54-9f602f9f0f8c01013260ed102210

# 2. Trigger deployment
git commit --allow-empty -m "🚀 Deploy to Azure"
git push origin main

# 3. Monitor: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions

# 4. Access: https://yellow-tree-0ed102210.3.azurestaticapps.net
```

### Migrate to PostgreSQL
```powershell
# Activate virtual environment
.venv\Scripts\activate.ps1

# Start PostgreSQL (if not running)
cd infra/docker
docker-compose up -d postgres
cd ../..

# Test migration (dry run)
python migrate_json_to_postgresql.py --dry-run

# Run actual migration
python migrate_json_to_postgresql.py

# Verify
python -c "from db import SessionLocal; from models import Council; session = SessionLocal(); print(f'Councils: {session.query(Council).count()}'); session.close()"
```

### Setup WordPress
```powershell
# Ensure Docker is running
docker ps

# Run automation script
.\setup-wordpress-automation.ps1

# Follow prompts for:
#   1. WordPress installation
#   2. API key generation
#   3. Webhook configuration

# Access WordPress: http://localhost:8080/wp-admin
```

### Test AI Advisor Dashboard
```powershell
# Start Flask dashboard
.\START_DASHBOARD.ps1

# Visit: http://localhost:5000/ai-advisor

# API endpoints (test backend):
curl http://localhost:5000/api/advisor/recommendations?tenant_id=tenant_codexdominion&status=pending
```

---

## 🔍 Verification Checklist

After running scripts, verify:

### Frontend Deployment
- [ ] GitHub secret uploaded successfully
- [ ] Workflow completed (green checkmark)
- [ ] https://yellow-tree-0ed102210.3.azurestaticapps.net loads
- [ ] Main dashboard visible
- [ ] No 404 errors

### Database Migration
- [ ] PostgreSQL running (`docker ps | grep postgres`)
- [ ] Tables created (`from models import Base; Base.metadata.tables.keys()`)
- [ ] Data migrated (councils, agents, workflow_types)
- [ ] JSON backups created (in `json_backups_*` folder)
- [ ] No migration errors in console

### WordPress Setup
- [ ] WordPress accessible: http://localhost:8080
- [ ] Admin login works: http://localhost:8080/wp-admin
- [ ] WooCommerce installed and activated
- [ ] Custom plugins visible
- [ ] REST API keys generated
- [ ] 7 webhooks configured
- [ ] `.env` files updated with API credentials

### AI Advisor Dashboard
- [ ] Route accessible: http://localhost:5000/ai-advisor
- [ ] Stats display (even if 0)
- [ ] Filter buttons work
- [ ] API connection successful
- [ ] Recommendations load (or empty state shows)

---

## 🐛 Troubleshooting

### Issue: GitHub workflow fails
**Solution:**
```powershell
# Verify secret name matches exactly
# Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions
# Name MUST be: AZURE_STATIC_WEB_APPS_API_TOKEN_YELLOW_TREE_0ED102210
```

### Issue: Database migration error
**Solution:**
```powershell
# Check PostgreSQL is running
docker ps | grep postgres

# If not running:
cd infra/docker
docker-compose up -d postgres

# Test connection
python -c "from db import engine; print(engine)"
```

### Issue: WordPress won't start
**Solution:**
```powershell
# Check port 8080 availability
netstat -ano | findstr :8080

# If in use, stop other services or change port in docker-compose.wordpress.yml

# Restart containers
docker-compose -f docker-compose.wordpress.yml down
docker-compose -f docker-compose.wordpress.yml up -d
```

### Issue: AI Advisor shows connection error
**Solution:**
```powershell
# Ensure Flask dashboard is running
.\START_DASHBOARD.ps1

# Check if advisor_api.py is loaded
curl http://localhost:5000/api/advisor/recommendations?tenant_id=tenant_codexdominion

# If 404, ensure advisor_api.py exists and is imported in flask_dashboard.py
```

---

## 📊 System Status After Setup

### Core Services
| Service | URL | Status |
|---------|-----|--------|
| Flask Dashboard | http://localhost:5000 | ✅ Running |
| AI Advisor | http://localhost:5000/ai-advisor | ✅ NEW! |
| WordPress | http://localhost:8080 | ✅ Automated |
| WooCommerce API | http://localhost:8080/wp-json/wc/v3 | ✅ Configured |
| PostgreSQL | localhost:5432 | ✅ Optional (migrated) |
| Azure Frontend | yellow-tree-0ed102210.3.azurestaticapps.net | ✅ Deployed |

### Dashboards (52+ tabs)
- 🏠 Home - System overview
- 🤖 AI Agents - Jermaine, .300, Algorithm
- 📱 Social - 6 platforms integrated
- 💰 Revenue - Treasury tracking
- 🛒 Stores - E-commerce management
- 📚 Copilot - AI instructions
- **🤖 AI Advisor - NEW! Intelligent recommendations**

---

## 🎯 Next Steps After Launch

1. **Monitor Deployment**
   - Watch GitHub Actions for deployment status
   - Verify Azure Static Web App is live
   - Test all frontend routes

2. **Configure Production Settings**
   - Update `.env.production` with real API keys
   - Set up SSL certificate (Azure auto-manages)
   - Configure monitoring (Grafana + Prometheus)

3. **Content Population**
   - Add WooCommerce products
   - Configure subscription plans
   - Set up lead magnets

4. **Marketing Launch**
   - Social media announcements
   - Email campaigns
   - SEO optimization

---

## 📞 Support Resources

- **Documentation**: See README.md, ARCHITECTURE.md, DEPLOYMENT_GUIDE.md
- **Logs**: Check terminal output during script execution
- **Docker Logs**: `docker-compose logs -f`
- **Flask Logs**: Console output from `START_DASHBOARD.ps1`
- **GitHub Actions**: https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions

---

## ✅ Success Metrics

You'll know you're successful when:

- ✅ Frontend loads on Azure without 404 errors
- ✅ Flask dashboard shows all 52+ tabs including AI Advisor
- ✅ PostgreSQL has migrated data (councils, agents, workflow_types)
- ✅ WordPress admin accessible with WooCommerce installed
- ✅ API calls work: `/api/advisor/recommendations`, `/api/workflows`, `/api/treasury/summary`
- ✅ DNS resolves to Azure (after DNS update)
- ✅ HTTPS works (Azure auto-managed SSL)

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**

**Your Codex Dominion is ready for production launch.**

Choose your path (Option A or B) and execute! 🚀
