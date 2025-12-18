# Test Render Deployment Script
# Replace YOUR-APP-URL with your actual Render URL

$APP_URL = "https://codex-portfolio.onrender.com"  # Update this!

Write-Host "🧪 Testing Render Deployment..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$APP_URL/health" -Method Get
    Write-Host "✅ Health check passed" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Home Page
Write-Host "Test 2: Home Page" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$APP_URL/" -Method Get
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Home page loaded" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Home page failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Auth Endpoints
Write-Host "Test 3: Auth Login Page" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$APP_URL/auth/login" -Method Get
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Login page loaded" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Login page failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Portfolio Dashboard (requires auth)
Write-Host "Test 4: Portfolio Dashboard" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$APP_URL/portfolio/dashboard" -Method Get
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Dashboard accessible" -ForegroundColor Green
    }
} catch {
    if ($_.Exception.Response.StatusCode -eq 401 -or $_.Exception.Response.StatusCode -eq 302) {
        Write-Host "✅ Dashboard requires authentication (expected)" -ForegroundColor Green
    } else {
        Write-Host "❌ Dashboard failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

Write-Host "🎉 Deployment test complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit $APP_URL in your browser" -ForegroundColor White
Write-Host "2. Test login with: admin@codexdominion.com / codex2025" -ForegroundColor White
Write-Host "3. If all works, proceed to PostgreSQL upgrade" -ForegroundColor White
