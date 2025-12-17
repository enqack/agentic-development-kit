#!/usr/bin/env python3
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"post_verify_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  report = Path("artifacts/logs/post_verify_report.md")
  if not report.exists():
    return die("missing artifacts/logs/post_verify_report.md")
  txt = report.read_text(encoding="utf-8")
  required = ["Completed items", "Items still open", "Evidence"]
  missing = [r for r in required if r not in txt]
  if missing:
    return die(f"post_verify_report.md missing: {', '.join(missing)}")
  print("post_verify_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
