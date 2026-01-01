# Codex Dominion - Complete Two-Cloud Architecture

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CODEX DOMINION                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🏛️  AZURE - THE CORE (Intelligence)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Flask Backend (52+ dashboards)                   │   │
│  │  • PostgreSQL Database (workflows, agents, councils)│   │
│  │  • Redis Cache (background workers, queues)         │   │
│  │  • Workflow Engine (RQ workers)                     │   │
│  │  • Automation Engine (dawn dispatch, treasury)      │   │
│  │  • Orchestration Engine (capsules)                  │   │
│  │  • Advisor Brain (AI decision-making)               │   │
│  │  • Notifications + Background Jobs                  │   │
│  │  • Health Monitoring + Auto-restart                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↕                                 │
│  🌍 IONOS - THE FACE (Interface)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Next.js 14 Dashboard (52+ pages)                 │   │
│  │  • Public Marketing Site                            │   │
│  │  • Static Assets + CDN                              │   │
│  │  • Domain Management                                │   │
│  │  • SSL/HTTPS                                        │   │
│  │  • Fast Global Delivery                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Deployment

### Complete Deployment (Recommended)
```powershell
.\deploy-dominion-complete.ps1
```

### Skip Azure (Already Deployed)
```powershell
.\deploy-dominion-complete.ps1 -SkipAzure
```

### Skip IONOS (Azure Only)
```powershell
.\deploy-dominion-complete.ps1 -SkipIONOS
```

### Quick Deploy (Use Existing Image)
```powershell
.\deploy-dominion-complete.ps1 -QuickDeploy
```

## 🏛️ Azure - The Core

### What Gets Deployed

**1. PostgreSQL Database**
- Flexible Server (Burstable tier)
- Database: `codexdb`
- Tables: councils, agents, workflows, metrics, capsules
- Auto-backup enabled
- SSL required

**2. Redis Cache**
- Basic tier (C0)
- Used for: RQ worker queues, session storage, caching
- SSL connection
- Background job processing

**3. Backend Container Instance**
- Image: Flask + AI service
- CPU: 2 cores
- Memory: 4GB
- Port: 5000
- Environment: Production
- Auto-restart: Always
- Health checks: Enabled

**4. Worker Container Instance**
- Same image as backend
- CPU: 1 core
- Memory: 2GB
- Command: `rq worker workflows`
- Processes: Background jobs, workflows, automation

### Azure Endpoints

After deployment:
- **API Base:** `http://codex-api.eastus.azurecontainer.io:5000`
- **Health:** `/health`
- **Dashboard:** `/`
- **AI Services:** `/api/ai/*`
- **Treasury:** `/api/treasury/*`
- **Workflows:** `/api/workflows/*`
- **Councils:** `/api/councils/*`
- **Agents:** `/api/agents/*`

### Azure Benefits

✅ **Auto-restart** - Container crashes? Azure restarts it automatically
✅ **Crash protection** - Built-in health checks and monitoring
✅ **Logs** - Centralized logging via Azure Portal
✅ **Monitoring** - CPU, memory, network metrics
✅ **Scaling** - Easy to scale up/down
✅ **Stable API** - Always-on, no localhost issues
✅ **Database** - Managed PostgreSQL with backups
✅ **Workers** - Background job processing

## 🌍 IONOS - The Face

### What Gets Deployed

**1. Next.js Dashboard**
- 52+ dashboard pages
- TypeScript + React
- Static export (fast loading)
- Tailwind CSS
- shadcn/ui components

**2. Static Assets**
- Optimized images
- JavaScript bundles
- CSS files
- Fonts

**3. Domain + DNS**
- codexdominion.app
- www.codexdominion.app
- A records → 74.208.123.158

**4. SSL/HTTPS**
- Let's Encrypt certificate
- Auto-renewal via Certbot
- HTTPS redirect

### IONOS Configuration

**nginx Configuration:**
```nginx
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;
    root /var/www/codexdominion.app;
    index index.html;

    # Frontend static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API to Azure
    location /api/ {
        proxy_pass http://codex-api.eastus.azurecontainer.io:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### IONOS Benefits

✅ **Fast delivery** - Static files served from IONOS CDN
✅ **Low cost** - Simple VPS hosting
✅ **Simple deployment** - Just upload files
✅ **Zero downtime** - nginx handles traffic gracefully
✅ **Global reach** - Fast loading worldwide
✅ **Custom domain** - Professional branding

## 🔗 Integration

### How They Connect

1. **User visits** https://codexdominion.app (IONOS)
2. **IONOS serves** Next.js static files
3. **User clicks** "View Workflows" button
4. **Next.js calls** `/api/workflows` (proxied by nginx)
5. **nginx forwards** to Azure backend
6. **Azure Flask** queries PostgreSQL
7. **Flask returns** JSON response
8. **Next.js renders** data in beautiful UI

### Data Flow

```
User Browser (IONOS)
    ↓ HTTPS
IONOS nginx (Proxy)
    ↓ HTTP
Azure Flask Backend
    ↓
PostgreSQL Database
    ↓
Response → nginx → Browser
```

## 📊 What You Get

### Before (Localhost)
- ❌ Must keep computer running
- ❌ Port conflicts
- ❌ Manual restarts after crashes
- ❌ No remote access
- ❌ No backups
- ❌ No monitoring
- ❌ Single point of failure

### After (Azure + IONOS)
- ✅ Always online (99.9% uptime)
- ✅ Auto-restart on crashes
- ✅ Global access
- ✅ Automatic backups
- ✅ Health monitoring
- ✅ Scalable architecture
- ✅ Professional setup
- ✅ Separated concerns
- ✅ Fast frontend delivery
- ✅ Stable backend API

## 🔧 Maintenance

### View Azure Logs
```bash
az container logs --resource-group codexdominion-prod --name codex-backend
az container logs --resource-group codexdominion-prod --name codex-worker
```

### Restart Containers
```bash
az container restart --resource-group codexdominion-prod --name codex-backend
az container restart --resource-group codexdominion-prod --name codex-worker
```

### Check Database
```bash
az postgres flexible-server show --resource-group codexdominion-prod --name codexdominion-db
```

### Update Frontend
```powershell
cd dashboard-app
npm run build
scp -r out/* root@74.208.123.158:/var/www/codexdominion.app/
```

### Update Backend
```powershell
# Rebuild image
az acr build --registry codexacr1216 --image codex-backend:latest --file Dockerfile.azure .

# Restart containers (they auto-pull new image)
az container restart --resource-group codexdominion-prod --name codex-backend
az container restart --resource-group codexdominion-prod --name codex-worker
```

## 💰 Cost Estimate

### Azure Monthly
- PostgreSQL Flexible Server (Burstable): ~$15
- Redis Cache (Basic C0): ~$17
- Container Instance Backend (2 CPU, 4GB): ~$50
- Container Instance Worker (1 CPU, 2GB): ~$25
- **Total Azure: ~$107/month**

### IONOS Monthly
- VPS hosting: ~$5-10
- Domain: ~$15/year ($1.25/month)
- **Total IONOS: ~$6-11/month**

### **Total System Cost: ~$113-118/month**

Compare to:
- Heroku Hobby: $7/dyno × 2 = $14 + $9 Postgres = $23 (limited features)
- AWS EC2 + RDS: $150-300/month
- Digital Ocean: $100-200/month

**Azure + IONOS = Professional setup at reasonable cost**

## 🎯 Success Metrics

After deployment, you'll have:

1. ✅ **Uptime:** 99.9%+ (Azure SLA)
2. ✅ **Response Time:** <200ms (static files from IONOS)
3. ✅ **API Latency:** <500ms (Azure backend)
4. ✅ **Database:** Managed, backed up, monitored
5. ✅ **Workers:** Background jobs processing 24/7
6. ✅ **Monitoring:** Real-time health checks
7. ✅ **Logs:** Centralized, searchable
8. ✅ **Security:** SSL, managed credentials
9. ✅ **Scalability:** Easy to scale up
10. ✅ **Professional:** Production-grade architecture

## 🔥 The End of Localhost Issues

No more:
- "Let me restart the server"
- "It works on my machine"
- "Port 5000 is already in use"
- "Database connection failed"
- "Redis not running"
- "Worker crashed"

Now you have:
- "Check https://codexdominion.app"
- "API is always available"
- "Everything is monitored"
- "Auto-restart on failures"
- "Logs show everything"
- "Professional deployment"

---

**🔥 The Flame Burns Sovereign and Eternal! 🔥**
