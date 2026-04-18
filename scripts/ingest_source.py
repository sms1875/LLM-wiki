#!/usr/bin/env python3
"""Create raw/wiki scaffolding entries for a newly ingested source.

Improvements over v1:
- Idempotent log entries (no duplicate ingest records for same source/date).
- Markdown-table-safe escaping for raw index cells.
- Stable append helpers and section insertion.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RAW_INDEX = ROOT / "raw" / "index.md"
WIKI_INDEX = ROOT / "wiki" / "index.md"
WIKI_LOG = ROOT / "wiki" / "log.md"
RAW_SOURCES = ROOT / "raw" / "sources"
WIKI_SOURCES = ROOT / "wiki" / "sources"


@dataclass
class Source:
    source_id: str
    title: str
    source_type: str
    ref: str
    date_str: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "untitled"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="source title")
    parser.add_argument(
        "--type",
        required=True,
        choices=["link", "file", "note"],
        help="source kind",
    )
    parser.add_argument("--ref", required=True, help="url or file path or note reference")
    parser.add_argument("--date", help="YYYY-MM-DD; default=today(UTC)")
    parser.add_argument(
        "--source-id",
        help="override generated source id (default: <date>-<slugified-title>)",
    )
    return parser.parse_args()


def resolve_date(user_date: str | None) -> str:
    if user_date:
        datetime.strptime(user_date, "%Y-%m-%d")
        return user_date
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def markdown_escape_table_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def append_if_missing_exact(path: Path, exact_block: str) -> bool:
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    if exact_block in content:
        return False
    with path.open("a", encoding="utf-8") as f:
        f.write(exact_block)
    return True


def ensure_section(path: Path, section_title: str) -> None:
    marker = f"## {section_title}\n"
    content = path.read_text(encoding="utf-8")
    if marker not in content:
        with path.open("a", encoding="utf-8") as f:
            f.write(f"\n{marker}")


def insert_under_section(path: Path, section_title: str, line: str) -> None:
    marker = f"## {section_title}\n"
    content = path.read_text(encoding="utf-8")
    if line in content:
        return
    if marker not in content:
        content += f"\n{marker}\n"
    content = content.replace(marker, marker + "\n" + line)
    path.write_text(content, encoding="utf-8")


def create_raw_card(src: Source) -> Path:
    raw_card = RAW_SOURCES / f"{src.source_id}.md"
    if raw_card.exists():
        return raw_card

    raw_card.write_text(
        (
            "---\n"
            f"title: {src.title}\n"
            "type: raw-source\n"
            f"source_kind: {src.source_type}\n"
            f"date: {src.date_str}\n"
            f"ref: {src.ref}\n"
            "status: immutable\n"
            "---\n\n"
            "# Source Card\n\n"
            f"- Title: {src.title}\n"
            f"- Type: {src.source_type}\n"
            f"- Date: {src.date_str}\n"
            f"- Ref: {src.ref}\n\n"
            "## Notes\n"
            "- 원문 내용을 이 파일에 요약으로 덮어쓰지 말고, 필요한 경우 별도 wiki 페이지에서 다루세요.\n"
        ),
        encoding="utf-8",
    )
    return raw_card


def create_wiki_source_page(src: Source) -> Path:
    wiki_page = WIKI_SOURCES / f"{src.source_id}.md"
    if wiki_page.exists():
        return wiki_page

    wiki_page.write_text(
        (
            "---\n"
            f"title: {src.title}\n"
            "type: source-summary\n"
            f"updated: {src.date_str}\n"
            "status: draft\n"
            f"source_refs:\n  - ../../raw/sources/{src.source_id}.md\n"
            "tags:\n  - source\n"
            "---\n\n"
            f"# {src.title}\n\n"
            f"원본: [raw card](../../raw/sources/{src.source_id}.md)\n\n"
            "## TL;DR\n"
            "- (작성 필요)\n\n"
            "## 핵심 주장\n"
            "- (작성 필요)\n\n"
            "## 근거/데이터\n"
            "- (작성 필요)\n\n"
            "## 반론/불확실성\n"
            "- (작성 필요)\n\n"
            "## wiki 반영 대상\n"
            "- entities: \n"
            "- concepts: \n"
            "- synthesis: \n"
        ),
        encoding="utf-8",
    )
    return wiki_page


def update_indexes(src: Source) -> None:
    RAW_INDEX.parent.mkdir(parents=True, exist_ok=True)
    WIKI_INDEX.parent.mkdir(parents=True, exist_ok=True)

    for p, init in (
        (RAW_INDEX, "# Raw Source Index\n\n원본 소스 카탈로그(불변).\n\n| date | id | title | type | ref |\n|---|---|---|---|---|\n"),
        (WIKI_INDEX, "# Wiki Index\n\nLLM이 관리하는 페이지 카탈로그.\n\n## Sources\n\n## Concepts\n\n## Entities\n\n## Synthesis\n\n## Queries\n"),
    ):
        if not p.exists():
            p.write_text(init, encoding="utf-8")

    raw_line = (
        f"| {markdown_escape_table_cell(src.date_str)} | "
        f"{markdown_escape_table_cell(src.source_id)} | "
        f"{markdown_escape_table_cell(src.title)} | "
        f"{markdown_escape_table_cell(src.source_type)} | "
        f"{markdown_escape_table_cell(src.ref)} |\n"
    )
    append_if_missing_exact(RAW_INDEX, raw_line)

    source_entry = f"- [{src.title}](sources/{src.source_id}.md) — {src.date_str}\n"
    ensure_section(WIKI_INDEX, "Sources")
    insert_under_section(WIKI_INDEX, "Sources", source_entry)


def update_log(src: Source) -> None:
    if not WIKI_LOG.exists():
        WIKI_LOG.write_text("# Wiki Log\n\nappend-only 작업 로그.\n", encoding="utf-8")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    header = f"## [{src.date_str}] ingest | {src.title}"

    content = WIKI_LOG.read_text(encoding="utf-8")
    if header in content and f"source_id: `{src.source_id}`" in content:
        return

    block = (
        f"\n{header}\n"
        f"- source_id: `{src.source_id}`\n"
        f"- source_type: `{src.source_type}`\n"
        f"- ref: `{src.ref}`\n"
        f"- processed_at_utc: `{timestamp}`\n"
    )
    append_if_missing_exact(WIKI_LOG, block)


def main() -> None:
    args = parse_args()
    date_str = resolve_date(args.date)
    source_id = args.source_id or f"{date_str}-{slugify(args.title)}"

    src = Source(
        source_id=source_id,
        title=args.title,
        source_type=args.type,
        ref=args.ref,
        date_str=date_str,
    )

    RAW_SOURCES.mkdir(parents=True, exist_ok=True)
    WIKI_SOURCES.mkdir(parents=True, exist_ok=True)

    raw_card = create_raw_card(src)
    wiki_page = create_wiki_source_page(src)
    update_indexes(src)
    update_log(src)

    print(f"Created/updated source: {src.source_id}")
    print(f"- raw card: {raw_card.relative_to(ROOT)}")
    print(f"- wiki page: {wiki_page.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
