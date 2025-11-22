#!/bin/bash
set -e

echo "🔥 Codex Dominion Go-Live Ceremony Initiated 🔥"

# Step 1: Install Argo Rollouts
echo "Installing Argo Rollouts..."
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace codex || true
helm upgrade --install argo-rollouts argo/argo-rollouts -n codex

# Step 2: Install Prometheus
echo "Installing Prometheus..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring || true
helm upgrade --install prometheus prometheus-community/prometheus -n monitoring

# Step 3: Install Grafana
echo "Installing Grafana..."
helm upgrade --install grafana prometheus-community/grafana -n monitoring

# Step 4: Apply Alertmanager Config
echo "Applying Alertmanager ceremonial routes..."
kubectl apply -f alertmanager/config.yaml -n monitoring

# Step 5: Apply ServiceMonitors + Dashboard
echo "Applying ServiceMonitors and Codex Dominion Dashboard..."
kubectl apply -f k8s/monitoring.yaml -n monitoring
kubectl apply -f grafana/codex-dominion-dashboard.json -n monitoring

echo "✅ Codex Dominion Guardianship System is now live!"
echo "GitHub dispatches → GKE vessels → Argo guides → Prometheus watches → Grafana mirrors → Alertmanager heralds → Twilio speaks → Copilot narrates → Super Action AI commands."
