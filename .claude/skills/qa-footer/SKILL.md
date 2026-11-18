---
name: qa-footer
description: QA Skill: playback-footer checks on every page, including the page-19 regression from Prompt 18 (left number = total pages, right = current page; pink dot moves right-to-left).
---

# qa-footer

Regression guard for the bug found in Prompt 18: when a page break fell inside the English bibliography, page 19's footer was typeset left to right ("91" / "02", mirrored bar). Fixed by `\\inhebrew` in the class.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks footer --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
