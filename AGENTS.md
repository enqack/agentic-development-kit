# Global Preconditions

## Project intent is mandatory

Until `docs/intent/project_intent.md` exists, the only permitted workflow is:

- `establish-intent`

All other workflows MUST fail closed and direct the user to run `establish-intent` first.

Rationale:
- Prevents premature domain assumptions (software vs writing vs research vs art).
- Keeps automation safe, predictable, and user-aligned.
