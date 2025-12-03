# CodexDominion Helm Chart - Quick Reference

## 🚀 Quick Start

### Prerequisites
```bash
# Install Helm 3.x
# Windows (Chocolatey)
choco install kubernetes-helm

# macOS (Homebrew)
brew install helm

# Linux (Snap)
snap install helm --classic
```

### Install Chart
```bash
# From local directory
cd helm
helm install codexdominion ./codexdominion --namespace codexdominion --create-namespace

# Or use deployment script (PowerShell)
.\deploy.ps1

# Or use deployment script (Bash)
chmod +x deploy.sh
./deploy.sh
```

## 📋 Common Commands

### Installation
```bash
# Standard install
helm install codexdominion ./codexdominion -n codexdominion --create-namespace

# Install with custom values
helm install codexdominion ./codexdominion -f custom-values.yaml -n codexdominion

# Dry run (test without installing)
helm install codexdominion ./codexdominion -n codexdominion --dry-run --debug
```

### Upgrade
```bash
# Upgrade existing release
helm upgrade codexdominion ./codexdominion -n codexdominion

# Upgrade or install (idempotent)
helm upgrade --install codexdominion ./codexdominion -n codexdominion

# Upgrade with new values
helm upgrade codexdominion ./codexdominion -f updated-values.yaml -n codexdominion
```

### Status & Info
```bash
# List all releases
helm list -n codexdominion

# Show release status
helm status codexdominion -n codexdominion

# Get release values
helm get values codexdominion -n codexdominion

# Get full manifest
helm get manifest codexdominion -n codexdominion

# Show release history
helm history codexdominion -n codexdominion
```

### Rollback
```bash
# Rollback to previous version
helm rollback codexdominion -n codexdominion

# Rollback to specific revision
helm rollback codexdominion 3 -n codexdominion
```

### Uninstall
```bash
# Uninstall release
helm uninstall codexdominion -n codexdominion

# Delete eternal ledger storage (optional)
kubectl delete pvc codexdominion-ledger -n codexdominion
```

## 🔧 Configuration Examples

### Custom Replica Count
```yaml
# custom-values.yaml
replicaCount: 5
```

```bash
helm install codexdominion ./codexdominion -f custom-values.yaml -n codexdominion
```

### Custom Domain
```yaml
# custom-values.yaml
ingress:
  host: my-domain.com
  tls:
    secretName: my-tls-cert
```

### Increase Resources
```yaml
# custom-values.yaml
nodeCrown:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

pythonCouncil:
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi
```

### Larger Eternal Ledger Storage
```yaml
# custom-values.yaml
storage:
  size: 100Gi
  className: fast-ssd
```

### Use Different Images
```yaml
# custom-values.yaml
nodeCrown:
  image: myregistry.com/codexdominion/node:v2.0.0

pythonCouncil:
  image: myregistry.com/codexdominion/python:v2.0.0

javaCrown:
  image: myregistry.com/codexdominion/java:v2.0.0
```

## 🔍 Debugging

### Check Pods
```bash
# List all pods
kubectl get pods -n codexdominion -l app=codexdominion

# Describe pod (see events)
kubectl describe pod -n codexdominion <pod-name>

# View pod logs
kubectl logs -n codexdominion -l component=node-crown -f
kubectl logs -n codexdominion -l component=python-council -f
kubectl logs -n codexdominion -l component=java-crown -f

# Execute into pod
kubectl exec -it -n codexdominion <pod-name> -- /bin/bash
```

### Check Services
```bash
# List services
kubectl get svc -n codexdominion -l app=codexdominion

# Describe service
kubectl describe svc -n codexdominion codexdominion-node-crown
```

### Check Ingress
```bash
# Get ingress details
kubectl get ingress -n codexdominion codexdominion

# Describe ingress
kubectl describe ingress -n codexdominion codexdominion

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller -f
```

### Check ConfigMap
```bash
# View schemas configmap
kubectl get configmap -n codexdominion codexdominion-schemas -o yaml

# Get specific schema
kubectl get configmap -n codexdominion codexdominion-schemas -o jsonpath='{.data.artifact\.yaml}'
```

### Check Storage
```bash
# List PVCs
kubectl get pvc -n codexdominion

# Describe PVC
kubectl describe pvc -n codexdominion codexdominion-ledger

# Check ledger contents
kubectl exec -it -n codexdominion deployment/codexdominion-python-council -- \
  ls -la /var/codexdominion/ledger
```

## 🌐 Port Forwarding

### Access Services Locally
```bash
# Node Crown (Frontend) - http://localhost:3000
kubectl port-forward -n codexdominion svc/codexdominion-node-crown 3000:3000

# Python Council (API) - http://localhost:8000
kubectl port-forward -n codexdominion svc/codexdominion-python-council 8000:8000

# Java Crown (Enterprise) - http://localhost:8080
kubectl port-forward -n codexdominion svc/codexdominion-java-crown 8080:8080
```

## 🔐 Secrets Management

### Create Image Pull Secret
```bash
kubectl create secret docker-registry regcred \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password> \
  --namespace codexdominion
```

### Add to values.yaml
```yaml
imagePullSecrets:
  - name: regcred
```

### Create TLS Secret
```bash
kubectl create secret tls codexdominion-tls \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem \
  --namespace codexdominion
```

## 📊 Monitoring

### Check Deployment Status
```bash
# Watch pods
kubectl get pods -n codexdominion -l app=codexdominion -w

# Check deployment rollout
kubectl rollout status deployment/codexdominion-node-crown -n codexdominion
kubectl rollout status deployment/codexdominion-python-council -n codexdominion
kubectl rollout status deployment/codexdominion-java-crown -n codexdominion
```

### Resource Usage
```bash
# Pod resource usage
kubectl top pods -n codexdominion

# Node resource usage
kubectl top nodes
```

## 🔄 Upgrade Strategies

### Zero-Downtime Upgrade
```bash
# Ensure readiness probes are configured
# Upgrade with increased timeout
helm upgrade codexdominion ./codexdominion \
  --namespace codexdominion \
  --timeout 10m \
  --wait \
  --atomic
```

### Blue-Green Deployment
```bash
# Install new version with different name
helm install codexdominion-v2 ./codexdominion \
  --namespace codexdominion \
  -f new-version-values.yaml

# Switch traffic in ingress, then remove old
helm uninstall codexdominion -n codexdominion
```

## 📦 Packaging & Distribution

### Package Chart
```bash
# Create chart archive
helm package codexdominion

# Creates: codexdominion-1.0.0.tgz
```

### Create Chart Repository
```bash
# Generate index
helm repo index . --url https://charts.codexdominion.app

# Upload to chart repository
# Upload *.tgz and index.yaml to web server
```

### Use Remote Chart
```bash
# Add repository
helm repo add codexdominion https://charts.codexdominion.app

# Update repositories
helm repo update

# Install from repository
helm install codexdominion codexdominion/codexdominion -n codexdominion
```

## 🎯 Best Practices

1. **Always use version pinning**
   ```yaml
   nodeCrown:
     image: codexdominion/node:1.0.0  # Not 'latest'
   ```

2. **Use resource limits**
   ```yaml
   resources:
     limits:
       cpu: 500m
       memory: 512Mi
   ```

3. **Enable health checks**
   - Charts already include liveness/readiness probes
   - Ensure your apps respond to `/health` and `/ready` endpoints

4. **Use atomic upgrades**
   ```bash
   helm upgrade --atomic --cleanup-on-fail
   ```

5. **Always backup before upgrade**
   ```bash
   # Export current values
   helm get values codexdominion -n codexdominion > backup-values.yaml
   
   # Backup eternal ledger
   kubectl cp codexdominion/<pod-name>:/var/codexdominion/ledger ./ledger-backup
   ```

## 🆘 Emergency Procedures

### Rollback Failed Upgrade
```bash
helm rollback codexdominion -n codexdominion
```

### Force Delete Stuck Resources
```bash
kubectl delete pod <pod-name> -n codexdominion --grace-period=0 --force
```

### Restart All Deployments
```bash
kubectl rollout restart deployment/codexdominion-node-crown -n codexdominion
kubectl rollout restart deployment/codexdominion-python-council -n codexdominion
kubectl rollout restart deployment/codexdominion-java-crown -n codexdominion
```

## 📚 Additional Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [CodexDominion Full README](./codexdominion/README.md)

---

**Eternal Ledger Version:** 1.0  
**Lineage:** Preserved ✨
