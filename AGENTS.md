# LLM Wiki 운영 스키마 (Codex용)

이 저장소는 **Raw source → Wiki compilation** 패턴으로 동작합니다.

## 0) 핵심 원칙
1. `raw/`는 불변(immutable) 소스 저장소입니다. 원문/원본 파일은 수정하지 않습니다.
2. `wiki/`는 LLM이 관리하는 지식 레이어입니다. 요약, 개념, 엔티티, 비교, 종합 페이지를 갱신합니다.
3. 변경 이력은 `wiki/log.md`에 append-only로 남깁니다.
4. 새 소스가 들어오면 최소 아래를 수행합니다.
   - `raw/sources/`에 소스 카드 생성
   - `wiki/sources/`에 소스 요약/주장/근거 정리
   - 관련 `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/` 갱신
   - `wiki/index.md` 갱신
   - `wiki/log.md` 기록

## 1) 디렉토리 의미
- `raw/`: 원본 링크/문서/파일 메타데이터 및 원문 위치
- `wiki/`: LLM이 읽고 쓰는 지식 페이지
- `scripts/`: 반복 작업 자동화 도구
- `docs/`: 운영 가이드

## 2) 작업 워크플로우
### ingest
새 링크/문서/파일을 전달받으면:
1. `python3 scripts/ingest_source.py`로 소스 카드 및 기본 wiki 페이지 생성
2. 생성된 `wiki/sources/*.md`를 읽고 요약/핵심 주장/반론/모호점 보강
3. 기존 페이지와 충돌 여부 확인 후 관련 페이지 업데이트
4. 변경사항이 `wiki/index.md`, `wiki/log.md`에 반영되었는지 확인

### query
질의 응답 시:
1. 먼저 `wiki/index.md`에서 관련 후보 페이지 탐색
2. 필요한 페이지를 교차 읽고 답변 생성
3. 가치 있는 답변은 `wiki/synthesis/` 신규 페이지로 보존 가능

### lint
주기적으로:
- `python3 scripts/lint_wiki.py` 실행
- 고아 페이지(링크 없음)
- 상충 주장
- 오래된 주장
- 끊긴 링크
- 누락된 핵심 개념
을 점검하고 `wiki/log.md` 및 `wiki/lint/latest.md`를 기록

## 3) 문서 작성 규칙
- 모든 wiki 문서는 markdown.
- 가급적 문서 상단에 YAML frontmatter 사용:
  - `title`, `type`, `updated`, `source_refs`, `tags`
- 내부 링크는 상대경로 markdown 링크 사용.
- 추론과 사실을 분리해 작성.
- 새 source summary는 `wiki/templates/source-summary.md` 템플릿을 참고.

## 4) 금지 사항
- raw 원본을 요약 형태로 덮어쓰기 금지.
- 출처 없는 단정 금지.
- 대규모 구조 변경 시 `wiki/index.md`와 `wiki/log.md` 미갱신 금지.
