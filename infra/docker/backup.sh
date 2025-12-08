#!/bin/bash
# Backup Script for CodexDominion

BACKUP_DIR="/var/backups/codexdominion"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="codex_backup_$DATE.tar.gz"

mkdir -p $BACKUP_DIR

echo "Starting backup at $(date)"

# Stop services for consistent backup
echo "Stopping services..."
docker-compose stop

# Backup database
echo "Backing up database..."
docker-compose exec -T db mysqldump -u root -p"$DB_ROOT_PASSWORD" --all-databases > $BACKUP_DIR/db_$DATE.sql

# Backup volumes
echo "Backing up volumes..."
docker run --rm \
    -v $(pwd):/source \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/$BACKUP_FILE \
    /source/data \
    /source/wp-content \
    /source/.env \
    /source/docker-compose.yml \
    /source/nginx

# Backup SSL certificates
echo "Backing up SSL certificates..."
tar czf $BACKUP_DIR/ssl_$DATE.tar.gz /etc/letsencrypt

# Restart services
echo "Restarting services..."
docker-compose start

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "codex_backup_*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "ssl_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/$BACKUP_FILE"
echo "Backup size: $(du -h $BACKUP_DIR/$BACKUP_FILE | cut -f1)"
