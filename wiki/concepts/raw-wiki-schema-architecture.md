---
title: Raw-Wiki-Schema Architecture
type: concept
updated: 2026-04-18
source_refs:
  - ../sources/2026-04-04-karpathy-llm-wiki-gist.md
tags:
  - concept
  - architecture
---

# Raw-Wiki-Schema Architecture

## 정의
- Raw: 원본 소스 저장소(불변)
- Wiki: LLM이 유지보수하는 누적 지식 저장소
- Schema: LLM 행동 규칙(예: `AGENTS.md`)

## 기대 효과
- 질문 시점의 재탐색 비용 감소
- 지식의 누적/연결/갱신 가능
- 유지보수 자동화
