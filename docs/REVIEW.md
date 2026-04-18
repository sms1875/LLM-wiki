# External Review (Karpathy LLM Wiki implementations)

검토일: 2026-04-18 (UTC)

## 참고한 구현 사례
- https://github.com/Pratiyush/llm-wiki
- https://github.com/ussumant/llm-wiki-compiler
- https://github.com/atomicmemory/llm-wiki-compiler
- 원문 아이디어: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## 기존 상태에서 보인 한계
1. ingest 재실행 시 `wiki/log.md`에 동일 소스가 중복 기록됨.
2. lint 자동화가 없어 위키 건강도(고아 페이지/깨진 링크/형식 누락)를 정기 점검하기 어려움.
3. 템플릿 계층이 없어 문서 품질 편차가 커질 수 있음.
4. `raw/index.md`는 Markdown 테이블 특수문자(`|`) 처리 미흡 시 깨질 가능성.

## 이번 개선 사항
1. `scripts/ingest_source.py`
   - idempotent ingest 로그 처리
   - 테이블 셀 escape 추가
   - `--source-id` 지원
   - 섹션 삽입 유틸 안정화
2. `scripts/lint_wiki.py` 추가
   - frontmatter 키 누락 점검
   - 깨진 상대 링크 점검
   - 고아 페이지 탐지
   - source id 중복 탐지
   - `wiki/lint/latest.md` 리포트 + `wiki/log.md` 기록
3. `wiki/templates/source-summary.md` 추가
   - source summary 기본 템플릿 제공
4. 문서 업데이트
   - `README.md`, `AGENTS.md`, `docs/WORKFLOW.md`

## 아직 남은 확장 아이디어
- query 결과 저장 자동화(`wiki/queries/`)
- build artifact(`llms.txt`, graph export) 생성
- lint severity 분류(critical/warn/info) 및 CI 연동
- 대규모 corpus 대비 검색 도구(BM25/vector) 연결
