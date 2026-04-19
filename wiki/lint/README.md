# Lint Reports

`wiki/lint/latest.md`는 충돌을 줄이기 위해 git에서 추적하지 않습니다.

## 기본 사용
```bash
python3 scripts/lint_wiki.py
```
- 결과: `.cache/wiki-lint/latest.md`

## 위키 경로에도 출력이 필요할 때
```bash
python3 scripts/lint_wiki.py --write-wiki-report
```
- 결과: `.cache/wiki-lint/latest.md`, `wiki/lint/latest.md`

## 로그까지 남길 때
```bash
python3 scripts/lint_wiki.py --append-log
```
