#!/usr/bin/env python3
"""Lint journal artifacts for required metadata and path hygiene."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable, List

from lint_common import ABS_PATH_RE, FILE_URL_RE

JOURNAL_DIR = Path("artifacts/journal")
REQUIRED_TITLE = "# Journal"
REQUIRED_DISCLAIMER = "> Journal entries are ephemeral and must not include secrets or sensitive data."
MAX_WORDS = 400
MAX_LINES = 40
HTTP_URL_RE = re.compile(r"https?://")


def collect_journals() -> list[Path]:
  if not JOURNAL_DIR.exists():
    return []
  return sorted(p for p in JOURNAL_DIR.glob("*.md") if p.is_file())


def check_paths(text: str, path: Path) -> Iterable[str]:
  if FILE_URL_RE.search(text):
    yield f"{path}: contains file:// URL; use repo-relative paths only"
  if HTTP_URL_RE.search(text):
    yield f"{path}: contains external URL; use repo-relative paths only"
  if ABS_PATH_RE.search(text):
    yield f"{path}: contains absolute path; use repo-relative paths only"


def lint_journal(path: Path) -> List[str]:
  errors: List[str] = []
  text = path.read_text(encoding="utf-8")

  if REQUIRED_TITLE not in text:
    errors.append(f"{path}: missing required '{REQUIRED_TITLE}' heading")
  if REQUIRED_DISCLAIMER not in text:
    errors.append(f"{path}: missing required disclaimer '{REQUIRED_DISCLAIMER}'")

  words = text.split()
  if len(words) > MAX_WORDS:
    errors.append(f"{path}: exceeds {MAX_WORDS} words ({len(words)})")

  lines = text.splitlines()
  if len(lines) > MAX_LINES:
    errors.append(f"{path}: exceeds {MAX_LINES} lines ({len(lines)})")

  errors.extend(check_paths(text, path))
  return errors


def main() -> int:
  journals = collect_journals()
  if not journals:
    print("journal_lint: no journal entries found; skipping")
    return 0

  all_errors: List[str] = []
  for path in journals:
    all_errors.extend(lint_journal(path))

  if all_errors:
    for err in all_errors:
      print(f"journal_lint: ERROR: {err}", file=sys.stderr)
    return 1

  for path in journals:
    print(f"journal_lint: OK ({path.as_posix()})")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
