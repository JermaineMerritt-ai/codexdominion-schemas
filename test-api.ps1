# Test Sovereign Bridge API Endpoints
# Run this script after deployment completes

$baseUrl = "https://mango-wave-0fcc4e40f.3.azurestaticapps.net"

Write-Host "`n=== SOVEREIGN BRIDGE API TESTS ===" -ForegroundColor Cyan
Write-Host "Base URL: $baseUrl" -ForegroundColor Gray
Write-Host "=" * 60 -ForegroundColor Gray

# Test 1: GET request (query task)
Write-Host "`n[TEST 1] GET /api/agent-commands?taskId=test_123" -ForegroundColor Yellow
try {
    $getResult = Invoke-RestMethod -Uri "$baseUrl/api/agent-commands?taskId=test_123" -Method Get
    Write-Host "[PASS] GET request successful" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Gray
    $getResult | ConvertTo-Json -Depth 5
} catch {
    Write-Host "[FAIL] GET request failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: POST request (create task)
Write-Host "`n[TEST 2] POST /api/agent-commands (create agent task)" -ForegroundColor Yellow
try {
    $postBody = @{
        agent = "super_action_ai"
        mode = "build"
        prompt = "Create video project from PDF"
        targets = @("realm:video_studio", "document:test_doc")
        context = @{
            documentIds = @("test_doc_123")
            priority = "high"
        }
    } | ConvertTo-Json

    $postResult = Invoke-RestMethod -Uri "$baseUrl/api/agent-commands" `
        -Method Post `
        -Body $postBody `
        -ContentType "application/json"

    Write-Host "[PASS] POST request successful" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Gray
    $postResult | ConvertTo-Json -Depth 5

    # Save taskId for follow-up test
    $taskId = $postResult.taskId

    # Test 3: Query the created task
    if ($taskId) {
        Write-Host "`n[TEST 3] GET /api/agent-commands?taskId=$taskId (query created task)" -ForegroundColor Yellow
        Start-Sleep -Seconds 2
        try {
            $queryResult = Invoke-RestMethod -Uri "$baseUrl/api/agent-commands?taskId=$taskId" -Method Get
            Write-Host "[PASS] Task query successful" -ForegroundColor Green
            Write-Host "Response:" -ForegroundColor Gray
            $queryResult | ConvertTo-Json -Depth 5
        } catch {
            Write-Host "[FAIL] Task query failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "[FAIL] POST request failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Error handling (missing parameters)
Write-Host "`n[TEST 4] POST with missing parameters (error handling)" -ForegroundColor Yellow
try {
    $invalidBody = @{
        agent = "super_action_ai"
        # Missing mode and prompt
    } | ConvertTo-Json

    $errorResult = Invoke-RestMethod -Uri "$baseUrl/api/agent-commands" `
        -Method Post `
        -Body $invalidBody `
        -ContentType "application/json"

    Write-Host "[WARN] Expected validation error but got success" -ForegroundColor Yellow
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 400) {
        Write-Host "[PASS] Validation error handled correctly (HTTP 400)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n" + ("=" * 60) -ForegroundColor Gray
Write-Host "=== TESTS COMPLETE ===" -ForegroundColor Cyan
Write-Host "`nAPI Documentation:" -ForegroundColor Gray
Write-Host "  GET  /api/agent-commands?taskId=<id>  - Query task status" -ForegroundColor Gray
Write-Host "  POST /api/agent-commands              - Create agent task" -ForegroundColor Gray
Write-Host "`nExample POST body:" -ForegroundColor Gray
Write-Host @"
{
  "agent": "super_action_ai",
  "mode": "build",
  "prompt": "Your command here",
  "targets": ["realm:video_studio"],
  "context": { "documentIds": ["doc_id"] }
}
"@ -ForegroundColor DarkGray
