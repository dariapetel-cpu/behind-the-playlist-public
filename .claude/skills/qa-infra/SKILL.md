---
name: qa-infra
description: QA Skill: project-structure checks (A2 §3.3 required files, no layout code in chapter files, README links, student-ID leak scan, source ZIP freshness).
---

# qa-infra

Checks the A2 §3.3 required files, that no layout code remains in `book/chapters/` (the iron law), that README links resolve, that no student ID appears outside `book/main.tex` and the PDFs, and that `submission/project-source.zip` holds the approved PDF and the class.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks infra --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
