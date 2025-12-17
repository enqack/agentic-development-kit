---
description: Capture institutional memory from an executed plan
operating_mode: audit-only
artifacts_required:
  - docs/exec/lessons-learned.md
---

# post-execution-review

Inputs:
- `docs/exec/runs/<run-id>/walkthrough.md`
- `artifacts/logs/post_verify_report.md` (preferred)
- Evidence under `artifacts/`

Rules:
- Entries MUST include evidence pointers (repo-relative paths).
- Do NOT add an entry if there is no evidence.
