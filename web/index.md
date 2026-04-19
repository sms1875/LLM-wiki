# LLM Wiki (Web)

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
