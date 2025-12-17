# Patch v5.7: Language-agnostic testing hook + verification requirements rename

This patch makes the template more explicitly language-agnostic by:
- introducing `tools/test.sh` as the canonical project test hook (Go/Rust/Node/Python examples included)
- renaming verification dependencies to `requirements-verify.txt` (preferred), while keeping legacy `requirements.txt` acceptable
- updating `tools/verify_all.sh` to run tests only via `tools/test.sh`

## Local setup (verification tooling)

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-verify.txt
```

## Defining tests for your language

Edit `tools/test.sh` to run your project’s tests deterministically.
