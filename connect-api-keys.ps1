# Option B: Connect Real API Keys
# Interactive wizard to configure social media and affiliate APIs

$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "OPTION B: CONNECT REAL API KEYS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "This wizard will help you configure:" -ForegroundColor White
Write-Host "  1. YouTube Data API v3" -ForegroundColor Gray
Write-Host "  2. TikTok Business API" -ForegroundColor Gray
Write-Host "  3. Pinterest API" -ForegroundColor Gray
Write-Host "  4. ShareASale Affiliate Network" -ForegroundColor Gray
Write-Host "  5. Instagram Basic Display API" -ForegroundColor Gray
Write-Host ""

# Load existing configs
$youtubeConfig = Get-Content "youtube_config.json" -Raw | ConvertFrom-Json
$tiktokConfig = Get-Content "tiktok_config.json" -Raw | ConvertFrom-Json
$pinterestConfig = Get-Content "pinterest_config.json" -Raw | ConvertFrom-Json
$affiliateConfig = Get-Content "affiliate_config.json" -Raw | ConvertFrom-Json

$updated = $false

# YouTube Configuration
Write-Host "[1/5] YouTube Data API Configuration" -ForegroundColor Yellow
Write-Host "Current API Key: $($youtubeConfig.youtube.api_key)" -ForegroundColor Gray
$response = Read-Host "Do you want to update YouTube API key? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "📝 How to get YouTube API key:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://console.cloud.google.com/apis/credentials" -ForegroundColor Gray
    Write-Host "  2. Create API key" -ForegroundColor Gray
    Write-Host "  3. Enable YouTube Data API v3" -ForegroundColor Gray
    Write-Host ""
    $apiKey = Read-Host "Enter YouTube API key"
    $channelId = Read-Host "Enter YouTube Channel ID"

    if ($apiKey -and $channelId) {
        $youtubeConfig.youtube.api_key = $apiKey
        $youtubeConfig.youtube.channel_id = $channelId
        $youtubeConfig | ConvertTo-Json -Depth 10 | Set-Content "youtube_config.json"
        Write-Host "  ✅ YouTube configured!" -ForegroundColor Green
        $updated = $true
    }
}

# TikTok Configuration
Write-Host "`n[2/5] TikTok Business API Configuration" -ForegroundColor Yellow
Write-Host "Current Username: $($tiktokConfig.tiktok.username)" -ForegroundColor Gray
$response = Read-Host "Do you want to update TikTok credentials? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "📝 How to get TikTok API access:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://developers.tiktok.com/" -ForegroundColor Gray
    Write-Host "  2. Register for TikTok for Developers" -ForegroundColor Gray
    Write-Host "  3. Create app and get API keys" -ForegroundColor Gray
    Write-Host ""
    $clientKey = Read-Host "Enter TikTok Client Key"
    $clientSecret = Read-Host "Enter TikTok Client Secret"
    $username = Read-Host "Enter TikTok Username"

    if ($clientKey -and $clientSecret) {
        $tiktokConfig.tiktok.client_key = $clientKey
        $tiktokConfig.tiktok.client_secret = $clientSecret
        $tiktokConfig.tiktok.username = $username
        $tiktokConfig | ConvertTo-Json -Depth 10 | Set-Content "tiktok_config.json"
        Write-Host "  ✅ TikTok configured!" -ForegroundColor Green
        $updated = $true
    }
}

# Pinterest Configuration
Write-Host "`n[3/5] Pinterest API Configuration" -ForegroundColor Yellow
Write-Host "Current App ID: $($pinterestConfig.pinterest.app_id)" -ForegroundColor Gray
$response = Read-Host "Do you want to update Pinterest credentials? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "📝 How to get Pinterest API access:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://developers.pinterest.com/" -ForegroundColor Gray
    Write-Host "  2. Create app" -ForegroundColor Gray
    Write-Host "  3. Get App ID and App Secret" -ForegroundColor Gray
    Write-Host ""
    $appId = Read-Host "Enter Pinterest App ID"
    $appSecret = Read-Host "Enter Pinterest App Secret"
    $username = Read-Host "Enter Pinterest Username"

    if ($appId -and $appSecret) {
        $pinterestConfig.pinterest.app_id = $appId
        $pinterestConfig.pinterest.app_secret = $appSecret
        $pinterestConfig.pinterest.username = $username
        $pinterestConfig | ConvertTo-Json -Depth 10 | Set-Content "pinterest_config.json"
        Write-Host "  ✅ Pinterest configured!" -ForegroundColor Green
        $updated = $true
    }
}

# ShareASale Affiliate Configuration
Write-Host "`n[4/5] ShareASale Affiliate Network Configuration" -ForegroundColor Yellow
Write-Host "Current Merchant ID: $($affiliateConfig.affiliate_networks.primary_network.merchant_id)" -ForegroundColor Gray
$response = Read-Host "Do you want to update ShareASale credentials? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "📝 How to get ShareASale API access:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://account.shareasale.com/a-apiAffiliates.cfm" -ForegroundColor Gray
    Write-Host "  2. Generate API Token and Secret" -ForegroundColor Gray
    Write-Host ""
    $apiToken = Read-Host "Enter ShareASale API Token"
    $apiSecret = Read-Host "Enter ShareASale API Secret"
    $merchantId = Read-Host "Enter Merchant ID"
    $affiliateId = Read-Host "Enter Affiliate ID"

    if ($apiToken -and $apiSecret) {
        $affiliateConfig.affiliate_api_key = $apiToken
        $affiliateConfig.affiliate_networks.primary_network.merchant_id = $merchantId
        $affiliateConfig.affiliate_networks.primary_network.affiliate_id = $affiliateId
        $affiliateConfig.demo_mode = $false
        $affiliateConfig | ConvertTo-Json -Depth 10 | Set-Content "affiliate_config.json"
        Write-Host "  ✅ ShareASale configured! (Demo mode disabled)" -ForegroundColor Green
        $updated = $true
    }
}

# Instagram Configuration
Write-Host "`n[5/5] Instagram Basic Display API Configuration" -ForegroundColor Yellow
$response = Read-Host "Do you want to configure Instagram API? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "📝 How to get Instagram API access:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://developers.facebook.com/apps" -ForegroundColor Gray
    Write-Host "  2. Create app with Instagram Basic Display" -ForegroundColor Gray
    Write-Host "  3. Get Client ID and Client Secret" -ForegroundColor Gray
    Write-Host ""
    $clientId = Read-Host "Enter Instagram Client ID"
    $clientSecret = Read-Host "Enter Instagram Client Secret"

    if ($clientId -and $clientSecret) {
        $instagramConfig = @{
            instagram = @{
                client_id = $clientId
                client_secret = $clientSecret
                username = "@codexdominion"
                enabled = $true
            }
        }
        $instagramConfig | ConvertTo-Json -Depth 10 | Set-Content "instagram_config.json"
        Write-Host "  ✅ Instagram configured!" -ForegroundColor Green
        $updated = $true
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "API CONFIGURATION COMPLETE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($updated) {
    Write-Host "✅ Configuration files updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next Steps:" -ForegroundColor White
    Write-Host "  1. Restart dashboard to load new configs" -ForegroundColor Gray
    Write-Host "  2. Test API connections in dashboard tabs" -ForegroundColor Gray
    Write-Host "  3. Update dashboard_data_integrator.py to use real APIs" -ForegroundColor Gray
    Write-Host "  4. Run: python dashboard_data_integrator.py" -ForegroundColor Gray
    Write-Host ""

    # Create API status file
    @{
        youtube = ($youtubeConfig.youtube.api_key -ne "YOUR_YOUTUBE_API_KEY_HERE")
        tiktok = ($tiktokConfig.tiktok.client_key -ne "YOUR_CLIENT_KEY")
        pinterest = ($pinterestConfig.pinterest.app_id -ne "YOUR_APP_ID")
        shareasale = (-not $affiliateConfig.demo_mode)
        instagram = (Test-Path "instagram_config.json")
        last_updated = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    } | ConvertTo-Json | Out-File "api_keys_status.json"

    Write-Host "💾 API status saved to: api_keys_status.json" -ForegroundColor Gray
} else {
    Write-Host "⚠️  No configuration changes made" -ForegroundColor Yellow
    Write-Host "   Run this script again when you have API keys ready" -ForegroundColor Gray
}

Write-Host ""
