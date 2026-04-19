#!/usr/bin/env python3
"""Analyze merge conflicts between current HEAD and a target branch.

Usage:
  python3 scripts/pr_conflict_analyze.py --target main
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", default="main", help="target/base branch to merge into")
    return p.parse_args()


def suggested_resolution(path: str) -> str:
    if path.startswith("web/") or path.startswith(".site-src/"):
        return "generated artifact: remove from git tracking and regenerate via scripts/build_site.py"
    if path in {"wiki/lint/latest.md"}:
        return "regenerated file: run python3 scripts/lint_wiki.py after merge"
    if path == "wiki/log.md":
        return "append-only log: keep both entries, then de-duplicate exact repeated blocks"
    if path.startswith("wiki/") and path.endswith(".md"):
        return "manual semantic merge needed (knowledge content)"
    return "manual merge"


def main() -> None:
    args = parse_args()

    run(["git", "rev-parse", "--verify", args.target])

    with TemporaryDirectory(prefix="pr-merge-check-") as tmp:
        tmp_path = Path(tmp)
        run(["git", "worktree", "add", "--detach", str(tmp_path), args.target])
        try:
            merge = subprocess.run(
                ["git", "merge", "--no-commit", "--no-ff", "HEAD"],
                cwd=tmp_path,
                text=True,
                capture_output=True,
            )
            if merge.returncode == 0:
                print("No merge conflicts detected.")
                return

            out = run(["git", "diff", "--name-only", "--diff-filter=U"], cwd=tmp_path)
            conflicted = [line.strip() for line in out.stdout.splitlines() if line.strip()]
            if not conflicted:
                print("Merge failed, but no explicit conflicted files were found.")
                print(merge.stdout)
                print(merge.stderr)
                return

            print(f"Detected {len(conflicted)} conflicted file(s):")
            for p in conflicted:
                print(f"- {p}")
                print(f"  resolution: {suggested_resolution(p)}")

            print("\nRecommended sequence:")
            print("1) Resolve listed files (prefer removing generated artifacts from tracking).")
            print("2) Re-run this script until no conflicts remain.")
            print("3) Run: python3 scripts/lint_wiki.py && python3 scripts/build_site.py")
        finally:
            run(["git", "worktree", "remove", "--force", str(tmp_path)], check=False)


if __name__ == "__main__":
    main()
