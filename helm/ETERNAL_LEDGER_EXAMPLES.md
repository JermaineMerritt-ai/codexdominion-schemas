# Eternal Ledger Integration Examples

## PowerShell Examples

### Basic Deployment with Ledger Logging
```powershell
# Deploy using eternal-ledger wrapper
.\scripts\eternal-ledger.ps1 install codexdominion ./codexdominion codexdominion -f working-values.yaml

# Upgrade with ledger logging
.\scripts\eternal-ledger.ps1 upgrade codexdominion ./codexdominion codexdominion -f working-values.yaml --history-max 10

# Deploy using deploy.ps1 with ledger
.\deploy.ps1 -Upgrade -WithLedger -ValuesFile working-values.yaml
```

### Query Ledger
```powershell
# View all ledger entries
.\scripts\eternal-ledger.ps1 view

# Query specific release
.\scripts\eternal-ledger.ps1 query codexdominion

# Backup ledger
.\scripts\eternal-ledger.ps1 backup
```

### Rollback with Logging
```powershell
# Rollback to previous version
.\scripts\eternal-ledger.ps1 rollback codexdominion codexdominion

# Rollback to specific revision
.\scripts\eternal-ledger.ps1 rollback codexdominion codexdominion 3
```

### Manual Ledger Entry
```powershell
# Log custom action
.\scripts\eternal-ledger.ps1 log "manual-upgrade" codexdominion codexdominion 5 "1.1.0" "deployed"
```

---

## Bash Examples

### Basic Deployment with Ledger Logging
```bash
# Deploy using eternal-ledger wrapper
./scripts/eternal-ledger.sh install codexdominion ./charts/codexdominion codex -f values.yaml

# Upgrade with ledger logging
./scripts/eternal-ledger.sh upgrade codexdominion ./charts/codexdominion codex \
  -f values.yaml --history-max=10

# Set custom ledger path
export ETERNAL_LEDGER_PATH=/mnt/ledger/eternal-ledger.json
./scripts/eternal-ledger.sh install codexdominion ./charts/codexdominion codex
```

### Query Ledger
```bash
# View all ledger entries
./scripts/eternal-ledger.sh view

# Query specific release
./scripts/eternal-ledger.sh query codexdominion

# Backup ledger
./scripts/eternal-ledger.sh backup
```

### Rollback with Logging
```bash
# Rollback to previous version
./scripts/eternal-ledger.sh rollback codexdominion codex

# Rollback to specific revision
./scripts/eternal-ledger.sh rollback codexdominion codex 3
```

### Initialize Genesis Block
```bash
# Create ledger with genesis block
./scripts/eternal-ledger.sh init
```

---

## Kubernetes Pod Integration

### Mount Ledger as PVC
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: eternal-ledger-pvc
  namespace: codex
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: batch/v1
kind: Job
metadata:
  name: helm-deploy-with-ledger
  namespace: codex
spec:
  template:
    spec:
      containers:
      - name: helm-deployer
        image: alpine/helm:3.13.3
        command: ["/scripts/eternal-ledger.sh", "upgrade", "codexdominion", "/charts/codexdominion", "codex"]
        volumeMounts:
        - name: ledger
          mountPath: /var/log
        - name: scripts
          mountPath: /scripts
        - name: charts
          mountPath: /charts
        env:
        - name: ETERNAL_LEDGER_PATH
          value: "/var/log/eternal-ledger.json"
      volumes:
      - name: ledger
        persistentVolumeClaim:
          claimName: eternal-ledger-pvc
      - name: scripts
        configMap:
          name: eternal-ledger-scripts
          defaultMode: 0755
      - name: charts
        configMap:
          name: codexdominion-chart
      restartPolicy: Never
```

---

## CI/CD Integration Examples

### GitHub Actions
```yaml
name: Deploy with Eternal Ledger

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: '3.13.3'

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Deploy with Eternal Ledger
        run: |
          chmod +x ./scripts/eternal-ledger.sh
          ./scripts/eternal-ledger.sh upgrade codexdominion ./charts/codexdominion codex \
            -f values-prod.yaml \
            --history-max=10 \
            --wait \
            --timeout 10m

      - name: Backup Ledger
        run: ./scripts/eternal-ledger.sh backup

      - name: Upload Ledger Artifact
        uses: actions/upload-artifact@v3
        with:
          name: eternal-ledger
          path: /var/log/eternal-ledger.json*
```

### Azure DevOps
```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: HelmInstaller@1
    inputs:
      helmVersionToInstall: '3.13.3'

  - task: Kubernetes@1
    inputs:
      connectionType: 'Azure Resource Manager'
      azureSubscriptionEndpoint: '$(azureSubscription)'
      azureResourceGroup: '$(resourceGroup)'
      kubernetesCluster: '$(clusterName)'
      command: 'login'

  - bash: |
      chmod +x ./scripts/eternal-ledger.sh
      ./scripts/eternal-ledger.sh upgrade codexdominion ./charts/codexdominion codex \
        -f values-prod.yaml \
        --history-max=10 \
        --wait \
        --timeout 10m
    displayName: 'Deploy with Eternal Ledger'

  - bash: ./scripts/eternal-ledger.sh view
    displayName: 'Show Ledger Contents'

  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: '/var/log/eternal-ledger.json'
      artifactName: 'eternal-ledger'
```

### GitLab CI
```yaml
stages:
  - deploy

deploy-production:
  stage: deploy
  image: alpine/helm:3.13.3
  before_script:
    - apk add --no-cache bash jq
    - kubectl config use-context production
  script:
    - chmod +x ./scripts/eternal-ledger.sh
    - ./scripts/eternal-ledger.sh upgrade codexdominion ./charts/codexdominion codex
        -f values-prod.yaml
        --history-max=10
        --wait
        --timeout 10m
    - ./scripts/eternal-ledger.sh backup
  artifacts:
    paths:
      - /var/log/eternal-ledger.json*
    expire_in: 1 year
  only:
    - main
```

---

## Advanced Usage

### Pre-Deployment Hook
```bash
#!/bin/bash
# pre-deploy-hook.sh

# Run smoke tests before deployment
echo "Running smoke tests..."
kubectl run smoke-test --image=curlimages/curl --rm -it -- \
  curl http://codexdominion-node-crown/health

if [ $? -eq 0 ]; then
  echo "✓ Smoke tests passed, proceeding with deployment"
  ./scripts/eternal-ledger.sh upgrade codexdominion ./charts/codexdominion codex -f values.yaml
else
  echo "✗ Smoke tests failed, aborting deployment"
  exit 1
fi
```

### Post-Deployment Verification
```bash
#!/bin/bash
# post-deploy-verify.sh

RELEASE="codexdominion"
NAMESPACE="codex"

echo "Verifying deployment..."

# Check pod status
PODS_READY=$(kubectl get pods -n $NAMESPACE -l app=$RELEASE -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}')

if [[ "$PODS_READY" == *"False"* ]]; then
  echo "✗ Some pods not ready, rolling back"
  ./scripts/eternal-ledger.sh rollback $RELEASE $NAMESPACE
  exit 1
fi

# Test endpoints
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://codexdominion.app/health)

if [ "$RESPONSE" -ne 200 ]; then
  echo "✗ Health check failed (HTTP $RESPONSE), rolling back"
  ./scripts/eternal-ledger.sh rollback $RELEASE $NAMESPACE
  exit 1
fi

echo "✓ Deployment verified successfully"
./scripts/eternal-ledger.sh log "verification" $RELEASE $NAMESPACE "$(helm history $RELEASE -n $NAMESPACE --max 1 -o json | jq -r '.[0].revision')" "verified" "success"
```

### Ledger Analytics
```bash
#!/bin/bash
# ledger-analytics.sh

# Show deployment frequency
echo "📊 Deployment Frequency:"
jq '.releases | group_by(.action) | map({action: .[0].action, count: length})' /var/log/eternal-ledger.json

# Show failed deployments
echo "❌ Failed Deployments:"
jq '.releases[] | select(.status == "failed")' /var/log/eternal-ledger.json

# Show rollbacks
echo "⏮️ Rollback History:"
jq '.releases[] | select(.action == "rollback")' /var/log/eternal-ledger.json

# Export to CSV
echo "Exporting to CSV..."
jq -r '.releases[] | [.timestamp, .action, .release, .revision, .status] | @csv' \
  /var/log/eternal-ledger.json > eternal-ledger.csv
```

---

## Ledger File Format

```json
{
  "genesis_block": {
    "timestamp": "2025-12-02T10:30:00Z",
    "principles": ["Archive", "Lineage", "Ceremonial Closure"],
    "signatures": {
      "crown": ["Efficiency", "Knowledge", "Commerce", "Companion"],
      "council": ["Law", "Healthcare", "Commerce", "Education", "AI", "Family"]
    }
  },
  "releases": [
    {
      "action": "install",
      "release": "codexdominion",
      "namespace": "codexdominion",
      "revision": "1",
      "chart_version": "codexdominion-1.0.0",
      "status": "deployed",
      "timestamp": "2025-12-02T10:35:00Z",
      "operator": "jmerritt",
      "host": "deploy-server",
      "signatures": {
        "crown": ["Efficiency", "Knowledge", "Commerce", "Companion"],
        "council": ["Law", "Healthcare", "Commerce", "Education", "AI", "Family"]
      },
      "lineage_preserved": true
    },
    {
      "action": "upgrade",
      "release": "codexdominion",
      "namespace": "codexdominion",
      "revision": "2",
      "chart_version": "codexdominion-1.1.0",
      "status": "deployed",
      "timestamp": "2025-12-02T14:20:00Z",
      "operator": "jmerritt",
      "host": "deploy-server",
      "signatures": {
        "crown": ["Efficiency", "Knowledge", "Commerce", "Companion"],
        "council": ["Law", "Healthcare", "Commerce", "Education", "AI", "Family"]
      },
      "lineage_preserved": true
    }
  ]
}
```

---

**Eternal Principles:** Archive · Lineage · Ceremonial Closure
