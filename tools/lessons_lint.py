#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"lessons_lint: ERROR: {msg}", file=sys.stderr)
  return 1

ABS_PATH_RE = re.compile(r"(^|\\s)(/|[A-Za-z]:\\\\)")
TRUNC_RE = re.compile(r"\\.{3}")

def main() -> int:
  p = Path("docs/exec/lessons-learned.md")
  if not p.exists():
    return die("docs/exec/lessons-learned.md missing")

  txt = p.read_text(encoding="utf-8")

  if "# Lessons Learned" not in txt:
    return die("missing title")

  if "Evidence:" not in txt:
    return die("missing Evidence field in template or entries")

  if "file://" in txt:
    return die("lessons-learned.md contains file://; use repo-relative paths only")

  if ABS_PATH_RE.search(txt):
    return die("lessons-learned.md appears to contain an absolute path; use repo-relative paths only")

  if TRUNC_RE.search(txt):
    return die("lessons-learned.md contains '...'; do not truncate evidence pointers")

  print("lessons_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
