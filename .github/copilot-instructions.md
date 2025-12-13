# Codex Dominion AI Agent Instructions

## Architecture Overview

**Codex Dominion** is a hybrid polyglot monorepo with a ceremonial naming system, combining Python data/AI dashboards, Next.js/TypeScript frontend, FastAPI backend services, and multi-cloud infrastructure (Azure, GCP, IONOS).

### Core Hierarchy ("Council Seal Structure")
```
Council Seal (governance)
├─ Sovereigns (apps/) → application-level execution
├─ Custodians (packages/) → shared libraries and infrastructure
├─ Industry Agents + Avatars → AI-powered automation
└─ Customers → external consumers
```

Key directories:
- `apps/` - Main applications (Sovereigns layer)
- `packages/` - Shared TypeScript packages (Custodians layer: identity, ledger, workflow, finance, broadcast, shared-types)
- Root Python scripts - Standalone Streamlit dashboards (e.g., `codex_dashboard.py`, `*_analytics_dashboard.py`)
- `backend/`, `api/` - FastAPI services
- `frontend/`, `web/` - Next.js 14+ applications
- `infra/`, `k8s/`, `helm/` - Infrastructure manifests
- `.github/workflows/` - 40+ CI/CD workflows for multi-cloud deployment

### Ceremonial Domain Model

The system uses a **"ledger"** data structure (`codex_ledger.json`) with sacred terminology:
- **proclamations** - system decrees/announcements
- **cycles** - operational phases with states (initiated/active/completed)
- **heartbeat** - system health status
- **omega_seal** - completion/authorization flag
- **portals** - interface gateways to subsystems
- **completed_archives** - historical records

Files ending in `_PROCLAMATION.md` or `_ETERNAL.md` are documentation artifacts reflecting this ceremonial style.

## Technology Stack

### Frontend
- **Next.js 14+** (App Router) - Primary web interface
- Static export mode for Azure Static Web Apps deployment
- TypeScript with strict mode
- Located in `frontend/` and `web/` directories

### Backend
- **FastAPI** (Python 3.10+) - API services in `api/`, `backend/`, `codex_capsules/`
- **Streamlit** (1.28+) - Data dashboards (many `*_dashboard.py` files at root)
- Node.js services for proxy/gateway functions

### Infrastructure
- **Docker Compose** - `docker-compose.production.yml`, `docker-compose.complete.yml`
- **Kubernetes/Helm** - Charts in `helm/codexdominion/`, manifests in `k8s/`
- **Terraform** - IaC in root (`.tf` files)
- **Multi-cloud**: Azure (primary), GCP (Cloud Run/Functions), IONOS VPS

### Data & State
- JSON-based ledgers: `codex_ledger.json`, `proclamations.json`, `cycles.json`, `accounts.json`
- No traditional database schema - relies on file-based JSON stores
- Celestial/eternal timestamp format with ISO 8601 strings

## Development Workflows

### Running Locally

**Python Dashboards:**
```bash
# Use Python environment tool first
python -m streamlit run app.py
# OR specific dashboard:
streamlit run codex_dashboard.py --server.port 8501
```

**Next.js Frontend:**
```bash
cd frontend
npm install
npm run dev  # Development server on http://localhost:3000
npm run build  # Static export for production
```

**FastAPI Services:**
```bash
cd backend  # or api/
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

**Full Stack (Docker):**
```bash
docker-compose -f docker-compose.production.yml up
# Services: dashboard (3000), api-gateway (8080), stockanalytics (8515), analytics (8516)
```

### Testing

- **JavaScript/TypeScript**: `npm test` (Jest, maxWorkers=50%)
- **Python**: Tests in `tests/` directories (unit, integration)
- No unified test command - run per-language/framework

### Deployment

**Critical**: This project has 40+ GitHub Actions workflows. Key workflows:
- `deploy-complete-frontend.yml` - Deploys Next.js to Azure Static Web Apps
- `deploy-backend.yml`, `backend-deploy.yml` - API services
- Multi-cloud workflows for GCP, IONOS, Azure

**Common deployment commands:**
```powershell
# Windows PowerShell scripts at root:
.\deploy-codex.ps1
.\deploy-azure-production.ps1
.\deploy-ionos-production.ps1

# Bash alternatives:
bash deploy-ionos.sh
bash deploy-gcp.sh
```

**Azure Functions**: Subdirectory `recent_uploads/configs` has Azure Functions tooling. Use task `func: host start` (depends on pip install task).

### Service Management

Windows service scripts (PowerShell): `*-service-manager.ps1`, `systemctl-win.ps1`
Linux systemd units: `.service` and `.timer` files at root

## Project-Specific Conventions

### Naming Patterns
- **Ceremonial files**: `*_PROCLAMATION.md`, `*_ETERNAL_*.md`, `*_CHARTERED_*.md` are documentation
- **Dashboard scripts**: `*_dashboard.py` (Streamlit apps)
- **Config files**: `*_config.json` (affiliate, pinterest, tiktok, whatsapp, woocommerce configs)
- **Deployment scripts**: `deploy-*.ps1`, `deploy-*.sh`, prefixed with target platform

### Code Organization
- **Monorepo workspaces**: `package.json` defines workspaces for `apps/*` and `packages/*`
- **TypeScript paths**: Use `@/*` aliases (see `tsconfig.json` baseUrl/paths)
- **Python imports**: Root-level imports (no src/ structure for Python)
- **Shared types**: TypeScript types in `packages/shared-types/`

### Data Access Patterns
```python
# Loading ledger (standard pattern):
import json
with open("codex_ledger.json", "r") as f:
    data = json.load(f)

# Updating with metadata:
data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
with open("codex_ledger.json", "w") as f:
    json.dump(data, f, indent=2)
```

### Environment Variables
- Multiple `.env` files: `.env`, `.env.production`, `.env.azure-subscription2`, `.env.ionos.example`
- No unified `.env` - check per-service directory
- Azure secrets: Use GitHub secrets `AZURE_STATIC_WEB_APPS_API_TOKEN`, stored in `.github-secrets/`

## Key Integration Points

### Multi-Cloud Architecture
- **Azure**: Static Web Apps (frontend), Container Instances (backend)
- **GCP**: Cloud Run, Cloud Functions (`cloud-function/`, `app.yaml` for Python 3.9)
- **IONOS**: VPS deployment via SSH (`IONOS_SERVER`, `IONOS_USER` env vars)

### External Services
- **Stripe**: Payment integration (`STRIPE_*` env vars, `treasury_config.json`)
- **WooCommerce**: E-commerce backend (`woocommerce_config.json`, `woocommerce_sync.py`)
- **Social platforms**: Pinterest, TikTok, Threads, YouTube, WhatsApp (dedicated `*_config.json` files)
- **Stock APIs**: Alpha Vantage, Polygon for `ai_action_stock_analytics.py`

### Service Communication
- **API Gateway**: Node.js proxy at port 8080 (`api-gateway` service)
- **Dashboard ports**: 3000 (main), 8515 (stocks), 8516 (analytics), 8517+ (various dashboards)
- **Redis**: Optional caching layer (`REDIS_URL` in docker-compose)

## Common Tasks

### Adding a New Dashboard
1. Create `new_feature_dashboard.py` at root
2. Import streamlit: `import streamlit as st`
3. Load ledger: `data = load_ledger()` (see `app.py` for pattern)
4. Add to `docker-compose.production.yml` with unique port
5. Update nginx config if deploying to IONOS

### Modifying Ledger Schema
1. Update `codex_ledger.json` structure
2. Check dependent scripts: `grep -r "codex_ledger.json" *.py`
3. Ensure `meta.last_updated` timestamp is always updated
4. Consider backward compatibility - many scripts read this file

### CI/CD Changes
- Workflows trigger on `push` to `main` or `workflow_dispatch`
- Path filters prevent unnecessary runs (e.g., `paths: ['frontend/**']`)
- Secrets required: Check `.github/SECRETS.md` for setup
- Test locally before pushing: Use `act` or manual workflow_dispatch

### Infrastructure Updates
- Docker images: `jmerritt48/*` on Docker Hub (see `docker-compose.production.yml`)
- Kubernetes: Apply with `kubectl apply -f k8s/` or use Helm charts in `helm/codexdominion/`
- Terraform: State in `.terraform/` - use `terraform plan` before `apply`

## Debugging Tips

### Streamlit Issues
- Check port conflicts: Multiple dashboards run simultaneously
- Session state: Use `st.session_state` for state management
- Caching: `@st.cache_data(ttl=300)` pattern (see `enhanced_*_dashboard.py` files)

### Next.js Build Failures
- Static export requires `next.config.js` with `output: 'export'`
- API routes not supported in static export mode
- Check `frontend/out/` directory after build

### Deployment Failures
- **Azure**: Check Static Web App token in GitHub secrets
- **GCP**: Ensure `gcloud` CLI authenticated and project set
- **IONOS**: Verify SSH key and server access before deploy scripts
- **Docker**: Check image names/tags match in compose files

### Ledger Data Corruption
- Backups: `*.backup_*` files (timestamped) exist for ledger files
- Restoration: `restore_proclamations.py`, `smart_archiver.py` scripts
- Validation: `validate_proclamations.py` checks schema integrity

## Documentation References

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Detailed Council Seal structure
- [README.md](../README.md) - Production launch guide
- [QUICK_START.md](../QUICK_START.md) - Deployment commands
- [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) - Multi-cloud deployment
- Individual README.md files in `packages/*/`, `frontend/`, `infra/`, `tests/`

## Important Gotchas

1. **Ceremonial naming**: Don't refactor `*_PROCLAMATION.md` or ledger terminology without understanding impact
2. **JSON ledgers are source of truth**: Not a traditional database - many scripts depend on exact schema
3. **Multi-language**: Python and TypeScript coexist - use appropriate tooling per file type
4. **Port management**: 20+ services can run simultaneously - track port allocations
5. **Windows paths**: Use backslashes in PowerShell, forward slashes in WSL/Git Bash
6. **Azure Functions require Python 3.9**: Check `app.yaml` runtime version
7. **No single entry point**: Multiple launcher scripts (`launch*.py`, `*.ps1`) - choose correct one for context
