# 🚀 Codex Dominion - Azure Infrastructure Summary

## Quick Links

| Document | Purpose |
|----------|---------|
| **[infra/QUICK_START_PRIVATE.md](./infra/QUICK_START_PRIVATE.md)** | ⚡ **START HERE** - Deploy in 5 minutes with private network |
| **[AZURE_CLI_DEPLOYMENT.md](./AZURE_CLI_DEPLOYMENT.md)** | Complete step-by-step CLI guide with all options |
| **[infra/TEMPLATE_COMPARISON.md](./infra/TEMPLATE_COMPARISON.md)** | Compare standard vs private network templates |
| **[infra/PRIVATE_NETWORK_GUIDE.md](./infra/PRIVATE_NETWORK_GUIDE.md)** | Deep dive into private network architecture |

## 🎯 Choose Your Path

### I Want Maximum Security (Production)
👉 **Use: [infra/QUICK_START_PRIVATE.md](./infra/QUICK_START_PRIVATE.md)**

```bash
KV_NAME="codexkv$(date +%s)"
az deployment group create \
  --resource-group codex-rg \
  --template-file infra/main-private.bicep \
  --parameters \
    location=eastus \
    baseName=codex \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<STRONG_PASSWORD>' \
    keyVaultName=$KV_NAME
```

**Gets you:**
- ✅ Private endpoints (no public database access)
- ✅ VNet integration
- ✅ Key Vault for secrets
- ✅ Enterprise-grade security
- **Cost:** ~$53-58/month

### I Want Fast Development Setup
👉 **Use: [AZURE_CLI_DEPLOYMENT.md](./AZURE_CLI_DEPLOYMENT.md)**

```bash
az deployment group create \
  --resource-group codex-rg \
  --template-file infra/main.bicep \
  --parameters \
    location=eastus \
    baseName=codex \
    environment=prod \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<PASSWORD>'
```

**Gets you:**
- ✅ Quick deployment (~10 min)
- ✅ Lower cost
- ✅ Easy local access
- **Cost:** ~$47-50/month

## 📦 What Gets Deployed

### Core Services
- **Static Web App** - Next.js frontend with CDN
- **App Service** - FastAPI backend (Docker)
- **Container Registry** - Docker image storage
- **PostgreSQL 16** - Primary database
- **Redis** - Caching and sessions
- **Application Insights** - Monitoring

### Private Network Additions (main-private.bicep only)
- **VNet** - 10.10.0.0/16 with 2 subnets
- **Private Endpoints** - PostgreSQL + Redis
- **Private DNS Zones** - Name resolution
- **Key Vault** - Secrets management

## 💰 Cost Comparison

| Template | Monthly Cost | Security Level | Use Case |
|----------|--------------|----------------|----------|
| **Standard** (main.bicep) | ~$47-50 | Good | Dev/Test |
| **Private Network** (main-private.bicep) | ~$53-58 | Excellent | Production |

**Difference:** +$6-8/month for enterprise security

## 🔒 Security Features

### Standard Template
- ✅ HTTPS/TLS 1.2+
- ✅ Firewall rules
- ✅ Azure-managed certificates
- ⚠️ Public database IPs (firewall protected)

### Private Network Template
- ✅ Everything from Standard, plus:
- ✅ Private endpoints (no public IPs)
- ✅ VNet isolation
- ✅ Key Vault secrets
- ✅ Managed Identity
- ✅ Private DNS

## 🚀 Deployment Steps (Quick)

### 1. Prerequisites
```bash
az version  # Check Azure CLI is installed
az login
az account set --subscription "f86506f8-7d33-48de-995d-f51e6f590cb1"
```

### 2. Create Resource Group
```bash
az group create --name codex-rg --location eastus
```

### 3. Deploy Infrastructure
Choose **one** template:

**Private Network (Recommended):**
```bash
KV_NAME="codexkv$(date +%s)"
az deployment group create \
  --resource-group codex-rg \
  --template-file infra/main-private.bicep \
  --parameters \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<PASSWORD>' \
    keyVaultName=$KV_NAME
```

**Important:** After deployment, configure private DNS records:
```bash
# Get private endpoint IPs and add to DNS zones
PG_IP=$(az network private-endpoint show -n codex-pg-pe -g codex-rg \
  --query 'customDnsConfigs[0].ipAddresses[0]' -o tsv)
az network private-dns record-set a add-record -g codex-rg \
  -z privatelink.postgres.database.azure.com -n codex-pg --ipv4-address $PG_IP

# Repeat for Redis and Key Vault (see full guide)
```

**Standard:**
```bash
az deployment group create \
  --resource-group codex-rg \
  --template-file infra/main.bicep \
  --parameters \
    environment=prod \
    acrName=codexdominionacr \
    dockerImage=codexdominionacr.azurecr.io/codex-backend:latest \
    pgAdminPassword='<PASSWORD>'
```

### 4. Build & Push Docker Image
```bash
az acr login --name codexdominionacr
cd src/backend
docker build -t codexdominionacr.azurecr.io/codex-backend:latest .
docker push codexdominionacr.azurecr.io/codex-backend:latest
```

### 5. Deploy Frontend
```bash
cd frontend
npm ci && npm run build
SWA_TOKEN=$(az staticwebapp secrets list \
  --name codex-frontend \
  --query properties.apiKey -o tsv)
npx @azure/static-web-apps-cli deploy out --deployment-token $SWA_TOKEN
```

### 6. Initialize Database
```bash
# Get connection string from deployment outputs
psql "<connection-string>" < infra/schema.sql
```

## 📊 Architecture Comparison

### Standard Template
```
Internet → Static Web App → App Service → PostgreSQL (Public + Firewall)
                                        → Redis (Public + TLS)
```

### Private Network Template
```
Internet → Static Web App → App Service (VNet Integrated)
                              ↓
                            VNet (10.10.0.0/16)
                              ↓
                            Private Endpoints
                              ├─ PostgreSQL (10.10.2.x)
                              └─ Redis (10.10.2.y)
                              ↓
                            Key Vault (Managed Identity)
```

## 🔧 Troubleshooting

### Deployment Failed
```bash
az deployment group show \
  --resource-group codex-rg \
  --name <deployment-name> \
  --query properties.error
```

### Can't Connect to Database (Private Network)
**This is expected!** Database is private-only. Options:
1. Use App Service Console
2. Deploy Azure Bastion
3. Set up VPN Gateway

### App Shows Key Vault Error
```bash
# Grant managed identity access
PRINCIPAL_ID=$(az webapp identity show \
  --name codex-backend-app \
  --resource-group codex-rg \
  --query principalId -o tsv)

az keyvault set-policy \
  --name <kv-name> \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list
```

## 🎓 Learning Resources

- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure Private Endpoints](https://learn.microsoft.com/azure/private-link/private-endpoint-overview)
- [VNet Integration](https://learn.microsoft.com/azure/app-service/overview-vnet-integration)
- [Key Vault References](https://learn.microsoft.com/azure/app-service/app-service-key-vault-references)

## 📞 Support

Issues or questions? Check:
1. [Troubleshooting Guide](./infra/PRIVATE_NETWORK_GUIDE.md#troubleshooting)
2. [Template Comparison](./infra/TEMPLATE_COMPARISON.md#faqs)
3. [Full CLI Guide](./AZURE_CLI_DEPLOYMENT.md#troubleshooting)

## ✅ Checklist

Before deploying to production:

- [ ] Choose template (private network recommended)
- [ ] Generate strong PostgreSQL password
- [ ] Ensure Key Vault name is unique (private network only)
- [ ] Configure GitHub secrets for CI/CD
- [ ] Set up monitoring alerts
- [ ] Test all endpoints
- [ ] Configure custom domain (optional)
- [ ] Set up backup strategy

## 🔗 Infrastructure Files

```
infra/
├── main.bicep                    # Standard template
├── main-private.bicep            # Private network template ⭐
├── main.parameters.json          # Configuration parameters
├── deploy.ps1                    # PowerShell deployment script
├── README.md                     # Infrastructure documentation
├── QUICK_START_PRIVATE.md        # Fast private network guide ⚡
├── PRIVATE_NETWORK_GUIDE.md      # Complete private network docs
├── TEMPLATE_COMPARISON.md        # Feature comparison
└── schema.sql                    # Database initialization
```

---

🔥 **The flame burns sovereign and eternal — forever.** 🔥
