# Task V1: Reviewer (sent by Boss, 2026-11-14)

Run via Claude Code's built-in Agent tool, `subagent_type: reviewer` (definition: `.claude/agents/reviewer.md`). The agent prompt points to this file; the task text is below the line.

---

Task V1 (date 2026-11-14): review the **complete manuscript** of „מאחורי הפלייליסט" (20 pages) and write `docs/agents/review-01.md`. Report only; do not edit any other file.

Read:
- `PRD.md` (§5, §6, §8)
- `docs/agents/research-notes.md` (the claim → source mapping, plus "Gaps / unverified")
- `book/references.bib`
- `book/chapters/00-abstract.tex` … `08-play.tex`
- `book/figures/pipeline.tex`
- `figures/data/noa_week.csv`
- the rendered pages `build/pages/page-01.png` … `page-20.png` (110 dpi)

Note: in the page images, Hebrew is right-to-left, and brackets and parentheses are mirrored glyphs. The Boss has already verified word order at glyph level for the diagram, the graph and the cover. Report a layout issue only if it is visible.

Check, and report every finding with file:line or page:
1. **Citation support.** For each `\cite`, does the cited key's research-notes entry actually support the sentence, at that strength? Flag overstatement, wrong key, or a factual sentence without a citation.
2. **Research limitations.** Every item in "Gaps / unverified" is respected: no spectrograms, no repeats or playlist adds as named signals, no skip percentage from a source, no time-of-day platform claim, no Daily Mix/Discover/radio internals, Goldberg only for the name and year, Hu and Koren at abstract level, Schwartz as an argument, Spotify figures with "accessed".
3. **Platform vs. general.** Platform claims are attributed; nothing says or implies "this is how Spotify works"; the Ch. 6 diagram is presented as an educational simplification.
4. **Mathematics.** Recompute the cosine example (Ch. 3), the 570-year estimate (Ch. 1), and the Ch. 2 numbers against `figures/data/noa_week.csv` (totals, 28.8%, 41%, 19%, 11%).
5. **Fictional-data labels.** Every scene, every invented number, table and figure is labelled (scene box, `\fictional`, `\educational`, `lab` box).
6. **The Ch. 4 comparison table.** Rule on each cell: supported by which note, definitional (acceptable as a definition), or unsupported (must be fixed). The Boss flagged two cells in the "hybrid / context" column: "דורש יותר סוגי נתונים" and "תלוי במידע הזמין". Give a concrete fix for each unsupported cell.
7. **Hebrew and consistency.** Grammar, natural phrasing, consistent terms across chapters, and repetition between chapters.
8. **PRD §8 acceptance criteria.** Mark each one pass / fail / not checkable now.
9. **Layout (from the page images).** Visible problems only: reversed text, clipping, empty or near-empty pages, box or colour inconsistencies, figure placement, and the readability of the bibliography.

Use the report format in your definition: header, issue table (# | severity | location | problem | suggested fix), a section per check above, and a verdict.
