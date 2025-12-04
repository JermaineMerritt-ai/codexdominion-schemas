#!/bin/bash
# secrets-scan.sh - Scans for secrets, API keys, and credentials
# Part of Codex Dominion pre-commit hooks
# Exit code 0: No secrets found
# Exit code 1: Secrets detected

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "🔍 Scanning for secrets and credentials..."

# Patterns to detect secrets
SECRET_PATTERNS=(
    "password\s*=\s*['\"][^'\"]+['\"]"
    "api[_-]?key\s*=\s*['\"][^'\"]+['\"]"
    "secret\s*=\s*['\"][^'\"]+['\"]"
    "token\s*=\s*['\"][^'\"]+['\"]"
    "bearer\s+[A-Za-z0-9\-._~+/]+=*"
    "authorization:\s*['\"][^'\"]+['\"]"
    "aws_access_key_id\s*=\s*['\"][^'\"]+['\"]"
    "aws_secret_access_key\s*=\s*['\"][^'\"]+['\"]"
    "AKIA[0-9A-Z]{16}"  # AWS Access Key
    "AIza[0-9A-Za-z\\-_]{35}"  # Google API Key
    "sk-[A-Za-z0-9]{48}"  # OpenAI API Key
    "ghp_[A-Za-z0-9]{36}"  # GitHub Personal Access Token
    "gho_[A-Za-z0-9]{36}"  # GitHub OAuth Token
    "ghs_[A-Za-z0-9]{36}"  # GitHub Server Token
    "xoxb-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24}"  # Slack Bot Token
    "xoxp-[0-9]{10,13}-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{32}"  # Slack User Token
)

# Directories to exclude
EXCLUDE_DIRS=(
    "node_modules"
    ".venv"
    ".git"
    ".next"
    "dist"
    "build"
    "coverage"
    ".pytest_cache"
    "__pycache__"
    "ledger"  # Ledger may contain encrypted secrets
)

# Files to exclude
EXCLUDE_FILES=(
    "*.lock"
    "package-lock.json"
    "yarn.lock"
    "pnpm-lock.yaml"
    "*.min.js"
    "*.min.css"
    ".env.example"
    ".env.template"
)

# Build exclude arguments for grep
EXCLUDE_ARGS=""
for dir in "${EXCLUDE_DIRS[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude-dir=$dir"
done
for file in "${EXCLUDE_FILES[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$file"
done

# Scan for secrets
SECRETS_FOUND=0
for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -rniE $EXCLUDE_ARGS "$pattern" . 2>/dev/null | grep -v "secrets-scan.sh" | grep -v ".pre-commit-config.yaml"; then
        SECRETS_FOUND=1
    fi
done

# Check for .env files (should not be committed)
if find . -name ".env" -not -path "*/node_modules/*" -not -path "*/.venv/*" | grep -q .; then
    echo -e "${RED}❌ .env files detected (should be in .gitignore):${NC}"
    find . -name ".env" -not -path "*/node_modules/*" -not -path "*/.venv/*"
    SECRETS_FOUND=1
fi

# Check for private key files
if find . \( -name "*.pem" -o -name "*.key" -o -name "*_rsa" -o -name "*.p12" -o -name "*.pfx" \) \
    -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/certs/*" | grep -q .; then
    echo -e "${RED}❌ Private key files detected:${NC}"
    find . \( -name "*.pem" -o -name "*.key" -o -name "*_rsa" -o -name "*.p12" -o -name "*.pfx" \) \
        -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/certs/*"
    SECRETS_FOUND=1
fi

# Check for hardcoded IPs (potential security issue)
if grep -rniE $EXCLUDE_ARGS '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' . 2>/dev/null | \
    grep -v "127.0.0.1" | grep -v "0.0.0.0" | grep -v "localhost" | grep -v "secrets-scan.sh" | grep -q .; then
    echo -e "${YELLOW}⚠️  Hardcoded IP addresses detected (review for security):${NC}"
    grep -rniE $EXCLUDE_ARGS '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' . 2>/dev/null | \
        grep -v "127.0.0.1" | grep -v "0.0.0.0" | grep -v "localhost" | grep -v "secrets-scan.sh" | head -5
fi

if [ $SECRETS_FOUND -eq 1 ]; then
    echo -e "${RED}❌ Secrets or credentials detected in code!${NC}"
    echo -e "${YELLOW}ACTION REQUIRED:${NC}"
    echo "1. Remove secrets from code"
    echo "2. Use environment variables (.env files)"
    echo "3. Add sensitive files to .gitignore"
    echo "4. Rotate any exposed credentials"
    echo "5. Use secrets management (Azure Key Vault, AWS Secrets Manager)"
    exit 1
fi

echo -e "${GREEN}✅ No secrets detected${NC}"
exit 0
