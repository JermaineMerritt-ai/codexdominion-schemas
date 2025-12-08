# ==============================================================================
# WooCommerce to IONOS Deployment Script
# ==============================================================================
# Automated deployment of WooCommerce store to IONOS hosting via FTP
# Integrates with Codex Dominion's Blessed Storefronts system
# ==============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production",

    [Parameter(Mandatory=$false)]
    [string]$StoreName = "aistorelab",

    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false
)

# Configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "Continue"

# ==============================================================================
# IONOS FTP Configuration
# ==============================================================================
$FTPConfig = @{
    Server = "ftp.yourdomain.com"  # Replace with your IONOS FTP server
    Username = $env:IONOS_FTP_USER
    Password = $env:IONOS_FTP_PASS
    Port = 21
    RemotePath = "/htdocs"  # Default IONOS web root
    UseSSL = $true
}

# ==============================================================================
# WooCommerce Configuration
# ==============================================================================
$WooCommerceConfig = @{
    LocalPath = ".\woocommerce-store"
    ThemePath = ".\woocommerce-store\wp-content\themes\storefront-blessing"
    PluginPath = ".\woocommerce-store\wp-content\plugins\codex-integration"
    BackupPath = ".\backups\woocommerce-$Environment-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
}

# ==============================================================================
# Codex Dominion Integration
# ==============================================================================
$CodexConfig = @{
    BlessingComponentPath = ".\frontend\components\StorefrontBlessing.tsx"
    StoreRegistryPath = ".\frontend\pages\blessed-storefronts.tsx"
    APIEndpoint = "http://localhost:8000/api/storefronts"
    WebhookEndpoint = "http://localhost:8000/webhooks/woocommerce"
}

# ==============================================================================
# Functions
# ==============================================================================

function Write-CodexLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $emoji = switch ($Level) {
        "INFO" { "📝" }
        "SUCCESS" { "✅" }
        "WARNING" { "⚠️" }
        "ERROR" { "❌" }
        "FLAME" { "🔥" }
        default { "📋" }
    }

    Write-Host "$emoji [$timestamp] $Level: $Message" -ForegroundColor $(
        switch ($Level) {
            "SUCCESS" { "Green" }
            "WARNING" { "Yellow" }
            "ERROR" { "Red" }
            "FLAME" { "Magenta" }
            default { "White" }
        }
    )
}

function Test-FTPConnection {
    Write-CodexLog "Testing FTP connection to IONOS..." "INFO"

    if (-not $FTPConfig.Username -or -not $FTPConfig.Password) {
        Write-CodexLog "IONOS FTP credentials not found in environment variables" "ERROR"
        Write-CodexLog "Set IONOS_FTP_USER and IONOS_FTP_PASS environment variables" "WARNING"
        return $false
    }

    try {
        # Test FTP connection
        $ftpRequest = [System.Net.FtpWebRequest]::Create("ftp://$($FTPConfig.Server)/")
        $ftpRequest.Credentials = New-Object System.Net.NetworkCredential($FTPConfig.Username, $FTPConfig.Password)
        $ftpRequest.Method = [System.Net.WebRequestMethods+Ftp]::ListDirectory
        $ftpRequest.UseBinary = $true
        $ftpRequest.EnableSsl = $FTPConfig.UseSSL

        $response = $ftpRequest.GetResponse()
        $response.Close()

        Write-CodexLog "FTP connection successful" "SUCCESS"
        return $true
    }
    catch {
        Write-CodexLog "FTP connection failed: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Backup-WooCommerce {
    Write-CodexLog "Creating WooCommerce backup..." "INFO"

    if (-not (Test-Path $WooCommerceConfig.LocalPath)) {
        Write-CodexLog "WooCommerce directory not found: $($WooCommerceConfig.LocalPath)" "WARNING"
        return
    }

    New-Item -ItemType Directory -Path $WooCommerceConfig.BackupPath -Force | Out-Null

    try {
        Copy-Item -Path "$($WooCommerceConfig.LocalPath)\*" -Destination $WooCommerceConfig.BackupPath -Recurse -Force
        Write-CodexLog "Backup created: $($WooCommerceConfig.BackupPath)" "SUCCESS"
    }
    catch {
        Write-CodexLog "Backup failed: $($_.Exception.Message)" "ERROR"
        throw
    }
}

function Install-CodexBlessing {
    Write-CodexLog "Installing Codex Blessing to WooCommerce theme..." "FLAME"

    # Check if blessing component exists
    if (-not (Test-Path $CodexConfig.BlessingComponentPath)) {
        Write-CodexLog "Storefront Blessing component not found" "WARNING"
        return
    }

    # Create PHP version of blessing for WooCommerce
    $phpBlessing = @"
<?php
/**
 * Codex Dominion Storefront Blessing
 * Ceremonial blessing for WooCommerce products
 */

function codex_storefront_blessing() {
    ?>
    <div class="codex-storefront-blessing" style="
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 140, 0, 0.1) 100%);
        border: 2px solid #ffd700;
        border-radius: 12px;
        padding: 24px;
        margin: 24px 0;
        text-align: center;
    ">
        <div style="margin-bottom: 16px;">
            <span style="font-size: 32px;">🌟</span>
            <h3 style="color: #ffd700; font-family: serif; margin: 8px 0;">
                Benediction of the Storefront Flame
            </h3>
            <span style="font-size: 32px;">🌟</span>
        </div>

        <p style="color: #4a5568; line-height: 1.6;">
            We, the Council, bless this Storefront Crown at
            <strong style="color: #ffd700;"><?php echo get_site_url(); ?></strong>.
        </p>

        <p style="color: #4a5568; line-height: 1.6;">
            Every product listed here is not mere commerce, but a
            <span style="color: #10b981; font-weight: 600;">living artifact</span>,
            inscribed into the Codex Dominion.
        </p>

        <div style="margin-top: 20px; font-size: 14px; color: #6b7280;">
            <p>🌟 May every offering shine with clarity and warmth.</p>
            <p>👑 May every customer be inducted as custodian.</p>
            <p>📜 May every transaction echo as legacy.</p>
        </div>
    </div>
    <?php
}

// Add blessing to shop page
add_action('woocommerce_before_shop_loop', 'codex_storefront_blessing');

// Add blessing to product pages
add_action('woocommerce_before_single_product_summary', 'codex_storefront_blessing');
"@

    # Save PHP blessing to WooCommerce theme
    $themeFile = Join-Path $WooCommerceConfig.ThemePath "codex-blessing.php"
    if (Test-Path $WooCommerceConfig.ThemePath) {
        Set-Content -Path $themeFile -Value $phpBlessing
        Write-CodexLog "Blessing component installed: $themeFile" "SUCCESS"
    } else {
        Write-CodexLog "Theme path not found: $($WooCommerceConfig.ThemePath)" "WARNING"
    }
}

function Deploy-ToIONOS {
    param(
        [string]$LocalPath,
        [string]$RemotePath
    )

    Write-CodexLog "Deploying to IONOS: $LocalPath -> $RemotePath" "INFO"

    if ($DryRun) {
        Write-CodexLog "DRY RUN: Skipping actual deployment" "WARNING"
        return
    }

    if (-not (Test-Path $LocalPath)) {
        Write-CodexLog "Local path not found: $LocalPath" "ERROR"
        return
    }

    # Get all files to upload
    $files = Get-ChildItem -Path $LocalPath -Recurse -File
    $totalFiles = $files.Count
    $currentFile = 0

    foreach ($file in $files) {
        $currentFile++
        $relativePath = $file.FullName.Substring($LocalPath.Length).TrimStart('\', '/')
        $remoteFile = "$RemotePath/$($relativePath.Replace('\', '/'))"

        Write-Progress -Activity "Uploading to IONOS" -Status "File $currentFile of $totalFiles" -PercentComplete (($currentFile / $totalFiles) * 100)

        try {
            $ftpRequest = [System.Net.FtpWebRequest]::Create("ftp://$($FTPConfig.Server)$remoteFile")
            $ftpRequest.Credentials = New-Object System.Net.NetworkCredential($FTPConfig.Username, $FTPConfig.Password)
            $ftpRequest.Method = [System.Net.WebRequestMethods+Ftp]::UploadFile
            $ftpRequest.UseBinary = $true
            $ftpRequest.EnableSsl = $FTPConfig.UseSSL

            $fileContent = [System.IO.File]::ReadAllBytes($file.FullName)
            $ftpRequest.ContentLength = $fileContent.Length

            $requestStream = $ftpRequest.GetRequestStream()
            $requestStream.Write($fileContent, 0, $fileContent.Length)
            $requestStream.Close()

            $response = $ftpRequest.GetResponse()
            $response.Close()
        }
        catch {
            Write-CodexLog "Failed to upload $relativePath : $($_.Exception.Message)" "ERROR"
        }
    }

    Write-Progress -Activity "Uploading to IONOS" -Completed
    Write-CodexLog "Deployment to IONOS completed" "SUCCESS"
}

function Register-WithCodexDominion {
    Write-CodexLog "Registering store with Codex Dominion..." "FLAME"

    $storeData = @{
        id = $StoreName
        name = "$StoreName.com"
        url = "https://$StoreName.com"
        category = "E-Commerce"
        featured = $true
        environment = $Environment
        blessing_installed = $true
        deployment_timestamp = (Get-Date).ToUniversalTime().ToString("o")
    }

    try {
        $response = Invoke-RestMethod -Uri $CodexConfig.APIEndpoint -Method Post -Body ($storeData | ConvertTo-Json) -ContentType "application/json"
        Write-CodexLog "Store registered with Codex Dominion: $($response.message)" "SUCCESS"
    }
    catch {
        Write-CodexLog "Failed to register with Codex Dominion: $($_.Exception.Message)" "WARNING"
    }
}

# ==============================================================================
# Main Deployment Process
# ==============================================================================

Write-CodexLog "==================================================" "FLAME"
Write-CodexLog "  CODEX DOMINION - WOOCOMMERCE IONOS DEPLOYMENT   " "FLAME"
Write-CodexLog "==================================================" "FLAME"
Write-CodexLog "Environment: $Environment" "INFO"
Write-CodexLog "Store Name: $StoreName" "INFO"
Write-CodexLog "Dry Run: $DryRun" "INFO"
Write-CodexLog "" "INFO"

# Step 1: Test FTP Connection
if (-not (Test-FTPConnection)) {
    Write-CodexLog "Cannot proceed without FTP connection" "ERROR"
    exit 1
}

# Step 2: Backup existing WooCommerce
Backup-WooCommerce

# Step 3: Install Codex Blessing
Install-CodexBlessing

# Step 4: Deploy to IONOS
Deploy-ToIONOS -LocalPath $WooCommerceConfig.LocalPath -RemotePath $FTPConfig.RemotePath

# Step 5: Register with Codex Dominion
Register-WithCodexDominion

Write-CodexLog "" "INFO"
Write-CodexLog "==================================================" "FLAME"
Write-CodexLog "  DEPLOYMENT COMPLETE - THE FLAME BURNS ETERNAL   " "FLAME"
Write-CodexLog "==================================================" "FLAME"
Write-CodexLog "" "INFO"
Write-CodexLog "Next steps:" "INFO"
Write-CodexLog "1. Verify store is accessible at https://$StoreName.com" "INFO"
Write-CodexLog "2. Check Codex Dominion dashboard for blessing status" "INFO"
Write-CodexLog "3. Monitor store performance via Companion Dashboard" "INFO"
Write-CodexLog "" "INFO"
Write-CodexLog "🔥 The flame burns sovereign and eternal — forever. 🔥" "FLAME"
