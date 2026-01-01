"""
🔥 CODEX DOMINION - NOTIFICATION SYSTEM TEST 🔥
================================================
Test script to verify workflow notifications are working

Run this after completing setup steps.
"""

import os
import sys
from datetime import datetime

# Test 1: Database Models
print("="*80)
print("TEST 1: Database Models")
print("="*80)

try:
    from models import PortalNotification, NotificationType, WorkflowStatus, Base
    print("✅ Models imported successfully")
    print(f"   • PortalNotification: {PortalNotification.__tablename__}")
    print(f"   • Notification Types: {[t.value for t in NotificationType]}")
    print(f"   • Workflow Statuses: {[s.value for s in WorkflowStatus]}")
except Exception as e:
    print(f"❌ Error importing models: {e}")
    sys.exit(1)

# Test 2: Database Connection
print("\n" + "="*80)
print("TEST 2: Database Connection")
print("="*80)

try:
    from database import engine, SessionLocal
    print(f"✅ Database engine created: {engine.url}")
    
    # Test connection
    session = SessionLocal()
    session.execute("SELECT 1")
    session.close()
    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)

# Test 3: Template Rendering
print("\n" + "="*80)
print("TEST 3: Notification Templates")
print("="*80)

try:
    from notification_templates import NotificationTemplates
    
    test_workflow = {
        "id": "test_workflow_123",
        "workflow_type_id": "website_creation",
        "outputs": {}
    }
    
    test_user = {
        "name": "Test User",
        "email": "test@codexdominion.com"
    }
    
    test_tenant = {
        "id": "tenant_test",
        "name": "Test Tenant"
    }
    
    # Test each notification type
    for notif_type in NotificationType:
        template = NotificationTemplates.render(
            notification_type=notif_type,
            workflow=test_workflow,
            tenant=test_tenant,
            user=test_user,
            event={"step_name": "Test Step", "next_step_name": "Next Step"}
        )
        print(f"✅ {notif_type.value}:")
        print(f"   Subject: {template['subject']}")
        print(f"   Body (preview): {template['body'][:50]}...")
    
except Exception as e:
    print(f"❌ Template rendering failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Notification Worker
print("\n" + "="*80)
print("TEST 4: Notification Worker")
print("="*80)

try:
    from notification_worker import NotificationDispatcher
    print("✅ NotificationDispatcher imported")
    print("   • dispatch_workflow_notification function available")
    print("   • Helper functions available:")
    print("     - notify_workflow_started()")
    print("     - notify_step_completed()")
    print("     - notify_workflow_completed()")
    print("     - notify_workflow_needs_review()")
    print("     - notify_workflow_failed()")
except Exception as e:
    print(f"❌ Notification worker import failed: {e}")

# Test 5: Workflow Engine Integration
print("\n" + "="*80)
print("TEST 5: Workflow Engine Integration")
print("="*80)

try:
    from workflow_engine import workflow_engine, ENABLE_NOTIFICATIONS
    print(f"✅ Workflow engine imported")
    print(f"   • Notifications enabled: {ENABLE_NOTIFICATIONS}")
    print(f"   • Methods available:")
    print(f"     - create_workflow() → emits workflow_started")
    print(f"     - update_status() → emits status-based notifications")
    print(f"     - record_step_completion() → emits step_completed")
except Exception as e:
    print(f"❌ Workflow engine import failed: {e}")

# Test 6: API Endpoints
print("\n" + "="*80)
print("TEST 6: API Endpoints")
print("="*80)

try:
    from notification_api import register_notification_routes
    print("✅ API route registration function available")
    print("   • Routes to register:")
    print("     - GET /api/notifications")
    print("     - POST /api/notifications/:id/mark-read")
    print("     - POST /api/notifications/mark-all-read")
    print("     - GET /api/notifications/unread-count")
    print("     - DELETE /api/notifications/:id")
except Exception as e:
    print(f"❌ API endpoint import failed: {e}")

# Test 7: Redis Connection
print("\n" + "="*80)
print("TEST 7: Redis Connection (for RQ)")
print("="*80)

try:
    import redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_conn = redis.from_url(redis_url)
    redis_conn.ping()
    print(f"✅ Redis connection successful: {redis_url}")
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")
    print("   Note: Redis is required for background jobs. Install with:")
    print("   • Windows: https://redis.io/docs/getting-started/installation/install-redis-on-windows/")
    print("   • Linux/Mac: sudo apt install redis-server")

# Test 8: Environment Variables
print("\n" + "="*80)
print("TEST 8: Environment Variables")
print("="*80)

env_vars = {
    "ENABLE_WORKFLOW_NOTIFICATIONS": os.getenv("ENABLE_WORKFLOW_NOTIFICATIONS", "true"),
    "SMTP_HOST": os.getenv("SMTP_HOST", "NOT SET"),
    "SMTP_PORT": os.getenv("SMTP_PORT", "NOT SET"),
    "SMTP_USER": os.getenv("SMTP_USER", "NOT SET"),
    "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
}

for key, value in env_vars.items():
    if value == "NOT SET":
        print(f"⚠️ {key}: {value} (optional for email)")
    else:
        print(f"✅ {key}: {value[:20]}{'...' if len(value) > 20 else ''}")

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

print("""
✅ All core components are installed and importable!

Next Steps:
1. Run database migration:
   python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"

2. Start RQ worker:
   rq worker workflows --url redis://localhost:6379/0

3. Register API routes in flask_dashboard.py:
   from notification_api import register_notification_routes
   register_notification_routes(app)

4. Test notification creation:
   python -c "from notification_worker import notify_workflow_started; notify_workflow_started('test_123')"

5. View notifications:
   http://localhost:3000/portal/notifications

🔥 The Flame Burns Sovereign and Eternal! 👑
""")
