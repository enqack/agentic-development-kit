# Deep Thoughts Journal Index

This index ties together per-run journals stored at `artifacts/journal/<run-id>.md`. Keep the header stable and treat the entries as append-only so the narrative stays deterministic.

## Update helper
- Run `python tools/update_deep_thoughts.py` to append any newly discovered journals in lexicographic run-id order.
- Use `--check` to validate the index is current without writing to disk.
- Summaries are taken from the first non-empty line of each journal; edit the journal entry itself to change the summary.

## Rules
- Do not reorder or edit existing entries; append new runs to the end of the Entries section.
- Keep journal filenames aligned with their run IDs (for example, `2024-01-01T00-00-00Z.md`).
- Journals must live in `artifacts/journal/` so links remain stable.

## Entries (append-only)
