# Codex Dominion First Rollout Ceremony (PowerShell)
$ErrorActionPreference = 'Stop'

Write-Host "⚔️ Codex Dominion First Rollout Ceremony Initiated ⚔️"

# Step 1: Apply manifests for orchestrator, codex-core, and engines
Write-Host "Applying Codex Constellation manifests..."
kubectl apply -f k8s/apply-all.yaml -n codex

# Step 2: Start rollout for orchestrator
Write-Host "Starting orchestrator rollout..."
kubectl argo rollouts get rollout orchestrator -n codex --watch

# Step 3: Start rollout for codex-core
Write-Host "Starting codex-core rollout..."
kubectl argo rollouts get rollout codex-core -n codex --watch

# Step 4: Start rollout for engines (01–16)
For ($i = 1; $i -le 16; $i++) {
    $engine = "engine" + $i.ToString("D2")
    Write-Host "Starting rollout for $engine..."
    kubectl argo rollouts get rollout $engine -n codex --watch
}

Write-Host "✅ Codex Dominion Rollouts initiated — guardianship system now narrates and commands closures."
