#!/usr/bin/env python3
from pathlib import Path
from lint_common import die, ABS_PATH_RE, TRUNC_RE


def main() -> int:
  p = Path("docs/exec/lessons-learned.md")
  if not p.exists():
    return die("lessons_lint", "docs/exec/lessons-learned.md missing")

  txt = p.read_text(encoding="utf-8")

  if "# Lessons Learned" not in txt:
    return die("lessons_lint", "missing title")

  if "Evidence:" not in txt:
    return die("lessons_lint", "missing Evidence field in template or entries")

  if "file://" in txt:
    return die("lessons_lint", "lessons-learned.md contains file://; use repo-relative paths only")

  if ABS_PATH_RE.search(txt):
    return die("lessons_lint", "lessons-learned.md appears to contain an absolute path; use repo-relative paths only")

  if TRUNC_RE.search(txt):
    return die("lessons_lint", "lessons-learned.md contains '...'; do not truncate evidence pointers")

  print("lessons_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
