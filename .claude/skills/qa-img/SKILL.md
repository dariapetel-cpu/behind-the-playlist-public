---
name: qa-img
description: QA Skill: figure checks (eight-block diagram with every label inside its block; Fig. 2.1 and 6.1 captioned and tagged as fictional/educational; no visible ink in the side margins).
---

# qa-img

Counts the eight diagram blocks and checks that each Hebrew label lies fully inside its block. Confirms the figure captions and their tags, and renders every page to verify that nothing visible sits in the side margins.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks img --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
