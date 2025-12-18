# Human Guide to the Agentic Development Kit

Welcome! This repository uses the Agentic Development Kit (ADK) to structure collaboration between humans and AI agents.

## 🚀 Getting Started

1.  **Install Dependencies**:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-verify.txt
    ```

2.  **Establish Intent**:
    Run `/establish-intent` to define what we are building.

## 🔄 Core Workflows

The ADK revolves around a disciplined **Plan -> Execute -> Verify** loop.

### 1. Planning
Triggers: `/plan-execution` or `/plan-hardening`
- The agent analyzes requirements and produces an `implementation_plan.md`.
- **Your Job**: Review the plan. Verify the hypotheses and safety checks.

### 2. Execution
- The agent writes code and tests.
- **Your Job**: Review artifacts and code changes.

### 3. Verification & Closure
- Run `tools/verify_all.sh` to ensure everything is green.
- Run `python3 tools/close_run.py <run-id>` to seal the run.
- **Result**: A "Deep Thoughts" journal entry is created in `artifacts/journal/`, summarizing the session.

## 🛑 Panic Mode
If the agent detects a missing strict precondition (like missing Intent), it will **Fail Closed**.
- It will stop immediately.
- It will ask you the "Canonical Intent Question" to get back on track.
- **Do not** try to override this. Just answer the question.

## 📂 Artifacts to Watch

- **`docs/intent/project_intent.md`**: The North Star of the project.
- **`docs/exec/runs/<run-id>/`**: Where the work happens (plans, reports, walkthroughs).
- **`artifacts/journal/`**: Narrative summaries of what the agent did.
- **`docs/exec/deep-thoughts.md`**: The chronological story of the project.
