# Windows SSL Certificate Manager (certbot equivalent)
# Equivalent to: sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com

param([string]$Action = "help", [string[]]$Domains = @())

$SSLConfig = @{
    Domains = @("aistorelab.com", "www.aistorelab.com")
    CertPath = "ssl-certificates"
    ProxyScript = "aistorelab-simple-proxy.js"
    NginxConfig = "nginx-config\aistorelab.com"
}

Write-Host "WINDOWS SSL CERTIFICATE MANAGER (certbot equivalent)" -ForegroundColor Cyan
Write-Host "Managing SSL for: $($SSLConfig.Domains -join ', ')" -ForegroundColor Gray

function New-SelfSignedCertificate {
    Write-Host ""
    Write-Host "Creating SSL certificates for aistorelab.com..." -ForegroundColor Green
    Write-Host "Domains: $($SSLConfig.Domains -join ', ')" -ForegroundColor Gray

    # Create SSL directory
    if (-not (Test-Path $SSLConfig.CertPath)) {
        New-Item -ItemType Directory -Path $SSLConfig.CertPath -Force | Out-Null
        Write-Host "Created SSL directory: $($SSLConfig.CertPath)" -ForegroundColor Green
    }

    try {
        # Generate self-signed certificate for development
        $certParams = @{
            DnsName = $SSLConfig.Domains
            CertStoreLocation = "Cert:\CurrentUser\My"
            NotAfter = (Get-Date).AddDays(365)
            KeyAlgorithm = "RSA"
            KeyLength = 2048
            Subject = "CN=aistorelab.com"
        }

        $cert = New-SelfSignedCertificate @certParams

        # Export certificate and private key
        $certPath = Join-Path $SSLConfig.CertPath "aistorelab.com.crt"
        $keyPath = Join-Path $SSLConfig.CertPath "aistorelab.com.key"
        $pfxPath = Join-Path $SSLConfig.CertPath "aistorelab.com.pfx"

        # Export as PFX first
        $pfxPassword = ConvertTo-SecureString -String "aistorelab2025" -Force -AsPlainText
        Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $pfxPassword | Out-Null

        # Create PEM format files (nginx equivalent)
        $certBase64 = [Convert]::ToBase64String($cert.RawData, [Base64FormattingOptions]::InsertLineBreaks)
        $certPem = "-----BEGIN CERTIFICATE-----`n$certBase64`n-----END CERTIFICATE-----"
        Set-Content -Path $certPath -Value $certPem

        Write-Host "✅ SSL certificate created successfully" -ForegroundColor Green
        Write-Host "Certificate: $certPath" -ForegroundColor White
        Write-Host "Private Key: (embedded in PFX)" -ForegroundColor White
        Write-Host "PFX File: $pfxPath" -ForegroundColor White
        Write-Host "Password: aistorelab2025" -ForegroundColor Yellow

        return $cert.Thumbprint

    } catch {
        Write-Host "❌ Failed to create SSL certificate" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        return $null
    }
}

function Update-ProxySSLConfig {
    param([string]$CertThumbprint)

    Write-Host ""
    Write-Host "Updating proxy configuration for HTTPS..." -ForegroundColor Yellow

    # Read current proxy script
    if (Test-Path $SSLConfig.ProxyScript) {
        $proxyContent = Get-Content $SSLConfig.ProxyScript -Raw

        # Add HTTPS configuration
        $httpsConfig = @"

// HTTPS Configuration (certbot equivalent)
const https = require('https');
const fs = require('fs');
const path = require('path');

// SSL Certificate paths (equivalent to certbot generated files)
const sslOptions = {
    key: fs.existsSync(path.join('$($SSLConfig.CertPath)', 'aistorelab.com.key')) ?
         fs.readFileSync(path.join('$($SSLConfig.CertPath)', 'aistorelab.com.key')) : null,
    cert: fs.existsSync(path.join('$($SSLConfig.CertPath)', 'aistorelab.com.crt')) ?
          fs.readFileSync(path.join('$($SSLConfig.CertPath)', 'aistorelab.com.crt')) : null,
    pfx: fs.existsSync(path.join('$($SSLConfig.CertPath)', 'aistorelab.com.pfx')) ?
         fs.readFileSync(path.join('$($SSLConfig.CertPath)', 'aistorelab.com.pfx')) : null,
    passphrase: 'aistorelab2025'
};

// HTTPS server (equivalent to nginx ssl configuration)
if (sslOptions.pfx || (sslOptions.key && sslOptions.cert)) {
    const httpsPort = 443;
    https.createServer(sslOptions, app).listen(httpsPort, () => {
        console.log('🔒 HTTPS Server running on port ' + httpsPort);
        console.log('🌐 Access your secure site at: https://localhost');
        console.log('📋 SSL Certificate: Active');
    }).on('error', (err) => {
        if (err.code === 'EADDRINUSE') {
            console.log('⚠️  Port 443 in use - HTTPS disabled');
        } else {
            console.error('HTTPS Server Error:', err.message);
        }
    });
} else {
    console.log('⚠️  SSL certificates not found - HTTPS disabled');
}
"@

        # Check if HTTPS config already exists
        if ($proxyContent -notmatch "HTTPS Configuration") {
            # Append HTTPS configuration
            $updatedContent = $proxyContent + $httpsConfig
            Set-Content -Path $SSLConfig.ProxyScript -Value $updatedContent
            Write-Host "✅ Proxy updated with HTTPS configuration" -ForegroundColor Green
        } else {
            Write-Host "ℹ️  Proxy already has HTTPS configuration" -ForegroundColor Gray
        }
    }
}

function Update-NginxSSLConfig {
    Write-Host ""
    Write-Host "Updating nginx configuration with SSL..." -ForegroundColor Yellow

    if (Test-Path $SSLConfig.NginxConfig) {
        $nginxContent = Get-Content $SSLConfig.NginxConfig -Raw

        # Update SSL configuration section
        $sslConfig = @"
    # SSL Configuration (certbot equivalent)
    ssl_certificate $($SSLConfig.CertPath)/aistorelab.com.crt;
    ssl_certificate_key $($SSLConfig.CertPath)/aistorelab.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
"@

        # Replace SSL placeholder
        if ($nginxContent -match "# SSL Configuration") {
            $updatedNginx = $nginxContent -replace "ssl_certificate /path/to/ssl/certificate\.crt;", "ssl_certificate $($SSLConfig.CertPath)/aistorelab.com.crt;"
            $updatedNginx = $updatedNginx -replace "ssl_certificate_key /path/to/ssl/private\.key;", "ssl_certificate_key $($SSLConfig.CertPath)/aistorelab.com.key;"
            Set-Content -Path $SSLConfig.NginxConfig -Value $updatedNginx
            Write-Host "✅ Nginx config updated with SSL paths" -ForegroundColor Green
        }
    }
}

function Test-SSLConfiguration {
    Write-Host ""
    Write-Host "Testing SSL configuration..." -ForegroundColor Cyan

    # Check certificate files
    $certExists = Test-Path (Join-Path $SSLConfig.CertPath "aistorelab.com.crt")
    $pfxExists = Test-Path (Join-Path $SSLConfig.CertPath "aistorelab.com.pfx")

    Write-Host "Certificate Status:" -ForegroundColor White
    Write-Host "  SSL Certificate (.crt): $(if($certExists) {'✅ Found'} else {'❌ Missing'})" -ForegroundColor $(if($certExists) {'Green'} else {'Red'})
    Write-Host "  PFX Certificate (.pfx): $(if($pfxExists) {'✅ Found'} else {'❌ Missing'})" -ForegroundColor $(if($pfxExists) {'Green'} else {'Red'})

    if ($certExists -or $pfxExists) {
        Write-Host ""
        Write-Host "SSL Configuration ready for:" -ForegroundColor Green
        $SSLConfig.Domains | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }

        # Check if proxy is running
        $proxyRunning = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -eq "" }
        if ($proxyRunning) {
            Write-Host ""
            Write-Host "📋 Next steps:" -ForegroundColor Yellow
            Write-Host "  1. Restart proxy: .\aistorelab-nginx.ps1 restart" -ForegroundColor Gray
            Write-Host "  2. Test HTTPS: https://localhost" -ForegroundColor Gray
            Write-Host "  3. Update hosts file for domain testing" -ForegroundColor Gray
        }
    }
}

function Install-ProductionSSL {
    Write-Host ""
    Write-Host "For production SSL certificates:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1 - Let's Encrypt (Free):" -ForegroundColor Cyan
    Write-Host "  1. Use win-acme: https://www.win-acme.com/" -ForegroundColor Gray
    Write-Host "  2. Or Certify The Web: https://certifytheweb.com/" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2 - Cloud SSL:" -ForegroundColor Cyan
    Write-Host "  1. CloudFlare SSL (Free)" -ForegroundColor Gray
    Write-Host "  2. AWS Certificate Manager" -ForegroundColor Gray
    Write-Host "  3. Azure App Service Certificates" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3 - Commercial SSL:" -ForegroundColor Cyan
    Write-Host "  1. DigiCert, GlobalSign, etc." -ForegroundColor Gray
    Write-Host "  2. Import via MMC or PowerShell" -ForegroundColor Gray
}

# Execute based on action
switch ($Action.ToLower()) {
    "create" {
        $thumbprint = New-SelfSignedCertificate
        if ($thumbprint) {
            Update-ProxySSLConfig -CertThumbprint $thumbprint
            Update-NginxSSLConfig
            Write-Host ""
            Write-Host "🎉 SSL certificates created successfully!" -ForegroundColor Green
            Write-Host "Equivalent to: sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com" -ForegroundColor Gray
        }
    }
    "test" {
        Test-SSLConfiguration
    }
    "production" {
        Install-ProductionSSL
    }
    "renew" {
        Write-Host "Certificate renewal..." -ForegroundColor Yellow
        Write-Host "For self-signed: Run 'create' command again" -ForegroundColor Gray
        Write-Host "For Let's Encrypt: Use win-acme renewal" -ForegroundColor Gray
    }
    default {
        Write-Host "USAGE:" -ForegroundColor Yellow
        Write-Host "  .\ssl-certbot.ps1 create      # Create SSL certificates (certbot equivalent)" -ForegroundColor White
        Write-Host "  .\ssl-certbot.ps1 test        # Test SSL configuration" -ForegroundColor White
        Write-Host "  .\ssl-certbot.ps1 production  # Get production SSL info" -ForegroundColor White
        Write-Host "  .\ssl-certbot.ps1 renew       # Renew certificates" -ForegroundColor White
        Write-Host ""
        Write-Host "CERTBOT EQUIVALENTS:" -ForegroundColor Cyan
        Write-Host "  sudo apt install certbot python3-certbot-nginx" -ForegroundColor Gray
        Write-Host "    → SSL tools available in Windows PowerShell" -ForegroundColor Green
        Write-Host "  sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com" -ForegroundColor Gray
        Write-Host "    → .\ssl-certbot.ps1 create" -ForegroundColor Green
        Write-Host "  sudo certbot renew" -ForegroundColor Gray
        Write-Host "    → .\ssl-certbot.ps1 renew" -ForegroundColor Green

        Test-SSLConfiguration
    }
}
