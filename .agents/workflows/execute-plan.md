---
description: Execute an approved implementation plan, collect evidence, and summarize results
operating_mode: full-execution
artifacts_required:
  - walkthrough.md
  - artifacts/test_results/
  - artifacts/logs/
---

# execute-plan

Inputs:
- `implementation_plan.md`
- `implementation_plan.json` (must conform to schema)

Procedure:
1. Apply the smallest changes needed to test each hypothesis.
2. Run tests defined in the plan (unit/integration/build).
3. Record evidence under `artifacts/test_results/` and `artifacts/logs/`.
4. Produce `walkthrough.md` (commands + outcomes + evidence paths).
5. Run `post-verify` (audit-only).
6. Run `post-execution-review` (audit-only).

Fail closed if full-execution guarantees cannot be met.
