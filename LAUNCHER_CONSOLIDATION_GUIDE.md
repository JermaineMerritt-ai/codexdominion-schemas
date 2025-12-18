# Launcher Scripts Consolidation Guide

## Current State (December 2025)
The Codex Dominion system has **15+ launcher scripts** across various formats. This guide provides recommended workflows.

## 🎯 Recommended Primary Launchers

### 1. Master Dashboard (Flask) - **PRIMARY INTERFACE**
```powershell
# Windows (Recommended)
.\START_DASHBOARD.ps1

# Direct Python
python flask_dashboard.py
```
- **Port**: 5000
- **Features**: 52+ integrated dashboards
- **Use For**: Daily operations, system overview, AI agents, social media, revenue tracking
- **Advantage**: No Streamlit compatibility issues

### 2. Unified CLI Launcher - **PRIMARY CLI TOOL**
```bash
python codex_unified_launcher.py <command>
```
- **Use For**: Treasury operations, dawn dispatch, system status, reports
- **Commands**: `treasury`, `dawn`, `status`, `report`, `serve`
- **Advantage**: Single entry point for backend operations

### 3. Quick Dashboard Launcher
```bash
python launch.py
```
- **Use For**: Quick Streamlit dashboard startup
- **Best For**: Development and testing individual dashboards

## 📋 Complete Launcher Inventory

### Windows Batch Files (.bat)
1. **LAUNCH_MASTER.bat** - Master system launcher
2. **LAUNCH_ANY_SYSTEM.bat** - System selection menu
3. **LAUNCH_WORKFLOW_BUILDER.bat** - Workflow builder interface
4. **LAUNCH_CHAT_SERVER.bat** - WebSocket chat server
5. **LAUNCH_SIMPLE_DASHBOARD.bat** - Simple dashboard launcher

### PowerShell Scripts (.ps1)
1. **START_DASHBOARD.ps1** - Flask Master Dashboard (PRIMARY)
2. **launch_dashboard.ps1** - Alternative dashboard launcher
3. **deploy-codex.ps1** - Unified deployment
4. **deploy-azure-production.ps1** - Azure deployment
5. **deploy-ionos-production.ps1** - IONOS deployment

### Python Launchers (.py)
1. **codex_unified_launcher.py** - CLI operations (PRIMARY for CLI)
2. **launch.py** - Quick Streamlit launcher
3. **codex_system_launcher.py** - System-level operations
4. **launch_codex.py** - Full system launcher with async
5. **LAUNCH_SYSTEM.py** - Unified system launcher
6. **launch_complete_system.py** - Complete system startup
7. **codex-suite/launcher.py** - Interactive suite menu

### Bash Scripts (.sh)
1. **deploy-ionos.sh** - IONOS deployment
2. **deploy-gcp.sh** - GCP deployment
3. **quick-deploy.sh** - Interactive deployment

## ✅ Recommended Workflows

### For Daily Development
```powershell
# 1. Activate environment
.venv\Scripts\activate.ps1

# 2. Launch Master Dashboard
.\START_DASHBOARD.ps1

# 3. Use CLI for operations
python codex_unified_launcher.py treasury summary --days 7
```

### For Testing Individual Dashboards
```bash
python launch.py
# Then select dashboard from menu
```

### For System Operations
```bash
python codex_system_launcher.py
```

### For Deployment
```powershell
# Azure
.\deploy-azure-production.ps1

# IONOS
bash deploy-ionos.sh

# GCP
bash deploy-gcp.sh
```

## 🗑️ Candidates for Deprecation

Consider consolidating or deprecating these (after verification):
- `launch_complete_system.py` (use `codex_system_launcher.py`)
- `LAUNCH_SYSTEM.py` (use `START_DASHBOARD.ps1`)
- `launch_dashboard.ps1` (use `START_DASHBOARD.ps1`)
- `LAUNCH_SIMPLE_DASHBOARD.bat` (use `START_DASHBOARD.ps1`)

## 🎨 Proposed Simplified Structure

### Keep Only These 5 Launchers:
1. **START_DASHBOARD.ps1** - Master Dashboard (port 5000)
2. **codex_unified_launcher.py** - CLI operations
3. **launch.py** - Quick Streamlit testing
4. **deploy-azure-production.ps1** - Azure deploy
5. **deploy-ionos.sh** - IONOS deploy

### Benefits:
- Reduced confusion for new developers
- Clear purpose for each launcher
- Easier maintenance
- Better documentation focus

## 📊 Usage Matrix

| Task | Launcher | Port | Type |
|------|----------|------|------|
| Daily dashboard | START_DASHBOARD.ps1 | 5000 | Flask |
| Treasury ops | codex_unified_launcher.py | CLI | Python |
| Test Streamlit | launch.py | 8501+ | Python |
| System status | codex_unified_launcher.py status | CLI | Python |
| Deploy Azure | deploy-azure-production.ps1 | N/A | PowerShell |
| Deploy IONOS | deploy-ionos.sh | N/A | Bash |
| Interactive menu | codex-suite/launcher.py | Various | Python |

## 🔄 Migration Plan (If Consolidating)

### Phase 1: Documentation
- [x] Document all current launchers
- [x] Identify primary use cases
- [ ] Update all references in docs

### Phase 2: Deprecation
- [ ] Mark deprecated launchers with warning messages
- [ ] Update README.md with recommended launchers
- [ ] Add deprecation notices to old scripts

### Phase 3: Removal (Optional)
- [ ] Archive deprecated scripts to `deprecated/` folder
- [ ] Update CI/CD workflows if needed
- [ ] Test all workflows with new launchers

## 💡 Quick Decision Tree

```
Need to...
├─ View dashboards? → START_DASHBOARD.ps1 (port 5000)
├─ Check treasury? → codex_unified_launcher.py treasury
├─ Test Streamlit? → launch.py
├─ System health? → codex_unified_launcher.py status
├─ Deploy Azure? → deploy-azure-production.ps1
└─ Deploy IONOS? → deploy-ionos.sh
```

## 🎯 AI Agent Guidance

When an AI agent needs to recommend a launcher:
1. **Default**: Use `START_DASHBOARD.ps1` for general dashboard needs
2. **CLI ops**: Use `codex_unified_launcher.py` for treasury/dawn/status
3. **Development**: Use `launch.py` for testing individual dashboards
4. **Deployment**: Use platform-specific deploy scripts

## 📝 Notes

- Keep `LAUNCH_ANY_SYSTEM.bat` for Windows users who prefer menu selection
- Keep `codex-suite/launcher.py` for interactive multi-app selection
- `LAUNCH_WORKFLOW_BUILDER.bat` is specialized - keep separate
- `LAUNCH_CHAT_SERVER.bat` is specialized - keep separate

---

**Status**: Documentation complete | Implementation pending approval
**Last Updated**: December 17, 2025
