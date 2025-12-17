---
description: Produce implementation_plan.md and implementation_plan.json from verified agenda
operating_mode: design-only
artifacts_required:
  - implementation_plan.md
  - implementation_plan.json
---

# plan-execution

## Outputs

This workflow MUST produce:
- `implementation_plan.md` (human-readable)
- `implementation_plan.json` (machine-checkable; schema: `tools/plan_schema.json`)

## Requirements

The plan MUST include:
- hypotheses (stable IDs)
- invariants and failure criteria
- tests (unit, integration, build verification)
- dependencies and sequencing
- risks and unknowns

The plan MUST NOT claim execution or evidence.
