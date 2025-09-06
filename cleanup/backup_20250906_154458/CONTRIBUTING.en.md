# Contributing — Copilotage

This repository uses the Copilotage workflow (issue → branch → PR → journal).

Read first:
- Copilotage/COPILOTAGE_WORKFLOW.md
- Copilotage/README.md
- Copilotage/AGENT_CONVENTION.md

Quick start
- Open an issue (templates provided)
- Create a branch via: `Copilotage/scripts/devops/gh_task_init.sh "[type] title" type slug`
- Short commits with refs: `Refs #<num>`
- Open a PR (template provided) and append your session journal under `Copilotage/journal/`

Agent ID and cross-check
- Include an agent ID in PR titles: `[agent:ID]` (e.g., `[agent:steph-laptop]`) or branch name `agents/ID/...`.
- A workflow auto-applies a `agent:<id>` label for cross-validation.

CI
- Keep it light (CodeQL + minimal CI). Aim for small, frequent PRs.

Please follow the “Camping” spirit: simplicity, low coupling, clear docs.

## Submodules — edited independently

Important: submodules are separate repositories, edited and versioned independently.

- Don’t modify files directly inside directories declared in `.gitmodules` (e.g., `modules/*`, `copilotage/shared`, `RESEARCH`). Any content change must go through a PR in the submodule repository.
- To propose a submodule change, open an issue here using the “Submodule change request” template, then open the mirrored issue in the submodule repo. This issue tracks cross-repo alignment from the monorepo perspective.
- After the submodule PR is merged, update the submodule pointer in this repo (submodule update commit), then open the aggregation PR here.
- Recommended labels: `target:submodule` + `submodule:<name>` and `type:submodule-change`.
- VS Code: work within the submodule’s own workspace (each submodule is a separate VS Code project/workspace). See `SUBMODULES_TEMPLATE/README.md` for practices (dedicated workspaces, Peacock color, local docs, minimal CI).

Guidance for AI Copilot agents:
- State explicitly the target of the change (monorepo vs submodule) in issue/PR titles and descriptions.
- If a submodule edit is needed, create the task in the target repo before any attempt to edit from this repo. Here, only commit the submodule pointer update.
- Plan a short “propagation path”: submodule PR → pointer update → CI/docs validations.

Indicative list of submodules (see `.gitmodules` for the up-to-date list):
- modules/autonomous-missions
- modules/semantic-core
- modules/publication-engine
- modules/ultra-reactive
- modules/execution-orchestrator
- modules/datasets-ingestion
- modules/attribution-registry
- modules/ontowave-app
- copilotage/shared
- RESEARCH

