---
name: qa-bidi
description: "QA Skill: Hebrew/English direction checks. Reads every page from glyph positions (never from extracted strings alone) and asserts expected phrases in RTL reading order in their own place, plus ascending multi-number citations."
---

# qa-bidi

Implements the PRD §6 verification rule and the lesson of INC-001: word order is asserted from **glyph x-positions**, because both images and PyMuPDF word extraction can mislead for right-to-left text. Phrases cover the diagram labels, graph labels, table cells, mixed Hebrew/English runs, numbers and the cover lines.

A phrase counts only **in its own place**: graph labels inside Fig. 2.1 (p. 7), diagram labels as the label of their own block in Fig. 6.1 (p. 14), table cells inside Table 4.1 (p. 11), cover lines on p. 1. The same words in the prose never satisfy the check. In the public edition the cover must hold no digit at all, and no ID or date label.

**Run** (from the project root; read-only, never edits project files; Windows: `.venv/Scripts/python.exe`):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks bidi --out <report dir>
```

- Default inputs (public edition): `--pdf pdf/behind-the-playlist.pdf --no-log`. Submission edition only (these files are not in the public repository): `--edition submission --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- `--no-log` reports log-dependent checks as `n/a` with the reason. Never read `n/a` as a pass.
- Exit code: 0 = no fail, 1 = at least one fail, 2 = usage error or crash (no `findings.json` is left). A check that crashes, or a family with fewer findings than `min_findings`, is a fail.
- Writes `<report dir>/findings.json`. Each finding has `id, check, name, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`. Read the evidence of passes too.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
- Every check has a negative test in `tests/test_qa_mutations.py` (`python -m unittest discover -s tests`).
