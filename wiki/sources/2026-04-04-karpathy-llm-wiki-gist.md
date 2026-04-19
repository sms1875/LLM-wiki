---
title: Karpathy LLM Wiki Gist
type: source-summary
updated: 2026-04-04
status: reviewed
source_refs:
  - ../../raw/sources/2026-04-04-karpathy-llm-wiki-gist.md
tags:
  - source
  - llm-wiki
---

# Karpathy LLM Wiki Gist

원본: [raw card](../../raw/sources/2026-04-04-karpathy-llm-wiki-gist.md)

## TL;DR
- RAG처럼 질문할 때마다 원문에서 재탐색하는 대신, LLM이 지속적으로 업데이트하는 markdown wiki를 지식의 중심 레이어로 둔다.
- 구조는 `raw(불변 소스) → wiki(누적 지식) → schema(운영 규칙)` 3층으로 설계한다.
- 운영 사이클은 ingest / query / lint이며, `index.md`, `log.md`를 핵심 네비게이션 파일로 유지한다.

## 핵심 주장
- 질문 시점 재구성보다 사전 컴파일된 지식(wiki)을 누적하는 편이 장기적으로 효율적이다.
- 인간은 소스 큐레이션/판단에 집중하고, LLM은 요약/상호링크/유지보수를 담당한다.

## 근거/데이터
- 소스 문서는 중소 규모에서 index 기반 탐색만으로도 충분할 수 있음을 제시한다.
- 운영이 커질 경우 검색 도구(예: 로컬 markdown 검색) 도입을 제안한다.

## 반론/불확실성
- 완전 자동화보다 사람 검토가 섞인 ingest가 현실적이다.
- 도메인에 따라 스키마/폴더 구조는 크게 달라질 수 있다.

## wiki 반영 대상
- entities: [LLM Agent](../entities/llm-agent.md)
- concepts: [Raw-Wiki-Schema Architecture](../concepts/raw-wiki-schema-architecture.md)
- synthesis: [운영 원칙 초안](../synthesis/operating-principles.md)
