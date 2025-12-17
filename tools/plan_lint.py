#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"plan_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  plan_path = Path("implementation_plan.json")
  if not plan_path.exists():
    return die("implementation_plan.json not found")

  plan = json.loads(plan_path.read_text(encoding="utf-8"))
  if not isinstance(plan, dict):
    return die("plan is not an object")
  for k in ["meta", "items"]:
    if k not in plan:
      return die(f"missing top-level key: {k}")

  items = plan["items"]
  if not isinstance(items, list) or not items:
    return die("items must be non-empty array")

  print("plan_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
