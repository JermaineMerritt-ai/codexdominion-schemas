#!/bin/bash
# adr-validate.sh - Validates ADR format and required sections
# Part of Codex Dominion pre-commit hooks

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

ADR_FILE="$1"

echo "📋 Validating ADR: $(basename "$ADR_FILE")"

# Required sections in ADR
REQUIRED_SECTIONS=(
    "# ADR-"
    "## Status"
    "## Context"
    "## Decision"
    "## Consequences"
    "## Decision Drivers"
    "## Options Considered"
    "## Compliance"
    "## Performance"
    "## Cost"
)

MISSING_SECTIONS=()

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "^$section" "$ADR_FILE"; then
        MISSING_SECTIONS+=("$section")
    fi
done

if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
    echo -e "${RED}❌ ADR validation failed: Missing required sections${NC}"
    for section in "${MISSING_SECTIONS[@]}"; do
        echo "   - $section"
    done
    echo ""
    echo "ADR must include all required sections per template."
    exit 1
fi

# Validate status is one of: Proposed, Accepted, Deprecated, Superseded
if ! grep -E "^## Status\s*$" -A 1 "$ADR_FILE" | grep -qE "(Proposed|Accepted|Deprecated|Superseded)"; then
    echo -e "${YELLOW}⚠️  Status should be: Proposed, Accepted, Deprecated, or Superseded${NC}"
fi

# Validate ADR number format
if ! grep -qE "^# ADR-[0-9]{3}:" "$ADR_FILE"; then
    echo -e "${YELLOW}⚠️  ADR title should follow format: # ADR-XXX: Title${NC}"
fi

# Validate Caribbean jurisdiction if compliance section exists
if grep -q "^## Compliance" "$ADR_FILE" && ! grep -qiE "(trinidad|tobago|caribbean|caricom)" "$ADR_FILE"; then
    echo -e "${YELLOW}⚠️  Compliance section should specify Caribbean jurisdiction${NC}"
fi

echo -e "${GREEN}✅ ADR validation passed${NC}"
exit 0
