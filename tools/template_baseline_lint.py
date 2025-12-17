#!/usr/bin/env python3
import sys
from pathlib import Path
from lint_common import die


def main() -> int:
  # Allow either requirements-verify.txt (preferred) or legacy requirements.txt.
  req_ok = Path("requirements-verify.txt").exists() or Path("requirements.txt").exists()
  if not req_ok:
    return die("template_baseline_lint", "missing verification requirements file: requirements-verify.txt (preferred) or requirements.txt (legacy)")

  required = [
    Path(".gitignore"),
    Path(".agentsignore"),
    Path("AGENTS.md"),
    Path("AGENDA.md"),
    Path(".agent"),
  ]
  missing = [str(p) for p in required if not p.exists()]
  if missing:
    return die("template_baseline_lint", "missing required template files/dirs: " + ", ".join(missing))

  print("template_baseline_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
