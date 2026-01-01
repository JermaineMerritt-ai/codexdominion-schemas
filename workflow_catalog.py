"""
Workflow Catalog - Defines workflow types with metadata and calculator profiles
Used for domain determination, council oversight, and automated calculator configuration.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class WorkflowType:
    """Defines a workflow type with its metadata and requirements."""
    id: str
    name: str
    description: str
    category: str
    required_inputs: List[str]
    domain: str
    default_calculator_profile: Dict[str, Any]


WORKFLOW_TYPES: Dict[str, WorkflowType] = {
    "customer_followup": WorkflowType(
        id="customer_followup",
        name="Customer Follow-up Automation",
        description="Automate weekly follow-up messages to existing customers.",
        category="crm",
        required_inputs=[
            "tasks_per_week",
            "time_per_task_minutes",
            "hourly_wage",
            "automation_percent",
            "error_rate",
            "cost_per_error"
        ],
        domain="commerce",
        default_calculator_profile={
            "value_per_accelerated_task": 0
        }
    ),
    "invoice_reminders": WorkflowType(
        id="invoice_reminders",
        name="Invoice Reminder Automation",
        description="Send automated reminders for unpaid invoices.",
        category="finance",
        required_inputs=[
            "invoices_per_month",
            "time_per_invoice_minutes",
            "hourly_wage",
            "automation_percent"
        ],
        domain="commerce",
        default_calculator_profile={
            "error_rate": 0.05,
            "cost_per_error": 25,
            "value_per_accelerated_task": 15
        }
    ),
    "content_scheduler": WorkflowType(
        id="content_scheduler",
        name="Content Publishing Scheduler",
        description="Schedule and publish content across platforms automatically.",
        category="marketing",
        required_inputs=[
            "posts_per_week",
            "time_per_post_minutes",
            "hourly_wage",
            "automation_percent"
        ],
        domain="media",
        default_calculator_profile={
            "error_rate": 0.02,
            "cost_per_error": 10,
            "value_per_accelerated_task": 20
        }
    ),
    "data_entry_automation": WorkflowType(
        id="data_entry_automation",
        name="Data Entry Automation",
        description="Automate repetitive data entry tasks across systems.",
        category="operations",
        required_inputs=[
            "entries_per_week",
            "time_per_entry_minutes",
            "hourly_wage",
            "automation_percent"
        ],
        domain="automation",
        default_calculator_profile={
            "error_rate": 0.15,
            "cost_per_error": 30,
            "value_per_accelerated_task": 0
        }
    ),
    "report_generation": WorkflowType(
        id="report_generation",
        name="Automated Report Generation",
        description="Generate and distribute reports automatically on schedule.",
        category="analytics",
        required_inputs=[
            "reports_per_month",
            "time_per_report_hours",
            "hourly_wage",
            "automation_percent"
        ],
        domain="analytics",
        default_calculator_profile={
            "error_rate": 0.03,
            "cost_per_error": 50,
            "value_per_accelerated_task": 100
        }
    ),
    "email_triage": WorkflowType(
        id="email_triage",
        name="Email Triage and Routing",
        description="Automatically categorize and route incoming emails.",
        category="communication",
        required_inputs=[
            "emails_per_day",
            "time_per_email_minutes",
            "hourly_wage",
            "automation_percent"
        ],
        domain="automation",
        default_calculator_profile={
            "error_rate": 0.08,
            "cost_per_error": 15,
            "value_per_accelerated_task": 5
        }
    )
}


def get_workflow_type(workflow_type_id: str) -> Optional[WorkflowType]:
    """Get workflow type by ID."""
    return WORKFLOW_TYPES.get(workflow_type_id)


def list_workflow_types() -> Dict[str, Any]:
    """List all available workflow types with metadata."""
    return {
        wid: {
            "id": wt.id,
            "name": wt.name,
            "description": wt.description,
            "category": wt.category,
            "domain": wt.domain,
            "required_inputs": wt.required_inputs
        }
        for wid, wt in WORKFLOW_TYPES.items()
    }


def get_workflow_domain(workflow_type_id: str) -> Optional[str]:
    """Get the domain for a workflow type."""
    wt = WORKFLOW_TYPES.get(workflow_type_id)
    return wt.domain if wt else None


def get_calculator_defaults(workflow_type_id: str) -> Dict[str, Any]:
    """Get default calculator profile for a workflow type."""
    wt = WORKFLOW_TYPES.get(workflow_type_id)
    return wt.default_calculator_profile if wt else {}


def merge_calculator_inputs(workflow_type_id: str, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge user inputs with workflow type defaults.
    User inputs take precedence over defaults.
    """
    defaults = get_calculator_defaults(workflow_type_id)
    merged = defaults.copy()
    merged.update(user_inputs)
    return merged
