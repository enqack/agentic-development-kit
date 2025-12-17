#!/usr/bin/env python3
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = ["## Active Hypotheses", "## Blockers", "## Deferred Risks"]
VALID_STATUSES = {"finished", "in-progress", "blocked", "not-started", "unknown"}

def die(msg: str) -> int:
  print(f"agenda_lint: ERROR: {msg}", file=sys.stderr)
  return 1

def main() -> int:
  path = Path("AGENDA.md")
  if not path.exists():
    return die("AGENDA.md not found")

  text = path.read_text(encoding="utf-8")

  for h in REQUIRED_HEADINGS:
    if h not in text:
      return die(f"missing required heading: {h}")

  statuses = re.findall(r"^\\s*Status:\\s*([A-Za-z\\-]+)\\s*$", text, flags=re.MULTILINE)
  if not statuses:
    return die("no agenda item statuses found (expected 'Status: not-started')")

  bad = sorted({s for s in statuses if s not in VALID_STATUSES})
  if bad:
    return die(f"invalid status values: {', '.join(bad)}")

  blocks = re.split(r"\\n\\s*\\n", text)
  for b in blocks:
    if re.search(r"^\\s*Status:\\s*finished\\s*$", b, flags=re.MULTILINE):
      m = re.search(r"^\\s*Evidence:\\s*(.+)\\s*$", b, flags=re.MULTILINE)
      if not m or not m.group(1).strip():
        return die("an item marked finished is missing non-empty Evidence:")

  print("agenda_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
