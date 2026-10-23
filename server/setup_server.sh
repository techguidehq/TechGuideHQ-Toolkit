#!/usr/bin/env bash
if [ "$EUID" -ne 0 ]; then
  echo "[X] Run as root: sudo bash setup_server.sh"
  exit 1
fi
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 21115:21119/tcp comment 'AnyDesk / RustDesk'
ufw --force enable
echo "[✓] UFW firewall configured successfully."
