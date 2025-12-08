# Generate self-signed SSL certificates for Codex Dominion

Write-Host "🔐 Generating self-signed SSL certificates..." -ForegroundColor Cyan

# Create self-signed certificate
$cert = New-SelfSignedCertificate `
    -DnsName "localhost", "codex-dominion.local", "127.0.0.1" `
    -CertStoreLocation "cert:\CurrentUser\My" `
    -NotAfter (Get-Date).AddYears(1) `
    -KeyExportPolicy Exportable `
    -KeySpec Signature `
    -KeyLength 2048 `
    -KeyAlgorithm RSA `
    -HashAlgorithm SHA256

Write-Host "✅ Certificate created with thumbprint: $($cert.Thumbprint)" -ForegroundColor Green

# Export to PFX
$pwd = ConvertTo-SecureString -String "temppass" -Force -AsPlainText
$pfxPath = Join-Path $PSScriptRoot "localhost.pfx"
Export-PfxCertificate -Cert "cert:\CurrentUser\My\$($cert.Thumbprint)" -FilePath $pfxPath -Password $pwd | Out-Null

# Convert PFX to PEM format
$pfx = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($pfxPath, "temppass", [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::Exportable)

# Export certificate as PEM
$certPem = "-----BEGIN CERTIFICATE-----`n"
$certPem += [System.Convert]::ToBase64String($pfx.RawData, [System.Base64FormattingOptions]::InsertLineBreaks)
$certPem += "`n-----END CERTIFICATE-----`n"
$certPath = Join-Path $PSScriptRoot "fullchain.pem"
[System.IO.File]::WriteAllText($certPath, $certPem)

# Export private key as PEM
$rsa = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($pfx)
$keyBytes = $rsa.ExportRSAPrivateKey()
$keyPem = "-----BEGIN RSA PRIVATE KEY-----`n"
$keyPem += [System.Convert]::ToBase64String($keyBytes, [System.Base64FormattingOptions]::InsertLineBreaks)
$keyPem += "`n-----END RSA PRIVATE KEY-----`n"
$keyPath = Join-Path $PSScriptRoot "privkey.pem"
[System.IO.File]::WriteAllText($keyPath, $keyPem)

# Cleanup
Remove-Item $pfxPath -Force

Write-Host "`n✅ SSL certificates generated successfully!" -ForegroundColor Green
Write-Host "   📄 Certificate: $certPath" -ForegroundColor Yellow
Write-Host "   🔑 Private Key: $keyPath" -ForegroundColor Yellow
Write-Host "`n⚠️  These are self-signed certificates for development only." -ForegroundColor Magenta
Write-Host "   For production, use Let's Encrypt or a trusted CA." -ForegroundColor Magenta

Get-ChildItem $PSScriptRoot -Filter "*.pem" | Format-Table Name, Length, LastWriteTime -AutoSize
