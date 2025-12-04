#!/bin/bash
# risk-tier-validation.sh - Validates changes match declared risk tier
# Part of Codex Dominion pre-commit hooks

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Read assessed risk tier from commit-risk-tier.sh
if [ -f ".git/COMMIT_RISK_TIER" ]; then
    RISK_TIER=$(cat .git/COMMIT_RISK_TIER)
else
    echo -e "${YELLOW}⚠️  Risk tier not assessed, skipping validation${NC}"
    exit 0
fi

echo "🔍 Validating $RISK_TIER risk tier changes..."

# Get changed files
CHANGED_FILES=$(git diff --cached --name-only)

# Validation rules based on risk tier
case "$RISK_TIER" in
    HIGH)
        # HIGH risk requires:
        # 1. ADR approval reference
        # 2. No direct changes to production configs
        # 3. Test coverage for critical paths

        if ! git diff --cached | grep -qiE 'ADR-[0-9]{3}'; then
            echo -e "${YELLOW}⚠️  HIGH risk change should reference ADR approval${NC}"
            echo "   Add 'Approved by ADR-XXX' to commit message"
        fi

        if echo "$CHANGED_FILES" | grep -qE '\.env\.production|production\.json|prod\.yaml'; then
            echo -e "${RED}❌ HIGH risk: Direct production config changes not allowed${NC}"
            echo "   Use deployment process with council approval"
            exit 1
        fi

        if echo "$CHANGED_FILES" | grep -qE '(auth|payment|encryption)' && ! echo "$CHANGED_FILES" | grep -qE 'test|spec'; then
            echo -e "${RED}❌ HIGH risk: Critical changes require corresponding tests${NC}"
            exit 1
        fi

        echo -e "${GREEN}✅ HIGH risk validation passed${NC}"
        ;;

    MEDIUM)
        # MEDIUM risk requires:
        # 1. Documentation updates for API changes
        # 2. Tests for new features

        if echo "$CHANGED_FILES" | grep -qE 'api|endpoint' && ! echo "$CHANGED_FILES" | grep -qE 'docs|README'; then
            echo -e "${YELLOW}⚠️  MEDIUM risk: API changes should include documentation updates${NC}"
        fi

        if echo "$CHANGED_FILES" | grep -qE 'src.*\.(ts|tsx|js|jsx|py)$' && ! echo "$CHANGED_FILES" | grep -qE 'test|spec'; then
            echo -e "${YELLOW}⚠️  MEDIUM risk: New features should include tests${NC}"
        fi

        echo -e "${GREEN}✅ MEDIUM risk validation passed${NC}"
        ;;

    LOW)
        # LOW risk: Minimal validation
        # 1. Documentation changes should not affect code

        if echo "$CHANGED_FILES" | grep -qE '\.md$' && echo "$CHANGED_FILES" | grep -qE '\.(ts|tsx|js|jsx|py)$'; then
            echo -e "${YELLOW}⚠️  LOW risk: Consider separating docs and code changes${NC}"
        fi

        echo -e "${GREEN}✅ LOW risk validation passed${NC}"
        ;;
esac

exit 0
