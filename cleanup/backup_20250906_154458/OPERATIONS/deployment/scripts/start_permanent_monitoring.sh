#!/bin/bash
cd /home/stephane/GitHub/PaniniFS-1
source venv_externalization/bin/activate

while true; do
    echo "🤖 $(date): Cycle monitoring autonome"
    python3 Copilotage/agents/simple_autonomous_orchestrator.py >> logs/permanent_monitoring.log 2>&1
    echo "⏰ Pause 30 minutes..."
    sleep 1800  # 30 minutes
done
