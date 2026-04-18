# LLM-wiki

karpathy의 LLM Wiki 아이디어를 참고해, **앞으로 링크/문서/파일을 넣으면 누적형 wiki를 유지**할 수 있도록 기본 환경을 구성한 저장소입니다.

## 무엇을 개선했나 (실제 구현 사례 반영)
최근 공개된 LLM Wiki 구현들(`Pratiyush/llm-wiki`, `ussumant/llm-wiki-compiler`, `atomicmemory/llm-wiki-compiler`)을 참고해 아래를 반영했습니다.
- ingest 자동화 + **idempotent 로그**(중복 ingest 기록 방지)
- lint 자동화(고아 페이지, 깨진 상대링크, frontmatter 누락, source id 중복)
- 템플릿 기반 문서 작성(`wiki/templates/`)

## 목표
- `raw/`: 원본(불변) 보관
- `wiki/`: LLM이 관리하는 누적 지식 베이스
- `AGENTS.md`: Codex가 일관된 규칙으로 ingest/query/lint 수행

## 빠른 시작
새 소스를 추가할 때:

```bash
python3 scripts/ingest_source.py \
  --title "문서 제목" \
  --type link \
  --ref "https://example.com/article"
```

파일 기반 소스:

```bash
python3 scripts/ingest_source.py \
  --title "PDF 노트" \
  --type file \
  --ref "raw/sources/my-paper.pdf"
```

위키 lint:

```bash
python3 scripts/lint_wiki.py
```

실행하면 다음이 자동 생성/갱신됩니다.
- `raw/sources/*.md` 소스 카드
- `raw/index.md`
- `wiki/sources/*.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/lint/latest.md` (lint 실행 시)

## 구조
```text
.
├─ AGENTS.md
├─ raw/
│  ├─ index.md
│  ├─ assets/
│  └─ sources/
├─ wiki/
│  ├─ index.md
│  ├─ log.md
│  ├─ lint/
│  ├─ templates/
│  ├─ sources/
│  ├─ entities/
│  ├─ concepts/
│  └─ synthesis/
├─ scripts/
│  ├─ ingest_source.py
│  └─ lint_wiki.py
└─ docs/
   ├─ WORKFLOW.md
   └─ REVIEW.md
```

## 참고
- 원문 gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
