# Task D1: Detector, red-team QA round 1 (sent by Boss, 2026-11-18)

Run via Claude Code's Agent tool, `subagent_type: detector` (definition `.claude/agents/detector.md`; procedure in Skill `.claude/skills/detector/SKILL.md`). The task text is below the line.

---

Task D1 (2026-11-18): red-team QA, round 1, on the **approved** book.

- PDF: `submission/behind-the-playlist.pdf` (approved, 20 pages)
- LaTeX log of that exact build: `build/lualatex/main.log` (and `build/lualatex/main.blg`)
- Sources: `book/` (class, main.tex, chapters, references.bib), `tools/qa/expectations.json`
- Report directory: `docs/qa/round-01/detect/`

Follow the detector Skill:
1. Run qa-super with `--checks all` on that PDF and log, writing to the report directory.
2. Do the red-team review of the rendered pages in `docs/qa/round-01/detect/pages/`. Check all 20, and look especially at:
   - the cover;
   - pp. 7 (graph), 8–9 (formula), 11 (table) and 14 (diagram);
   - pp. 18–20 (footer and bibliography).
3. Write `docs/qa/round-01/detect/detector-report.md`:
   - each finding with page or file, evidence, expected result, severity and kind;
   - an explicit line for the **page-19 footer regression check**;
   - a plain statement if there are no actionable template/skill defects.

Do not edit anything outside the report directory. Do not write student ID numbers.
