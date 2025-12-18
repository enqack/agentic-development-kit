from pathlib import Path

import journal_lint


def _write_journal(root: Path, content: str, name: str = "entry-1.md") -> Path:
  journal_dir = root / "artifacts/journal"
  journal_dir.mkdir(parents=True, exist_ok=True)
  p = journal_dir / name
  p.write_text(content, encoding="utf-8")
  return p


def test_no_journal_files(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)

  rc = journal_lint.main()
  captured = capsys.readouterr()

  assert rc == 0
  assert "no journal entries found" in captured.out


def test_missing_header_or_disclaimer(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  _write_journal(tmp_path, "Some notes without required metadata.")

  rc = journal_lint.main()
  captured = capsys.readouterr()

  assert rc == 1
  assert journal_lint.REQUIRED_TITLE in captured.err
  assert "missing required disclaimer" in captured.err


def test_exceeds_limits(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  wordy = "word " * (journal_lint.MAX_WORDS + 10)
  tall = "\n".join("line" for _ in range(journal_lint.MAX_LINES + 5))
  _write_journal(
    tmp_path,
    f"{journal_lint.REQUIRED_TITLE}\n"
    f"{journal_lint.REQUIRED_DISCLAIMER}\n"
    f"{wordy}\n{tall}\n",
  )

  rc = journal_lint.main()
  captured = capsys.readouterr()

  assert rc == 1
  assert f"exceeds {journal_lint.MAX_WORDS} words" in captured.err
  assert f"exceeds {journal_lint.MAX_LINES} lines" in captured.err


def test_absolute_paths_and_urls(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  _write_journal(
    tmp_path,
    f"{journal_lint.REQUIRED_TITLE}\n"
    f"{journal_lint.REQUIRED_DISCLAIMER}\n"
    "See file://tmp/resource and /abs/path plus https://example.com\n",
  )

  rc = journal_lint.main()
  captured = capsys.readouterr()

  assert rc == 1
  assert "file:// URL" in captured.err
  assert "external URL" in captured.err
  assert "absolute path" in captured.err


def test_valid_journal(monkeypatch, tmp_path, capsys):
  monkeypatch.chdir(tmp_path)
  path = _write_journal(
    tmp_path,
    f"{journal_lint.REQUIRED_TITLE}\n"
    f"{journal_lint.REQUIRED_DISCLAIMER}\n"
    "Short notes about the day.\n",
  )

  rc = journal_lint.main()
  captured = capsys.readouterr()

  assert rc == 0
  assert path.relative_to(tmp_path).as_posix() in captured.out
