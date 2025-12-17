# General Software Development Agent Template (v2)

This repository template provides a **planning + execution** workflow for an agent that behaves
like a planning compiler: verify -> plan -> execute -> summarize, with CI guardrails.

## Workflows

- `prep-context` (audit-only): load required context
- `verify-agenda` (audit/design-only): classify agenda items + completion evidence
- `plan-execution` (design-only): produce `implementation_plan.md` + `implementation_plan.json`
- `execute-plan` (full-execution): apply plan, run tests, write evidence, produce `walkthrough.md`

## Local checks

```sh
python3 tools/agenda_lint.py
python3 tools/plan_lint.py
```
