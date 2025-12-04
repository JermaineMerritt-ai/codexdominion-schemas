#!/usr/bin/env bash
# Risk Tier Assessment Script
# Classifies changes based on intent, files changed, and risk keywords

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Get commit message and changed files
COMMIT_MSG=$(git log -1 --pretty=%B)
CHANGED_FILES=$(git diff --name-only HEAD~1..HEAD 2>/dev/null || echo "")

# High risk keywords
HIGH_RISK_KEYWORDS=(
  "avatar" "AI model" "autonomous agent" "multi-agent"
  "GDPR" "compliance" "consent" "PII" "personal data" "cross-border"
  "authentication" "authorization" "RBAC" "permissions" "IAM"
  "encryption" "secrets" "cryptography" "key rotation"
  "data migration" "schema breaking" "drop table" "alter table"
  "architecture" "microservice" "API contract" "breaking change"
  "payment" "billing" "transaction" "financial"
)

# Medium risk keywords
MEDIUM_RISK_KEYWORDS=(
  "feature" "integration" "API endpoint" "REST API"
  "database schema" "new table" "migration" "column"
  "feature flag" "configuration" "environment"
  "UI change" "user flow" "navigation" "routing"
  "dependency" "upgrade" "update"
)

# Low risk keywords
LOW_RISK_KEYWORDS=(
  "documentation" "README" "comment" "docs"
  "test" "unit test" "integration test" "e2e"
  "performance" "optimization" "caching" "query"
  "refactor" "formatting" "linting" "style"
  "fix typo" "update comment"
)

# High risk file patterns
HIGH_RISK_FILES=(
  "**/auth/**"
  "**/avatar/**"
  "**/compliance/**"
  "**/encryption/**"
  "**/payment/**"
  "**/*.rego"
  "**/policies/**"
  "**/consent-envelopes/**"
  "**/*migration*.sql"
  "**/*schema*.sql"
)

# Medium risk file patterns
MEDIUM_RISK_FILES=(
  "**/api/**"
  "**/routes/**"
  "**/pages/**"
  "**/components/**"
  "**/*config*"
  "package.json"
  "requirements.txt"
  "**/*.env*"
)

# Low risk file patterns
LOW_RISK_FILES=(
  "**/*.md"
  "**/*.test.*"
  "**/*.spec.*"
  "docs/**"
  "**/*.example"
)

# Function to check if text contains any keywords
contains_keyword() {
  local text="$1"
  shift
  local keywords=("$@")

  for keyword in "${keywords[@]}"; do
    if echo "$text" | grep -qi "$keyword"; then
      return 0
    fi
  done
  return 1
}

# Function to check if files match patterns
matches_pattern() {
  local files="$1"
  shift
  local patterns=("$@")

  for pattern in "${patterns[@]}"; do
    if echo "$files" | grep -q "$pattern"; then
      return 0
    fi
  done
  return 1
}

# Assess risk tier
RISK_TIER="LOW"

# Check commit message and changed files for HIGH risk
if contains_keyword "$COMMIT_MSG" "${HIGH_RISK_KEYWORDS[@]}" || \
   matches_pattern "$CHANGED_FILES" "${HIGH_RISK_FILES[@]}"; then
  RISK_TIER="HIGH"
elif contains_keyword "$COMMIT_MSG" "${MEDIUM_RISK_KEYWORDS[@]}" || \
     matches_pattern "$CHANGED_FILES" "${MEDIUM_RISK_FILES[@]}"; then
  RISK_TIER="MEDIUM"
fi

# Override if only low-risk files changed
if matches_pattern "$CHANGED_FILES" "${LOW_RISK_FILES[@]}" && \
   ! matches_pattern "$CHANGED_FILES" "${MEDIUM_RISK_FILES[@]}" && \
   ! matches_pattern "$CHANGED_FILES" "${HIGH_RISK_FILES[@]}"; then
  RISK_TIER="LOW"
fi

# Output risk tier
case $RISK_TIER in
  HIGH)
    echo -e "${RED}[RISK TIER] HIGH${NC}" >&2
    echo "HIGH"
    ;;
  MEDIUM)
    echo -e "${YELLOW}[RISK TIER] MEDIUM${NC}" >&2
    echo "MEDIUM"
    ;;
  LOW)
    echo -e "${GREEN}[RISK TIER] LOW${NC}" >&2
    echo "LOW"
    ;;
esac

exit 0
