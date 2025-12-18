# Agentic Development Template

A language-agnostic repository template for **planning → execution → verification → reconciliation** with explicit evidence.

The project inside the repo may be software, writing, research, art, or mixed. The workflow system uses Python as a **verification runtime only** (to run `tools/*.py`).

## First run

Run:

- `/establish-intent`

This creates `docs/intent/project_intent.md`, which is required before planning or execution.

## Panic / fail-closed behavior

If you invoke a workflow that requires intent (e.g., `/plan-execution`) before intent exists, the agent MUST fail closed and immediately ask the canonical intent question, write the intent file, and then resume the requested workflow. No override prompts.

## Ignore semantics

`.gitignore` and `.agentsignore` are NOT permission systems. They do not block file creation.

- Planning artifacts MUST be written under `docs/exec/runs/<run-id>/` even though that directory is typically gitignored.
- Agents MUST NOT ask the user to "override gitignore" to create run artifacts.

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

## Optional history

You can maintain a structured history that captures major runs, decisions, and reconciliations. Regenerate it from the current artifacts with `python update_history.py`, keep the formatting tidy with `python history_lint.py`, and sanity-check the output with `./history_check.sh`.
