#!/usr/bin/env python3
"""Lint design journal artifacts in artifacts/journal/.

This script enforces structure and hygiene for design journal markdown files.
It validates a required header, presence of an editor's note disclaimer, word
and line length limits, optional sentience-leaning phrasing checks, and path
hygiene using lint_common utilities.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List

from lint_common import die, validate_paths


SCRIPT_NAME = "journal_lint"
JOURNAL_DIR = Path("artifacts/journal")
REQUIRED_HEADER = "# Design Journal"
EDITOR_NOTE_PHRASE = "editor's note"
WORD_LIMIT = 250
MAX_LINE_LENGTH = 120
SENTIENCE_PATTERNS = [
    (re.compile(r"\bI felt\b", re.IGNORECASE), "I felt"),
    (re.compile(r"\bI believed\b", re.IGNORECASE), "I believed"),
]


def iter_journal_files() -> Iterable[Path]:
  if not JOURNAL_DIR.exists():
    return []
  return sorted(JOURNAL_DIR.glob("*.md"))


def count_words(text: str) -> int:
  return len(re.findall(r"\b[\w'-]+\b", text))


def lint_file(path: Path, check_sentience: bool) -> List[str]:
  errors: List[str] = []
  try:
    text = path.read_text(encoding="utf-8")
  except Exception as exc:  # noqa: BLE001 - surface read failures directly
    return [f"{path}: failed to read: {exc}"]

  lines = text.splitlines()
  if not lines:
    return [f"{path}: file is empty"]

  header = lines[0].strip()
  if header != REQUIRED_HEADER:
    errors.append(f"{path}: first line must be '{REQUIRED_HEADER}'")

  if EDITOR_NOTE_PHRASE not in text.lower():
    errors.append(f"{path}: missing editor's note disclaimer containing '{EDITOR_NOTE_PHRASE}'")

  word_count = count_words(text)
  if word_count > WORD_LIMIT:
    errors.append(f"{path}: word count {word_count} exceeds limit {WORD_LIMIT}")

  for lineno, line in enumerate(lines, start=1):
    if len(line) > MAX_LINE_LENGTH:
      errors.append(
          f"{path}:{lineno}: line length {len(line)} exceeds limit {MAX_LINE_LENGTH}"
      )

    path_error = validate_paths(line)
    if path_error:
      errors.append(f"{path}:{lineno}: {path_error}")

    if check_sentience:
      for pattern, phrase in SENTIENCE_PATTERNS:
        if pattern.search(line):
          errors.append(
              f"{path}:{lineno}: avoid sentience-leaning phrase "
              f"""'{phrase}'"""
          )

  return errors


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description="Lint design journal artifacts")
  parser.add_argument(
      "--allow-sentience",
      action="store_true",
      help="Permit sentience-leaning phrasing instead of rejecting it",
  )
  args = parser.parse_args(argv)

  files = list(iter_journal_files())
  if not files:
    print(f"{SCRIPT_NAME}: no journal entries found; skipping")
    return 0

  all_errors: List[str] = []
  for path in files:
    all_errors.extend(lint_file(path, check_sentience=not args.allow_sentience))

  if all_errors:
    for err in all_errors:
      print(f"{SCRIPT_NAME}: ERROR: {err}", file=sys.stderr)
    return die(SCRIPT_NAME, "journal checks failed")

  print(f"{SCRIPT_NAME}: OK ({len(files)} file(s) checked)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
