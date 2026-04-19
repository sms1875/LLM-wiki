#!/usr/bin/env python3
"""Prepare publish-ready docs content from repository markdown sources.

Copies selected markdown trees into `.site-src/` (ephemeral build directory)
so MkDocs can publish them without committing generated mirror files.
"""

from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE_SRC = ROOT / ".site-src"

COPY_DIRS = ["wiki", "raw", "docs"]
COPY_FILES = ["README.md"]


def reset_target(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


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
    (SITE_SRC / "index.md").write_text(content, encoding="utf-8")


def main() -> None:
    reset_target(SITE_SRC)
    SITE_SRC.mkdir(parents=True, exist_ok=True)

    for d in COPY_DIRS:
        src = ROOT / d
        dst = SITE_SRC / d
        shutil.copytree(src, dst)

    for f in COPY_FILES:
        shutil.copy2(ROOT / f, SITE_SRC / f)

    write_index()
    print("Built site source under .site-src/")


if __name__ == "__main__":
    main()
