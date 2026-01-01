# Start Flask Dashboard and Test Execute-Action Flow

Write-Host "`n🔥 STARTING FLASK DASHBOARD WITH EXECUTE-ACTION FLOW`n" -ForegroundColor Cyan

# Kill any existing Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Start Flask in background
$job = Start-Job -ScriptBlock {
    Set-Location "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
    python flask_dashboard.py 2>&1
}

Write-Host "Waiting for Flask to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test health
Write-Host "`n🧪 Testing Flask..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod "http://localhost:5000/api/health" -ErrorAction Stop
    Write-Host "✅ Flask is running`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Flask not responding!" -ForegroundColor Red
    Stop-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job -ErrorAction SilentlyContinue
    exit 1
}

# Test Execute-Action Flow  
Write-Host "🧪 TESTING EXECUTE-ACTION FLOW`n" -ForegroundColor Cyan

$body = @{
    agent_id = "agent_jermaine_super_action"
    message = "Automate my weekly customer follow-up messages"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Action Type: $($response.action_type)" -ForegroundColor Gray
    Write-Host "Workflow Detected: $($response.workflow_detected)" -ForegroundColor Gray
    
    if ($response.workflow_detected) {
        Write-Host "Workflow ID: $($response.workflow_id)" -ForegroundColor Yellow
        Write-Host "✅ SUCCESS!" -ForegroundColor Green
    } else {
        Write-Host "❌ Workflow not detected" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ ERROR: $_" -ForegroundColor Red
}

Write-Host "`n✨ Flask running on http://localhost:5000`n" -ForegroundColor Green

# Keep job running
Wait-Job $job
