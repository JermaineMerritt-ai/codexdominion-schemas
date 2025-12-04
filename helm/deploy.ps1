#!/usr/bin/env pwsh
# CodexDominion Helm Chart Deployment Script
# Eternal Ledger Version: 1.0

param(
    [Parameter(Mandatory=$false)]
    [string]$Namespace = "codexdominion",

    [Parameter(Mandatory=$false)]
    [string]$ReleaseName = "codexdominion",

    [Parameter(Mandatory=$false)]
    [string]$ValuesFile = "",

    [Parameter(Mandatory=$false)]
    [switch]$DryRun,

    [Parameter(Mandatory=$false)]
    [switch]$Upgrade,

    [Parameter(Mandatory=$false)]
    [switch]$Uninstall,

    [Parameter(Mandatory=$false)]
    [switch]$Validate,

    [Parameter(Mandatory=$false)]
    [switch]$WithLedger  # Enable Eternal Ledger logging
)

$ChartPath = Join-Path $PSScriptRoot "codexdominion"
$LedgerScript = Join-Path $PSScriptRoot "scripts\eternal-ledger.ps1"
$ErrorActionPreference = "Stop"

Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║              CODEXDOMINION HELM DEPLOYMENT                     ║
║                 Eternal Ledger Version 1.0                     ║
║                    Lineage: Preserved                          ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check if Helm is installed
Write-Host "`n🔍 Checking prerequisites..." -ForegroundColor Yellow
try {
    $helmVersion = helm version --short
    Write-Host "✓ Helm installed: $helmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Helm is not installed. Please install Helm 3.x" -ForegroundColor Red
    exit 1
}

# Check if kubectl is installed
try {
    $kubectlVersion = kubectl version --client -o json | ConvertFrom-Json
    Write-Host "✓ kubectl installed" -ForegroundColor Green
} catch {
    Write-Host "✗ kubectl is not installed" -ForegroundColor Red
    exit 1
}

# Validate chart
if ($Validate -or $true) {
    Write-Host "`n📋 Validating Helm chart..." -ForegroundColor Yellow
    try {
        helm lint $ChartPath
        Write-Host "✓ Chart validation passed" -ForegroundColor Green
    } catch {
        Write-Host "✗ Chart validation failed" -ForegroundColor Red
        exit 1
    }
}

# Uninstall if requested
if ($Uninstall) {
    Write-Host "`n🗑️  Uninstalling release: $ReleaseName" -ForegroundColor Yellow

    if ($WithLedger -and (Test-Path $LedgerScript)) {
        Write-Host "📜 Using Eternal Ledger logging..." -ForegroundColor Cyan
        & $LedgerScript uninstall $ReleaseName $Namespace
    } else {
        helm uninstall $ReleaseName --namespace $Namespace --keep-history
    }

    Write-Host "✓ Release uninstalled" -ForegroundColor Green

    Write-Host "`n⚠️  Note: PersistentVolumeClaim '$ReleaseName-ledger' not deleted" -ForegroundColor Yellow
    Write-Host "   To delete eternal ledger storage, run:" -ForegroundColor Yellow
    Write-Host "   kubectl delete pvc $ReleaseName-ledger -n $Namespace" -ForegroundColor Cyan
    exit 0
}

# Create namespace if it doesn't exist
Write-Host "`n🏗️  Ensuring namespace exists..." -ForegroundColor Yellow
kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✓ Namespace ready: $Namespace" -ForegroundColor Green

# Build helm command
$helmCmd = if ($Upgrade) { "upgrade --install" } else { "install" }
$helmArgs = @(
    $helmCmd,
    $ReleaseName,
    $ChartPath,
    "--namespace", $Namespace,
    "--create-namespace"
)

if ($ValuesFile -and (Test-Path $ValuesFile)) {
    $helmArgs += @("--values", $ValuesFile)
    Write-Host "✓ Using custom values: $ValuesFile" -ForegroundColor Green
}

if ($DryRun) {
    $helmArgs += "--dry-run"
    Write-Host "`n🧪 Running dry-run (no changes will be made)..." -ForegroundColor Yellow
}

# Deploy
Write-Host "`n🚀 Deploying CodexDominion..." -ForegroundColor Yellow
Write-Host "   Command: helm $($helmArgs -join ' ')" -ForegroundColor Gray

try {
    if ($WithLedger -and (Test-Path $LedgerScript)) {
        # Use Eternal Ledger wrapper
        Write-Host "📜 Using Eternal Ledger logging..." -ForegroundColor Cyan
        if ($Upgrade) {
            & $LedgerScript upgrade $ReleaseName $ChartPath $Namespace $(if ($ValuesFile) { "-f", $ValuesFile })
        } else {
            & $LedgerScript install $ReleaseName $ChartPath $Namespace $(if ($ValuesFile) { "-f", $ValuesFile })
        }
    } else {
        # Standard Helm deployment
        $output = & helm $helmArgs 2>&1
        Write-Host $output
    }
    Write-Host "`n✓ Deployment successful!" -ForegroundColor Green
} catch {
    Write-Host "`n✗ Deployment failed: $_" -ForegroundColor Red
    exit 1
}

if (-not $DryRun) {
    # Wait for deployments
    Write-Host "`n⏳ Waiting for deployments to be ready..." -ForegroundColor Yellow

    $deployments = @(
        "$ReleaseName-node-crown",
        "$ReleaseName-python-council",
        "$ReleaseName-java-crown"
    )

    foreach ($deployment in $deployments) {
        Write-Host "   Waiting for $deployment..." -ForegroundColor Gray
        kubectl rollout status deployment/$deployment -n $Namespace --timeout=300s
    }

    Write-Host "`n✓ All deployments ready!" -ForegroundColor Green

    # Show status
    Write-Host "`n📊 Deployment Status:" -ForegroundColor Cyan
    kubectl get pods -n $Namespace -l app=$ReleaseName

    Write-Host "`n🌐 Services:" -ForegroundColor Cyan
    kubectl get svc -n $Namespace -l app=$ReleaseName

    Write-Host "`n🔗 Ingress:" -ForegroundColor Cyan
    kubectl get ingress -n $Namespace $ReleaseName

    # Show access instructions
    Write-Host @"

╔════════════════════════════════════════════════════════════════╗
║                   DEPLOYMENT COMPLETE                          ║
╚════════════════════════════════════════════════════════════════╝

📜 View release info:
   helm list -n $Namespace
   helm status $ReleaseName -n $Namespace

📋 View schemas:
   kubectl get configmap $ReleaseName-schemas -n $Namespace -o yaml

🔍 View logs:
   kubectl logs -l component=node-crown -n $Namespace -f
   kubectl logs -l component=python-council -n $Namespace -f
   kubectl logs -l component=java-crown -n $Namespace -f

🌐 Access services locally:
   kubectl port-forward -n $Namespace svc/$ReleaseName-node-crown 3000:3000
   kubectl port-forward -n $Namespace svc/$ReleaseName-python-council 8000:8000
   kubectl port-forward -n $Namespace svc/$ReleaseName-java-crown 8080:8080

💾 Check Eternal Ledger:
   kubectl exec -it -n $Namespace deployment/$ReleaseName-python-council -- ls -la /var/codexdominion/ledger

═══════════════════════════════════════════════════════════════
"@ -ForegroundColor White
}

Write-Host "✨ Eternal Principles Enforced ✨`n" -ForegroundColor Magenta
