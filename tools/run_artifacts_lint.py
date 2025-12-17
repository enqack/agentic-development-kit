#!/usr/bin/env python3
import sys
from pathlib import Path

def die(msg: str) -> int:
  print(f"run_artifacts_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def find_run_artifact(filename: str) -> Path | None:
  runs = Path("docs/exec/runs")
  if not runs.exists():
    return None
  for p in runs.rglob(filename):
    if p.is_file():
      return p
  return None

def main() -> int:
  # Require at least one run folder with these artifacts.
  plan = find_run_artifact("implementation_plan.json")
  w = find_run_artifact("walkthrough.md")
  if plan is None:
    return die("no docs/exec/runs/**/implementation_plan.json found")
  if w is None:
    return die("no docs/exec/runs/**/walkthrough.md found")

  # Root hygiene checks
  bad = []
  for name in ["implementation_plan.md", "implementation_plan.json", "walkthrough.md"]:
    if Path(name).exists():
      bad.append(name)
  # Any *.resolved* or *.metadata.json at root
  for p in Path(".").glob("*.resolved*"):
    bad.append(p.name)
  for p in Path(".").glob("*.metadata.json"):
    bad.append(p.name)

  if bad:
    return die("root contains forbidden execution artifacts: " + ", ".join(sorted(set(bad))))

  print("run_artifacts_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
