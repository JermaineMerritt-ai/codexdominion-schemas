#!/usr/bin/env pwsh
# Test Chat API Script

Write-Host "`n🧪 TESTING CHAT API SYSTEM`n" -ForegroundColor Cyan

# Test 1: Check if Flask is running
Write-Host "1️⃣  Checking Flask server..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod "http://localhost:5000/api/agents" -TimeoutSec 3
    Write-Host "   ✅ Flask is running ($($health.agents.Count) agents loaded)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Flask not running: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Verify agent exists
Write-Host "`n2️⃣  Checking for Jermaine Super Action AI..." -ForegroundColor Yellow
try {
    $agent = Invoke-RestMethod "http://localhost:5000/api/agents/agent_jermaine_super_action"
    Write-Host "   ✅ Agent found: $($agent.name)" -ForegroundColor Green
    Write-Host "   📋 Role: $($agent.role)" -ForegroundColor Gray
    Write-Host "   🎭 Personality: $($agent.personality)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Agent not found: $_" -ForegroundColor Red
    exit 1
}

# Test 3: Send chat message
Write-Host "`n3️⃣  Sending chat message..." -ForegroundColor Yellow
$body = @{
    agent_id = "agent_jermaine_super_action"
    message = "Help me plan a 3-step launch sequence for my new platform."
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body

    Write-Host "   ✅ Chat successful!`n" -ForegroundColor Green
    Write-Host "🤖 Agent: $($response.agent_name)" -ForegroundColor Cyan
    Write-Host "⏰ Time: $($response.timestamp)`n" -ForegroundColor Gray
    Write-Host "📝 Response:" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host $response.response -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray
    
    Write-Host "✨ ALL TESTS PASSED!`n" -ForegroundColor Green
    
} catch {
    Write-Host "   ❌ Chat failed: $_" -ForegroundColor Red
    exit 1
}
