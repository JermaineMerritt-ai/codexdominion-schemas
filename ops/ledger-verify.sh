#!/bin/bash
# ledger-verify.sh - Validates artifact ledger integrity
# Part of Codex Dominion pre-commit hooks

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "📜 Verifying artifact ledger integrity..."

LEDGER_DIR="ledger"

if [ ! -d "$LEDGER_DIR" ]; then
    echo -e "${GREEN}✅ No ledger directory (skipping)${NC}"
    exit 0
fi

VIOLATIONS=0

# Check for required ledger structure
REQUIRED_DIRS=(
    "ledger/artifacts"
    "ledger/approvals"
    "ledger/lineage"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ] && [ ! -f "$dir/.gitkeep" ]; then
        if [ -z "$(ls -A "$dir")" ]; then
            echo -e "${YELLOW}⚠️  $dir is empty but tracked${NC}"
        fi
    fi
done

# Validate JSON files in ledger
find "$LEDGER_DIR" -name "*.json" -type f | while read -r file; do
    if ! jq empty "$file" 2>/dev/null; then
        echo -e "${RED}❌ Invalid JSON: $file${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi

    # Check for required fields in approval files
    if echo "$file" | grep -q "approvals"; then
        if ! jq -e '.artifact_id and .risk_tier and .approved_by and .timestamp' "$file" >/dev/null 2>&1; then
            echo -e "${RED}❌ Missing required fields in approval: $file${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi

    # Check for required fields in artifact files
    if echo "$file" | grep -q "artifacts"; then
        if ! jq -e '.artifact_id and .commit_sha and .timestamp and .risk_tier' "$file" >/dev/null 2>&1; then
            echo -e "${RED}❌ Missing required fields in artifact: $file${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

# Check for SHA-256 hash files
find "$LEDGER_DIR/artifacts" -name "*.json" -type f | while read -r file; do
    ARTIFACT_ID=$(jq -r '.artifact_id' "$file" 2>/dev/null || echo "")
    if [ -n "$ARTIFACT_ID" ]; then
        HASH_FILE="$LEDGER_DIR/artifacts/$ARTIFACT_ID.sha256"
        if [ ! -f "$HASH_FILE" ]; then
            echo -e "${YELLOW}⚠️  Missing SHA-256 hash for artifact: $ARTIFACT_ID${NC}"
        fi
    fi
done

if [ $VIOLATIONS -gt 0 ]; then
    echo -e "${RED}❌ Ledger integrity check failed with $VIOLATIONS violations${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Ledger integrity verified${NC}"
exit 0
