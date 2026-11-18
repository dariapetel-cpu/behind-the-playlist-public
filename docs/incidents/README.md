# Incident log

Incident analysis for bugs we found ourselves (Moodle announcement, MA-4, `docs/assignment-compliance.md`). Each report rests only on existing records (prompt log, PRD, reviews, test outputs) and cites them. No incident is invented or reconstructed beyond what those records show.

| ID | Title | Found by | Date | Status |
|---|---|---|---|---|
| [INC-001](INC-001-reversed-tikz-labels.md) | Reversed Hebrew word order in TikZ diagram labels | Daria (human reader), after a coordinator PASS | 2026-11-11 | Closed |
| [INC-002](INC-002-qa-bib-check-false-pass.md) | The QA bibliography check could pass without the heading | Detector agent (QA round 1, D1-02) | 2026-11-18 | Closed |

**Pending reports.** These are genuine findings that are already recorded but don't have a report yet (`TODO.md` P6):
- the tlmgr mirror hang;
- `[heb]` + colour rendering white text;
- matplotlib double bidi;
- a paragraph starting with TikZ flipping to LTR;
- `%` comments swallowing TikZ `;`;
- black text in floats;
- the LuaLaTeX smoke-test findings of 2026-11-18 (`tests/lualatex-smoke/RESULTS.md`).

## Report template

Symptom · How it was found (who, how) · Why earlier checks missed it · Root cause · Fix (including failed attempts) · How the correction was verified · Prevention / Skill update · Sources.
