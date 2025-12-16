Write-Host "`n🌐 DNS CONFIGURATION VERIFICATION" -ForegroundColor Cyan
Write-Host "===================================`n" -ForegroundColor Cyan

$domains = @(
    @{Name = "Root Domain"; Domain = "codexdominion.app"; Expected = "mango-wave-0fcc4e40f.3.azurestaticapps.net"},
    @{Name = "API Subdomain"; Domain = "api.codexdominion.app"; Expected = "codex-backend-api.eastus2.azurecontainer.io"}
)

foreach ($entry in $domains) {
    Write-Host "Checking $($entry.Name): $($entry.Domain)" -ForegroundColor White

    try {
        $result = Resolve-DnsName -Name $entry.Domain -Type CNAME -ErrorAction Stop 2>$null

        if ($result) {
            $target = $result | Where-Object {$_.Type -eq "CNAME"} | Select-Object -First 1 -ExpandProperty NameHost

            if ($target -like "*$($entry.Expected)*") {
                Write-Host "  ✅ CONFIGURED: $target" -ForegroundColor Green
            } else {
                Write-Host "  ⚠️  FOUND: $target" -ForegroundColor Yellow
                Write-Host "     EXPECTED: $($entry.Expected)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  ⏳ NOT YET PROPAGATED (this is normal, wait 5-30 minutes)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⏳ NOT CONFIGURED YET (add DNS records at your provider)" -ForegroundColor Yellow
    }

    Write-Host ""
}

Write-Host "`n📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. If showing '⏳ NOT CONFIGURED': Add DNS records at your provider" -ForegroundColor White
Write-Host "2. If showing '⏳ NOT YET PROPAGATED': Wait 5-30 minutes and run script again" -ForegroundColor White
Write-Host "3. If showing '✅ CONFIGURED': Proceed to bind domain in Azure" -ForegroundColor White

Write-Host "`n🔗 Useful Links:" -ForegroundColor Cyan
Write-Host "  DNS Checker: https://dnschecker.org/#CNAME/codexdominion.app" -ForegroundColor Gray
Write-Host "  Azure Portal: https://portal.azure.com" -ForegroundColor Gray
Write-Host "  Configuration Guide: .\configure-dns.md" -ForegroundColor Gray
Write-Host ""
