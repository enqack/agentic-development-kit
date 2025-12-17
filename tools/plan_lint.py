#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"plan_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def load(path: Path) -> dict:
  try:
    return json.loads(path.read_text(encoding="utf-8"))
  except FileNotFoundError:
    raise
  except Exception as e:
    raise ValueError(str(e))

def lint_obj(obj: object) -> None:
  if not isinstance(obj, dict) or "meta" not in obj or "items" not in obj:
    raise ValueError("plan missing meta/items")
  if not isinstance(obj["items"], list) or not obj["items"]:
    raise ValueError("plan items must be non-empty array")

def find_run_plan() -> Path | None:
  runs = Path("docs/exec/runs")
  if not runs.exists():
    return None
  for p in runs.rglob("implementation_plan.json"):
    if p.is_file():
      return p
  return None

def main(argv: list[str]) -> int:
  mode_run = False
  if len(argv) >= 2 and argv[1] == "--run":
    mode_run = True

  if mode_run:
    p = find_run_plan()
    if p is None:
      return die("no docs/exec/runs/**/implementation_plan.json found")
  else:
    p = Path("implementation_plan.json")
    if not p.exists():
      return die("implementation_plan.json not found")

  try:
    obj = load(p)
    lint_obj(obj)
  except FileNotFoundError:
    return die(f"{p.as_posix()} not found")
  except ValueError as e:
    return die(f"{p.as_posix()}: {e}")

  print(f"plan_lint: OK ({p.as_posix()})")
  return 0

if __name__ == "__main__":
  raise SystemExit(main(sys.argv))
