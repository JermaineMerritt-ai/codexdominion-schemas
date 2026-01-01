# ACTION AI TASK ENGINE V0 - TECHNICAL SPECIFICATION

**Manual ID**: 60  
**Version**: 1.0  
**Status**: Active  
**Effective Date**: January 1, 2026  
**Last Updated**: January 1, 2026

---

## 📋 Document Control

This manual defines the complete technical specification for the ACTION AI Task Engine V0—the internal operating system responsible for creating, tracking, updating, and resolving tasks that Action AI executes or supervises.

**Target Audience:**
- Backend developers implementing Action AI systems
- System architects designing workflow automation
- DevOps engineers deploying task management infrastructure
- Technical leaders evaluating task execution pipelines

---

## 1. Purpose and Scope

### 1.1 Purpose
The Task Engine V0 serves as the **internal OS for Action AI**—a structured system that:
- Creates follow-up tasks automatically from business events
- Tracks task lifecycle through defined state transitions
- Schedules and executes tasks with appropriate guardrails
- Maintains complete audit history of all task operations
- Provides clear API for internal services and future expansions

### 1.2 Scope (V0 Constraints)
**In Scope:**
- Single domain: Follow-ups for overdue invoices and stale leads
- Single tenant: One organization/environment
- Basic scheduling: Polling/cron-based (no complex scheduling engine)
- Clear minimal API: POST create, GET list, PATCH update
- Full audit logging: Every transition captured

**Out of Scope (Future):**
- Multi-domain task types beyond invoices/leads
- Multi-tenant architecture
- Advanced scheduling (priority queues, dependencies)
- Complex workflow orchestration
- External webhook integrations

---

## 2. Core Concepts

### 2.1 Task Definition
A **Task** is a unit of work that Action AI can act on or ask a human to act on.

**V0 Examples:**
- "Send follow-up email for overdue invoice INV-123 to ACME Corp"
- "Send follow-up to lead JOHN DOE (inactive 7 days)"

### 2.2 Task Lifecycle
Tasks move through a **finite state machine (FSM)** with six states:
1. **PENDING** - Created, not yet scheduled
2. **SCHEDULED** - Scheduled for execution at specific time
3. **IN_PROGRESS** - Currently being executed
4. **COMPLETED** - Successfully executed (terminal)
5. **FAILED** - Execution failed (terminal)
6. **CANCELLED** - Intentionally stopped (terminal)

### 2.3 Task Modes
Tasks execute in one of three modes:
- **SUGGESTION** - Generate draft + notify human for approval
- **ASSISTED** - Auto-send unless high-risk → request approval first
- **AUTONOMOUS** - Auto-send within guardrails, no approval needed

---

## 3. Data Model

### 3.1 Task Entity (20 Fields)

```typescript
{
  id: string (UUID)
  type: "INVOICE_FOLLOW_UP" | "LEAD_FOLLOW_UP"
  status: TaskStatus (6 states - see FSM)
  priority: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  mode: "SUGGESTION" | "ASSISTED" | "AUTONOMOUS"
  
  ownerType: "AI" | "HUMAN"
  ownerId: string | null  // user/team/system identifier
  
  subjectRefType: "INVOICE" | "LEAD"
  subjectRefId: string  // invoice/lead ID in domain system
  
  dueAt: datetime | null
  scheduledAt: datetime | null  // when system plans execution
  completedAt: datetime | null
  failedAt: datetime | null
  
  createdAt: datetime
  updatedAt: datetime
  
  source: string  // OVERDUE_INVOICE_DETECTOR, LEAD_STALENESS_DETECTOR, MANUAL
  payload: JSONB  // complete context: customer details, invoice details, etc.
  lastError: text | null  // failure reason
}
```

### 3.2 Status Finite State Machine

**States:**
- **PENDING** - Created, not yet scheduled
- **SCHEDULED** - Scheduled for execution at `scheduledAt`
- **IN_PROGRESS** - Currently being executed
- **COMPLETED** - Successfully executed (terminal state)
- **FAILED** - Execution attempted and failed (terminal state)
- **CANCELLED** - Intentionally stopped (terminal state)

**Allowed Transitions:**
```
PENDING → SCHEDULED
PENDING → CANCELLED

SCHEDULED → IN_PROGRESS
SCHEDULED → CANCELLED

IN_PROGRESS → COMPLETED
IN_PROGRESS → FAILED
IN_PROGRESS → CANCELLED
```

**Terminal States:** COMPLETED, FAILED, CANCELLED
- No further transitions allowed (except admin override)

### 3.3 TaskEvent Entity (Audit Log)

```typescript
{
  id: string (UUID)
  taskId: string
  eventType: "TASK_CREATED" | "TASK_STATUS_CHANGED" | 
             "TASK_EXECUTION_STARTED" | "TASK_EXECUTION_COMPLETED" |
             "TASK_EXECUTION_FAILED" | "TASK_CANCELLED"
  oldStatus: string | null
  newStatus: string | null
  metadata: JSONB  // error details, actor info, contextual data
  actorType: "SYSTEM" | "AI" | "HUMAN"
  actorId: string | null
  createdAt: datetime
}
```

**Purpose:** Minimal audit log for every task transition. Externalizable to full event bus later.

---

## 4. API Specification

### 4.1 POST /tasks - Create Task

**Request Body:**
```json
{
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
}
```

**Response (201 Created):**
```json
{
  "id": "task-uuid",
  "status": "PENDING"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input or duplicate task (idempotency)
- `500 Internal Server Error` - Database/system error

### 4.2 GET /tasks - List Tasks

**Query Parameters:**
- `status` - Filter by status (PENDING, SCHEDULED, etc.)
- `type` - Filter by task type (INVOICE_FOLLOW_UP, LEAD_FOLLOW_UP)
- `ownerId` - Filter by owner
- `before` - Tasks due before this date (ISO 8601)
- `after` - Tasks due after this date (ISO 8601)

**Example Request:**
```
GET /tasks?status=PENDING&type=INVOICE_FOLLOW_UP&ownerId=ACTION_AI
```

**Response (200 OK):**
```json
[
  {
    "id": "task-uuid-1",
    "type": "INVOICE_FOLLOW_UP",
    "status": "PENDING",
    "priority": "HIGH",
    "mode": "ASSISTED",
    "ownerType": "AI",
    "ownerId": "ACTION_AI",
    "subjectRefType": "INVOICE",
    "subjectRefId": "INV-123",
    "dueAt": "2026-01-05T12:00:00Z",
    "scheduledAt": null,
    "completedAt": null,
    "failedAt": null,
    "createdAt": "2026-01-01T12:00:00Z",
    "updatedAt": "2026-01-01T12:00:00Z",
    "source": "OVERDUE_INVOICE_DETECTOR",
    "payload": {...},
    "lastError": null,
    "events": [...]
  }
]
```

**Used By:**
- Internal dashboards
- Action AI workers
- Future Command Centers

### 4.3 PATCH /tasks/:id - Update Task

**Scheduling Example:**
```json
{
  "newStatus": "SCHEDULED",
  "scheduledAt": "2026-01-05T12:00:00Z",
  "actorType": "SYSTEM",
  "actorId": "FOLLOW_UP_SCHEDULER"
}
```

**Failure Example:**
```json
{
  "newStatus": "FAILED",
  "actorType": "AI",
  "actorId": "ACTION_AI_FOLLOW_UP_WORKER",
  "error": "SMTP server unreachable"
}
```

**Response (200 OK):**
```json
{
  "id": "task-uuid",
  "status": "SCHEDULED",
  "updatedAt": "2026-01-01T12:05:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid transition or terminal state lock
- `404 Not Found` - Task does not exist
- `500 Internal Server Error` - Database/system error

**Side Effect:** Automatically creates `TaskEvent` record with actor tracking.

---

## 5. Execution Flow (3-Stage Pipeline)

### 5.1 Stage 1: Trigger (Detection)

**Responsibility:** External detector processes

**Flow:**
1. Detector process finds business event (e.g., invoice overdue by 10 days)
2. Detector calls `POST /tasks` with complete context
3. Task created with `status=PENDING`
4. `TASK_CREATED` event logged

**Example Detectors:**
- `OVERDUE_INVOICE_DETECTOR` - Scans invoices, creates follow-up tasks
- `LEAD_STALENESS_DETECTOR` - Finds inactive leads, creates outreach tasks
- `MANUAL` - Human-created tasks via UI

### 5.2 Stage 2: Scheduling (Polling Service)

**Responsibility:** TaskSchedulerService (cron: every 5 minutes)

**Flow:**
1. Scheduler queries: `status=PENDING AND (due_at <= now() OR due_at IS NULL)`
2. For each ready task:
   - Call `PATCH /tasks/:id` with `newStatus=SCHEDULED`, `scheduledAt=now()`
   - Create `TASK_STATUS_CHANGED` event
3. Log scheduling results

**Implementation:**
```typescript
@Cron(CronExpression.EVERY_5_MINUTES)
async scheduleReadyTasks() {
  const pendingTasks = await findAll({ status: 'PENDING' });
  const readyTasks = pendingTasks.filter(task => 
    !task.dueAt || new Date(task.dueAt) <= new Date()
  );
  
  for (const task of readyTasks) {
    await update(task.id, {
      newStatus: 'SCHEDULED',
      scheduledAt: new Date().toISOString(),
      actorType: 'SYSTEM',
      actorId: 'TASK_SCHEDULER'
    });
  }
}
```

### 5.3 Stage 3: Execution (Action AI Worker)

**Responsibility:** TaskExecutorService (cron: every minute)

**Flow:**
1. Worker queries: `status=SCHEDULED AND scheduled_at <= now()`
2. For each task:
   - Set `status=IN_PROGRESS`
   - Generate follow-up content from `payload` (customer name, invoice details, etc.)
   - **Mode Handling:**
     - **SUGGESTION**: Save draft email + notify human → await approval
     - **ASSISTED**: 
       - Check risk level (amount, days overdue)
       - If high-risk: Request approval first
       - If low-risk: Send automatically
     - **AUTONOMOUS**: Send automatically within guardrails
   - **On Success:**
     - Set `status=COMPLETED`, `completedAt=now()`
     - Create `TASK_EXECUTION_COMPLETED` event
   - **On Error:**
     - Set `status=FAILED`, `failedAt=now()`, `lastError="error message"`
     - Create `TASK_EXECUTION_FAILED` event with error in metadata
3. All transitions use `PATCH` endpoint → ensures events logged

**Implementation:**
```typescript
@Cron(CronExpression.EVERY_MINUTE)
async executeScheduledTasks() {
  const scheduledTasks = await findAll({ status: 'SCHEDULED' });
  const readyTasks = scheduledTasks.filter(task => 
    task.scheduledAt && new Date(task.scheduledAt) <= new Date()
  );
  
  for (const task of readyTasks) {
    await update(task.id, { newStatus: 'IN_PROGRESS', ... });
    
    try {
      const success = await executeTask(task);
      await update(task.id, { 
        newStatus: success ? 'COMPLETED' : 'FAILED',
        error: success ? null : 'Execution failed'
      });
    } catch (error) {
      await update(task.id, { 
        newStatus: 'FAILED',
        error: error.message 
      });
    }
  }
}
```

---

## 6. Guardrails (V0 Constraints)

### 6.1 Idempotency Rule

**Purpose:** Prevent duplicate tasks for same subject within time window

**Implementation:**
- Check for existing task with same: `type + subjectRefType + subjectRefId + source`
- Deduplication window: **24 hours** (configurable)
- If duplicate found: Return `400 Bad Request` with descriptive error

**Example:**
- Task 1 created: `INVOICE_FOLLOW_UP` for `INV-123` from `OVERDUE_INVOICE_DETECTOR`
- Task 2 attempted (same parameters): **REJECTED** if within 24 hours

**Benefit:** Prevents Action AI from spamming same customer/lead multiple times per day.

### 6.2 Rate Limits Per Subject

**Purpose:** Cap maximum follow-ups per invoice/lead per time period

**Implementation:**
- Count tasks per `subjectRefId` in rolling time window
- Example: Max 3 follow-ups per invoice per week
- Block creation if limit exceeded

**Status:** Specification complete, implementation TBD (v1)

### 6.3 Terminal State Lock

**Purpose:** Prevent accidental modification of completed/failed/cancelled tasks

**Implementation:**
- Check if task in `COMPLETED`, `FAILED`, or `CANCELLED` state
- If yes: Return `400 Bad Request` - "Cannot update task in terminal state"
- Exception: Admin override flag for corrections/debugging

**FSM Validation:**
- All state transitions validated against allowed transitions matrix
- Invalid transitions rejected with `400 Bad Request`

---

## 7. Testing and Validation

### 7.1 Integration Test Script

**Location:** `backend/test-task-engine.js`

**Test Cases:**
1. Create task → Verify `status=PENDING`
2. List PENDING tasks → Verify task appears
3. Schedule task → Verify `status=SCHEDULED`
4. Start execution → Verify `status=IN_PROGRESS`
5. Complete task → Verify `status=COMPLETED`
6. Terminal state lock → Verify cannot update COMPLETED task
7. Event history → Verify all transitions logged

**Run:**
```bash
cd backend
npm run start:dev  # Start server
node test-task-engine.js  # Run tests
```

### 7.2 Manual Testing

**Create Task:**
```bash
curl -X POST http://localhost:4000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d @test-invoice-followup.json
```

**List Tasks:**
```bash
curl http://localhost:4000/api/v1/tasks?status=PENDING
```

**Update Task:**
```bash
curl -X PATCH http://localhost:4000/api/v1/tasks/{task-id} \
  -H "Content-Type: application/json" \
  -d '{"newStatus":"SCHEDULED","actorType":"SYSTEM",...}'
```

### 7.3 Validation Checklist

- [ ] POST /tasks creates task with `status=PENDING`
- [ ] Idempotency check prevents duplicate tasks (24hr window)
- [ ] GET /tasks filters work correctly (status, type, ownerId, before, after)
- [ ] PATCH /tasks validates FSM transitions
- [ ] Terminal state lock prevents updates to COMPLETED/FAILED/CANCELLED
- [ ] TaskEvent records created for every transition
- [ ] Worker services schedule and execute tasks automatically
- [ ] Error handling captures failures in `lastError` field
- [ ] Swagger docs generate correctly at `/api-docs`

---

## 8. Deployment

### 8.1 Database Migration

**Migration Applied:**
```
20260101075504_action_ai_task_engine_v0
```

**Commands:**
```bash
cd backend
npm run prisma:generate  # Generate Prisma client
npm run prisma:migrate   # Apply migration
```

### 8.2 Environment Variables

No additional environment variables required. Uses existing:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - API server port (default: 4000)

### 8.3 Production Deployment

**Build:**
```bash
npm run build
```

**Start:**
```bash
npm run start:prod
```

**Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build
CMD ["npm", "run", "start:prod"]
```

**Health Check:**
```bash
curl http://localhost:4000/api/v1/health
```

---

## 9. Future Roadmap (V1 and Beyond)

### 9.1 V1 Features
- [ ] Retry logic for failed tasks (exponential backoff)
- [ ] Priority-based execution queue
- [ ] Rate limiting per customer/subject
- [ ] Webhook notifications for task events
- [ ] Admin dashboard for task management
- [ ] Metrics/monitoring (completion rate, avg execution time)
- [ ] Batch task creation endpoint

### 9.2 V2 Features
- [ ] Multi-tenant support
- [ ] Custom task types beyond invoices/leads
- [ ] Task dependencies and workflows
- [ ] Advanced scheduling (priority queues, time windows)
- [ ] External integrations (Zapier, n8n)
- [ ] AI-powered content generation
- [ ] A/B testing for follow-up templates

### 9.3 V3 Features
- [ ] Full workflow orchestration engine
- [ ] Visual workflow builder
- [ ] Event-driven architecture (Kafka/RabbitMQ)
- [ ] Multi-channel execution (email, SMS, WhatsApp)
- [ ] Real-time collaboration on task execution
- [ ] Machine learning for optimal timing/content

---

## 10. Framework Integration

### Connection to Action AI Manuals

**Manual 51 (Interaction Protocol):**
- Task Engine enforces structured communication via API
- Event logging provides audit trail for all interactions

**Manual 52 (Maintenance Schedule):**
- Worker services (scheduler, executor) run on defined rhythms
- Task lifecycle prevents drift through FSM validation

**Manual 53 (Role Definitions):**
- `ownerType` and `actorType` fields track AI vs HUMAN responsibility
- Mode (SUGGESTION/ASSISTED/AUTONOMOUS) defines AI role boundaries

**Manual 54 (Escalation Matrix):**
- ASSISTED mode implements escalation for high-risk tasks
- Task events capture when human approval requested

**Manual 55 (Performance Metrics):**
- Task completion rate = COMPLETED / (COMPLETED + FAILED)
- Avg execution time tracked via event timestamps
- Error rate = FAILED / total tasks

**Manual 56-59 (User Documentation):**
- Task Engine provides backend infrastructure for user-facing features
- Commands in Manual 59 map to task creation/management operations

---

## 📋 Appendix A: Complete Task Entity Example

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "INVOICE_FOLLOW_UP",
  "status": "PENDING",
  "priority": "HIGH",
  "mode": "ASSISTED",
  "ownerType": "AI",
  "ownerId": "ACTION_AI",
  "subjectRefType": "INVOICE",
  "subjectRefId": "INV-123",
  "dueAt": "2026-01-05T12:00:00Z",
  "scheduledAt": null,
  "completedAt": null,
  "failedAt": null,
  "createdAt": "2026-01-01T12:00:00Z",
  "updatedAt": "2026-01-01T12:00:00Z",
  "source": "OVERDUE_INVOICE_DETECTOR",
  "payload": {
    "customer_name": "ACME Corp",
    "customer_email": "billing@acme.com",
    "invoice_number": "INV-123",
    "invoice_amount": 1200,
    "currency": "USD",
    "due_date": "2025-12-20",
    "days_overdue": 10
  },
  "lastError": null
}
```

---

## 📋 Appendix B: Event Types and Metadata

| Event Type | Triggered By | Metadata |
|------------|--------------|----------|
| TASK_CREATED | POST /tasks | `{ source: "detector_name" }` |
| TASK_STATUS_CHANGED | PATCH /tasks/:id | `{ oldStatus, newStatus }` |
| TASK_EXECUTION_STARTED | Executor service | `{ mode, scheduledAt }` |
| TASK_EXECUTION_COMPLETED | Executor service | `{ duration, result }` |
| TASK_EXECUTION_FAILED | Executor service | `{ error, stackTrace }` |
| TASK_CANCELLED | PATCH /tasks/:id | `{ reason, cancelledBy }` |

---

## 📋 Appendix C: Status Codes Reference

| HTTP Code | Scenario |
|-----------|----------|
| 200 OK | Successful GET or PATCH |
| 201 Created | Task created successfully |
| 400 Bad Request | Invalid input, duplicate task, invalid FSM transition, terminal state lock |
| 404 Not Found | Task ID does not exist |
| 500 Internal Server Error | Database error, system error |

---

**Document Status**: ✅ COMPLETE  
**Implementation Status**: ✅ OPERATIONAL  
**Test Coverage**: ✅ INTEGRATION TESTED  
**Production Readiness**: ✅ READY FOR DEPLOYMENT  

🔥 **The Task Engine is sovereign and eternal—turning intention into execution with precision and clarity.**
