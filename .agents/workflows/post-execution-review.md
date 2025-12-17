---
description: Capture institutional memory from an executed plan
operating_mode: audit-only
artifacts_required:
  - lessons-learned.md
---

# post-execution-review

## Purpose

Record durable learnings from plan execution.

- `lessons-learned.md` is REQUIRED for non-trivial work that changes code.
- `cursed-knowledge.md` is OPTIONAL, but encouraged when a sharp edge cost real time.

## Inputs

- `walkthrough.md`
- `artifacts/logs/post_verify_report.md` (preferred)
- Evidence under `artifacts/`

If required inputs are missing, fail closed.

## Rules

- Entries MUST include evidence pointers (paths + optional anchors).
- Do NOT add an entry if there is no evidence (avoid mythmaking).

## Output format

Append a new section to `lessons-learned.md`:

### YYYY-MM-DD — <summary>
- What went well:
- What went poorly:
- Surprises:
- Changes to make next time:
- Follow-ups (new agenda items):
- Evidence: ...

Optionally append to `cursed-knowledge.md`:

### YYYY-MM-DD — <short title>
- Symptom:
- Trigger:
- Detection:
- Mitigation:
- Evidence: ...
- Notes:
