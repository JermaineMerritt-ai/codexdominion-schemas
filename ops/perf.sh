#!/usr/bin/env bash
# Codex Dominion - Performance Testing Script
# Validates performance against governance thresholds (p95 <= 300ms)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8001}"
REPORT_DIR="./reports/performance"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Governance thresholds
P50_THRESHOLD=100   # ms
P95_THRESHOLD=300   # ms - GOVERNANCE THRESHOLD
P99_THRESHOLD=500   # ms
ERROR_RATE_THRESHOLD=1.0  # percent

# Counters
PASSED=0
FAILED=0
WARNINGS=0

log() {
    echo -e "${BLUE}[PERF]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
    PASSED=$((PASSED + 1))
}

error() {
    echo -e "${RED}✗${NC} $1"
    FAILED=$((FAILED + 1))
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

# Setup
mkdir -p "$REPORT_DIR"

echo ""
echo "============================================"
echo "   CODEX DOMINION - PERFORMANCE TEST"
echo "============================================"
echo ""

# Check dependencies
if ! command -v ab >/dev/null 2>&1; then
    warning "Apache Bench (ab) not installed"
    log "Install with: sudo apt-get install apache2-utils"
fi

if ! command -v curl >/dev/null 2>&1; then
    error "curl not installed"
    exit 1
fi

# Endpoints to test
declare -A ENDPOINTS=(
    ["Homepage"]="$FRONTEND_URL/"
    ["Capsules"]="$FRONTEND_URL/capsules"
    ["Signals"]="$FRONTEND_URL/signals"
    ["API Health"]="$BACKEND_URL/health"
    ["API Status"]="$BACKEND_URL/api/v1/status"
)

# Simple performance test with curl
test_endpoint_simple() {
    local name=$1
    local url=$2
    local iterations=10

    log "Testing ${name} (${iterations} requests)..."

    local times=()
    local errors=0

    for ((i=1; i<=iterations; i++)); do
        if time_ms=$(curl -o /dev/null -s -w '%{time_total}' --max-time 10 "$url" 2>/dev/null | awk '{print int($1 * 1000)}'); then
            times+=("$time_ms")
        else
            errors=$((errors + 1))
        fi
    done

    if [[ ${#times[@]} -eq 0 ]]; then
        error "${name}: All requests failed"
        return 1
    fi

    # Calculate percentiles
    IFS=$'\n' sorted=($(sort -n <<<"${times[*]}"))
    unset IFS

    local p50_idx=$(( ${#sorted[@]} * 50 / 100 ))
    local p95_idx=$(( ${#sorted[@]} * 95 / 100 ))
    local p99_idx=$(( ${#sorted[@]} * 99 / 100 ))

    local p50=${sorted[$p50_idx]}
    local p95=${sorted[$p95_idx]}
    local p99=${sorted[$p99_idx]}

    local error_rate=$(awk "BEGIN {printf \"%.1f\", ($errors / $iterations) * 100}")

    echo "  p50: ${p50}ms"
    echo "  p95: ${p95}ms"
    echo "  p99: ${p99}ms"
    echo "  Error rate: ${error_rate}%"

    # Check against thresholds
    local status="PASS"

    if (( $(echo "$p95 > $P95_THRESHOLD" | bc -l) )); then
        error "${name}: p95 (${p95}ms) exceeds governance threshold (${P95_THRESHOLD}ms)"
        status="FAIL"
    elif (( $(echo "$p95 > $(($P95_THRESHOLD * 90 / 100))" | bc -l) )); then
        warning "${name}: p95 (${p95}ms) approaching threshold (${P95_THRESHOLD}ms)"
        status="WARN"
    else
        success "${name}: p95 (${p95}ms) within threshold (${P95_THRESHOLD}ms)"
    fi

    if (( $(echo "$error_rate > $ERROR_RATE_THRESHOLD" | bc -l) )); then
        error "${name}: Error rate (${error_rate}%) exceeds threshold (${ERROR_RATE_THRESHOLD}%)"
        status="FAIL"
    fi

    # Store results
    echo "${name},${p50},${p95},${p99},${error_rate},${status}" >> "${REPORT_DIR}/results-${TIMESTAMP}.csv"

    echo ""

    [[ "$status" != "FAIL" ]]
}

# Load test with Apache Bench (if available)
load_test_endpoint() {
    local name=$1
    local url=$2
    local requests=100
    local concurrency=10

    if ! command -v ab >/dev/null 2>&1; then
        return 0
    fi

    log "Load testing ${name} (${requests} requests, ${concurrency} concurrent)..."

    local ab_output="${REPORT_DIR}/ab-${name//[^a-zA-Z0-9]/_}-${TIMESTAMP}.txt"

    if ab -n "$requests" -c "$concurrency" -g "${ab_output}.tsv" "$url" > "$ab_output" 2>&1; then
        # Parse results
        local mean_time=$(grep "Time per request:" "$ab_output" | head -1 | awk '{print $4}')
        local p50=$(grep "50%" "$ab_output" | awk '{print $2}')
        local p95=$(grep "95%" "$ab_output" | awk '{print $2}')
        local p99=$(grep "99%" "$ab_output" | awk '{print $2}')
        local failed=$(grep "Failed requests:" "$ab_output" | awk '{print $3}')

        echo "  Mean: ${mean_time}ms"
        echo "  50%: ${p50}ms"
        echo "  95%: ${p95}ms"
        echo "  99%: ${p99}ms"
        echo "  Failed: ${failed} requests"

        if (( $(echo "$p95 > $P95_THRESHOLD" | bc -l) )); then
            warning "${name}: Load test p95 (${p95}ms) exceeds threshold under load"
        else
            success "${name}: Load test passed"
        fi
    else
        warning "${name}: Load test failed"
    fi

    echo ""
}

# Initialize CSV
echo "Endpoint,p50(ms),p95(ms),p99(ms),Error Rate(%),Status" > "${REPORT_DIR}/results-${TIMESTAMP}.csv"

# Run tests
for endpoint_name in "${!ENDPOINTS[@]}"; do
    test_endpoint_simple "$endpoint_name" "${ENDPOINTS[$endpoint_name]}"
done

# Load tests (optional)
if command -v ab >/dev/null 2>&1; then
    log "Running load tests..."
    echo ""
    for endpoint_name in "${!ENDPOINTS[@]}"; do
        load_test_endpoint "$endpoint_name" "${ENDPOINTS[$endpoint_name]}"
    done
fi

# Generate HTML report
log "Generating performance report..."
REPORT_HTML="${REPORT_DIR}/performance-report-${TIMESTAMP}.html"

cat > "$REPORT_HTML" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Report - Codex Dominion</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
        h1 { color: #1a1a1a; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
        .card { padding: 1.5rem; border-radius: 8px; background: #f5f5f5; }
        .card.pass { background: #efe; border-left: 4px solid #0a0; }
        .card.warn { background: #ffc; border-left: 4px solid #f90; }
        .card.fail { background: #fee; border-left: 4px solid #c00; }
        .number { font-size: 2rem; font-weight: bold; margin: 0; }
        .label { color: #666; font-size: 0.9rem; }
        table { width: 100%; border-collapse: collapse; margin: 2rem 0; }
        th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid #ddd; }
        th { background: #f5f5f5; font-weight: 600; }
        .pass { color: #0a0; font-weight: 600; }
        .warn { color: #f90; font-weight: 600; }
        .fail { color: #c00; font-weight: 600; }
        .threshold { background: #fff3cd; padding: 1rem; border-left: 4px solid #856404; margin: 1rem 0; }
        footer { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #ddd; color: #666; font-size: 0.9rem; }
    </style>
</head>
<body>
    <h1>Performance Report</h1>
    <p>Generated: $(date)</p>

    <div class="threshold">
        <strong>Governance Thresholds:</strong><br>
        p50: ≤ ${P50_THRESHOLD}ms | <strong>p95: ≤ ${P95_THRESHOLD}ms</strong> | p99: ≤ ${P99_THRESHOLD}ms | Error Rate: < ${ERROR_RATE_THRESHOLD}%
    </div>

    <div class="summary">
        <div class="card pass">
            <p class="number">$PASSED</p>
            <p class="label">Endpoints Passed</p>
        </div>
        <div class="card warn">
            <p class="number">$WARNINGS</p>
            <p class="label">Warnings</p>
        </div>
        <div class="card fail">
            <p class="number">$FAILED</p>
            <p class="label">Failed</p>
        </div>
    </div>

    <h2>Results</h2>
    <table>
        <thead>
            <tr>
                <th>Endpoint</th>
                <th>p50</th>
                <th>p95</th>
                <th>p99</th>
                <th>Error Rate</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
EOF

while IFS=, read -r endpoint p50 p95 p99 error_rate status; do
    if [[ "$endpoint" != "Endpoint" ]]; then
        echo "<tr><td>${endpoint}</td><td>${p50}ms</td><td><strong>${p95}ms</strong></td><td>${p99}ms</td><td>${error_rate}%</td><td class='${status,,}'>${status}</td></tr>" >> "$REPORT_HTML"
    fi
done < "${REPORT_DIR}/results-${TIMESTAMP}.csv"

cat >> "$REPORT_HTML" <<EOF
        </tbody>
    </table>

    <h2>Performance Recommendations</h2>
    <ul>
        <li>Monitor p95 latency continuously - governance threshold is 300ms</li>
        <li>Investigate any endpoints approaching thresholds</li>
        <li>Use caching for frequently accessed data</li>
        <li>Optimize database queries with EXPLAIN ANALYZE</li>
        <li>Consider CDN for static assets</li>
        <li>Enable HTTP/2 and compression</li>
        <li>Review slow endpoints in APM tool</li>
    </ul>

    <footer>
        <p>Codex Dominion - Performance Report</p>
        <p>CSV Data: <a href="results-${TIMESTAMP}.csv">results-${TIMESTAMP}.csv</a></p>
    </footer>
</body>
</html>
EOF

success "HTML report generated: ${REPORT_HTML}"

# Summary
echo ""
echo "============================================"
echo "        PERFORMANCE TEST SUMMARY"
echo "============================================"
echo -e "${GREEN}Passed:${NC}   $PASSED endpoints"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS endpoints"
echo -e "${RED}Failed:${NC}   $FAILED endpoints"
echo ""
echo "Governance Threshold: p95 ≤ ${P95_THRESHOLD}ms"
echo "Full report: ${REPORT_HTML}"
echo ""

if [[ $FAILED -gt 0 ]]; then
    echo -e "${RED}Performance test FAILED - governance thresholds violated${NC}"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}Performance test PASSED with warnings${NC}"
    exit 0
else
    echo -e "${GREEN}Performance test PASSED${NC}"
    exit 0
fi
