#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"context_manifest_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  p = Path("artifacts/logs/context_manifest.md")
  if not p.exists():
    return die("missing artifacts/logs/context_manifest.md (prep-context must emit it)")

  txt = p.read_text(encoding="utf-8")

  # Minimal required fields (keep tolerant on formatting; strict on presence).
  required = [
    "timestamp",
    "operating mode",
    ".agentsignore",
    "files read",
  ]
  missing = [r for r in required if re.search(rf"\\b{re.escape(r)}\\b", txt, flags=re.IGNORECASE) is None]
  if missing:
    return die(f"context_manifest.md missing required fields: {', '.join(missing)}")

  # Disallow file:// in manifest (helps catch accidental absolute pointers).
  if "file://" in txt:
    return die("context_manifest.md contains file://; use repo-relative paths only")

  print("context_manifest_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
