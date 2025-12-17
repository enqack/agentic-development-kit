# General Software Development Agent Template (v4)

Adds a **post-execution review** step that captures institutional memory:

- `lessons-learned.md` (required for non-trivial code changes)
- `cursed-knowledge.md` (optional; sharp edges registry)

## Pipeline

1. `prep-context` (audit-only)
2. `verify-agenda` (audit/design-only)
3. `plan-execution` (design-only) -> emits `implementation_plan.*`
4. `execute-plan` (full-execution) -> emits `walkthrough.md` + evidence under `artifacts/`
5. `post-verify` (audit-only) -> emits `artifacts/logs/post_verify_report.md`
6. `post-execution-review` (audit-only) -> updates `lessons-learned.md` (+ optional `cursed-knowledge.md`)

## Local checks

```sh
python3 tools/agenda_lint.py
python3 tools/plan_lint.py
python3 tools/post_verify_lint.py
python3 tools/lessons_lint.py
```
