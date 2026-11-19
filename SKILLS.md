# Project Skills

The Skills used in this project (A2 §5: "list of the Skills used in the project, including the files themselves"). All are in [`.claude/skills/`](.claude/skills/). Prompts used to run them are in [`prompts/`](prompts/).

| Skill | Purpose | Files | Actually run |
|---|---|---|---|
| `researcher` | Check claims against sources | `.claude/skills/researcher/SKILL.md` | Not run as a Skill. A role-check prompt was prepared in [`prompts/supplemental-role-check.md`](prompts/supplemental-role-check.md); no run is recorded |
| `writer` | Draft Hebrew chapters using research notes | `.claude/skills/writer/SKILL.md` | Not run as a Skill. A role-check prompt was prepared in [`prompts/supplemental-role-check.md`](prompts/supplemental-role-check.md); no run is recorded |
| `reviewer` | Review evidence and chapter text | `.claude/skills/reviewer/SKILL.md` | Not run as a Skill. A role-check prompt was prepared in [`prompts/supplemental-role-check.md`](prompts/supplemental-role-check.md); no run is recorded |
| `detector` | Detector role: run qa-super + visual red-team review; report only, never edit | `.claude/skills/detector/SKILL.md` | D1, D2 (2026-11-18) |
| `fixer` | Fixer role: fix only in the class or Skills; flag content and packaging; build a candidate PDF | `.claude/skills/fixer/SKILL.md` | F1 (2026-11-18) |
| `qa-super` | Orchestrator: all qa-* families in one pass | `.claude/skills/qa-super/SKILL.md`, `tools/qa/qa_lib.py` | D1, D2 |
| `qa-typeset` | Log, glyphs, page count, chapter starts, bibliography (reuses `tools/check_pdf.py`) | `SKILL.md` + `tools/qa/qa_lib.py`, `tools/check_pdf.py` | D1, D2 |
| `qa-bidi` | RTL reading order from glyph positions; ascending citations | `SKILL.md` + `tools/qa/qa_lib.py` | D1, D2 |
| `qa-table` | RTL column order and cell alignment | same | D1, D2 |
| `qa-img` | Diagram blocks/labels, captions and tags, side margins | same | D1, D2 |
| `qa-code` | Code boxes: honestly n/a (none in the book) | same | D1, D2 |
| `qa-footer` | Playback footer on every page, including the p.19 regression | same | D1, D2 |
| `qa-infra` | Required files, iron law, README links, ID-leak scan, ZIP freshness | same | D1, D2 |
| `qa-cls-version` | Class version: `\ProvidesClass` = CHANGELOG = build log | same | D1, D2 |

**Shared data:** `tools/qa/expectations.json`.
**Run records:** `docs/qa/round-01/`, `docs/agents/log.md` rows 6–8 and `docs/agents/transcripts/D1-*`, `F1-*`, `D2-*`.
