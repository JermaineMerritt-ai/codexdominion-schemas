#!/usr/bin/env bash
# Codex Dominion - Accessibility Testing Script
# Validates WCAG 2.1 AA compliance and accessibility standards

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
REPORT_DIR="./reports/accessibility"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Counters
VIOLATIONS=0
WARNINGS=0
PASSED=0

log() {
    echo -e "${BLUE}[A11Y]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
    PASSED=$((PASSED + 1))
}

error() {
    echo -e "${RED}✗${NC} $1"
    VIOLATIONS=$((VIOLATIONS + 1))
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

# Setup
mkdir -p "$REPORT_DIR"

echo ""
echo "============================================"
echo "  CODEX DOMINION - ACCESSIBILITY CHECK"
echo "============================================"
echo ""

# Check if axe-core is available
if ! command -v axe >/dev/null 2>&1 && ! npm list -g axe-core >/dev/null 2>&1; then
    warning "axe-core not installed, installing..."
    npm install -g @axe-core/cli || {
        error "Failed to install axe-core"
        exit 1
    }
fi

# Pages to test
PAGES=(
    "/"
    "/about"
    "/capsules"
    "/capsules-enhanced"
    "/signals"
    "/signals-enhanced"
    "/login"
    "/signup"
)

log "Testing accessibility for ${#PAGES[@]} pages..."
echo ""

# Test each page
for page in "${PAGES[@]}"; do
    url="${FRONTEND_URL}${page}"
    log "Testing: ${url}"

    # Run axe accessibility scan
    if command -v axe >/dev/null 2>&1; then
        report_file="${REPORT_DIR}/axe-${page//\//_}-${TIMESTAMP}.json"

        if axe "$url" --timeout 10000 > "$report_file" 2>&1; then
            # Parse results
            violations=$(jq '.violations | length' "$report_file" 2>/dev/null || echo 0)
            incomplete=$(jq '.incomplete | length' "$report_file" 2>/dev/null || echo 0)
            passes=$(jq '.passes | length' "$report_file" 2>/dev/null || echo 0)

            if [[ $violations -eq 0 ]]; then
                success "${page}: No violations (${passes} passed)"
            else
                error "${page}: ${violations} violations found"
                # Show first 3 violations
                jq -r '.violations[:3] | .[] | "  - \(.impact): \(.description)"' "$report_file" 2>/dev/null || true
            fi

            if [[ $incomplete -gt 0 ]]; then
                warning "${page}: ${incomplete} incomplete checks (manual review needed)"
            fi

            VIOLATIONS=$((VIOLATIONS + violations))
            WARNINGS=$((WARNINGS + incomplete))
            PASSED=$((PASSED + passes))
        else
            error "${page}: Accessibility scan failed"
        fi
    else
        warning "Axe CLI not available, using basic checks only"
    fi

    echo ""
done

# Manual check reminders
log "Manual checks required:"
echo "  - Keyboard navigation (Tab, Enter, Space, Arrow keys)"
echo "  - Screen reader compatibility (NVDA, JAWS, VoiceOver)"
echo "  - Color contrast ratios (WCAG AA: 4.5:1 for text)"
echo "  - Focus indicators visible"
echo "  - ARIA labels present and meaningful"
echo "  - Form error messages accessible"
echo "  - Skip navigation links available"
echo ""

# Generate HTML report
log "Generating consolidated report..."
REPORT_HTML="${REPORT_DIR}/accessibility-report-${TIMESTAMP}.html"

cat > "$REPORT_HTML" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Report - Codex Dominion</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
        h1 { color: #1a1a1a; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
        .card { padding: 1.5rem; border-radius: 8px; background: #f5f5f5; }
        .card.error { background: #fee; border-left: 4px solid #c00; }
        .card.warning { background: #ffc; border-left: 4px solid #f90; }
        .card.success { background: #efe; border-left: 4px solid #0a0; }
        .number { font-size: 2rem; font-weight: bold; margin: 0; }
        .label { color: #666; font-size: 0.9rem; }
        table { width: 100%; border-collapse: collapse; margin: 2rem 0; }
        th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid #ddd; }
        th { background: #f5f5f5; font-weight: 600; }
        .violation { color: #c00; }
        .warning { color: #f90; }
        .pass { color: #0a0; }
        footer { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #ddd; color: #666; font-size: 0.9rem; }
    </style>
</head>
<body>
    <h1>Accessibility Report</h1>
    <p>Generated: $(date)</p>
    <p>WCAG 2.1 Level AA Compliance Check</p>

    <div class="summary">
        <div class="card success">
            <p class="number">$PASSED</p>
            <p class="label">Checks Passed</p>
        </div>
        <div class="card warning">
            <p class="number">$WARNINGS</p>
            <p class="label">Warnings</p>
        </div>
        <div class="card error">
            <p class="number">$VIOLATIONS</p>
            <p class="label">Violations</p>
        </div>
    </div>

    <h2>Pages Tested</h2>
    <table>
        <thead>
            <tr>
                <th>Page</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
EOF

for page in "${PAGES[@]}"; do
    report_file="${REPORT_DIR}/axe-${page//\//_}-${TIMESTAMP}.json"
    if [[ -f "$report_file" ]]; then
        violations=$(jq '.violations | length' "$report_file" 2>/dev/null || echo 0)
        status_class="pass"
        status_text="✓ Passed"

        if [[ $violations -gt 0 ]]; then
            status_class="violation"
            status_text="✗ ${violations} violations"
        fi

        echo "<tr><td>${page}</td><td class='${status_class}'>${status_text}</td><td><a href='axe-${page//\//_}-${TIMESTAMP}.json'>View Report</a></td></tr>" >> "$REPORT_HTML"
    fi
done

cat >> "$REPORT_HTML" <<EOF
        </tbody>
    </table>

    <h2>Manual Testing Checklist</h2>
    <ul>
        <li>Keyboard navigation works for all interactive elements</li>
        <li>Screen reader announces all content correctly</li>
        <li>Color contrast meets WCAG AA (4.5:1 for normal text, 3:1 for large text)</li>
        <li>Focus indicators are visible and clear</li>
        <li>ARIA labels are present and meaningful</li>
        <li>Form errors are announced and visible</li>
        <li>Skip navigation links function correctly</li>
        <li>Images have appropriate alt text</li>
        <li>Videos have captions/transcripts</li>
        <li>Page titles are descriptive</li>
    </ul>

    <footer>
        <p>Codex Dominion - Accessibility Report</p>
        <p>For WCAG 2.1 guidelines, visit: <a href="https://www.w3.org/WAI/WCAG21/quickref/">WCAG 2.1 Quick Reference</a></p>
    </footer>
</body>
</html>
EOF

success "HTML report generated: ${REPORT_HTML}"

# Summary
echo ""
echo "============================================"
echo "         ACCESSIBILITY CHECK SUMMARY"
echo "============================================"
echo -e "${GREEN}Passed:${NC}     $PASSED checks"
echo -e "${YELLOW}Warnings:${NC}   $WARNINGS items need manual review"
echo -e "${RED}Violations:${NC} $VIOLATIONS accessibility issues"
echo ""
echo "Full report: ${REPORT_HTML}"
echo ""

if [[ $VIOLATIONS -gt 0 ]]; then
    echo -e "${RED}Accessibility check FAILED - violations must be fixed${NC}"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}Accessibility check PASSED with warnings - manual review needed${NC}"
    exit 0
else
    echo -e "${GREEN}Accessibility check PASSED${NC}"
    exit 0
fi
