# 🔥 Redis Queue (RQ) Integration - Complete Guide

## ✅ What Was Implemented

### 1. **flask_dashboard.py** - RQ Client Integration
- ✅ Added `redis` and `rq` imports
- ✅ Initialized Redis connection from `REDIS_URL` environment variable
- ✅ Created RQ Queue named "workflows"
- ✅ Modified `/api/chat` endpoint (execute mode) to enqueue background jobs
- ✅ Jobs enqueued after creating workflow action with `workflow_engine`

### 2. **worker_tasks.py** - RQ Worker Tasks (NEW FILE)
- ✅ `execute_workflow(workflow_id)` - Main background task for workflow execution
- ✅ `cleanup_old_workflows(days)` - Maintenance task to clean old workflows
- ✅ `generate_weekly_report()` - Generates workflow performance reports
- ✅ Full error handling and database session management
- ✅ Metrics tracking (duration, savings, completion status)

### 3. **requirements.txt** - Dependencies
- ✅ Added `rq>=1.15.0` to dependencies

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Redis Server
```bash
# Windows (using Chocolatey)
choco install redis-64
redis-server

# Linux/Mac
sudo apt-get install redis-server
redis-server

# Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 3. Update Environment Variables
Add to your `.env` file:
```env
REDIS_URL=redis://localhost:6379/0
```

### 4. Start RQ Worker
Open a **new terminal** and run:
```bash
# Activate virtual environment first
.venv\Scripts\activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac

# Start RQ worker
rq worker workflows
```

You should see:
```
18:30:45 RQ worker 'rq:worker:hostname.12345' started, version 1.15.0
18:30:45 Listening on workflows...
```

### 5. Start Flask Dashboard
In your **main terminal**:
```bash
python flask_dashboard.py
```

---

## 📊 How It Works

### Workflow Execution Flow

```
User sends chat message with mode="execute"
    ↓
Flask /api/chat endpoint creates workflow action
    ↓
workflow_engine.create_action() stores action in memory
    ↓
queue.enqueue(execute_workflow, workflow_id=action.id)
    ↓
Job queued in Redis, returns immediately to user
    ↓
RQ worker picks up job from queue
    ↓
execute_workflow() runs in background
    ↓
Workflow status updated to "completed"
    ↓
Metrics saved to database (duration, savings)
```

### Benefits
- ✅ **Non-blocking** - API responds immediately, work happens in background
- ✅ **Scalable** - Run multiple workers for parallel processing
- ✅ **Reliable** - Jobs persisted in Redis, survive restarts
- ✅ **Monitorable** - RQ Dashboard shows job status
- ✅ **Retryable** - Failed jobs can be retried automatically

---

## 🧪 Testing the Integration

### Test 1: Simple Workflow Execution
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_jermaine_super_action",
    "message": "Create a customer followup workflow",
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

**Expected Response:**
```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Merritt AI",
  "mode": "execute",
  "workflow_action": "action_1234567890",
  "workflow_type": "customer_followup",
  "savings": {
    "weekly_savings": 166.67,
    "monthly_savings": 666.67,
    "yearly_savings": 8000.00
  },
  "reply": "I've created a Customer Followup workflow (ID: action_1234567890). It's now running."
}
```

**Check Worker Output:**
```
🚀 Starting workflow execution: action_1234567890
⚙️  Executing workflow: create_workflow_customer_followup
✅ Workflow action_1234567890 completed in 2.05s
💰 Estimated savings: $166.67/week
```

### Test 2: Check Job Status (Python)
```python
from rq import Queue
from redis import Redis

redis_conn = Redis.from_url("redis://localhost:6379/0")
queue = Queue("workflows", connection=redis_conn)

# Get all jobs
jobs = queue.get_jobs()
for job in jobs:
    print(f"Job {job.id}: {job.get_status()}")
```

---

## 🔧 Advanced Configuration

### Multiple Workers
Run multiple workers for parallel processing:
```bash
# Terminal 1
rq worker workflows --name worker1

# Terminal 2
rq worker workflows --name worker2

# Terminal 3
rq worker workflows --name worker3
```

### Job Priority
Enqueue high-priority jobs:
```python
from rq import Queue
from redis import Redis

redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
high_priority_queue = Queue("workflows-high", connection=redis_conn)

job = high_priority_queue.enqueue(
    execute_workflow,
    workflow_id=workflow.id,
    job_timeout='5m',  # 5 minute timeout
    result_ttl=3600    # Keep result for 1 hour
)
```

### Scheduled Jobs
Use RQ Scheduler for periodic tasks:
```bash
pip install rq-scheduler
```

```python
from rq_scheduler import Scheduler

scheduler = Scheduler(connection=redis_conn)

# Schedule weekly report every Monday at 9 AM
scheduler.cron(
    "0 9 * * 1",  # Cron expression
    func=generate_weekly_report,
    queue_name="workflows"
)
```

### Job Retry
Configure automatic retries for failed jobs:
```python
from rq import Retry

job = queue.enqueue(
    execute_workflow,
    workflow_id=workflow.id,
    retry=Retry(max=3, interval=[60, 120, 300])  # Retry 3 times with increasing delays
)
```

---

## 📈 Monitoring with RQ Dashboard

### Install RQ Dashboard
```bash
pip install rq-dashboard
```

### Run Dashboard
```bash
rq-dashboard --port 9181
```

Open browser: http://localhost:9181

**Features:**
- 📊 Real-time job statistics
- 🔍 Search and filter jobs
- 🔄 Retry failed jobs
- 🗑️ Delete jobs
- 📝 View job results and errors

---

## 🔍 Troubleshooting

### Issue 1: Redis Connection Failed
```
redis.exceptions.ConnectionError: Error 10061 connecting to localhost:6379
```

**Solution:**
- Ensure Redis server is running: `redis-server`
- Check Redis is listening: `redis-cli ping` (should return "PONG")
- Verify REDIS_URL in .env file

### Issue 2: Worker Not Picking Up Jobs
**Solution:**
- Check worker is running: `rq info --url redis://localhost:6379/0`
- Ensure worker is listening to correct queue: `rq worker workflows`
- Check for worker errors in console output

### Issue 3: Import Error in worker_tasks.py
```
ModuleNotFoundError: No module named 'database'
```

**Solution:**
- Activate virtual environment before starting worker
- Ensure worker runs from project root directory
- Check PYTHONPATH includes project root

### Issue 4: Jobs Stuck in "started" State
**Solution:**
- Check worker logs for errors
- Increase job timeout: `job_timeout='10m'`
- Check database connection in worker

---

## 🎯 Next Steps

### 1. Migrate Workflows to Database
Currently workflows are stored in-memory with `workflow_engine`. Next step:
- Create Workflow database model (already exists in models.py)
- Save workflows to database instead of in-memory dict
- Update execute_workflow() to use database

### 2. Add Real Workflow Execution Logic
Replace this in worker_tasks.py:
```python
# TODO: Replace with actual workflow execution logic
time.sleep(2)  # Simulate work
```

With actual automation logic:
```python
# Execute the workflow based on type
if action.action_type == "create_workflow_customer_followup":
    result = execute_customer_followup(action.inputs)
elif action.action_type == "create_workflow_invoice_processing":
    result = execute_invoice_processing(action.inputs)
```

### 3. Add Notifications
Notify users when workflows complete:
```python
# In worker_tasks.py after workflow completion
send_notification(
    agent_id=action.created_by_agent,
    message=f"Workflow {workflow_id} completed successfully!",
    savings=weekly_savings
)
```

### 4. Docker Compose Integration
Add to `docker-compose.yml`:
```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  rq_worker:
    build: .
    command: rq worker workflows
    environment:
      DATABASE_URL: postgresql+psycopg2://postgres:password@postgres:5432/codexdominion
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - redis
      - postgres
```

---

## 📊 Architecture Diagram

```
┌─────────────────────┐
│  Flask Dashboard    │
│  (flask_dashboard)  │
│                     │
│  /api/chat (POST)   │
│  mode=execute       │
└──────────┬──────────┘
           │
           │ queue.enqueue()
           ▼
    ┌─────────────┐
    │   Redis     │
    │   Queue     │
    │  "workflows"│
    └──────┬──────┘
           │
           │ Job picked up
           ▼
┌──────────────────────┐
│   RQ Worker          │
│   (worker_tasks.py)  │
│                      │
│   execute_workflow() │
└──────────┬───────────┘
           │
           │ Read/Write
           ▼
    ┌─────────────┐       ┌──────────────┐
    │  Postgres   │       │  Workflow    │
    │  Database   │◄──────┤  Engine      │
    │             │       │  (in-memory) │
    └─────────────┘       └──────────────┘
```

---

## 🔥 The Flame Burns Asynchronously! 👑

**Status:** RQ Integration Complete ✅
- ✅ Redis connection configured
- ✅ Queue initialized
- ✅ Background jobs enqueued
- ✅ Worker tasks implemented
- ✅ Error handling added
- ✅ Metrics tracking enabled

**Next Phase:** Migrate workflows from in-memory to database for full persistence!

