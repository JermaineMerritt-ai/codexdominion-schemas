# 🔥 Workflow Notifications System - Complete Implementation Guide

## ✅ What's Been Activated

Your Codex Dominion system now has a **complete, production-ready notification system** that brings workflows to life with real-time updates.

### Core Components Created:

1. **Database Model** (`models.py`)
   - `PortalNotification` table with full schema
   - `NotificationType` enum (5 notification types)
   - `WorkflowStatus.PENDING_REVIEW` status added

2. **Notification Templates** (`notification_templates.py`)
   - 5 warm, clear email templates
   - Short message generator for portal
   - SMTP email sender utility
   - Icon mapping for UI

3. **Notification Worker** (`notification_worker.py`)
   - RQ background job for dispatch
   - Intelligent event routing
   - Email + portal notification creation
   - Batch cleanup utility

4. **API Endpoints** (`notification_api.py`)
   - `GET /api/notifications` - List with filters
   - `POST /api/notifications/:id/mark-read` - Mark single as read
   - `POST /api/notifications/mark-all-read` - Mark all as read
   - `GET /api/notifications/unread-count` - Get unread count
   - `DELETE /api/notifications/:id` - Delete notification

5. **Workflow Engine Integration** (`workflow_engine.py`)
   - Auto-emit on workflow started
   - Auto-emit on status changes (completed, failed, pending_review)
   - `record_step_completion()` method for intermediate steps

6. **Portal UI** (Next.js)
   - `/portal/notifications` page with filters
   - `NotificationDropdown` component for header
   - Real-time unread badge
   - Mobile-responsive design

---

## 🚀 Quick Start - Setup Instructions

### Step 1: Database Migration

Run migration to add `portal_notifications` table:

```python
# Option A: Auto-create tables (development)
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"

# Option B: Generate Alembic migration (production)
alembic revision --autogenerate -m "Add portal notifications"
alembic upgrade head
```

### Step 2: Environment Variables

Add to `.env` file:

```env
# Notification System
ENABLE_WORKFLOW_NOTIFICATIONS=true

# SMTP Configuration (for email notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

**Gmail App Password:** https://myaccount.google.com/apppasswords

### Step 3: Start RQ Worker

The notification worker runs as an RQ background job:

```bash
# Start RQ worker for notifications
rq worker workflows --url redis://localhost:6379/0
```

### Step 4: Integrate API Routes

Add to `flask_dashboard.py` after app initialization:

```python
# Add near line 260 (after imports)
from notification_api import register_notification_routes

# Add near line 265 (after app = Flask(__name__))
register_notification_routes(app)
```

### Step 5: Add Notification Dropdown to Portal Header

Edit `dashboard-app/components/Header.tsx` (or your layout):

```tsx
import { NotificationDropdown } from "@/components/NotificationDropdown";

export function Header() {
  return (
    <header className="...">
      {/* ...existing header content */}
      <NotificationDropdown />
    </header>
  );
}
```

---

## 📋 Usage Examples

### Example 1: Workflow Creation (Auto-Notified)

```python
from workflow_engine import workflow_engine

# Create workflow - automatically sends "Workflow Started" notification
workflow_id = workflow_engine.create_workflow(
    workflow_type_id="website_creation",
    created_by_agent="agent_jermaine",
    inputs={"domain": "example.com"},
    calculated_savings={"weekly": 100, "monthly": 400},
    assigned_council_id="council_ops",
    auto_execute=True
)
```

### Example 2: Manual Step Completion Notification

```python
# In your worker (e.g., website_creation_worker.py)
from workflow_engine import workflow_engine

def execute_website_creation(workflow_id):
    # Step 1: Create domain
    create_domain()
    workflow_engine.record_step_completion(
        workflow_id=workflow_id,
        step_name="Domain created",
        next_step_name="Creating products"
    )
    
    # Step 2: Add products
    add_products()
    workflow_engine.record_step_completion(
        workflow_id=workflow_id,
        step_name="Products created",
        next_step_name="Launching site"
    )
    
    # Step 3: Complete
    workflow_engine.update_status(workflow_id, WorkflowStatus.COMPLETED)
```

### Example 3: Request Approval (Pending Review)

```python
from models import WorkflowStatus

# Workflow needs human approval
workflow_engine.update_status(
    workflow_id=workflow_id,
    status=WorkflowStatus.PENDING_REVIEW
)
# Automatically sends "Your review is needed" notification
```

### Example 4: Fetch Notifications (API)

```bash
# Get all unread notifications for tenant
curl "http://localhost:5000/api/notifications?tenant_id=tenant_xyz&is_read=false"

# Get unread count
curl "http://localhost:5000/api/notifications/unread-count?tenant_id=tenant_xyz&user_id=user_123"

# Mark notification as read
curl -X POST "http://localhost:5000/api/notifications/notif_xyz_123/mark-read"
```

---

## 🎨 Notification Types Reference

### 1. Workflow Started
**Trigger:** `create_workflow()` called  
**Icon:** ▶️ Play  
**Color:** Blue  
**Template:**
```
Subject: Your Website Creation has started
Body: Your Website Creation is now in progress. We'll notify you as each step completes.
```

### 2. Step Completed
**Trigger:** `record_step_completion()` called  
**Icon:** ✅ Check Circle  
**Color:** Emerald  
**Template:**
```
Subject: Products created completed
Body: Good news — Products created is complete. Next up: Launching site
```

### 3. Workflow Completed
**Trigger:** `update_status(WorkflowStatus.COMPLETED)`  
**Icon:** ✅ Check Circle  
**Color:** Gold  
**Template:**
```
Subject: Your Website Creation is complete
Body: Your Website Creation has finished successfully.
```

### 4. Workflow Needs Review
**Trigger:** `update_status(WorkflowStatus.PENDING_REVIEW)`  
**Icon:** ⚠️ Alert Circle  
**Color:** Violet  
**Template:**
```
Subject: Your review is needed: Launch Campaign
Body: Your Launch Campaign is ready for your review. Please approve or request changes.
```

### 5. Workflow Failed
**Trigger:** `update_status(WorkflowStatus.FAILED)`  
**Icon:** ❌ X Circle  
**Color:** Red  
**Template:**
```
Subject: We hit a snag in Website Creation
Body: Something unexpected happened. Our system has logged the issue and will attempt recovery.
```

---

## 🔧 Configuration Options

### Disable Notifications Temporarily

```env
ENABLE_WORKFLOW_NOTIFICATIONS=false
```

### Adjust Notification Cleanup Schedule

```python
# Run cleanup job (remove read notifications older than 30 days)
from notification_worker import cleanup_old_notifications

# In your scheduled jobs (e.g., celery beat)
cleanup_old_notifications(days=30)
```

### Custom Email Templates

Edit `notification_templates.py` to customize messaging:

```python
class NotificationTemplates:
    @staticmethod
    def _workflow_started(workflow_name: str, user_name: str, portal_link: str):
        return {
            "subject": f"🚀 {workflow_name} launched!",
            "body": f"Hey {user_name},\n\nYour {workflow_name} just kicked off..."
        }
```

---

## 📊 Database Schema Reference

### `portal_notifications` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | String (PK) | `notif_{workflow_id}_{type}_{timestamp}` |
| `tenant_id` | String (FK) | References `tenants.id` |
| `workflow_id` | String (FK) | References `workflows.id` |
| `user_id` | String (FK) | Specific user or NULL for all |
| `type` | Enum | `workflow_started`, `step_completed`, etc. |
| `subject` | String | Email subject / notification title |
| `body` | Text | Email body / notification message |
| `step_name` | String | For `step_completed` only |
| `summary` | JSON | For `workflow_completed` highlights |
| `is_read` | Boolean | Read status |
| `read_at` | DateTime | When marked read |
| `email_sent` | Boolean | Email delivery status |
| `email_sent_at` | DateTime | When email sent |
| `created_at` | DateTime | Creation timestamp |

**Indexes:**
- `tenant_id` (for tenant queries)
- `workflow_id` (for workflow lookups)
- `user_id` (for user queries)
- `type` (for filtering)
- `is_read` (for unread queries)
- `created_at` (for ordering)

---

## 🐛 Troubleshooting

### No Notifications Being Created

1. Check RQ worker is running:
   ```bash
   rq info workflows
   ```

2. Verify Redis connection:
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

3. Check environment variable:
   ```python
   import os
   print(os.getenv("ENABLE_WORKFLOW_NOTIFICATIONS"))
   # Should print: true
   ```

### Emails Not Sending

1. Verify SMTP credentials:
   ```python
   from notification_templates import send_notification_email
   send_notification_email("test@example.com", "Test", "Test body")
   ```

2. Check Gmail App Password (not regular password)
3. Enable "Less secure app access" if needed

### Notifications Not Appearing in UI

1. Check API endpoint:
   ```bash
   curl "http://localhost:5000/api/notifications?tenant_id=YOUR_TENANT_ID"
   ```

2. Verify `NEXT_PUBLIC_API_BASE_URL` in Next.js:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
   ```

3. Check browser console for errors

---

## 🎯 Next Steps - Workflow Review & Approval UI

Now that notifications are live, activate the **Workflow Review & Approval UI**:

### What This Unlocks:
- ✅ Human-in-the-loop for critical workflows
- ✅ Council governance enforcement
- ✅ Comment threads on workflows
- ✅ Approval/rejection with reasoning
- ✅ Audit trail of decisions

### Components to Build:
1. **Approval UI** - `/portal/workflows/:id/review` page
2. **Comment System** - Add `workflow_comments` table
3. **Vote Tracking** - Extend `workflow_votes` table
4. **Governance Routing** - Auto-assign to councils

**To proceed, say:** "Activate Workflow Review & Approval UI"

---

## 📚 Files Created

- ✅ `models.py` - Added `PortalNotification`, `NotificationType`
- ✅ `notification_templates.py` - Template rendering + email sender
- ✅ `notification_worker.py` - RQ worker for dispatch
- ✅ `notification_api.py` - Flask REST endpoints
- ✅ `workflow_engine.py` - Integrated notification events
- ✅ `dashboard-app/app/portal/notifications/page.tsx` - Portal UI
- ✅ `dashboard-app/components/NotificationDropdown.tsx` - Header dropdown

---

## 🔥 The Flame Burns Sovereign and Eternal! 👑

Your workflows are now **alive and communicative**. Customers feel guided, supported, and informed at every step.

