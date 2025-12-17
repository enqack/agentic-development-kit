#!/usr/bin/env python3
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"lessons_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  p = Path("docs/exec/lessons-learned.md")
  if not p.exists():
    return die("docs/exec/lessons-learned.md missing")
  txt = p.read_text(encoding="utf-8")
  if "# Lessons Learned" not in txt:
    return die("missing title")
  if "Evidence:" not in txt:
    return die("missing Evidence field in template or entries")
  print("lessons_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
