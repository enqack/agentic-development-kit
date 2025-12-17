# Patch v5.5: Developer hygiene

This patch adds:
- `.gitignore` aligned with agent data-plane vs control-plane separation
- `requirements.txt` for tool/test environment setup

## Quick start (local)

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After this, all tools under `tools/` and `tools/verify_all.sh` should run cleanly.
