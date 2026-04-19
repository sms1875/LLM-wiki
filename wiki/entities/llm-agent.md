---
title: LLM Agent
type: entity
updated: 2026-04-18
source_refs:
  - ../sources/2026-04-04-karpathy-llm-wiki-gist.md
tags:
  - entity
---

# LLM Agent

## 역할
- raw 소스를 읽고 wiki를 생성/갱신하는 실행 주체.
- 요약, 교차참조, 모순표시, 인덱스/로그 유지 작업을 수행.

## 운영 규칙
- raw 원본은 수정하지 않는다.
- 변경사항은 wiki 레이어에 기록한다.
- 갱신 이력은 `wiki/log.md`에 남긴다.
