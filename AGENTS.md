# Panic Handling

## Fail-closed behavior

When a workflow cannot proceed due to a missing precondition, treat it as a **panic** and fail closed.

### Mandatory panic response

On any fail-closed precondition violation, the agent MUST:

1. State the missing precondition (one line).
2. Immediately initiate the remedial workflow interaction.
3. Default remedial workflow: `establish-intent` (unless a more specific remedial workflow is explicitly required).
4. Write/update required artifacts.
5. Resume the originally requested workflow.

### Interaction constraints

- Do NOT present override options.
- Do NOT ask the user to confirm compliance with workspace constraints.
- Do NOT offer to “skip the check”.
- Keep the precondition message short; prioritize asking the intent question immediately.

### Intent question (canonical)

Use this exact question when establishing or refreshing intent:

"What are you trying to produce in this repo (software, book, research notes, something else), and what does 'done' look like for the first milestone?"
