---
description: Produce implementation plan artifacts from verified agenda
operating_mode: design-only
artifacts_required:
  - docs/exec/runs/<run-id>/implementation_plan.md
  - docs/exec/runs/<run-id>/implementation_plan.json
---

# plan-execution

## Run directory

All plan artifacts MUST be written under:

`docs/exec/runs/<run-id>/`

Where `<run-id>` SHOULD be:
- `YYYY-MM-DD_HYP-####`
or another stable identifier agreed by the workspace.

## Outputs (normative paths)

- `docs/exec/runs/<run-id>/implementation_plan.md`
- `docs/exec/runs/<run-id>/implementation_plan.json`

The plan MUST include:
- hypotheses (stable IDs)
- invariants and failure criteria
- tests (unit, integration, build verification)
- dependencies and sequencing
- risks and unknowns

The plan MUST NOT claim execution or evidence.

Workspace root MUST NOT be used for plan artifacts.
