---
description: Begin a new session or work cycle
operating_mode: audit-only
artifacts_required:
  - artifacts/intent/project_intent.md
  - artifacts/logs/context_manifest.md
---

# start

## Purpose

User-friendly entry point for the agentic development cycle.

It ensures foundational artifacts exist (`project_intent.md`, context manifest) and then hands off to the main orchestrator (`plan-cycle`).

## Inputs

- `auto_approve` (boolean, optional): If true, skips the plan approval gate. default: `false`.

> [!WARNING]
> Setting `auto_approve: true` removes the human-in-the-loop safety check. Use only for routine tasks or trusted automated loops.

## Workflow

1. **Check Intent**

   - Check if `artifacts/intent/project_intent.md` exists.
   - If MISSING, run `establish-intent`.

2. **Ensure Context Prepared**

   - Check if `artifacts/logs/context_manifest.md` exists.
   - If MISSING, run `prep-context`.
   - If PRESENT, do not re-run `prep-context` (treat as already prepared for this working copy).

3. **Hand off to Cycle**

   - Run `plan-cycle` workflow with `auto_approve` argument.
