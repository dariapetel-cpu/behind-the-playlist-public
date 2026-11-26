---
name: qa-typeset
description: "QA Skill: compilation and typesetting checks for the book PDF (build log, missing glyphs, overfull boxes, undefined references, page count, chapter openings, text completeness, bibliography, biber warnings). Reuses tools/check_pdf.py."
---

# qa-typeset

Checks the build log and the PDF through `tools/check_pdf.py`: a completed LuaLaTeX log of this class whose page count equals the PDF's, 0 errors (classic, `file:line:` also with Windows paths, Lua), no fatal error, unfinished run or rerun request, no multiply-defined label or empty bibliography, 0 missing characters, no overfull `\hbox` or `\vbox` over 2 pt, 0 undefined references or citations (also when the log line is wrapped at 79 columns), no text outside the page, no faint text. The reasons of a fail are kept in the evidence.

Also checks the 20-page count, the 10 chapter start pages, the cover mask, the printed contents page, the bibliography (heading „מקורות" at heading size on p. 19, 18 numbered entries, every title printed, all inside the margins) and the biber log (`main.log` -> `main.blg`; absent, fatal or unfinished = fail). Log rules were tested on synthetic logs only.

**Text completeness:** every word of each chapter source must be printed on that chapter's pages, and no more printed-only words than in the approved PDF. Misses: word order, punctuation, single letters, formulas, and a deletion made in source and PDF together.

**Run** (from the project root; read-only, never edits project files; Windows: `.venv/Scripts/python.exe`):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks typeset --out <report dir>
```

- Default inputs (public edition): `--pdf pdf/behind-the-playlist.pdf --no-log`. Submission edition only (these files are not in the public repository): `--edition submission --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- `--no-log` reports log-dependent checks as `n/a` with the reason. Never read `n/a` as a pass.
- Exit code: 0 = no fail, 1 = at least one fail, 2 = usage error or crash (no `findings.json` is left). A check that crashes, or a family with fewer findings than `min_findings`, is a fail.
- Writes `<report dir>/findings.json`. Each finding has `id, check, name, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`. Read the evidence of passes too.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
- Every check has a negative test in `tests/test_qa_mutations.py` (`python -m unittest discover -s tests`).
