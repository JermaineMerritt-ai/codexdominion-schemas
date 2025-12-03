# 📋 Helm Release Checklist - CodexDominion

**Eternal Principles:** Archive · Lineage · Ceremonial Closure

---

## 🏷️ Version Control

- [ ] Tag releases consistently (e.g., `1.1.0` → `1.1.1`)
- [ ] Never skip versions; maintain sequential lineage
- [ ] Update `Chart.yaml` version and appVersion
- [ ] Document breaking changes in `Chart.yaml` annotations
- [ ] Update `CHANGELOG.md` with release notes

**Commands:**
```bash
# Update Chart.yaml
sed -i 's/version: 1.0.0/version: 1.1.0/' Chart.yaml
sed -i 's/appVersion: "1.0"/appVersion: "1.1"/' Chart.yaml

# Git tag
git tag -a v1.1.0 -m "Release 1.1.0: Added release checklist governance"
git push origin v1.1.0
```

---

## 📜 Lineage Preservation

- [ ] Archive lineage: Log `helm install/upgrade/rollback`
- [ ] Roll forward/back safely; never delete lineage
- [ ] Store revision history with `--history-max=10`
- [ ] Keep audit log of all deployments

**Commands:**
```bash
# View revision history
helm history codexdominion -n codexdominion

# Upgrade with history preservation
helm upgrade codexdominion ./codexdominion \
  -n codexdominion \
  -f values.yaml \
  --history-max=10 \
  --description "Upgraded to v1.1.0: Added governance checklist"

# Export lineage to file
helm history codexdominion -n codexdominion -o json > releases/lineage-$(date +%Y%m%d).json
```

---

## 🚦 Promotion Gates

- [ ] Gate promotions with readiness/liveness probes
- [ ] Promote `dev` → `staging` → `prod` with signed closures
- [ ] Require approval for production deployments
- [ ] Verify smoke tests pass before promotion
- [ ] Load test staging environment before prod

**Workflow:**
```bash
# Deploy to dev
helm upgrade codexdominion ./codexdominion -n codexdominion-dev -f values-dev.yaml

# Run smoke tests
kubectl run smoke-test --image=curlimages/curl -n codexdominion-dev --rm -it -- \
  curl http://codexdominion-node-crown/health

# Promote to staging (requires approval)
helm upgrade codexdominion ./codexdominion -n codexdominion-staging -f values-staging.yaml

# Production deployment (signed release)
helm upgrade codexdominion ./codexdominion -n codexdominion-prod -f values-prod.yaml \
  --verify \
  --wait \
  --timeout 10m
```

---

## 🔒 Security & RBAC

- [ ] Enforce image signing and RBAC least privilege
- [ ] Use sealed secrets or vault for sensitive data
- [ ] Scan images for CVEs before deployment
- [ ] Apply pod security standards (restricted/baseline)
- [ ] Never store secrets in `values.yaml` or Git
- [ ] Rotate secrets quarterly
- [ ] Enable network policies for pod isolation

**Commands:**
```bash
# Scan images for vulnerabilities
trivy image codexdominion/node:1.0.0
trivy image codexdominion/python:1.0.0
trivy image codexdominion/java:1.0.0

# Create sealed secret
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secure123 \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

# Apply pod security standard
kubectl label namespace codexdominion pod-security.kubernetes.io/enforce=restricted
```

---

## 💾 State Management

- [ ] Preserve state with PersistentVolumes and backups
- [ ] Use volumeSnapshots before major upgrades
- [ ] Test restore procedures quarterly
- [ ] Mount eternal-ledger PVC to preserve genesis block
- [ ] Document backup/restore procedures

**Commands:**
```bash
# Create volume snapshot before upgrade
kubectl create -f - <<EOF
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: eternal-ledger-snapshot-$(date +%Y%m%d)
  namespace: codexdominion
spec:
  source:
    persistentVolumeClaimName: codexdominion-ledger
EOF

# List snapshots
kubectl get volumesnapshot -n codexdominion

# Restore from snapshot (if needed)
# Update PVC to use snapshot as dataSource
```

---

## 🎯 Rollout Strategy

- [ ] Canary rollouts: `maxUnavailable=0`, `maxSurge=1`
- [ ] Use progressive delivery (10% → 50% → 100%)
- [ ] Monitor error rates during rollout
- [ ] Automatic rollback on failure thresholds
- [ ] Blue-green deployments for zero-downtime

**Deployment Strategy:**
```yaml
# In deployment.yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

**Progressive Rollout:**
```bash
# Deploy canary (10%)
helm upgrade codexdominion ./codexdominion -n codexdominion \
  --set replicaCount=10 \
  --set canary.enabled=true \
  --set canary.weight=10

# Monitor metrics for 15 minutes
# If success, promote to 50%
helm upgrade codexdominion ./codexdominion -n codexdominion \
  --set canary.weight=50

# Full rollout
helm upgrade codexdominion ./codexdominion -n codexdominion \
  --set canary.enabled=false
```

---

## ✅ Pre-Deployment Validation

- [ ] Run: `helm lint ./codexdominion`
- [ ] Run: `helm template codexdominion ./codexdominion --debug`
- [ ] Run: `helm diff upgrade codexdominion ./codexdominion -f values.yaml`
- [ ] Verify resource quotas and limits
- [ ] Check cluster capacity before scaling
- [ ] Test dry-run deployment

**Validation Commands:**
```bash
# Lint chart
helm lint ./codexdominion

# Template and debug
helm template codexdominion ./codexdominion \
  -f values.yaml \
  --debug \
  --validate

# Diff with current deployment (requires helm-diff plugin)
helm plugin install https://github.com/databus23/helm-diff
helm diff upgrade codexdominion ./codexdominion -n codexdominion -f values.yaml

# Dry-run
helm upgrade codexdominion ./codexdominion \
  -n codexdominion \
  -f values.yaml \
  --dry-run \
  --debug

# Check cluster resources
kubectl describe nodes | grep -A 5 "Allocated resources"
kubectl top nodes
```

---

## 🔍 Post-Deployment Verification

- [ ] `kubectl get pods -n codexdominion -l app=codexdominion`
- [ ] `kubectl get svc,ingress -n codexdominion`
- [ ] `kubectl get pvc -n codexdominion`
- [ ] Verify all pods reach Running state (1/1 READY)
- [ ] Test ingress endpoints return 200 OK
- [ ] Verify eternal-ledger PVC is Bound
- [ ] Check logs for errors

**Verification Commands:**
```bash
# Check all resources
kubectl get all,pvc,configmap,ingress -n codexdominion -l app=codexdominion

# Verify pod health
kubectl get pods -n codexdominion -l app=codexdominion
kubectl describe pods -n codexdominion -l app=codexdominion

# Test endpoints
curl -I https://codexdominion.app/
curl -I https://codexdominion.app/api/health
curl -I https://codexdominion.app/enterprise/actuator/health

# Verify PVC
kubectl get pvc codexdominion-ledger -n codexdominion
kubectl describe pvc codexdominion-ledger -n codexdominion

# Check logs
kubectl logs -l component=node-crown -n codexdominion --tail=50
kubectl logs -l component=python-council -n codexdominion --tail=50
kubectl logs -l component=java-crown -n codexdominion --tail=50

# Events
kubectl get events -n codexdominion --sort-by='.lastTimestamp' | tail -20
```

---

## ⏮️ Rollback Procedure

- [ ] `helm history codexdominion -n codexdominion`
- [ ] `helm rollback codexdominion [REVISION] -n codexdominion`
- [ ] Verify pods restart successfully
- [ ] Test application functionality post-rollback
- [ ] Document rollback reason

**Rollback Commands:**
```bash
# View revision history
helm history codexdominion -n codexdominion

# Rollback to previous version
helm rollback codexdominion -n codexdominion

# Rollback to specific revision
helm rollback codexdominion 3 -n codexdominion --wait --timeout 5m

# Verify rollback
kubectl get pods -n codexdominion -w
helm status codexdominion -n codexdominion

# Test application
curl https://codexdominion.app/health
```

---

## 📊 Monitoring & Observability

- [ ] Enable tracing for all microservices
- [ ] Configure Prometheus metrics scraping
- [ ] Set up alerting for pod restarts, OOMKilled
- [ ] Dashboard: grafana.codexdominion.app
- [ ] Configure logging aggregation (ELK/Loki)

**Monitoring Setup:**
```bash
# Install Prometheus & Grafana (if not present)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --create-namespace

# Add ServiceMonitor for CodexDominion
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: codexdominion
  namespace: codexdominion
spec:
  selector:
    matchLabels:
      app: codexdominion
  endpoints:
  - port: http
    path: /metrics
EOF

# View metrics
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
# Open http://localhost:9090

# View Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open http://localhost:3000 (admin/prom-operator)
```

---

## 📝 Documentation

- [ ] Update `CHANGELOG.md` with release notes
- [ ] Document configuration changes in `README.md`
- [ ] Tag Git commit: `git tag -a v1.1.0 -m "Release 1.1.0"`
- [ ] Push artifacts to Helm repository
- [ ] Update architecture diagrams if needed
- [ ] Notify stakeholders of release

**Release Process:**
```bash
# Update CHANGELOG.md
cat >> CHANGELOG.md <<EOF
## [1.1.0] - $(date +%Y-%m-%d)

### Added
- Helm release checklist ConfigMap for governance
- Release management best practices documentation

### Changed
- Updated deployment strategy to use maxUnavailable=0

### Fixed
- None

EOF

# Commit and tag
git add .
git commit -m "Release 1.1.0: Added governance checklist"
git tag -a v1.1.0 -m "Release 1.1.0: Governance and release management"
git push origin main --tags

# Package Helm chart
helm package ./codexdominion

# Push to Helm repository (if using ChartMuseum/Harbor)
curl --data-binary "@codexdominion-1.1.0.tgz" http://chartmuseum.codexdominion.app/api/charts
```

---

## 🎭 Ceremonial Closure

Upon completion of all checklist items:

```bash
# Generate closure certificate
cat > releases/CLOSURE_CERTIFICATE_v1.1.0.txt <<EOF
═══════════════════════════════════════════════════════════════
          HELM RELEASE CEREMONIAL CLOSURE CERTIFICATE
═══════════════════════════════════════════════════════════════

Chart Name:     CodexDominion
Chart Version:  1.1.0
App Version:    1.1
Release Date:   $(date +"%B %d, %Y at %H:%M:%S %Z")
Namespace:      codexdominion
Revision:       $(helm list -n codexdominion -o json | jq -r '.[0].revision')

───────────────────────────────────────────────────────────────
VALIDATION STATUS
───────────────────────────────────────────────────────────────

✓ Version Control:        VERIFIED
✓ Lineage Preservation:   ARCHIVED
✓ Promotion Gates:        PASSED
✓ Security & RBAC:        ENFORCED
✓ State Management:       BACKED UP
✓ Rollout Strategy:       CONFIGURED
✓ Pre-Deployment:         VALIDATED
✓ Post-Deployment:        VERIFIED
✓ Monitoring:             ACTIVE
✓ Documentation:          COMPLETE

───────────────────────────────────────────────────────────────
RESOURCES DEPLOYED
───────────────────────────────────────────────────────────────

Deployments:   3 (Node Crown, Python Council, Java Crown)
Services:      3 (ClusterIP)
Ingress:       1 (codexdominion.app)
ConfigMaps:    3 (schemas, ledger-config, release-checklist)
PVC:           1 (eternal-ledger: 10Gi, Bound)
Pods:          3/3 Running

───────────────────────────────────────────────────────────────
ETERNAL PRINCIPLES
───────────────────────────────────────────────────────────────

Archive:     All manifests preserved in cluster and Git
Lineage:     Revision history maintained (max 10)
Closure:     This release is ceremonially sealed and complete

───────────────────────────────────────────────────────────────

Signed: Helm Release Manager
Date: $(date +"%Y-%m-%d %H:%M:%S %Z")

═══════════════════════════════════════════════════════════════
             LINEAGE PRESERVED · CLOSURE COMPLETE
═══════════════════════════════════════════════════════════════
EOF

# Display certificate
cat releases/CLOSURE_CERTIFICATE_v1.1.0.txt

# Store in ConfigMap for permanent record
kubectl create configmap release-certificate-v1.1.0 \
  --from-file=certificate=releases/CLOSURE_CERTIFICATE_v1.1.0.txt \
  -n codexdominion
```

---

## 📌 Quick Reference

### Essential Commands
```bash
# Deploy/Upgrade
helm upgrade --install codexdominion ./codexdominion -n codexdominion -f values.yaml

# Status Check
helm status codexdominion -n codexdominion
kubectl get all,pvc -n codexdominion

# Rollback
helm rollback codexdominion -n codexdominion

# View History
helm history codexdominion -n codexdominion

# Uninstall (with lineage preservation)
helm uninstall codexdominion -n codexdominion --keep-history
```

### Troubleshooting
```bash
# Pod not starting
kubectl describe pod <pod-name> -n codexdominion
kubectl logs <pod-name> -n codexdominion --previous

# Service not accessible
kubectl get endpoints -n codexdominion
kubectl port-forward svc/codexdominion-node-crown 8080:80 -n codexdominion

# PVC not binding
kubectl describe pvc codexdominion-ledger -n codexdominion
kubectl get storageclass
```

---

**Eternal Principles Enforced:** ✓ Archive · ✓ Lineage · ✓ Ceremonial Closure

**Chart Version:** 1.1.0  
**Lineage:** Preserved  
**Status:** Complete
