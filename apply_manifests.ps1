# Automated manifest application script
# Validates standard resources with kubeval, skips custom resources, applies all manifests

$customKinds = @(
    'Charter',
    'OmegaCapsule',
    'InfinityArchive',
    'EternalCapsule',
    'Seal',
    'Ledger',
    'Hymn',
    'Decree'
)

foreach ($file in Get-ChildItem .\manifests\*.yaml) {
    $yaml = Get-Content $file.FullName -Raw
    $kindMatch = $yaml -match 'kind:\s*(\w+)' | Out-Null
    $kind = $Matches[1]
    if ($customKinds -contains $kind) {
        Write-Host "[SKIP kubeval] $($file.Name): Custom resource kind '$kind'"
        kubectl apply -f $file.FullName
    } else {
        .\kubeval.exe $file.FullName
        if ($LASTEXITCODE -eq 0) {
            kubectl apply -f $file.FullName
        } else {
            Write-Host "[FAIL kubeval] $($file.Name): Not applied due to validation error" -ForegroundColor Red
        }
    }
}
