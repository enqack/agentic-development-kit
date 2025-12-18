import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath("tools"))
import journal  # noqa: E402


def test_emit_journal_with_artifacts(tmp_path, capsys):
    run_dir = tmp_path / "docs/exec/runs/run-1"
    run_dir.mkdir(parents=True)
    (run_dir / "implementation_plan.json").write_text(
        json.dumps({
            "items": [
                {"id": "B", "status": "Done", "hypothesis": "B hyp", "evidence": {"required_artifacts": ["2.md", "1.md"]}},
                {"id": "A", "status": "Active", "hypothesis": "A hyp"},
            ]
        }),
        encoding="utf-8",
    )
    (run_dir / "walkthrough.md").write_text(
        "# Walkthrough\n\n## Lessons Learned\n- Lesson 2\n- Lesson 1\n",
        encoding="utf-8",
    )

    path = journal.emit_journal(run_dir)

    assert path == run_dir / "journal.json"
    data = json.loads(path.read_text())
    assert data["run"] == "run-1"
    assert list(data["artifacts"].keys()) == ["implementation_plan", "walkthrough"]
    assert [item["id"] for item in data["artifacts"]["implementation_plan"]["items"]] == ["A", "B"]
    assert data["artifacts"]["implementation_plan"]["items"][1]["evidence"] == ["1.md", "2.md"]
    assert data["artifacts"]["walkthrough"]["lessons"] == ["Lesson 2", "Lesson 1"]

    captured = capsys.readouterr()
    assert "wrote journal" in captured.out


def test_emit_journal_missing_sources(tmp_path, capsys):
    run_dir = tmp_path / "docs/exec/runs/run-2"
    run_dir.mkdir(parents=True)

    path = journal.emit_journal(run_dir)

    assert path is None
    assert not (run_dir / "journal.json").exists()
    captured = capsys.readouterr()
    assert "nothing to journal" in captured.out


def test_main_invalid_plan_json(tmp_path, capsys):
    run_dir = tmp_path / "docs/exec/runs/run-3"
    run_dir.mkdir(parents=True)
    (run_dir / "implementation_plan.json").write_text("{not-json", encoding="utf-8")

    rc = journal.main([str(run_dir)])

    captured = capsys.readouterr()
    assert rc == 1
    assert "invalid JSON" in captured.err
