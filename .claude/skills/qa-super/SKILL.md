---
name: qa-super
description: QA orchestrator. Runs every qa-* Skill (typeset, bidi, table, img, code, footer, infra, cls-version, visual) on one PDF in a single pass and summarises pass/fail/n/a. Used by the detector Skill.
---

# qa-super

Runs all QA families in one pass, using the same library as the individual Skills:

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks all --out <report dir>
```

Public edition: `--pdf pdf/behind-the-playlist.pdf --no-log`. Exit code 0 = no fail, 1 = fail, 2 = usage error or crash; always check it. `n/a` is not a pass.

To recheck only some families, pass a list such as `--checks footer,typeset`.

| Skill | Checks |
|---|---|
| qa-typeset | log, glyphs, page count, chapter starts, text completeness, bibliography, biber |
| qa-bidi | RTL reading order from glyph positions, each phrase in its own place |
| qa-table | RTL column order and cell alignment |
| qa-img | diagram blocks, captions and tags, margins |
| qa-code | code in the chapter sources (n/a only if there is none) |
| qa-footer | playback footer, including the p. 19 regression |
| qa-infra | required files, chapters, bibliography, class interface, iron law, README links, ID scan, ZIP freshness |
| qa-cls-version | template version |
| qa-visual | what the rendered page shows: visible text, figures and tables, fingerprint |
