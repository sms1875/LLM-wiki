#!/usr/bin/env python3
"""Prepare web docs content from repository markdown sources.

Copies selected markdown trees into `web/` so MkDocs can publish them.
"""

from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

COPY_DIRS = ["wiki", "raw", "docs"]
COPY_FILES = ["README.md"]


def reset_target(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst)


def write_index() -> None:
    content = """# LLM Wiki (Web)

이 사이트는 `raw/` + `wiki/` 지식 베이스를 웹에서 탐색하기 위한 정적 빌드 결과입니다.

## 시작
- [Repository README](README.md)
- [Wiki Index](wiki/index.md)
- [Raw Index](raw/index.md)
- [Workflow](docs/WORKFLOW.md)

## 업데이트 방법
1. 새 소스 ingest: `python3 scripts/ingest_source.py ...`
2. 위키 lint: `python3 scripts/lint_wiki.py`
3. 사이트 동기화: `python3 scripts/build_site.py`
4. GitHub Actions가 Pages 배포
"""
    (WEB / "index.md").write_text(content, encoding="utf-8")


def main() -> None:
    WEB.mkdir(parents=True, exist_ok=True)

    for d in COPY_DIRS:
        src = ROOT / d
        dst = WEB / d
        reset_target(dst)
        copy_tree(src, dst)

    for f in COPY_FILES:
        src = ROOT / f
        dst = WEB / f
        reset_target(dst)
        shutil.copy2(src, dst)

    write_index()
    print("Built web content under web/")


if __name__ == "__main__":
    main()
