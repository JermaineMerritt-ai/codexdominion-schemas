#!/usr/bin/env pwsh
# =============================================================================
# AZURE DNS SETUP COMPLETE - ACTION REQUIRED IN GOOGLE DOMAINS
# =============================================================================

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "🎉 AZURE DNS ZONE CREATED SUCCESSFULLY" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ DNS Zone: codexdominion.app" -ForegroundColor Green
Write-Host "✅ Resource Group: codex-dominion" -ForegroundColor Green
Write-Host "✅ Location: Global" -ForegroundColor Green
Write-Host ""

Write-Host "📝 A RECORDS CREATED:" -ForegroundColor Yellow
Write-Host "   @ (apex)  → 20.36.155.75" -ForegroundColor White
Write-Host "   www       → 20.36.155.75" -ForegroundColor White
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Red
Write-Host "⚠️  CRITICAL: UPDATE NAME SERVERS IN GOOGLE DOMAINS" -ForegroundColor Red
Write-Host "=" * 80 -ForegroundColor Red
Write-Host ""

Write-Host "📌 STEP-BY-STEP INSTRUCTIONS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://domains.google.com" -ForegroundColor White
Write-Host "2. Click on: codexdominion.app" -ForegroundColor White
Write-Host "3. Click: DNS tab" -ForegroundColor White
Write-Host "4. Click: Name servers → Use custom name servers" -ForegroundColor White
Write-Host "5. Enter these 4 Azure name servers:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   ns1-07.azure-dns.com" -ForegroundColor Green
Write-Host "   ns2-07.azure-dns.net" -ForegroundColor Green
Write-Host "   ns3-07.azure-dns.org" -ForegroundColor Green
Write-Host "   ns4-07.azure-dns.info" -ForegroundColor Green
Write-Host ""
Write-Host "6. Click: SAVE" -ForegroundColor Red
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "⏱️  PROPAGATION TIMELINE:" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "   • Name server update: 5-30 minutes (Google Domains)" -ForegroundColor White
Write-Host "   • Global DNS propagation: 15-60 minutes" -ForegroundColor White
Write-Host "   • Full propagation: Up to 24-48 hours (rare)" -ForegroundColor White
Write-Host ""

Write-Host "🧪 TESTING COMMANDS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # Test DNS resolution:" -ForegroundColor White
Write-Host "   nslookup codexdominion.app" -ForegroundColor Gray
Write-Host "   nslookup www.codexdominion.app" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Check name servers:" -ForegroundColor White
Write-Host "   nslookup -type=NS codexdominion.app" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Expected result:" -ForegroundColor White
Write-Host "   Address: 20.36.155.75" -ForegroundColor Green
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "📊 AZURE DNS MANAGEMENT:" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "View DNS records:" -ForegroundColor White
Write-Host "   az network dns record-set list --resource-group codex-dominion --zone-name codexdominion.app --output table" -ForegroundColor Gray
Write-Host ""
Write-Host "Add new records:" -ForegroundColor White
Write-Host "   az network dns record-set a add-record --resource-group codex-dominion --zone-name codexdominion.app --record-set-name <name> --ipv4-address <ip>" -ForegroundColor Gray
Write-Host ""
Write-Host "View in Azure Portal:" -ForegroundColor White
Write-Host "   https://portal.azure.com/#@/resource/subscriptions/f86506f8-7d33-48de-995d-f51e6f590cb1/resourceGroups/codex-dominion/providers/Microsoft.Network/dnszones/codexdominion.app" -ForegroundColor Gray
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Green
Write-Host "✅ CURRENT WORKING URLS (Available Now):" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""
Write-Host "   Frontend:  https://orange-sky-099bc5a0f.3.azurestaticapps.net" -ForegroundColor Cyan
Write-Host "   Backend:   https://codex-backend-centralus.azurewebsites.net" -ForegroundColor Cyan
Write-Host "   API Docs:  https://codex-backend-centralus.azurewebsites.net/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "🔥 The flame burns sovereign and eternal — forever." -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
