# Safe Antigravity IDE Configuration

This document describes a **safe configuration** for using the Antigravity IDE with
the agentic-development-kit template. It focuses on minimizing unintended access,
destructive operations, and agent behaviors that conflict with workspace policies.

> Note: Antigravity’s ignore and access controls (e.g., `.gitignore`, `.aiexclude`)
> are *not strong security boundaries*. They serve as **context filters**, not
> enforced OS permissions. Always pair them with human review and environment
> isolation.

---

## 1) Treat Workspace Boundaries as Policy, Not Security

- Ensure your project folder is explicitly added as the active workspace.
- Some users report the agent not recognizing context unless the folder is a Git
  repository (`git init`) or explicitly added via the IDE workspace UI.
- Avoid symbolic links from the workspace to sensitive directories.

---

## 2) Restrict Terminal and Command Execution

Antigravity agents may execute terminal commands.

Recommended configuration:
- Disable automatic terminal execution.
- Require manual approval for all command execution.
- Maintain a deny list for destructive commands such as:
  - `rm`, `rmdir`, `del`, `sudo`, `curl`, `wget`

---

## 3) Prefer Dedicated Agent Context Exclusion

Do not rely on `.gitignore` alone.

- Use `.aiexclude` (or equivalent) to exclude files from agent context.
- Treat ignore files as *context filters*, not permission systems.

Example `.aiexclude`:
```
secrets.json
*.key
.env
```

---

## 4) Enforce Human Review

Configure the IDE to require confirmation before:
- Writing files outside expected directories
- Running commands with filesystem side effects
- Modifying configuration or security-sensitive files

---

## 5) Use Isolated Environments

For maximum safety:
- Run Antigravity inside a container or virtual machine
- Mount only the project workspace into the environment
- Avoid running agents on hosts with sensitive data

---

## 6) Audit Agent Activity

- Review logs and proposed actions
- Inspect generated artifacts for unexpected access
- Do not assume ignore rules fully prevent access

---

## 7) Safe Mode Checklist

- Workspace access enabled
- Non-workspace access disabled
- Terminal auto-execution disabled
- `.aiexclude` configured (the template ships one that fences off `.agent/`, `tools/`, and run artifacts)
- Human approval required for risky actions
- Prefer container or VM execution

---

## Disclaimer

Antigravity IDE access controls are evolving and should not be treated as a complete
security boundary. Combine IDE settings with human oversight and environment
isolation for safe operation.
