---
description: Begin a new session or work cycle
operating_mode: audit-only
artifacts_required: 
  - docs/intent/project_intent.md
---

# start

## Purpose

User-friendly entry point for the agentic development cycle.

It ensures basics are in place (`project_intent.md`) and then hands off to the main orchestrator (`plan-cycle`).

## Workflow

1. **Check Intent**
   - Check if `docs/intent/project_intent.md` exists.
   - If MISSING, run `establish-intent`.

2. **Hand off to Cycle**
   - Run `plan-cycle` workflow.
