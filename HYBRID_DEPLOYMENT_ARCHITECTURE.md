# 🔥 Codex Dominion - Hybrid Deployment Architecture

**Frontend:** IONOS VPS (CodexDominion.app)
**Backend:** Azure App Service
**Architecture:** Decoupled, Cloud-Native

---

## 🏗️ **Deployment Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    IONOS Domain (DNS)                        │
│  codexdominion.app → IONOS VPS (Frontend)                   │
│  api.codexdominion.app → Azure App Service (Backend)        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│   IONOS VPS      │                  │  Azure Cloud     │
│  (Frontend)      │                  │  (Backend)       │
├──────────────────┤                  ├──────────────────┤
│ • Next.js 14     │◄────HTTPS────────┤ • FastAPI        │
│ • Nginx          │                  │ • Redis Cache    │
│ • SSL (Let's     │                  │ • SQLite DB      │
│   Encrypt)       │                  │ • Managed SSL    │
│ • Static Assets  │                  │ • Auto-scale     │
└──────────────────┘                  └──────────────────┘
 74.208.123.158                        Azure Region
```

---

## 📋 **Deployment Steps**

### **Step 1: Deploy Backend to Azure** ✅

Run the automated Azure deployment:

```powershell
.\deploy-azure-backend.ps1
```

This creates:
- Azure App Service with your backend container
- Azure Cache for Redis
- Secure environment variables
- HTTPS endpoint

**Result:** Backend live at `https://codex-dominion-backend.azurewebsites.net`

---

### **Step 2: Configure DNS for API Subdomain**

Add CNAME record in IONOS DNS panel:

```
Type:     CNAME
Host:     api
Points to: codex-dominion-backend.azurewebsites.net
TTL:      3600
```

**Or configure custom domain in Azure:**
```powershell
az webapp config hostname add \
  --webapp-name codex-dominion-backend \
  --resource-group codex-dominion-rg \
  --hostname api.codexdominion.app
```

---

### **Step 3: Update Frontend Configuration**

Update the IONOS deployment to point to Azure backend:

```bash
# Modify ionos-vps-deploy.sh to use Azure backend
AZURE_BACKEND_URL="https://codex-dominion-backend.azurewebsites.net"
# or if using custom domain:
AZURE_BACKEND_URL="https://api.codexdominion.app"
```

---

### **Step 4: Deploy Frontend to IONOS**

Modified deployment for frontend-only:

```powershell
# Upload the modified script
scp ionos-frontend-only-deploy.sh root@74.208.123.158:/root/

# SSH and deploy
ssh root@74.208.123.158
chmod +x /root/ionos-frontend-only-deploy.sh
/root/ionos-frontend-only-deploy.sh
```

---

## 📝 **Modified IONOS Deployment Script**

I'll create a frontend-only version that:
- ✅ Deploys only Next.js frontend
- ✅ Configures nginx to proxy to Azure backend
- ✅ Sets up SSL with Let's Encrypt
- ❌ Skips backend container deployment
- ❌ Skips Redis deployment

---

## 🔄 **Traffic Flow**

1. **User visits:** `https://codexdominion.app`
   - DNS → IONOS VPS (74.208.123.158)
   - Nginx serves Next.js frontend
   - SSL via Let's Encrypt

2. **Frontend makes API call:** `https://api.codexdominion.app/health`
   - DNS → Azure App Service (via CNAME)
   - Azure serves FastAPI backend
   - SSL via Azure managed certificates

3. **Backend accesses Redis:**
   - Azure App Service → Azure Cache for Redis
   - Internal Azure network (fast, secure)

---

## 💰 **Cost Breakdown**

| Component | Service | Monthly Cost |
|-----------|---------|--------------|
| Frontend | IONOS VPS | $10-20 |
| Backend | Azure App Service (B1) | $13 |
| Cache | Azure Redis (Basic C0) | $17 |
| SSL | Let's Encrypt (IONOS) | Free |
| SSL | Azure Managed | Free |
| **Total** | | **~$40-50/month** |

---

## ✅ **Benefits of This Architecture**

1. **Separation of Concerns**
   - Frontend: Static hosting optimized for speed
   - Backend: Scalable compute in Azure cloud

2. **Cost Optimization**
   - IONOS VPS: Fixed cost for frontend
   - Azure: Pay for backend resources only

3. **Scalability**
   - Frontend: Static, fast, CDN-ready
   - Backend: Auto-scale with Azure

4. **Reliability**
   - Frontend and backend can scale independently
   - Backend failures don't affect frontend serving
   - Azure provides 99.95% SLA

5. **Security**
   - Backend secrets managed in Azure
   - CORS properly configured
   - SSL on both endpoints

---

## 🚀 **Quick Deployment Commands**

```powershell
# 1. Deploy backend to Azure
.\deploy-azure-backend.ps1

# Wait for Azure deployment (5-10 min)

# 2. Get backend URL
# Copy from script output: https://codex-dominion-backend.azurewebsites.net

# 3. Generate frontend-only IONOS script
.\generate-ionos-frontend-deployment.ps1

# 4. Deploy frontend to IONOS
scp ionos-frontend-only-deploy.sh root@74.208.123.158:/root/
ssh root@74.208.123.158
chmod +x /root/ionos-frontend-only-deploy.sh
/root/ionos-frontend-only-deploy.sh
```

---

## 🔐 **Environment Variables**

**IONOS Frontend (.env):**
```bash
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.codexdominion.app
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
```

**Azure Backend (App Service settings):**
```bash
ENVIRONMENT=production
DATABASE_URL=sqlite:///./data/codex_dominion.db
REDIS_URL=redis://:<password>@codexredis.redis.cache.windows.net:6380/0?ssl=True
SECRET_KEY=<64-char-secret>
JWT_SECRET=<64-char-secret>
API_KEY=<64-char-secret>
CORS_ORIGINS=https://codexdominion.app,https://www.codexdominion.app
```

---

## 🔥 **The empire spans two realms. Frontend sovereign on IONOS. Backend eternal in Azure cloud.**

Ready to generate the frontend-only IONOS deployment script?
