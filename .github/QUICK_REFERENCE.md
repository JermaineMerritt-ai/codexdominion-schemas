# Codex Dominion - Quick Reference (AI Agent Cheat Sheet)

**Last Updated**: December 25, 2025

## 🚨 CRITICAL FIRST STEP
```powershell
.venv\Scripts\activate.ps1     # Windows - ALWAYS DO THIS FIRST
```

## 🔥 Most Common Operations

### View Dashboards
```powershell
.\START_DASHBOARD.ps1           # Primary Flask dashboard (port 5000)
```

### Backend Operations
```bash
python codex_unified_launcher.py treasury summary --days 30
python codex_unified_launcher.py dawn dispatch
python codex_unified_launcher.py status
```

### Database Operations
```python
from db import SessionLocal
session = SessionLocal()
try:
    # Your database operations
    session.commit()
finally:
    session.close()  # CRITICAL
```

### Load JSON (Flask)
```python
from flask_dashboard import load_json
data = load_json("cycles.json")  # Never fails, returns {} on error
```

### Next.js Development
```bash
cd dashboard-app
npm run dev                     # Port 3000
```

## 📂 File Locations Quick Lookup

| Need | Location |
|------|----------|
| Database models | `models.py` (root) |
| Database connection | `db.py` or `database.py` |
| Main Flask app | `flask_dashboard.py` |
| Workflow engine | `workflow_engine.py` |
| Treasury ops | `codex_treasury_database.py` |
| CLI launcher | `codex_unified_launcher.py` |
| Next.js design | `dashboard-app/lib/design-system.ts` |
| Config files | `*_config.json` |
| State ledger | `codex_ledger.json` |

## 🔧 Common Patterns

### Database Session Pattern
```python
from db import SessionLocal
session = SessionLocal()
try:
    result = session.query(Model).filter_by(id=id).first()
    session.commit()
finally:
    session.close()
```

### Workflow Creation
```python
from workflow_engine import workflow_engine
workflow_id = workflow_engine.create_workflow(
    workflow_type_id="store_creation",
    created_by_agent="agent_jermaine",
    inputs={"domain": "example.com"},
    auto_execute=True
)
```

### Next.js API Call
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";
const res = await fetch(`${API_BASE}/api/endpoint`, { cache: "no-store" });
```

## ⚡ Quick Decisions

**Need to display data?**
- Web UI → Flask Dashboard (port 5000) or Next.js (dashboard-app/)
- CLI → `codex_unified_launcher.py`

**Need to store data?**
- Structured (workflows, agents) → PostgreSQL (`models.py`)
- Config/state → JSON ledgers (`codex_ledger.json`, `*_config.json`)

**Which launcher?**
```
Dashboard viewing → START_DASHBOARD.ps1 (port 5000)
Treasury/backend → codex_unified_launcher.py
Testing Streamlit → python launch.py
Deployment → deploy-azure-production.ps1 or deploy-ionos.sh
```

## 🚫 Common Mistakes to Avoid

| DON'T | DO |
|-------|-----|
| `with open("file.json")` in Flask | `load_json("file.json")` |
| Leave DB session open | Use try/finally to close |
| Work in `codexdominion-schemas/` | Work in root directory |
| Use raw `python` commands | Activate `.venv` first |
| Direct `open()` for JSON | Use `load_json()` helper |
| Forget to close sessions | ALWAYS close DB sessions |

## 📊 Port Reference

| Service | Port |
|---------|------|
| Flask Master Dashboard | 5000 |
| Next.js Main | 3000 |
| Streamlit Production | 8501-8502 |
| API Gateway | 8080 |

## 🔑 Key Environment Variables

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

## 🆘 Emergency Commands

```bash
# Check what's using a port (Windows)
netstat -ano | findstr :5000

# Kill a process
taskkill /PID <process_id> /F

# Database health check
python -c "from db import SessionLocal; s=SessionLocal(); print('✅ OK'); s.close()"

# Redis health check
redis-cli ping  # Should return PONG
```

## 📚 Full Documentation
See `copilot-instructions.md` for complete details (14,570 lines)

---

**🔥 The Flame Burns Sovereign and Eternal!** 👑
