---
description: Re-run agenda verification after execution and record reconciliation results
operating_mode: audit-only
artifacts_required:
  - artifacts/logs/post_verify_report.md
---

# post-verify

After executing a plan, re-verify that `AGENDA.md` reflects reality.

Emit `artifacts/logs/post_verify_report.md` including:
- Completed items with evidence pointers
- Items still open + required evidence to close
- Mismatches between plan/walkthrough/agenda
