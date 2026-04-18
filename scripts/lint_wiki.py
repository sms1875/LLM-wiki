#!/usr/bin/env python3
"""Lightweight lint checks for the markdown wiki.

Checks:
- Missing required frontmatter keys in wiki pages.
- Broken relative markdown links.
- Orphan wiki pages (no inbound links), excluding index/log/README/templates.
- Duplicate source IDs in raw/index.md.

Writes a report to wiki/lint/latest.md and appends a log entry to wiki/log.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
RAW_INDEX = ROOT / "raw" / "index.md"
WIKI_LOG = WIKI_DIR / "log.md"
REPORT_DIR = WIKI_DIR / "lint"
REPORT_PATH = REPORT_DIR / "latest.md"

EXCLUDE_ORPHAN = {
    "index.md",
    "log.md",
    "README.md",
}

REQUIRED_FRONTMATTER_KEYS = {"title", "type", "updated", "source_refs", "tags"}


@dataclass
class Issue:
    level: str
    code: str
    path: str
    detail: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter_keys(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---\n", 4)
    if end == -1:
        return set()
    fm = text[4:end]
    keys: set[str] = set()
    for line in fm.splitlines():
        if not line or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def iter_wiki_pages() -> list[Path]:
    return sorted(
        p
        for p in WIKI_DIR.rglob("*.md")
        if "/lint/" not in p.as_posix() and "/templates/" not in p.as_posix()
    )


def find_markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def collect_issues() -> list[Issue]:
    issues: list[Issue] = []
    pages = iter_wiki_pages()
    inbound = {p.resolve(): 0 for p in pages}

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        text = read_text(page)

        if page.name not in EXCLUDE_ORPHAN:
            keys = parse_frontmatter_keys(text)
            missing = REQUIRED_FRONTMATTER_KEYS - keys
            if missing:
                issues.append(
                    Issue(
                        level="WARN",
                        code="missing_frontmatter_keys",
                        path=rel,
                        detail=f"missing: {', '.join(sorted(missing))}",
                    )
                )

        for link in find_markdown_links(text):
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
                continue
            target = (page.parent / link).resolve()
            if target.suffix == "":
                target = target.with_suffix(".md")
            if target.exists():
                if target in inbound:
                    inbound[target] += 1
            else:
                issues.append(
                    Issue(
                        level="WARN",
                        code="broken_relative_link",
                        path=rel,
                        detail=f"{link} -> missing",
                    )
                )

    for page, count in inbound.items():
        p = Path(page)
        if p.name in EXCLUDE_ORPHAN:
            continue
        if "/templates/" in p.as_posix() or "/lint/" in p.as_posix():
            continue
        if count == 0:
            issues.append(
                Issue(
                    level="WARN",
                    code="orphan_page",
                    path=p.relative_to(ROOT).as_posix(),
                    detail="no inbound markdown links",
                )
            )

    if RAW_INDEX.exists():
        ids: list[str] = []
        for line in read_text(RAW_INDEX).splitlines():
            if not line.startswith("|") or line.startswith("|---"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] != "date":
                ids.append(cells[1])
        seen = set()
        dupes = set()
        for sid in ids:
            if sid in seen:
                dupes.add(sid)
            seen.add(sid)
        for sid in sorted(dupes):
            issues.append(
                Issue(
                    level="WARN",
                    code="duplicate_source_id",
                    path="raw/index.md",
                    detail=sid,
                )
            )

    return issues


def write_report(issues: list[Issue]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    lines = [
        "# Wiki Lint Report",
        "",
        f"- generated_at_utc: `{now}`",
        f"- issue_count: `{len(issues)}`",
        "",
        "| level | code | path | detail |",
        "|---|---|---|---|",
    ]

    for i in issues:
        lines.append(
            f"| {i.level} | {i.code} | {i.path.replace('|', '\\|')} | {i.detail.replace('|', '\\|')} |"
        )

    if not issues:
        lines.append("| PASS | none | - | no issues found |")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_log(issues: list[Issue]) -> None:
    if not WIKI_LOG.exists():
        WIKI_LOG.write_text("# Wiki Log\n\nappend-only 작업 로그.\n", encoding="utf-8")

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    block = (
        f"\n## [{day}] lint | wiki health check\n"
        f"- issues: `{len(issues)}`\n"
        f"- report: `wiki/lint/latest.md`\n"
        f"- processed_at_utc: `{ts}`\n"
    )
    with WIKI_LOG.open("a", encoding="utf-8") as f:
        f.write(block)


def main() -> None:
    issues = collect_issues()
    write_report(issues)
    append_log(issues)
    print(f"Lint complete. issues={len(issues)} report={REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
