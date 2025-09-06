#!/usr/bin/env bash
set -euo pipefail

labels=(
  "documentation::Documentation related changes"
  "status:triage::New item pending triage"
)

repos=(
  "stephanedenis/PaniniFS-AutonomousMissions"
  "stephanedenis/PaniniFS-SemanticCore"
  "stephanedenis/PaniniFS-PublicationEngine"
  "stephanedenis/PaniniFS-UltraReactive"
  "stephanedenis/PaniniFS-ExecutionOrchestrator"
  "stephanedenis/PaniniFS-DatasetsIngestion"
  "stephanedenis/PaniniFS-AttributionRegistry"
  "stephanedenis/OntoWave"
  "stephanedenis/PaniniFS-CopilotageShared"
)

for r in "${repos[@]}"; do
  echo "[repo] $r"
  for l in "${labels[@]}"; do
    name=${l%%::*}
    desc=${l#*::}
    gh label create "$name" -R "$r" -d "$desc" -c "#cccccc" || echo "[skip] $name"
  done
done
