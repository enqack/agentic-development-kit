---
description: Execute an approved implementation plan, collect evidence, and summarize results
operating_mode: full-execution
artifacts_required:
  - docs/intent/project_intent.md
  - docs/exec/runs/<run-id>/walkthrough.md
  - artifacts/test_results/
  - artifacts/logs/
---

# execute-plan

Precondition:
- `docs/intent/project_intent.md` exists and reflects the repo's purpose.

If precondition is not met:
- fail closed (panic) and immediately initiate `establish-intent` by asking:
  - "What are you trying to produce in this repo (software, book, research notes, something else), and what does 'done' look like for the first milestone?"
- write `docs/intent/project_intent.md`
- then continue with `/execute-plan`

## Ignore semantics (normative)

`.gitignore` and `.agentsignore` are NOT permission systems.
They MUST NOT be treated as a precondition failure or a panic.

- Do NOT ask the user to bypass ignore rules.
- Ignore rules only affect what gets committed or included in agent context, not what can be created on disk.

## Verification (recommended default)

Run `tools/verify_all.sh` to:
- validate template baseline + intent
- execute lints
- run project tests via `tools/test.sh` (language-agnostic hook)
- capture outputs under `artifacts/logs/*.log` and `artifacts/test_results/*`
