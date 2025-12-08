#!/bin/bash
# Codex Dominion Frontend Startup Script

export NODE_ENV=production
export PORT=3000
export HOSTNAME=0.0.0.0

cd /var/www/codexdominion
node server.js
