#!/bin/bash
# Sauvegarde quotidienne pendant vacances
DATE=$(date +%Y%m%d)
BACKUP_DIR="vacation_backups"
mkdir -p "$BACKUP_DIR"

echo "💾 Sauvegarde quotidienne $(date)"

# Sauvegarde code critique
tar -czf "$BACKUP_DIR/paninifs_$DATE.tar.gz" \
    --exclude="*.log" \
    --exclude="vacation_backups" \
    --exclude=".git" \
    .

# Sauvegarde issues GitHub
gh issue list --limit 100 --json number,title,body,state > "$BACKUP_DIR/github_issues_$DATE.json"

# Push vers GitHub
git add vacation_backups/
git commit -m "🏖️ Vacation backup $DATE" || true
git push origin master || true

echo "✅ Sauvegarde $DATE terminée"
