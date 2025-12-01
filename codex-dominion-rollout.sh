#!/bin/bash
set -e

echo "⚔️ Codex Dominion First Rollout Ceremony Initiated ⚔️"

# Step 1: Apply manifests for orchestrator, codex-core, and engines
echo "Applying Codex Constellation manifests..."
kubectl apply -f k8s/apply-all.yaml -n codex

# Step 2: Start rollout for orchestrator
echo "Starting orchestrator rollout..."
kubectl argo rollouts get rollout orchestrator -n codex --watch

# Step 3: Start rollout for codex-core
echo "Starting codex-core rollout..."
kubectl argo rollouts get rollout codex-core -n codex --watch

# Step 4: Start rollout for engines (01–16)
for i in {01..16}; do
  rollout="engine$i"
  echo "Starting rollout for $rollout..."
  kubectl argo rollouts get rollout $rollout -n codex --watch
done

echo "✅ Codex Dominion Rollouts initiated — guardianship system now narrates and commands closures."
