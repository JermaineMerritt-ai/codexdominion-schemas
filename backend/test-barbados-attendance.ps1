# Test script to record attendance for Barbados Launch

Write-Host "`n🎭 Recording Attendance for Barbados Launch Event`n" -ForegroundColor Cyan

# Step 1: Login to get JWT token
Write-Host "Step 1: Authenticating..." -ForegroundColor Yellow
$loginPayload = '{"email":"admin@codexdominion.com","password":"Admin123!"}'
$loginResponse = curl.exe -s -X POST "http://localhost:4000/api/v1/auth/login" `
    -H "Content-Type: application/json" `
    -d $loginPayload | ConvertFrom-Json

if (-not $loginResponse.accessToken) {
    Write-Host "❌ Authentication failed" -ForegroundColor Red
    exit 1
}

$token = $loginResponse.accessToken
Write-Host "✓ Authenticated as $($loginResponse.user.email)" -ForegroundColor Green

# Step 2: Get a youth user ID to register
Write-Host "`nStep 2: Finding youth user..." -ForegroundColor Yellow
$usersResponse = curl.exe -s "http://localhost:4000/api/v1/users" `
    -H "Authorization: Bearer $token" | ConvertFrom-Json

$youthUser = $usersResponse | Where-Object { 
    $_.roles -contains 'YOUTH' 
} | Select-Object -First 1

if (-not $youthUser) {
    Write-Host "❌ No youth user found" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Found youth: $($youthUser.email) (ID: $($youthUser.id))" -ForegroundColor Green

# Step 3: Record attendance using batch format
Write-Host "`nStep 3: Recording attendance..." -ForegroundColor Yellow
$attendancePayload = @{
    records = @(
        @{
            user_id = $youthUser.id
            status = "REGISTERED"
        }
    )
} | ConvertTo-Json -Compress

Write-Host "Payload: $attendancePayload" -ForegroundColor Gray

$attendanceResponse = curl.exe -s -X POST "http://localhost:4000/api/v1/events/barbados-launch-2025/attendance" `
    -H "Authorization: Bearer $token" `
    -H "Content-Type: application/json" `
    -d $attendancePayload | ConvertFrom-Json

Write-Host "`n✅ Attendance Recorded!" -ForegroundColor Green
Write-Host "`nResponse:" -ForegroundColor Cyan
$attendanceResponse | ConvertTo-Json -Depth 5

# Step 4: Verify attendance
Write-Host "`nStep 4: Verifying attendance..." -ForegroundColor Yellow
$verifyResponse = curl.exe -s "http://localhost:4000/api/v1/events/barbados-launch-2025/attendance" | ConvertFrom-Json

Write-Host "`n📊 Attendance Summary:" -ForegroundColor Cyan
Write-Host "  Total: $($verifyResponse.summary.total)" -ForegroundColor White
Write-Host "  Present: $($verifyResponse.summary.present)" -ForegroundColor White
Write-Host "  Registered: $($verifyResponse.summary.registered)" -ForegroundColor White
Write-Host "  Absent: $($verifyResponse.summary.absent)" -ForegroundColor White

Write-Host "`n🔥 Barbados Launch attendance tracking active!" -ForegroundColor Green
