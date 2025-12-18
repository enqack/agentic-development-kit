# Execution History Artifacts

This directory stores optional execution-history artifacts that can be regenerated or reset without affecting runtime behavior. The files are designed to help with post-run analysis and continuity for long-lived agendas.

## Files
- `hypotheses.ndjson`: Append-only newline-delimited JSON capturing hypotheses considered during execution.
- `agenda.ndjson`: Append-only newline-delimited JSON capturing agenda items as they are created, updated, or resolved.
- `../agenda_state.json`: A lightweight snapshot of the current agenda state (IDs and items) meant to be easy to reset.

## Schemas
Each NDJSON file is a sequence of standalone JSON objects (one per line).

### `hypotheses.ndjson`
- `id` (number): Monotonically increasing identifier, unique within this log.
- `statement` (string): Hypothesis text.
- `status` (string): Current state, e.g., `"open"`, `"accepted"`, or `"rejected"`.
- `confidence` (number, optional): Confidence score between 0 and 1.
- `agenda_refs` (array<number>, optional): Related agenda item IDs.
- `created_at` (string, ISO-8601): Timestamp of the hypothesis entry.

### `agenda.ndjson`
- `id` (number): Agenda item identifier, matching `agenda_state.json`.
- `title` (string): Human-readable summary of the work item.
- `status` (string): Lifecycle state such as `"open"`, `"in_progress"`, `"blocked"`, or `"done"`.
- `notes` (string, optional): Freeform context or decision details.
- `created_at` (string, ISO-8601): Timestamp when the agenda item was created.
- `updated_at` (string, ISO-8601, optional): Timestamp for the most recent update.

### `agenda_state.json`
A JSON document holding the live agenda state. The `items` array should be kept in sync with `agenda.ndjson` events when those events represent durable changes.
- `version` (number): Schema version for the state document.
- `next_id` (number): The ID that will be assigned to the next agenda item.
- `items` (array): Current agenda entries.

## Regeneration and reset
- These files are optional scaffolding. If they go missing or become corrupted, recreate them using the schemas above.
- To reset history, delete the NDJSON files (or truncate them to zero bytes) and repopulate from trusted run logs or start capturing new entries.
- To rebuild `agenda_state.json`, set `next_id` to the next available number and list any active items in `items`; otherwise keep it empty.
