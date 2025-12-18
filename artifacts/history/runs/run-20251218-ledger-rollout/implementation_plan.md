# Implementation Plan: Refine Agent Activity Ledger

## Goal

Update `agent_activity.jsonl` schema to match the user's historical format, adding semantic depth and preventing log spam ("log aggression").

## User Review Required

> [!NOTE]
> New schema requires `intent`, `scope`, `result`, and `evidence`.

## Proposed Changes

### Schema Definition

#### [MODIFY] \[AGENTS.md (All Repos)\](file:///home/sysop/Projects/silo/agentic-development-kit/AGENTS.md)

Update "Agent Activity Ledger" section to mandate the richer schema:

- `intent`: High-level goal (e.g., "fix_ci")
- `scope`: Affected subsystem (e.g., "tools", "gapi/core")
- `result`: "ok" | "fail"
- `evidence`: List of files or artifacts
- `metadata`: (Optional) for extra context

### Infrastructure

#### [MODIFY] \[tools/cvr/log_action.py (All Repos)\](file:///home/sysop/Projects/silo/agentic-development-kit/tools/cvr/log_action.py)

Update arguments to accept:

- `--intent` (required)
- `--scope` (optional, default "workspace")
- `--result` (default "ok")
- `--evidence` (list, optional)

### Log Aggression Strategy

- **Policy**: Only log *state-changing* or *milestone* events.
- **Do not log**: Read-only operations (`ls`, `cat`), minor intermediate steps.
- **Must log**: Workflow starts/stops, file modifications, mode toggles, verification results.

## Verification Plan

1. Update tool in ADK.
1. Verify with `python3 tools/cvr/log_action.py --action test --intent verify_schema --scope ADK`.
1. Replicate to ecosystem.
