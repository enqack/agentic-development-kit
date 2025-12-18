---
description: Execute an approved implementation plan, collect evidence, and summarize results
operating_mode: full-execution
artifacts_required:
  - docs/intent/project_intent.md
  - docs/exec/runs/<run-id>/walkthrough.md
  - artifacts/test_results/
  - artifacts/logs/
---

# execute-plan

Precondition:
- `docs/intent/project_intent.md` exists and reflects the repo's purpose.

If precondition is not met:
- fail closed (panic) and immediately initiate `establish-intent` by asking the canonical intent question.
- write `docs/intent/project_intent.md`
- then continue with `/execute-plan`

## Verification (recommended default)

Run `tools/verify_all.sh` to:
- validate template baseline + intent
- execute lints
- run project tests via `tools/test.sh` (language-agnostic hook)
- capture outputs under `artifacts/logs/*.log` and `artifacts/test_results/*`
