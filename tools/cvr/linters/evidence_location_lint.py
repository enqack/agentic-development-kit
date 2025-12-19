#!/usr/bin/env python3
import sys
from pathlib import Path

# Import canonical paths
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from tools.cvr import paths
from lint_common import die


def main() -> int:
  bad = []
  tr = paths.TEST_RESULTS_DIR
  if tr.exists():
    for p in tr.glob("*lint*.log"):
      if p.is_file():
        bad.append(p.as_posix())

  if bad:
    return die("evidence_location_lint", "lint logs must be in artifacts/logs, but found under artifacts/test_results: " + ", ".join(bad))


  print("evidence_location_lint: OK")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
