# Building and Pushing Docker Images

## Current Status
✅ Helm chart deployed successfully to AKS
⚠️ Pods waiting for Docker images

## Required Images
1. `codexdominion/node:latest` - Node.js frontend
2. `codexdominion/python:latest` - Python backend
3. `codexdominion/java:latest` - Java enterprise

## Option 1: Build and Push to Docker Hub

### 1. Create Docker Hub Account
- Sign up at: https://hub.docker.com/

### 2. Login to Docker
```powershell
docker login
```

### 3. Build Images

**Node Crown (Frontend):**
```powershell
cd ..\frontend
docker build -t your-dockerhub-username/codexdominion-node:latest .
docker tag your-dockerhub-username/codexdominion-node:latest codexdominion/node:latest
docker push your-dockerhub-username/codexdominion-node:latest
```

**Python Council (Backend):**
```powershell
cd ..\backend
docker build -t your-dockerhub-username/codexdominion-python:latest .
docker tag your-dockerhub-username/codexdominion-python:latest codexdominion/python:latest
docker push your-dockerhub-username/codexdominion-python:latest
```

**Java Crown (Enterprise):**
```powershell
cd ..\random-java
docker build -t your-dockerhub-username/codexdominion-java:latest .
docker tag your-dockerhub-username/codexdominion-java:latest codexdominion/java:latest
docker push your-dockerhub-username/codexdominion-java:latest
```

## Option 2: Use Azure Container Registry (ACR)

### 1. Create ACR
```bash
az acr create --resource-group codex-rg --name codexdominion --sku Basic
```

### 2. Login to ACR
```bash
az acr login --name codexdominion
```

### 3. Build and Push
```powershell
# Get ACR login server
$acrServer = az acr show --name codexdominion --query loginServer -o tsv

# Build and push Node
cd ..\frontend
docker build -t "$acrServer/codexdominion/node:latest" .
docker push "$acrServer/codexdominion/node:latest"

# Build and push Python
cd ..\backend
docker build -t "$acrServer/codexdominion/python:latest" .
docker push "$acrServer/codexdominion/python:latest"

# Build and push Java
cd ..\random-java
docker build -t "$acrServer/codexdominion/java:latest" .
docker push "$acrServer/codexdominion/java:latest"
```

### 4. Update Helm Values
Create `custom-values.yaml`:
```yaml
nodeCrown:
  image: codexdominion.azurecr.io/codexdominion/node:latest

pythonCouncil:
  image: codexdominion.azurecr.io/codexdominion/python:latest

javaCrown:
  image: codexdominion.azurecr.io/codexdominion/java:latest
```

### 5. Upgrade Helm Release
```powershell
helm upgrade codexdominion ./codexdominion -n codexdominion -f custom-values.yaml
```

## Option 3: Use Placeholder Images (for testing)

Update to use existing public images temporarily:

```powershell
# Create test values
@"
nodeCrown:
  image: nginx:alpine

pythonCouncil:
  image: python:3.11-alpine

javaCrown:
  image: openjdk:21-slim
"@ | Out-File -FilePath test-values.yaml

# Upgrade deployment
helm upgrade codexdominion ./codexdominion -n codexdominion -f test-values.yaml
```

## Check Deployment Progress

```powershell
# Watch pods
kubectl get pods -n codexdominion -w

# Check pod details
kubectl describe pod -n codexdominion <pod-name>

# View logs
kubectl logs -n codexdominion -l component=node-crown -f
```

## Current Deployment Info

```powershell
# View release
helm list -n codexdominion

# Get status
helm status codexdominion -n codexdominion

# View manifests
helm get manifest codexdominion -n codexdominion
```

## Rollback if Needed

```powershell
# Rollback to previous version
helm rollback codexdominion -n codexdominion

# Uninstall completely
helm uninstall codexdominion -n codexdominion
```
