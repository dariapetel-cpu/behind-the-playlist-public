---
name: qa-cls-version
description: QA Skill: template version check (version in \\ProvidesClass = latest CHANGELOG entry = version in the LuaLaTeX build log).
---

# qa-cls-version

Compares the class version in `book/behind-the-playlist.cls` (`\\ProvidesClass` and CHANGELOG) with the version the build log reports.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks cls-version --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
