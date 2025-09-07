#!/usr/bin/env bash
set -euo pipefail

# Configure GitHub labels for clear targeting, including submodules.
# Requirements:
# - gh CLI authenticated (gh auth status)
# - GITHUB_REPO env var set to "owner/repo" or run inside a cloned repo with origin.

repo="${GITHUB_REPO:-}"
if [[ -z "${repo}" ]]; then
	if origin_url=$(git config --get remote.origin.url); then
		# Extract owner/repo from SSH or HTTPS URLs
		if [[ "$origin_url" =~ github.com(:|/)([^/]+)/([^/.]+)(.git)?$ ]]; then
			repo="${BASH_REMATCH[2]}/${BASH_REMATCH[3]}"
		else
			echo "Unable to derive owner/repo from origin URL: $origin_url" >&2
			exit 1
		fi
	else
		echo "Set GITHUB_REPO=owner/repo or run in a git repo with remote.origin" >&2
		exit 1
	fi
fi

echo "Using repo: $repo"

create_label() {
	local name="$1"; shift
	local color="$1"; shift
	local desc="$*"
	if gh label view "$name" -R "$repo" >/dev/null 2>&1; then
		gh label edit "$name" -R "$repo" --color "$color" --description "$desc" || true
	else
		gh label create "$name" -R "$repo" --color "$color" --description "$desc" || true
	fi
}

# Targeting labels
create_label "target:monorepo" "0e8a16" "Change lives in this monorepo"
create_label "target:submodule" "1d76db" "Change lives in a submodule (external repo)"

# Type labels
create_label "type:submodule-change" "c2e0c6" "Request to change a submodule and update pointer here"

# Submodule-specific labels (examples; extend as needed)
create_label "submodule:autonomous-missions" "f9d0c4" "modules/autonomous-missions"
create_label "submodule:semantic-core" "f9d0c4" "modules/semantic-core"
create_label "submodule:publication-engine" "f9d0c4" "modules/publication-engine"
create_label "submodule:ultra-reactive" "f9d0c4" "modules/ultra-reactive"
create_label "submodule:execution-orchestrator" "f9d0c4" "modules/execution-orchestrator"
create_label "submodule:datasets-ingestion" "f9d0c4" "modules/datasets-ingestion"
create_label "submodule:attribution-registry" "f9d0c4" "modules/attribution-registry"
create_label "submodule:ontowave-app" "f9d0c4" "modules/ontowave-app"
create_label "submodule:copilotage-shared" "f9d0c4" "copilotage/shared"
create_label "submodule:research" "f9d0c4" "RESEARCH"

echo "Labels ensured."

