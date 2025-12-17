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
    return die("implementation_plan.json not found (generate it via plan-execution)")

  plan = json.loads(plan_path.read_text(encoding="utf-8"))

  if not isinstance(plan, dict):
    return die("plan is not a JSON object")
  for k in ["meta", "items"]:
    if k not in plan:
      return die(f"missing top-level key: {k}")

  meta = plan["meta"]
  if not isinstance(meta, dict):
    return die("meta must be an object")
  for k in ["version", "generated_at", "operating_mode"]:
    if k not in meta:
      return die(f"meta missing key: {k}")

  items = plan["items"]
  if not isinstance(items, list) or len(items) == 0:
    return die("items must be a non-empty array")

  required_item_keys = ["id", "status", "hypothesis", "scope", "invariants", "tasks", "tests", "evidence"]
  for i, it in enumerate(items):
    if not isinstance(it, dict):
      return die(f"item[{i}] must be an object")
    for k in required_item_keys:
      if k not in it:
        return die(f"item[{i}] missing key: {k}")

  print("plan_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
