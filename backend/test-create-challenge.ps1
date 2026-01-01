# Test Script: Create Digital Heritage Map Challenge
# Usage: .\test-create-challenge.ps1

Write-Host "`n🎨 Testing Creator Challenge Creation" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

# Step 1: Get seasons to find valid season_id
Write-Host "`n📍 Step 1: Getting available seasons..." -ForegroundColor Yellow
$seasonsResponse = Invoke-RestMethod -Uri "http://localhost:4000/api/v1/seasons" -Method GET
$seasonId = $seasonsResponse[0].id
Write-Host "✅ Found season: $($seasonsResponse[0].name) ($seasonId)" -ForegroundColor Green

# Step 2: Login as admin
Write-Host "`n📍 Step 2: Logging in as admin..." -ForegroundColor Yellow
$loginBody = @{
    email = "admin@codex.app"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:4000/api/v1/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginBody

$token = $loginResponse.accessToken
Write-Host "✅ Got JWT token: $($token.Substring(0, 20))..." -ForegroundColor Green

# Step 3: Create the challenge
Write-Host "`n📍 Step 3: Creating 'Digital Heritage Map' challenge..." -ForegroundColor Yellow
$challengeBody = @{
    title = "Build a Digital Heritage Map"
    description = "Create an interactive artifact that maps diaspora stories."
    season_id = $seasonId
    deadline = "2025-03-31T23:59:59Z"
} | ConvertTo-Json

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

try {
    $challengeResponse = Invoke-RestMethod -Uri "http://localhost:4000/api/v1/creators/challenges" `
        -Method POST `
        -Headers $headers `
        -Body $challengeBody

    Write-Host "`n✅ Challenge Created Successfully!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "`n📦 Challenge Details:" -ForegroundColor Cyan
    Write-Host "   ID: $($challengeResponse.id)" -ForegroundColor White
    Write-Host "   Title: $($challengeResponse.title)" -ForegroundColor White
    Write-Host "   Description: $($challengeResponse.description)" -ForegroundColor White
    Write-Host "   Deadline: $($challengeResponse.deadline)" -ForegroundColor White
    Write-Host "   Created By: $($challengeResponse.createdBy)" -ForegroundColor White
    Write-Host "   Created At: $($challengeResponse.createdAt)" -ForegroundColor White

    Write-Host "`n🔥 Challenge is now live and accepting submissions!" -ForegroundColor Green
} catch {
    Write-Host "`n❌ Error creating challenge:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host "`nResponse:" -ForegroundColor Gray
    Write-Host $_.ErrorDetails.Message -ForegroundColor DarkGray
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
