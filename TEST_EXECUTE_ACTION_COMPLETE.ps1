# =============================================================================
# EXECUTE-ACTION FLOW - COMPLETE TEST SUITE
# =============================================================================

Write-Host "`n🔥 EXECUTE-ACTION FLOW - COMPREHENSIVE TESTING" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Start Flask in background
Write-Host "1️⃣  Starting Flask server..." -ForegroundColor Yellow
$job = Start-Job -ScriptBlock {
    Set-Location "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
    python flask_dashboard.py
}

Start-Sleep -Seconds 5

# Test 1: Health check
Write-Host "2️⃣  Health check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod "http://localhost:5000/api/health"
    Write-Host "   ✅ Server running: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Server not responding" -ForegroundColor Red
    Stop-Job $job; Remove-Job $job
    exit 1
}

Write-Host ""

# Test 2: Conversational message (should NOT trigger workflow)
Write-Host "3️⃣  Test: Conversational message..." -ForegroundColor Yellow
try {
    $body = @{
        agent_id = "agent_jermaine_super_action"
        message = "What can you help me with?"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    if ($response.action_type -eq "chat") {
        Write-Host "   ✅ Correctly identified as chat" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Expected 'chat', got: $($response.action_type)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Action request (SHOULD trigger workflow)
Write-Host "4️⃣  Test: Action request (workflow detection)..." -ForegroundColor Yellow
try {
    $body = @{
        agent_id = "agent_jermaine_super_action"
        message = "Automate my weekly customer follow-up messages"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "   📊 Results:" -ForegroundColor Cyan
    Write-Host "      Action Type: $($response.action_type)" -ForegroundColor White
    Write-Host "      Workflow Detected: $($response.workflow_detected)" -ForegroundColor White
    
    if ($response.workflow_detected) {
        Write-Host "      Workflow ID: $($response.workflow_id)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "   ✅ Workflow detected successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "   📝 Agent Response:" -ForegroundColor Cyan
        Write-Host "   $($response.response.Substring(0, [Math]::Min(300, $response.response.Length)))..." -ForegroundColor White
    } else {
        Write-Host "   ❌ Workflow NOT detected (should have been)" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Multi-turn input gathering
Write-Host "5️⃣  Test: Input gathering (turn 2)..." -ForegroundColor Yellow
try {
    $body = @{
        agent_id = "agent_jermaine_super_action"
        message = "20 customers per week"
        conversation_state = @{
            workflow_id = "customer_followup"
            step = 1
            collected_inputs = @{}
        }
    } | ConvertTo-Json -Depth 5
    
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    if ($response.current_step -eq 2) {
        Write-Host "   ✅ Progressed to step 2" -ForegroundColor Green
        Write-Host "   📍 Progress: Step $($response.current_step) of $($response.total_steps)" -ForegroundColor White
    } else {
        Write-Host "   ⚠️  Expected step 2, got: $($response.current_step)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 5: ROI calculation (final step)
Write-Host "6️⃣  Test: ROI calculation..." -ForegroundColor Yellow
try {
    $body = @{
        agent_id = "agent_jermaine_super_action"
        message = "80%"
        conversation_state = @{
            workflow_id = "customer_followup"
            step = 4
            collected_inputs = @{
                messages_per_week = "20"
                time_per_message = "5"
                hourly_rate = "25"
                automation_percentage = "80"
            }
        }
    } | ConvertTo-Json -Depth 5
    
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $body -ContentType "application/json"
    
    if ($response.ready_to_execute -and $response.roi_estimate) {
        Write-Host "   ✅ ROI calculated!" -ForegroundColor Green
        Write-Host ""
        Write-Host "   💰 ROI Metrics:" -ForegroundColor Cyan
        Write-Host "      Time Saved: $($response.roi_estimate.time_saved_per_week) hours/week" -ForegroundColor White
        Write-Host "      Monthly: `$$($response.roi_estimate.monthly_savings)" -ForegroundColor Green
        Write-Host "      Annual: `$$($response.roi_estimate.annual_savings)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ ROI not calculated" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 6: Workflow execution
Write-Host "7️⃣  Test: Workflow execution..." -ForegroundColor Yellow
try {
    $body = @{
        agent_id = "agent_jermaine_super_action"
        workflow_id = "customer_followup"
        inputs = @{
            messages_per_week = "20"
            time_per_message = "5"
            hourly_rate = "25"
            automation_percentage = "80"
        }
    } | ConvertTo-Json -Depth 5
    
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/workflow/execute" -Method Post -Body $body -ContentType "application/json"
    
    if ($response.success) {
        Write-Host "   ✅ Workflow deployed!" -ForegroundColor Green
        Write-Host "   🆔 ID: $($response.workflow_id)" -ForegroundColor White
        Write-Host "   📊 Status: $($response.status)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Execution failed" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "✨ ALL TESTS COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Next: Update frontend with EXECUTE_ACTION_FLOW_UPDATES.md" -ForegroundColor Yellow
Write-Host ""

# Cleanup
Stop-Job $job -ErrorAction SilentlyContinue
Remove-Job $job -ErrorAction SilentlyContinue
