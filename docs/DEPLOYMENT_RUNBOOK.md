# Codex Dominion Deployment Runbook

## System Overview

**Production Environment**: Azure Cloud
**Backend**: FastAPI on Azure Container Instances
**Frontend**: Vite + React on Azure Static Web Apps
**Database**: PostgreSQL 16 Flexible Server
**Cache**: Azure Cache for Redis (Basic C0)

## Prerequisites

- Azure CLI installed and authenticated
- Docker installed locally
- Access to Azure subscription: 054bb0e0-6e79-403f-b3fc-39a28d61e9c9
- Resource group: codex-dominion

## Quick Reference

### URLs
- **Frontend**: https://happy-hill-0f1fded0f.3.azurestaticapps.net
- **Backend API**: http://codex-api-eastus.eastus.azurecontainer.io:8000
- **API Docs**: http://codex-api-eastus.eastus.azurecontainer.io:8000/docs
- **Health Check**: http://codex-api-eastus.eastus.azurecontainer.io:8000/health

### Resource Names
- Container Registry: `codexdominionacr`
- Container Instance: `codex-backend-api`
- PostgreSQL Server: `codex-pg-centralus2`
- Redis Cache: `codexdominion-redis`
- Static Web App: `codexdominion-frontend`
- Storage Account: `codexbackups2025`

## Deployment Procedures

### 1. Backend Deployment

#### Build and Push Docker Image
```powershell
# Navigate to project root
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion

# Build Docker image
docker build -t codexdominionacr.azurecr.io/codex-backend:v1.0.3 -f backend/Dockerfile .

# Login to ACR
az acr login --name codexdominionacr

# Push image
docker push codexdominionacr.azurecr.io/codex-backend:v1.0.3
```

#### Restart Container
```powershell
# Restart to pull latest image
az container restart `
    --resource-group codex-dominion `
    --name codex-backend-api

# Wait for startup
Start-Sleep -Seconds 20

# Verify health
curl http://codex-api-eastus.eastus.azurecontainer.io:8000/health
```

### 2. Frontend Deployment

#### Build Vite App
```powershell
cd frontend-vite
npm run build
```

#### Deploy to Static Web App
```powershell
$env:SWA_CLI_DEPLOYMENT_TOKEN='5c31dcc01f66d750703-f0b50c9a-958f-4a37-93ea-7889a853674300f20130f1fded0f'

npx @azure/static-web-apps-cli deploy ./dist `
    --deployment-token $env:SWA_CLI_DEPLOYMENT_TOKEN `
    --env production
```

### 3. Database Maintenance

#### Backup Database
```powershell
# Backups are automatic (30-day retention)
# To create manual backup:
az postgres flexible-server backup create `
    --resource-group codex-dominion `
    --name codex-pg-centralus2 `
    --backup-name manual-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')
```

#### Restore from Backup
```powershell
az postgres flexible-server restore `
    --resource-group codex-dominion `
    --name codex-pg-centralus2-restored `
    --source-server codex-pg-centralus2 `
    --restore-time "2025-12-11T00:00:00Z"
```

### 4. Monitor System Health

#### Check Container Status
```powershell
az container show `
    --resource-group codex-dominion `
    --name codex-backend-api `
    --query "{State:instanceView.state,Events:instanceView.events}" `
    -o table
```

#### View Logs
```powershell
# Backend logs
az container logs `
    --resource-group codex-dominion `
    --name codex-backend-api `
    --tail 50

# Follow logs in real-time
az container attach `
    --resource-group codex-dominion `
    --name codex-backend-api
```

#### Check Metrics
```powershell
# PostgreSQL CPU
az monitor metrics list `
    --resource /subscriptions/054bb0e0-6e79-403f-b3fc-39a28d61e9c9/resourceGroups/codex-dominion/providers/Microsoft.DBforPostgreSQL/flexibleServers/codex-pg-centralus2 `
    --metric cpu_percent `
    --start-time 2025-12-11T00:00:00Z

# Redis Memory
az monitor metrics list `
    --resource /subscriptions/054bb0e0-6e79-403f-b3fc-39a28d61e9c9/resourceGroups/codex-dominion/providers/Microsoft.Cache/Redis/codexdominion-redis `
    --metric usedmemorypercentage `
    --start-time 2025-12-11T00:00:00Z
```

## Troubleshooting

### Backend Not Responding

1. Check container status:
```powershell
az container show --name codex-backend-api --resource-group codex-dominion --query "instanceView.state"
```

2. View recent logs:
```powershell
az container logs --name codex-backend-api --resource-group codex-dominion --tail 100
```

3. Restart container:
```powershell
az container restart --name codex-backend-api --resource-group codex-dominion
```

### Database Connection Issues

1. Check firewall rules:
```powershell
az postgres flexible-server firewall-rule list `
    --resource-group codex-dominion `
    --name codex-pg-centralus2 `
    -o table
```

2. Test connection:
```powershell
psql -h codex-pg-centralus2.postgres.database.azure.com -U pgadmin -d codexdb
```

3. Check backend environment variables:
```powershell
az container show `
    --name codex-backend-api `
    --resource-group codex-dominion `
    --query "containers[0].environmentVariables"
```

### Frontend Not Loading

1. Check deployment status:
```powershell
az staticwebapp show `
    --name codexdominion-frontend `
    --resource-group codex-dominion `
    --query "{defaultHostname:defaultHostname,customDomains:customDomains}"
```

2. Redeploy frontend:
```powershell
cd frontend-vite
npm run build
# Deploy again using SWA CLI
```

### Redis Cache Issues

1. Check Redis status:
```powershell
az redis show `
    --name codexdominion-redis `
    --resource-group codex-dominion `
    --query "{provisioningState:provisioningState,redisVersion:redisVersion}"
```

2. Flush cache if needed:
```powershell
az redis force-reboot `
    --name codexdominion-redis `
    --resource-group codex-dominion `
    --reboot-type AllNodes
```

## Rollback Procedures

### Backend Rollback
```powershell
# Identify previous version
docker images | Select-String "codex-backend"

# Update container to use previous version
az container restart `
    --resource-group codex-dominion `
    --name codex-backend-api
# Note: Container pulls from :latest tag, so push previous version as :latest
```

### Database Rollback
```powershell
# Restore from automatic backup
az postgres flexible-server restore `
    --resource-group codex-dominion `
    --name codex-pg-centralus2-rollback `
    --source-server codex-pg-centralus2 `
    --restore-time "2025-12-10T00:00:00Z"
```

## Security

### Rotate Credentials

#### PostgreSQL Admin Password
```powershell
az postgres flexible-server update `
    --resource-group codex-dominion `
    --name codex-pg-centralus2 `
    --admin-password "NewSecurePassword!"

# Update container environment variables
az container restart --name codex-backend-api --resource-group codex-dominion
```

#### Redis Access Key
```powershell
az redis regenerate-keys `
    --name codexdominion-redis `
    --resource-group codex-dominion `
    --key-type Primary

# Get new key
az redis list-keys `
    --name codexdominion-redis `
    --resource-group codex-dominion
```

## Monitoring Alerts

### Active Alerts
- **PostgreSQL-High-CPU**: Triggers when CPU > 80% for 15 minutes
- **Redis-High-Memory**: Triggers when memory > 85% for 15 minutes

### Alert Actions
- Email notification to: jermainemerrittjr@gmail.com

### View Alert History
```powershell
az monitor activity-log list `
    --resource-group codex-dominion `
    --max-events 50
```

## Backup Strategy

### Automated Backups
- **PostgreSQL**: 30-day retention, daily backups
- **Redis**: Basic tier (no persistence - use Premium for persistence)
- **Exports**: Manual backup to codexbackups2025 storage account

### Manual Backup Exports
```powershell
# Export all formats
curl "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=yaml" -o backup.yaml
curl "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=markdown" -o backup.md
curl "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=pdf" -o backup.pdf
```

## Contacts

- **System Administrator**: Jermaine Merritt Jr.
- **Email**: jermainemerrittjr@gmail.com
- **Alert Notifications**: jermainemerrittjr@gmail.com

## Changelog

- **2025-12-11**: Initial production deployment v1.0.3
  - Backend with Redis caching
  - PostgreSQL database integration
  - Vite frontend deployment
  - Automated backups configured
