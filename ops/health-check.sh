#!/usr/bin/env bash
# Codex Dominion - Health Check Script
# Validates all services are operational and meet governance thresholds

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
TIMEOUT=5

# Counters
PASSED=0
FAILED=0
WARNINGS=0

log() {
    echo -e "${BLUE}[HEALTH]${NC} $1"
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

check_service() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}

    log "Checking ${name}..."

    if response=$(curl -s -w "\n%{http_code}" --max-time "$TIMEOUT" "$url" 2>/dev/null); then
        status=$(echo "$response" | tail -n1)
        body=$(echo "$response" | sed '$d')

        if [[ "$status" == "$expected_status" ]]; then
            success "${name} responding (HTTP ${status})"
            echo "$body" | jq '.' 2>/dev/null || true
            return 0
        else
            error "${name} returned HTTP ${status}, expected ${expected_status}"
            return 1
        fi
    else
        error "${name} not responding at ${url}"
        return 1
    fi
}

check_performance() {
    local name=$1
    local url=$2
    local threshold_ms=${3:-300}  # Governance p95 threshold

    log "Measuring ${name} response time..."

    if time_ms=$(curl -o /dev/null -s -w '%{time_total}' --max-time "$TIMEOUT" "$url" 2>/dev/null | awk '{print int($1 * 1000)}'); then
        if [[ $time_ms -le $threshold_ms ]]; then
            success "${name} response time: ${time_ms}ms (threshold: ${threshold_ms}ms)"
            return 0
        else
            warning "${name} response time: ${time_ms}ms exceeds threshold ${threshold_ms}ms"
            return 1
        fi
    else
        error "${name} performance check failed"
        return 1
    fi
}

check_systemd_service() {
    local service=$1

    log "Checking systemd service: ${service}..."

    if systemctl is-active --quiet "$service" 2>/dev/null; then
        success "${service} is active"
        return 0
    else
        error "${service} is not active"
        systemctl status "$service" --no-pager || true
        return 1
    fi
}

check_database() {
    log "Checking database connectivity..."

    if command -v psql >/dev/null 2>&1; then
        if psql -h localhost -U codexdominion -d codexdominion -c "SELECT 1;" >/dev/null 2>&1; then
            success "Database connected"
            return 0
        else
            error "Database connection failed"
            return 1
        fi
    else
        warning "psql not available, skipping database check"
        return 1
    fi
}

check_disk_space() {
    log "Checking disk space..."

    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

    if [[ $usage -lt 80 ]]; then
        success "Disk usage: ${usage}%"
        return 0
    elif [[ $usage -lt 90 ]]; then
        warning "Disk usage: ${usage}% (approaching limit)"
        return 1
    else
        error "Disk usage: ${usage}% (critical)"
        return 1
    fi
}

check_memory() {
    log "Checking memory usage..."

    if command -v free >/dev/null 2>&1; then
        local usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')

        if [[ $usage -lt 80 ]]; then
            success "Memory usage: ${usage}%"
            return 0
        elif [[ $usage -lt 90 ]]; then
            warning "Memory usage: ${usage}% (high)"
            return 1
        else
            error "Memory usage: ${usage}% (critical)"
            return 1
        fi
    else
        warning "Memory check not available"
        return 1
    fi
}

check_ssl_certificate() {
    local domain=${1:-codexdominion.app}

    log "Checking SSL certificate for ${domain}..."

    if command -v openssl >/dev/null 2>&1; then
        if expiry=$(echo | openssl s_client -servername "$domain" -connect "${domain}:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2); then
            expiry_epoch=$(date -d "$expiry" +%s)
            now_epoch=$(date +%s)
            days_remaining=$(( (expiry_epoch - now_epoch) / 86400 ))

            if [[ $days_remaining -gt 30 ]]; then
                success "SSL certificate valid for ${days_remaining} days"
                return 0
            elif [[ $days_remaining -gt 7 ]]; then
                warning "SSL certificate expires in ${days_remaining} days"
                return 1
            else
                error "SSL certificate expires in ${days_remaining} days"
                return 1
            fi
        else
            warning "Could not check SSL certificate for ${domain}"
            return 1
        fi
    else
        warning "openssl not available, skipping SSL check"
        return 1
    fi
}

echo ""
echo "============================================"
echo "    CODEX DOMINION - HEALTH CHECK"
echo "============================================"
echo ""

# Frontend checks
check_service "Frontend Homepage" "$FRONTEND_URL" 200
check_service "Frontend API Route" "$FRONTEND_URL/api/health" 200
check_performance "Frontend" "$FRONTEND_URL" 300

# Backend checks
check_service "Backend Health" "$BACKEND_URL/health" 200
check_service "Backend API" "$BACKEND_URL/api/v1/status" 200
check_performance "Backend API" "$BACKEND_URL/health" 300

# Systemd services (if available)
if command -v systemctl >/dev/null 2>&1; then
    check_systemd_service "codexdominion-frontend" || true
    check_systemd_service "codexdominion-api" || true
    check_systemd_service "nginx" || true
fi

# Database
check_database || true

# System resources
check_disk_space
check_memory

# SSL certificate (production only)
if [[ "${ENVIRONMENT:-development}" == "production" ]]; then
    check_ssl_certificate "codexdominion.app" || true
fi

# Summary
echo ""
echo "============================================"
echo "             HEALTH CHECK SUMMARY"
echo "============================================"
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC}   $FAILED"
echo ""

if [[ $FAILED -gt 0 ]]; then
    echo -e "${RED}Health check FAILED${NC}"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}Health check PASSED with warnings${NC}"
    exit 0
else
    echo -e "${GREEN}Health check PASSED${NC}"
    exit 0
fi
