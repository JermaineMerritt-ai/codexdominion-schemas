# PowerShell script to clean up unused pods and scale down non-critical deployments in a Kubernetes namespace

$Namespace = "codex"
Write-Host "🔍 Checking for unused pods in namespace: $Namespace..."

# Delete pods that are not running (Succeeded or Failed)
$unusedPods = kubectl get pods -n $Namespace --field-selector=status.phase!=Running --no-headers | ForEach-Object { $_.Split(' ')[0] }
foreach ($pod in $unusedPods) {
    if ($pod) {
        Write-Host "🗑 Deleting unused pod: $pod"
        kubectl delete pod $pod -n $Namespace
    }
}
Write-Host "✅ Unused pods removed."

# Scale down non-critical deployments
Write-Host "🔍 Scaling down non-critical deployments..."
$deployments = kubectl get deployments -n $Namespace --no-headers | ForEach-Object { $_.Split(' ')[0] }
foreach ($deploy in $deployments) {
    # Skip critical deployments (adjust names as needed)
    if ($deploy -like "*critical*") {
        Write-Host "⏩ Skipping critical deployment: $deploy"
    } else {
        Write-Host "📉 Scaling down deployment: $deploy to 1 replica"
        kubectl scale deployment $deploy --replicas=1 -n $Namespace
    }
}
Write-Host "✅ Scaling down completed."
