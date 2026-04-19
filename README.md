# LLM-wiki

karpathy의 LLM Wiki 아이디어를 참고해, **앞으로 링크/문서/파일을 넣으면 누적형 wiki를 유지**할 수 있도록 기본 환경을 구성한 저장소입니다.

## 무엇을 개선했나 (실제 구현 사례 반영)
최근 공개된 LLM Wiki 구현들(`Pratiyush/llm-wiki`, `ussumant/llm-wiki-compiler`, `atomicmemory/llm-wiki-compiler`)을 참고해 아래를 반영했습니다.
- ingest 자동화 + **idempotent 로그**(중복 ingest 기록 방지)
- lint 자동화(고아 페이지, 깨진 상대링크, frontmatter 누락, source id 중복)
- 템플릿 기반 문서 작성(`wiki/templates/`)
- PR 컨플릭트 감소를 위해 **웹 빌드 산출물은 git에 커밋하지 않고** `.site-src/`에서 생성

## 목표
- `raw/`: 원본(불변) 보관
- `wiki/`: LLM이 관리하는 누적 지식 베이스
- `AGENTS.md`: Codex가 일관된 규칙으로 ingest/query/lint/publish 수행

## 빠른 시작
새 소스를 추가할 때:

```bash
python3 scripts/ingest_source.py \
  --title "문서 제목" \
  --type link \
  --ref "https://example.com/article"
```

위키 lint:

```bash
python3 scripts/lint_wiki.py
```

PR 충돌 사전 분석:

```bash
python3 scripts/pr_conflict_analyze.py --target main
```

웹 빌드 소스 생성(커밋 대상 아님):

```bash
python3 scripts/build_site.py
```

## 웹에서 확인하기 (GitHub Pages)
현재 구조를 웹에서 보려면 아래 순서를 따르면 됩니다.

1. GitHub 원격 저장소 연결 후 push
2. GitHub Actions `Deploy docs to GitHub Pages` 실행(자동)
3. 저장소 Settings → Pages에서 GitHub Actions 소스를 활성화

배포 시 워크플로우가 `.site-src/`를 자동 생성한 뒤 `mkdocs build`로 배포합니다.

## 구조
```text
.
├─ AGENTS.md
├─ raw/
├─ wiki/
├─ scripts/
│  ├─ ingest_source.py
│  ├─ lint_wiki.py
│  ├─ build_site.py
│  └─ pr_conflict_analyze.py
├─ docs/
├─ mkdocs.yml
└─ .github/workflows/deploy-pages.yml
```

## 참고
- 원문 gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
