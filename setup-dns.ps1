# DNS Setup Script for CodexDominion.app
# This script helps you configure DNS records for your domain

Write-Host "=== CodexDominion.app DNS Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Get IONOS Server IP
Write-Host "Step 1: Obtain your IONOS Server IP Address" -ForegroundColor Yellow
Write-Host "You can find this in your IONOS dashboard or by SSHing into your server and running:"
Write-Host "  curl ifconfig.me" -ForegroundColor Green
Write-Host ""
$serverIP = Read-Host "Enter your IONOS server IP address"

if ([string]::IsNullOrEmpty($serverIP)) {
    Write-Host "ERROR: Server IP is required!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Using Server IP: $serverIP" -ForegroundColor Green
Write-Host ""

# Step 2: DNS Provider Selection
Write-Host "Step 2: Select your DNS Provider" -ForegroundColor Yellow
Write-Host "1. Google Domains"
Write-Host "2. Cloudflare"
Write-Host "3. Manual Configuration (I'll do it myself)"
Write-Host ""
$provider = Read-Host "Enter your choice (1-3)"

Write-Host ""
Write-Host "=== DNS Records to Configure ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Add the following DNS records to codexdominion.app:" -ForegroundColor White
Write-Host ""
Write-Host "A Records:" -ForegroundColor Yellow
Write-Host "  @ (root)              →  $serverIP" -ForegroundColor Green
Write-Host "  www                   →  $serverIP" -ForegroundColor Green
Write-Host "  api                   →  $serverIP" -ForegroundColor Green
Write-Host "  monitoring            →  $serverIP" -ForegroundColor Green
Write-Host "  dashboard             →  $serverIP" -ForegroundColor Green
Write-Host ""
Write-Host "CNAME Records:" -ForegroundColor Yellow
Write-Host "  *                     →  codexdominion.app" -ForegroundColor Green
Write-Host ""
Write-Host "TTL: 3600 seconds (1 hour)" -ForegroundColor Gray
Write-Host ""

switch ($provider) {
    "1" {
        Write-Host "=== Google Domains Configuration ===" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Go to: https://domains.google.com" -ForegroundColor White
        Write-Host "2. Select 'codexdominion.app'" -ForegroundColor White
        Write-Host "3. Navigate to 'DNS' section" -ForegroundColor White
        Write-Host "4. Click 'Manage custom records'" -ForegroundColor White
        Write-Host "5. Add the A records listed above" -ForegroundColor White
        Write-Host "6. Add the CNAME record for wildcard subdomain" -ForegroundColor White
        Write-Host ""
    }
    "2" {
        Write-Host "=== Cloudflare Configuration ===" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Option A: Manual Configuration" -ForegroundColor Yellow
        Write-Host "1. Go to: https://dash.cloudflare.com" -ForegroundColor White
        Write-Host "2. Select 'codexdominion.app'" -ForegroundColor White
        Write-Host "3. Go to DNS → Records" -ForegroundColor White
        Write-Host "4. Add the A records listed above" -ForegroundColor White
        Write-Host "5. Add the CNAME record" -ForegroundColor White
        Write-Host ""
        Write-Host "Option B: Terraform (Automated)" -ForegroundColor Yellow
        Write-Host "Run the Terraform configuration in:" -ForegroundColor White
        Write-Host "  c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion-terraform\" -ForegroundColor Green
        Write-Host ""

        $useTerraform = Read-Host "Do you want to update Terraform configuration? (y/n)"
        if ($useTerraform -eq "y") {
            $tfFile = "c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion-terraform\main.tf"
            $content = Get-Content $tfFile -Raw
            $content = $content -replace 'value\s*=\s*"98\.19\.211\.133"', "value   = `"$serverIP`""
            Set-Content -Path $tfFile -Value $content
            Write-Host "Updated Terraform configuration with your server IP" -ForegroundColor Green
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Yellow
            Write-Host "1. cd c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion-terraform\" -ForegroundColor White
            Write-Host "2. terraform init" -ForegroundColor White
            Write-Host "3. terraform plan" -ForegroundColor White
            Write-Host "4. terraform apply" -ForegroundColor White
        }
    }
    "3" {
        Write-Host "Manual configuration selected." -ForegroundColor White
        Write-Host "Please add the DNS records listed above to your DNS provider." -ForegroundColor White
    }
}

Write-Host ""
Write-Host "=== DNS Propagation ===" -ForegroundColor Cyan
Write-Host "After adding the records, DNS propagation can take 5-60 minutes." -ForegroundColor Yellow
Write-Host ""
Write-Host "You can check DNS propagation with:" -ForegroundColor White
Write-Host "  Resolve-DnsName codexdominion.app -Type A -Server 8.8.8.8" -ForegroundColor Green
Write-Host "  Resolve-DnsName www.codexdominion.app -Type A -Server 8.8.8.8" -ForegroundColor Green
Write-Host "  Resolve-DnsName api.codexdominion.app -Type A -Server 8.8.8.8" -ForegroundColor Green
Write-Host ""

Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Wait for DNS propagation (5-60 minutes)" -ForegroundColor White
Write-Host "2. Verify DNS with the commands above" -ForegroundColor White
Write-Host "3. SSH into your IONOS server and set up SSL:" -ForegroundColor White
Write-Host "   certbot certonly --nginx -d codexdominion.app -d www.codexdominion.app -d api.codexdominion.app" -ForegroundColor Green
Write-Host "4. Deploy your application" -ForegroundColor White
Write-Host ""
Write-Host "DNS Setup Script Complete!" -ForegroundColor Cyan
