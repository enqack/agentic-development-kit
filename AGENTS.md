# Software Development Architect (Agent Contract)

This document is **normative, enforceable, auditable, and durable**.

## Normative Language

- **MUST / MUST NOT**: absolute requirements
- **SHOULD / SHOULD NOT**: strong defaults; deviation requires justification
- **MAY**: optional behavior

When constraints cannot be satisfied, the agent MUST **fail closed**.

## Terminology

- **Workspace**: this repository root
- **Artifact**: durable evidence output (plans, logs, test results, diffs)
- **Non-trivial work**: changes that affect behavior, APIs, data, security, architecture, or failure modes

## Epistemic Contract

All outputs are working theories validated only through evidence.

For non-trivial work, the agent MUST:
- record hypotheses in `implementation_plan.*`
- define invariants and failure criteria
- propose tests and evidence artifacts

## Fail-Closed Semantics

Fail closed means:
- no code/config modifications
- no partial artifacts written
- halt with an explicit explanation

## Core Workflow (Authoritative)

All non-trivial work MUST follow:

1. Perceive – inspect current state and context
2. Plan – produce `implementation_plan.md` and `implementation_plan.json`
3. Act – apply changes (only in full-execution mode)
4. Prove or Falsify – run tests and collect evidence
5. Summarize – produce `walkthrough.md`
6. Reconcile – run `post-verify` and emit reconciliation report
7. Reflect – update `docs/exec/lessons-learned.md` (+ optional `docs/exec/cursed-knowledge.md`)

Absence of proof is unresolved work.

## Operating Modes

- **full-execution**: filesystem writes + command execution; artifacts + tests REQUIRED
- **design-only**: plans only; MUST NOT claim runtime evidence
- **audit-only**: evaluate existing code/docs; MUST NOT claim runtime evidence

If guarantees cannot be met, fail closed or downgrade mode.

## Artifacts (Canonical)

```
artifacts/
├── logs/
├── diffs/
└── test_results/
```

## Agent Ignore

Agents MUST respect `.agentsignore` when selecting files to read as context.
If `.agentsignore` is missing, fail closed.

## AGENDA.md Minimum

AGENDA.md MUST contain:
- Active hypotheses
- Blockers
- Deferred risks
