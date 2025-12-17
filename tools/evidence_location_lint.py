#!/usr/bin/env python3
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"evidence_location_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  bad = []
  tr = Path("artifacts/test_results")
  if tr.exists():
    for p in tr.glob("*lint*.log"):
      if p.is_file():
        bad.append(p.as_posix())

  if bad:
    return die("lint logs must be in artifacts/logs, but found under artifacts/test_results: " + ", ".join(bad))

  print("evidence_location_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
