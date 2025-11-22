# Simple SSL Certificate Creator (certbot equivalent)
Write-Host "CREATING SSL CERTIFICATES FOR AISTORELAB.COM" -ForegroundColor Cyan
Write-Host "Equivalent to: sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com" -ForegroundColor Gray

# Create SSL directory
$sslPath = "ssl-certificates"
New-Item -ItemType Directory -Path $sslPath -Force -ErrorAction SilentlyContinue | Out-Null
Write-Host "Created SSL directory: $sslPath" -ForegroundColor Green

try {
    # Create self-signed certificate
    $domains = @("aistorelab.com", "www.aistorelab.com", "localhost")
    $cert = New-SelfSignedCertificate -DnsName $domains -CertStoreLocation "Cert:\CurrentUser\My" -NotAfter (Get-Date).AddDays(365)
    
    # Export certificate files
    $pfxPath = Join-Path $sslPath "aistorelab.com.pfx"
    $certPath = Join-Path $sslPath "aistorelab.com.crt"
    $password = "aistorelab2025"
    
    # Export PFX
    $securePassword = ConvertTo-SecureString -String $password -Force -AsPlainText
    Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $securePassword | Out-Null
    
    # Export CRT
    $certBytes = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
    $certBase64 = [Convert]::ToBase64String($certBytes, 1)
    $certPem = "-----BEGIN CERTIFICATE-----`n$certBase64`n-----END CERTIFICATE-----"
    Set-Content -Path $certPath -Value $certPem
    
    Write-Host ""
    Write-Host "SSL CERTIFICATE CREATED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "Certificate: $certPath" -ForegroundColor White
    Write-Host "PFX File: $pfxPath" -ForegroundColor White  
    Write-Host "Password: $password" -ForegroundColor Yellow
    Write-Host "Domains: aistorelab.com, www.aistorelab.com" -ForegroundColor White
    
} catch {
    Write-Host "Certificate creation failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Update proxy with SSL configuration" -ForegroundColor White
Write-Host "2. Restart proxy: .\aistorelab-nginx.ps1 restart" -ForegroundColor White
Write-Host "3. Access via HTTPS: https://localhost:3000" -ForegroundColor White