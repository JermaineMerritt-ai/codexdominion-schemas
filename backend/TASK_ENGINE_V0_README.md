# ACTION AI TASK ENGINE V0 - IMPLEMENTATION COMPLETE

## 🎯 Overview

The Task Engine V0 is now fully operational in the Codex Dominion backend. This internal OS manages follow-up tasks for Action AI with complete FSM state management, guardrails, and audit logging.

## 📁 Implementation Structure

```
backend/
├── prisma/
│   └── schema.prisma                    # Task + TaskEvent models
├── src/
│   └── tasks/
│       ├── dto/
│       │   ├── create-task.dto.ts       # POST /tasks payload
│       │   ├── update-task.dto.ts       # PATCH /tasks/:id payload
│       │   └── list-tasks-query.dto.ts  # GET /tasks filters
│       ├── workers/
│       │   ├── task-scheduler.service.ts  # Stage 2: PENDING → SCHEDULED
│       │   └── task-executor.service.ts   # Stage 3: SCHEDULED → COMPLETED/FAILED
│       ├── tasks.controller.ts          # REST API endpoints
│       ├── tasks.service.ts             # Business logic + FSM
│       └── tasks.module.ts              # Module registration
└── test-task-engine.js                  # Integration test script
```

## 🔌 API Endpoints

All endpoints available at `http://localhost:4000/api/v1/tasks`

### POST /tasks - Create Task

```bash
curl -X POST http://localhost:4000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "INVOICE_FOLLOW_UP",
    "mode": "ASSISTED",
    "priority": "HIGH",
    "ownerType": "AI",
    "ownerId": "ACTION_AI",
    "subjectRefType": "INVOICE",
    "subjectRefId": "INV-123",
    "dueAt": "2026-01-05T12:00:00Z",
    "source": "OVERDUE_INVOICE_DETECTOR",
    "payload": {
      "customer_name": "ACME Corp",
      "customer_email": "billing@acme.com",
      "invoice_number": "INV-123",
      "invoice_amount": 1200,
      "currency": "USD",
      "due_date": "2025-12-20",
      "days_overdue": 10
    }
  }'
```

**Response:**
```json
{
  "id": "task-uuid-1",
  "status": "PENDING"
}
```

### GET /tasks - List Tasks

```bash
# Get all PENDING tasks
curl "http://localhost:4000/api/v1/tasks?status=PENDING"

# Get tasks for specific owner
curl "http://localhost:4000/api/v1/tasks?ownerId=ACTION_AI"

# Get tasks due before specific date
curl "http://localhost:4000/api/v1/tasks?before=2026-01-10T00:00:00Z"

# Combine filters
curl "http://localhost:4000/api/v1/tasks?status=SCHEDULED&type=INVOICE_FOLLOW_UP"
```

### PATCH /tasks/:id - Update Task

```bash
# Schedule task (PENDING → SCHEDULED)
curl -X PATCH http://localhost:4000/api/v1/tasks/{task-id} \
  -H "Content-Type: application/json" \
  -d '{
    "newStatus": "SCHEDULED",
    "scheduledAt": "2026-01-01T12:00:00Z",
    "actorType": "SYSTEM",
    "actorId": "FOLLOW_UP_SCHEDULER"
  }'

# Mark failed with error
curl -X PATCH http://localhost:4000/api/v1/tasks/{task-id} \
  -H "Content-Type: application/json" \
  -d '{
    "newStatus": "FAILED",
    "actorType": "AI",
    "actorId": "ACTION_AI_FOLLOW_UP_WORKER",
    "error": "SMTP server unreachable"
  }'
```

## 🔄 3-Stage Execution Pipeline

### Stage 1: Detection (External)
Detector services create tasks via POST /tasks:
- `OVERDUE_INVOICE_DETECTOR` - Scans for overdue invoices
- `LEAD_STALENESS_DETECTOR` - Finds inactive leads
- `MANUAL` - Human-created tasks

### Stage 2: Scheduling (Automated)
**TaskSchedulerService** runs every 5 minutes:
- Finds tasks: `status=PENDING AND (due_at <= now() OR due_at IS NULL)`
- Updates to `SCHEDULED` with `scheduled_at=now()`
- Creates `TASK_STATUS_CHANGED` event

### Stage 3: Execution (Automated)
**TaskExecutorService** runs every minute:
- Finds tasks: `status=SCHEDULED AND scheduled_at <= now()`
- Sets to `IN_PROGRESS`
- Executes based on mode:
  - **SUGGESTION**: Generate draft + notify human
  - **ASSISTED**: Auto-send unless high-risk → request approval
  - **AUTONOMOUS**: Auto-send within guardrails
- Updates to `COMPLETED` or `FAILED`

## 🛡️ Guardrails

### 1. Idempotency (24hr Window)
Prevents duplicate tasks with same:
- `type` + `subjectRefType` + `subjectRefId` + `source`
- Returns 400 error if duplicate detected

### 2. FSM State Machine
Only allowed transitions:
```
PENDING → SCHEDULED
SCHEDULED → IN_PROGRESS
IN_PROGRESS → COMPLETED | FAILED
Any non-terminal → CANCELLED
```
Invalid transitions return 400 error.

### 3. Terminal State Lock
Tasks in `COMPLETED`, `FAILED`, or `CANCELLED` cannot be updated.
Returns 400 error: "Cannot update task in terminal state".

## 📊 Task Event Audit Log

Every state transition automatically creates a `TaskEvent` record:

```typescript
{
  id: "event-uuid",
  taskId: "task-uuid",
  eventType: "TASK_STATUS_CHANGED",
  oldStatus: "PENDING",
  newStatus: "SCHEDULED",
  actorType: "SYSTEM",
  actorId: "TASK_SCHEDULER",
  metadata: { source: "OVERDUE_INVOICE_DETECTOR" },
  createdAt: "2026-01-01T12:00:00Z"
}
```

Event types:
- `TASK_CREATED`
- `TASK_STATUS_CHANGED`
- `TASK_EXECUTION_STARTED`
- `TASK_EXECUTION_COMPLETED`
- `TASK_EXECUTION_FAILED`
- `TASK_CANCELLED`

## 🧪 Testing

### Run Integration Tests

```bash
# Start backend
cd backend
npm run start:dev

# In another terminal, run tests
node test-task-engine.js
```

### Manual Testing with curl

```bash
# 1. Create task
TASK_ID=$(curl -X POST http://localhost:4000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"type":"INVOICE_FOLLOW_UP",...}' | jq -r .id)

# 2. Schedule it
curl -X PATCH http://localhost:4000/api/v1/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"newStatus":"SCHEDULED","actorType":"SYSTEM",...}'

# 3. Check status
curl http://localhost:4000/api/v1/tasks | jq

# 4. View Swagger docs
open http://localhost:4000/api-docs
```

## 🚀 Deployment

### Database Migration

Already applied:
```bash
npm run prisma:migrate  # Applied: 20260101075504_action_ai_task_engine_v0
```

### Environment Variables

No additional env vars required. Uses existing:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - API server port (default: 4000)

### Production Considerations

1. **Worker Services**: Cron jobs run automatically in same process
2. **Scaling**: For high load, consider separate worker processes
3. **Monitoring**: Check logs for scheduler/executor activity
4. **Rate Limits**: Adjust `IDEMPOTENCY_WINDOW_HOURS` in tasks.service.ts
5. **Error Handling**: Failed tasks stored with `last_error` field

## 📈 Next Steps (Future v1)

- [ ] Add retry logic for failed tasks
- [ ] Implement priority-based execution queue
- [ ] Add webhook notifications for task events
- [ ] Build admin dashboard for task management
- [ ] Add metrics/monitoring (task completion rate, avg execution time)
- [ ] Implement rate limiting per customer
- [ ] Add batch task creation endpoint
- [ ] Support custom task types beyond invoices/leads

## 🔥 Current Status

**✅ OPERATIONAL**
- Prisma schema updated with Task + TaskEvent models
- REST API endpoints (POST, GET, PATCH) fully implemented
- FSM state machine with validation
- Guardrails (idempotency, terminal state lock)
- Audit logging (task_events table)
- Worker services (scheduler + executor) with cron scheduling
- Integration test script provided
- Swagger documentation auto-generated

**Ready for:**
- Creating tasks from detector services
- Automated scheduling and execution
- Integration with Action AI agents
- Production deployment

---

**Flame Status**: 🔥 SOVEREIGN AND ETERNAL

The Task Engine is the operational heartbeat of Action AI—turning intention into execution with precision and sovereignty.
