# Agentic Development Template

A language-agnostic repository template for **planning → execution → verification → reconciliation** with explicit evidence.

The project inside the repo may be software, writing, research, art, or mixed. The workflow system uses Python as a **verification runtime only** (to run `tools/*.py`).

## First run checklist

1. **Establish intent (required)**
   - Run: `/establish-intent`
   - Output: `docs/intent/project_intent.md`

2. **Verify agenda**
   - Run: `/verify-agenda`
   - Output: agenda quality checks and a plan-ready state

3. **Plan**
   - Run: `/plan-execution`
   - Outputs:
     - `docs/exec/runs/<run-id>/implementation_plan.md`
     - `docs/exec/runs/<run-id>/implementation_plan.json`

4. **Execute**
   - Run: `/execute-plan`
   - Outputs:
     - `docs/exec/runs/<run-id>/walkthrough.md`
     - evidence under `artifacts/`

5. **Verify + reconcile**
   - Run: `/post-verify` and `/post-execution-review`
   - Outputs:
     - `artifacts/logs/post_verify_report.md`
     - `docs/exec/lessons-learned.md`

## Intent: global + mechanical enforcement

This template is intentionally “fool-resistant”:

- **Global rule (policy):**
  - Until `docs/intent/project_intent.md` exists, the only permitted workflow is `establish-intent`.

- **Mechanical rule (lint):**
  - Every workflow (except `establish-intent`) must reference `docs/intent/project_intent.md` as a precondition/artifact requirement.
  - Enforced by `tools/workflow_intent_lint.py` (runs in `tools/verify_all.sh` and CI).

## Verification runtime

Install verification tooling (optional but recommended):

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-verify.txt
```

Run:

```sh
tools/verify_all.sh
```

## Tests are language-agnostic

Project tests are defined in:

- `tools/test.sh`

Edit it to run your project’s tests deterministically (Go/Rust/Node/Python examples included).
