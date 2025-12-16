# Codex Dominion AI Agent Instructions

## Architecture Overview

**Codex Dominion** is a hybrid polyglot monorepo with a ceremonial naming system, combining Python data/AI dashboards, Flask/Next.js web interfaces, FastAPI backend services, and multi-cloud infrastructure (Azure, GCP, IONOS).

### Core Hierarchy ("Council Seal Structure")
```
Council Seal (governance)
├─ Sovereigns (apps/) → application-level execution
├─ Custodians (packages/) → shared libraries and infrastructure
├─ Industry Agents + Avatars → AI-powered automation
└─ Customers → external consumers
```

Key directories:
- `apps/` - Main applications (Sovereigns layer): api, chatbot, commerce, compliance, consent_capsule, dashboard, flutter, observatory, react-native, replay_shell, sovereign-bridge, system, treaty_capsule
- `packages/` - Shared TypeScript packages (broadcast, council-seal, finance, healing, identity, ledger, schemas, shared, shared-types, ui, utils, workflow)
- Root Python scripts - Standalone Streamlit/Flask dashboards (`codex_dashboard.py`, `*_analytics_dashboard.py`, `*_dashboard.py`, `flask_dashboard.py`)
- `backend/`, `api/`, `codex_capsules/` - FastAPI services
- `frontend/`, `web/`, `frontend-vite/` - Next.js 14+ and Vite applications
- `infra/`, `k8s/`, `helm/` - Infrastructure manifests (Docker, Kubernetes, Helm charts)
- `.github/workflows/` - 50+ CI/CD workflows for multi-cloud deployment
- **Note**: `codexdominion-schemas/` and `codexdominion-clean/` are duplicate/archived directories - prefer root-level files

### Ceremonial Domain Model

The system uses a **"ledger"** data structure (`codex_ledger.json`) with ceremonial terminology:
- **meta** - version, omega_seal (boolean), last_updated (ISO 8601), custodian_authority, ledger_type, seal_power
- **heartbeat** - status (luminous/active), last_dispatch, next_dispatch, pulse_count, health_status
- **proclamations** - system decrees with id, title, status, issued_by, issued_date, content
- **cycles** - operational phases with states (initiated/active/completed)
- **contributions** - developer/system contributions logged with timestamps
- **completed_archives** - historical records of completed work
- **capsules** - autonomous execution units
- **video_generations** - ceremonial video production records
- **ai_commands** - AI system command history
- **portals** - interface gateways to subsystems

Files ending in `_PROCLAMATION.md`, `_ETERNAL.md`, `_CHARTERED.md` are documentation artifacts reflecting this ceremonial style.

### Ceremonial AI Integration

The system has ceremonial AI systems that follow specific guidelines:
- **Copilot-instruction.md** at root - Primary AI governance document (loaded by dashboards for ceremonial context)
- **Jermaine Super Action AI** (`jermaine_super_action_ai.py`) - Conversational AI with Copilot instruction awareness
- **Super Action AI** (`super_action_ai.py`) - Deployment automation with ceremonial validation
- **.300 Action AI** (`dot300_action_ai.py`) - High-precision automation with Copilot guideline integration

All AI systems honor:
- Ceremonial tone with flame metaphors
- Seasonal awareness (Spring/Summer/Autumn/Winter)
- Council governance patterns
- SSL-first validation before operations
- Dual environment support (production/staging)

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
- **Critical**: No traditional database - file-based JSON stores are source of truth
- Ledger backup files: `*.backup_*` (timestamped, used for restoration)
- Timestamp format: ISO 8601 with 'Z' suffix (e.g., `"2025-11-22T21:20:35.473129Z"`)
- Always update `meta.last_updated` when modifying ledger files
- **Current Status**: Production deployment recorded in `codex_ledger.json` under `portals.azure-production`

### Production Deployment (December 2025)

**Status**: \u2705 LIVE and OPERATIONAL

**Azure Infrastructure** (Resource Group: `codex-rg`, Region: East US 2):
- **Frontend (Static Web App)**: https://happy-flower-0e39c5c0f-preview.eastus2.3.azurestaticapps.net
  - Auto-managed SSL certificate (renewed automatically)
  - Static export from Next.js 14+ App Router
  - No port 443 blocking issues (Azure-managed)

- **Backend (Container App with SSL)**: https://codex-backend-https.delightfulpond-6c97660b.eastus2.azurecontainerapps.io
  - FastAPI services with automatic HTTPS
  - Auto-scaling (1-3 replicas)
  - Monthly cost: ~$30
  - Legacy HTTP endpoint: http://codex-api.eastus2.azurecontainer.io:8000

- **Container Registry**: `codexdominionacr.azurecr.io`
  - Stores Docker images (`jmerritt48/*` namespace)

**Deployment Tokens**: All stored in GitHub secrets, configured in workflows

**SSL Certificate Details** (recorded in ledger):
```json
{
  "issuer": "GeoTrust Global TLS RSA4096 SHA256 2022 CA1",
  "expires": "2026-04-14T23:59:59+00:00",
  "type": "SNI"
}
```

**CI/CD Status**: Auto-deploys on push to `main` branch via GitHub Actions

### Revenue & Treasury System
- **Treasury Database**: `codex_treasury_database.py` - Revenue tracking with 8+ streams
- **Revenue Targets**: $95,000/month across affiliate, YouTube, TikTok, WooCommerce, memberships
- **Treasury Config**: `treasury_config.json` - Configuration for revenue stream tracking
- **Dawn Dispatch**: `dawn_dispatch_simple.py` - Scheduled messaging and notifications
- **Access via**: `codex_unified_launcher.py treasury` commands for all treasury operations

## Development Workflows

### CLI Entry Points

The system has multiple launcher scripts for different purposes:

**Master Dashboard (Primary Interface)**:
```powershell
# Launch Flask-based Master Dashboard Ultimate (2,187 lines, 52+ dashboards)
.\START_DASHBOARD.ps1
# Or Python directly
python flask_dashboard.py  # Runs on http://localhost:5000
```

**Unified CLI Launcher** (Backend Operations):
```bash
# Treasury and Dawn dispatch operations - preferred for system operations
python codex_unified_launcher.py treasury summary --days 30
python codex_unified_launcher.py treasury ingest --stream affiliate --amount 49.99
python codex_unified_launcher.py treasury list --limit 10
python codex_unified_launcher.py dawn dispatch
python codex_unified_launcher.py dawn status
python codex_unified_launcher.py status  # Overall system status
python codex_unified_launcher.py report  # Comprehensive system report
python codex_unified_launcher.py serve   # Flask API server for Cloud Run
python codex_unified_launcher.py setup   # Database setup (PostgreSQL)
```

**Available commands**:
- `treasury` - Revenue tracking (summary, ingest, list)
- `dawn` - Dawn dispatch operations (dispatch, status)
- `status` - System health check across all components
- `report` - Generate detailed report with treasury + dawn data
- `serve` - Start web API on port 8080 (supports /health, /api/treasury/summary, /api/dawn/status)
- `setup` - Initialize PostgreSQL database if available

**Quick Dashboard Launchers**:
```bash
python launch.py  # Quick launcher for Streamlit dashboards
python codex_system_launcher.py  # System-level operations
```

**Suite Launcher** (Interactive menu):
```bash
cd codex-suite && python launcher.py  # Interactive menu for multiple apps
```

### Running Locally

**Python Dashboards:**
```bash
# CRITICAL: Always configure Python environment first
# Use configure_python_environment tool before running
streamlit run codex_dashboard.py --server.port 8501

# Check Python environment details with get_python_environment_details
```

**Next.js Frontend:**
```bash
cd frontend  # or web/ or frontend-vite/
npm install
npm run dev  # Development server on http://localhost:3000
npm run build  # Static export for production (outputs to out/)
```

**FastAPI Services:**
```bash
cd backend  # or api/
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

**Full Stack (Docker):**
```bash
docker-compose -f docker-compose.production.yml up -d
# Services exposed:
# - dashboard: 3000, api-gateway: 8080
# - stockanalytics: 8515, analytics: 8516
# - Additional dashboards: 8517+
```

**View logs:**
```bash
docker-compose -f docker-compose.production.yml logs -f [service-name]
docker ps  # Check running containers
```

### Master Dashboard Ultimate

**Primary Web Interface** (Flask-based, 2,187 lines, 52+ integrated dashboards):
```powershell
# Quick launch
.\START_DASHBOARD.ps1

# Or directly
python flask_dashboard.py
```

Access at: http://localhost:5000

**Integrated Features**:
- 🏠 Home - System overview
- 🤖 AI Agents - Jermaine Super Action AI, .300 Action AI, Algorithm AI
- 📱 Social Media - YouTube, TikTok, Instagram, Facebook, Pinterest, Threads
- 💰 Revenue - Treasury tracking ($95k/month target)
- 🛒 E-Commerce - WooCommerce integration
- 📚 Copilot - AI instruction management (loads Copilot-instruction.md)
- 👤 Avatar - Digital identity system
- 🤝 Council - Governance & approval system

**Key Advantage**: No Streamlit platform compatibility issues - works with any Python version.

### Testing

- **JavaScript/TypeScript**: `npm test` (Jest, maxWorkers=50%)
- **Python**: Tests in `tests/` directories (unit, integration)
- No unified test command - run per-language/framework

### Deployment

**Production Status**: LIVE on Azure (as of December 2025)
- **Frontend**: https://happy-flower-0e39c5c0f-preview.eastus2.3.azurestaticapps.net (Auto SSL)
- **Backend API**: http://codex-api.eastus.azurecontainer.io:8001
- **Deployment Token**: Stored in GitHub secrets (`AZURE_STATIC_WEB_APPS_API_TOKEN`)
- **Monthly Cost**: ~$14-20 (Azure Container Instance + Static Web App)

**Critical**: This project has 50+ GitHub Actions workflows. Key workflows:
- `azure-static-web-apps-yellow-tree-0ed102210.yml` - Frontend deployment (auto SSL)
- `azure-backend-deploy.yml` - Backend Container Instance deployment
- `deploy-complete-frontend.yml` - Complete Next.js to Azure Static Web Apps
- `deploy-backend.yml`, `backend-deploy.yml` - API services
- Multi-cloud workflows for GCP, IONOS, Azure
- Security scanning with Trivy integrated into deployment pipelines

**Common deployment commands:**
```powershell
# Windows PowerShell scripts at root:
.\deploy-codex.ps1              # Unified deployment script (WSL or Git Bash wrapper)
.\deploy-azure-production.ps1   # Azure-specific deployment
.\deploy-ionos-production.ps1   # IONOS VPS deployment

# Bash alternatives:
bash deploy-ionos.sh            # Direct IONOS deployment
bash deploy-gcp.sh              # GCP deployment
bash quick-deploy.sh            # Interactive setup with connection testing
```

**Azure Tasks**: VS Code tasks available for Azure Functions development:
- `func: host start` - Start Azure Functions host (depends on pip install task)
- Located in workspace root (no recent_uploads/configs directory)

### Service Management

Windows service scripts (PowerShell): `*-service-manager.ps1`, `systemctl-win.ps1`
Linux systemd units: `.service` and `.timer` files at root

## Project-Specific Conventions

### Ceremonial Behavioral Guidelines

When working with this codebase, maintain ceremonial standards:
- **Always Do**: Use dignified language, think revenue impact, integrate systems, be proactive
- **Never Do**: Avoid redundancy, hesitation, vague recommendations, working in silos
- **Tone**: Ceremonial clarity with flame metaphors and seasonal awareness
- **Authority Levels**:
  - Level 1: Data retrieval, analytics, navigation (execute immediately)
  - Level 2: Optimization, configuration, automation (suggest & confirm)
  - Level 3: Strategic planning only for finance, legal, architecture (escalate)

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
# Loading ledger (standard pattern across all dashboards):
import json
from datetime import datetime

def load_ledger():
    """Standard ledger loading pattern - see codex_dashboard.py"""
    with open("codex_ledger.json", "r") as f:
        return json.load(f)

# Updating ledger with proper metadata:
data = load_ledger()
data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
with open("codex_ledger.json", "w") as f:
    json.dump(data, f, indent=2)

# Safe execution wrapper (common pattern):
def safe_execute(func, *args, **kwargs):
    """Execute function with error handling - see codex_dashboard.py"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None
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

## Python Development Patterns

### Streamlit Dashboard Structure
All dashboards follow a consistent pattern (see `codex_dashboard.py` as reference):
```python
import streamlit as st
import json
from datetime import datetime

LEDGER_PATH = "codex_ledger.json"

def load_ledger():
    """Standard ledger loading"""
    with open(LEDGER_PATH, "r") as f:
        return json.load(f)

def apply_cosmic_styling():
    """Apply ceremonial styling with st.markdown"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7f1e3 0%, #efe7d4 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard Name", layout="wide")
    apply_cosmic_styling()
    # Dashboard logic here
```

### Common Dashboard Patterns
- **Caching**: Use `@st.cache_data(ttl=300)` for expensive operations
- **Session state**: Store state in `st.session_state`
- **Error handling**: Wrap operations with `safe_execute()` helper
- **Styling**: Use `apply_cosmic_styling()` for consistent look
- **Metrics**: Display with custom CSS `.metric-card` class

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

1. **Ceremonial naming**: Don't refactor `*_PROCLAMATION.md` or ledger terminology without understanding impact - these are part of the governance/branding system
2. **JSON ledgers are source of truth**: Not a traditional database - many scripts depend on exact schema. Always update `meta.last_updated` with ISO 8601 + 'Z' suffix
3. **Multi-language**: Python and TypeScript coexist - use appropriate tooling per file type. Node.js 18+, Python 3.10+ required
4. **Port management**: 20+ services can run simultaneously - track port allocations:
   - **5000: Master Dashboard Ultimate (Flask) - PRIMARY INTERFACE**
   - 3000: Next.js dashboard (secondary)
   - 5555: Working dashboard (development)
   - 8080: API Gateway
   - 8501-8502: Production/Staging Streamlit
   - 8515-8517+: Various specialized dashboards
5. **Windows paths**: Use backslashes in PowerShell, forward slashes in WSL/Git Bash
6. **Azure Functions require Python 3.9**: Check `app.yaml` runtime version for GCP deployment
7. **No single entry point**: Multiple launcher scripts (`launch*.py`, `*.ps1`) - choose correct one for context:
   - `codex_unified_launcher.py` - Treasury, dawn dispatch, system operations (primary CLI)
   - `launch.py` - Quick Streamlit dashboard launcher
   - `codex_system_launcher.py` - System-level operations
   - `codex-suite/launcher.py` - Interactive menu for suite apps
8. **Duplicate directories**: `codexdominion-schemas/` and `codexdominion-clean/` contain archived copies - **always work in root directory**
9. **Workflow count**: 50+ GitHub Actions workflows in `.github/workflows/` - key ones are:
   - `azure-static-web-apps-yellow-tree-0ed102210.yml` - Azure Static Web Apps (PRIMARY)
   - `azure-backend-deploy.yml` - Backend Container Instance (LIVE)
   - `deploy-complete-frontend.yml` - Next.js to Azure Static Web Apps
   - `deploy-backend.yml`, `backend-deploy.yml` - API services
   - `super-action-ai-deployment.yaml`, `super-action-ai.yaml` - AI-powered deployments
10. **Static export mode**: Next.js uses static export (`output: 'export'`) - no API routes, only client-side or external API calls
11. **Streamlit port conflicts**: Multiple dashboards may conflict - use `--server.port` flag to specify unique ports
12. **Docker image naming**: Images prefixed with `jmerritt48/*` on Docker Hub (e.g., `jmerritt48/codex-dashboard:latest`)
