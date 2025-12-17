#!/usr/bin/env python3
import re
import sys
from pathlib import Path
import subprocess

def die(msg: str) -> int:
  print(f"post_verify_lint: ERROR: {msg}", file=sys.stderr)
  return 1

ABS_PATH_RE = re.compile(r"(^|\s)(/|[A-Za-z]:\\)")
TRUNC_RE = re.compile(r"\.\.\.")

def main() -> int:
  report = Path("artifacts/logs/post_verify_report.md")
  if not report.exists():
    return die("missing artifacts/logs/post_verify_report.md")

  txt = report.read_text(encoding="utf-8")

  required_headings = [
    "## Completed items",
    "## Items still open",
    "## Evidence",
  ]
  missing = [h for h in required_headings if h not in txt]
  if missing:
    return die(f"post_verify_report.md missing required headings: {', '.join(missing)}")

  if "file://" in txt:
    return die("post_verify_report.md contains file://; use repo-relative paths only")
  if ABS_PATH_RE.search(txt):
    return die("post_verify_report.md appears to contain an absolute path; use repo-relative paths only")
  if TRUNC_RE.search(txt):
    return die("post_verify_report.md contains '...'; do not truncate evidence pointers")

  # Cross-check with AGENDA status
  helper = Path("tools/post_verify_agenda_lint.py")
  if helper.exists():
    r = subprocess.run([sys.executable, str(helper)], capture_output=True, text=True)
    if r.returncode != 0:
      msg = r.stderr.strip() or r.stdout.strip() or "AGENDA cross-check failed"
      return die(msg)

  print("post_verify_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
