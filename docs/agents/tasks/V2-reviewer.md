# Task V2: Reviewer, focused second pass (sent by Boss, 2026-11-14)

Run via Claude Code's built-in Agent tool, `subagent_type: reviewer`. The agent prompt points to this file; the task text is below the line.

---

Task V2 (date 2026-11-14): a **focused re-review** of the revised manuscript. Write `docs/agents/review-02.md`. Report only; do not edit any other file.

**Privacy rule:** the cover now contains real student ID numbers. Do NOT open `book/main.tex`, and never write any ID number in your report. Check the cover only from `build/pages/page-01.png`, where the IDs are masked as "ID hidden". The Boss has verified the unmasked IDs at glyph level, in left-to-right digit order and on the row of the correct author.

Read:
- `docs/agents/review-01.md` (your first report) and `docs/agents/review-01-response.md` (what the Boss did about each issue)
- `docs/agents/research-notes.md` (only the entries you need to re-check claims)
- `book/chapters/00-abstract.tex` … `08-play.tex`, `book/figures/pipeline.tex`, `book/style.sty`, `book/references.bib`
- `PRD.md` §6 and §8
- the rendered pages `build/pages/page-01.png` … `page-20.png` (re-rendered after the fixes)

Check:
1. **Every review-01 issue marked "Applied".** Is it actually fixed in the source and the render, and correctly? Give particular attention to the five majors (#1–#5) and to the partly resolved #27.
2. **Open and accepted items** (#29 near-empty p. 13, #32, #33, #36). Is the Boss's reasoning acceptable, or is there a substantive problem left? #36 is now resolved: cover details were supplied by the user and the institution line was removed at the user's request. Check from the masked page that the cover shows the author, course, lecturer and date in correct Hebrew order, and that no placeholder text remains.
3. **Regressions.** Did any fix introduce a new error (facts, citations, Hebrew, layout, numbering, references to "the table on the right", etc.)?
4. **PRD §8 acceptance criteria.** Re-mark each one pass / fail / not checkable. README (criterion 9) does not exist yet, so mark it "not checkable".

Report format: header; a table of review-01 items with columns # | status (verified fixed / not fixed / partially / acceptable as is) | note; a separate table of NEW issues with severity; then the PRD §8 table; then a **final verdict**: APPROVE, APPROVE WITH MINOR NOTES, or CHANGES REQUESTED. Be honest: do not approve if a major problem remains.
