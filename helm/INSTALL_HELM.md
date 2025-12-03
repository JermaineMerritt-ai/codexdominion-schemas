# Installing Helm

## Prerequisites Not Met

Helm 3.x is required to deploy this chart but is not currently installed.

## Installation Options

### Option 1: Chocolatey (Recommended for Windows)

```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Helm
choco install kubernetes-helm
```

### Option 2: Scoop

```powershell
# Install Scoop (if not already installed)
iwr -useb get.scoop.sh | iex

# Install Helm
scoop install helm
```

### Option 3: Direct Download

1. Download Helm from: https://github.com/helm/helm/releases
2. Download the Windows AMD64 version (e.g., `helm-v3.13.0-windows-amd64.zip`)
3. Extract the ZIP file
4. Move `helm.exe` to a directory in your PATH (e.g., `C:\Program Files\helm\`)
5. Add that directory to your system PATH
6. Restart your terminal

### Option 4: Winget (Windows 11)

```powershell
winget install Helm.Helm
```

## Verify Installation

After installing, verify Helm is working:

```powershell
helm version --short
```

Expected output:
```
v3.x.x+gxxxxxxx
```

## Also Required: Kubernetes Cluster

To deploy this Helm chart, you also need:

1. **Kubernetes cluster** (one of):
   - Local: Docker Desktop with Kubernetes enabled
   - Local: Minikube
   - Local: Kind (Kubernetes in Docker)
   - Cloud: AKS (Azure), EKS (AWS), GKE (Google Cloud)

2. **kubectl** - Kubernetes command-line tool
   ```powershell
   choco install kubernetes-cli
   ```

3. **kubectl configured** to access your cluster:
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

## Quick Local Setup (Docker Desktop)

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Enable Kubernetes in Docker Desktop settings
3. Install Helm (see options above)
4. Verify:
   ```powershell
   kubectl get nodes
   helm version
   ```

## Alternative: Template Without Installing

If you just want to see the rendered Kubernetes manifests without Helm:

```powershell
# This would work if Helm were installed
helm template codexdominion ./codexdominion > rendered-manifests.yaml
```

Then you could deploy with kubectl:
```powershell
kubectl apply -f rendered-manifests.yaml -n codexdominion
```

## Next Steps

After installing Helm and setting up Kubernetes:

1. Return to the helm directory
2. Run the deployment script:
   ```powershell
   .\deploy.ps1
   ```

Or deploy directly:
```powershell
helm install codexdominion ./codexdominion -n codexdominion --create-namespace
```

## Resources

- Helm Documentation: https://helm.sh/docs/
- Kubernetes Documentation: https://kubernetes.io/docs/
- Docker Desktop: https://docs.docker.com/desktop/
