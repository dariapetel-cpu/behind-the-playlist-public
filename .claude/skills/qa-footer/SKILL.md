---
name: qa-footer
description: "QA Skill: playback-footer checks on every page, including the page-19 regression from Prompt 18 (left number = total pages, right = current page; pink dot moves right-to-left; footer visible in the render)."
---

# qa-footer

Regression guard for the bug found in Prompt 18: when a page break fell inside the English bibliography, page 19's footer was typeset left to right ("91" / "02", mirrored bar). Fixed by `\inhebrew` in the class.

Pages 2-20 must all exist (a shorter PDF fails), and the numbers and the pink dot must be **visible in the rendered page**, not only in the text layer.

**Run** (from the project root; read-only, never edits project files; Windows: `.venv/Scripts/python.exe`):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks footer --out <report dir>
```

- Default inputs (public edition): `--pdf pdf/behind-the-playlist.pdf --no-log`. Submission edition only (these files are not in the public repository): `--edition submission --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- `--no-log` reports log-dependent checks as `n/a` with the reason. Never read `n/a` as a pass.
- Exit code: 0 = no fail, 1 = at least one fail, 2 = usage error or crash (no `findings.json` is left). A check that crashes, or a family with fewer findings than `min_findings`, is a fail.
- Writes `<report dir>/findings.json`. Each finding has `id, check, name, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`. Read the evidence of passes too.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
- Every check has a negative test in `tests/test_qa_mutations.py` (`python -m unittest discover -s tests`).
