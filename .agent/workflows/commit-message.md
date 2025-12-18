---
description: Generate a Conventional Commit message from changes since the last commit
operating_mode: audit-only | design-only
artifacts_required:
  - docs/intent/project_intent.md
---

# commit-message

Precondition:
- `docs/intent/project_intent.md` exists.

If precondition is not met:
- fail closed (panic) and immediately initiate `establish-intent` by asking:
  - "What are you trying to produce in this repo (software, book, research notes, something else), and what does 'done' look like for the first milestone?"
- write `docs/intent/project_intent.md`
- then continue with this workflow

## Commit message format (normative)

Use **Conventional Commits**:

```
<type>(<scope>): <short summary>

<body>   # optional: why + what changed
<footer> # optional: Fixes #123, BREAKING CHANGE: ...
```

Allowed `type` values (preferred): `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`.

Rules:
- Summary line is imperative mood, <= ~72 chars, no trailing period.
- `scope` is optional; use a short subsystem name if it clarifies impact.
- If change is breaking, include `!` after type/scope (e.g., `feat(api)!:`) and add `BREAKING CHANGE:` in footer.

## Steps

1. **Review diff since last commit**
   - Read and summarize the workspace diff vs `HEAD`.
   - Identify: user-facing behavior changes, refactors, tests/docs, build/CI, and any breaking changes.

2. **Propose message candidates**
   - Produce 2–3 candidate commit messages (header + optional body/footer) matching the format above.
   - Prefer the most semantically accurate `type`.
   - If multiple concerns exist, choose the dominant one and mention secondary changes in the body.

3. **Approval gate**
   - Present the top candidate as the default.
   - Ask the user to approve or edit the message (no committing yet).

4. **Stage and commit (only after approval)**
   - Stage the intended files.
   - Commit using the approved message exactly.
