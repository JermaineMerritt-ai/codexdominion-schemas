#!/usr/bin/env bash
# Sovereign Sign-off Gate
# Enforces risk-tiered approval requirements per ADR-002

set -euo pipefail

RISK_TIER="$1"
ARTIFACT_ID="$2"
METRICS_FILE="${3:-canary-metrics.json}"
LEDGER_PATH="${4:-./ledger}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}[SIGN-OFF GATE] Starting approval validation for $RISK_TIER risk tier${NC}"

# Function to check approval requirements
check_approvals() {
  local tier="$1"
  local artifact_id="$2"

  case $tier in
    LOW)
      # Low risk: Auto-approve after CI green
      echo -e "${GREEN}[LOW RISK] Auto-approved after CI validation${NC}"

      # Record auto-approval in ledger
      cat > "$LEDGER_PATH/approvals/$artifact_id.json" <<EOF
{
  "artifact_id": "$artifact_id",
  "risk_tier": "LOW",
  "approval_type": "auto",
  "approved_by": "ci-system",
  "approved_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "steward_notified": true,
  "post_merge_review_due": "$(date -u -d '+24 hours' +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
      echo "APPROVED"
      return 0
      ;;

    MEDIUM)
      # Medium risk: Requires steward sign-off
      echo -e "${YELLOW}[MEDIUM RISK] Steward approval required${NC}"

      # Check for steward approval (GitHub PR approval)
      if [ -n "${GITHUB_TOKEN:-}" ]; then
        # In GitHub Actions, check PR approvals
        PR_NUMBER=$(gh pr view --json number -q .number 2>/dev/null || echo "")

        if [ -n "$PR_NUMBER" ]; then
          APPROVALS=$(gh pr view "$PR_NUMBER" --json reviews -q '[.reviews[] | select(.state=="APPROVED")] | length')

          if [ "$APPROVALS" -ge 1 ]; then
            echo -e "${GREEN}[MEDIUM RISK] Steward approval found ($APPROVALS approvals)${NC}"

            # Record steward approval
            STEWARD=$(gh pr view "$PR_NUMBER" --json reviews -q '[.reviews[] | select(.state=="APPROVED")] | .[0].author.login')
            cat > "$LEDGER_PATH/approvals/$artifact_id.json" <<EOF
{
  "artifact_id": "$artifact_id",
  "risk_tier": "MEDIUM",
  "approval_type": "steward",
  "approved_by": "$STEWARD",
  "approved_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "pr_number": $PR_NUMBER,
  "approval_count": $APPROVALS
}
EOF
            echo "APPROVED"
            return 0
          else
            echo -e "${RED}[MEDIUM RISK] No steward approvals found${NC}"
            echo "PENDING_STEWARD_APPROVAL"
            return 1
          fi
        else
          echo -e "${YELLOW}[MEDIUM RISK] No PR found, checking manual override${NC}"

          # Check for manual approval file (for non-PR workflows)
          if [ -f "$LEDGER_PATH/manual-approvals/$artifact_id.steward" ]; then
            echo -e "${GREEN}[MEDIUM RISK] Manual steward approval found${NC}"
            echo "APPROVED"
            return 0
          else
            echo -e "${RED}[MEDIUM RISK] No manual approval found${NC}"
            echo "PENDING_STEWARD_APPROVAL"
            return 1
          fi
        fi
      else
        # No GitHub token, check for manual approval
        if [ -f "$LEDGER_PATH/manual-approvals/$artifact_id.steward" ]; then
          echo -e "${GREEN}[MEDIUM RISK] Manual steward approval found${NC}"
          echo "APPROVED"
          return 0
        else
          echo -e "${RED}[MEDIUM RISK] No approval found${NC}"
          echo "PENDING_STEWARD_APPROVAL"
          return 1
        fi
      fi
      ;;

    HIGH)
      # High risk: Requires council multi-sign (2 of 3)
      echo -e "${RED}[HIGH RISK] Council multi-sign required (2 of 3)${NC}"

      # Check for council approvals
      COUNCIL_APPROVALS=0
      COUNCIL_ROLES=("engineering-manager" "security-lead" "compliance-officer")
      APPROVED_BY=()

      for role in "${COUNCIL_ROLES[@]}"; do
        if [ -f "$LEDGER_PATH/council-approvals/$artifact_id.$role" ]; then
          COUNCIL_APPROVALS=$((COUNCIL_APPROVALS + 1))
          APPROVED_BY+=("$role")
          echo -e "${GREEN}  ✓ $role approval found${NC}"
        else
          echo -e "${YELLOW}  ✗ $role approval pending${NC}"
        fi
      done

      if [ $COUNCIL_APPROVALS -ge 2 ]; then
        echo -e "${GREEN}[HIGH RISK] Council quorum reached ($COUNCIL_APPROVALS/3 approvals)${NC}"

        # Record council approval
        cat > "$LEDGER_PATH/approvals/$artifact_id.json" <<EOF
{
  "artifact_id": "$artifact_id",
  "risk_tier": "HIGH",
  "approval_type": "council_multi_sign",
  "approved_by": $(printf '%s\n' "${APPROVED_BY[@]}" | jq -R . | jq -s .),
  "approved_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "quorum": "2_of_3",
  "total_approvals": $COUNCIL_APPROVALS
}
EOF
        echo "APPROVED"
        return 0
      else
        echo -e "${RED}[HIGH RISK] Insufficient council approvals ($COUNCIL_APPROVALS/3, need 2)${NC}"
        echo "PENDING_COUNCIL_QUORUM"
        return 1
      fi
      ;;

    *)
      echo -e "${RED}[ERROR] Unknown risk tier: $tier${NC}"
      echo "ERROR_UNKNOWN_TIER"
      return 1
      ;;
  esac
}

# Validate canary metrics (for production deployments)
validate_canary_metrics() {
  if [ -f "$METRICS_FILE" ]; then
    echo -e "${GREEN}[CANARY] Validating canary metrics${NC}"

    ERROR_RATE=$(jq -r '.error_rate // 0' "$METRICS_FILE")
    LATENCY_P95=$(jq -r '.latency_p95 // 0' "$METRICS_FILE")
    HEALTH_CHECKS=$(jq -r '.health_check_failures // 0' "$METRICS_FILE")

    echo "  Error Rate: ${ERROR_RATE}%"
    echo "  Latency P95: ${LATENCY_P95}ms"
    echo "  Health Check Failures: $HEALTH_CHECKS"

    # Check thresholds based on risk tier
    case $RISK_TIER in
      LOW)
        MAX_ERROR_RATE=1.0
        MAX_LATENCY=500
        ;;
      MEDIUM)
        MAX_ERROR_RATE=0.5
        MAX_LATENCY=500
        ;;
      HIGH)
        MAX_ERROR_RATE=0.1
        MAX_LATENCY=400
        ;;
    esac

    if (( $(echo "$ERROR_RATE > $MAX_ERROR_RATE" | bc -l) )); then
      echo -e "${RED}[CANARY] Error rate exceeds threshold (${ERROR_RATE}% > ${MAX_ERROR_RATE}%)${NC}"
      return 1
    fi

    if (( $(echo "$LATENCY_P95 > $MAX_LATENCY" | bc -l) )); then
      echo -e "${RED}[CANARY] Latency exceeds threshold (${LATENCY_P95}ms > ${MAX_LATENCY}ms)${NC}"
      return 1
    fi

    if [ "$HEALTH_CHECKS" -gt 0 ]; then
      echo -e "${RED}[CANARY] Health check failures detected${NC}"
      return 1
    fi

    echo -e "${GREEN}[CANARY] Metrics validation passed${NC}"
  else
    echo -e "${YELLOW}[CANARY] No metrics file found, skipping validation${NC}"
  fi

  return 0
}

# Create ledger directories if needed
mkdir -p "$LEDGER_PATH/approvals"
mkdir -p "$LEDGER_PATH/manual-approvals"
mkdir -p "$LEDGER_PATH/council-approvals"

# Validate canary metrics first
if ! validate_canary_metrics; then
  echo "REJECTED_METRICS_FAILED"
  exit 1
fi

# Check approvals
check_approvals "$RISK_TIER" "$ARTIFACT_ID"
EXIT_CODE=$?

exit $EXIT_CODE
