#!/usr/bin/env python3
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"template_baseline_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  required = [
    Path(".gitignore"),
    Path("requirements.txt"),
    Path(".agentsignore"),
    Path("AGENTS.md"),
    Path("AGENDA.md"),
    Path(".agent"),
  ]
  missing = [str(p) for p in required if not p.exists()]
  if missing:
    return die("missing required template files/dirs: " + ", ".join(missing))

  print("template_baseline_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
