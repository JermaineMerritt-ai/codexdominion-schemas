# Simple Flask Test Script
Write-Host "Starting Flask..." -ForegroundColor Cyan

$job = Start-Job -ScriptBlock {
    Set-Location "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
    python flask_dashboard.py
}

Start-Sleep -Seconds 5

Write-Host "Testing..." -ForegroundColor Yellow

try {
    $health = Invoke-RestMethod "http://localhost:5000/api/health"
    Write-Host "Flask OK" -ForegroundColor Green
    
    $body = '{"agent_id":"agent_jermaine_super_action","message":"Automate my weekly customer follow-up messages"}'
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Workflow Detected: $($response.workflow_detected)" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "Flask running at http://localhost:5000" -ForegroundColor Green
Wait-Job $job
