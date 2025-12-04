#!/bin/bash
# commit-risk-tier.sh - Assesses risk tier from commit message
# Part of Codex Dominion pre-commit hooks
# Writes risk tier to .git/COMMIT_RISK_TIER for validation

set -euo pipefail

COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Extract risk tier from commit message if specified
# Format: [LOW/MEDIUM/HIGH] or risk: LOW/MEDIUM/HIGH
DECLARED_TIER=""
if echo "$COMMIT_MSG" | grep -qiE '^\[?(LOW|MEDIUM|HIGH)\]?'; then
    DECLARED_TIER=$(echo "$COMMIT_MSG" | grep -oiE '^(LOW|MEDIUM|HIGH)' | tr '[:lower:]' '[:upper:]')
elif echo "$COMMIT_MSG" | grep -qiE 'risk:\s*(LOW|MEDIUM|HIGH)'; then
    DECLARED_TIER=$(echo "$COMMIT_MSG" | grep -oiE 'risk:\s*(LOW|MEDIUM|HIGH)' | sed 's/risk:\s*//i' | tr '[:lower:]' '[:upper:]')
fi

# Get changed files
CHANGED_FILES=$(git diff --cached --name-only)

# Assess risk tier based on changed files (using risk-tier.sh logic)
ASSESSED_TIER="LOW"

# HIGH risk patterns
if echo "$CHANGED_FILES" | grep -qE '(auth|payment|encryption|avatar|gdpr|consent|migration|security|policy|ledger)'; then
    ASSESSED_TIER="HIGH"
elif echo "$COMMIT_MSG" | grep -qiE '(BREAKING|avatar|AI model|GDPR|auth|encryption|payment|schema breaking|security vulnerability|data breach)'; then
    ASSESSED_TIER="HIGH"
# MEDIUM risk patterns
elif echo "$CHANGED_FILES" | grep -qE '(api|backend|database|integration|workflow)'; then
    ASSESSED_TIER="MEDIUM"
elif echo "$COMMIT_MSG" | grep -qiE '(feature|integration|API|endpoint|database schema|workflow)'; then
    ASSESSED_TIER="MEDIUM"
fi

# Store assessed tier
echo "$ASSESSED_TIER" > .git/COMMIT_RISK_TIER

# Validate declared tier matches assessed tier
if [ -n "$DECLARED_TIER" ]; then
    if [ "$DECLARED_TIER" != "$ASSESSED_TIER" ]; then
        echo -e "${YELLOW}⚠️  Risk Tier Mismatch:${NC}"
        echo "   Declared: $DECLARED_TIER"
        echo "   Assessed: $ASSESSED_TIER"
        echo ""
        echo "Changed files suggest $ASSESSED_TIER risk tier."
        echo "Update commit message or file changes."
        echo ""
        echo "Proceeding with assessed tier: $ASSESSED_TIER"
    else
        echo -e "${GREEN}✅ Risk tier: $ASSESSED_TIER${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  Risk tier assessed: $ASSESSED_TIER${NC}"
    echo "   (Add [LOW/MEDIUM/HIGH] to commit message to declare explicitly)"
fi

exit 0
