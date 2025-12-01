#!/bin/bash
# Codex Dominion Cleanup Scroll
# Purpose: Purge heavy folders before Docker builds

echo "🔥 Initiating Custodian’s Sweep..."

# Exclude transient and heavy folders
rm -rf recent_uploads/ \
       .terraform/ \
       node_modules/ \
       .venv/ \
       .mypy_cache/ \
       .next/ \
       coverage/ \
       __pycache__/ \
       ebooks/ \
       templates/

echo "✅ Sweep complete. Workspace purified."
