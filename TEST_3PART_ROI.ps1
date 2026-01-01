# Test 3-Part ROI Calculator
# Labor + Error + Scaling Savings

Write-Host "`n🎯 TESTING 3-PART ROI CALCULATOR" -ForegroundColor Cyan
Write-Host "=" -NoNewline; for($i=0;$i -lt 70;$i++){Write-Host "=" -NoNewline}
Write-Host "`n"

# Example inputs with ALL 3 ROI components
$inputs = @{
    tasks_per_week = 200
    time_per_task = 10
    hourly_wage = 25
    automation_percent = 0.7
    errors_per_month = 5
    cost_per_error = 500
    value_per_accelerated_task = 50
}

Write-Host "📋 INPUTS:" -ForegroundColor Yellow
Write-Host "  • Tasks per week: $($inputs.tasks_per_week)" -ForegroundColor White
Write-Host "  • Time per task: $($inputs.time_per_task) minutes" -ForegroundColor White
Write-Host "  • Hourly wage: `$$($inputs.hourly_wage)" -ForegroundColor White
Write-Host "  • Automation: $($inputs.automation_percent*100)%" -ForegroundColor White
Write-Host "  • Errors per month: $($inputs.errors_per_month)" -ForegroundColor White
Write-Host "  • Cost per error: `$$($inputs.cost_per_error)" -ForegroundColor White
Write-Host "  • Value per accelerated task: `$$($inputs.value_per_accelerated_task)" -ForegroundColor White
Write-Host ""

# Calculate 3-Part ROI
$tasks = $inputs.tasks_per_week
$time_min = $inputs.time_per_task
$hourly = $inputs.hourly_wage
$auto_pct = $inputs.automation_percent
$errors_month = $inputs.errors_per_month
$error_cost = $inputs.cost_per_error
$task_value = $inputs.value_per_accelerated_task

# 1. LABOR SAVINGS
$hours_week = ($tasks * $time_min) / 60
$auto_hours = $hours_week * $auto_pct
$labor_weekly = $auto_hours * $hourly
$labor_monthly = $labor_weekly * 4.33
$labor_annual = $labor_monthly * 12

# 2. ERROR SAVINGS
$error_monthly = ($error_cost * $errors_month * $auto_pct)
$error_annual = $error_monthly * 12

# 3. SCALING SAVINGS
$accelerated_tasks = $tasks * $auto_pct
$scaling_weekly = $accelerated_tasks * $task_value
$scaling_monthly = $scaling_weekly * 4.33
$scaling_annual = $scaling_monthly * 12

# TOTAL ROI
$total_monthly = $labor_monthly + $error_monthly + $scaling_monthly
$total_annual = $labor_annual + $error_annual + $scaling_annual

Write-Host "🎯 HERE'S WHAT YOUR AUTOMATION UNLOCKS:" -ForegroundColor Green
Write-Host ""
Write-Host "• Weekly savings: `$$([math]::Round($labor_weekly + $scaling_weekly, 0))" -ForegroundColor White
Write-Host "• Monthly savings: `$$([math]::Round($total_monthly, 0))" -ForegroundColor White
Write-Host "• Yearly savings: `$$([math]::Round($total_annual, 0))" -ForegroundColor White
Write-Host "• Error reduction: $($auto_pct*100)%" -ForegroundColor White
Write-Host "• Time reclaimed: $([math]::Round($auto_hours, 1)) hours/week" -ForegroundColor White
Write-Host ""

Write-Host "📊 ROI BREAKDOWN:" -ForegroundColor Cyan
Write-Host "   • Labor savings: `$$([math]::Round($labor_monthly, 0))/month" -ForegroundColor White
Write-Host "   • Error reduction: `$$([math]::Round($error_monthly, 0))/month" -ForegroundColor White
Write-Host "   • Scaling value: `$$([math]::Round($scaling_monthly, 0))/month" -ForegroundColor White
Write-Host ""

$workdays_saved = [math]::Round($auto_hours / 8, 1)
$employees_eq = [math]::Round($auto_hours / 40, 2)

Write-Host "💡 EQUIVALENT TO:" -ForegroundColor Cyan
Write-Host "   • Saving $workdays_saved workdays per week" -ForegroundColor White
Write-Host "   • $employees_eq full-time employees" -ForegroundColor White
Write-Host ""

Write-Host "✅ Would you like me to build and activate this workflow now?" -ForegroundColor Green
Write-Host ""
