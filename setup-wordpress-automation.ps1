# ============================================================================
# WordPress + WooCommerce Setup Automation Script
# ============================================================================
# 
# Automates the complete setup of WordPress, WooCommerce, and integrations
# for Codex Dominion production deployment.
#
# Prerequisites:
#   - Docker Desktop installed and running
#   - Port 8080 available (WordPress)
#   - Port 3306 available (MySQL)
#   - .env file with WooCommerce credentials
#
# Usage:
#   .\setup-wordpress-automation.ps1
#
# ============================================================================

param(
    [switch]$SkipBackup,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-Header {
    param([string]$Message)
    Write-Host "`n$('=' * 70)" -ForegroundColor Magenta
    Write-Host $Message.PadLeft((70 + $Message.Length) / 2) -ForegroundColor Magenta
    Write-Host "$('=' * 70)`n" -ForegroundColor Magenta
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# ============================================================================
# STEP 1: Pre-flight Checks
# ============================================================================

Write-Header "🔥 CODEX DOMINION - WORDPRESS AUTOMATION 🔥"

Write-Info "Checking prerequisites..."

# Check Docker
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed. Please install Docker Desktop."
    exit 1
}

# Check Docker is running
try {
    docker ps | Out-Null
    Write-Success "Docker is running"
} catch {
    Write-Error "Docker is not running. Please start Docker Desktop."
    exit 1
}

# Check ports
$portsInUse = @()
$portsToCheck = @(8080, 3306)

foreach ($port in $portsToCheck) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        $portsInUse += $port
    }
}

if ($portsInUse.Count -gt 0) {
    Write-Warning "Ports in use: $($portsInUse -join ', ')"
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y') {
        exit 1
    }
}

Write-Success "Pre-flight checks complete"

# ============================================================================
# STEP 2: Backup Existing Data (if requested)
# ============================================================================

if (!$SkipBackup) {
    Write-Info "Creating backup of existing WordPress data..."
    
    $backupDir = "wordpress_backups\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    # Backup docker volumes (if they exist)
    docker volume ls -q | Where-Object { $_ -match "wordpress|mysql" } | ForEach-Object {
        Write-Info "Backing up volume: $_"
        docker run --rm -v ${_}:/source -v ${PWD}/${backupDir}:/backup alpine tar czf /backup/$_.tar.gz -C /source .
    }
    
    Write-Success "Backup saved to: $backupDir"
}

# ============================================================================
# STEP 3: Docker Compose Setup
# ============================================================================

Write-Info "Setting up Docker Compose configuration..."

# Navigate to docker directory
$dockerDir = Join-Path $PSScriptRoot "infra\docker"

if (!(Test-Path $dockerDir)) {
    Write-Warning "Docker directory not found at $dockerDir"
    Write-Info "Creating docker-compose.wordpress.yml in current directory..."
    $dockerDir = $PSScriptRoot
}

Set-Location $dockerDir

# Create docker-compose.wordpress.yml if it doesn't exist
$dockerCompose = @"
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    container_name: codex-wordpress
    restart: always
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: codex-mysql
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress_password_change_me
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress_data:/var/www/html
      - ./wordpress-plugins:/var/www/html/wp-content/plugins/codex-custom
    networks:
      - codex-network

  mysql:
    image: mysql:8.0
    container_name: codex-mysql
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress_password_change_me
      MYSQL_ROOT_PASSWORD: root_password_change_me
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - codex-network
    command: '--default-authentication-plugin=mysql_native_password'

volumes:
  wordpress_data:
  mysql_data:

networks:
  codex-network:
    driver: bridge
"@

$dockerCompose | Out-File -FilePath "docker-compose.wordpress.yml" -Encoding UTF8
Write-Success "Docker Compose configuration created"

# ============================================================================
# STEP 4: Start WordPress & MySQL
# ============================================================================

Write-Info "Starting WordPress and MySQL containers..."

docker-compose -f docker-compose.wordpress.yml up -d

# Wait for services to be healthy
Write-Info "Waiting for services to start (30 seconds)..."
Start-Sleep -Seconds 30

# Check if containers are running
$wpRunning = docker ps --filter "name=codex-wordpress" --format "{{.Status}}" | Select-String "Up"
$mysqlRunning = docker ps --filter "name=codex-mysql" --format "{{.Status}}" | Select-String "Up"

if ($wpRunning -and $mysqlRunning) {
    Write-Success "WordPress and MySQL containers are running"
} else {
    Write-Error "Containers failed to start. Check logs with: docker-compose -f docker-compose.wordpress.yml logs"
    exit 1
}

Write-Info "WordPress available at: http://localhost:8080"

# ============================================================================
# STEP 5: WordPress Initial Setup
# ============================================================================

Write-Info "Waiting for WordPress initialization..."
Start-Sleep -Seconds 10

Write-Header "WORDPRESS SETUP REQUIRED"
Write-Info "Complete WordPress installation:"
Write-Info "1. Open http://localhost:8080 in your browser"
Write-Info "2. Select language: English (United States)"
Write-Info "3. Fill in site information:"
Write-Info "   - Site Title: Codex Dominion"
Write-Info "   - Username: admin (or your choice)"
Write-Info "   - Password: (strong password)"
Write-Info "   - Email: your-email@example.com"
Write-Info "4. Click 'Install WordPress'"

$continue = Read-Host "`nPress ENTER when WordPress installation is complete..."

# ============================================================================
# STEP 6: Install WooCommerce via WP-CLI
# ============================================================================

Write-Info "Installing WooCommerce plugin..."

# Install WP-CLI in the WordPress container
docker exec codex-wordpress bash -c "curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp"

# Install and activate WooCommerce
docker exec codex-wordpress wp plugin install woocommerce --activate --allow-root

Write-Success "WooCommerce installed and activated"

# ============================================================================
# STEP 7: Install Custom Plugins
# ============================================================================

Write-Info "Installing custom Codex Dominion plugins..."

$pluginsDir = Join-Path $PSScriptRoot "wordpress-plugin"

if (Test-Path $pluginsDir) {
    # Copy custom plugins to WordPress container
    Get-ChildItem -Path $pluginsDir -Directory | ForEach-Object {
        $pluginName = $_.Name
        Write-Info "Installing plugin: $pluginName"
        
        docker cp $_.FullName codex-wordpress:/var/www/html/wp-content/plugins/
        docker exec codex-wordpress wp plugin activate $pluginName --allow-root
    }
    
    Write-Success "Custom plugins installed"
} else {
    Write-Warning "Custom plugins directory not found: $pluginsDir"
}

# ============================================================================
# STEP 8: Generate WooCommerce REST API Keys
# ============================================================================

Write-Info "Generating WooCommerce REST API keys..."

Write-Header "MANUAL STEP: GENERATE API KEYS"
Write-Info "Generate WooCommerce REST API keys:"
Write-Info "1. Open http://localhost:8080/wp-admin"
Write-Info "2. Navigate to: WooCommerce → Settings → Advanced → REST API"
Write-Info "3. Click 'Add key'"
Write-Info "4. Fill in:"
Write-Info "   - Description: Codex Dominion API"
Write-Info "   - User: admin (or your WordPress user)"
Write-Info "   - Permissions: Read/Write"
Write-Info "5. Click 'Generate API key'"
Write-Info "6. Copy the Consumer key and Consumer secret"

$continue = Read-Host "`nPress ENTER when API keys are generated..."

# Prompt for API keys
Write-Info "Enter your WooCommerce API credentials:"
$consumerKey = Read-Host "Consumer Key"
$consumerSecret = Read-Host "Consumer Secret" -AsSecureString
$consumerSecretPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($consumerSecret)
)

# ============================================================================
# STEP 9: Update .env Files
# ============================================================================

Write-Info "Updating environment files with API credentials..."

# Update web/.env.local
$webEnvPath = Join-Path $PSScriptRoot "web\.env.local"
$webEnvContent = @"
WC_CONSUMER_KEY=$consumerKey
WC_CONSUMER_SECRET=$consumerSecretPlain
WC_API_URL=http://localhost:8080/wp-json/wc/v3
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
"@

New-Item -ItemType Directory -Path (Split-Path $webEnvPath) -Force -ErrorAction SilentlyContinue | Out-Null
$webEnvContent | Out-File -FilePath $webEnvPath -Encoding UTF8

Write-Success "Updated: web/.env.local"

# Update api/.env
$apiEnvPath = Join-Path $PSScriptRoot "api\.env"
$apiEnvContent = @"
WC_WEBHOOK_SECRET=$(New-Guid)
WC_CONSUMER_KEY=$consumerKey
WC_CONSUMER_SECRET=$consumerSecretPlain
WC_API_URL=http://localhost:8080/wp-json/wc/v3
SITE_URL=http://localhost:4000
"@

New-Item -ItemType Directory -Path (Split-Path $apiEnvPath) -Force -ErrorAction SilentlyContinue | Out-Null
$apiEnvContent | Out-File -FilePath $apiEnvPath -Encoding UTF8

Write-Success "Updated: api/.env"

# ============================================================================
# STEP 10: Configure WooCommerce Webhooks
# ============================================================================

Write-Header "WEBHOOKS CONFIGURATION"

Write-Info "Configure WooCommerce webhooks to enable real-time notifications:"
Write-Info ""
Write-Info "1. Open http://localhost:8080/wp-admin"
Write-Info "2. Navigate to: WooCommerce → Settings → Advanced → Webhooks"
Write-Info "3. Click 'Add webhook' for EACH of the following:"
Write-Info ""

$webhooks = @(
    @{ Name = "Subscription Created"; Topic = "Subscription created"; Delivery = "http://host.docker.internal:4000/webhooks/wc/subscription" },
    @{ Name = "Subscription Updated"; Topic = "Subscription updated"; Delivery = "http://host.docker.internal:4000/webhooks/wc/subscription" },
    @{ Name = "Subscription Deleted"; Topic = "Subscription deleted"; Delivery = "http://host.docker.internal:4000/webhooks/wc/subscription" },
    @{ Name = "Subscription Renewal"; Topic = "Subscription renewal"; Delivery = "http://host.docker.internal:4000/webhooks/wc/subscription" },
    @{ Name = "Subscription Trial End"; Topic = "Subscription trial end"; Delivery = "http://host.docker.internal:4000/webhooks/wc/subscription" },
    @{ Name = "Order Created"; Topic = "Order created"; Delivery = "http://host.docker.internal:4000/webhooks/wc/order" },
    @{ Name = "Order Updated"; Topic = "Order updated"; Delivery = "http://host.docker.internal:4000/webhooks/wc/order" }
)

$webhookSecret = (Get-Content $apiEnvPath | Select-String "WC_WEBHOOK_SECRET=").ToString().Split("=")[1]

foreach ($webhook in $webhooks) {
    Write-Info "   Webhook: $($webhook.Name)"
    Write-Info "   Topic: $($webhook.Topic)"
    Write-Info "   Delivery URL: $($webhook.Delivery)"
    Write-Info "   Secret: $webhookSecret"
    Write-Info ""
}

Write-Warning "Use 'host.docker.internal' instead of 'localhost' for webhook URLs (Docker networking)"

$continue = Read-Host "`nPress ENTER when webhooks are configured..."

# ============================================================================
# STEP 11: Verify Setup
# ============================================================================

Write-Info "Running setup verification..."

# Test WordPress
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Success "WordPress is accessible"
    }
} catch {
    Write-Warning "WordPress check failed: $_"
}

# Test WooCommerce API
try {
    $authHeader = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${consumerKey}:${consumerSecretPlain}"))
    $response = Invoke-WebRequest -Uri "http://localhost:8080/wp-json/wc/v3/products" `
        -Headers @{ Authorization = $authHeader } `
        -UseBasicParsing -TimeoutSec 5
    
    if ($response.StatusCode -eq 200) {
        Write-Success "WooCommerce API is working"
    }
} catch {
    Write-Warning "WooCommerce API check failed: $_"
}

# ============================================================================
# FINAL SUMMARY
# ============================================================================

Write-Header "SETUP COMPLETE! 🔥"

Write-Success "WordPress + WooCommerce setup completed successfully!"
Write-Info ""
Write-Info "Access your installation:"
Write-Info "  • WordPress Frontend: http://localhost:8080"
Write-Info "  • WordPress Admin: http://localhost:8080/wp-admin"
Write-Info "  • WooCommerce: http://localhost:8080/wp-admin/admin.php?page=wc-admin"
Write-Info ""
Write-Info "API Configuration:"
Write-Info "  • Consumer Key: $consumerKey"
Write-Info "  • API Base URL: http://localhost:8080/wp-json/wc/v3"
Write-Info ""
Write-Info "Next Steps:"
Write-Info "  1. Configure WooCommerce settings (currency, shipping, tax)"
Write-Info "  2. Add products and subscriptions"
Write-Info "  3. Test webhook delivery: http://localhost:4000/webhooks/health"
Write-Info "  4. Start backend API: cd api && npm run dev"
Write-Info "  5. Start frontend: cd web && npm run dev"
Write-Info ""
Write-Info "Docker Management:"
Write-Info "  • Stop: docker-compose -f docker-compose.wordpress.yml down"
Write-Info "  • Restart: docker-compose -f docker-compose.wordpress.yml restart"
Write-Info "  • Logs: docker-compose -f docker-compose.wordpress.yml logs -f"
Write-Info ""

Write-Header "🔥 The Flame Burns Sovereign and Eternal! 👑"
