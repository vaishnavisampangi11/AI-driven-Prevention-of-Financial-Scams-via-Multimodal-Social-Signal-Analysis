#!/bin/bash
set -e
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="$(dirname "$0")/../backups"
mkdir -p "$BACKUP_DIR"
pg_dump -U postgres -d scam_prevention > "$BACKUP_DIR/scam_prevention_$DATE.sql"
echo "Backup created: $BACKUP_DIR/scam_prevention_$DATE.sql"
