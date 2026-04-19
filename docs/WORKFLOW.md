# Workflow

## 1) Ingest
1. 사용자로부터 링크/문서/파일을 받는다.
2. `scripts/ingest_source.py`로 소스 카드 및 기본 wiki 페이지를 생성한다.
3. 생성된 wiki 소스 페이지를 보강한다.
4. 관련 엔티티/개념/종합 페이지를 업데이트한다.
5. `wiki/index.md`와 `wiki/log.md` 업데이트를 확인한다.

## 2) Query
1. `wiki/index.md`에서 관련 페이지를 찾는다.
2. 문서를 교차 검토해 답변한다.
3. 장기 가치가 있는 분석이면 `wiki/synthesis/`에 저장한다.

## 3) Lint
정기적으로 `python3 scripts/lint_wiki.py` 실행:
- 끊긴 상대 링크
- 고아 페이지
- frontmatter 누락
- `raw/index.md` 내 중복 source id

결과는 `wiki/lint/latest.md`와 `wiki/log.md`에 기록한다.

## 4) PR Conflict Analysis
병합 전 `python3 scripts/pr_conflict_analyze.py --target main` 실행:
- 예상 충돌 파일 목록
- 파일별 해결 가이드
- 재검증 순서

## 5) Publish (Web)
정적 웹 퍼블리시는 아래 순서로 진행:
1. `python3 scripts/build_site.py` (로컬 확인용)
2. `mkdocs build --strict`
3. GitHub Actions Pages 배포

참고: `.site-src/`, `site/`는 생성 산출물이므로 git 커밋 대상이 아니다.
