---
name: qa-table
description: "QA Skill: table checks for RTL tables (first column on the right, cells flush right with one right edge per column, every number in its column) for Table 4.1 and the Chapter 3 data table."
---

# qa-table

Measures cell positions inside the regions of Table 4.1 (p. 11) and the Chapter 3 data table (p. 9). The first column must be rightmost, and each column's cells must share one right edge. The p. 9 table is also compared number by number. A missing table, header or cell is a **fail**, never a skipped check.

**Run** (from the project root; read-only, never edits project files; Windows: `.venv/Scripts/python.exe`):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks table --out <report dir>
```

- Default inputs (public edition): `--pdf pdf/behind-the-playlist.pdf --no-log`. Submission edition only (these files are not in the public repository): `--edition submission --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- `--no-log` reports log-dependent checks as `n/a` with the reason. Never read `n/a` as a pass.
- Exit code: 0 = no fail, 1 = at least one fail, 2 = usage error or crash (no `findings.json` is left). A check that crashes, or a family with fewer findings than `min_findings`, is a fail.
- Writes `<report dir>/findings.json`. Each finding has `id, check, name, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`. Read the evidence of passes too.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
- Every check has a negative test in `tests/test_qa_mutations.py` (`python -m unittest discover -s tests`).
