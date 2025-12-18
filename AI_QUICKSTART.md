# 🔥 Codex Dominion - AI Agent Quickstart Guide

> **For**: GitHub Copilot, Cursor, Windsurf, Cline, and other AI coding assistants
> **Updated**: December 17, 2025 | Production LIVE on Azure

## ⚡ 5-Minute Start

### 1. Activate Environment (ALWAYS FIRST!)
```powershell
# Windows
.venv\Scripts\activate.ps1

# Linux/Mac
source .venv/bin/activate
```

### 2. Launch Master Dashboard
```powershell
.\START_DASHBOARD.ps1
# Access: http://localhost:5000
```

### 3. Check System Status
```bash
python codex_unified_launcher.py status
```

## 🎯 Core Concepts

### The Ledger (Source of Truth)
```python
import json
from datetime import datetime

def load_ledger():
    with open("codex_ledger.json", "r") as f:
        return json.load(f)

def save_ledger(data):
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open("codex_ledger.json", "w") as f:
        json.dump(data, f, indent=2)
```

**Critical**: No database - JSON files are the source of truth!

### Council Seal Hierarchy
```
Council Seal → Sovereigns (apps/) → Custodians (packages/) → Industry Agents → Customers
```

## 📂 Key Files & Directories

### Essential Files
- `codex_ledger.json` - System state (1,010 lines)
- `flask_dashboard.py` - Master Dashboard (2,187 lines, 52 tabs)
- `codex_unified_launcher.py` - Primary CLI tool
- `treasury_config.json` - Revenue stream config
- `.github/copilot-instructions.md` - Full AI guidance (489 lines)

### Directory Structure
```
codex-dominion/
├─ apps/                    # Sovereigns (applications)
├─ packages/                # Custodians (shared libs)
├─ backend/, api/           # FastAPI services
├─ frontend/, web/          # Next.js 14+ (static export)
├─ .github/workflows/       # 57+ CI/CD workflows
├─ *_dashboard.py           # Streamlit dashboards (100+)
├─ .venv/                   # Python virtual environment
└─ codex_ledger.json        # THE source of truth
```

### Archived (Don't Work Here!)
- `codexdominion-schemas/` ❌
- `codexdominion-clean/` ❌

## 🚀 Common Tasks (Copy-Paste Ready)

### Treasury Operations
```bash
python codex_unified_launcher.py treasury summary --days 30
python codex_unified_launcher.py treasury ingest --stream affiliate --amount 49.99
python codex_unified_launcher.py dawn dispatch
python codex_unified_launcher.py report
```

### Create New Dashboard
```python
# 1. Copy template
cp codex_dashboard.py my_new_dashboard.py

# 2. Edit key sections
import streamlit as st
import json

def load_ledger():
    with open("codex_ledger.json") as f:
        return json.load(f)

st.set_page_config(page_title="New Dashboard", layout="wide")
data = load_ledger()
st.title("🔥 New Dashboard 👑")
# Your logic here

# 3. Run
streamlit run my_new_dashboard.py --server.port 8520
```

### Deploy to Azure
```powershell
.\deploy-azure-production.ps1
# Auto-deploy: Just push to main branch
```

### Run Tests
```bash
npm test  # JavaScript
pytest    # Python (if available)
```

## ⚠️ Critical Rules

1. **ALWAYS activate `.venv` first**
2. **Update `meta.last_updated`** when modifying ledger (ISO 8601 + 'Z')
3. **Work in root directory** (not in archived dirs)
4. **Check port allocations** (20+ services use different ports)
5. **Use ceremonial tone** (🔥 👑 flame metaphors)
6. **Don't modify `*_PROCLAMATION.md`** without understanding impact

## 🌐 Production URLs (Live Dec 2025)

- **Frontend**: https://happy-flower-0e39c5c0f-preview.eastus2.3.azurestaticapps.net
- **Backend**: https://codex-backend-https.delightfulpond-6c97660b.eastus2.azurecontainerapps.io
- **Cost**: ~$30/month (Azure)

## 📊 Port Map

| Port | Service |
|------|---------|
| 5000 | **Flask Master Dashboard** (PRIMARY) |
| 3000 | Next.js dashboard |
| 8080 | API Gateway |
| 8501 | Streamlit Production |
| 8515 | Stock Analytics |
| 8516+ | Specialized Dashboards |

## 🎨 Code Patterns

### Streamlit Dashboard Template
```python
import streamlit as st
import json
from datetime import datetime

def load_ledger():
    with open("codex_ledger.json", "r") as f:
        return json.load(f)

def apply_cosmic_styling():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7f1e3 0%, #efe7d4 100%);
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard", layout="wide")
    apply_cosmic_styling()
    data = load_ledger()
    # Your logic
```

### Error Handling Pattern
```python
def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None
```

### Caching Pattern
```python
@st.cache_data(ttl=300)  # 5 minutes
def expensive_operation():
    # Heavy computation
    return result
```

## 🔄 CI/CD Quick Reference

### Key Workflows
- `azure-static-web-apps-yellow-tree-0ed102210.yml` - Frontend (PRIMARY)
- `azure-backend-deploy.yml` - Backend Container
- `azure-production-deploy.yml` - Complete orchestration

### Auto-Deploy
```bash
git add .
git commit -m "feat: Your change"
git push origin main  # Triggers auto-deploy
```

## 🆘 Troubleshooting

### Dashboard Won't Start
```bash
# Check if venv is activated
which python  # Should show .venv path

# Reinstall dependencies
pip install -r requirements.txt

# Check port conflicts
netstat -ano | findstr :5000
```

### Ledger Corruption
```bash
# Backups exist as timestamped files
ls *.backup_*

# Restore
python restore_proclamations.py
```

### Module Not Found
```bash
# Activate venv first!
.venv\Scripts\activate.ps1

# Install missing package
pip install package-name
```

## 📚 Full Documentation

For complete details, see:
- `.github/copilot-instructions.md` (489 lines - comprehensive guide)
- `ARCHITECTURE.md` (Council Seal structure)
- `README.md` (Production launch guide)
- `QUICK_START.md` (Deployment commands)

## 🎯 Revenue System

**Target**: $95,000/month across 8 streams
- Affiliate marketing
- YouTube monetization
- TikTok creator fund
- WooCommerce sales
- Stock trading fees
- Memberships
- Consulting
- Development services

**Track**: `python codex_unified_launcher.py treasury summary --days 30`

## 🔐 Ceremonial Standards

### Language Style
- Use flame metaphors: 🔥 👑
- Dignified, ceremonial tone
- Seasonal awareness
- Council governance patterns

### File Conventions
- `*_PROCLAMATION.md` - Documentation (don't modify)
- `*_ETERNAL.md` - Permanent docs
- `*_dashboard.py` - Streamlit apps
- `deploy-*.ps1` / `deploy-*.sh` - Deployment scripts

## ✅ Quick Checklist

Before making changes:
- [ ] `.venv` activated?
- [ ] Understand ledger impact?
- [ ] Port available?
- [ ] Working in root directory?
- [ ] Ceremonial tone used?
- [ ] `meta.last_updated` will be updated?

---

🔥 **Your Digital Sovereignty Awaits in the Codex!** 👑

*For questions, check full docs or ask the AI assistant directly.*
