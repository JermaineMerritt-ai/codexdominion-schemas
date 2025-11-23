#!/bin/bash
set -euo pipefail

# Create ledger directory
mkdir -p .codex/ledger

# Run ESLint and save results
npx eslint . -f json > .codex/ledger/eslint.json || true

# Run Prettier check and save results
npx prettier -c . > .codex/ledger/prettier.txt || true

# Build project and capture errors
npm run build || echo "Build errors captured"

# Run Trivy scan and save results
trivy fs . --severity HIGH,CRITICAL --format json > .codex/ledger/trivy.json || true
