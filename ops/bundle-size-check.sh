#!/bin/bash
# bundle-size-check.sh - Validates bundle size is within budget
# Part of Codex Dominion pre-commit hooks

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "📦 Checking bundle size..."

# Bundle size budget (bytes)
MAX_BUNDLE_SIZE=512000  # 500KB

FRONTEND_DIR="frontend"
BUILD_DIR="$FRONTEND_DIR/.next"

if [ ! -d "$BUILD_DIR" ]; then
    echo -e "${YELLOW}⚠️  No build directory found, skipping bundle size check${NC}"
    exit 0
fi

# Find main bundle file
MAIN_BUNDLE=$(find "$BUILD_DIR/static" -name "main-*.js" 2>/dev/null | head -1)

if [ -z "$MAIN_BUNDLE" ]; then
    echo -e "${YELLOW}⚠️  Main bundle not found, skipping size check${NC}"
    exit 0
fi

BUNDLE_SIZE=$(stat -c%s "$MAIN_BUNDLE" 2>/dev/null || stat -f%z "$MAIN_BUNDLE" 2>/dev/null)
BUNDLE_SIZE_KB=$((BUNDLE_SIZE / 1024))
MAX_SIZE_KB=$((MAX_BUNDLE_SIZE / 1024))

echo "   Main bundle: ${BUNDLE_SIZE_KB}KB"
echo "   Budget: ${MAX_SIZE_KB}KB"

if [ "$BUNDLE_SIZE" -gt "$MAX_BUNDLE_SIZE" ]; then
    echo -e "${RED}❌ Bundle size exceeds budget!${NC}"
    echo "   Current: ${BUNDLE_SIZE_KB}KB"
    echo "   Budget: ${MAX_SIZE_KB}KB"
    echo "   Overage: $((BUNDLE_SIZE_KB - MAX_SIZE_KB))KB"
    echo ""
    echo "Reduce bundle size by:"
    echo "  1. Code splitting (dynamic imports)"
    echo "  2. Tree shaking (remove unused code)"
    echo "  3. Lazy loading components"
    echo "  4. Using smaller dependencies"
    exit 1
fi

# Check all chunks
echo ""
echo "📊 Bundle analysis:"
find "$BUILD_DIR/static" -name "*.js" -type f | while read -r file; do
    SIZE=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    SIZE_KB=$((SIZE / 1024))
    echo "   $(basename "$file"): ${SIZE_KB}KB"
done

echo -e "${GREEN}✅ Bundle size within budget${NC}"
exit 0
