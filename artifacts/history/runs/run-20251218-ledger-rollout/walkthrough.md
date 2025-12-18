# Walkthrough: Workflow Migration and Activity Ledger

## Changes (v2)

### Workflow Migration

Migrated `.agent/workflows` from `goppydae-silo` to `agentic-development-kit`.

- **Source**: `goppydae-silo/.agent/workflows/`
- **Destination**: `agentic-development-kit/.agent/workflows/`
- **Verification**: Confirmed `finish.md` includes ADK-specific formatting steps.

### Agent Activity Ledger (Schema v2)

Implemented a persistent, ecosystem-wide ledger to track agent actions with a **rich schema**.

#### Infrastructure

- **Tool**: `tools/cvr/log_action.py`
  - Appends to `artifacts/agent_activity.jsonl` (NDJSON)
  - **Schema**:
    - `ts`: Timestamp (UTC, ISO-8601)
    - `actor`: `$USER` or "unknown"
    - `intent`: High-level goal (e.g., "fix_ci")
    - `scope`: Affected subsystem
    - `mode`: "normal" | "maintenance"
    - `action`: verb (e.g., "modify")
    - `result`: "ok" | "fail"
    - `evidence`: list of files
- **Workflow**: `toggle-maintenance-mode`
  - Updated to use rich schema flags (`--intent`, `--action`, etc.)

#### Documentation

- **AGENTS.md**: Updated logic and schema definition.
- **.gitignore**: Allowed `!artifacts/agent_activity.jsonl`.

#### Ecosystem Scope

Applied to all 4 repositories:

1. `agentic-development-kit`
1. `goppydae-silo`
1. `gapi`
1. `goblin`

## Verification Results

### Functionality

Ran verification loop in all 4 repos:

```bash
python3 tools/cvr/log_action.py --intent verify_schema --action test --scope $repo --evidence tools/cvr/log_action.py
```

**Result**: Success.
Sample Output:

```json
{"ts": "2025-12-18T22:11:18Z", "actor": "sysop", "intent": "verify_schema", "scope": "gapi", "action": "test", "result": "ok", "evidence": ["tools/cvr/log_action.py"], "mode": "normal"}
```

### Documentation

Checked `AGENTS.md` and confirmed schema match.
