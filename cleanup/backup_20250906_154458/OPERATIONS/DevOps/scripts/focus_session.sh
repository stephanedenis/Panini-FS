#!/bin/bash
# 🦉 TOTORO FOCUS SESSION SCRIPT
# Usage: ./focus_session.sh

echo "🦉 STARTING TOTORO FOCUS SESSION"
echo "================================"

# 1. System cleanup
echo "🧹 System cleanup..."
sync
find /tmp -user $(whoami) -type f -atime +1 -delete 2>/dev/null || true
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# 2. Memory status
echo "📊 Memory status:"
free -h

# 3. Focus reminders
echo ""
echo "📝 FOCUS CHECKLIST:"
echo "□ VSCode: Fermer fichiers non-essentiels"
echo "□ Firefox: Garder seulement Colab + GitHub"
echo "□ Désactiver: CodeQL, Remote Dev, Docker"
echo "□ Garder: Copilot, Python, Rust Analyzer"
echo ""
echo "🚀 Ready for CLOUD ACCELERATION!"
echo "   → https://colab.research.google.com/"
