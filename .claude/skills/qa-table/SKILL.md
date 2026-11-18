---
name: qa-table
description: QA Skill: table checks for RTL tables (first column on the right, cells flush right with one right edge per column) for Table 4.1, the Chapter 3 data table.
---

# qa-table

Measures cell positions in Table 4.1 and the Chapter 3 data table. The first column must be rightmost, and each column's cells must share one right edge.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks table --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
