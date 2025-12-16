#!/usr/bin/env pwsh
# Check SSL and Domain Status for api.codexdominion.app

Write-Host "`n════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "   🔐 SSL Certificate Status Check" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════`n" -ForegroundColor Yellow

# Check custom domain binding
Write-Host "1️⃣ Custom Domain Binding:" -ForegroundColor Cyan
az webapp config hostname list `
    --webapp-name codexdominion-backend `
    --resource-group codexdominion-basic `
    --query "[?name=='api.codexdominion.app'].{Hostname:name,SSL:sslState,Thumbprint:thumbprint}" `
    -o table

Write-Host "`n2️⃣ SSL Certificates:" -ForegroundColor Cyan
az webapp config ssl list `
    --resource-group codexdominion-basic `
    -o table

Write-Host "`n3️⃣ Testing HTTPS Endpoint:" -ForegroundColor Cyan
Write-Host "   Waiting 5 seconds for propagation..." -ForegroundColor Gray
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "https://api.codexdominion.app/health" -UseBasicParsing -TimeoutSec 15
    Write-Host "   ✅ SUCCESS!" -ForegroundColor Green
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor White
    Write-Host "   Response: $($response.Content)" -ForegroundColor White
} catch {
    Write-Host "   ⚠️ Not ready yet (normal during SSL provisioning)" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host "`n   💡 Try the direct URL while waiting:" -ForegroundColor Cyan
    Write-Host "   https://codexdominion-backend.azurewebsites.net/health" -ForegroundColor White
}

Write-Host "`n4️⃣ DNS Resolution:" -ForegroundColor Cyan
try {
    $dns = Resolve-DnsName api.codexdominion.app -Type CNAME -ErrorAction Stop
    Write-Host "   ✅ DNS: $($dns.NameHost)" -ForegroundColor Green
} catch {
    Write-Host "   ⏳ DNS still propagating..." -ForegroundColor Yellow
}

Write-Host "`n════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "📋 EXPECTED TIMELINE:" -ForegroundColor Cyan
Write-Host "   • SSL Certificate: 5-10 minutes" -ForegroundColor White
Write-Host "   • DNS Propagation: 15-60 minutes" -ForegroundColor White
Write-Host "   • Full HTTPS: 10-15 minutes typical" -ForegroundColor White
Write-Host "════════════════════════════════════════════════`n" -ForegroundColor Yellow
