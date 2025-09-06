# Editorial Sync Policy

This repository keeps “rich sources” under `RESEARCH/…` and exposes publication-ready mirrors at the repository root for convenience (Medium and Leanpub).

- Source of truth: `RESEARCH/publications/...`
- Root files are mirrors with a provenance banner. Do not edit root mirrors.
- Final placeholders (`*_FINAL_*`) indicate editorial state and export status.

## Manual sync (temporary)

Until automation is added, mirrors are updated by PRs that copy from sources and add a `SYNC` banner with date and branch.

## Planned automation

- A script `Copilotage/scripts/editorial/sync_publications.py` will:
  - Validate that sources exist and are non-empty
  - Copy content to root mirrors with a provenance header
  - Update FINAL placeholders when flagged via `--final`
  - Add a small changelog to `Copilotage/journal`

## Provenance banner

Each mirrored file starts with:

`<!-- SYNC: Source=<path>; Date=<YYYY-MM-DD>; Branch=<branch>. Edit the source, not this file. -->`

## Contacts

Open an issue with label `editorial` for any sync request or mismatch.
