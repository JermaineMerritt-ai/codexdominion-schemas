"""
CODEX DOMINION - CUSTOMER SERVICE AUTOMATION WORKFLOW
======================================================
Automated customer support ticket handling and response

This workflow type uses the savings parameters you provided:
- 20 tasks per week
- 30 minutes per task
- $40/hour labor cost
- 85% automation rate
- 5% error rate
- $20 per error cost

Annual savings: $18,564
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow_savings_calculator import calculate_savings

# Calculate savings using your parameters
SAVINGS = calculate_savings(
    tasks_per_week=20,
    time_per_task_minutes=30,
    hourly_wage=40,
    automation_percent=0.85,
    error_rate=0.05,
    cost_per_error=20
)

WORKFLOW_TYPE_CUSTOMER_SERVICE = {
    "id": "customer_service.ticket_automation",
    "name": "Customer Service Ticket Automation",
    "description": "Automatically classify, prioritize, and respond to customer support tickets",
    "domain": "commerce",  # Routes to Commerce Council
    "category": "customer_service",
    "estimated_duration_minutes": 5,
    
    "required_inputs": [
        {
            "name": "ticket_source",
            "type": "string",
            "description": "Source of tickets (email, chat, portal)",
            "required": True,
            "options": ["email", "live_chat", "support_portal", "social_media"]
        },
        {
            "name": "response_templates",
            "type": "array",
            "description": "Pre-approved response templates by category",
            "required": True,
            "default": ["order_status", "returns", "technical_support", "billing"]
        },
        {
            "name": "escalation_keywords",
            "type": "array",
            "description": "Keywords that trigger human escalation",
            "required": False,
            "default": ["angry", "lawsuit", "manager", "cancel account", "urgent"]
        },
        {
            "name": "auto_response_threshold",
            "type": "number",
            "description": "Confidence threshold for auto-response (0.0-1.0)",
            "required": False,
            "default": 0.85
        },
        {
            "name": "business_hours",
            "type": "object",
            "description": "Business hours for human escalation availability",
            "required": False,
            "default": {
                "start": "09:00",
                "end": "17:00",
                "timezone": "America/New_York",
                "weekdays_only": True
            }
        },
        {
            "name": "notification_email",
            "type": "email",
            "description": "Email for escalation notifications",
            "required": True
        }
    ],
    
    "outputs": [
        "tickets_processed",
        "tickets_auto_resolved",
        "tickets_escalated",
        "average_response_time_seconds",
        "customer_satisfaction_score",
        "execution_log_url"
    ],
    
    "calculated_savings": {
        "tasks_per_week": 20,
        "time_per_task_minutes": 30,
        "hourly_wage": 40,
        "automation_percent": 0.85,
        "weekly_savings": round(SAVINGS.total_weekly_savings, 2),
        "monthly_savings": round(SAVINGS.total_weekly_savings * 4.33, 2),
        "annual_savings": round(SAVINGS.total_annual_savings, 2),
        "time_saved_hours_per_week": round(SAVINGS.automated_hours_per_week, 2),
        "error_reduction_percent": round(((SAVINGS.errors_before - SAVINGS.errors_after) / SAVINGS.errors_before * 100), 2)
    },
    
    "execution_steps": [
        {
            "step": 1,
            "name": "Fetch New Tickets",
            "description": "Pull unprocessed tickets from ticket_source",
            "duration_seconds": 30,
            "actions": ["connect_to_source", "query_new_tickets", "parse_ticket_data"]
        },
        {
            "step": 2,
            "name": "Classify Tickets",
            "description": "Use AI to classify ticket category and urgency",
            "duration_seconds": 60,
            "actions": ["analyze_content", "extract_intent", "assign_category", "calculate_urgency"]
        },
        {
            "step": 3,
            "name": "Check Escalation Criteria",
            "description": "Determine if ticket requires human intervention",
            "duration_seconds": 15,
            "actions": ["scan_for_keywords", "check_sentiment", "evaluate_complexity"]
        },
        {
            "step": 4,
            "name": "Generate Response",
            "description": "Create AI-powered response using templates",
            "duration_seconds": 90,
            "actions": ["select_template", "personalize_response", "add_relevant_links", "format_message"]
        },
        {
            "step": 5,
            "name": "Quality Check",
            "description": "Validate response quality and accuracy",
            "duration_seconds": 30,
            "actions": ["check_grammar", "verify_policy_compliance", "validate_links"]
        },
        {
            "step": 6,
            "name": "Send or Escalate",
            "description": "Either send auto-response or escalate to human",
            "duration_seconds": 45,
            "actions": ["route_decision", "send_response", "create_escalation_ticket", "notify_team"]
        },
        {
            "step": 7,
            "name": "Record Metrics",
            "description": "Log performance metrics and outcomes",
            "duration_seconds": 30,
            "actions": ["save_to_database", "update_dashboard", "calculate_satisfaction"]
        }
    ],
    
    "success_criteria": {
        "auto_resolution_rate": ">=80%",
        "average_response_time": "<=5 minutes",
        "customer_satisfaction": ">=4.0/5.0",
        "escalation_rate": "<=20%",
        "policy_compliance": "100%"
    },
    
    "failure_conditions": [
        "API connection timeout (>30 seconds)",
        "Response confidence <85% without escalation",
        "Policy violation detected",
        "Profanity filter triggered without escalation"
    ],
    
    "council_oversight": {
        "required": True,
        "council_domain": "commerce",
        "approval_threshold": "simple_majority",
        "review_criteria": [
            "Response quality and professionalism",
            "Customer satisfaction impact",
            "Brand voice consistency",
            "Escalation appropriateness",
            "Cost savings vs. quality trade-off"
        ]
    }
}


def register_customer_service_workflow():
    """Register customer service automation workflow in database"""
    from db import SessionLocal
    from models import WorkflowType
    from datetime import datetime
    
    session = SessionLocal()
    
    try:
        # Check if already exists
        existing = session.query(WorkflowType).filter(
            WorkflowType.id == WORKFLOW_TYPE_CUSTOMER_SERVICE["id"]
        ).first()
        
        if existing:
            print(f"⚠️  Workflow type '{WORKFLOW_TYPE_CUSTOMER_SERVICE['id']}' already exists")
            return existing
        
        # Create new workflow type
        workflow_type = WorkflowType(
            id=WORKFLOW_TYPE_CUSTOMER_SERVICE["id"],
            name=WORKFLOW_TYPE_CUSTOMER_SERVICE["name"],
            description=WORKFLOW_TYPE_CUSTOMER_SERVICE["description"],
            domain=WORKFLOW_TYPE_CUSTOMER_SERVICE["domain"],
            category=WORKFLOW_TYPE_CUSTOMER_SERVICE["category"],
            required_inputs=WORKFLOW_TYPE_CUSTOMER_SERVICE["required_inputs"],
            expected_outputs=WORKFLOW_TYPE_CUSTOMER_SERVICE["outputs"],
            estimated_duration_minutes=WORKFLOW_TYPE_CUSTOMER_SERVICE["estimated_duration_minutes"],
            estimated_savings_weekly=float(WORKFLOW_TYPE_CUSTOMER_SERVICE["calculated_savings"]["weekly_savings"]),
            created_at=datetime.utcnow()
        )
        
        session.add(workflow_type)
        session.commit()
        session.refresh(workflow_type)
        
        print(f"✅ Workflow type '{WORKFLOW_TYPE_CUSTOMER_SERVICE['id']}' registered successfully!")
        print(f"   Domain: {workflow_type.domain}")
        print(f"   Weekly Savings: ${workflow_type.estimated_savings_weekly:.2f}")
        print(f"   Annual Savings: ${workflow_type.estimated_savings_weekly * 52:.2f}")
        print(f"   Time Saved: {WORKFLOW_TYPE_CUSTOMER_SERVICE['calculated_savings']['time_saved_hours_per_week']} hours/week")
        
        return workflow_type
        
    except Exception as e:
        session.rollback()
        print(f"❌ Failed to register workflow type: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOMER SERVICE TICKET AUTOMATION - WORKFLOW TYPE")
    print("=" * 60)
    print()
    print("📋 Workflow Details:")
    print(f"   ID: {WORKFLOW_TYPE_CUSTOMER_SERVICE['id']}")
    print(f"   Name: {WORKFLOW_TYPE_CUSTOMER_SERVICE['name']}")
    print(f"   Domain: {WORKFLOW_TYPE_CUSTOMER_SERVICE['domain']}")
    print(f"   Category: {WORKFLOW_TYPE_CUSTOMER_SERVICE['category']}")
    print()
    print("💰 Calculated Savings:")
    print(f"   Weekly: ${WORKFLOW_TYPE_CUSTOMER_SERVICE['calculated_savings']['weekly_savings']}")
    print(f"   Monthly: ${WORKFLOW_TYPE_CUSTOMER_SERVICE['calculated_savings']['monthly_savings']}")
    print(f"   Annual: ${WORKFLOW_TYPE_CUSTOMER_SERVICE['calculated_savings']['annual_savings']}")
    print(f"   Time Saved: {WORKFLOW_TYPE_CUSTOMER_SERVICE['calculated_savings']['time_saved_hours_per_week']} hours/week")
    print(f"   Error Reduction: {WORKFLOW_TYPE_CUSTOMER_SERVICE['calculated_savings']['error_reduction_percent']}%")
    print()
    print("🔧 Execution Steps:")
    for step in WORKFLOW_TYPE_CUSTOMER_SERVICE["execution_steps"]:
        print(f"   {step['step']}. {step['name']} ({step['duration_seconds']}s)")
    print()
    print("=" * 60)
    print("Registering in database...")
    print("=" * 60)
    
    # Register the workflow type
    register_customer_service_workflow()
