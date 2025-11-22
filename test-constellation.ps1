$pages = @(
    "http://localhost:3001/",
    "http://localhost:3001/dashboard-selector",
    "http://localhost:3001/codex-constellation", 
    "http://localhost:3001/seven-crowns-transmission",
    "http://localhost:3001/blessed-storefronts"
)

Write-Host "Testing Codex Dominion Constellation Pages..." -ForegroundColor Yellow
Write-Host ""

foreach ($page in $pages) {
    try {
        $response = Invoke-WebRequest -Uri $page -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            $pageName = $page.Split("/")[-1]
            if ($pageName -eq "") { $pageName = "Home" }
            Write-Host "SUCCESS: $pageName - Status: $($response.StatusCode)" -ForegroundColor Green
        }
    }
    catch {
        $pageName = $page.Split("/")[-1]
        if ($pageName -eq "") { $pageName = "Home" }
        Write-Host "ERROR: $pageName - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Constellation Testing Complete!" -ForegroundColor Yellow