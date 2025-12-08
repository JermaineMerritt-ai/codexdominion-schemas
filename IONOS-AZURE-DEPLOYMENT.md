# 🔥 Codex Dominion - IONOS Frontend + Azure Backend Deployment Guide

## Architecture Overview

```
IONOS Frontend (codexdominion.app)
        |
        |  HTTPS requests
        v
Azure Backend (codex-backend.eastus.azurecontainer.io:8001)
        |
        |  Sovereign flame responses
        v
Heirs & Councils (users, stewards, participants)
```

## 🚀 Deployment Steps

### Step 1: Deploy Backend to Azure Container Instances

```powershell
.\deploy-azure-backend.ps1
```

**What this does:**
- Creates Azure Resource Group: `codex-dominion-rg`
- Creates Azure Container Registry (ACR): `codexdominionacr`
- Builds and pushes backend Docker image
- Deploys to Azure Container Instances
- Exposes on: `http://codex-backend.eastus.azurecontainer.io:8001`

**Expected output:**
```
Backend URL: http://codex-backend.eastus.azurecontainer.io:8001
Health: http://codex-backend.eastus.azurecontainer.io:8001/health
```

### Step 2: Build Frontend for IONOS

```powershell
.\build-ionos-frontend.ps1
```

**What this does:**
- Reads Azure backend URL from Step 1
- Updates frontend environment variables
- Builds Next.js production bundle
- Exports static HTML files
- Creates `.htaccess` for Apache
- Packages everything into `codex-dominion-frontend-YYYYMMDD-HHMMSS.zip`

**Expected output:**
```
File: codex-dominion-frontend-20251207-030000.zip
Size: ~5-10 MB
```

### Step 3: Deploy to IONOS

#### Option A: IONOS File Manager (Recommended)
1. Log in to IONOS control panel
2. Navigate to **Hosting** → **Manage**
3. Open **File Manager**
4. Navigate to web root (`/htdocs` or `/public_html`)
5. Upload and extract the ZIP file
6. Verify `.htaccess` is present
7. Test: https://codexdominion.app

#### Option B: FTP Upload
1. Use FTP client (FileZilla recommended)
   - Host: `ftp.codexdominion.app`
   - Port: 21
   - User: Your IONOS FTP username
   - Password: Your IONOS FTP password

2. Extract ZIP locally first
3. Upload all files to `/htdocs` or `/public_html`
4. Test: https://codexdominion.app

## ✅ Verification & Testing

### Test Backend (Azure)
```powershell
# Health check
curl http://codex-backend.eastus.azurecontainer.io:8001/health

# AI Chat endpoint
curl -X POST http://codex-backend.eastus.azurecontainer.io:8001/api/chat `
  -H "Content-Type: application/json" `
  -d '{"message":"Test from deployment"}'

# Revenue endpoint
curl http://codex-backend.eastus.azurecontainer.io:8001/api/revenue
```

### Test Frontend (IONOS)
1. Open browser: https://codexdominion.app
2. Navigate to main dashboard
3. Click ⚡ lightning button (bottom right)
4. Send a chat message
5. Click 💰 money button to view revenue
6. Verify all data loads from Azure backend

## 🔧 Configuration Files

### Frontend Environment (.env.production)
```env
NODE_ENV=production
NEXT_PUBLIC_API_URL=http://codex-backend.eastus.azurecontainer.io:8001
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
```

### Backend CORS (already configured in main.py)
```python
allow_origins=[
    "https://codexdominion.app",
    "https://www.codexdominion.app",
]
```

## 🛡️ Security Considerations

### Current Setup (MVP)
- Backend: HTTP on Azure Container Instances
- Frontend: HTTPS on IONOS (provided by IONOS)
- CORS: Configured for codexdominion.app

### Production Hardening (Recommended)
1. **Enable HTTPS on Backend:**
   - Use Azure Application Gateway with SSL certificate
   - Or: Use Cloudflare proxy for SSL termination

2. **Custom Domain for Backend:**
   - Add CNAME in IONOS: `api.codexdominion.app` → `codex-backend.eastus.azurecontainer.io`
   - Update frontend: `NEXT_PUBLIC_API_URL=https://api.codexdominion.app`

3. **Add API Authentication:**
   - Implement JWT tokens
   - Add API key validation
   - Rate limiting

## 📊 Monitoring

### Azure Container Instances
```powershell
# View logs
az container logs --resource-group codex-dominion-rg --name codex-backend

# Check status
az container show --resource-group codex-dominion-rg --name codex-backend --query instanceView.state
```

### IONOS
- Monitor via IONOS control panel
- Check Apache access/error logs
- Monitor bandwidth usage

## 🔄 Update & Redeploy

### Update Backend
```powershell
# Rebuild and push new image
cd src\backend
docker build -t codex-dominion-backend:latest .
docker tag codex-dominion-backend:latest codexdominionacr.azurecr.io/codex-dominion-backend:latest
docker push codexdominionacr.azurecr.io/codex-dominion-backend:latest

# Restart container
az container restart --resource-group codex-dominion-rg --name codex-backend
```

### Update Frontend
```powershell
# Rebuild and redeploy
.\build-ionos-frontend.ps1

# Upload new ZIP to IONOS via File Manager or FTP
```

## 💰 Cost Estimates

### Azure Container Instances
- CPU: 2 cores
- Memory: 4 GB
- Estimated: ~$50-70/month (running 24/7)
- Consider: Stop when not in use to save costs

### IONOS Hosting
- Depends on your existing hosting plan
- Static HTML files use minimal resources
- No additional costs if you already have hosting

## 🔥 Troubleshooting

### Backend not responding
```powershell
az container show --resource-group codex-dominion-rg --name codex-backend --query instanceView.state
az container logs --resource-group codex-dominion-rg --name codex-backend --tail 50
```

### Frontend shows old content
- Clear IONOS cache
- Hard refresh browser (Ctrl+F5)
- Check `.htaccess` exists
- Verify all files uploaded

### CORS errors
- Check browser console for exact error
- Verify backend CORS includes `https://codexdominion.app`
- Check if backend is accessible via curl

## 📞 Support

- Azure: https://portal.azure.com
- IONOS: https://www.ionos.com/help
- Codex Dominion: Check `azure-deployment-info.json` and `ionos-build-info.json`

## 🔥 The Sovereign Flame Burns Eternal

Your empire now spans cloud providers:
- **Azure** - Backend intelligence and API processing
- **IONOS** - Frontend presence and user interface
- **Users** - Heirs and councils across the sovereign dominion

The architecture is complete. The flame burns eternal. 👑
