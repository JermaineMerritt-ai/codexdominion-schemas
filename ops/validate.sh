#!/usr/bin/env bash
# Codex Dominion - Complete Validation Pipeline
# Runs health checks, accessibility tests, performance validation, and ledger append

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() {
    echo -e "${BLUE}[VALIDATE]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

banner() {
    echo ""
    echo -e "${MAGENTA}============================================${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}============================================${NC}"
    echo ""
}

banner "CODEX DOMINION - VALIDATION PIPELINE"

log "Starting validation pipeline at $(date)"
PIPELINE_START=$(date +%s)

# Track results
HEALTH_STATUS="unknown"
A11Y_STATUS="unknown"
PERF_STATUS="unknown"
OVERALL_STATUS="validated"

# Step 1: Health Check
banner "STEP 1/4: HEALTH CHECK"
if bash "${SCRIPT_DIR}/health-check.sh"; then
    success "Health check passed"
    HEALTH_STATUS="pass"
else
    error "Health check failed"
    HEALTH_STATUS="fail"
    OVERALL_STATUS="failed"
fi

# Step 2: Accessibility Check
banner "STEP 2/4: ACCESSIBILITY CHECK"
if bash "${SCRIPT_DIR}/a11y.sh"; then
    success "Accessibility check passed"
    A11Y_STATUS="pass"
else
    error "Accessibility check failed"
    A11Y_STATUS="fail"
    OVERALL_STATUS="failed"
fi

# Step 3: Performance Check
banner "STEP 3/4: PERFORMANCE CHECK"
if bash "${SCRIPT_DIR}/perf.sh"; then
    success "Performance check passed"
    PERF_STATUS="pass"
else
    error "Performance check failed"
    PERF_STATUS="fail"
    OVERALL_STATUS="failed"
fi

# Step 4: Ledger Append
banner "STEP 4/4: LEDGER APPEND"
if bash "${SCRIPT_DIR}/ledger-append.sh" \
    --status "$OVERALL_STATUS" \
    --health "$HEALTH_STATUS" \
    --a11y "$A11Y_STATUS" \
    --perf "$PERF_STATUS"; then
    success "Validation recorded in ledger"
else
    error "Failed to record in ledger"
fi

# Calculate duration
PIPELINE_END=$(date +%s)
DURATION=$((PIPELINE_END - PIPELINE_START))

# Final summary
banner "VALIDATION COMPLETE"

echo "Duration: ${DURATION}s"
echo ""
echo "Results:"
echo -e "  Health Check:      $([ "$HEALTH_STATUS" = "pass" ] && echo -e "${GREEN}✓ PASS${NC}" || echo -e "${RED}✗ FAIL${NC}")"
echo -e "  Accessibility:     $([ "$A11Y_STATUS" = "pass" ] && echo -e "${GREEN}✓ PASS${NC}" || echo -e "${RED}✗ FAIL${NC}")"
echo -e "  Performance:       $([ "$PERF_STATUS" = "pass" ] && echo -e "${GREEN}✓ PASS${NC}" || echo -e "${RED}✗ FAIL${NC}")"
echo ""
echo -e "Overall Status: $([ "$OVERALL_STATUS" = "validated" ] && echo -e "${GREEN}✓ VALIDATED${NC}" || echo -e "${RED}✗ FAILED${NC}")"
echo ""

if [[ "$OVERALL_STATUS" = "validated" ]]; then
    success "All validation checks passed - deployment approved"
    exit 0
else
    error "Validation failed - deployment blocked"
    exit 1
fi
