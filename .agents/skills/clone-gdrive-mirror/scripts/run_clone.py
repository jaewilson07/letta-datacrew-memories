#!/usr/bin/env python3
"""Clone the configured Google Drive folder tree(s) into the local markdown mirror.

Thin runner over cboti ``mirror.clone_tree``: reads config.yaml, clones each
source recursively, and prints a per-source report. Incremental — documents
unchanged by Drive ``modifiedTime`` are skipped, so re-running is cheap.

Run (GDOC_CLIENT / GDOC_TOKEN come from Infisical /datacrew):

    infisical run --domain=https://infisical.datacrew.space \\
      --projectId=3fbb4296-d4e6-4c17-83ee-b852a57a5e50 --env=prod --path=/datacrew -- \\
      uv run --project libraries/cboti python \\
      datacrew-private-memories/.agents/skills/clone-gdrive-mirror/scripts/run_clone.py

Exit code 0 = success; 1 = one or more documents failed.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[4]          # datacrew-private-memories/
MONOREPO_ROOT = _HERE.parents[5]      # simpleDiscordBot/
SKILL_DIR = _HERE.parents[1]

# env_loader lives at <repo>/.agents/; cboti source is in the monorepo.
sys.path.insert(0, str(_HERE.parents[3]))
_CBOTI_SRC = MONOREPO_ROOT / "libraries" / "cboti" / "src"
if _CBOTI_SRC.exists():
    sys.path.insert(0, str(_CBOTI_SRC))

from env_loader import require_env  # noqa: E402

from cboti.integrations.google.drive import mirror  # noqa: E402
from cboti.integrations.google.drive.service import GoogleDriveService  # noqa: E402

DEFAULT_CONFIG = SKILL_DIR / "config.yaml"
DEFAULT_REPORT = SKILL_DIR / "EXPORTS" / "clone-report.json"


def _resolve_dest(dest: str) -> Path:
    path = Path(dest)
    return path if path.is_absolute() else REPO_ROOT / path


async def run(config_path: Path, report_path: Path | None, force: bool, only: str | None) -> int:
    require_env("GDOC_CLIENT", "GDOC_TOKEN")
    config = yaml.safe_load(config_path.read_text())
    sources = config.get("sources") or []
    if only:
        sources = [s for s in sources if s.get("name") == only]
    if not sources:
        print("No matching sources in", config_path)
        return 1

    svc = GoogleDriveService()
    results = []
    any_failed = False
    for src in sources:
        name = src.get("name", src["folder_id"])
        dest = _resolve_dest(src["dest"])
        print(f"\n=== {name} → {dest} ===")
        report = await mirror.clone_tree(svc, src["folder_id"], dest, force=force)
        any_failed = any_failed or bool(report.failed)
        results.append({
            "name": name,
            "folder_id": src["folder_id"],
            "dest": str(dest),
            "cloned": report.cloned,
            "skipped": report.skipped,
            "failed": report.failed,
        })

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(results, indent=2))
        print(f"\nReport written to {report_path}")

    return 1 if any_failed else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--force", action="store_true", help="Re-clone even unchanged docs.")
    parser.add_argument("--only", help="Clone just the named source from config.")
    parser.add_argument(
        "--report", type=Path, default=DEFAULT_REPORT,
        help="Where to write the JSON report (under EXPORTS/, gitignored). Pass '' to skip.",
    )
    args = parser.parse_args()
    report = args.report if str(args.report) else None
    raise SystemExit(asyncio.run(run(args.config, report, args.force, args.only)))


if __name__ == "__main__":
    main()
