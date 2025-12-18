---
description: Verify Markdown structure and quality
---

# Markdown Checklist

Run this workflow when creating or modifying significant Markdown documentation.

## Precondition
- `docs/intent/project_intent.md` exists.

## Steps

1. **Format**
   - Run `python3 tools/format_md.py`
   - If it fails, check `tools/check_tools.sh` and resolve dependencies.

2. **Verify Structure**
   - [ ] Fenced code blocks have language identifiers?
   - [ ] Blank lines surround code blocks?
   - [ ] Lists use consistent indentation (2 spaces)?
   - [ ] No mixed bullets (`-` vs `*`)?
   - [ ] No hard-coded file links (`file://`)? (Run `linters/lint_common.py` checks)

3. **Verify Links**
   - [ ] All internal links are repo-relative?
   - [ ] External links are valid (`https://`)?

4. **Commit**
   - Only commit after formatting passes cleanly.
