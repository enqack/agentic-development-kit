#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ALLOWED = {"software", "writing", "research", "art", "mixed", "unknown"}

def die(msg: str) -> int:
  print(f"intent_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def parse_frontmatter(txt: str) -> dict[str, str]:
  # Minimal YAML frontmatter parser for key: value pairs.
  m = re.match(r"(?s)\A---\s*\n(.*?)\n---\s*\n", txt)
  if not m:
    return {}
  block = m.group(1)
  out: dict[str, str] = {}
  for line in block.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
      continue
    if ":" not in line:
      continue
    k, v = line.split(":", 1)
    out[k.strip()] = v.strip().strip('"').strip("'")
  return out

def main() -> int:
  p = Path("docs/intent/project_intent.md")
  if not p.exists():
    return die("missing docs/intent/project_intent.md (run establish-intent first)")

  txt = p.read_text(encoding="utf-8")
  fm = parse_frontmatter(txt)
  if not fm:
    return die("project_intent.md missing YAML frontmatter (--- ... ---)")

  required = ["primary_domain", "deliverable", "first_milestone_done", "constraints", "non_goals"]
  missing = [k for k in required if k not in fm or fm[k] == ""]
  if missing:
    return die("project_intent.md missing required keys: " + ", ".join(missing))

  dom = fm["primary_domain"]
  if dom not in ALLOWED:
    return die(f"primary_domain must be one of {sorted(ALLOWED)}, got '{dom}'")

  print("intent_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
