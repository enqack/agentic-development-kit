#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from textwrap import dedent
from typing import Iterable, List, Tuple

DOC_PATH = Path("docs/exec/deep-thoughts.md")
JOURNAL_DIR = Path("artifacts/journal")
ENTRIES_HEADER = "## Entries (append-only)"

BASE_DOCUMENT = dedent(
    """\
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
    """
)

ENTRY_PATTERN = re.compile(r"^- \[(?P<run>[^\]]+)\]\(artifacts/journal/[^\)]+\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append new journal entries to docs/exec/deep-thoughts.md")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with a non-zero status if the deep-thoughts index would change",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DOC_PATH,
        help="Path to the deep thoughts index (default: docs/exec/deep-thoughts.md)",
    )
    parser.add_argument(
        "--journal-dir",
        type=Path,
        default=JOURNAL_DIR,
        help="Directory containing journal files (default: artifacts/journal)",
    )
    return parser.parse_args()


def ensure_document(output: Path) -> str:
    if output.exists():
        return output.read_text(encoding="utf-8")
    return BASE_DOCUMENT


def extract_recorded_runs(doc_text: str) -> List[str]:
    in_entries = False
    runs: List[str] = []
    for line in doc_text.splitlines():
        stripped = line.strip()
        if stripped == ENTRIES_HEADER:
            in_entries = True
            continue
        if not in_entries or not stripped:
            continue
        match = ENTRY_PATTERN.match(stripped)
        if match:
            runs.append(match.group("run"))
    return runs


def discover_journals(journal_dir: Path) -> List[Tuple[str, Path]]:
    if not journal_dir.exists():
        return []
    return sorted((path.stem, path) for path in journal_dir.glob("*.md"))


def summarize_journal(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("#"):
            text = text.lstrip("#").strip()
        if text:
            return text
    return "Journal entry available"


def format_entry(run_id: str, summary: str) -> str:
    return f"- [{run_id}](artifacts/journal/{run_id}.md) — {summary}"


def append_entries(doc_text: str, entries: Iterable[str]) -> str:
    text = doc_text
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n".join(entries) + ("\n" if entries else "")


def main() -> int:
    args = parse_args()
    doc_text = ensure_document(args.output)
    if ENTRIES_HEADER not in doc_text:
        raise SystemExit(f"{args.output} is missing the entries header: {ENTRIES_HEADER}")

    recorded_runs = set(extract_recorded_runs(doc_text))
    journals = discover_journals(args.journal_dir)

    new_entries: List[str] = []
    for run_id, path in journals:
        if run_id in recorded_runs:
            continue
        summary = summarize_journal(path)
        new_entries.append(format_entry(run_id, summary))

    new_content = append_entries(doc_text, new_entries)
    output_exists = args.output.exists()
    changed = (new_content != doc_text) or not output_exists

    if args.check:
        return 1 if changed else 0

    if changed:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(new_content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
