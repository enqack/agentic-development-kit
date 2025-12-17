---
description: Execute an approved implementation plan, collect evidence, and summarize results
operating_mode: full-execution
artifacts_required:
  - walkthrough.md
  - artifacts/test_results/
  - artifacts/logs/
---

# execute-plan

Apply an approved plan and produce evidence suitable for third-party review.

Inputs:
- `implementation_plan.md`
- `implementation_plan.json` (MUST conform to `tools/plan_schema.json`)

Procedure:
1. Confirm operating mode is **full-execution**.
2. Apply the smallest changes needed to test each hypothesis.
3. Run tests defined in the plan (unit/integration/build).
4. Record evidence under `artifacts/test_results/` and `artifacts/logs/`.
5. Produce `walkthrough.md` (commands run + outcomes + evidence paths).
6. Run `post-verify` (audit-only) and record reconciliation results.

Fail closed if full-execution guarantees cannot be met.
