---
description: Verify agenda items and classify completion status
operating_mode: audit-only | design-only
artifacts_required:
  - artifacts/intent/project_intent.md
---

# verify-agenda

Precondition:

- `artifacts/intent/project_intent.md` exists.

If precondition is not met:

- **FAIL CLOSED**
- Ask the operator:
  - "What are you trying to produce in this repo (software, book, research notes, something else), and what does 'done' look like for the first milestone?"
- Initiate the `establish-intent` workflow.
- Do **not** continue with any other workflow until intent is established.

Agenda items MUST be classified as one of:

- finished
- in-progress
- blocked
- not-started
- unknown

Rules:

- `finished` items MUST include evidence pointers (paths only).
- `unknown` items are defects and MUST specify what evidence would resolve them.

Planning rule:
Items marked `finished` MUST NOT appear in `implementation_plan.*`
unless explicitly reopened under a new hypothesis ID (or marked regression-only).
