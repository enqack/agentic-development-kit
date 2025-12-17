---
description: Verify agenda items and classify completion status
operating_mode: audit-only | design-only
---

# verify-agenda

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
