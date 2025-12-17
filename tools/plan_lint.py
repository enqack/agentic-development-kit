#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"plan_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  p = Path("implementation_plan.json")
  if not p.exists():
    return die("implementation_plan.json not found")
  obj = json.loads(p.read_text(encoding="utf-8"))
  if not isinstance(obj, dict) or "meta" not in obj or "items" not in obj:
    return die("plan missing meta/items")
  if not isinstance(obj["items"], list) or not obj["items"]:
    return die("plan items must be non-empty array")
  print("plan_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
