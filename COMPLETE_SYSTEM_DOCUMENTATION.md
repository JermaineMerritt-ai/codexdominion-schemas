# Codex Dominion - Complete System Documentation

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [Master Dashboard User Manual](#master-dashboard-user-manual)
3. [API Documentation](#api-documentation)
4. [Deployment Runbook](#deployment-runbook)
5. [Troubleshooting Guide](#troubleshooting-guide)
6. [Video Tutorials](#video-tutorials)

---

## Quick Start Guide

### Prerequisites
- Windows 10/11 with PowerShell 5.1+
- Python 3.10+
- Node.js 18+
- Azure CLI
- Git

### Installation Steps

1. **Clone Repository**
```powershell
git clone https://github.com/JermaineMerritt-ai/codex-dominion.git
cd codex-dominion
```

2. **Start Master Dashboard**
```powershell
.\START_DASHBOARD.ps1
```

Access at: http://localhost:5000

3. **Test Azure Deployment**
- Frontend: https://witty-glacier-0ebbd971e.3.azurestaticapps.net
- Backend API (HTTPS): https://codex-backend-https.delightfulpond-6c97660b.eastus2.azurecontainerapps.io

---

## Master Dashboard User Manual

### Overview
The Master Dashboard Ultimate is a Flask-based web interface with 52+ integrated dashboards for managing your entire Codex Dominion ecosystem.

### Main Tabs

#### 1. Home Dashboard
- System overview
- Recent activity
- Quick stats
- Health indicators

**Features:**
- Real-time system status
- Treasury summary ($95,000/month target)
- Recent proclamations
- Active cycles

#### 2. AI Agents
Manage autonomous AI systems:
- **Jermaine Super Action AI**: Conversational AI assistant
- **.300 Action AI**: High-precision automation
- **Algorithm AI**: Data analysis and predictions

**Actions:**
- Deploy new agents
- Monitor agent performance
- View agent logs
- Configure agent behavior

#### 3. Social Media Management
Unified dashboard for all platforms:
- **YouTube**: 1,247 subscribers, 34,567 views/month
- **TikTok**: 3,456 followers, 87 videos
- **Pinterest**: 567 followers, 234 pins
- **Instagram**: 2,345 followers, 123 posts
- **Facebook**: 1,890 likes, 15,678 reach

**Features:**
- Schedule posts
- View analytics
- Manage content calendar
- Track engagement metrics

#### 4. Revenue Tracking
Treasury system with 8+ revenue streams:
- Affiliate Marketing: $2,156.73/month
- YouTube AdSense: $245.67/month
- Consulting: $3,000/month (estimated)
- Development: $2,000/project

**Features:**
- Real-time revenue tracking
- Monthly target progress
- Revenue stream breakdown
- Historical trends

#### 5. Affiliate Marketing
Manage affiliate partnerships:
- ShareASale: $1,203.50 (24 conversions)
- Amazon Associates: $687.23 (13 conversions)
- Commission Junction: $266.00 (6 conversions)

**Features:**
- Click tracking
- Conversion analytics
- Commission reports
- Top-performing products

#### 6. E-Commerce
WooCommerce integration:
- Product management
- Order processing
- Inventory tracking
- Customer analytics

#### 7. Copilot AI Instructions
Manage AI agent guidelines:
- View current instructions
- Edit ceremonial protocols
- Version control
- Deployment rules

#### 8. Avatar System
Digital identity management:
- Customer support avatar
- Sales agent avatar
- Analyst avatar
- Orchestrator avatar

#### 9. Council Governance
System-wide decision making:
- Proclamations
- Approvals
- Policies
- Oversight

#### 10. Action Chatbot
Interactive AI assistant:
- Natural language queries
- System commands
- Real-time responses
- Context-aware suggestions

#### 11. Algorithm AI
Advanced analytics:
- Predictive modeling
- Data processing
- Pattern recognition
- Automated insights

#### 12. Auto-Publish System
Content automation:
- Scheduled publishing
- Cross-platform distribution
- Content templates
- Performance tracking

### Navigation
- **Top Menu**: Quick access to all tabs
- **Sidebar**: Contextual actions
- **Footer**: System info and links

### Keyboard Shortcuts
- `Ctrl + H`: Home
- `Ctrl + A`: AI Agents
- `Ctrl + S`: Social Media
- `Ctrl + R`: Revenue
- `Ctrl + Q`: Quick search

---

## API Documentation

### Base URL
- **Production (HTTPS)**: https://codex-backend-https.delightfulpond-6c97660b.eastus2.azurecontainerapps.io
- **Legacy (HTTP)**: http://codex-api.eastus2.azurecontainer.io:8000

### Authentication
All API endpoints currently use open access. Future versions will implement:
- API key authentication
- OAuth 2.0
- JWT tokens

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "codex-dominion-api",
  "version": "1.0.0"
}
```

#### Treasury Summary
```http
GET /api/treasury/summary?days=30
```

**Parameters:**
- `days` (optional): Number of days to summarize (default: 30)

**Response:**
```json
{
  "total_revenue": 5049.99,
  "streams": [
    {"name": "affiliate", "amount": 2156.73},
    {"name": "youtube", "amount": 245.67}
  ]
}
```

#### Dawn Dispatch Status
```http
GET /api/dawn/status
```

**Response:**
```json
{
  "last_dispatch": "2025-12-16T06:00:00Z",
  "next_dispatch": "2025-12-17T06:00:00Z",
  "status": "active"
}
```

### Rate Limits
- 100 requests/minute per IP
- 1000 requests/hour per IP

### Error Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

---

## Deployment Runbook

### Pre-Deployment Checklist
- [ ] Code reviewed and tested
- [ ] Environment variables configured
- [ ] Database backups completed
- [ ] DNS records verified
- [ ] SSL certificates valid

### Standard Deployment Process

#### 1. Backend Deployment
```powershell
# Build and push Docker image
docker build -t codexdominionacr.azurecr.io/codex-backend:latest ./backend
docker push codexdominionacr.azurecr.io/codex-backend:latest

# Deploy to Azure Container Apps
az containerapp update \
  --name codex-backend-https \
  --resource-group codex-rg \
  --image codexdominionacr.azurecr.io/codex-backend:latest
```

#### 2. Frontend Deployment
```powershell
# Build Next.js static export
cd frontend
npm run build

# Deploy to Azure Static Web Apps (automatic via GitHub Actions)
git push origin main
```

#### 3. Database Migration
```powershell
# Run migration script
python migrate_to_database.py

# Verify data
python verify_migration.py
```

### Rollback Procedure
```powershell
# Rollback to previous container image
az containerapp revision list \
  --name codex-backend-https \
  --resource-group codex-rg \
  --query "[0].name" -o tsv

az containerapp revision activate \
  --name codex-backend-https \
  --resource-group codex-rg \
  --revision <previous-revision-name>
```

### Post-Deployment Verification
```powershell
# Run system status check
.\system-status-check.ps1

# Verify endpoints
curl https://codex-backend-https.delightfulpond-6c97660b.eastus2.azurecontainerapps.io/health
curl https://witty-glacier-0ebbd971e.3.azurestaticapps.net
```

---

## Troubleshooting Guide

### Common Issues

#### Dashboard Not Starting
**Symptoms**: Error when running `START_DASHBOARD.ps1`

**Solutions:**
1. Check Python version: `python --version` (must be 3.10+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check port 5000: `netstat -ano | findstr :5000`
4. Kill blocking process: `taskkill /F /PID <pid>`

#### Backend API Timeout
**Symptoms**: 504 Gateway Timeout errors

**Solutions:**
1. Check container status:
```powershell
az container show --resource-group codex-rg --name codex-backend
```

2. View logs:
```powershell
az container logs --resource-group codex-rg --name codex-backend --tail 100
```

3. Restart container:
```powershell
az container restart --resource-group codex-rg --name codex-backend
```

#### DNS Not Resolving
**Symptoms**: Custom domain not accessible

**Solutions:**
1. Wait for DNS propagation (5-10 minutes, up to 48 hours)
2. Check DNS records:
```powershell
nslookup codexdominion.app
nslookup api.codexdominion.app
```

3. Clear DNS cache:
```powershell
ipconfig /flushdns
```

#### SSL Certificate Errors
**Symptoms**: "Certificate not trusted" warnings

**Solutions:**
1. Verify certificate status in Azure Portal
2. Wait for Let's Encrypt provisioning (2-5 minutes)
3. Check certificate expiration date

### Debug Mode

Enable verbose logging:
```powershell
$env:DEBUG = "true"
$env:LOG_LEVEL = "DEBUG"
.\START_DASHBOARD.ps1
```

### Support Contacts
- Email: support@codexdominion.app
- GitHub Issues: https://github.com/JermaineMerritt-ai/codex-dominion/issues
- Documentation: https://docs.codexdominion.app

---

## Video Tutorials

### Available Tutorials
1. **Getting Started** (10 minutes)
   - Installation walkthrough
   - First dashboard launch
   - Basic navigation

2. **Master Dashboard Deep Dive** (20 minutes)
   - All 52+ tabs explained
   - Key features demonstration
   - Power user tips

3. **Azure Deployment** (15 minutes)
   - Complete deployment process
   - DNS configuration
   - SSL setup

4. **API Integration** (12 minutes)
   - Connecting social media APIs
   - Affiliate network setup
   - Testing endpoints

5. **Database Migration** (8 minutes)
   - PostgreSQL setup
   - Data migration
   - Verification

6. **Troubleshooting Common Issues** (10 minutes)
   - Dashboard startup problems
   - API connectivity
   - DNS resolution

### Creating Your Own Tutorials

Record screencast:
```powershell
# Use OBS Studio or similar
# Screen resolution: 1920x1080
# Frame rate: 30fps
# Format: MP4
```

Upload to YouTube:
- Title format: "Codex Dominion - [Tutorial Name]"
- Tags: codexdominion, tutorial, azure, dashboard
- Playlist: Codex Dominion Tutorials

---

## Maintenance Schedule

### Daily
- Monitor system health: `.\system-status-check.ps1`
- Review error logs
- Check revenue metrics

### Weekly
- Update dependencies: `npm update`, `pip list --outdated`
- Review GitHub Actions workflows
- Backup database: `.\backup-database.ps1`

### Monthly
- Security updates
- SSL certificate renewal (automatic)
- Performance optimization
- Cost review

---

## System Requirements

### Local Development
- **OS**: Windows 10/11, macOS 11+, or Ubuntu 20.04+
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 20GB free space
- **Internet**: Broadband connection

### Azure Resources
- **Static Web App**: FREE tier
- **Container Apps**: 1 vCPU, 2GB RAM (~$30/month)
- **PostgreSQL**: Burstable tier (~$15/month)
- **Application Insights**: Basic usage (~$5/month)
- **Total**: ~$50/month

---

## License & Legal

Copyright © 2025 Codex Dominion. All rights reserved.

This documentation is provided "as is" without warranty of any kind.

---

**Last Updated**: December 16, 2025
**Version**: 2.0.0
**Status**: Production Ready

🔥 **The Flame Burns Sovereign and Eternal!** 👑
