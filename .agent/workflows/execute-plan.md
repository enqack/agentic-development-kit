---
description: Execute an approved implementation plan, collect evidence, and summarize results
operating_mode: full-execution
artifacts_required:
  - docs/exec/runs/<run-id>/walkthrough.md
  - artifacts/test_results/
  - artifacts/logs/
---

# execute-plan

## Inputs

- `docs/exec/runs/<run-id>/implementation_plan.md`
- `docs/exec/runs/<run-id>/implementation_plan.json`

If inputs are missing, fail closed.

## Walkthrough requirements (normative)

`docs/exec/runs/<run-id>/walkthrough.md` MUST:
- reference files using **repo-relative paths only**
- NOT use `file://` URLs
- NOT use absolute filesystem paths
- NOT truncate evidence pointers with `...`
- list only **workspace artifacts** as evidence

It MUST NOT include an "Artifacts (Brain)" (or equivalent) section.

## Root hygiene (normative)

Workspace root MUST NOT contain:
- `implementation_plan.*`
- `walkthrough.md`
- `*.resolved*`
- `*.metadata.json`

If such files are produced by tooling, move them into the run directory or delete them.

## Verification (recommended default)

Run `tools/verify_all.sh` to:
- execute lints
- run project tests via `tools/test.sh` (language-agnostic hook)
- capture outputs under `artifacts/logs/*.log` and `artifacts/test_results/*`

These logs are preferred evidence pointers in `post_verify_report.md`.
