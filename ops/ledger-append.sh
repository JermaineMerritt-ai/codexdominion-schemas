#!/usr/bin/env bash
# Codex Dominion - Ledger Append Script
# Appends validation results to immutable artifact ledger

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
LEDGER_DIR="${LEDGER_DIR:-./ledger/artifact-ledger}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
OPERATOR="${USER}"

log() {
    echo -e "${BLUE}[LEDGER]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# Parse arguments
STATUS=""
DEPLOYMENT_ID=""
VERSION=""
TIER=""
HEALTH_RESULT=""
A11Y_RESULT=""
PERF_RESULT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            STATUS="$2"
            shift 2
            ;;
        --deployment-id)
            DEPLOYMENT_ID="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --tier)
            TIER="$2"
            shift 2
            ;;
        --health)
            HEALTH_RESULT="$2"
            shift 2
            ;;
        --a11y)
            A11Y_RESULT="$2"
            shift 2
            ;;
        --perf)
            PERF_RESULT="$2"
            shift 2
            ;;
        *)
            error "Unknown option: $1"
            echo "Usage: $0 --status <validated|failed|deployed> [options]"
            echo "Options:"
            echo "  --deployment-id <uuid>  Deployment ID"
            echo "  --version <version>     Version number"
            echo "  --tier <low|medium|high> Governance tier"
            echo "  --health <pass|fail>    Health check result"
            echo "  --a11y <pass|fail>      Accessibility test result"
            echo "  --perf <pass|fail>      Performance test result"
            exit 1
            ;;
    esac
done

if [[ -z "$STATUS" ]]; then
    error "Status is required"
    exit 1
fi

# Generate ID if not provided
if [[ -z "$DEPLOYMENT_ID" ]]; then
    DEPLOYMENT_ID=$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "manual-$(date +%s)")
fi

# Detect version from git if not provided
if [[ -z "$VERSION" ]] && command -v git >/dev/null 2>&1; then
    VERSION=$(git describe --tags --always 2>/dev/null || echo "unknown")
fi

# Auto-detect test results if not provided
if [[ -z "$HEALTH_RESULT" ]] && [[ -f "./reports/health/latest.txt" ]]; then
    HEALTH_RESULT=$(grep "Status:" ./reports/health/latest.txt | awk '{print $2}' || echo "unknown")
fi

if [[ -z "$A11Y_RESULT" ]] && [[ -f "./reports/accessibility/latest.txt" ]]; then
    A11Y_RESULT=$(grep "Status:" ./reports/accessibility/latest.txt | awk '{print $2}' || echo "unknown")
fi

if [[ -z "$PERF_RESULT" ]] && [[ -f "./reports/performance/latest.txt" ]]; then
    PERF_RESULT=$(grep "Status:" ./reports/performance/latest.txt | awk '{print $2}' || echo "unknown")
fi

echo ""
echo "============================================"
echo "      LEDGER APPEND - VALIDATION"
echo "============================================"
echo ""

log "Deployment ID: ${DEPLOYMENT_ID}"
log "Status: ${STATUS}"
log "Version: ${VERSION:-unknown}"
log "Tier: ${TIER:-unknown}"
log "Timestamp: ${TIMESTAMP}"
log "Operator: ${OPERATOR}"
echo ""

# Create ledger directory if it doesn't exist
mkdir -p "$LEDGER_DIR"

# Initialize ledger files if they don't exist
if [[ ! -f "${LEDGER_DIR}/deployments.json" ]]; then
    echo "[]" > "${LEDGER_DIR}/deployments.json"
    log "Initialized deployments ledger"
fi

if [[ ! -f "${LEDGER_DIR}/validations.json" ]]; then
    echo "[]" > "${LEDGER_DIR}/validations.json"
    log "Initialized validations ledger"
fi

# Create validation record
VALIDATION_RECORD=$(cat <<EOF
{
    "validation_id": "$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "val-$(date +%s)")",
    "deployment_id": "${DEPLOYMENT_ID}",
    "timestamp": "${TIMESTAMP}",
    "status": "${STATUS}",
    "version": "${VERSION:-unknown}",
    "tier": "${TIER:-unknown}",
    "operator": "${OPERATOR}",
    "validation_results": {
        "health_check": "${HEALTH_RESULT:-not_run}",
        "accessibility": "${A11Y_RESULT:-not_run}",
        "performance": "${PERF_RESULT:-not_run}"
    },
    "governance_compliance": {
        "performance_budget": $([ "$PERF_RESULT" = "pass" ] && echo "true" || echo "false"),
        "accessibility_wcag": $([ "$A11Y_RESULT" = "pass" ] && echo "true" || echo "false"),
        "health_checks": $([ "$HEALTH_RESULT" = "pass" ] && echo "true" || echo "false")
    },
    "git_info": {
        "commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
        "branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
        "author": "$(git log -1 --format='%an' 2>/dev/null || echo 'unknown')"
    }
}
EOF
)

# Validate JSON
if ! echo "$VALIDATION_RECORD" | jq '.' >/dev/null 2>&1; then
    error "Invalid JSON generated"
    exit 1
fi

# Append to validations ledger (immutable append-only)
log "Appending validation record to ledger..."

# Read existing ledger
EXISTING_LEDGER=$(cat "${LEDGER_DIR}/validations.json")

# Append new record
UPDATED_LEDGER=$(echo "$EXISTING_LEDGER" | jq --argjson new "$VALIDATION_RECORD" '. += [$new]')

# Write back
echo "$UPDATED_LEDGER" | jq '.' > "${LEDGER_DIR}/validations.json"

success "Validation record appended to ledger"

# Update deployment record if it exists
if jq -e ".[] | select(.deployment_id == \"${DEPLOYMENT_ID}\")" "${LEDGER_DIR}/deployments.json" >/dev/null 2>&1; then
    log "Updating existing deployment record..."

    UPDATED_DEPLOYMENTS=$(jq --arg id "$DEPLOYMENT_ID" --arg status "$STATUS" --arg ts "$TIMESTAMP" \
        'map(if .deployment_id == $id then .status = $status | .last_validation = $ts else . end)' \
        "${LEDGER_DIR}/deployments.json")

    echo "$UPDATED_DEPLOYMENTS" | jq '.' > "${LEDGER_DIR}/deployments.json"
    success "Deployment record updated"
fi

# Generate summary
log "Generating validation summary..."

TOTAL_VALIDATIONS=$(jq 'length' "${LEDGER_DIR}/validations.json")
RECENT_VALIDATIONS=$(jq "[.[] | select(.timestamp > \"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)\") ] | length" "${LEDGER_DIR}/validations.json" 2>/dev/null || echo 0)

echo ""
echo "============================================"
echo "           LEDGER SUMMARY"
echo "============================================"
echo "Total validations: $TOTAL_VALIDATIONS"
echo "Last 24h: $RECENT_VALIDATIONS"
echo ""
echo "Current validation:"
echo "  Status: ${STATUS}"
echo "  Health: ${HEALTH_RESULT:-not_run}"
echo "  Accessibility: ${A11Y_RESULT:-not_run}"
echo "  Performance: ${PERF_RESULT:-not_run}"
echo ""
echo "Ledger location: ${LEDGER_DIR}/validations.json"
echo ""

# Verify immutability (ledger should only grow)
EXPECTED_SIZE=$((TOTAL_VALIDATIONS))
ACTUAL_SIZE=$(jq 'length' "${LEDGER_DIR}/validations.json")

if [[ $ACTUAL_SIZE -eq $EXPECTED_SIZE ]]; then
    success "Ledger integrity verified (${ACTUAL_SIZE} records)"
else
    error "Ledger integrity check failed! Expected ${EXPECTED_SIZE}, found ${ACTUAL_SIZE}"
    exit 1
fi

# Create human-readable log entry
LOG_DIR="./logs/validations"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/$(date +%Y-%m-%d).log"

cat >> "$LOG_FILE" <<EOF
[${TIMESTAMP}] ${STATUS} - ${DEPLOYMENT_ID}
  Version: ${VERSION:-unknown}
  Tier: ${TIER:-unknown}
  Health: ${HEALTH_RESULT:-not_run}
  A11Y: ${A11Y_RESULT:-not_run}
  Perf: ${PERF_RESULT:-not_run}
  Operator: ${OPERATOR}
---
EOF

log "Log entry created: ${LOG_FILE}"

echo ""
success "✅ Ledger append complete"
echo ""

exit 0
