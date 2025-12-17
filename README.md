# General Software Development Agent Template (v5)

v5 changes:
- `.agents/` renamed to `.agent/`
- institutional memory moved under `docs/exec/`
  - `docs/exec/lessons-learned.md`
  - `docs/exec/cursed-knowledge.md`
- `.agentsignore` added (agent-side ignore rules)
- CI gate + scripts updated to new paths
- `prep-context` now specifies emitting `artifacts/logs/context_manifest.md`

## Pipeline

1. `prep-context` (audit-only) -> emits `artifacts/logs/context_manifest.md`
2. `verify-agenda` (audit/design-only)
3. `plan-execution` (design-only) -> emits `implementation_plan.*`
4. `execute-plan` (full-execution) -> emits `walkthrough.md` + evidence under `artifacts/`
5. `post-verify` (audit-only) -> emits `artifacts/logs/post_verify_report.md`
6. `post-execution-review` (audit-only) -> updates `docs/exec/lessons-learned.md` (+ optional `docs/exec/cursed-knowledge.md`)

## Local checks

```sh
python3 tools/agenda_lint.py
python3 tools/plan_lint.py
python3 tools/post_verify_lint.py
python3 tools/lessons_lint.py
```
