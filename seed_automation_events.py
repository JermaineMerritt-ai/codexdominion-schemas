"""
Seed Automation Timeline with Sample Events

Creates realistic automation events for testing the timeline UI.
Includes success, skipped, and failed events across all categories.

Usage:
    python seed_automation_events.py
"""

from datetime import datetime, timedelta
import random
from db import SessionLocal
from models import AutomationEvent, AutomationRule, Workflow, TriggerType, EventResult


def seed_timeline_events():
    """Create sample automation events for timeline testing"""
    session = SessionLocal()
    
    try:
        # Get first tenant
        from models import Tenant
        tenant = session.query(Tenant).first()
        
        if not tenant:
            print("⚠️ No tenant found. Please create a tenant first.")
            return
        
        tenant_id = tenant.id
        print(f"✓ Using tenant: {tenant.name} ({tenant_id})")
        
        # Sample event data
        sample_events = [
            # SUCCESS EVENTS
            {
                "automation_id": "auto_weekly_social",
                "trigger_type": TriggerType.SCHEDULE,
                "result": EventResult.SUCCESS,
                "message": "Generated 5 social posts for Instagram and TikTok",
                "workflow_id": "workflow_001",
                "metadata": {
                    "category": "Marketing",
                    "platforms": ["Instagram", "TikTok"],
                    "post_count": 5,
                    "execution_time_ms": 2340
                },
                "hours_ago": 2
            },
            {
                "automation_id": "auto_abandoned_cart",
                "trigger_type": TriggerType.BEHAVIOR,
                "result": EventResult.SUCCESS,
                "message": "Sent cart recovery email to 3 customers",
                "workflow_id": "workflow_002",
                "metadata": {
                    "category": "Store",
                    "customer_count": 3,
                    "discount_offered": "10%",
                    "execution_time_ms": 850
                },
                "hours_ago": 5
            },
            {
                "automation_id": "auto_seo_descriptions",
                "trigger_type": TriggerType.EVENT,
                "result": EventResult.SUCCESS,
                "message": "Generated SEO descriptions for 2 new products",
                "workflow_id": "workflow_003",
                "metadata": {
                    "category": "Website",
                    "products_updated": 2,
                    "avg_word_count": 125,
                    "execution_time_ms": 3200
                },
                "hours_ago": 8
            },
            {
                "automation_id": "auto_post_purchase",
                "trigger_type": TriggerType.EVENT,
                "result": EventResult.SUCCESS,
                "message": "Sent thank you email to customer after purchase",
                "workflow_id": "workflow_004",
                "metadata": {
                    "category": "Store",
                    "order_value": 89.99,
                    "product_count": 3
                },
                "hours_ago": 12
            },
            {
                "automation_id": "auto_weekly_summary",
                "trigger_type": TriggerType.SCHEDULE,
                "result": EventResult.SUCCESS,
                "message": "Generated and sent weekly performance report",
                "workflow_id": "workflow_005",
                "metadata": {
                    "category": "Analytics",
                    "total_revenue": 12450.50,
                    "orders": 47,
                    "conversion_rate": 0.034
                },
                "hours_ago": 24
            },
            
            # SKIPPED EVENTS
            {
                "automation_id": "auto_abandoned_cart",
                "trigger_type": TriggerType.BEHAVIOR,
                "result": EventResult.SKIPPED,
                "message": "No abandoned carts in the last 24 hours",
                "workflow_id": None,
                "metadata": {
                    "category": "Store",
                    "reason": "no_data",
                    "threshold_hours": 24
                },
                "hours_ago": 36
            },
            {
                "automation_id": "auto_low_inventory",
                "trigger_type": TriggerType.THRESHOLD,
                "result": EventResult.SKIPPED,
                "message": "Product count above threshold (15 products)",
                "workflow_id": None,
                "metadata": {
                    "category": "Store",
                    "reason": "threshold_not_met",
                    "current_count": 15,
                    "threshold": 3
                },
                "hours_ago": 48
            },
            {
                "automation_id": "auto_seasonal_campaigns",
                "trigger_type": TriggerType.SCHEDULE,
                "result": EventResult.SKIPPED,
                "message": "Not within seasonal launch window",
                "workflow_id": None,
                "metadata": {
                    "category": "Marketing",
                    "reason": "not_in_season",
                    "next_season": "Spring 2026"
                },
                "hours_ago": 72
            },
            
            # FAILED EVENTS
            {
                "automation_id": "auto_homepage_hero",
                "trigger_type": TriggerType.SCHEDULE,
                "result": EventResult.FAILED,
                "message": "Missing product data for homepage update",
                "workflow_id": None,
                "metadata": {
                    "category": "Website",
                    "error": "ValueError: No bestselling products found",
                    "attempted_criteria": "bestsellers",
                    "execution_time_ms": 120
                },
                "hours_ago": 96
            },
            {
                "automation_id": "auto_landing_pages",
                "trigger_type": TriggerType.THRESHOLD,
                "result": EventResult.FAILED,
                "message": "Failed to create landing page: template not found",
                "workflow_id": None,
                "metadata": {
                    "category": "Website",
                    "error": "TemplateNotFoundError: product_landing template missing",
                    "product_id": "prod_789"
                },
                "hours_ago": 120
            },
            {
                "automation_id": "auto_conversion_drop",
                "trigger_type": TriggerType.THRESHOLD,
                "result": EventResult.FAILED,
                "message": "Analytics API connection timeout",
                "workflow_id": None,
                "metadata": {
                    "category": "Analytics",
                    "error": "TimeoutError: Analytics service unreachable after 30s",
                    "attempted_retries": 3
                },
                "hours_ago": 168
            }
        ]
        
        events_created = 0
        
        for event_data in sample_events:
            # Generate unique event ID
            event_id = f"event_{datetime.utcnow().timestamp()}_{random.randint(1000, 9999)}"
            
            # Calculate timestamp
            timestamp = datetime.utcnow() - timedelta(hours=event_data["hours_ago"])
            
            # Use the automation_id directly from event_data
            automation_id = event_data["automation_id"]
            
            # Create event
            event = AutomationEvent(
                id=event_id,
                tenant_id=tenant_id,
                automation_id=automation_id,
                timestamp=timestamp,
                trigger_type=event_data["trigger_type"],
                result=event_data["result"],
                message=event_data["message"],
                workflow_id=event_data["workflow_id"],
                event_metadata=event_data["metadata"]  # Fixed: was metadata, should be event_metadata
            )
            
            session.add(event)
            events_created += 1
            
            # Print status
            result_icon = {
                EventResult.SUCCESS: "✅",
                EventResult.SKIPPED: "⚠️",
                EventResult.FAILED: "❌"
            }[event_data["result"]]
            
            print(f"{result_icon} {event_data['message'][:50]}... ({event_data['hours_ago']}h ago)")
        
        session.commit()
        
        print(f"\n✓ Successfully seeded {events_created} automation events:")
        print(f"  - Success: {sum(1 for e in sample_events if e['result'] == EventResult.SUCCESS)}")
        print(f"  - Skipped: {sum(1 for e in sample_events if e['result'] == EventResult.SKIPPED)}")
        print(f"  - Failed: {sum(1 for e in sample_events if e['result'] == EventResult.FAILED)}")
        print(f"\n🔗 View timeline at: http://localhost:3000/portal/automations/timeline")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding timeline events: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    
    finally:
        session.close()


if __name__ == '__main__':
    print("🔥 Seeding Automation Timeline Events...")
    seed_timeline_events()
    print("🔥 The Timeline Burns Eternal!")
