from pathlib import Path

import workflow_intent_lint


def test_missing_workflows(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)

  rc = workflow_intent_lint.main()
  captured = capsys.readouterr()

  assert rc == 1
  assert "missing .agent/workflows directory" in captured.err


def test_workflow_missing_intent(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  wf_dir = Path(".agent/workflows")
  wf_dir.mkdir(parents=True)
  (wf_dir / "build.md").write_text("Steps only", encoding="utf-8")

  rc = workflow_intent_lint.main()
  captured = capsys.readouterr()

  assert rc == 1
  assert "workflows missing intent requirement" in captured.err


def test_compliant_workflows(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  wf_dir = Path(".agent/workflows")
  wf_dir.mkdir(parents=True)
  (wf_dir / "establish-intent.md").write_text("bootstrap", encoding="utf-8")
  (wf_dir / "work.md").write_text(
    "Precondition: artifacts/intent/project_intent.md must exist", encoding="utf-8"
  )

  rc = workflow_intent_lint.main()
  captured = capsys.readouterr()

  assert rc == 0
  assert "workflow_intent_lint: OK" in captured.out
