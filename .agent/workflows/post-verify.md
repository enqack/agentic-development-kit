---
description: Re-run agenda verification after execution and record reconciliation results
operating_mode: audit-only
artifacts_required:
  - artifacts/logs/post_verify_report.md
---

# post-verify

## Purpose

After executing a plan, re-verify that `AGENDA.md` reflects reality and that any items
marked `finished` have evidence pointers referencing existing artifacts.

## Preconditions

- `walkthrough.md` exists
- `AGENDA.md` can be read

If preconditions fail, fail closed.

## Procedure

1. Run `verify-agenda` in **audit-only** mode.
2. Reconcile statuses:
   - Items supported by evidence MAY be marked `finished`.
   - Items without proof MUST remain unresolved (not `finished`).
3. Emit `artifacts/logs/post_verify_report.md` including:
   - Completed items (with evidence pointers)
   - Items still open + required evidence to close
   - Detected mismatches between plan/walkthrough/agenda
