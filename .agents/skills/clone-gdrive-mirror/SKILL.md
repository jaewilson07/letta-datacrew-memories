---
name: clone-gdrive-mirror
description: >
  Recursively clone a Google Drive folder tree into the local markdown mirror
  (one .md per doc tab, with baselines + images). Use for: "clone the customers
  drive", "refresh the client mirror", "sync gdrive folder to markdown", "add a
  drive folder to the mirror".
metadata:
  version: 1.0.0
  updated: 2026-07-18
---

# clone-gdrive-mirror

## Overview

Materializes a Google Drive folder tree as a local markdown mirror. For every
Google Doc under the configured folder it writes `<client>/<document>/<tab>.md`
with `sync:` frontmatter, persists embedded images to `assets/`, and stores a
`.sync/` baseline for the future 3-way merge. It's a thin, config-driven runner
over cboti's `mirror.clone_tree`; the conversion/walk engine lives in cboti,
while the customer-specific folder ids and destinations live here (private).

The clone is **one-way** (Drive → local) and **incremental** — documents
unchanged by Drive `modifiedTime` are skipped, so re-running only re-fetches
what changed.

## Core Capabilities

- **Recursive walk** — every Google Doc under a folder, at any nesting depth.
- **Faithful conversion** — bold/italic/strike/headings/lists/tables/links via cboti's structural converter.
- **Image persistence** — embedded images downloaded to `assets/`, links rewritten to relative paths.
- **Stable identity** — `sync:` frontmatter (`document_id`, `tab_id`, `base_revision`, `base_sha256`, `source_modified`, …) maps each file back to Drive across renames.
- **Incremental & resumable** — unchanged docs skipped; a failed doc is isolated and reported, the rest continue.

## When to Use

- First-time population of the client mirror from Drive.
- Refreshing the mirror after docs change in Drive (cheap — only changed docs re-fetch).
- Adding a new Drive folder tree to the mirror (add a `sources` entry).

## Quick Start

Credentials (`GDOC_CLIENT`, `GDOC_TOKEN`) come from Infisical `/datacrew`. Run
from the monorepo root under `infisical run`, using cboti's environment:

```bash
infisical run --domain=https://infisical.datacrew.space \
  --projectId=3fbb4296-d4e6-4c17-83ee-b852a57a5e50 --env=prod --path=/datacrew -- \
  uv run --project libraries/cboti python \
  datacrew-private-memories/.agents/skills/clone-gdrive-mirror/scripts/run_clone.py
```

Typical output:

```text
=== datacrew-customers → …/agents/datacrew/clients ===
Discovered 59 document(s) under 17_UlOsQpyniJvypl2rSGW6vEjNd80fDy
  = skip (unchanged): Cricut/Cricut — Outreach Dossier
  + cloned: Bissell/Bissell — Outreach Dossier
Done: 3 cloned, 56 skipped, 0 failed
```

Flags: `--force` re-clones everything; `--only <name>` clones one configured
source; `--config <path>` uses a different config.

## Detailed Workflow

### Step 1: Configure sources

Edit `config.yaml`. Each `sources` entry needs `name`, `folder_id` (the Drive
folder), and `dest` (relative to this repo's root, e.g.
`agents/datacrew/clients`).

### Step 2: Run the clone

Use the Quick Start command. Each doc is walked, converted, image-localized, and
written with frontmatter + a `.sync/` shadow baseline.

### Step 3: Review & commit

Inspect the diff, then commit the mirror to this (private) repo. Re-runs are
incremental, so routine refreshes produce small diffs. A JSON report of what was
cloned/skipped/failed is written to `EXPORTS/clone-report.json` (gitignored).

### Step 4: Handle failures

Any doc that errors is listed under `failed` and does not stop the run — fix the
cause (usually access/scope) and re-run; only the failed docs re-fetch.

## References

- `config.yaml` — the Drive folder(s) and destinations to mirror.
- `scripts/run_clone.py` — the runner (loads config → `mirror.clone_tree` → report).
- `cboti.integrations.google.drive.mirror` — the walk/clone engine (in the cboti library).
- `validate-gdoc-conversion` (cboti) — guards the converter this clone relies on.

## Related Skills

- `upsert-gdoc` — write markdown back into a Google Doc (the eventual sync write-path).
- `pattern-hunter` — produces client dossiers that land in this mirror.
