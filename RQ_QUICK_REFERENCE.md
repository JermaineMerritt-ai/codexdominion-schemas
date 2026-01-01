# 🎯 RQ Quick Reference Card

## Start Services (3 Terminals)

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Flask
python flask_dashboard.py

# Terminal 3: RQ Worker
.\START_RQ_WORKER.ps1
```

## Test Workflow Enqueue

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_jermaine_super_action",
    "mode": "execute",
    "context": {
      "workflow_type": "customer_followup",
      "calculator_inputs": {
        "tasks_per_week": 20,
        "time_per_task_minutes": 5,
        "hourly_wage": 25,
        "automation_percent": 80
      }
    }
  }'
```

## Common Commands

```bash
# Check queue status
rq info --url redis://localhost:6379/0

# Empty queue
rq empty workflows --url redis://localhost:6379/0

# Start multiple workers
rq worker workflows --name worker1
rq worker workflows --name worker2

# Start RQ Dashboard
pip install rq-dashboard
rq-dashboard --port 9181
```

## Environment Variables

```env
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/codexdominion
```

## File Locations

| File | Purpose |
|------|---------|
| `flask_dashboard.py` | Main app (enqueues jobs) |
| `worker_tasks.py` | Worker functions |
| `START_RQ_WORKER.ps1` | Launch script |
| `RQ_INTEGRATION_GUIDE.md` | Full documentation |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Redis connection failed | `redis-server` |
| Worker not picking up jobs | Check queue name: `rq worker workflows` |
| Import errors | Activate venv: `.venv\Scripts\activate.ps1` |
| Jobs stuck | Check worker logs for errors |

## Key Functions (worker_tasks.py)

- `execute_workflow(workflow_id)` - Main executor
- `cleanup_old_workflows(days=30)` - Maintenance
- `generate_weekly_report()` - Analytics

## Expected Output

**Flask Console:**
```
✅ Enqueued workflow action_123 to background queue (Job ID: abc)
```

**Worker Console:**
```
🚀 Starting workflow execution: action_123
✅ Workflow action_123 completed in 2.05s
💰 Estimated savings: $166.67/week
```

---

🔥 **Status:** Production Ready | 🚀 **Phase:** 2/6 Complete
