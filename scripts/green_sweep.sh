#!/usr/bin/env bash
set -euo pipefail

echo "=== Infinity Crown Green Sweep: START ==="

has() { command -v "$1" >/dev/null 2>&1; }

# 0) Best-effort tool install (skip on errors)
echo "--- Tool bootstrap (best effort) ---"
if has pip; then pip install --user yamllint pylint bandit safety black isort flake8 mdformat markdownlint-cli; fi
if has npm; then npm i -g prettier eslint markdownlint-cli || true; fi
if has apt-get; then sudo apt-get update && sudo apt-get install -y jq shellcheck || true; fi

# 1) YAML & Markdown first (syntax blockers)
echo "--- YAML validation ---"
if has yamllint; then yamllint . || { echo "YAML syntax errors detected"; exit 1; }; fi

echo "--- Markdown lint & format ---"
if has mdformat; then mdformat . || true; fi
if has markdownlint; then markdownlint "**/*.md" || true; fi

# 2) Shell scripts
echo "--- Shell checks ---"
shfiles=$(git ls-files '*.sh' || true)
if [ -n "$shfiles" ]; then
  if has shellcheck; then shellcheck $shfiles || true; fi
  for f in $shfiles; do chmod +x "$f" || true; done
fi

# 3) Node.js/JavaScript
echo "--- Node.js lint/format/test ---"
if has npm; then
  npm install || true
  if has npx; then
    npx eslint . --ext .js,.jsx,.ts,.tsx --fix || true
    npx prettier --write "**/*.{js,jsx,ts,tsx,json,yml,yaml,md,css,scss}" || true
  fi
  npm test --if-present || true
  npm audit fix || true
fi

# 4) Python
echo "--- Python format/lint/security/test ---"
pyfiles=$(git ls-files '*.py' || true)
if [ -n "$pyfiles" ]; then
  if [ -f requirements-dev.txt ] && has pip; then pip install -r requirements-dev.txt || true; fi
  if has black; then black . || true; fi
  if has isort; then isort . || true; fi
  if has flake8; then flake8 || true; fi
  if has pylint; then pylint $pyfiles || true; fi
  if has bandit; then bandit -r . || true; fi
  if has safety; then safety check || true; fi
  if has pytest; then pytest || true; fi
fi

# 5) Final whitespace/EOL hygiene
echo "--- Final hygiene ---"
git ls-files | xargs -I{} bash -c 'sed -i.bak -e "s/[ \t]*$//" "{}" && rm -f "{}".bak' || true

echo "=== Infinity Crown Green Sweep: COMPLETE ==="
echo "Next: review diffs, fix any blockers, commit and push."
