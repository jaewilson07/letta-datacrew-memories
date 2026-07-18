#!/usr/bin/env python3
"""Deterministic ratchet for quality drift over `.agents/skills/` and
`.agents/runbooks/`.

Wraps `npx @microsoft/vally-cli lint` (Microsoft's Vally eval platform — the
same engine behind github/awesome-copilot's nightly "Skill Quality Report")
and ratchets the result against a committed baseline, mirroring
scripts/check_naked_except.py. Fails only on an entry NEWLY joining the
failing set; entries already broken today are grandfathered in a baseline
file. Drain the baseline as entries are fixed; once empty, run --strict to
forbid all failures outright.

Both `.agents/skills/` and `.agents/runbooks/` hold the same SKILL.md-shaped
directories (see .agents/skills/review-agents-folder/SKILL.md's canonical
structure) and vally lint checks either one identically: frontmatter
validity, name-matches-directory, description length (<=1024 chars), file
length (<=500 lines), metadata value typing, and file references resolving
inside the entry's own directory. They're tracked as two SEPARATE ratchets
(separate baseline files, separate pre-commit hooks) because skills and
runbooks are different categories — skills are how agents/developers should
work, runbooks are human-operated procedures — and conflating their reports
would make it unclear which kind of thing broke.

Scope is THIS repo only. Nested sub-repos (alix, libraries/*, datacrew,
infrastructure/*, mdrag, cboti, crew-dcs, ...) are separate git repos with
their own .agents/{skills,runbooks} and .pre-commit-config.yaml; each needs
its own copy of this script + baselines (see
.agents/skills/scan-skill-quality/SKILL.md).

Usage:
    python3 scripts/check_skill_quality.py                              # skills, only new drift fails
    python3 scripts/check_skill_quality.py --path .agents/runbooks       # runbooks instead
    python3 scripts/check_skill_quality.py --strict                     # fail on ANY failing entry
    python3 scripts/check_skill_quality.py --json                       # machine-readable report
    python3 scripts/check_skill_quality.py --update-baseline            # seed/refresh the baseline

Exit codes:
  0 — clean (no failing entries outside the baseline)
  1 — violations found (new drift, or any in --strict)
  2 — usage / environment error (npx missing, unreadable baseline, etc.)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

# vally lint prints one header line per entry, e.g.:
#   ✅ create-skill (2/2 checks passed)
#   ❌ excalidraw-diagram (1/2 checks passed, 1 failed)
HEADER_RE = re.compile(r"^(✅|❌)\s+(\S+)\s+\(")

# Baseline filename + report label per `.agents/<category>/` directory name.
# Falls back to a generic `.{name}-quality-baseline.json` / "entry" for any
# other path passed via --path.
CATEGORY_BASELINE = {"skills": ".skill-quality-baseline.json", "runbooks": ".runbook-quality-baseline.json"}
CATEGORY_LABEL = {"skills": "skill", "runbooks": "runbook"}


def default_baseline_for(path: Path) -> Path:
    return REPO_ROOT / CATEGORY_BASELINE.get(path.name, f".{path.name}-quality-baseline.json")


def label_for(path: Path) -> str:
    return CATEGORY_LABEL.get(path.name, "entry")


def run_vally(path: Path) -> str:
    if not shutil.which("npx"):
        print(
            "ERROR: `npx` not found on PATH. vally lint requires Node.js "
            "(node --version >= 20). Install Node or skip this check.",
            file=sys.stderr,
        )
        sys.exit(2)
    proc = subprocess.run(
        ["npx", "--yes", "@microsoft/vally-cli", "lint", str(path), "--verbose"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    # vally exits 1 when it finds violations — that's expected, not a run failure.
    if proc.returncode not in (0, 1):
        print(
            f"ERROR: vally lint failed to run (exit {proc.returncode}):\n{proc.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(2)
    return proc.stdout


def collect_failures(output: str) -> set[str]:
    failing: set[str] = set()
    for line in output.splitlines():
        m = HEADER_RE.match(line.strip())
        if m and m.group(1) == "❌":
            failing.add(m.group(2))
    return failing


def load_baseline(baseline_path: Path) -> set[str]:
    if not baseline_path.exists():
        return set()
    try:
        data = json.loads(baseline_path.read_text(encoding="utf-8"))
        return set(data.get("known_failing_skills", []))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        print(f"ERROR: cannot read baseline {baseline_path}: {e}", file=sys.stderr)
        sys.exit(2)


def write_baseline(baseline_path: Path, label: str, failing: set[str]) -> None:
    baseline_path.write_text(
        json.dumps(
            {
                "_comment": f"Grandfathered {label}s failing `vally lint` (spec-compliance / "
                f"valid-refs), pending burndown. Drain entries as {label}s are fixed; do NOT "
                "add new ones. Regenerate with: "
                f"python3 scripts/check_skill_quality.py --path <dir> --update-baseline",
                "known_failing_skills": sorted(failing),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    try:
        shown = baseline_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        shown = baseline_path
    print(f"Wrote {len(failing)} grandfathered {label}(s) to {shown}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Ratchet quality drift (vally lint) over an .agents/ subdirectory.")
    ap.add_argument("--strict", action="store_true", help="fail on ANY failing entry (ignore baseline)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--update-baseline", action="store_true", help="seed/refresh the baseline file")
    ap.add_argument("--path", default=str(SKILLS_DIR), help="directory to scan (default: .agents/skills)")
    ap.add_argument("--baseline", default=None, help="baseline file path (default: derived from --path)")
    args = ap.parse_args()

    scan_path = Path(args.path)
    baseline_path = Path(args.baseline) if args.baseline else default_baseline_for(scan_path)
    label = label_for(scan_path)

    output = run_vally(scan_path)
    failing = collect_failures(output)

    if args.update_baseline:
        write_baseline(baseline_path, label, failing)
        sys.exit(0)

    baseline = set() if args.strict else load_baseline(baseline_path)
    new = sorted(failing - baseline)
    grandfathered = sorted(failing & baseline)

    if args.json:
        print(
            json.dumps(
                {"total_failing": len(failing), "new_failures": new, "grandfathered": grandfathered},
                indent=2,
            )
        )
        sys.exit(1 if new else 0)

    if grandfathered and not args.strict:
        print(
            f"ℹ {len(grandfathered)} known-failing {label}(s) grandfathered via baseline "
            f"(pending burndown): {', '.join(grandfathered)}"
        )
    if not new:
        print(f"✓ {label.capitalize()} quality ratchet OK ({len(failing)} total failing, all grandfathered).")
        sys.exit(0)

    print(
        f"✗ {len(new)} {label}(s) newly failing vally lint"
        f"{' (strict)' if args.strict else ' outside the baseline'}: {', '.join(new)}\n"
    )
    print(output)
    print(
        "\nFix the entry (see .agents/skills/scan-skill-quality/SKILL.md), or if this is "
        "pre-existing drift being deferred, re-seed the baseline with: "
        f"python3 scripts/check_skill_quality.py --path {scan_path} --update-baseline"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
