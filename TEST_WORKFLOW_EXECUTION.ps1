# Test Execute-Action Flow with Customer Follow-up Workflow
# 200 tasks/week, 10 min each, $25/hr, 70% automation

Write-Host "`n🧪 TESTING WORKFLOW EXECUTION" -ForegroundColor Cyan
Write-Host "=" -NoNewline; for($i=0;$i -lt 50;$i++){Write-Host "=" -NoNewline}
Write-Host "`n"

# Test data
$workflowRequest = @{
    agent_id = "agent_jermaine_super_action"
    workflow_id = "customer_followup"
    inputs = @{
        messages_per_week = "200"
        time_per_message = "10"
        hourly_rate = "25"
        automation_percentage = "70"
    }
} | ConvertTo-Json -Depth 3

Write-Host "📋 Workflow Request:" -ForegroundColor Yellow
Write-Host $workflowRequest
Write-Host ""

try {
    # Send workflow execution request
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/workflow/execute" `
        -Method POST `
        -Body $workflowRequest `
        -ContentType "application/json" `
        -ErrorAction Stop
    
    Write-Host "✅ WORKFLOW DEPLOYED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 ROI Metrics:" -ForegroundColor Cyan
    Write-Host "  • Time Saved: $($response.execution_details.roi_metrics.time_saved_per_week) hrs/week" -ForegroundColor White
    Write-Host "  • Weekly Savings: `$$($response.execution_details.roi_metrics.weekly_savings)" -ForegroundColor White
    Write-Host "  • Monthly Savings: `$$($response.execution_details.roi_metrics.monthly_savings)" -ForegroundColor Green
    Write-Host "  • Annual Savings: `$$($response.execution_details.roi_metrics.annual_savings)" -ForegroundColor Green
    Write-Host "  • Automation: $($response.execution_details.roi_metrics.automation_percentage)%" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Workflow ID: $($response.workflow_id)" -ForegroundColor Yellow
    Write-Host "🔗 Dashboard: $($response.dashboard_url)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✨ Next Steps:" -ForegroundColor Cyan
    foreach ($step in $response.next_steps) {
        Write-Host "   • $step" -ForegroundColor White
    }
    Write-Host ""
    
} catch {
    Write-Host "❌ ERROR: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Make sure Flask is running on port 5000" -ForegroundColor Yellow
    Write-Host "   Run: python flask_dashboard.py" -ForegroundColor Gray
}

Write-Host ""
