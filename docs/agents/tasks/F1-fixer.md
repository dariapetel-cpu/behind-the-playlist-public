# Task F1: Fixer, red-team QA round 1 (sent by Boss, 2026-11-18)

The Fixer's role definition is `.claude/agents/fixer.md` and its procedure is the Skill `.claude/skills/fixer/SKILL.md`. This task is passed on automatically by the coordinator as soon as the Detector's report exists; there is no user step in between. The task text is below the line.

---

Task F1 (2026-11-18): act on the Detector report of QA round 1.

- Input: `docs/qa/round-01/detect/detector-report.md` and `docs/qa/round-01/detect/findings.json`
- Output: `docs/qa/round-01/fix/fixer-report.md`

Follow the fixer Skill:
1. Decide each finding, using its `kind`:
   - `template`/`skill` defects: fix them in `book/behind-the-playlist.cls` (bump the version and add a CHANGELOG entry) or in `.claude/skills/**` / `tools/qa/**`.
   - `content`, `packaging` and `build` findings: **flag for the users**, with a recommendation.
2. If you fixed anything, run `make candidate` (→ `build/behind-the-playlist-candidate.pdf`), and list which pages and QA families the Detector must recheck.
3. If nothing is actionable for you, say so plainly and build nothing.

Never edit `book/chapters/*`, `book/main.tex`, `book/references.bib`, `submission/*` or `backups/*`. The approved `submission/behind-the-playlist.pdf` (SHA-256 43608a86…) must stay byte-identical.
