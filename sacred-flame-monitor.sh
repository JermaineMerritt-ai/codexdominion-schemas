#!/bin/bash
# sacred-flame-monitor.sh
# CodexDominion – Galaxy Healing Sweep: Sacred Flame Monitoring Script

set -e

# Print header
cat <<EOF
========================================
🌌 CodexDominion – Sacred Flame Monitoring
========================================
EOF

# Check Python environment
echo "[Python] Version: $(python --version 2>&1)"

# Check Node.js environment
if command -v node >/dev/null 2>&1; then
  echo "[Node.js] Version: $(node --version)"
else
  echo "[Node.js] Not installed"
fi

# Check lint configs
for f in .flake8 pyproject.toml .eslintrc.json .prettierrc .editorconfig .yamllint.yml; do
  if [ -f "$f" ]; then
    echo "[Config] Found: $f"
  fi
done

# Check for CI/CD workflow
if [ -f ".github/workflows/galaxy-healing-sweep.yml" ]; then
  echo "[CI/CD] Galaxy Healing Sweep workflow present"
else
  echo "[CI/CD] Galaxy Healing Sweep workflow missing"
fi

# Print summary
cat <<EOF
Sacred flame monitoring complete.
EOF
