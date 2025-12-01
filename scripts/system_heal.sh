#!/bin/bash
# system_heal.sh - Healing sweep for Codex Dominion
set -e

# Print header
cat <<EOF
========================================
 Codex Dominion System Healing Sweep
========================================
EOF

# Python environment checks
if command -v pip &>/dev/null; then
    echo "[Python] Checking requirements..."
    pip check || echo "pip check failed"
    echo "[Python] Running Black formatter..."
    if command -v black &>/dev/null; then
        black . || echo "Black failed"
    fi
    echo "[Python] Running isort..."
    if command -v isort &>/dev/null; then
        isort . || echo "isort failed"
    fi
    echo "[Python] Running flake8..."
    if command -v flake8 &>/dev/null; then
        flake8 . || echo "flake8 failed"
    fi
fi

# Node.js environment checks
if command -v npm &>/dev/null; then
    echo "[Node.js] Installing dependencies..."
    npm install || echo "npm install failed"
    echo "[Node.js] Running audit fix..."
    npm audit fix || echo "npm audit fix failed"
    echo "[Node.js] Running ESLint..."
    if command -v eslint &>/dev/null; then
        eslint . --fix || echo "ESLint failed"
    fi
    echo "[Node.js] Running Prettier..."
    if command -v prettier &>/dev/null; then
        prettier --write . || echo "Prettier failed"
    fi
fi

# Shell script linting
if command -v shellcheck &>/dev/null; then
    echo "[Shell] Running shellcheck on all .sh files..."
    find . -name "*.sh" -exec shellcheck {} + || echo "Shellcheck failed"
fi

# YAML workflow validation
if command -v sort-yaml &>/dev/null; then
    echo "[YAML] Validating workflow YAML files..."
    find .github/workflows -name "*.yaml" -exec sort-yaml {} + || echo "sort-yaml failed"
fi

# Print onboarding instructions
if [ -f GUARDIAN_QUICKSTART.md ]; then
    echo "\n[Onboarding] Quickstart instructions:"
    head -20 GUARDIAN_QUICKSTART.md
fi

# Print environment health summary
echo "\n[Summary] Healing sweep complete. Please review any errors above."
