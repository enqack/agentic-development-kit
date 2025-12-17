# General Software Development Agent Template (v3)

Adds **post-execution agenda verification** to keep the work queue aligned with reality.

## Pipeline

1. `prep-context` (audit-only)
2. `verify-agenda` (audit/design-only)
3. `plan-execution` (design-only) -> emits `implementation_plan.*`
4. `execute-plan` (full-execution) -> emits `walkthrough.md` + evidence under `artifacts/`
5. `post-verify` (audit-only) -> emits `artifacts/logs/post_verify_report.md`

## Local checks

```sh
python3 tools/agenda_lint.py
python3 tools/plan_lint.py
python3 tools/post_verify_lint.py
```
