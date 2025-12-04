# 🔥 YouTube Charts Dependency Installer 👑
# Automated setup for YouTube API integration
# The Merritt Method™ - One-Click Digital Sovereignty

Write-Host "🔥 CODEX YOUTUBE CHARTS - DEPENDENCY INSTALLER 👑" -ForegroundColor Yellow
Write-Host "=" * 55 -ForegroundColor Yellow

# Check if virtual environment exists
$venvPath = ".\.venv\Scripts\python.exe"
if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    $pythonExe = $venvPath
} else {
    Write-Host "⚠️ Virtual environment not found, using system Python" -ForegroundColor Yellow
    $pythonExe = "python"
}

Write-Host "`n📦 Installing YouTube API Dependencies..." -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Cyan

# Install required packages
$packages = @(
    "google-api-python-client",
    "google-auth-oauthlib",
    "google-auth-httplib2"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor White
    try {
        & $pythonExe -m pip install $package --quiet
        Write-Host "✅ $package installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to install $package" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
    }
}

Write-Host "`n🧪 Testing Installation..." -ForegroundColor Cyan
Write-Host "-" * 30 -ForegroundColor Cyan

# Test imports
$testScript = @"
try:
    from googleapiclient.discovery import build
    print('✅ google-api-python-client')
except ImportError:
    print('❌ google-api-python-client')

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    print('✅ google-auth-oauthlib')
except ImportError:
    print('❌ google-auth-oauthlib')

try:
    from google.auth.transport.requests import Request
    print('✅ google-auth-httplib2')
except ImportError:
    print('❌ google-auth-httplib2')

try:
    from codex_youtube_charts import CodexYouTubeCharts
    print('✅ YouTube Charts System')
except ImportError as e:
    print(f'❌ YouTube Charts System: {e}')
"@

& $pythonExe -c $testScript

Write-Host "`n🔧 Configuration Check..." -ForegroundColor Cyan
Write-Host "-" * 30 -ForegroundColor Cyan

# Check configuration
if (Test-Path "youtube_config.json") {
    Write-Host "✅ Configuration file exists" -ForegroundColor Green

    $config = Get-Content "youtube_config.json" | ConvertFrom-Json
    $apiKey = $config.youtube.api_key
    $channelId = $config.youtube.channel_id

    if ($apiKey -eq "YOUR_YOUTUBE_API_KEY_HERE") {
        Write-Host "⚠️ API Key needs to be configured" -ForegroundColor Yellow
    } else {
        Write-Host "✅ API Key configured" -ForegroundColor Green
    }

    if ($channelId -eq "YOUR_CHANNEL_ID_HERE") {
        Write-Host "⚠️ Channel ID needs to be configured" -ForegroundColor Yellow
    } else {
        Write-Host "✅ Channel ID configured" -ForegroundColor Green
    }
} else {
    Write-Host "❌ Configuration file not found" -ForegroundColor Red
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "-" * 15 -ForegroundColor Cyan
Write-Host "1. Get YouTube API Key from Google Cloud Console" -ForegroundColor White
Write-Host "2. Edit youtube_config.json with your API key" -ForegroundColor White
Write-Host "3. Add your Channel ID to youtube_config.json" -ForegroundColor White
Write-Host "4. Run: python youtube_setup_guide.py" -ForegroundColor White
Write-Host "5. Access dashboard: http://127.0.0.1:18080" -ForegroundColor White

Write-Host "`n🔥 YouTube Charts Dependencies Installation Complete! 👑" -ForegroundColor Yellow

# Pause to show results
Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
