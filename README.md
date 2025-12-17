# Patch v5.3: Run directory hygiene

This patch relocates plan and walkthrough artifacts into per-run folders:

- `docs/exec/runs/<run-id>/implementation_plan.*`
- `docs/exec/runs/<run-id>/walkthrough.md`

and prohibits root-level spillover of intermediate artifacts.
