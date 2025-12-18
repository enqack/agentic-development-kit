---
name: commit-message
description: Generate a Conventional Commit message based on unstaged changes and then stage & commit.
---

# Commit Message Generator

Describe: A structured workflow that guides an agent to review the diff since the last commit, draft a Conventional Commit message, present it for approval, and then stage & commit.

## Commit Message Format
Commit messages must follow the **Conventional Commits** format:
```
<type>(<scope>): <short summary>

<body — optional, detailed description>

<footer — optional, e.g., issue references, breaking changes>
```
Types (examples): `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`

## Steps

1. **Review Diff**
   ```
   Review all unstaged changes since the last commit and summarize the edits.
   ```

2. **Draft Header**
   ```
   Based on the diff summary, propose a Conventional Commit header:
   <type>(<scope>): <short imperative summary>
   ```

3. **Draft Body**
   ```
   Provide an optional body explaining why changes were made and any context.
   ```

4. **Draft Footer**
   ```
   Suggest an optional footer with references, tickets, or breaking changes.
   ```

5. **Present Draft**
   ```
   Display the full proposed commit message for user approval, editing, or rewrite.
   ```

6. **Stage & Commit**
   ```
   Stage modified files and commit using the approved message.
   ```
