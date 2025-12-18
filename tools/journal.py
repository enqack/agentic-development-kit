#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


class JournalError(Exception):
    """Raised when journal emission fails."""


def die(msg: str) -> int:
    print(f"journal: ERROR: {msg}", file=sys.stderr)
    return 1


def note(msg: str):
    print(f"journal: {msg}")


def normalize_status(status: Optional[str]) -> str:
    normalized = (status or "").strip().lower()
    return normalized or "active"


def load_plan(plan_path: Path) -> Optional[Dict]:
    if not plan_path.exists():
        return None

    try:
        data = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise JournalError(f"invalid JSON in {plan_path}: {exc}") from exc
    except OSError as exc:
        raise JournalError(f"failed to read {plan_path}: {exc}") from exc

    items: List[Dict] = []
    for raw in data.get("items", []):
        evidence = raw.get("evidence", {}).get("required_artifacts", []) if isinstance(raw, Dict) else []
        entry = {
            "id": raw.get("id") if isinstance(raw, Dict) else None,
            "hypothesis": (raw.get("hypothesis") if isinstance(raw, Dict) else "") or "",
            "status": normalize_status(raw.get("status") if isinstance(raw, Dict) else None),
            "evidence": sorted({ev for ev in evidence if ev}),
        }
        items.append(entry)

    items.sort(key=lambda item: ("" if item["id"] is None else str(item["id"])))

    return {
        "path": plan_path.name,
        "items": items,
    }


def extract_lessons(walkthrough_path: Path) -> List[str]:
    content = walkthrough_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    lessons: List[str] = []
    in_lessons = False

    for line in lines:
        if line.startswith("#") and "lessons" in line.lower():
            in_lessons = True
            continue
        if in_lessons and line.startswith("#"):
            break
        if in_lessons and line.strip().startswith("- "):
            lessons.append(line.strip()[2:])

    return lessons


def load_walkthrough(walkthrough_path: Path) -> Optional[Dict]:
    if not walkthrough_path.exists():
        return None

    try:
        lessons = extract_lessons(walkthrough_path)
    except OSError as exc:
        raise JournalError(f"failed to read {walkthrough_path}: {exc}") from exc

    return {
        "path": walkthrough_path.name,
        "lessons": lessons,
    }


def build_journal(run_dir: Path) -> Optional[Dict]:
    artifacts: Dict[str, Dict] = {}

    plan_info = load_plan(run_dir / "implementation_plan.json")
    if plan_info is None:
        note(f"no implementation_plan.json found in {run_dir}; skipping plan capture")
    else:
        artifacts["implementation_plan"] = plan_info

    walkthrough_info = load_walkthrough(run_dir / "walkthrough.md")
    if walkthrough_info is None:
        note(f"no walkthrough.md found in {run_dir}; skipping walkthrough capture")
    else:
        artifacts["walkthrough"] = walkthrough_info

    if not artifacts:
        note(f"no recognized artifacts found in {run_dir}; nothing to journal")
        return None

    return {
        "run": run_dir.name,
        "artifacts": artifacts,
    }


def emit_journal(run_dir: Path) -> Optional[Path]:
    journal = build_journal(run_dir)
    if journal is None:
        return None

    journal_path = run_dir / "journal.json"
    try:
        journal_path.write_text(json.dumps(journal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError as exc:
        raise JournalError(f"failed to write {journal_path}: {exc}") from exc

    note(f"wrote journal to {journal_path}")
    return journal_path


def get_latest_run() -> Optional[Path]:
    runs_dir = Path("docs/exec/runs")
    if not runs_dir.exists():
        return None
    runs = sorted([d for d in runs_dir.iterdir() if d.is_dir()])
    return runs[-1] if runs else None


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv or sys.argv[1:]
    if argv:
        run_dir = Path(argv[0])
    else:
        run_dir = get_latest_run()
        if not run_dir:
            return die("no runs found")

    if not run_dir.exists():
        return die(f"run directory {run_dir} does not exist")

    try:
        emit_journal(run_dir)
    except JournalError as exc:
        return die(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
