# =============================================================================
# TEST EXECUTE-ACTION FLOW
# =============================================================================
# Tests the enhanced workflow automation system

Write-Host "🧪 TESTING EXECUTE-ACTION FLOW SYSTEM" -ForegroundColor Cyan
Write-Host ""

# Check Flask server
Write-Host "1️⃣  Checking Flask server..." -ForegroundColor Yellow
try {
    $healthCheck = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -ErrorAction Stop
    Write-Host "   ✅ Flask is running" -ForegroundColor Green
    Write-Host "   📊 Agents: $($healthCheck.agents_count)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Flask not responding. Start with: python flask_dashboard.py" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 1: Simple conversational message (should NOT trigger workflow)
Write-Host "2️⃣  Test 1: Conversational message (no workflow)..." -ForegroundColor Yellow
try {
    $chatBody = @{
        agent_id = "agent_jermaine_super_action"
        message = "What can you help me with?"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $chatBody -ContentType "application/json" -ErrorAction Stop
    
    if ($response.action_type -eq "chat" -and -not $response.workflow_detected) {
        Write-Host "   ✅ Correctly identified as conversational" -ForegroundColor Green
        Write-Host "   📝 Action Type: $($response.action_type)" -ForegroundColor Gray
    } else {
        Write-Host "   ⚠️  Expected conversational, got: $($response.action_type)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: Action request (should trigger workflow detection)
Write-Host "3️⃣  Test 2: Action request (should detect workflow)..." -ForegroundColor Yellow
try {
    $chatBody = @{
        agent_id = "agent_jermaine_super_action"
        message = "Automate my weekly customer follow-up messages"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $chatBody -ContentType "application/json" -ErrorAction Stop
    
    if ($response.workflow_detected) {
        Write-Host "   ✅ Workflow detected!" -ForegroundColor Green
        Write-Host "   🔄 Workflow ID: $($response.workflow_id)" -ForegroundColor Gray
        Write-Host "   📝 Action Type: $($response.action_type)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "   🤖 Agent Response:" -ForegroundColor Cyan
        Write-Host "   $($response.response)" -ForegroundColor White
        Write-Host ""
        Write-Host "   📋 Next Inputs Required:" -ForegroundColor Gray
        $response.next_inputs_required | ForEach-Object { Write-Host "      • $_" -ForegroundColor Gray }
    } else {
        Write-Host "   ❌ Workflow not detected" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Multi-turn input gathering
Write-Host "4️⃣  Test 3: Input gathering flow..." -ForegroundColor Yellow
try {
    # Turn 1: Initial request
    $chatBody1 = @{
        agent_id = "agent_jermaine_super_action"
        message = "Automate my weekly customer follow-up messages"
    } | ConvertTo-Json

    $response1 = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $chatBody1 -ContentType "application/json"
    
    # Turn 2: Answer first question (messages per week)
    $chatBody2 = @{
        agent_id = "agent_jermaine_super_action"
        message = "20 customers per week"
        conversation_state = @{
            workflow_id = $response1.workflow_id
            step = 1
            collected_inputs = @{}
        }
    } | ConvertTo-Json

    $response2 = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $chatBody2 -ContentType "application/json"
    
    if ($response2.current_step -eq 2) {
        Write-Host "   ✅ Input gathering working!" -ForegroundColor Green
        Write-Host "   📍 Current Step: $($response2.current_step) / $($response2.total_steps)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "   🤖 Next Question:" -ForegroundColor Cyan
        Write-Host "   $($response2.response)" -ForegroundColor White
    } else {
        Write-Host "   ⚠️  Expected step 2, got: $($response2.current_step)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Complete workflow with ROI calculation
Write-Host "5️⃣  Test 4: Complete workflow with ROI..." -ForegroundColor Yellow
try {
    # Simulate completing all input steps
    $chatBody = @{
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
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method Post -Body $chatBody -ContentType "application/json"
    
    if ($response.ready_to_execute -and $response.roi_estimate) {
        Write-Host "   ✅ ROI calculated successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "   💰 ROI Metrics:" -ForegroundColor Cyan
        Write-Host "      Time Saved: $($response.roi_estimate.time_saved_per_week) hours/week" -ForegroundColor Gray
        Write-Host "      Monthly Savings: `$$($response.roi_estimate.monthly_savings)" -ForegroundColor Green
        Write-Host "      Annual Savings: `$$($response.roi_estimate.annual_savings)" -ForegroundColor Green
        Write-Host "      Setup Time: $($response.roi_estimate.setup_time) minutes" -ForegroundColor Gray
        Write-Host ""
        Write-Host "   🤖 Agent Response:" -ForegroundColor Cyan
        Write-Host "   $($response.response)" -ForegroundColor White
    } else {
        Write-Host "   ❌ ROI calculation failed" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 5: Workflow execution
Write-Host "6️⃣  Test 5: Workflow execution..." -ForegroundColor Yellow
try {
    $executeBody = @{
        agent_id = "agent_jermaine_super_action"
        workflow_id = "customer_followup"
        inputs = @{
            messages_per_week = "20"
            time_per_message = "5"
            hourly_rate = "25"
            automation_percentage = "80"
        }
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/workflow/execute" -Method Post -Body $executeBody -ContentType "application/json"
    
    if ($response.success) {
        Write-Host "   ✅ Workflow executed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "   🆔 Workflow ID: $($response.workflow_id)" -ForegroundColor Gray
        Write-Host "   📊 Status: $($response.status)" -ForegroundColor Green
        Write-Host "   🔗 Dashboard URL: $($response.dashboard_url)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "   📋 Next Steps:" -ForegroundColor Cyan
        $response.next_steps | ForEach-Object { Write-Host "      • $_" -ForegroundColor Gray }
    } else {
        Write-Host "   ❌ Execution failed" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "✨ ALL EXECUTE-ACTION FLOW TESTS COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Update frontend with EXECUTE_ACTION_FLOW_UPDATES.md" -ForegroundColor Gray
Write-Host "   2. Test in UI: http://localhost:3000/dashboard/chat?agent=agent_jermaine_super_action" -ForegroundColor Gray
Write-Host "   3. Try: 'Automate my weekly customer follow-up messages'" -ForegroundColor Gray
Write-Host ""
