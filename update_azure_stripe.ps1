# =============================================================================
# Codex Dominion - Update Azure Container with Stripe Configuration
# =============================================================================

Write-Host "`n🔷 Updating Azure Container Instance with Stripe Keys..." -ForegroundColor Cyan

# Load environment variables
$envFile = Get-Content .env.production
$stripeSecretKey = ($envFile | Select-String "^STRIPE_SECRET_KEY=").Line -replace "STRIPE_SECRET_KEY=", ""
$stripeWebhookSecret = ($envFile | Select-String "^STRIPE_WEBHOOK_SECRET=").Line -replace "STRIPE_WEBHOOK_SECRET=", ""

Write-Host "✅ Loaded Stripe keys from .env.production" -ForegroundColor Green

# Delete existing container
Write-Host "`n🗑️  Deleting existing container..." -ForegroundColor Yellow
az container delete --resource-group codex-dominion-rg --name codex-backend --yes

Start-Sleep -Seconds 5

# Create new container with Stripe configuration
Write-Host "`n📦 Creating new Azure Container Instance..." -ForegroundColor Yellow

az container create `
  --resource-group codex-dominion-rg `
  --name codex-backend `
  --image codexdominion3840.azurecr.io/codex-dominion-backend:2.0.0 `
  --registry-login-server codexdominion3840.azurecr.io `
  --registry-username codexdominion3840 `
  --registry-password $(az acr credential show --name codexdominion3840 --query "passwords[0].value" -o tsv) `
  --dns-name-label codex-backend `
  --ports 8000 8001 `
  --os-type Linux `
  --cpu 1 `
  --memory 1.5 `
  --environment-variables `
    NODE_ENV=production `
    ENVIRONMENT=production `
    PORT=8001 `
    BACKEND_PORT=8000 `
    STRIPE_SECRET_KEY=$stripeSecretKey `
    STRIPE_WEBHOOK_SECRET=$stripeWebhookSecret `
    STRIPE_ENABLED=true `
    DATABASE_URL=sqlite:///./codex_dominion.db `
    REDIS_URL=redis://localhost:6379/0 `
    JWT_SECRET=0VJNI1a8LMdBErKmQjnRheXpkoWi63ZDzy7YA4gPs2O9GlqSwvfxCubF5THUtc `
    SECRET_KEY=PgoniCuZqAdzFJDcExQmNjGU1a0tT5B3Sf47vY8sw9WhLbe2krROV6pHlIKXyM `
    CORS_ORIGINS=https://codexdominion.app,https://www.codexdominion.app

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Azure Container Instance updated successfully!" -ForegroundColor Green
    Write-Host "`n📊 Container Status:" -ForegroundColor Cyan
    az container show --resource-group codex-dominion-rg --name codex-backend --query "{Name:name, State:instanceView.state, IP:ipAddress.ip}" -o table
} else {
    Write-Host "`n❌ Failed to update Azure Container Instance" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔗 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Configure Stripe webhook at: https://dashboard.stripe.com/webhooks"
Write-Host "   Webhook URL: https://codexdominion.app/api/webhooks/stripe"
Write-Host "   Events: payment_intent.succeeded, checkout.session.completed"
Write-Host "`n2. Test payment flow at: https://codexdominion.app/products"
Write-Host "`n3. Monitor backend: http://codex-backend.eastus.azurecontainer.io:8001/health"
