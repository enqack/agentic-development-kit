---
description: Produce implementation plan artifacts from verified agenda
operating_mode: design-only
artifacts_required:
  - docs/intent/project_intent.md
  - docs/exec/runs/<run-id>/implementation_plan.md
  - docs/exec/runs/<run-id>/implementation_plan.json
---

# plan-execution

Precondition:
- `docs/intent/project_intent.md` exists and reflects the repo's purpose.

If precondition is not met:
- fail closed (panic) and immediately initiate `establish-intent` by asking the canonical intent question.
- write `docs/intent/project_intent.md`
- then continue with `/plan-execution`

## Context load (normative)

Before drafting any plan, read:
- `docs/intent/project_intent.md`
- `AGENTS.md`
- `AGENDA.md`

Use the intent to choose domain-appropriate planning:
- software: design + tests + build verification
- writing: outlines + milestones + editorial workflow
- research: hypotheses + methods + citations + reproducibility steps
- art: briefs + iterations + asset workflow
- mixed/unknown: minimal, conservative plan with explicit unknowns

## Run directory

All plan artifacts MUST be written under:

`docs/exec/runs/<run-id>/`

## Outputs (normative paths)

- `docs/exec/runs/<run-id>/implementation_plan.md`
- `docs/exec/runs/<run-id>/implementation_plan.json`

Workspace root MUST NOT be used for plan artifacts.
