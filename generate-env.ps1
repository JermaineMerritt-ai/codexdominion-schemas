# Generate production .env file with secure secrets

Write-Host "🔐 Generating production environment file..." -ForegroundColor Cyan

# Function to generate random secret
function New-RandomSecret {
    param([int]$Length = 64)
    $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    -join ((1..$Length) | ForEach-Object { $chars[(Get-Random -Maximum $chars.Length)] })
}

# Generate secrets
$SECRET_KEY = New-RandomSecret
$JWT_SECRET = New-RandomSecret
$API_KEY = New-RandomSecret
$DB_PASSWORD = New-RandomSecret -Length 32
$REDIS_PASSWORD = New-RandomSecret -Length 32

# Read template
$templatePath = Join-Path $PSScriptRoot ".env.production.template"
$envContent = Get-Content $templatePath -Raw

# Replace placeholders
$envContent = $envContent -replace "your-secret-key-here", $SECRET_KEY
$envContent = $envContent -replace "your-jwt-secret-here", $JWT_SECRET
$envContent = $envContent -replace "your-api-key-here", $API_KEY
$envContent = $envContent -replace "your-database-password-here", $DB_PASSWORD
$envContent = $envContent -replace "your-redis-password-here", $REDIS_PASSWORD

# Write .env file
$envPath = Join-Path $PSScriptRoot ".env"
Set-Content -Path $envPath -Value $envContent -NoNewline

Write-Host "`n✅ Production .env file created successfully!" -ForegroundColor Green
Write-Host "   📄 Location: $envPath" -ForegroundColor Yellow
Write-Host "`n🔒 Generated secrets:" -ForegroundColor Cyan
Write-Host "   SECRET_KEY: $($SECRET_KEY.Substring(0, 16))... (64 chars)" -ForegroundColor Gray
Write-Host "   JWT_SECRET: $($JWT_SECRET.Substring(0, 16))... (64 chars)" -ForegroundColor Gray
Write-Host "   API_KEY: $($API_KEY.Substring(0, 16))... (64 chars)" -ForegroundColor Gray
Write-Host "   DB_PASSWORD: $($DB_PASSWORD.Substring(0, 8))... (32 chars)" -ForegroundColor Gray
Write-Host "   REDIS_PASSWORD: $($REDIS_PASSWORD.Substring(0, 8))... (32 chars)" -ForegroundColor Gray

Write-Host "`n⚠️  IMPORTANT: Keep .env file secure!" -ForegroundColor Magenta
Write-Host "   - Never commit to git" -ForegroundColor Yellow
Write-Host "   - Store backups encrypted" -ForegroundColor Yellow
Write-Host "   - Use environment-specific secrets in production" -ForegroundColor Yellow
