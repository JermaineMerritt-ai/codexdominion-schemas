# Codex Dominion - Infrastructure as Code

Complete Azure infrastructure deployment using Bicep templates.

## 📦 Available Templates

### 1. `main.bicep` - Standard Deployment
- PostgreSQL with firewall rules (allows Azure services)
- Redis with public access + TLS
- Secrets in environment variables
- Log Analytics + Application Insights
- **Cost:** ~$47-50/month
- **Use case:** Development, testing, quick deployments

### 2. `main-private.bicep` - Private Network ⭐ RECOMMENDED
- Private endpoints for PostgreSQL and Redis
- VNet integration for App Service (10.10.0.0/16)
- Azure Key Vault for secrets management
- Private DNS zones for name resolution
- No public database/cache access
- **Cost:** ~$53-58/month (+$6-8 for security)
- **Use case:** Production, compliance, enterprise security

📖 **[Compare Templates](./TEMPLATE_COMPARISON.md)** - Detailed feature comparison

## 🚀 Quick Start

### Private Network (Recommended for Production)

```bash
# One command - secure deployment
KV_NAME="codexkv$(date +%s)"
az deployment group create \
  --resource-group codex-rg \
  --template-file infra/main-private.bicep \
  --parameters \
    baseName=codex \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<STRONG_PASSWORD>' \
    keyVaultName=$KV_NAME
```

📖 **[Private Network Quick Start](./QUICK_START_PRIVATE.md)** - Complete guide with all steps

### Standard Deployment (Development/Testing)

```bash
az deployment group create \
  --resource-group codex-rg \
  --template-file infra/main.bicep \
  --parameters \
    baseName=codex \
    environment=prod \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<STRONG_PASSWORD>'
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICK_START_PRIVATE.md](./QUICK_START_PRIVATE.md)** | Fast deployment with private network template |
| **[PRIVATE_NETWORK_GUIDE.md](./PRIVATE_NETWORK_GUIDE.md)** | Complete private network architecture guide |
| **[TEMPLATE_COMPARISON.md](./TEMPLATE_COMPARISON.md)** | Feature comparison and decision guide |
| **[deploy.ps1](./deploy.ps1)** | PowerShell deployment automation script |
| **[main.bicep](./main.bicep)** | Standard Bicep template |
| **[main-private.bicep](./main-private.bicep)** | Private network Bicep template |

## 🎛️ Template Parameters

### main-private.bicep (Recommended)

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `location` | No | `eastus` | Azure region |
| `baseName` | No | `codex` | Resource prefix |
| `acrName` | Yes | - | Container registry name (globally unique) |
| `dockerImage` | Yes | - | Full Docker image path |
| `pgAdminPassword` | Yes | - | PostgreSQL password (secure!) |
| `pgDbName` | No | `codexdb` | Database name |
| `keyVaultName` | Yes | - | Key Vault name (globally unique) |
| `backendPort` | No | `8000` | Container port |
| `allowedOrigins` | No | `*` | CORS origins |

### main.bicep (Standard)

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `location` | No | `eastus` | Azure region |
| `baseName` | No | `codex` | Resource prefix |
| `environment` | No | `prod` | Environment (dev/staging/prod) |
| `acrName` | Yes | - | Container registry name |
| `dockerImage` | Yes | - | Full Docker image path |
| `pgAdminPassword` | Yes | - | PostgreSQL password |
| `appServiceSku` | No | `B1` | App Service tier |
| `redisSku` | No | `Basic` | Redis tier |

## 💰 Cost Estimates

### Base Configuration (Recommended)
| Resource | SKU | Monthly Cost |
|----------|-----|--------------|
| Static Web Apps | Free | **$0** |
| App Service Plan | B1 | **~$13** |
| Container Registry | Basic | **~$5** |
| PostgreSQL | Standard_B1ms | **~$12-15** |
| Redis Cache | Basic C0 | **~$15** |
| Application Insights | Pay-as-you-go | **~$2** (5GB free) |
| **Total** | | **~$47-50/month** |

### Production Configuration
| Resource | SKU | Monthly Cost |
|----------|-----|--------------|
| Static Web Apps | Standard | **~$9** |
| App Service Plan | P1V2 | **~$80** |
| Container Registry | Basic | **~$5** |
| PostgreSQL | General Purpose | **~$100+** |
| Redis Cache | Standard C1 | **~$55** |
| Application Insights | Pay-as-you-go | **~$5-10** |
| **Total** | | **~$254-259/month** |

## 📊 Deployment Outputs

After successful deployment, you'll receive:

```json
{
  "staticWebAppHostname": "codex-frontend-prod-abc123.azurestaticapps.net",
  "backendUrl": "https://codex-backend-prod.azurewebsites.net",
  "acrLoginServer": "codexacrprod.azurecr.io",
  "postgresFqdn": "codex-pg-prod.postgres.database.azure.com",
  "redisHostname": "codex-redis-prod.redis.cache.windows.net",
  "appInsightsKey": "abc123...",
  "staticWebAppToken": "deployment-token-here"
}
```

These outputs are automatically saved to `infra/deployment-outputs.json`.

## 🔄 CI/CD Integration

### GitHub Actions Secrets

Add these secrets to your GitHub repository:

```bash
# Get Static Web Apps deployment token
az staticwebapp secrets list \
  --name codex-frontend-prod \
  --resource-group codex-rg \
  --query "properties.apiKey" -o tsv

# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "codex-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/codex-rg \
  --sdk-auth
```

Required GitHub Secrets:
- `AZURE_STATIC_WEB_APPS_API_TOKEN` - For frontend deployment
- `AZURE_CREDENTIALS` - For backend deployment
- `ACR_USERNAME` and `ACR_PASSWORD` - For Docker push

### Automated Deployment Workflow

The infrastructure supports these workflows:
1. **Frontend** - Auto-deploys on push to `main`
2. **Backend** - Auto-deploys on `src/backend/**` changes
3. **Database** - Manual trigger for schema updates
4. **Redis** - Manual trigger for cache provisioning

## 🔧 Post-Deployment Steps

### 1. Build and Push Docker Image

```bash
# Login to ACR
az acr login --name codexacrprod

# Build backend image
cd src/backend
docker build -t codexacrprod.azurecr.io/codex-backend:latest .

# Push to ACR
docker push codexacrprod.azurecr.io/codex-backend:latest
```

### 2. Deploy Frontend

```bash
cd frontend
npm install
npm run build

# Deploy to Static Web Apps
npx @azure/static-web-apps-cli deploy out \
  --deployment-token <token-from-outputs>
```

### 3. Initialize Database Schema

```bash
# Connect to PostgreSQL
psql "postgresql://codexadmin@codex-pg-prod.postgres.database.azure.com:5432/codexdb?sslmode=require"

# Run schema initialization
\i infra/schema.sql
```

### 4. Verify Deployment

```bash
# Test frontend
curl https://codex-frontend-prod-abc123.azurestaticapps.net

# Test backend
curl https://codex-backend-prod.azurewebsites.net/health

# Test database connection (via backend)
curl https://codex-backend-prod.azurewebsites.net/health | jq .database
```

## 🛠️ Management Operations

### Update Environment Variables

```bash
# Add new environment variable to App Service
az webapp config appsettings set \
  --name codex-backend-prod \
  --resource-group codex-rg \
  --settings NEW_VARIABLE=value
```

### Scale Resources

```bash
# Scale App Service Plan
az appservice plan update \
  --name codex-plan-prod \
  --resource-group codex-rg \
  --sku P1V2

# Scale Redis Cache
az redis update \
  --name codex-redis-prod \
  --resource-group codex-rg \
  --sku Standard \
  --vm-size c1
```

### Backup Database

```bash
# Create PostgreSQL backup
az postgres flexible-server backup create \
  --name codex-pg-prod \
  --resource-group codex-rg \
  --backup-name daily-$(date +%Y%m%d)
```

### View Logs

```bash
# App Service logs
az webapp log tail \
  --name codex-backend-prod \
  --resource-group codex-rg

# Application Insights queries
az monitor app-insights query \
  --app codex-insights-prod \
  --analytics-query "requests | where timestamp > ago(1h)"
```

## 🔐 Security Best Practices

### Production Checklist
- [ ] Use Key Vault for secrets (enable with `enableKeyVault=true`)
- [ ] Restrict PostgreSQL firewall to specific IPs
- [ ] Enable Advanced Threat Protection for PostgreSQL
- [ ] Configure custom domain with SSL for Static Web Apps
- [ ] Enable diagnostic settings for all resources
- [ ] Set up Azure Monitor alerts
- [ ] Configure backup retention policies
- [ ] Review and restrict CORS origins
- [ ] Enable Azure AD authentication for App Service
- [ ] Use managed identities instead of connection strings

### Managed Identity Setup

```bash
# Grant App Service access to Key Vault
az keyvault set-policy \
  --name codex-kv-prod \
  --object-id $(az webapp show --name codex-backend-prod --resource-group codex-rg --query identity.principalId -o tsv) \
  --secret-permissions get list
```

## 📈 Monitoring & Alerts

### Application Insights Queries

```kusto
// Failed requests in last hour
requests
| where timestamp > ago(1h)
| where success == false
| summarize count() by resultCode

// Average response time
requests
| where timestamp > ago(24h)
| summarize avg(duration) by bin(timestamp, 1h)

// Database query performance
dependencies
| where type == "SQL"
| where timestamp > ago(1h)
| summarize avg(duration), percentile(duration, 95) by name
```

### Create Alerts

```bash
# Alert on failed requests
az monitor metrics alert create \
  --name "high-error-rate" \
  --resource-group codex-rg \
  --scopes $(az webapp show --name codex-backend-prod --resource-group codex-rg --query id -o tsv) \
  --condition "count requests/failed > 10" \
  --window-size 5m \
  --evaluation-frequency 1m
```

## 🗑️ Cleanup

### Delete Everything

```bash
# Delete entire resource group (irreversible!)
az group delete --name codex-rg --yes --no-wait
```

### Delete Specific Resources

```bash
# Delete just the App Service (keep data)
az webapp delete --name codex-backend-prod --resource-group codex-rg
```

## 📚 Additional Resources

- [Azure Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Static Web Apps Docs](https://learn.microsoft.com/azure/static-web-apps/)
- [App Service on Linux](https://learn.microsoft.com/azure/app-service/quickstart-custom-container)
- [PostgreSQL Flexible Server](https://learn.microsoft.com/azure/postgresql/flexible-server/)
- [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/)

## 🆘 Troubleshooting

### Deployment Fails

```bash
# Check deployment logs
az deployment group show \
  --resource-group codex-rg \
  --name <deployment-name> \
  --query properties.error

# Validate template
az deployment group validate \
  --resource-group codex-rg \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json
```

### App Service Not Starting

```bash
# Check container logs
az webapp log tail --name codex-backend-prod --resource-group codex-rg

# Restart App Service
az webapp restart --name codex-backend-prod --resource-group codex-rg
```

### Database Connection Issues

```bash
# Test PostgreSQL connectivity
psql "postgresql://codexadmin@codex-pg-prod.postgres.database.azure.com:5432/codexdb?sslmode=require"

# Check firewall rules
az postgres flexible-server firewall-rule list \
  --name codex-pg-prod \
  --resource-group codex-rg
```

---

**Last Updated**: December 8, 2025
**Version**: 2.0
**Maintained By**: DevOps Team
