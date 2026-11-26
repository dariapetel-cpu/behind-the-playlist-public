---
name: qa-visual
description: "QA Skill: rendered visibility checks. Every character must be visible in the rendered page; no rotation, annotations, raster images or overprinting; figures and tables show their ink; each page matches the approved coarse render fingerprint."
---

# qa-visual

The text layer is not what the reader sees (QA round 2: a black rectangle over the cover passed every check). This family looks at the render:

1. **Without a baseline.** Each page is rendered twice, with and without its text operators; every character must change its own pixels. Also: page rotation 0 and A4, no annotations except links, no raster images, no line printed over another, and the palette ink and minimum text of Fig. 2.1, Fig. 6.1, Table 4.1, the p. 9 table and the p. 9 formulas.
   *Misses:* wrong but visible text or graphics outside those regions, colour nuances, rule lines and box frames, damage smaller than a character.
2. **Fingerprint.** 20x28 RGB cell means per page against `tools/qa/visual_baseline.json`; tolerance max cell 4 and page mean 0.3 (noise measured with the pinned PyMuPDF: 0 after re-saving the PDF, at most 4 and 0.14 with half the antialiasing levels).
   *Misses:* changes of a few characters and shifts below about 0.5 pt; a different PyMuPDF version may need a new baseline. It cannot say whether a difference is a defect: after an intended layout change it fails until the users approve a new baseline.

Regenerate the baseline **only with the users' approval**, by this explicit command, which refuses to run without the approval text:

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <approved pdf> --write-visual-baseline --users-approval "<who, when, why>"
```

**Run** (from the project root; read-only, never edits project files; Windows: `.venv/Scripts/python.exe`):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks visual --out <report dir>
```

- Default inputs (public edition): `--pdf pdf/behind-the-playlist.pdf --no-log`. Submission edition only (these files are not in the public repository): `--edition submission --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- `--no-log` reports log-dependent checks as `n/a` with the reason. Never read `n/a` as a pass.
- Exit code: 0 = no fail, 1 = at least one fail, 2 = usage error or crash (no `findings.json` is left). A check that crashes, or a family with fewer findings than `min_findings`, is a fail.
- Writes `<report dir>/findings.json`. Each finding has `id, check, name, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`. Read the evidence of passes too.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
- Every check has a negative test in `tests/test_qa_mutations.py` (`python -m unittest discover -s tests`).
