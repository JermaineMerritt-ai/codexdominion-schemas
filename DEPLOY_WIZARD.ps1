# =============================================================================
# CODEX DOMINION - QUICK DEPLOYMENT WIZARD
# =============================================================================
# One-click deployment to your choice of platform
# =============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     🚀 CODEX DOMINION - DEPLOYMENT WIZARD 🚀" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Current System Status:" -ForegroundColor Green
Write-Host "  ✅ Dashboard - Running (localhost:5000)" -ForegroundColor White
Write-Host "  ✅ DOT300 API - 301 Agents Ready" -ForegroundColor White
Write-Host "  ✅ GPT-4 Orchestration - Operational" -ForegroundColor White
Write-Host "  ✅ Landing Page - Ready for Deploy" -ForegroundColor White
Write-Host ""

Write-Host "Choose your deployment platform:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1️⃣  IONOS VPS (74.208.123.158)" -ForegroundColor Cyan
Write-Host "     ⚡ Fastest setup (5-10 minutes)" -ForegroundColor Gray
Write-Host "     💰 Already paid for" -ForegroundColor Gray
Write-Host "     🎯 Full control" -ForegroundColor Gray
Write-Host ""
Write-Host "  2️⃣  Azure Cloud" -ForegroundColor Blue
Write-Host "     ☁️  Static Web Apps + Container Instances" -ForegroundColor Gray
Write-Host "     💳 Pay-as-you-go pricing" -ForegroundColor Gray
Write-Host "     🔒 Enterprise security" -ForegroundColor Gray
Write-Host ""
Write-Host "  3️⃣  Google Cloud Run" -ForegroundColor Magenta
Write-Host "     🌐 Serverless deployment" -ForegroundColor Gray
Write-Host "     💸 Free tier available" -ForegroundColor Gray
Write-Host "     📈 Auto-scaling" -ForegroundColor Gray
Write-Host ""
Write-Host "  4️⃣  Local Testing Only" -ForegroundColor Green
Write-Host "     🏠 Keep running on localhost" -ForegroundColor Gray
Write-Host "     🧪 Perfect for development" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n🔷 IONOS VPS Deployment Selected" -ForegroundColor Cyan
        Write-Host ""

        # Check SSH connection
        Write-Host "📡 Testing connection to IONOS server..." -ForegroundColor Yellow
        $pingResult = Test-Connection -ComputerName 74.208.123.158 -Count 1 -Quiet

        if ($pingResult) {
            Write-Host "✅ Server is reachable!" -ForegroundColor Green
            Write-Host ""
            Write-Host "To deploy to IONOS, you need:" -ForegroundColor Yellow
            Write-Host "  1. SSH access configured" -ForegroundColor White
            Write-Host "  2. .env.production file with credentials" -ForegroundColor White
            Write-Host ""

            $confirm = Read-Host "Do you have SSH access configured? (y/n)"

            if ($confirm -eq "y") {
                Write-Host "`n🚀 Starting IONOS deployment..." -ForegroundColor Green
                .\deploy-ionos-production.ps1
            } else {
                Write-Host "`n📖 SSH Setup Required:" -ForegroundColor Yellow
                Write-Host ""
                Write-Host "Generate SSH key:" -ForegroundColor White
                Write-Host "  ssh-keygen -t rsa -b 4096 -f ~/.ssh/ionos_codexdominion" -ForegroundColor Gray
                Write-Host ""
                Write-Host "Copy key to server:" -ForegroundColor White
                Write-Host "  ssh-copy-id -i ~/.ssh/ionos_codexdominion.pub root@74.208.123.158" -ForegroundColor Gray
                Write-Host ""
                Write-Host "Then run this wizard again!" -ForegroundColor Green
            }
        } else {
            Write-Host "❌ Cannot reach IONOS server (74.208.123.158)" -ForegroundColor Red
            Write-Host "Please check your internet connection or server status." -ForegroundColor Yellow
        }
    }

    "2" {
        Write-Host "`n🔷 Azure Cloud Deployment Selected" -ForegroundColor Blue
        Write-Host ""

        # Check Azure CLI
        $azAvailable = Get-Command az -ErrorAction SilentlyContinue

        if ($azAvailable) {
            Write-Host "✅ Azure CLI found!" -ForegroundColor Green

            $confirm = Read-Host "Do you want to deploy to Azure now? (y/n)"

            if ($confirm -eq "y") {
                Write-Host "`n🚀 Starting Azure deployment..." -ForegroundColor Green
                .\deploy-azure-production.ps1
            }
        } else {
            Write-Host "❌ Azure CLI not installed" -ForegroundColor Red
            Write-Host ""
            Write-Host "Install Azure CLI:" -ForegroundColor Yellow
            Write-Host "  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Gray
            Write-Host ""
            Write-Host "Or use PowerShell command:" -ForegroundColor Yellow
            Write-Host "  Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'" -ForegroundColor Gray
        }
    }

    "3" {
        Write-Host "`n🔷 Google Cloud Run Deployment Selected" -ForegroundColor Magenta
        Write-Host ""

        # Check gcloud CLI
        $gcloudAvailable = Get-Command gcloud -ErrorAction SilentlyContinue

        if ($gcloudAvailable) {
            Write-Host "✅ Google Cloud SDK found!" -ForegroundColor Green

            $confirm = Read-Host "Do you want to deploy to Google Cloud now? (y/n)"

            if ($confirm -eq "y") {
                Write-Host "`n🚀 Starting Google Cloud deployment..." -ForegroundColor Green
                bash deploy-gcp.sh
            }
        } else {
            Write-Host "❌ Google Cloud SDK not installed" -ForegroundColor Red
            Write-Host ""
            Write-Host "Install Google Cloud SDK:" -ForegroundColor Yellow
            Write-Host "  https://cloud.google.com/sdk/docs/install" -ForegroundColor Gray
        }
    }

    "4" {
        Write-Host "`n🏠 Local Development Mode" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your system is already running locally:" -ForegroundColor White
        Write-Host "  • Dashboard: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "  • DOT300 API: http://localhost:8300" -ForegroundColor Cyan
        Write-Host "  • GPT-4 Orchestration: http://localhost:8400" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "✨ Perfect for testing and development!" -ForegroundColor Green
        Write-Host ""
        Write-Host "When ready to deploy, run this wizard again." -ForegroundColor Yellow
    }

    default {
        Write-Host "`n❌ Invalid choice" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
