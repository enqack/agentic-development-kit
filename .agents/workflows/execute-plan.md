---
description: Execute an approved implementation plan, collect evidence, and summarize results
operating_mode: full-execution
artifacts_required:
  - walkthrough.md
  - artifacts/test_results/
  - artifacts/logs/
---

# execute-plan

## Purpose

Apply an approved plan and produce evidence suitable for third-party review.

This workflow is the only workflow permitted to:
- modify code/config
- run commands/tests
- claim runtime results

## Inputs

- `implementation_plan.md`
- `implementation_plan.json` (MUST conform to `tools/plan_schema.json`)

If inputs are missing or invalid, fail closed.

## Procedure

1. Confirm operating mode is **full-execution**.
2. For each plan item (in order):
   - restate hypothesis and invariants
   - apply the smallest change that tests the hypothesis
   - record diffs under `artifacts/diffs/` (optional but recommended)
3. Run tests defined in the plan:
   - unit
   - integration
   - build verification
4. Record evidence:
   - test outputs under `artifacts/test_results/`
   - relevant logs under `artifacts/logs/`
5. Produce `walkthrough.md` including:
   - what changed (high level)
   - which hypotheses were supported or falsified
   - which tests ran (commands + outcomes)
   - where evidence artifacts live (paths)
   - unresolved risks/unknowns

## Fail-Closed

If full-execution guarantees cannot be met (no write access, no test runner, missing deps),
fail closed and do not modify the working tree.
