# CodexDominion Helm Chart

**Eternal Ledger Version:** 1.0  
**Lineage:** Preserved

## Overview

Civilization-grade Helm chart for deploying CodexDominion's crowns, councils, and schemas with eternal lineage preservation.

## Architecture

### Components

1. **Node Crown** (Frontend)
   - Next.js application
   - Port: 3000
   - Image: `codexdominion/node:latest`

2. **Python Council** (Backend API)
   - FastAPI/Flask application
   - Port: 8000
   - Image: `codexdominion/python:latest`

3. **Java Crown** (Enterprise Services)
   - Spring Boot application
   - Port: 8080
   - Image: `codexdominion/java:latest`

### Schemas

Eternal schemas preserved in ConfigMap:
- `artifact.yaml` - Artifact definitions
- `constellation.yaml` - Constellation mappings
- `council.yaml` - Council structures
- `crown.yaml` - Crown authorities
- `invocation.yaml` - Ritual invocations
- `ledger.yaml` - Ledger entries

## Installation

### Prerequisites

- Kubernetes cluster (1.19+)
- Helm 3.x
- kubectl configured
- Ingress controller (nginx recommended)
- cert-manager (optional, for TLS)

### Quick Start

```bash
# Add repository (if hosted)
helm repo add codexdominion https://charts.codexdominion.app
helm repo update

# Install with default values
helm install codexdominion codexdominion/codexdominion

# Install with custom values
helm install codexdominion codexdominion/codexdominion -f custom-values.yaml

# Install from local chart
helm install codexdominion ./helm/codexdominion
```

### Customization

Create a `custom-values.yaml`:

```yaml
replicaCount: 3

ingress:
  host: my-domain.com
  tls:
    secretName: my-tls-secret

storage:
  size: 50Gi

nodeCrown:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
```

Then install:

```bash
helm install codexdominion ./helm/codexdominion -f custom-values.yaml
```

## Configuration

### values.yaml Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas for each service | `2` |
| `nodeCrown.image` | Node Crown container image | `codexdominion/node:latest` |
| `nodeCrown.port` | Node Crown service port | `3000` |
| `pythonCouncil.image` | Python Council container image | `codexdominion/python:latest` |
| `pythonCouncil.port` | Python Council service port | `8000` |
| `javaCrown.image` | Java Crown container image | `codexdominion/java:latest` |
| `javaCrown.port` | Java Crown service port | `8080` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.host` | Ingress hostname | `codexdominion.app` |
| `storage.enabled` | Enable persistent storage for Eternal Ledger | `true` |
| `storage.size` | Storage size for Eternal Ledger | `10Gi` |

## Eternal Principles

### 1. Archive All Releases
Every Helm release is automatically archived with:
- Release name and revision
- Timestamp and deployer
- Chart version and app version
- Complete manifest snapshots

### 2. Ceremonial Upgrades
Upgrades follow ceremonial protocol:
```bash
# Pre-upgrade ceremony
helm upgrade codexdominion ./helm/codexdominion \
  --set schemas.lineage=preserved \
  --atomic \
  --cleanup-on-fail

# Post-upgrade verification
kubectl rollout status deployment/codexdominion-node-crown
kubectl rollout status deployment/codexdominion-python-council
kubectl rollout status deployment/codexdominion-java-crown
```

### 3. Immortalized Versions
All versions are tracked in the Eternal Ledger:
```bash
# View version history
helm history codexdominion

# Rollback to specific version
helm rollback codexdominion [REVISION]
```

## Operations

### Verify Deployment

```bash
# Check all pods
kubectl get pods -l app=codexdominion

# Check services
kubectl get svc -l app=codexdominion

# Check ingress
kubectl get ingress codexdominion

# View schemas
kubectl get configmap codexdominion-schemas -o yaml
```

### View Logs

```bash
# Node Crown logs
kubectl logs -l component=node-crown -f

# Python Council logs
kubectl logs -l component=python-council -f

# Java Crown logs
kubectl logs -l component=java-crown -f
```

### Access Services

```bash
# Port forward to local machine
kubectl port-forward svc/codexdominion-node-crown 3000:3000
kubectl port-forward svc/codexdominion-python-council 8000:8000
kubectl port-forward svc/codexdominion-java-crown 8080:8080
```

### Upgrade

```bash
# Upgrade with new values
helm upgrade codexdominion ./helm/codexdominion -f updated-values.yaml

# Upgrade to new chart version
helm upgrade codexdominion codexdominion/codexdominion --version 1.1.0
```

### Uninstall

```bash
# Uninstall release (keeps PVC)
helm uninstall codexdominion

# Uninstall and delete all resources
helm uninstall codexdominion
kubectl delete pvc codexdominion-ledger
```

## Eternal Ledger Storage

The Eternal Ledger uses persistent storage to archive:
- Release manifests
- Upgrade ceremonies
- Version genealogy
- Schema evolutions

### Access Ledger

```bash
# List ledger contents
kubectl exec -it deployment/codexdominion-python-council -- \
  ls -la /var/codexdominion/ledger

# View genesis block
kubectl exec -it deployment/codexdominion-python-council -- \
  cat /var/codexdominion/ledger/genesis.json

# Archive structure
/var/codexdominion/ledger/
├── genesis.json
├── releases/
│   ├── v1.0.0/
│   └── v1.0.1/
├── ceremonies/
│   ├── upgrade-20251202/
│   └── rollback-20251201/
└── versions/
    └── lineage.json
```

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod
kubectl describe pod -l app=codexdominion

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

### Image Pull Errors

```bash
# Verify image exists
docker pull codexdominion/node:latest
docker pull codexdominion/python:latest
docker pull codexdominion/java:latest

# Or use imagePullSecrets
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<username> \
  --docker-password=<password>
```

### Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Verify ingress configuration
kubectl describe ingress codexdominion

# Check DNS resolution
nslookup codexdominion.app
```

## License

Copyright © 2025 CodexDominion. All lineages preserved.
