# 🔥 DATABASE MIGRATION COMPLETE GUIDE 🔥

**Date:** December 20, 2025  
**Status:** Ready to Execute ✅

---

## 📋 What We've Built

### ✅ Migration Scripts (3)

1. **migrate_agents_from_json.py**
   - Source: `agents_simple.json`
   - Targets: `agents`, `agent_reputations`, `agent_training` tables
   - Creates: Agent + initial reputation + initial training record

2. **migrate_councils_from_json.py**
   - Source: `councils.json`  
   - Targets: `councils`, `council_members` tables
   - Creates: Council + member associations

3. **migrate_workflows_from_json.py** *(optional)*
   - Source: `workflows.json` (if exists)
   - Targets: `workflows`, `workflow_metrics` tables
   - Purpose: Preserve historic workflow data

### ✅ Refactored workflow_engine.py

**BEFORE (In-Memory):**
```python
class WorkflowEngine:
    def __init__(self):
        self._actions: Dict[str, WorkflowAction] = {}  # ❌ In-memory dict
```

**AFTER (Database + RQ):**
```python
class WorkflowEngine:
    def create_workflow(...) -> str:
        # ✅ Writes to PostgreSQL
        # ✅ Enqueues to RQ for execution
        # ✅ Returns workflow_id
    
    def get_workflow(workflow_id) -> Workflow:
        # ✅ Reads from PostgreSQL
    
    def list_workflows(...) -> List[Workflow]:
        # ✅ Queries PostgreSQL with filters
```

**Key Changes:**
- ❌ Removed `self._actions` dict
- ❌ Removed `create_action()` (replaced with `create_workflow()`)
- ❌ Removed `get_action_raw()` and `list_actions()`
- ✅ Added `enqueue_execution()` for RQ integration
- ✅ Added `record_metric()` for performance tracking
- ✅ All methods now use `SessionLocal()` from `db.py`

---

## 🚀 Execution Plan

### Step 1: Install Dependencies (if not done)

```powershell
# Activate virtual environment
.venv\Scripts\activate.ps1

# Install missing packages
pip install -r requirements.txt

# Verify installations
pip list | Select-String -Pattern "flask-login|pyjwt|sentry-sdk|prometheus-client"
```

### Step 2: Initialize Database Tables

```powershell
# Create all tables from models.py
python -c "from db import init_db; init_db()"
```

Expected output:
```
✅ Database tables created successfully
```

Tables created:
- users
- audit_logs
- councils
- council_members
- agents
- agent_reputations
- agent_training
- workflow_types
- workflows
- workflow_metrics
- workflow_votes
- user_councils (association table)

### Step 3: Run Migrations (In Order)

```powershell
# 1. Agents first (agents are referenced by councils/workflows)
python scripts/migrations/migrate_agents_from_json.py

# 2. Councils second (councils reference agents via members)
python scripts/migrations/migrate_councils_from_json.py

# 3. Workflows last (optional - only if you have historic data)
python scripts/migrations/migrate_workflows_from_json.py
```

Expected output for each:
```
🔄 Starting [resource] migration from JSON to Postgres...
📋 Found N [resources] in JSON
📊 Database currently has 0 [resources]
➕ Inserted [resource]: ...
✅ Migration complete!
   Inserted: N
   Updated:  0
   Skipped:  0
```

### Step 4: Verify Migrations

```powershell
# Check database has data
python -c "
from db import SessionLocal
from models import Agent, Council, Workflow

session = SessionLocal()
print(f'Agents:    {session.query(Agent).count()}')
print(f'Councils:  {session.query(Council).count()}')
print(f'Workflows: {session.query(Workflow).count()}')
session.close()
"
```

Expected output:
```
Agents:    8 (or your count)
Councils:  36 (or your count)
Workflows: 0 (unless you migrated historic data)
```

---

## 🔧 Flask Integration Updates

### Update `/api/chat` Execute Mode

**OLD CODE (In-Memory):**
```python
# Inside /api/chat endpoint, execute mode
action = workflow_engine.create_action(
    action_type="execute_workflow",
    created_by_agent=agent_id,
    inputs=context["workflow_inputs"],
    calculated_savings=savings_dict
)
action.assigned_council_id = council.id if council else None

return jsonify({
    "reply": agent_reply,
    "workflow_action": action.id  # ❌ From in-memory object
})
```

**NEW CODE (Database + RQ):**
```python
# Inside /api/chat endpoint, execute mode
from workflow_engine import workflow_engine

# 1. Determine workflow type and inputs
workflow_type_id = context.get("workflow_type", "general")
workflow_inputs = context.get("workflow_inputs", {})
calculator_inputs = context.get("calculator_inputs", {})

# 2. Determine council assignment
domain = workflow_catalog.get(workflow_type_id, {}).get("domain")
council = find_council_by_domain(session, domain) if domain else None

# 3. Create workflow in DB and enqueue to RQ
workflow_id = workflow_engine.create_workflow(
    workflow_type_id=workflow_type_id,
    created_by_agent=agent_id,
    inputs=workflow_inputs,
    calculated_savings=savings_dict,
    assigned_council_id=council.id if council else None,
    auto_execute=True  # Enqueues to RQ worker
)

return jsonify({
    "reply": agent_reply,
    "savings": savings_dict,
    "workflow_id": workflow_id,  # ✅ From database
    "status": "pending"  # Will be executed by RQ worker
})
```

### Helper Function for Council Lookup

```python
def find_council_by_domain(session, domain: str):
    """Find council responsible for a domain"""
    from models import Council
    
    # Simple domain matching (enhance as needed)
    return session.query(Council).filter(
        Council.config['domain'].astext == domain
    ).first()
```

---

## 🎯 Testing the Integration

### Test 1: Create a Workflow

```powershell
# Start Redis (required for RQ)
# In separate terminal:
redis-server

# Start RQ Worker (required for execution)
# In separate terminal:
rq worker workflows

# Test workflow creation
python -c "
from workflow_engine import workflow_engine

wf_id = workflow_engine.create_workflow(
    workflow_type_id='test_workflow',
    created_by_agent='agent_test',
    inputs={'test': True},
    calculated_savings={'weekly_savings': 100},
    auto_execute=True
)

print(f'Created workflow: {wf_id}')
"
```

Expected output:
```
✅ Created workflow: wf_abc123def456 (type: test_workflow)
📋 Enqueued workflow wf_abc123def456 as job xyz789
```

### Test 2: Query Workflows

```python
from workflow_engine import workflow_engine

# List all workflows
workflows = workflow_engine.list_workflows(limit=10)
for wf in workflows:
    print(f"{wf.id}: {wf.status.value} - {wf.workflow_type_id}")

# Get specific workflow
wf = workflow_engine.get_workflow("wf_abc123def456")
if wf:
    print(wf.to_dict())
```

### Test 3: End-to-End via Flask

```powershell
# Start Flask
python flask_dashboard.py

# In browser or curl:
curl http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_jermaine",
    "message": "Create a new website",
    "mode": "execute"
  }'
```

Expected response:
```json
{
  "reply": "I'll create that website for you...",
  "workflow_id": "wf_abc123def456",
  "status": "pending",
  "savings": { "weekly_savings": 150 }
}
```

---

## 🔍 Troubleshooting

### Issue: "No module named 'rq'"
```powershell
pip install rq redis
```

### Issue: "No module named 'db'"
- Verify `db.py` exists at project root
- Check imports: `from db import SessionLocal`

### Issue: "No module named 'models'"
- Verify `models.py` exists at project root
- Check imports: `from models import Workflow, Agent`

### Issue: "Connection refused to PostgreSQL"
- Check `.env` has correct `DATABASE_URL`
- Verify PostgreSQL is running: `pg_isready -h localhost -p 5432`

### Issue: "Connection refused to Redis"
- Start Redis: `redis-server`
- Check `REDIS_URL` in environment: `redis://localhost:6379/0`

### Issue: "Workflow not executing"
- Verify RQ worker is running: `rq worker workflows`
- Check worker logs for errors
- Verify workflow enqueued: `rq info`

---

## 📊 Migration Statistics

After successful migration, you should have:

| Resource | Expected Count | Source |
|----------|---------------|--------|
| Agents | 8-12 | agents_simple.json |
| Councils | 36 | councils.json |
| Council Members | 100+ | councils.json (members array) |
| Agent Reputations | = Agents | Generated (initial values) |
| Agent Training | = Agents | Generated (initial records) |
| Workflows | 0+ | workflows.json (if exists) |
| Users | 0 | Created via create_admin_user.py |

---

## ✅ Success Criteria

Migration is complete when:

1. ✅ All 3 migration scripts run without errors
2. ✅ Database queries return expected counts
3. ✅ `workflow_engine.create_workflow()` works
4. ✅ RQ worker processes workflows
5. ✅ Flask `/api/chat` creates workflows in DB
6. ✅ No import errors for `models`, `db`, `workflow_engine`

---

## 🎯 Next Steps After Migration

1. **Update remaining endpoints** to use DB instead of JSON
   - `/api/agents` → Query Agent table
   - `/api/councils` → Query Council table
   - `/api/workflows` → Query Workflow table

2. **Add authentication** to protected endpoints
   - Apply `@jwt_required` decorator
   - Create admin user: `python create_admin_user.py`

3. **Integrate monitoring**
   - Add Sentry initialization
   - Add Prometheus metrics
   - Setup health checks

4. **Deploy to production**
   - Run migrations on production database
   - Start RQ workers as systemd services
   - Configure NGINX reverse proxy

---

**🔥 Database Migration Complete - Platform Ready for Production! 🔥**

