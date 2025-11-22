# 🏛️ NGINX DEPLOYMENT SCRIPT FOR AISTORELAB.COM
# PowerShell script for WSL Ubuntu deployment

Write-Host "🚀 Deploying Nginx Configuration for AIStoreLab.com" -ForegroundColor Green
Write-Host "🏛️ Operational Sovereignty Platform Nginx Setup" -ForegroundColor Cyan

# Step 1: Copy configuration to WSL
Write-Host "`n📁 Step 1: Copying configuration file..." -ForegroundColor Yellow
$sourcePath = "/mnt/c/Users/JMerr/OneDrive/Documents/.vscode/codex-dominion/nginx-aistorelab.conf"
$targetPath = "/etc/nginx/sites-available/aistorelab.com"

wsl sudo cp $sourcePath $targetPath
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Configuration file copied successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to copy configuration file" -ForegroundColor Red
    exit 1
}

# Step 2: Create symbolic link
Write-Host "`n🔗 Step 2: Enabling site..." -ForegroundColor Yellow
wsl sudo ln -sf /etc/nginx/sites-available/aistorelab.com /etc/nginx/sites-enabled/
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Site enabled successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to enable site" -ForegroundColor Red
    exit 1
}

# Step 3: Test Nginx configuration
Write-Host "`n🧪 Step 3: Testing Nginx configuration..." -ForegroundColor Yellow
wsl sudo nginx -t
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Nginx configuration is valid" -ForegroundColor Green
} else {
    Write-Host "❌ Nginx configuration has errors" -ForegroundColor Red
    exit 1
}

# Step 4: Reload Nginx
Write-Host "`n🔄 Step 4: Reloading Nginx..." -ForegroundColor Yellow
wsl sudo systemctl reload nginx
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Nginx reloaded successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to reload Nginx" -ForegroundColor Red
    # Try starting nginx if it's not running
    Write-Host "🔧 Attempting to start Nginx..." -ForegroundColor Yellow
    wsl sudo systemctl start nginx
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Nginx started successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to start Nginx" -ForegroundColor Red
        Write-Host "💡 Check if port 80 is available or run: wsl sudo systemctl status nginx" -ForegroundColor Blue
    }
}

# Step 5: Check Nginx status
Write-Host "`n📊 Step 5: Checking Nginx status..." -ForegroundColor Yellow
wsl sudo systemctl status nginx --no-pager -l

# Step 6: Display next steps
Write-Host "`n🎯 Next Steps for Complete Deployment:" -ForegroundColor Cyan
Write-Host "1. 🌐 Configure DNS: Point aistorelab.com to your server IP" -ForegroundColor White
Write-Host "2. 🔐 Setup SSL: Run 'wsl sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com'" -ForegroundColor White
Write-Host "3. 🚀 Start Services: Ensure your application is running on port 8501" -ForegroundColor White
Write-Host "4. 🧪 Test: Visit http://localhost (or your server IP)" -ForegroundColor White

Write-Host "`n🏛️ OPERATIONAL SOVEREIGNTY NGINX DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "Your aistorelab.com configuration is ready for production." -ForegroundColor Cyan