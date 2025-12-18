import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.append(os.path.abspath("tools"))
import aggregate_history


class AggregateHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self) -> None:
        os.chdir(self.old_cwd)
        shutil.rmtree(self.tmpdir)

    def _write_history(self, records):
        path = Path("docs/exec/history.ndjson")
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(r, sort_keys=True, separators=(",", ":")) for r in records]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_builds_history_from_run_and_agenda(self):
        run_dir = Path("docs/exec/runs/run1")
        run_dir.mkdir(parents=True)

        plan = {
            "meta": {"version": "1.0", "generated_at": "now", "operating_mode": "full-execution"},
            "items": [
                {
                    "id": "HYP-0001",
                    "status": "proposed",
                    "hypothesis": "Hypothesis about stability",
                    "scope": {"components": ["core"], "files": []},
                    "invariants": ["always"],
                    "tasks": [
                        {"step": 1, "description": "do", "done_definition": "done"},
                    ],
                    "tests": {"unit": [], "integration": [], "build": []},
                    "evidence": {
                        "required_artifacts": [
                            "docs/exec/runs/run1/walkthrough.md",
                            str(Path.cwd() / "docs/exec/runs/run1/plan.md"),
                            "artifacts/logs/result.txt",
                            "https://example.com/outside",
                        ]
                    },
                }
            ],
        }
        (run_dir / "implementation_plan.json").write_text(json.dumps(plan), encoding="utf-8")

        walkthrough = """# Walkthrough\n\nHypothesis: Run observation\n- HYP-0001 - initial note\nEvidence: artifacts/logs/result.txt\nSee docs/exec/runs/run1/walkthrough.md\n"""
        (run_dir / "walkthrough.md").write_text(walkthrough, encoding="utf-8")

        report = """Run ID: 2024-01-01_HYP-0001\nStatus: finished\nEvidence: docs/exec/runs/run1/walkthrough.md\n"""
        (run_dir / "post_verify_report.md").write_text(report, encoding="utf-8")

        agenda_state = {
            "items": [
                {
                    "id": "HYP-0002",
                    "summary": "Need data",
                    "status": "blocked",
                    "evidence": ["docs/exec/runs/run1/walkthrough.md"],
                }
            ]
        }
        Path("docs/exec").mkdir(parents=True, exist_ok=True)
        (Path("docs/exec") / "agenda_state.json").write_text(json.dumps(agenda_state), encoding="utf-8")

        exit_code = aggregate_history.main(["--output", "docs/exec/history.ndjson"])
        self.assertEqual(exit_code, 0)

        history_path = Path("docs/exec/history.ndjson")
        self.assertTrue(history_path.exists())
        records = [json.loads(l) for l in history_path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(records), 2)

        hyp = records[0]
        self.assertEqual(hyp["record_type"], "hypothesis")
        self.assertEqual(hyp["id"], "HYP-0001")
        self.assertEqual(hyp["claim"], "Hypothesis about stability")
        self.assertEqual(hyp["status"], "finished")
        self.assertEqual(hyp["first_seen_run"], "run1")
        self.assertEqual(hyp["last_seen_run"], "run1")
        self.assertEqual(
            hyp["evidence"],
            [
                "artifacts/logs/result.txt",
                "docs/exec/runs/run1/plan.md",
                "docs/exec/runs/run1/walkthrough.md",
            ],
        )

        agenda = records[1]
        self.assertEqual(agenda["record_type"], "agenda")
        self.assertEqual(agenda["id"], "HYP-0002")
        self.assertEqual(agenda["summary"], "Need data")
        self.assertEqual(agenda["status"], "blocked")
        self.assertEqual(agenda["first_seen_run"], "unknown")
        self.assertEqual(agenda["last_seen_run"], "unknown")
        self.assertEqual(agenda["evidence"], ["docs/exec/runs/run1/walkthrough.md"])

    def test_merges_existing_history_and_supports_check_mode(self):
        Path("docs/exec/runs/run2").mkdir(parents=True, exist_ok=True)
        Path("docs/exec").mkdir(parents=True, exist_ok=True)

        existing = [
            {
                "record_type": "hypothesis",
                "id": "HYP-0001",
                "claim": "Old claim",
                "status": "active",
                "first_seen_run": "init",
                "last_seen_run": "init",
                "evidence": ["docs/exec/runs/init/walkthrough.md"],
            },
            {
                "record_type": "agenda",
                "id": "HYP-0003",
                "summary": "Existing",
                "status": "in-progress",
                "first_seen_run": "init",
                "last_seen_run": "init",
                "evidence": [],
            },
        ]
        self._write_history(existing)

        plan = {
            "meta": {"version": "1.0", "generated_at": "later", "operating_mode": "full-execution"},
            "items": [
                {
                    "id": "HYP-0001",
                    "hypothesis": "Updated claim",
                    "scope": {"components": ["core"], "files": []},
                    "invariants": ["always"],
                    "tasks": [
                        {"step": 1, "description": "step", "done_definition": "done"},
                    ],
                    "tests": {"unit": [], "integration": [], "build": []},
                    "evidence": {"required_artifacts": ["docs/exec/runs/run2/walkthrough.md"]},
                }
            ],
        }
        Path("docs/exec/runs/run2/implementation_plan.json").write_text(json.dumps(plan), encoding="utf-8")

        walkthrough = """# Walkthrough\nHYP-0001: updated note\nEvidence: docs/exec/runs/run2/walkthrough.md\n"""
        Path("docs/exec/runs/run2/walkthrough.md").write_text(walkthrough, encoding="utf-8")

        agenda_state = {
            "items": [
                {
                    "id": "HYP-0003",
                    "summary": "Updated summary",
                    "status": "finished",
                    "first_seen_run": "init",
                    "last_seen_run": "run2",
                    "evidence": "docs/exec/runs/run2/walkthrough.md",
                }
            ]
        }
        Path("docs/exec/agenda_state.json").write_text(json.dumps(agenda_state), encoding="utf-8")

        self.assertEqual(aggregate_history.main(["--output", "docs/exec/history.ndjson", "--check"]), 1)

        exit_code = aggregate_history.main(["--output", "docs/exec/history.ndjson"])
        self.assertEqual(exit_code, 0)

        records = [json.loads(l) for l in Path("docs/exec/history.ndjson").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(records), 2)

        hyp = next(r for r in records if r["record_type"] == "hypothesis")
        self.assertEqual(hyp["claim"], "Updated claim")
        self.assertEqual(hyp["status"], "active")
        self.assertEqual(hyp["first_seen_run"], "init")
        self.assertEqual(hyp["last_seen_run"], "run2")
        self.assertEqual(
            hyp["evidence"],
            [
                "docs/exec/runs/init/walkthrough.md",
                "docs/exec/runs/run2/walkthrough.md",
            ],
        )

        agenda = next(r for r in records if r["record_type"] == "agenda")
        self.assertEqual(agenda["id"], "HYP-0003")
        self.assertEqual(agenda["summary"], "Updated summary")
        self.assertEqual(agenda["status"], "finished")
        self.assertEqual(agenda["first_seen_run"], "init")
        self.assertEqual(agenda["last_seen_run"], "run2")
        self.assertEqual(agenda["evidence"], ["docs/exec/runs/run2/walkthrough.md"])

        self.assertEqual(aggregate_history.main(["--output", "docs/exec/history.ndjson", "--check"]), 0)


    def test_ingests_journals_and_generates_narrative(self):
        # Create a journal file
        Path("artifacts/journal").mkdir(parents=True)
        (Path("artifacts/journal") / "run-j1.md").write_text(
            "### Header\nContent for J1\n", encoding="utf-8"
        )
        
        exit_code = aggregate_history.main([
            "--output", "docs/exec/history.ndjson",
            "--narrative", "docs/exec/deep-thoughts.md"
        ])
        
        self.assertEqual(exit_code, 0)
        
        # Verify history record
        history = [json.loads(l) for l in Path("docs/exec/history.ndjson").read_text(encoding="utf-8").splitlines()]
        journal_rec = next(r for r in history if r["record_type"] == "journal")
        self.assertEqual(journal_rec["timestamp"], "run-j1")
        self.assertEqual(journal_rec["summary"], "Journal entry for run-j1")
        self.assertEqual(journal_rec["evidence"], ["artifacts/journal/run-j1.md"])
        
        # Verify narrative
        narrative = Path("docs/exec/deep-thoughts.md").read_text(encoding="utf-8")
        assert "### Header" in narrative
        assert "Content for J1" in narrative


if __name__ == "__main__":
    unittest.main()
