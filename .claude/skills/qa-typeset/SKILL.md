---
name: qa-typeset
description: QA Skill: compilation and typesetting checks for the book PDF (errors, missing glyphs, overfull boxes, undefined references, page count, chapter openings, bibliography heading/entries/margins, biber warnings). Reuses tools/check_pdf.py.
---

# qa-typeset

Checks the build log and the PDF: 0 errors, 0 missing characters, no overfull lines over 2 pt, 0 undefined references or citations, no text outside the page, no white text on a light background (all via `tools/check_pdf.py`). Also checks the 20-page count, the 10 chapter start pages, the bibliography (heading „מקורות" at heading size on the expected page, `chapter_starts.מקורות` = 19, not just in the running header; 18 numbered entries, all inside the margins) and the biber warnings.

**Run** (from the project root; read-only, never edits project files):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks typeset --out <report dir>
```

- Default inputs: `--pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- Writes `<report dir>/findings.json`. Each finding has `id, check, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
