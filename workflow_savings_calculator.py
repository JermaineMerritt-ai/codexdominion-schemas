"""
CODEX DOMINION - WORKFLOW SAVINGS CALCULATOR
==============================================
Calculate ROI and time savings for automated workflows

Usage:
    from workflow_savings_calculator import calculate_savings
    
    savings = calculate_savings(
        tasks_per_week=20,
        time_per_task_minutes=30,
        hourly_wage=40,
        automation_percent=0.85,
        error_rate=0.05,
        cost_per_error=20
    )
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class WorkflowSavings:
    """Comprehensive savings calculation result"""
    # Time savings
    total_hours_per_week: float
    automated_hours_per_week: float
    manual_hours_per_week: float
    
    # Cost savings
    labor_cost_before: float
    labor_cost_after: float
    labor_savings_weekly: float
    
    # Error savings
    errors_before: float
    errors_after: float
    error_cost_before: float
    error_cost_after: float
    error_savings_weekly: float
    
    # Total savings
    total_weekly_savings: float
    total_annual_savings: float
    
    # Efficiency metrics
    time_saved_percent: float
    roi_percent: float
    payback_period_weeks: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "time_savings": {
                "total_hours_per_week": round(self.total_hours_per_week, 2),
                "automated_hours_per_week": round(self.automated_hours_per_week, 2),
                "manual_hours_per_week": round(self.manual_hours_per_week, 2),
                "time_saved_percent": round(self.time_saved_percent, 2)
            },
            "cost_savings": {
                "labor_cost_before": round(self.labor_cost_before, 2),
                "labor_cost_after": round(self.labor_cost_after, 2),
                "labor_savings_weekly": round(self.labor_savings_weekly, 2),
                "error_cost_before": round(self.error_cost_before, 2),
                "error_cost_after": round(self.error_cost_after, 2),
                "error_savings_weekly": round(self.error_savings_weekly, 2)
            },
            "total_savings": {
                "weekly": round(self.total_weekly_savings, 2),
                "monthly": round(self.total_weekly_savings * 4.33, 2),
                "annual": round(self.total_annual_savings, 2)
            },
            "efficiency_metrics": {
                "roi_percent": round(self.roi_percent, 2),
                "payback_period_weeks": round(self.payback_period_weeks, 2) if self.payback_period_weeks else None
            }
        }


def calculate_savings(
    tasks_per_week: int,
    time_per_task_minutes: int,
    hourly_wage: float,
    automation_percent: float = 0.85,
    error_rate: float = 0.05,
    cost_per_error: float = 20,
    implementation_cost: float = 0
) -> WorkflowSavings:
    """
    Calculate comprehensive savings for a workflow automation
    
    Args:
        tasks_per_week: Number of tasks performed per week
        time_per_task_minutes: Time in minutes per task
        hourly_wage: Hourly wage of worker (USD)
        automation_percent: Percentage of task that can be automated (0.0-1.0)
        error_rate: Error rate as decimal (0.0-1.0)
        cost_per_error: Cost per error in USD
        implementation_cost: One-time cost to implement automation
    
    Returns:
        WorkflowSavings object with complete breakdown
    
    Example:
        >>> savings = calculate_savings(
        ...     tasks_per_week=20,
        ...     time_per_task_minutes=30,
        ...     hourly_wage=40,
        ...     automation_percent=0.85,
        ...     error_rate=0.05,
        ...     cost_per_error=20
        ... )
        >>> print(f"Weekly savings: ${savings.total_weekly_savings:.2f}")
        Weekly savings: $357.00
    """
    
    # Time calculations
    total_hours_per_week = (tasks_per_week * time_per_task_minutes) / 60
    automated_hours_per_week = total_hours_per_week * automation_percent
    manual_hours_per_week = total_hours_per_week * (1 - automation_percent)
    
    # Labor cost calculations
    labor_cost_before = total_hours_per_week * hourly_wage
    labor_cost_after = manual_hours_per_week * hourly_wage
    labor_savings_weekly = labor_cost_before - labor_cost_after
    
    # Error calculations
    errors_before = tasks_per_week * error_rate
    errors_after = errors_before * (1 - automation_percent)
    error_cost_before = errors_before * cost_per_error
    error_cost_after = errors_after * cost_per_error
    error_savings_weekly = error_cost_before - error_cost_after
    
    # Total savings
    total_weekly_savings = labor_savings_weekly + error_savings_weekly
    total_annual_savings = total_weekly_savings * 52
    
    # Efficiency metrics
    time_saved_percent = automation_percent * 100
    roi_percent = (total_annual_savings / implementation_cost * 100) if implementation_cost > 0 else float('inf')
    payback_period_weeks = implementation_cost / total_weekly_savings if total_weekly_savings > 0 else float('inf')
    
    return WorkflowSavings(
        total_hours_per_week=total_hours_per_week,
        automated_hours_per_week=automated_hours_per_week,
        manual_hours_per_week=manual_hours_per_week,
        labor_cost_before=labor_cost_before,
        labor_cost_after=labor_cost_after,
        labor_savings_weekly=labor_savings_weekly,
        errors_before=errors_before,
        errors_after=errors_after,
        error_cost_before=error_cost_before,
        error_cost_after=error_cost_after,
        error_savings_weekly=error_savings_weekly,
        total_weekly_savings=total_weekly_savings,
        total_annual_savings=total_annual_savings,
        time_saved_percent=time_saved_percent,
        roi_percent=roi_percent,
        payback_period_weeks=payback_period_weeks
    )


def format_savings_summary(savings: WorkflowSavings) -> str:
    """Format savings as a human-readable summary"""
    return f"""
💰 WORKFLOW SAVINGS ANALYSIS
============================

⏱️  TIME SAVINGS
   • Total time: {savings.total_hours_per_week:.1f} hours/week
   • Automated: {savings.automated_hours_per_week:.1f} hours/week ({savings.time_saved_percent:.0f}%)
   • Still manual: {savings.manual_hours_per_week:.1f} hours/week

💵 COST SAVINGS
   • Labor before: ${savings.labor_cost_before:.2f}/week
   • Labor after: ${savings.labor_cost_after:.2f}/week
   • Labor saved: ${savings.labor_savings_weekly:.2f}/week
   
   • Error cost before: ${savings.error_cost_before:.2f}/week
   • Error cost after: ${savings.error_cost_after:.2f}/week
   • Error cost saved: ${savings.error_savings_weekly:.2f}/week

📊 TOTAL SAVINGS
   • Weekly: ${savings.total_weekly_savings:.2f}
   • Monthly: ${savings.total_weekly_savings * 4.33:.2f}
   • Annual: ${savings.total_annual_savings:.2f}

🎯 ROI METRICS
   • Time saved: {savings.time_saved_percent:.0f}%
   • Errors reduced: {((savings.errors_before - savings.errors_after) / savings.errors_before * 100):.0f}%
   • Payback period: {savings.payback_period_weeks:.1f} weeks
"""


# Example usage
if __name__ == "__main__":
    # Example 1: Customer service automation
    print("=" * 50)
    print("EXAMPLE 1: Customer Service Automation")
    print("=" * 50)
    
    savings1 = calculate_savings(
        tasks_per_week=20,
        time_per_task_minutes=30,
        hourly_wage=40,
        automation_percent=0.85,
        error_rate=0.05,
        cost_per_error=20
    )
    
    print(format_savings_summary(savings1))
    
    # Example 2: Data entry automation
    print("=" * 50)
    print("EXAMPLE 2: Data Entry Automation")
    print("=" * 50)
    
    savings2 = calculate_savings(
        tasks_per_week=100,
        time_per_task_minutes=10,
        hourly_wage=25,
        automation_percent=0.95,
        error_rate=0.10,
        cost_per_error=15,
        implementation_cost=5000
    )
    
    print(format_savings_summary(savings2))
    
    # Example 3: Website creation (from our workflow type)
    print("=" * 50)
    print("EXAMPLE 3: Website Creation")
    print("=" * 50)
    
    savings3 = calculate_savings(
        tasks_per_week=1,
        time_per_task_minutes=180,  # 3 hours
        hourly_wage=75,  # Professional developer rate
        automation_percent=0.80,
        error_rate=0.15,  # Higher error rate for manual builds
        cost_per_error=100  # Higher cost for website errors
    )
    
    print(format_savings_summary(savings3))
    
    # JSON output
    print("=" * 50)
    print("JSON OUTPUT (for API responses)")
    print("=" * 50)
    import json
    print(json.dumps(savings1.to_dict(), indent=2))
