import json
from pathlib import Path

import pytest

import os
import sys

# Add linters to path
sys.path.append(os.path.abspath("tools/linters"))
import plan_lint


def test_missing_plan_file(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)

  rc = plan_lint.main(["plan_lint"])
  captured = capsys.readouterr()

  assert rc == 1
  assert "implementation_plan.json not found" in captured.err


def test_run_mode_missing_artifact(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)

  rc = plan_lint.main(["plan_lint", "--run"])
  captured = capsys.readouterr()

  assert rc == 1
  assert "no docs/exec/runs/**/implementation_plan.json found" in captured.err


def test_malformed_json(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  p = Path("implementation_plan.json")
  p.write_text("{ invalid", encoding="utf-8")

  rc = plan_lint.main(["plan_lint"])
  captured = capsys.readouterr()

  assert rc == 1
  assert "implementation_plan.json: Expecting property name enclosed in double quotes" in captured.err


def test_lint_obj_validation():
  with pytest.raises(ValueError):
    plan_lint.lint_obj({})
  with pytest.raises(ValueError):
    plan_lint.lint_obj({"meta": {}, "items": []})


def test_valid_plan_root(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  p = Path("implementation_plan.json")
  p.write_text(json.dumps({"meta": {}, "items": [{"task": "one"}]}), encoding="utf-8")

  rc = plan_lint.main(["plan_lint"])
  captured = capsys.readouterr()

  assert rc == 0
  assert "plan_lint: OK" in captured.out


def test_valid_plan_run_mode(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  run = Path("docs/exec/runs/run-1")
  run.mkdir(parents=True)
  (run / "implementation_plan.json").write_text(
    json.dumps({"meta": {}, "items": [{"task": "two"}]}), encoding="utf-8"
  )

  rc = plan_lint.main(["plan_lint", "--run"])
  captured = capsys.readouterr()

  assert rc == 0
  assert "docs/exec/runs/run-1/implementation_plan.json" in captured.out
