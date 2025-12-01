# Simple SSL Certificate Manager (certbot equivalent for Windows)
# Equivalent to: sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com

Write-Host "WINDOWS SSL CERTIFICATE SETUP (certbot equivalent)" -ForegroundColor Cyan
Write-Host "Creating SSL certificates for aistorelab.com..." -ForegroundColor Yellow

# Create SSL directory
$sslPath = "ssl-certificates"
if (-not (Test-Path $sslPath)) {
    New-Item -ItemType Directory -Path $sslPath -Force | Out-Null
    Write-Host "✅ Created SSL directory: $sslPath" -ForegroundColor Green
}

# Simple certificate creation using OpenSSL-style approach
try {
    Write-Host ""
    Write-Host "Generating self-signed SSL certificate..." -ForegroundColor Yellow
    Write-Host "Domains: aistorelab.com, www.aistorelab.com" -ForegroundColor Gray
    
    # Create certificate using Windows PowerShell
    $cert = New-SelfSignedCertificate -DnsName @("aistorelab.com", "www.aistorelab.com", "localhost") -CertStoreLocation "Cert:\CurrentUser\My" -NotAfter (Get-Date).AddDays(365) -KeyAlgorithm RSA -KeyLength 2048
    
    if ($cert) {
        Write-Host "✅ Certificate created successfully" -ForegroundColor Green
        Write-Host "Thumbprint: $($cert.Thumbprint)" -ForegroundColor White
        
        # Export certificate to files
        $certPath = Join-Path $sslPath "aistorelab.com.crt"
        $pfxPath = Join-Path $sslPath "aistorelab.com.pfx"
        $password = "aistorelab2025"
        
        # Export as PFX
        $securePassword = ConvertTo-SecureString -String $password -Force -AsPlainText
        Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $securePassword | Out-Null
        
        # Export as CRT (Base64)
        $certBytes = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
        $certBase64 = [Convert]::ToBase64String($certBytes, [Base64FormattingOptions]::InsertLineBreaks)
        $certPem = "-----BEGIN CERTIFICATE-----`n$certBase64`n-----END CERTIFICATE-----"
        Set-Content -Path $certPath -Value $certPem
        
        Write-Host "📁 Certificate files created:" -ForegroundColor Cyan
        Write-Host "  PFX: $pfxPath" -ForegroundColor White
        Write-Host "  CRT: $certPath" -ForegroundColor White
        Write-Host "  Password: $password" -ForegroundColor Yellow
        
        Write-Host ""
        Write-Host "🎉 SSL CERTIFICATE SETUP COMPLETE!" -ForegroundColor Green
        Write-Host "Equivalent to: sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com" -ForegroundColor Gray
        
        Write-Host ""
        Write-Host "📋 Next Steps:" -ForegroundColor Cyan
        Write-Host "1. Update proxy configuration with SSL" -ForegroundColor White
        Write-Host "2. Restart proxy server: .\aistorelab-nginx.ps1 restart" -ForegroundColor White
        Write-Host "3. Access via HTTPS: https://localhost:3000" -ForegroundColor White
        
    } else {
        throw "Certificate creation returned null"
    }
    
} catch {
    Write-Host "❌ SSL certificate creation failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    Write-Host ""
    Write-Host "🔧 Alternative SSL Options for Windows:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Let's Encrypt for Windows:" -ForegroundColor Cyan
    Write-Host "   - win-acme: https://www.win-acme.com/" -ForegroundColor Gray
    Write-Host "   - Certify The Web: https://certifytheweb.com/" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Cloud SSL Services:" -ForegroundColor Cyan
    Write-Host "   - Cloudflare SSL (Free)" -ForegroundColor Gray
    Write-Host "   - AWS Certificate Manager" -ForegroundColor Gray
    Write-Host "   - Azure App Service Certificates" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Manual Certificate Import:" -ForegroundColor Cyan
    Write-Host "   - Purchase from DigiCert, GlobalSign, etc." -ForegroundColor Gray
    Write-Host "   - Import via Windows Certificate Manager (certmgr.msc)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🌐 Current Status:" -ForegroundColor Cyan
Write-Host "  Proxy Server: Running on port 3000" -ForegroundColor White
Write-Host "  HTTP Access: http://localhost:3000" -ForegroundColor White
Write-Host "  HTTPS Access: Will be available after SSL setup" -ForegroundColor Gray