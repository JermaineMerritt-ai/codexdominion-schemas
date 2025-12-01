# PowerShell script for Kubernetes cluster automation
# ===========================
# CONFIGURATION
# ===========================
$Namespace = "codex"
$SlackWebhookUrl = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
$CpuThreshold = 80      # % CPU usage threshold
$MemThreshold = 80      # % Memory usage threshold
$NodePool = "default"  # Node pool name for scaling
$MaxNodes = 5           # Max nodes allowed
$MinNodes = 1           # Min nodes allowed

# ===========================
# FUNCTIONS
# ===========================
function Send-Slack {
    param([string]$Message)
    Invoke-RestMethod -Uri $SlackWebhookUrl -Method Post -ContentType 'application/json' -Body (@{text=$Message} | ConvertTo-Json)
}

function Check-Resources {
    Write-Host "🔍 Checking cluster resource usage..."
    $nodeStats = kubectl top nodes | Select-Object -Skip 1
    $cpuUsage = 0
    $memUsage = 0
    foreach ($line in $nodeStats) {
        $fields = $line -split '\s+'
        if ($fields.Length -ge 5) {
            $cpuUsage += [int]($fields[2] -replace '%','')
            $memUsage += [int]($fields[4] -replace '%','')
        }
    }
    Write-Host "Current CPU Usage: $cpuUsage%"
    Write-Host "Current Memory Usage: $memUsage%"
    return @{CPU=$cpuUsage; MEM=$memUsage}
}

function Delete-UnusedPods {
    Write-Host "🗑 Deleting unused pods..."
    $unusedPods = kubectl get pods -n $Namespace --field-selector=status.phase!=Running --no-headers | ForEach-Object { $_.Split(' ')[0] }
    foreach ($pod in $unusedPods) {
        if ($pod) {
            Write-Host "Deleting pod: $pod"
            kubectl delete pod $pod -n $Namespace
        }
    }
}

function Scale-DownDeployments {
    Write-Host "📉 Scaling down non-critical deployments..."
    $deployments = kubectl get deployments -n $Namespace --no-headers | ForEach-Object { $_.Split(' ')[0] }
    foreach ($deploy in $deployments) {
        if ($deploy -like "*critical*") {
            Write-Host "⏩ Skipping critical deployment: $deploy"
        } else {
            Write-Host "Scaling down $deploy to 1 replica"
            kubectl scale deployment $deploy --replicas=1 -n $Namespace
        }
    }
}

function Auto-ScaleCluster {
    Write-Host "⚠️ Checking if cluster needs scaling..."
    $nodeCount = (kubectl get nodes --no-headers | Measure-Object).Count
    if ($nodeCount -lt $MaxNodes) {
        Write-Host "Scaling cluster up by 1 node..."
        # Placeholder for actual cloud CLI scaling command
        # Example for Azure AKS:
        # az aks scale --resource-group YOUR_RESOURCE_GROUP --name YOUR_AKS_CLUSTER --node-count ($nodeCount+1)
        Send-Slack "Cluster scaled up to $($nodeCount+1) nodes due to high resource usage."
    } else {
        Write-Host "Cluster already at max nodes."
    }
}

# ===========================
# MAIN LOGIC
# ===========================
$usage = Check-Resources
Delete-UnusedPods
Scale-DownDeployments

if (($usage.CPU -gt $CpuThreshold) -or ($usage.MEM -gt $MemThreshold)) {
    Send-Slack "⚠️ High resource usage detected! CPU: $($usage.CPU)%, Memory: $($usage.MEM)%. Initiating autoscale..."
    Auto-ScaleCluster
} else {
    Send-Slack "✅ Cluster resources are healthy. No scaling needed."
}

Write-Host "✅ Automation complete."
