# Codex Dominion - CI/CD Architecture

```mermaid
flowchart TD
    subgraph GitHub["GitHub Repository"]
        FE[Frontend Workflow<br>(Static Web Apps)]
        BE[Backend Workflow<br>(App Service via ACR)]
        DB[Database Migration Workflow<br>(PostgreSQL)]
        RE[Redis Migration Workflow<br>(Redis Cache)]
        ORCH[Infra Orchestrator<br>(Bicep + DNS Finalizer)]
    end

    subgraph Azure["Azure Cloud"]
        SWA[Static Web Apps<br>Global CDN + HTTPS]
        ACR[Azure Container Registry]
        ASP[App Service Plan]
        APP[App Service (Backend)<br>VNet Integrated]
        PG[PostgreSQL Flexible Server<br>Private Endpoint]
        REDIS[Redis Cache<br>Private Endpoint]
        KV[Key Vault<br>Private Endpoint]
        VNET[VNet + Private DNS Zones]
        AI[Application Insights]
    end

    FE --> SWA
    BE --> ACR --> APP
    APP --> PG
    APP --> REDIS
    APP --> KV
    ORCH --> SWA
    ORCH --> APP
    ORCH --> PG
    ORCH --> REDIS
    ORCH --> KV
    ORCH --> VNET
    APP --> AI
    SWA --> APP
```

## Workflow Descriptions

### 1. **Infra Orchestrator** (`deploy-private-infrastructure.yml`)
- Deploys complete infrastructure using `main-private.bicep`
- Automatically configures private DNS records post-deployment
- Creates VNet, private endpoints, DNS zones, and all Azure resources
- **Trigger:** Manual (workflow_dispatch)

### 2. **Frontend Workflow** (Static Web Apps)
- Builds and deploys React/Vue/Angular frontend
- Deploys to Azure Static Web Apps with global CDN
- Automatic HTTPS with custom domains
- **Trigger:** Push to main branch (frontend changes)

### 3. **Backend Workflow** (App Service via ACR)
- Builds Docker image from backend code
- Pushes to Azure Container Registry
- Updates App Service container configuration
- **Trigger:** Push to main branch (backend changes)

### 4. **Database Migration Workflow** (PostgreSQL)
- Runs schema migrations against PostgreSQL
- Executes via App Service (VNet-integrated access)
- Uses private endpoint connectivity
- **Trigger:** Manual or after backend deployment

### 5. **Redis Migration Workflow** (Redis Cache)
- Configures Redis cache settings
- Loads initial data if needed
- Tests connectivity via private endpoint
- **Trigger:** Manual or after infrastructure deployment

## Security Features

- ✅ All data services behind private endpoints (no public access)
- ✅ VNet integration for App Service backend
- ✅ Secrets managed in Key Vault (no environment variables)
- ✅ Managed identities for service-to-service authentication
- ✅ Private DNS zones for internal name resolution
- ✅ Application Insights for monitoring and diagnostics

## Deployment Order

1. **Infra Orchestrator** - Deploy infrastructure first
2. **Backend Workflow** - Build and deploy backend container
3. **Database Migration** - Initialize database schema
4. **Redis Migration** - Configure cache (optional)
5. **Frontend Workflow** - Deploy frontend to Static Web Apps

## Repository Structure

```
repo-root/
├── infra/
│   ├── main-private.bicep        # Hardened Azure infra template (VNet, Private Endpoints, DNS)
│   ├── QUICK_START_PRIVATE.md    # Fast deployment guide
│   ├── PRIVATE_NETWORK_GUIDE.md  # Complete private network documentation
│   └── TEMPLATE_COMPARISON.md    # Standard vs Private comparison
├── frontend/
│   ├── next.config.js            # API_BASE_URL binding to backend
│   └── ...                       # Your Next.js app files
├── backend/
│   ├── Dockerfile                # Exposes port 8000, runs FastAPI/Node backend
│   └── ...                       # Your backend app files
└── .github/
    └── workflows/
        ├── deploy-private-infrastructure.yml  # Master: Bicep deploy + DNS finalizer
        ├── finalize-private-dns.yml           # Standalone DNS configuration
        ├── frontend-deploy.yml                # Deploy Next.js → Static Web Apps
        ├── backend-deploy.yml                 # Build Docker → ACR → App Service
        ├── db-migrate.yml                     # PostgreSQL migrations (via VNet)
        └── redis-migrate.yml                  # Redis configuration (via VNet)
```

## Infrastructure Components

### Private Network Resources
- **VNet** (`10.10.0.0/16`) with two subnets:
  - App Service integration subnet (`10.10.1.0/24`)
  - Private endpoint subnet (`10.10.2.0/24`)
- **Private Endpoints** for PostgreSQL, Redis, Key Vault
- **Private DNS Zones** (3):
  - `privatelink.postgres.database.azure.com`
  - `privatelink.redis.cache.windows.net`
  - `privatelink.vaultcore.azure.net`

### Compute & Storage
- **Azure Static Web Apps** (Frontend)
- **App Service** (Backend with VNet integration)
- **Azure Container Registry** (Docker images)
- **PostgreSQL Flexible Server** (Private endpoint only)
- **Redis Cache** (Private endpoint only)
- **Key Vault** (Private endpoint only)
- **Application Insights** (Monitoring)
