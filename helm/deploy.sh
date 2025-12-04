#!/bin/bash
# CodexDominion Helm Chart Deployment Script (Bash)
# Eternal Ledger Version: 1.0

set -e

# Default values
NAMESPACE="codexdominion"
RELEASE_NAME="codexdominion"
VALUES_FILE=""
DRY_RUN=false
UPGRADE=false
UNINSTALL=false
VALIDATE=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -r|--release)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -f|--values)
            VALUES_FILE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --upgrade)
            UPGRADE=true
            shift
            ;;
        --uninstall)
            UNINSTALL=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART_PATH="$SCRIPT_DIR/codexdominion"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              CODEXDOMINION HELM DEPLOYMENT                     ║"
echo "║                 Eternal Ledger Version 1.0                     ║"
echo "║                    Lineage: Preserved                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Check prerequisites
echo -e "\n🔍 Checking prerequisites..."
if ! command -v helm &> /dev/null; then
    echo "✗ Helm is not installed"
    exit 1
fi
echo "✓ Helm installed: $(helm version --short)"

if ! command -v kubectl &> /dev/null; then
    echo "✗ kubectl is not installed"
    exit 1
fi
echo "✓ kubectl installed"

# Validate chart
if [ "$VALIDATE" = true ]; then
    echo -e "\n📋 Validating Helm chart..."
    helm lint "$CHART_PATH"
    echo "✓ Chart validation passed"
fi

# Uninstall if requested
if [ "$UNINSTALL" = true ]; then
    echo -e "\n🗑️  Uninstalling release: $RELEASE_NAME"
    helm uninstall "$RELEASE_NAME" --namespace "$NAMESPACE"
    echo "✓ Release uninstalled"
    echo -e "\n⚠️  Note: PersistentVolumeClaim '$RELEASE_NAME-ledger' not deleted"
    echo "   To delete eternal ledger storage, run:"
    echo "   kubectl delete pvc $RELEASE_NAME-ledger -n $NAMESPACE"
    exit 0
fi

# Create namespace
echo -e "\n🏗️  Ensuring namespace exists..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
echo "✓ Namespace ready: $NAMESPACE"

# Build helm command
HELM_CMD="install"
if [ "$UPGRADE" = true ]; then
    HELM_CMD="upgrade --install"
fi

HELM_ARGS=(
    "$RELEASE_NAME"
    "$CHART_PATH"
    "--namespace" "$NAMESPACE"
    "--create-namespace"
)

if [ -n "$VALUES_FILE" ] && [ -f "$VALUES_FILE" ]; then
    HELM_ARGS+=("--values" "$VALUES_FILE")
    echo "✓ Using custom values: $VALUES_FILE"
fi

if [ "$DRY_RUN" = true ]; then
    HELM_ARGS+=("--dry-run")
    echo -e "\n🧪 Running dry-run (no changes will be made)..."
fi

# Deploy
echo -e "\n🚀 Deploying CodexDominion..."
echo "   Command: helm $HELM_CMD ${HELM_ARGS[*]}"

helm "$HELM_CMD" "${HELM_ARGS[@]}"
echo -e "\n✓ Deployment successful!"

if [ "$DRY_RUN" = false ]; then
    # Wait for deployments
    echo -e "\n⏳ Waiting for deployments to be ready..."

    DEPLOYMENTS=(
        "$RELEASE_NAME-node-crown"
        "$RELEASE_NAME-python-council"
        "$RELEASE_NAME-java-crown"
    )

    for deployment in "${DEPLOYMENTS[@]}"; do
        echo "   Waiting for $deployment..."
        kubectl rollout status "deployment/$deployment" -n "$NAMESPACE" --timeout=300s
    done

    echo -e "\n✓ All deployments ready!"

    # Show status
    echo -e "\n📊 Deployment Status:"
    kubectl get pods -n "$NAMESPACE" -l "app=$RELEASE_NAME"

    echo -e "\n🌐 Services:"
    kubectl get svc -n "$NAMESPACE" -l "app=$RELEASE_NAME"

    echo -e "\n🔗 Ingress:"
    kubectl get ingress -n "$NAMESPACE" "$RELEASE_NAME"

    # Show access instructions
    cat << EOF

╔════════════════════════════════════════════════════════════════╗
║                   DEPLOYMENT COMPLETE                          ║
╚════════════════════════════════════════════════════════════════╝

📜 View release info:
   helm list -n $NAMESPACE
   helm status $RELEASE_NAME -n $NAMESPACE

📋 View schemas:
   kubectl get configmap $RELEASE_NAME-schemas -n $NAMESPACE -o yaml

🔍 View logs:
   kubectl logs -l component=node-crown -n $NAMESPACE -f
   kubectl logs -l component=python-council -n $NAMESPACE -f
   kubectl logs -l component=java-crown -n $NAMESPACE -f

🌐 Access services locally:
   kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-node-crown 3000:3000
   kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-python-council 8000:8000
   kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-java-crown 8080:8080

💾 Check Eternal Ledger:
   kubectl exec -it -n $NAMESPACE deployment/$RELEASE_NAME-python-council -- ls -la /var/codexdominion/ledger

═══════════════════════════════════════════════════════════════
EOF
fi

echo "✨ Eternal Principles Enforced ✨"
