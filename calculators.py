"""
Automation Savings Calculator
==============================

Reusable calculation engine for ROI analysis across all systems.
Used by Flask dashboard, Jermaine agent, and analytics.
"""

from dataclasses import dataclass


@dataclass
class SavingsInput:
    """Input parameters for savings calculation"""
    tasks_per_week: float
    time_per_task_minutes: float
    hourly_wage: float
    automation_percent: float  # 0-1 (e.g., 0.7 for 70%)
    error_rate: float          # 0-1 (e.g., 0.1 for 10%)
    cost_per_error: float
    value_per_accelerated_task: float = 0.0  # Optional: revenue value


@dataclass
class SavingsResult:
    """Calculated savings breakdown"""
    weekly_savings: float
    monthly_savings: float
    yearly_savings: float
    hours_saved_per_week: float
    error_savings_weekly: float
    scaling_savings_weekly: float
    total_weekly_savings: float


def calculate_savings(inp: SavingsInput) -> SavingsResult:
    """
    Calculate comprehensive automation savings
    
    Factors considered:
    1. Labor cost reduction (time saved × hourly wage)
    2. Error prevention savings (errors avoided × cost per error)
    3. Scaling value (tasks accelerated × value per task)
    
    Args:
        inp: SavingsInput with all calculation parameters
        
    Returns:
        SavingsResult with complete savings breakdown
    """
    # Base labor hours per week
    total_minutes = inp.tasks_per_week * inp.time_per_task_minutes
    total_hours = total_minutes / 60.0

    # Hours saved by automation
    hours_saved = total_hours * inp.automation_percent

    # Labor cost savings
    labor_savings_weekly = hours_saved * inp.hourly_wage

    # Error reduction savings
    errors_per_week = inp.tasks_per_week * inp.error_rate
    error_savings_weekly = (
        errors_per_week * inp.cost_per_error * inp.automation_percent
    )

    # Business scaling value (optional)
    accelerated_tasks = inp.tasks_per_week * inp.automation_percent
    scaling_savings_weekly = (
        accelerated_tasks * inp.value_per_accelerated_task
    )

    # Total calculations
    total_weekly = (
        labor_savings_weekly +
        error_savings_weekly +
        scaling_savings_weekly
    )
    monthly = total_weekly * 4.33  # More accurate than 4
    yearly = total_weekly * 52

    return SavingsResult(
        weekly_savings=round(total_weekly, 2),
        monthly_savings=round(monthly, 2),
        yearly_savings=round(yearly, 2),
        hours_saved_per_week=round(hours_saved, 2),
        error_savings_weekly=round(error_savings_weekly, 2),
        scaling_savings_weekly=round(scaling_savings_weekly, 2),
        total_weekly_savings=round(total_weekly, 2),
    )


def get_effectiveness_rating(yearly_savings: float) -> str:
    """
    Classify automation effectiveness based on yearly value
    
    Args:
        yearly_savings: Total yearly savings amount
        
    Returns:
        Rating string (STELLAR, EXCELLENT, STRONG, VIABLE, MARGINAL)
    """
    if yearly_savings >= 20000:
        return "STELLAR"
    elif yearly_savings >= 10000:
        return "EXCELLENT"
    elif yearly_savings >= 5000:
        return "STRONG"
    elif yearly_savings >= 1000:
        return "VIABLE"
    else:
        return "MARGINAL"


def format_currency(amount: float) -> str:
    """Format amount as currency string"""
    return f"${amount:,.2f}"


def format_hours(hours: float) -> str:
    """Format hours with appropriate precision"""
    return f"{hours:.1f} hours"


# Example usage
if __name__ == "__main__":
    # Sample calculation
    sample_input = SavingsInput(
        tasks_per_week=200,
        time_per_task_minutes=10,
        hourly_wage=25.0,
        automation_percent=0.70,
        error_rate=0.10,
        cost_per_error=15.0,
        value_per_accelerated_task=0.0
    )
    
    result = calculate_savings(sample_input)
    rating = get_effectiveness_rating(result.yearly_savings)
    
    print("=" * 60)
    print("AUTOMATION SAVINGS CALCULATION")
    print("=" * 60)
    print(f"Weekly Savings:  {format_currency(result.weekly_savings)}")
    print(f"Monthly Savings: {format_currency(result.monthly_savings)}")
    print(f"Yearly Savings:  {format_currency(result.yearly_savings)}")
    print(f"Hours Saved/Week: {format_hours(result.hours_saved_per_week)}")
    print(f"Effectiveness: {rating}")
    print("=" * 60)
