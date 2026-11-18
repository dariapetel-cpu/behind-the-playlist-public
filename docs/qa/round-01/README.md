# QA round 1: red-team detect → fix → recheck (2026-11-18, local)

**Target:** the approved book, `submission/behind-the-playlist.pdf` (20 pp, SHA-256 `43608a86…`). It was **not modified** in this round.

**Roles** (separate agents with project Skills; definitions in `.claude/agents/`, procedures in `.claude/skills/`):

| Step | Agent | How it ran | Skills used | Output |
|---|---|---|---|---|
| D1 detect | **Detector** | general-purpose subagent bound to `.claude/agents/detector.md`: the `detector` type was created in this turn and was not yet registered. Tool limits were enforced by instruction, and the write scope was verified from the transcript | `detector` (Skill tool) → `qa-super` (all qa-* families) + visual red-team review of 20 pages | [detect/detector-report.md](detect/detector-report.md), `detect/findings.json` |
| F1 fix | **Fixer** | registered `fixer` agent type (harness-enforced tools); handed the D1 report automatically by the coordinator, with no user step in between | `fixer` (procedure file read via shell; no Skill-tool call recorded) | [fix/fixer-report.md](fix/fixer-report.md), candidate `build/behind-the-playlist-candidate.pdf` |
| D2 recheck | **Detector** | registered `detector` agent type | `detector` (Skill tool), recheck mode, → `qa-super` | [recheck/recheck-report.md](recheck/recheck-report.md), `recheck/findings.json` |

**Harness calibration before D1 (coordinator, not an agent):** the first dry run of the new checks gave 5 failures. Four came from the harness itself:
- a smoke-test phrase used as if it were book text;
- a table cell that wraps onto two lines;
- the trailing "%" split from "28.8%";
- matplotlib hatch-pattern definitions reported outside the margins.

These were corrected in `tools/qa/` and `expectations.json` (see its `_calibration` note). The fifth failure, the stale ZIP, was real.

## Findings and outcome

| ID | Finding | Kind | Decision | Recheck (D2) |
|---|---|---|---|---|
| D1-01 | `submission/project-source.zip` is stale: old PDF, no `.cls` | packaging | flagged for the users | still open |
| D1-02 | The QA bibliography check matched the running header on p.20 and never compared it with the expected page, so a missing heading would still pass (**a bug in the QA harness itself**) | skill | fixed in `tools/qa/qa_lib.py` + the qa-typeset SKILL.md | **verified fixed** (negative tests on copies) |
| D1-03 | Bibliography URL break right after `https:` (entry [13], p.20) | template | fixed: class **v1.0 → v1.1** | **verified fixed**; only p.20 changes |
| D1-04 | Label „לולאת משוב" almost touches the dashed loop line (Fig. 6.1, p.14) | figure (content file) | flagged for the users (optional offset in `book/figures/pipeline.tex`) | still open, cosmetic |

**Regression check, p.19 footer:** PASS in D1 and in D2.
**Page count:** 20 in D1 and D2.
**Automated totals:** D1 55 pass / 1 fail / 1 n/a; D2 the same, where the one fail is D1-01 and the n/a is that there are no code boxes.
**Content:** the Detector found no claim that contradicts the research notes.

**Follow-up (Prompts 23–24, users' decisions):**
- The users approved the ref [13] layout.
- For D1-04 they asked for „לולאת משוב" to move right with a ≈2 mm gap. The **coordinator** made the change in `book/figures/pipeline.tex`, on the users' decision; it is not a Fixer action, because figures are content files. The label moved 5.5 pt; a phantom copy keeps the picture's bounding box, so the blocks do not move.

| Step | Agent | Result |
|---|---|---|
| D3 recheck | **Detector** | [recheck-2/recheck-report.md](recheck-2/recheck-report.md): label legible; gap 1.86 mm (ink edge) / 2.00 mm (glyph box, coordinator measurement); 8 blocks + dashed line identical to approved; only p.20 text differs; 20 pp; p.19 PASS; **acceptable** |

**New findings from D3:**
- **D3-01 (skill, open):** the bidi check for „לולאת משוב" matched body text on p.15, not the rotated label on p.14.
- **D3-02 (content, flagged):** the label's ink extends 0.51 mm past the text block's right edge.

**Final state:** candidate `build/behind-the-playlist-candidate.pdf` (class v1.1 + label offset) is **acceptable per D3**. It is **not promoted**: `submission/` and the ZIP wait for the users' approval.

## Approval and open tool defect (2026-11-18, Prompt 25)

- **The users approved** the page-14 layout and this version of the book.
  - The candidate (`ed844348…`, class v1.1 + label offset, 20 pp) is now `submission/behind-the-playlist.pdf`.
  - The previous submission PDF (`43608a86…`) is backed up as `backups/behind-the-playlist-v1.2-lualatex-cls1.0-2026-11-18.pdf`.
- **Manual check of the label „לולאת משוב": PASSED.** The Detector (D3) checked it by hand at 1200 dpi: legible, correct Hebrew, not clipped, no overlap, gap ≈2 mm. The users approved it visually (Prompt 25).
- **The automated tool still needs fixing (D3-01, open):** the `qa-bidi` phrase check for „לולאת משוב" passes on body text of p.15, so it has never verified the rotated label on p.14. Until it is fixed, that label is covered only by the manual check above. The fix belongs in `tools/qa/qa_lib.py`: read rotated lines, i.e. `dir ≠ (1,0)`, as their own text, and require the label on the diagram page. It is listed in `TODO.md`.
- **D1-01 (stale ZIP): resolved.** `submission/project-source.zip` was rebuilt with the approved PDF and current sources (203 files). `qa-infra` now passes (5/5). The old ZIP is backed up in `backups/`.
