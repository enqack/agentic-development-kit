# Agentic Development Template

A language-agnostic repository template for **planning → execution → verification → reconciliation** with explicit evidence.

The project inside the repo may be software, writing, research, art, or mixed. The workflow system uses Python as a **verification runtime only** (to run `tools/*.py`).

## First run

Run:

- `/establish-intent`

This creates `docs/intent/project_intent.md`, which is required before planning or execution.

## Panic / fail-closed behavior

If you invoke a workflow that requires intent (e.g., `/plan-execution`) before intent exists, the agent MUST fail closed and immediately ask the canonical intent question, write the intent file, and then resume the requested workflow. No override prompts.

## Verification runtime

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
