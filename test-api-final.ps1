# Final API Test Script for Sovereign Bridge
# Tests both GET and POST endpoints once deployment completes

$apiBase = "https://mango-wave-0fcc4e40f.3.azurestaticapps.net/api/agent-commands"

Write-Host "`n=== Sovereign Bridge API Final Test ===" -ForegroundColor Cyan
Write-Host "API Endpoint: $apiBase`n" -ForegroundColor Yellow

# Test 1: GET request (query task status)
Write-Host "[TEST 1] GET /api/agent-commands?taskId=test_123" -ForegroundColor Cyan
try {
    $getResponse = Invoke-RestMethod -Uri "$apiBase?taskId=test_123" -Method Get
    Write-Host "[PASS] GET request successful" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Gray
    $getResponse | ConvertTo-Json -Depth 3
} catch {
    Write-Host "[FAIL] GET request failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 2: POST request (create agent task)
Write-Host "[TEST 2] POST /api/agent-commands (create task)" -ForegroundColor Cyan
$postBody = @{
    agent = "super_action_ai"
    mode = "build"
    prompt = "Create video project from Kids Christmas Story PDF"
    targets = @("realm:video_studio", "document:kids_christmas_story")
    context = @{
        documentIds = @("kids_christmas_story")
    }
} | ConvertTo-Json

try {
    $postResponse = Invoke-RestMethod -Uri $apiBase -Method Post -Body $postBody -ContentType "application/json"
    Write-Host "[PASS] POST request successful" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Gray
    $postResponse | ConvertTo-Json -Depth 3

    # Test 3: Query the task we just created
    if ($postResponse.success -and $postResponse.data.taskId) {
        Write-Host "`n---`n"
        Write-Host "[TEST 3] GET /api/agent-commands?taskId=$($postResponse.data.taskId)" -ForegroundColor Cyan
        $queryResponse = Invoke-RestMethod -Uri "$apiBase?taskId=$($postResponse.data.taskId)" -Method Get
        Write-Host "[PASS] Query created task successful" -ForegroundColor Green
        Write-Host "Response:" -ForegroundColor Gray
        $queryResponse | ConvertTo-Json -Depth 3
    }
} catch {
    Write-Host "[FAIL] POST request failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Test Summary ===" -ForegroundColor Cyan
Write-Host "If all tests passed, your API is fully operational!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Integrate with your video project creation workflow"
Write-Host "  2. Add actual database persistence (currently using mock data)"
Write-Host "  3. Implement task execution logic"
Write-Host "  4. Add authentication if needed"
