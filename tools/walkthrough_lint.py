#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"walkthrough_lint: ERROR: {msg}", file=sys.stderr)
  return 1

ABS_PATH_RE = re.compile(r"(^|\s)(/|[A-Za-z]:\\)")
TRUNC_RE = re.compile(r"\.\.\.")
FILE_URL_RE = re.compile(r"file://")

def find_walkthrough() -> Path | None:
  root = Path("walkthrough.md")
  if root.exists():
    return root
  runs = Path("docs/exec/runs")
  if not runs.exists():
    return None
  for p in runs.rglob("walkthrough.md"):
    if p.is_file():
      return p
  return None

def main() -> int:
  p = find_walkthrough()
  if p is None:
    return die("no walkthrough.md found (expected docs/exec/runs/**/walkthrough.md)")

  # Root walkthrough is forbidden by v5.3, but we keep a specific message here.
  if p.resolve().name == "walkthrough.md" and p.parent.resolve() == Path(".").resolve():
    return die("walkthrough.md is at repo root; must be under docs/exec/runs/<run-id>/")

  txt = p.read_text(encoding="utf-8")

  if FILE_URL_RE.search(txt):
    return die("walkthrough contains file:// URLs; use repo-relative paths only")
  if ABS_PATH_RE.search(txt):
    return die("walkthrough contains an absolute path; use repo-relative paths only")
  if TRUNC_RE.search(txt):
    return die("walkthrough contains '...'; do not truncate evidence pointers")
  if re.search(r"Artifacts\s*\(Brain\)", txt, flags=re.IGNORECASE):
    return die("walkthrough contains 'Artifacts (Brain)'; workspace artifacts only")

  print(f"walkthrough_lint: OK ({p.as_posix()})")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
