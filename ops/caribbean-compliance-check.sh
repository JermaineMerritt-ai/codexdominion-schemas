#!/bin/bash
# caribbean-compliance-check.sh - Validates Caribbean jurisdiction requirements
# Part of Codex Dominion pre-commit hooks

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "🌴 Checking Caribbean compliance requirements..."

VIOLATIONS=0

# Check for PII processing without consent envelope references
PII_FILES=$(git diff --cached --name-only | grep -E '\.(ts|tsx|js|jsx|py)$' || true)

for file in $PII_FILES; do
    if git diff --cached "$file" | grep -qiE '(email|phone|ssn|passport|address|identity|biometric|financial)' && \
       ! git diff --cached "$file" | grep -qiE '(consent|consent_envelope|has_consent)'; then
        echo -e "${YELLOW}⚠️  $file: Potential PII processing without consent check${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

# Check for cross-border data transfer without encryption
for file in $PII_FILES; do
    if git diff --cached "$file" | grep -qiE '(api\..*\.(com|net|org)|https?://[^/]*\.(com|net|org))' && \
       ! git diff --cached "$file" | grep -qiE '(encrypt|tls|ssl|https)'; then
        echo -e "${YELLOW}⚠️  $file: Cross-border transfer should use encryption${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

# Check for data retention without policy reference
for file in $PII_FILES; do
    if git diff --cached "$file" | grep -qiE '(store|save|persist|database|db\.)' && \
       git diff --cached "$file" | grep -qiE '(email|phone|identity|personal)' && \
       ! git diff --cached "$file" | grep -qiE '(retention|expire|delete|purge)'; then
        echo -e "${YELLOW}⚠️  $file: Data storage should specify retention policy${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

# Check for consent envelopes have proper jurisdiction
CONSENT_FILES=$(git diff --cached --name-only | grep -E 'consent.*\.json$' || true)
for file in $CONSENT_FILES; do
    if [ -f "$file" ]; then
        if ! grep -qiE '(caribbean|trinidad|tobago|caricom)' "$file"; then
            echo -e "${RED}❌ $file: Consent envelope must specify Caribbean jurisdiction${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
        if ! grep -qE '"retention"' "$file"; then
            echo -e "${RED}❌ $file: Consent envelope must specify retention policy${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
        if ! grep -qE '"revocation"' "$file"; then
            echo -e "${RED}❌ $file: Consent envelope must specify revocation mechanism${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

# Check OPA policies reference Caribbean compliance
OPA_FILES=$(git diff --cached --name-only | grep -E '\.rego$' || true)
for file in $OPA_FILES; do
    if git diff --cached "$file" | grep -qiE '(pii|personal|data|privacy)' && \
       ! git diff --cached "$file" | grep -qiE '(caribbean|caricom)'; then
        echo -e "${YELLOW}⚠️  $file: Data policies should reference Caribbean compliance${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

if [ $VIOLATIONS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $VIOLATIONS Caribbean compliance warnings detected${NC}"
    echo "   Review changes for GDPR/CARICOM requirements"
    echo "   This is a warning only - commit will proceed"
fi

echo -e "${GREEN}✅ Caribbean compliance check complete${NC}"
exit 0
