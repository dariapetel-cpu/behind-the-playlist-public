---
name: qa-bidi
description: QA Skill: Hebrew/English direction checks. Reads every page from glyph positions (never from extracted strings alone) and asserts expected phrases in RTL reading order, plus ascending multi-number citations.
---

# qa-bidi

Implements the PRD §6 verification rule and the lesson of INC-001: word order is asserted from **glyph x-positions**, because both images and PyMuPDF word extraction can mislead for right-to-left text. Phrases cover the diagram labels, graph labels, table cells, mixed Hebrew/English runs, numbers and the cover lines.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks bidi --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
