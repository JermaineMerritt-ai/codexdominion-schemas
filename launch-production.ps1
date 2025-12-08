# ==============================================================================
# Codex Dominion - Production Launch Script
# ==============================================================================
# This script automates pre-flight checks and production deployment
# Run with: .\launch-production.ps1
# ==============================================================================

param(
    [switch]$SkipChecks,
    [switch]$DryRun,
    [switch]$RollbackMode
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# ==============================================================================
# Configuration
# ==============================================================================
$DOMAIN = "codexdominion.app"
$API_DOMAIN = "api.codexdominion.app"
$COMPOSE_FILE = "docker-compose.production.yml"
$BACKUP_DIR = "./backups"
$LOG_FILE = "./logs/deployment_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# ==============================================================================
# Helper Functions
# ==============================================================================

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $LOG_FILE -Value $logMessage
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Test-Port {
    param([string]$Host, [int]$Port, [int]$Timeout = 5)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $asyncResult = $tcpClient.BeginConnect($Host, $Port, $null, $null)
        $wait = $asyncResult.AsyncWaitHandle.WaitOne($Timeout * 1000, $false)

        if ($wait) {
            $tcpClient.EndConnect($asyncResult)
            $tcpClient.Close()
            return $true
        } else {
            $tcpClient.Close()
            return $false
        }
    } catch {
        return $false
    }
}

# ==============================================================================
# Pre-Flight Checks
# ==============================================================================

function Invoke-PreFlightChecks {
    Write-Log "🔍 Starting Pre-Flight Checks..." "INFO"

    $checksPassed = $true

    # Check 1: Required commands available
    Write-Log "Checking required commands..." "INFO"
    $requiredCommands = @("docker", "docker-compose", "curl", "git")
    foreach ($cmd in $requiredCommands) {
        if (Test-Command $cmd) {
            Write-Log "✅ $cmd found" "INFO"
        } else {
            Write-Log "❌ $cmd not found - please install" "ERROR"
            $checksPassed = $false
        }
    }

    # Check 2: Environment files exist
    Write-Log "Checking environment files..." "INFO"
    $envFiles = @(".env", ".env.production", "frontend/.env.production")
    foreach ($file in $envFiles) {
        if (Test-Path $file) {
            Write-Log "✅ $file exists" "INFO"
        } else {
            Write-Log "❌ $file missing" "ERROR"
            $checksPassed = $false
        }
    }

    # Check 3: Docker Compose file exists
    if (Test-Path $COMPOSE_FILE) {
        Write-Log "✅ $COMPOSE_FILE exists" "INFO"
    } else {
        Write-Log "❌ $COMPOSE_FILE missing" "ERROR"
        $checksPassed = $false
    }

    # Check 4: Verify secrets are not default values
    Write-Log "Checking for production secrets..." "INFO"
    $envContent = Get-Content ".env.production" -Raw
    if ($envContent -match "CHANGE_THIS") {
        Write-Log "⚠️ WARNING: Default placeholder values detected in .env.production" "WARN"
        Write-Log "   Please update SECRET_KEY, JWT_SECRET, API_KEY, and DATABASE_URL" "WARN"
        $checksPassed = $false
    } else {
        Write-Log "✅ Production secrets appear to be set" "INFO"
    }

    # Check 5: DNS Resolution
    Write-Log "Checking DNS resolution..." "INFO"
    try {
        $dnsResult = Resolve-DnsName $DOMAIN -ErrorAction Stop
        Write-Log "✅ DNS resolves for $DOMAIN" "INFO"
    } catch {
        Write-Log "⚠️ WARNING: DNS not resolving for $DOMAIN" "WARN"
    }

    # Check 6: Docker daemon running
    Write-Log "Checking Docker daemon..." "INFO"
    try {
        docker ps | Out-Null
        Write-Log "✅ Docker daemon is running" "INFO"
    } catch {
        Write-Log "❌ Docker daemon is not running" "ERROR"
        $checksPassed = $false
    }

    if ($checksPassed) {
        Write-Log "✅ All pre-flight checks passed!" "INFO"
        return $true
    } else {
        Write-Log "❌ Pre-flight checks failed. Please resolve issues before deployment." "ERROR"
        return $false
    }
}

# ==============================================================================
# Backup Functions
# ==============================================================================

function Invoke-Backup {
    Write-Log "📦 Creating backup before deployment..." "INFO"

    # Create backup directory if not exists
    if (!(Test-Path $BACKUP_DIR)) {
        New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
    }

    $backupTimestamp = Get-Date -Format "yyyyMMdd_HHmmss"

    # Backup environment files
    Copy-Item ".env.production" "$BACKUP_DIR/.env.production.$backupTimestamp" -ErrorAction SilentlyContinue
    Write-Log "✅ Environment files backed up" "INFO"

    # Backup database (if PostgreSQL is accessible)
    if (Test-Command "pg_dump") {
        Write-Log "Attempting database backup..." "INFO"
        # Note: Requires DATABASE_URL to be set
        # pg_dump command would go here if database is accessible
        Write-Log "ℹ️ Database backup requires manual execution with pg_dump" "INFO"
    }

    Write-Log "✅ Backup completed" "INFO"
}

# ==============================================================================
# Deployment Functions
# ==============================================================================

function Invoke-Deployment {
    Write-Log "🚀 Starting production deployment..." "INFO"

    try {
        # Build Docker images
        Write-Log "Building Docker images..." "INFO"
        docker-compose -f $COMPOSE_FILE build --no-cache

        # Start services
        Write-Log "Starting services..." "INFO"
        docker-compose -f $COMPOSE_FILE up -d

        # Wait for services to initialize
        Write-Log "Waiting for services to start (30 seconds)..." "INFO"
        Start-Sleep -Seconds 30

        # Check container health
        Write-Log "Checking container health..." "INFO"
        $containers = docker ps --format "{{.Names}}: {{.Status}}"
        foreach ($container in $containers) {
            Write-Log "  $container" "INFO"
        }

        Write-Log "✅ Deployment completed successfully!" "INFO"
        return $true

    } catch {
        Write-Log "❌ Deployment failed: $_" "ERROR"
        return $false
    }
}

# ==============================================================================
# Health Check Functions
# ==============================================================================

function Test-ServiceHealth {
    Write-Log "🏥 Running health checks..." "INFO"

    $allHealthy = $true

    # Check main site
    Write-Log "Checking $DOMAIN..." "INFO"
    try {
        $response = Invoke-WebRequest -Uri "https://$DOMAIN" -Method Head -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ $DOMAIN is healthy (200 OK)" "INFO"
        } else {
            Write-Log "⚠️ $DOMAIN returned status $($response.StatusCode)" "WARN"
            $allHealthy = $false
        }
    } catch {
        Write-Log "❌ $DOMAIN health check failed: $_" "ERROR"
        $allHealthy = $false
    }

    # Check API endpoint
    Write-Log "Checking $API_DOMAIN/health..." "INFO"
    try {
        $response = Invoke-WebRequest -Uri "https://$API_DOMAIN/health" -Method Get -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ API is healthy (200 OK)" "INFO"
        } else {
            Write-Log "⚠️ API returned status $($response.StatusCode)" "WARN"
            $allHealthy = $false
        }
    } catch {
        Write-Log "❌ API health check failed: $_" "ERROR"
        $allHealthy = $false
    }

    return $allHealthy
}

# ==============================================================================
# Rollback Functions
# ==============================================================================

function Invoke-Rollback {
    Write-Log "🔄 Initiating rollback..." "INFO"

    try {
        # Stop current deployment
        Write-Log "Stopping current services..." "INFO"
        docker-compose -f $COMPOSE_FILE down

        # Restore from backup (would need to be implemented)
        Write-Log "Restore backup manually if needed" "WARN"

        Write-Log "✅ Rollback completed" "INFO"

    } catch {
        Write-Log "❌ Rollback failed: $_" "ERROR"
    }
}

# ==============================================================================
# Main Execution
# ==============================================================================

function Main {
    Write-Log "========================================" "INFO"
    Write-Log "Codex Dominion Production Launch" "INFO"
    Write-Log "========================================" "INFO"

    # Create logs directory
    $logDir = Split-Path -Parent $LOG_FILE
    if (!(Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir | Out-Null
    }

    # Handle rollback mode
    if ($RollbackMode) {
        Invoke-Rollback
        return
    }

    # Run pre-flight checks
    if (!$SkipChecks) {
        $checksPass = Invoke-PreFlightChecks
        if (!$checksPass) {
            Write-Log "Pre-flight checks failed. Aborting deployment." "ERROR"
            Write-Log "Run with -SkipChecks to bypass (not recommended)" "WARN"
            exit 1
        }
    } else {
        Write-Log "⚠️ Skipping pre-flight checks (use with caution)" "WARN"
    }

    # Create backup
    Invoke-Backup

    # Dry run mode
    if ($DryRun) {
        Write-Log "🔍 DRY RUN MODE - No actual deployment" "INFO"
        Write-Log "Would execute: docker-compose -f $COMPOSE_FILE up -d" "INFO"
        return
    }

    # Execute deployment
    $deploySuccess = Invoke-Deployment

    if ($deploySuccess) {
        # Wait a bit for services to fully start
        Start-Sleep -Seconds 10

        # Run health checks
        $healthyServices = Test-ServiceHealth

        if ($healthyServices) {
            Write-Log "========================================" "INFO"
            Write-Log "🎉 DEPLOYMENT SUCCESSFUL!" "INFO"
            Write-Log "========================================" "INFO"
            Write-Log "Site: https://$DOMAIN" "INFO"
            Write-Log "API: https://$API_DOMAIN" "INFO"
            Write-Log "Monitor logs: docker-compose -f $COMPOSE_FILE logs -f" "INFO"
        } else {
            Write-Log "⚠️ Deployment completed but health checks failed" "WARN"
            Write-Log "Check logs: docker-compose -f $COMPOSE_FILE logs" "WARN"
        }
    } else {
        Write-Log "❌ Deployment failed. Check logs for details." "ERROR"
        Write-Log "To rollback: .\launch-production.ps1 -RollbackMode" "ERROR"
        exit 1
    }
}

# ==============================================================================
# Script Entry Point
# ==============================================================================

try {
    Main
} catch {
    Write-Log "❌ Unexpected error: $_" "ERROR"
    exit 1
}
