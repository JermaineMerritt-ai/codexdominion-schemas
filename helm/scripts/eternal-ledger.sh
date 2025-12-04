#!/bin/bash
# Eternal Ledger - Helm Action Logger
# Archives every Helm operation for lineage preservation
# Lineage: Preserved | Archive: Enabled

set -euo pipefail

LEDGER_PATH="${ETERNAL_LEDGER_PATH:-/var/log/eternal-ledger.json}"
LEDGER_DIR=$(dirname "$LEDGER_PATH")

# Initialize ledger if not exists
initialize_ledger() {
  if [[ ! -f "$LEDGER_PATH" ]]; then
    mkdir -p "$LEDGER_DIR"
    cat > "$LEDGER_PATH" <<EOF
{
  "genesis_block": {
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "principles": ["Archive", "Lineage", "Ceremonial Closure"],
    "signatures": {
      "crown": ["Efficiency", "Knowledge", "Commerce", "Companion"],
      "council": ["Law", "Healthcare", "Commerce", "Education", "AI", "Family"]
    }
  },
  "releases": []
}
EOF
    echo "✓ Eternal Ledger genesis block created at $LEDGER_PATH"
  fi
}

# Log Helm action to Eternal Ledger
log_helm_action() {
  local ACTION=$1
  local RELEASE=$2
  local NAMESPACE=$3
  local REVISION=${4:-"N/A"}
  local CHART_VERSION=${5:-"N/A"}
  local STATUS=${6:-"unknown"}

  local TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local ENTRY=$(cat <<EOF
{
  "action": "$ACTION",
  "release": "$RELEASE",
  "namespace": "$NAMESPACE",
  "revision": "$REVISION",
  "chart_version": "$CHART_VERSION",
  "status": "$STATUS",
  "timestamp": "$TIMESTAMP",
  "operator": "${USER:-unknown}",
  "host": "${HOSTNAME:-unknown}",
  "signatures": {
    "crown": ["Efficiency", "Knowledge", "Commerce", "Companion"],
    "council": ["Law", "Healthcare", "Commerce", "Education", "AI", "Family"]
  },
  "lineage_preserved": true
}
EOF
)

  # Append to releases array
  initialize_ledger

  # Use jq to properly append to JSON array (if available), otherwise append as newline
  if command -v jq &> /dev/null; then
    local TEMP_FILE=$(mktemp)
    jq ".releases += [$ENTRY]" "$LEDGER_PATH" > "$TEMP_FILE"
    mv "$TEMP_FILE" "$LEDGER_PATH"
  else
    # Fallback: append as separate JSON objects (newline-delimited JSON)
    echo "$ENTRY" >> "${LEDGER_PATH}.ndjson"
  fi

  echo "✓ Logged $ACTION for $RELEASE (revision $REVISION) to Eternal Ledger"
}

# Get latest revision for a release
get_latest_revision() {
  local RELEASE=$1
  local NAMESPACE=$2

  helm history "$RELEASE" --namespace "$NAMESPACE" --max 1 -o json 2>/dev/null | \
    jq -r '.[0].revision // "unknown"' || echo "unknown"
}

# Get chart version from release
get_chart_version() {
  local RELEASE=$1
  local NAMESPACE=$2

  helm list --namespace "$NAMESPACE" -o json 2>/dev/null | \
    jq -r ".[] | select(.name==\"$RELEASE\") | .chart // \"unknown\"" || echo "unknown"
}

# Get release status
get_release_status() {
  local RELEASE=$1
  local NAMESPACE=$2

  helm status "$RELEASE" --namespace "$NAMESPACE" -o json 2>/dev/null | \
    jq -r '.info.status // "unknown"' || echo "unknown"
}

# Comprehensive logging wrapper for Helm commands
log_helm_install() {
  local RELEASE=$1
  local CHART=$2
  local NAMESPACE=$3
  shift 3

  echo "⏳ Installing $RELEASE from $CHART..."

  if helm install "$RELEASE" "$CHART" --namespace "$NAMESPACE" --create-namespace "$@"; then
    local REVISION=$(get_latest_revision "$RELEASE" "$NAMESPACE")
    local CHART_VERSION=$(get_chart_version "$RELEASE" "$NAMESPACE")
    local STATUS=$(get_release_status "$RELEASE" "$NAMESPACE")
    log_helm_action "install" "$RELEASE" "$NAMESPACE" "$REVISION" "$CHART_VERSION" "$STATUS"
    echo "✓ Installation complete and logged"
    return 0
  else
    log_helm_action "install_failed" "$RELEASE" "$NAMESPACE" "N/A" "N/A" "failed"
    echo "✗ Installation failed and logged"
    return 1
  fi
}

log_helm_upgrade() {
  local RELEASE=$1
  local CHART=$2
  local NAMESPACE=$3
  shift 3

  echo "⏳ Upgrading $RELEASE from $CHART..."

  if helm upgrade "$RELEASE" "$CHART" --namespace "$NAMESPACE" "$@"; then
    local REVISION=$(get_latest_revision "$RELEASE" "$NAMESPACE")
    local CHART_VERSION=$(get_chart_version "$RELEASE" "$NAMESPACE")
    local STATUS=$(get_release_status "$RELEASE" "$NAMESPACE")
    log_helm_action "upgrade" "$RELEASE" "$NAMESPACE" "$REVISION" "$CHART_VERSION" "$STATUS"
    echo "✓ Upgrade complete and logged"
    return 0
  else
    log_helm_action "upgrade_failed" "$RELEASE" "$NAMESPACE" "N/A" "N/A" "failed"
    echo "✗ Upgrade failed and logged"
    return 1
  fi
}

log_helm_rollback() {
  local RELEASE=$1
  local NAMESPACE=$2
  local TARGET_REVISION=${3:-0}

  echo "⏳ Rolling back $RELEASE to revision $TARGET_REVISION..."

  if helm rollback "$RELEASE" "$TARGET_REVISION" --namespace "$NAMESPACE"; then
    local REVISION=$(get_latest_revision "$RELEASE" "$NAMESPACE")
    local CHART_VERSION=$(get_chart_version "$RELEASE" "$NAMESPACE")
    local STATUS=$(get_release_status "$RELEASE" "$NAMESPACE")
    log_helm_action "rollback" "$RELEASE" "$NAMESPACE" "$REVISION" "$CHART_VERSION" "$STATUS"
    echo "✓ Rollback complete and logged"
    return 0
  else
    log_helm_action "rollback_failed" "$RELEASE" "$NAMESPACE" "$TARGET_REVISION" "N/A" "failed"
    echo "✗ Rollback failed and logged"
    return 1
  fi
}

log_helm_uninstall() {
  local RELEASE=$1
  local NAMESPACE=$2

  echo "⏳ Uninstalling $RELEASE (preserving history)..."

  local REVISION=$(get_latest_revision "$RELEASE" "$NAMESPACE")
  local CHART_VERSION=$(get_chart_version "$RELEASE" "$NAMESPACE")

  if helm uninstall "$RELEASE" --namespace "$NAMESPACE" --keep-history; then
    log_helm_action "uninstall" "$RELEASE" "$NAMESPACE" "$REVISION" "$CHART_VERSION" "uninstalled"
    echo "✓ Uninstall complete and logged (history preserved)"
    return 0
  else
    log_helm_action "uninstall_failed" "$RELEASE" "$NAMESPACE" "$REVISION" "$CHART_VERSION" "failed"
    echo "✗ Uninstall failed and logged"
    return 1
  fi
}

# View ledger contents
view_ledger() {
  if [[ ! -f "$LEDGER_PATH" ]]; then
    echo "✗ No ledger found at $LEDGER_PATH"
    return 1
  fi

  if command -v jq &> /dev/null; then
    echo "📜 Eternal Ledger Contents:"
    jq '.' "$LEDGER_PATH"
  else
    echo "📜 Eternal Ledger Contents (raw):"
    cat "$LEDGER_PATH"
  fi
}

# Query ledger by release name
query_ledger() {
  local RELEASE=$1

  if [[ ! -f "$LEDGER_PATH" ]]; then
    echo "✗ No ledger found at $LEDGER_PATH"
    return 1
  fi

  if command -v jq &> /dev/null; then
    echo "📜 Ledger entries for release '$RELEASE':"
    jq ".releases[] | select(.release==\"$RELEASE\")" "$LEDGER_PATH"
  else
    echo "✗ jq not installed. Install jq for querying."
    return 1
  fi
}

# Export ledger to timestamped backup
backup_ledger() {
  local BACKUP_PATH="${LEDGER_PATH}.backup.$(date +%Y%m%d-%H%M%S)"

  if [[ -f "$LEDGER_PATH" ]]; then
    cp "$LEDGER_PATH" "$BACKUP_PATH"
    echo "✓ Ledger backed up to $BACKUP_PATH"
  else
    echo "✗ No ledger to backup"
    return 1
  fi
}

# Main CLI
case "${1:-help}" in
  install)
    shift
    log_helm_install "$@"
    ;;
  upgrade)
    shift
    log_helm_upgrade "$@"
    ;;
  rollback)
    shift
    log_helm_rollback "$@"
    ;;
  uninstall)
    shift
    log_helm_uninstall "$@"
    ;;
  log)
    shift
    log_helm_action "$@"
    ;;
  view)
    view_ledger
    ;;
  query)
    shift
    query_ledger "$@"
    ;;
  backup)
    backup_ledger
    ;;
  init)
    initialize_ledger
    ;;
  *)
    cat <<EOF
Eternal Ledger - Helm Action Logger
Usage: $0 <command> [args...]

Commands:
  install <release> <chart> <namespace> [helm-args...]
      Install a chart and log to ledger

  upgrade <release> <chart> <namespace> [helm-args...]
      Upgrade a release and log to ledger

  rollback <release> <namespace> [revision]
      Rollback a release and log to ledger

  uninstall <release> <namespace>
      Uninstall a release (keep history) and log to ledger

  log <action> <release> <namespace> [revision] [chart_version] [status]
      Manually log an action to ledger

  view
      View entire ledger contents

  query <release>
      Query ledger for specific release

  backup
      Create timestamped backup of ledger

  init
      Initialize genesis block

Environment Variables:
  ETERNAL_LEDGER_PATH    Path to ledger file (default: /var/log/eternal-ledger.json)

Examples:
  # Install with logging
  $0 install codexdominion ./charts/codexdominion codex -f values.yaml

  # Upgrade with logging
  $0 upgrade codexdominion ./charts/codexdominion codex -f values.yaml --history-max=10

  # Rollback with logging
  $0 rollback codexdominion codex 3

  # View all logged actions
  $0 view

  # Query specific release
  $0 query codexdominion

  # Backup ledger
  $0 backup

Eternal Principles: Archive · Lineage · Ceremonial Closure
EOF
    ;;
esac
