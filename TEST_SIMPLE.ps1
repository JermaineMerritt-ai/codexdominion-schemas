# Simple Execute-Action Flow Test

Write-Host "🧪 TESTING EXECUTE-ACTION FLOW" -ForegroundColor Cyan
Write-Host ""

# Test action detection
Write-Host "1️⃣  Testing workflow detection..." -ForegroundColor Yellow
$body = @{
    agent_id = "agent_jermaine_super_action"
    message = "Automate my weekly customer follow-up messages"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "   ✅ Response received!" -ForegroundColor Green
    Write-Host "   Action Type: $($response.action_type)" -ForegroundColor Gray
    Write-Host "   Workflow Detected: $($response.workflow_detected)" -ForegroundColor Gray
    if ($response.workflow_id) {
        Write-Host "   Workflow ID: $($response.workflow_id)" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "   Agent Response:" -ForegroundColor Cyan
    Write-Host "   $($response.response)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "✨ Test complete!" -ForegroundColor Green
