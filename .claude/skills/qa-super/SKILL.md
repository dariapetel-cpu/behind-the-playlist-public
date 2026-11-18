---
name: qa-super
description: QA orchestrator. Runs every qa-* Skill (typeset, bidi, table, img, code, footer, infra, cls-version) on one PDF in a single pass and summarises pass/fail/n/a. Used by the detector Skill.
---

# qa-super

Runs all QA families in one pass, using the same library as the individual Skills:

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks all --out <report dir>
```

To recheck only some families, pass a list such as `--checks footer,typeset`.

| Skill | Checks |
|---|---|
| qa-typeset | log, glyphs, page count, chapter starts, bibliography |
| qa-bidi | RTL reading order from glyph positions |
| qa-table | RTL column order and cell alignment |
| qa-img | diagram blocks, captions and tags, margins |
| qa-code | code boxes (n/a for this book) |
| qa-footer | playback footer, including the p. 19 regression |
| qa-infra | required files, iron law, README links, ID leaks, ZIP freshness |
| qa-cls-version | template version |
