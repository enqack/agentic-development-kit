---
description: Re-run agenda verification after execution and record reconciliation results
operating_mode: audit-only
artifacts_required:
  - artifacts/logs/post_verify_report.md
---

# post-verify

After executing a plan, re-verify that `AGENDA.md` reflects reality.

## Output requirements

Emit `artifacts/logs/post_verify_report.md` with the following **exact** section headings:

- `## Completed items`
- `## Items still open`
- `## Evidence`

Rules:
- Evidence pointers MUST be repo-relative paths (e.g. `artifacts/test_results/...`).
- Evidence pointers MUST NOT be absolute paths and MUST NOT use `file://` URLs.
- Avoid truncation (`...`) in evidence pointers; they must be auditable.
