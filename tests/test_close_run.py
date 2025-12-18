import unittest
import tempfile
import shutil
import json
from pathlib import Path
import sys
import os

# We need to import close_run, but it depends on file system structure.
# We'll test the extraction and update logic primarily.

# Mocking the imports or using subprocess might be better for full E2E, 
# but let's try to import functions first.
sys.path.append(os.path.abspath("tools"))
from close_run import extract_lessons, update_global_lessons

class TestCloseRun(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
        
    def test_extract_lessons(self):
        run_dir = Path("docs/exec/runs/test_run")
        run_dir.mkdir(parents=True)
        wt = run_dir / "walkthrough.md"
        wt.write_text("# Walkthrough\n\n## Lessons Learned\n- Lesson 1\n- Lesson 2\n\n## Other\n", encoding="utf-8")
        
        lessons = extract_lessons(run_dir)
        self.assertEqual(lessons, ["Lesson 1", "Lesson 2"])
        
    def test_extract_lessons_empty(self):
        run_dir = Path("docs/exec/runs/test_run")
        run_dir.mkdir(parents=True)
        wt = run_dir / "walkthrough.md"
        wt.write_text("# Walkthrough\n\nNo lessons section\n", encoding="utf-8")
        
        lessons = extract_lessons(run_dir)
        self.assertEqual(lessons, [])

    def test_update_global_lessons(self):
        global_dir = Path("docs/exec")
        global_dir.mkdir(parents=True)
        
        lessons = ["New Lesson"]
        added = update_global_lessons(lessons, "test_run")
        
        f = global_dir / "lessons-learned.md"
        self.assertTrue(f.exists())
        content = f.read_text()
        self.assertEqual(added, 1)
        self.assertIn("- New Lesson (from [test_run](runs/test_run/walkthrough.md))", content)

    def test_update_global_lessons_dedup(self):
        global_dir = Path("docs/exec")
        global_dir.mkdir(parents=True)

        existing = global_dir / "lessons-learned.md"
        existing.write_text(
            "# Lessons Learned\n\n- Old Lesson (from [old_run](runs/old_run/walkthrough.md))\n",
            encoding="utf-8",
        )

        added = update_global_lessons(["Old Lesson", "New Lesson"], "new_run")

        content = existing.read_text()
        self.assertEqual(added, 1)
        self.assertEqual(content.count("Old Lesson"), 1)
        self.assertIn("- New Lesson (from [new_run](runs/new_run/walkthrough.md))", content)

if __name__ == "__main__":
    unittest.main()
