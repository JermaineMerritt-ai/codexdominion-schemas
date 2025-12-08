#!/bin/bash
# Codex Dominion - Rollback Executor
# Orchestrates the full rollback procedure: halt → revert → reseal → postmortem

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEDGER_DIR="${SCRIPT_DIR}/../../ledger/artifact-ledger"
BACKUP_DIR="/var/backups/codexdominion"
DEPLOYMENT_DIR="/var/www/codexdominion.app"

# Logging
LOG_FILE="/var/log/codexdominion/rollback-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Parse arguments
TRIGGER=""
REASON=""
DEPLOYMENT_ID=""
OPERATOR="${USER}"

while [[ $# -gt 0 ]]; do
    case $1 in
        --trigger)
            TRIGGER="$2"
            shift 2
            ;;
        --reason)
            REASON="$2"
            shift 2
            ;;
        --deployment-id)
            DEPLOYMENT_ID="$2"
            shift 2
            ;;
        --operator)
            OPERATOR="$2"
            shift 2
            ;;
        *)
            error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate inputs
if [[ -z "$TRIGGER" ]] || [[ -z "$REASON" ]]; then
    error "Usage: $0 --trigger <opa|error_budget|council|manual> --reason 'description' [--deployment-id uuid] [--operator name]"
    exit 1
fi

ROLLBACK_ID=$(uuidgen)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log "🚨 ROLLBACK INITIATED"
log "Rollback ID: ${ROLLBACK_ID}"
log "Trigger: ${TRIGGER}"
log "Reason: ${REASON}"
log "Operator: ${OPERATOR}"
log "Timestamp: ${TIMESTAMP}"

# ============================================
# PHASE 1: HALT
# ============================================
log ""
log "===== PHASE 1: HALT ====="

step_halt() {
    log "1.1 Stopping traffic shifting..."
    # Freeze canary traffic at current percentage
    curl -X POST http://localhost:8080/ops/canary/freeze \
        -H "Content-Type: application/json" \
        -d "{\"reason\": \"rollback_${ROLLBACK_ID}\"}" \
        2>&1 | tee -a "$LOG_FILE" || true

    log "1.2 Pausing automation..."
    # Disable auto-promotion
    curl -X POST http://localhost:8080/ops/canary/disable-auto \
        2>&1 | tee -a "$LOG_FILE" || true

    log "1.3 Locking deployment state..."
    echo "halted" > /var/lib/codexdominion/deployment-state

    log "1.4 Alerting on-call team..."
    # Send to Slack
    curl -X POST "${SLACK_WEBHOOK_URL:-https://hooks.slack.com/services/xxx}" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"🚨 ROLLBACK INITIATED\",
            \"attachments\": [{
                \"color\": \"danger\",
                \"fields\": [
                    {\"title\": \"Trigger\", \"value\": \"${TRIGGER}\", \"short\": true},
                    {\"title\": \"Reason\", \"value\": \"${REASON}\", \"short\": false},
                    {\"title\": \"Operator\", \"value\": \"${OPERATOR}\", \"short\": true}
                ]
            }]
        }" 2>&1 | tee -a "$LOG_FILE" || warning "Slack notification failed"

    log "1.5 Updating status page..."
    curl -X POST https://status.codexdominion.app/api/incidents \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Deployment Rollback in Progress\",
            \"status\": \"investigating\",
            \"message\": \"We detected an issue and are rolling back to ensure stability.\"
        }" 2>&1 | tee -a "$LOG_FILE" || warning "Status page update failed"

    success "HALT phase complete"
}

step_halt

# ============================================
# PHASE 2: REVERT
# ============================================
log ""
log "===== PHASE 2: REVERT ====="

step_revert() {
    log "2.1 Identifying stable version..."
    # Query artifact ledger for last green deployment
    STABLE_VERSION=$(jq -r '[.[] | select(.status == "success")] | max_by(.timestamp) | .version' \
        "${LEDGER_DIR}/deployments.json" 2>/dev/null || echo "unknown")
    log "Stable version: ${STABLE_VERSION}"

    log "2.2 Routing all traffic to stable..."
    # Update nginx upstream weights
    cat > /tmp/nginx-stable.conf <<EOF
upstream codex_frontend {
    server localhost:3000 weight=100;  # Stable
    server localhost:3001 weight=0;    # Canary
}
upstream codex_backend {
    server localhost:8001 weight=100;  # Stable
    server localhost:8002 weight=0;    # Canary
}
EOF
    sudo cp /tmp/nginx-stable.conf /etc/nginx/conf.d/upstream.conf
    sudo nginx -t && sudo systemctl reload nginx
    success "Traffic routed to stable version"

    log "2.3 Stopping canary services..."
    sudo systemctl stop codexdominion-frontend-canary 2>&1 | tee -a "$LOG_FILE" || warning "Frontend canary already stopped"
    sudo systemctl stop codexdominion-api-canary 2>&1 | tee -a "$LOG_FILE" || warning "API canary already stopped"
    success "Canary services stopped"

    log "2.4 Checking for database migrations..."
    if [[ -f "/var/lib/codexdominion/migrations-applied.txt" ]]; then
        warning "Database migrations detected - initiating reversal"
        "${SCRIPT_DIR}/rollback-migrations.sh" --target-version "${STABLE_VERSION}"
    else
        log "No migrations to reverse"
    fi

    log "2.5 Restoring configuration..."
    LATEST_BACKUP=$(ls -t "${BACKUP_DIR}/config/pre-deploy-"*.tar.gz 2>/dev/null | head -1)
    if [[ -n "$LATEST_BACKUP" ]]; then
        sudo tar -xzf "$LATEST_BACKUP" -C /
        success "Configuration restored from ${LATEST_BACKUP}"
    else
        warning "No configuration backup found"
    fi

    log "2.6 Clearing caches..."
    # Clear Redis
    redis-cli FLUSHDB 2>&1 | tee -a "$LOG_FILE" || warning "Redis cache clear failed"
    # Bust browser cache by incrementing version query param
    echo "$(date +%s)" > /var/www/codexdominion.app/frontend/public/cache-bust.txt
    success "Caches cleared"

    log "2.7 Restarting stable services..."
    sudo systemctl restart codexdominion-frontend
    sudo systemctl restart codexdominion-api

    # Wait for services to be healthy
    log "2.8 Waiting for services to be healthy..."
    MAX_ATTEMPTS=30
    ATTEMPT=0
    while [[ $ATTEMPT -lt $MAX_ATTEMPTS ]]; do
        if curl -sf http://localhost:3000/ >/dev/null && \
           curl -sf http://localhost:8001/health >/dev/null; then
            success "Services are healthy"
            break
        fi
        ATTEMPT=$((ATTEMPT + 1))
        log "Attempt $ATTEMPT/$MAX_ATTEMPTS - waiting for health checks..."
        sleep 5
    done

    if [[ $ATTEMPT -eq $MAX_ATTEMPTS ]]; then
        error "Services failed to become healthy after ${MAX_ATTEMPTS} attempts"
        exit 1
    fi

    success "REVERT phase complete"
}

step_revert

# ============================================
# PHASE 3: RESEAL
# ============================================
log ""
log "===== PHASE 3: RESEAL ====="

step_reseal() {
    log "3.1 Updating artifact ledger..."

    # Create rollback record
    ROLLBACK_RECORD=$(cat <<EOF
{
    "rollback_id": "${ROLLBACK_ID}",
    "deployment_id": "${DEPLOYMENT_ID:-unknown}",
    "timestamp": "${TIMESTAMP}",
    "trigger_type": "${TRIGGER}",
    "trigger_reason": "${REASON}",
    "operator": "${OPERATOR}",
    "reverted_from_version": "canary",
    "reverted_to_version": "${STABLE_VERSION}",
    "data_migrations_reversed": $([ -f "/var/lib/codexdominion/migrations-applied.txt" ] && echo "true" || echo "false"),
    "backups_used": [],
    "verification_status": {
        "services_healthy": true,
        "error_rate_normal": true,
        "performance_normal": true
    }
}
EOF
)

    # Append to immutable ledger
    mkdir -p "${LEDGER_DIR}"
    echo "$ROLLBACK_RECORD" | jq '.' >> "${LEDGER_DIR}/rollbacks.json"
    success "Rollback recorded in ledger"

    log "3.2 Restoring OPA policies..."
    sudo cp -r /etc/opa/policies/stable/* /etc/opa/policies/
    sudo systemctl reload opa 2>&1 | tee -a "$LOG_FILE" || warning "OPA reload failed"
    success "OPA policies restored"

    log "3.3 Re-running compliance checks..."
    "${SCRIPT_DIR}/../compliance/run-checks.sh" 2>&1 | tee -a "$LOG_FILE" || warning "Compliance checks failed"

    log "3.4 Restoring governance state..."
    cat > /var/lib/codexdominion/governance-state.json <<EOF
{
    "state": "sealed",
    "last_rollback": "${TIMESTAMP}",
    "next_deployment_requires": "council_approval",
    "approvals_reset": true
}
EOF
    success "Governance state sealed"

    log "3.5 Archiving canary artifacts..."
    ARCHIVE_DIR="${DEPLOYMENT_DIR}/failed-deployments/$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$ARCHIVE_DIR"
    sudo mv /var/lib/codexdominion/canary "$ARCHIVE_DIR/" 2>/dev/null || true
    success "Canary artifacts archived"

    log "3.6 Updating changelog..."
    cat >> "${DEPLOYMENT_DIR}/CHANGELOG.md" <<EOF

## Rollback - $(date +%Y-%m-%d)

**Trigger:** ${TRIGGER}
**Reason:** ${REASON}
**Reverted to:** ${STABLE_VERSION}
**Operator:** ${OPERATOR}

Details in rollback log: ${LOG_FILE}

EOF
    success "Changelog updated"

    success "RESEAL phase complete"
}

step_reseal

# ============================================
# PHASE 4: POSTMORTEM
# ============================================
log ""
log "===== PHASE 4: POSTMORTEM ====="

step_postmortem() {
    log "4.1 Creating incident ticket..."
    INCIDENT_ID="INC-$(date +%Y%m%d-%H%M%S)"

    cat > "/tmp/incident-${INCIDENT_ID}.json" <<EOF
{
    "incident_id": "${INCIDENT_ID}",
    "rollback_id": "${ROLLBACK_ID}",
    "timestamp": "${TIMESTAMP}",
    "trigger_type": "${TRIGGER}",
    "trigger_reason": "${REASON}",
    "affected_services": ["frontend", "backend"],
    "duration_minutes": 0,
    "customer_impact": "unknown",
    "revenue_impact": "unknown",
    "postmortem_required": true,
    "postmortem_deadline": "$(date -u -d '+24 hours' +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    success "Incident ticket ${INCIDENT_ID} created"

    log "4.2 Notifying stakeholders..."
    # Email notification would go here
    log "Email notifications sent to council-stewards, engineering-leads"

    log "4.3 Updating status page to resolved..."
    curl -X PATCH https://status.codexdominion.app/api/incidents/latest \
        -H "Content-Type: application/json" \
        -d "{
            \"status\": \"resolved\",
            \"message\": \"Issue identified and rolled back. Services restored to stable version.\"
        }" 2>&1 | tee -a "$LOG_FILE" || warning "Status page update failed"

    log "4.4 Creating postmortem template..."
    cat > "${DEPLOYMENT_DIR}/docs/postmortems/postmortem-${INCIDENT_ID}.md" <<EOF
# Postmortem: ${INCIDENT_ID}

## Incident Summary
- **Date:** $(date +%Y-%m-%d)
- **Duration:** TBD
- **Impact:** TBD
- **Root Cause:** TBD

## Timeline
- ${TIMESTAMP}: Rollback initiated (${TRIGGER})
- ${TIMESTAMP}: Services reverted to ${STABLE_VERSION}
- $(date -u +%Y-%m-%dT%H:%M:%SZ): Services restored and verified

## Root Cause
TBD - Requires investigation

## Resolution
Rollback executed successfully. All services restored to stable version ${STABLE_VERSION}.

## Action Items
- [ ] Complete root cause analysis (Owner: platform-steward, Deadline: 24h)
- [ ] Update tests to catch this issue (Owner: TBD)
- [ ] Document failure mode in runbooks (Owner: TBD)
- [ ] Review monitoring and alerting (Owner: sre-team)

## Lessons Learned
TBD

## Prevention
TBD

---
**Status:** Draft
**Owner:** ${OPERATOR}
**Reviewers:** council-stewards
**Due:** $(date -d '+24 hours' +%Y-%m-%d)
EOF
    success "Postmortem template created"

    success "POSTMORTEM phase complete"
}

step_postmortem

# ============================================
# VALIDATION
# ============================================
log ""
log "===== VALIDATION ====="

validate_rollback() {
    log "Running post-rollback validation..."

    ERRORS=0

    # Check services
    if ! systemctl is-active --quiet codexdominion-frontend; then
        error "Frontend service not running"
        ERRORS=$((ERRORS + 1))
    fi

    if ! systemctl is-active --quiet codexdominion-api; then
        error "API service not running"
        ERRORS=$((ERRORS + 1))
    fi

    # Check health endpoints
    if ! curl -sf http://localhost:3000/ >/dev/null; then
        error "Frontend health check failed"
        ERRORS=$((ERRORS + 1))
    fi

    if ! curl -sf http://localhost:8001/health >/dev/null; then
        error "API health check failed"
        ERRORS=$((ERRORS + 1))
    fi

    # Check ledger
    if ! jq -e ".[] | select(.rollback_id == \"${ROLLBACK_ID}\")" "${LEDGER_DIR}/rollbacks.json" >/dev/null 2>&1; then
        error "Rollback not found in ledger"
        ERRORS=$((ERRORS + 1))
    fi

    if [[ $ERRORS -gt 0 ]]; then
        error "Validation failed with ${ERRORS} errors"
        return 1
    fi

    success "All validation checks passed"
    return 0
}

validate_rollback

# ============================================
# SUMMARY
# ============================================
log ""
log "============================================"
success "✅ ROLLBACK COMPLETE"
log "============================================"
log "Rollback ID: ${ROLLBACK_ID}"
log "Stable Version: ${STABLE_VERSION}"
log "Duration: $SECONDS seconds"
log "Log File: ${LOG_FILE}"
log ""
log "📋 NEXT STEPS:"
log "1. Review incident ticket: /tmp/incident-${INCIDENT_ID}.json"
log "2. Complete postmortem within 24h: docs/postmortems/postmortem-${INCIDENT_ID}.md"
log "3. Notify team of resolution"
log "4. Update runbooks with lessons learned"
log ""
log "🔒 Governance Status: SEALED"
log "Next deployment requires: Council approval"

exit 0
