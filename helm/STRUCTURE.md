# Helm Chart Structure Overview

## 📁 Directory Layout

```
helm/
├── deploy.ps1                          # PowerShell deployment script
├── deploy.sh                           # Bash deployment script
├── QUICKSTART.md                       # This file
└── codexdominion/
    ├── Chart.yaml                      # Chart metadata
    ├── values.yaml                     # Default configuration values
    ├── README.md                       # Comprehensive documentation
    ├── .helmignore                     # Files to exclude from package
    └── templates/
        ├── NOTES.txt                   # Post-install instructions
        ├── node-crown-deployment.yaml  # Node.js frontend deployment
        ├── python-council-deployment.yaml # Python backend deployment
        ├── java-crown-deployment.yaml  # Java enterprise deployment
        ├── codex-schemas-configmap.yaml # Schema definitions
        ├── ingress.yaml                # Ingress routing rules
        └── eternal-ledger-pvc.yaml     # Persistent storage
```

## 📄 File Descriptions

### Chart.yaml
Chart metadata including:
- Name: `codexdominion`
- Version: `1.0.0`
- App Version: `1.0`
- Description and keywords

### values.yaml
Default configuration with:
- **replicaCount**: 2 (number of replicas per service)
- **nodeCrown**: Node.js frontend configuration
  - Image, port (3000), resources, environment
- **pythonCouncil**: Python backend configuration
  - Image, port (8000), resources, environment
- **javaCrown**: Java enterprise configuration
  - Image, port (8080), resources, environment
- **schemas**: Schema definitions (version 1.0, lineage preserved)
- **ingress**: Ingress configuration
  - Host: `codexdominion.app`
  - TLS enabled
  - Routing to all services
- **storage**: Persistent storage for Eternal Ledger
  - Size: 10Gi
  - Mount path: `/var/codexdominion/ledger`

### Templates

#### node-crown-deployment.yaml
- Deployment with 2 replicas
- Service exposing port 3000
- Health checks at `/health` and `/ready`
- Resource limits and requests
- Environment variables from values.yaml

#### python-council-deployment.yaml
- Deployment with 2 replicas
- Service exposing port 8000
- Health checks
- Volume mounts for schemas and eternal ledger
- ConfigMap injection for schema version

#### java-crown-deployment.yaml
- Deployment with 2 replicas
- Service exposing port 8080
- Spring Boot actuator health checks
- Volume mounts for schemas and eternal ledger
- Java-specific environment variables

#### codex-schemas-configmap.yaml
Complete schema definitions:
- **artifact.yaml**: Artifact schema
- **constellation.yaml**: Constellation mappings
- **council.yaml**: Council structures
- **crown.yaml**: Crown authorities
- **invocation.yaml**: Ritual invocations
- **ledger.yaml**: Ledger entry definitions
- **principles.yaml**: Eternal Ledger principles

#### ingress.yaml
Routing configuration:
- `/` → Node Crown (frontend)
- `/api` → Python Council (backend API)
- `/enterprise` → Java Crown (enterprise services)
- `/actuator` → Java Crown (Spring Boot actuator)
- TLS termination with cert-manager

#### eternal-ledger-pvc.yaml
- PersistentVolumeClaim for eternal storage
- Size configurable (default 10Gi)
- ReadWriteMany access mode
- Initialization script for genesis block

## 🎨 Customization Points

### Image Tags
```yaml
nodeCrown:
  image: codexdominion/node:v2.0.0  # Change version

pythonCouncil:
  image: myregistry.com/codexdominion/python:latest

javaCrown:
  image: codexdominion/java:1.5.0
```

### Scaling
```yaml
replicaCount: 5  # Scale all services to 5 replicas
```

### Resources
```yaml
nodeCrown:
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi
```

### Domain & TLS
```yaml
ingress:
  host: production.codexdominion.com
  tls:
    secretName: prod-tls-cert
```

### Storage
```yaml
storage:
  size: 100Gi
  className: fast-ssd
  mountPath: /var/codexdominion/ledger
```

## 🔧 Template Functions Used

### Helm Built-in Functions
- `{{ .Chart.Name }}` - Chart name
- `{{ .Chart.Version }}` - Chart version
- `{{ .Values.* }}` - Values from values.yaml
- `{{ .Release.Name }}` - Release name
- `{{ .Release.Namespace }}` - Target namespace

### Flow Control
```yaml
{{- if .Values.ingress.enabled }}
  # Ingress configuration
{{- end }}

{{- range .Values.nodeCrown.env }}
  - name: {{ .name }}
    value: {{ .value }}
{{- end }}
```

### YAML Processing
```yaml
resources:
  {{- toYaml .Values.nodeCrown.resources | nindent 10 }}
```

### String Processing
```yaml
value: {{ .value | quote }}
```

## 🏷️ Labels & Selectors

All resources use consistent labels:
```yaml
labels:
  app: codexdominion                  # Chart name
  component: node-crown               # Component type
  version: 1.0.0                      # Chart version
  lineage: preserved                  # Eternal ledger marker
```

Selectors match on:
```yaml
selector:
  matchLabels:
    app: codexdominion
    component: node-crown
```

## 🔐 Security Features

### Resource Limits
All containers have CPU and memory limits to prevent resource exhaustion.

### Health Checks
- **Liveness probes**: Restart unhealthy containers
- **Readiness probes**: Remove unready pods from service

### Network Policies
Can be added for pod-to-pod communication restrictions.

### Image Pull Policies
Set to `IfNotPresent` to cache images locally.

### TLS
Ingress supports TLS termination with cert-manager integration.

## 📊 Observability

### Prometheus Annotations
```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "3000"
```

### Logging
All containers log to stdout/stderr for aggregation.

### Health Endpoints
- Node Crown: `/health`, `/ready`
- Python Council: `/health`, `/ready`
- Java Crown: `/actuator/health`, `/actuator/health/readiness`

## 🔄 Upgrade Path

### Version 1.0.0 → 1.1.0
1. Update `Chart.yaml` version
2. Update image tags in `values.yaml`
3. Add/modify templates as needed
4. Run: `helm upgrade codexdominion ./codexdominion`

### Schema Evolution
Schemas are versioned in ConfigMap:
```yaml
data:
  version: "1.1"
  artifact.yaml: |
    schema: artifact
    version: 1.1
    # Updated schema definition
```

## 💡 Tips & Tricks

### Test Templates Locally
```bash
helm template codexdominion ./codexdominion
```

### Debug Values
```bash
helm install --dry-run --debug codexdominion ./codexdominion
```

### Validate YAML
```bash
helm lint codexdominion
```

### Get Rendered Manifest
```bash
helm get manifest codexdominion -n codexdominion
```

### Compare Changes
```bash
# Before upgrade
helm get manifest codexdominion -n codexdominion > old.yaml

# After upgrade
helm get manifest codexdominion -n codexdominion > new.yaml

# Diff
diff old.yaml new.yaml
```

## 🎯 Production Checklist

- [ ] Update image tags to specific versions (no `latest`)
- [ ] Configure resource limits appropriately
- [ ] Set up TLS certificates
- [ ] Configure ingress hostname
- [ ] Adjust replica counts for load
- [ ] Set up monitoring/alerting
- [ ] Configure backup strategy for eternal ledger
- [ ] Test rollback procedure
- [ ] Document custom values
- [ ] Set up CI/CD pipeline

---

**Chart Version:** 1.0.0  
**Eternal Ledger:** Preserved ✨
