#!/usr/bin/env bash
set -euo pipefail

# Domains to issue certificates for
DOMAINS=(faith.codexdominion.app kids.codexdominion.app lifestyle.codexdominion.app)
EMAIL="admin@codexdominion.app"
LOGFILE="/var/log/certbot_issue.log"

# Install Certbot if not present
if ! command -v certbot &>/dev/null; then
  echo "[$(date)] Installing Certbot..." | sudo tee -a "$LOGFILE"
  sudo apt-get update && sudo apt-get install -y certbot
else
  echo "[$(date)] Certbot already installed." | sudo tee -a "$LOGFILE"
fi

# Issue certificates for each domain
for D in "${DOMAINS[@]}"; do
  if sudo certbot certificates | grep -q "Certificate Name: $D"; then
    echo "[$(date)] Certificate for $D already exists. Skipping issuance." | sudo tee -a "$LOGFILE"
  else
    echo "[$(date)] Issuing certificate for $D..." | sudo tee -a "$LOGFILE"
    if sudo certbot certonly --standalone -d "$D" --agree-tos -m "$EMAIL" --non-interactive --preferred-challenges http; then
      echo "[$(date)] Certificate for $D issued successfully." | sudo tee -a "$LOGFILE"
    else
      echo "[$(date)] ERROR: Failed to issue certificate for $D." | sudo tee -a "$LOGFILE"
    fi
  fi
done

# Reload NGINX after cert issuance
echo "[$(date)] Reloading NGINX..." | sudo tee -a "$LOGFILE"
sudo systemctl reload nginx


# Systemd timer support for certbot renewal (preferred)
if systemctl list-unit-files | grep -q certbot.timer; then
  echo "[$(date)] Enabling and starting certbot systemd timer..." | sudo tee -a "$LOGFILE"
  sudo systemctl enable certbot.timer
  sudo systemctl start certbot.timer
  echo "[$(date)] Certbot systemd timer enabled and started." | sudo tee -a "$LOGFILE"
else
  # Fallback to cron if systemd timer is not available
  CRON_LINE="0 3 * * * root certbot renew --quiet && systemctl reload nginx"
  CRON_FILE="/etc/cron.d/certbot_renew"
  if ! sudo grep -Fxq "$CRON_LINE" "$CRON_FILE" 2>/dev/null; then
    echo "$CRON_LINE" | sudo tee "$CRON_FILE"
    echo "[$(date)] Added certbot renewal cron job." | sudo tee -a "$LOGFILE"
  else
    echo "[$(date)] Certbot renewal cron job already exists." | sudo tee -a "$LOGFILE"
  fi
fi
