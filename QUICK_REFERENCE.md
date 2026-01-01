# Codex Dominion - Quick Reference Guide

**⚡ For Immediate AI Agent Onboarding**

## 1️⃣ Activate Environment FIRST
```powershell
.venv\Scripts\activate.ps1  # Windows - ALWAYS DO THIS FIRST
```

## 2️⃣ Launch Primary Interface
```powershell
.\START_DASHBOARD.ps1       # Flask dashboard → http://localhost:5000
```

## 3️⃣ Core Patterns (Copy-Paste Ready)

### Database Session (ALWAYS use try/finally)
```python
from db import SessionLocal
session = SessionLocal()
try:
    result = session.query(Model).filter_by(id=id).first()
    session.commit()
finally:
    session.close()  # CRITICAL: Prevents pool exhaustion
```

### JSON Loading (Flask - Never fails)
```python
from flask_dashboard import load_json
data = load_json("cycles.json")  # Returns {} on error, never None
```

### Workflow Creation (Auto-routes to councils)
```python
from workflow_engine import workflow_engine
workflow_id = workflow_engine.create_workflow(
    workflow_type_id="store_creation",
    created_by_agent="agent_jermaine",
    inputs={"domain": "mystore.com"},
    auto_execute=True
)
```

## 4️⃣ Quick Decision Tree
- **View dashboards?** → `START_DASHBOARD.ps1` (port 5000)
- **CLI operations?** → `python codex_unified_launcher.py <command>`
- **Test Streamlit?** → `python launch.py`
- **Deploy Azure?** → `.\deploy-azure-production.ps1`
- **Deploy IONOS?** → `bash deploy-ionos.sh`

## 5️⃣ Critical Files
- `flask_dashboard.py` - Master dashboard (20K+ lines, PRIMARY)
- `workflow_engine.py` - Database-backed workflows (NO in-memory storage)
- `db.py` / `models.py` - SQLAlchemy ORM (PostgreSQL)
- `codex_ledger.json` - JSON state store

## 6️⃣ Emergency Troubleshooting
```powershell
# Check venv active
echo $env:VIRTUAL_ENV  # Should show path to .venv

# Test database
python -c "from db import SessionLocal; s=SessionLocal(); print('✅ DB OK'); s.close()"

# Test Redis (required for workflows)
redis-cli ping  # Should return PONG

# View system status
python codex_unified_launcher.py status
```

## 📚 Full Documentation
See `.github/copilot-instructions.md` (14,570 lines) for complete reference.
