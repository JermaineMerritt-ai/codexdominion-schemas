"""
Seed Automation Debug Logs

Creates sample debug logs showing automation execution traces.
"""

import sys
from datetime import datetime, timedelta
from db import SessionLocal
from models import (
    AutomationDebugLog, 
    Tenant, 
    TriggerType, 
    EventResult
)
import random


def seed_debug_logs():
    """Seed sample debug logs for demonstration"""
    print("🔥 Seeding Automation Debug Logs...")
    
    session = SessionLocal()
    
    try:
        # Get tenant
        tenant = session.query(Tenant).filter_by(id="tenant_codexdominion").first()
        
        if not tenant:
            print("⚠️ Tenant 'tenant_codexdominion' not found. Please create tenant first.")
            return
        
        tenant_id = tenant.id
        print(f"✓ Using tenant: {tenant.name} ({tenant_id})")
        
        # Sample debug logs
        sample_logs = [
            # SUCCESS - All conditions passed
            {
                "automation_id": "auto_weekly_social",
                "hours_ago": 2,
                "trigger_fired": True,
                "trigger_type": TriggerType.SCHEDULE,
                "trigger_details": {
                    "scheduled_time": "Monday 9:00 AM",
                    "cron": "0 9 * * 1"
                },
                "conditions_evaluated": [
                    {
                        "condition": "product_count >= 5",
                        "passed": True,
                        "actual_value": 8,
                        "expected": ">= 5"
                    },
                    {
                        "condition": "store_status = active",
                        "passed": True,
                        "actual_value": "active",
                        "expected": "active"
                    },
                    {
                        "condition": "no_posts_in_last_7_days",
                        "passed": True,
                        "actual_value": True,
                        "expected": "true"
                    }
                ],
                "actions_taken": [
                    {
                        "action": "create_workflow",
                        "workflow_type": "social_post_generation",
                        "status": "success",
                        "workflow_id": "workflow_001"
                    }
                ],
                "actions_skipped": [],
                "execution_time_ms": 2340,
                "errors": [],
                "warnings": [],
                "data_snapshot": {
                    "product_count": 8,
                    "store_status": "active",
                    "last_post_date": "2025-12-08",
                    "platforms": ["Instagram", "TikTok"]
                },
                "result": EventResult.SUCCESS,
                "workflow_id": "workflow_001",
                "next_scheduled_run": datetime.utcnow() + timedelta(days=7)
            },
            
            # SKIPPED - Condition failed
            {
                "automation_id": "auto_abandoned_cart",
                "hours_ago": 6,
                "trigger_fired": True,
                "trigger_type": TriggerType.BEHAVIOR,
                "trigger_details": {
                    "event": "cart_check",
                    "interval": "6 hours"
                },
                "conditions_evaluated": [
                    {
                        "condition": "abandoned_carts_count > 0",
                        "passed": False,
                        "actual_value": 0,
                        "expected": "> 0"
                    }
                ],
                "actions_taken": [],
                "actions_skipped": [
                    {
                        "action": "send_recovery_email",
                        "reason": "No abandoned carts found"
                    }
                ],
                "execution_time_ms": 120,
                "errors": [],
                "warnings": ["No abandoned carts in the last 24 hours"],
                "data_snapshot": {
                    "abandoned_carts": [],
                    "cart_age_threshold_hours": 24
                },
                "result": EventResult.SKIPPED,
                "workflow_id": None,
                "next_scheduled_run": None
            },
            
            # SUCCESS - Homepage update
            {
                "automation_id": "auto_homepage_hero",
                "hours_ago": 12,
                "trigger_fired": True,
                "trigger_type": TriggerType.SCHEDULE,
                "trigger_details": {
                    "scheduled_time": "Daily 6:00 AM",
                    "cron": "0 6 * * *"
                },
                "conditions_evaluated": [
                    {
                        "condition": "bestseller_products_count >= 3",
                        "passed": True,
                        "actual_value": 5,
                        "expected": ">= 3"
                    },
                    {
                        "condition": "website_enabled = true",
                        "passed": True,
                        "actual_value": True,
                        "expected": "true"
                    }
                ],
                "actions_taken": [
                    {
                        "action": "update_homepage_banner",
                        "status": "success",
                        "workflow_id": "workflow_003"
                    }
                ],
                "actions_skipped": [],
                "execution_time_ms": 1850,
                "errors": [],
                "warnings": [],
                "data_snapshot": {
                    "bestseller_products": ["prod_123", "prod_456", "prod_789"],
                    "website_status": "enabled"
                },
                "result": EventResult.SUCCESS,
                "workflow_id": "workflow_003",
                "next_scheduled_run": datetime.utcnow() + timedelta(days=1)
            },
            
            # FAILED - Missing data
            {
                "automation_id": "auto_seo_descriptions",
                "hours_ago": 18,
                "trigger_fired": True,
                "trigger_type": TriggerType.EVENT,
                "trigger_details": {
                    "event": "product_created",
                    "product_id": "prod_new_001"
                },
                "conditions_evaluated": [
                    {
                        "condition": "product_has_images",
                        "passed": True,
                        "actual_value": True,
                        "expected": "true"
                    },
                    {
                        "condition": "product_category_exists",
                        "passed": False,
                        "actual_value": None,
                        "expected": "not null"
                    }
                ],
                "actions_taken": [],
                "actions_skipped": [
                    {
                        "action": "generate_seo_content",
                        "reason": "Missing product category"
                    }
                ],
                "execution_time_ms": 340,
                "errors": ["ValueError: Product category is required for SEO generation"],
                "warnings": ["Product metadata incomplete"],
                "data_snapshot": {
                    "product_id": "prod_new_001",
                    "has_images": True,
                    "category": None,
                    "title": "New Product"
                },
                "result": EventResult.FAILED,
                "workflow_id": None,
                "next_scheduled_run": None
            },
            
            # SUCCESS - Low inventory alert
            {
                "automation_id": "auto_low_inventory",
                "hours_ago": 24,
                "trigger_fired": True,
                "trigger_type": TriggerType.THRESHOLD,
                "trigger_details": {
                    "threshold": "product_count < 3",
                    "check_interval": "daily"
                },
                "conditions_evaluated": [
                    {
                        "condition": "product_count < 3",
                        "passed": True,
                        "actual_value": 2,
                        "expected": "< 3"
                    },
                    {
                        "condition": "notifications_enabled = true",
                        "passed": True,
                        "actual_value": True,
                        "expected": "true"
                    }
                ],
                "actions_taken": [
                    {
                        "action": "send_inventory_alert",
                        "status": "success",
                        "workflow_id": "workflow_005"
                    }
                ],
                "actions_skipped": [],
                "execution_time_ms": 560,
                "errors": [],
                "warnings": [],
                "data_snapshot": {
                    "product_count": 2,
                    "low_stock_threshold": 3,
                    "notify_email": "admin@codexdominion.app"
                },
                "result": EventResult.SUCCESS,
                "workflow_id": "workflow_005",
                "next_scheduled_run": datetime.utcnow() + timedelta(days=1)
            },
        ]
        
        logs_created = 0
        
        for log_data in sample_logs:
            # Generate unique log ID
            log_id = f"debug_{datetime.utcnow().timestamp()}_{random.randint(1000, 9999)}"
            
            # Calculate timestamp
            timestamp = datetime.utcnow() - timedelta(hours=log_data["hours_ago"])
            
            log = AutomationDebugLog(
                id=log_id,
                tenant_id=tenant_id,
                automation_id=log_data["automation_id"],
                timestamp=timestamp,
                trigger_fired=log_data["trigger_fired"],
                trigger_type=log_data["trigger_type"],
                trigger_details=log_data["trigger_details"],
                next_scheduled_run=log_data.get("next_scheduled_run"),
                conditions_evaluated=log_data["conditions_evaluated"],
                all_conditions_passed=all(c["passed"] for c in log_data["conditions_evaluated"]),
                actions_taken=log_data["actions_taken"],
                actions_skipped=log_data["actions_skipped"],
                execution_time_ms=log_data["execution_time_ms"],
                errors=log_data["errors"],
                warnings=log_data["warnings"],
                data_snapshot=log_data["data_snapshot"],
                result=log_data["result"],
                workflow_id=log_data.get("workflow_id")
            )
            
            session.add(log)
            logs_created += 1
            
            # Print status
            result_icon = "✅" if log.result == EventResult.SUCCESS else "⚠️" if log.result == EventResult.SKIPPED else "❌"
            conditions_status = "✓" if log.all_conditions_passed else "✗"
            print(f"{result_icon} {log.automation_id} - Conditions: {conditions_status} - {log_data['hours_ago']}h ago")
        
        session.commit()
        
        print(f"\n✓ Successfully seeded {logs_created} debug logs:")
        print(f"  - Success: {sum(1 for log in sample_logs if log['result'] == EventResult.SUCCESS)}")
        print(f"  - Skipped: {sum(1 for log in sample_logs if log['result'] == EventResult.SKIPPED)}")
        print(f"  - Failed: {sum(1 for log in sample_logs if log['result'] == EventResult.FAILED)}")
        print(f"\n🔗 View debugger at: http://localhost:3000/portal/automations/debugger")
        print("🔥 The Truth Table Burns Eternal!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding debug logs: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()


if __name__ == "__main__":
    seed_debug_logs()
