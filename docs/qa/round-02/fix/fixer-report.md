> Author: Fixer agent · 2026-11-25 · input: docs/qa/round-02/detect/detector-report.md

# Fixer report, QA round 2 (Task F2)

**Summary:** of the 26 D4 rows (H1-H3, M2-M5, L3, N1-N18), 25 are fixed (M4/N16 with two explicitly allowed exceptions, flagged for the users) and 1 is partly fixed (N7); see "Open" for what the fixes still miss. **No candidate:** no class change, so nothing to build. D4 found no defect in the book.

**Approved PDF** `pdf/behind-the-playlist.pdf`: SHA-256 `7ab8276a…e7ece` at the start and at the end (identical). Nothing under `book/`, `pdf/` or `figures/` was changed. No commit, push, install or TeX run.

**Scope note.** The fixer role normally covers the class, Skills and `tools/qa/`. `tools/check_pdf.py` and `tests/test_qa_mutations.py` were edited because Roni Sagi's prompt names them (`prompts/qa-round-02-01-implementation.md`, steps 4-6).

## Files changed
`tools/qa/qa_lib.py`, `tools/qa/expectations.json`, `tools/qa/visual_baseline.json` (new), `tools/check_pdf.py`, `tests/test_qa_mutations.py` (new), `.claude/skills/{detector,fixer,qa-super,qa-typeset,qa-bidi,qa-table,qa-img,qa-code,qa-footer,qa-infra,qa-cls-version}/SKILL.md`, `.claude/skills/qa-visual/SKILL.md` (new), this report.

## Test results (verbatim)

New code (`python -m unittest discover -s tests`, Windows, Python 3.12.2, PyMuPDF 1.28.2):

```
Ran 116 tests in 588.275s

OK
```
(114 tests in `test_qa_mutations.py` plus the 2 existing ones in `test_feedback_label.py`.)

Old code (a clone of commit 12efa82 with only the new test file added):

```
Ran 116 tests in 392.057s

FAILED (failures=147, errors=3)
```
That is **106 of the 114 mutation-file tests failing** on the old code (the counts in the block include sub-tests). 107 of the failing runs printed "0 fail" and exited 0, so the old harness was silent on them. A caveat: the old findings have no `name` field, so on the old code a test that asserts a named check fails even where the old harness reported the damage under another label (about 30 runs, for example ID on the cover, version in the log, `WARN` in the `.blg`). 8 tests pass on the old code, all of them "valid input must pass" or "no false alarm" tests. The Skill, baseline and minimum tests fail there because those things did not exist.

Earlier full runs while working: 110 tests with 2 errors, and 116 tests with 1 failure; both were faults in the tests (fixture file reused, relative path applied twice), then corrected.

Real project, `--no-log`, machine locale cp1255 without PYTHONUTF8:

```
QA all [public edition]: 106 pass, 0 fail, 5 n/a
exit 0
```

## Decisions per finding

| ID | Decision | Files | Tests (tests/test_qa_mutations.py) |
|---|---|---|---|
| H1 | fixed: every character must change the rendered pixels at its place; figure/table regions need their text and palette ink | qa_lib.py, expectations.json, qa-visual | `H1Visual.test_h1_*`, `test_one_removed_line_fails` |
| H2 | fixed: missing targets fail; `min_findings` per family; a crash is a fail | qa_lib.py, expectations.json | `H2NoSilentSkips.*` |
| H3 | fixed: exit 0/1/2; completed LuaLaTeX log of this class with the PDF's page count | qa_lib.py, check_pdf.py | `H3Logs.*`, `Cli.*` |
| M2 | fixed: eight descriptions quoted; also checked once with PyYAML (14 Skills and 5 agents parse) | SKILL.md files | `Skills.test_m2_frontmatter_scalars` |
| M3 | fixed: by pattern; `.git`/`.venv` excluded by path part | qa_lib.py | `Privacy.test_m3_*`, `test_similar_folder_name_is_not_excluded` |
| M4, N16 | fixed; two existing pieces of code allowed once each and **flagged** (below) | qa_lib.py, expectations.json | `Sources.test_m4_*`, `test_n16_*`, `test_escaped_percent_*`, `test_allowed_figure_*` |
| M5 | fixed: sources inspected, comments ignored; code present = fail | qa_lib.py | `Sources.test_m5_*` |
| L3 | fixed | qa_lib.py | `Cli.test_l3_*` |
| N1 | fixed | qa_lib.py | `H1Visual.test_n1_*` |
| N2 | fixed (text completeness 0 missing words per chapter; contents page; bibliography titles) | qa_lib.py | `test_n2_*` |
| N3 | fixed | qa_lib.py | `test_n3_*` |
| N4, N5 | fixed: evidence from the figure's own page and region | qa_lib.py | `Figures.test_n4_*`, `test_n5_*`, `test_fig61_*`, `H2NoSilentSkips.test_fig61_*` |
| N6 | fixed (rotation, image, annotation, overprint) | qa_lib.py | `H1Visual.test_n6_*` |
| N7 | fixed for the log; partly for "log and PDF belong together": only class and page count are compared | check_pdf.py | `H3Logs.test_n7_*`, `test_complete_79_*` |
| N8 | fixed: reasons kept in the evidence | qa_lib.py | `H3Logs.*` (evidence asserted), `test_n18_*` |
| N9 | fixed | qa_lib.py | `H3Logs.test_n9_*` |
| N10, N11 | fixed | qa_lib.py | `Cli.test_n10_*`, `test_n11_*`, `Privacy.test_n11_*` |
| N12 | fixed; the image with an ID is caught as an image (none is expected), its text is not read | qa_lib.py, expectations.json | `Privacy.test_n12_*` |
| N13 | fixed | qa_lib.py | `Privacy.test_n13_*` |
| N14 | fixed | qa_lib.py, expectations.json | `Sources.test_n14_*`, `test_bib_entry_*`, `test_chapter_not_loaded_*` |
| N15 | fixed | qa_lib.py | `Sources.test_n15_*` |
| N17 | fixed: full page height, pale ink, expected page colour | qa_lib.py | `Figures.test_n17_*`, `test_dark_page_background` |
| N18 | fixed: luminance difference instead of pure white | check_pdf.py, qa_lib.py | `test_n18_*` |

**Also found and fixed while working:** the Table 4.1 column check read the word "שילוב" from the prose above the table, so it never measured the header (`H2NoSilentSkips.test_table41_header_removed_*`).

## Calibration
- **Visible ink** (100 dpi, grey): lowest value of any real character 75 of 255 ("i" inside a ligature, looked up 2 pt wider); threshold 60. Covered text gives 0.
- **Palette pixels** (72 dpi, tolerance 24 per channel): minima about 75-80 % of the approved counts, 50 % for the small charcoal badges of Fig. 6.1.
- **Text:** 0 source words missing in all nine chapters of the approved PDF, so the threshold is 0. Printed-only words (titles, box and figure labels) are capped at the approved counts.
- **Fingerprint** (20x28 RGB cells): re-saving 0; antialiasing 6 and 4 bits: max cell 3 and 4, mean 0.05 and 0.14. Removing one arrow of Fig. 6.1: cell 7. Page shifted by 0.5 pt: mean up to 0.45. Tolerance: cell 4, mean 0.3. Rendering at other resolutions (cell 6-7, mean 0.46) or without antialiasing (28) exceeds it; the harness always renders at 72 dpi.
- **Margins:** inner margin difference 0; threshold 12 (outermost 3 pt ignored).
- **IDs:** with the final pattern the only hits in the whole project are public catalogue/document numbers in the R1 transcripts; they form the three-line allow-list.

## expectations.json: reason for each change
Nothing was removed or relaxed. `required_files`: chapters 00, 02-08 added (N14). `forbidden_patterns`: ISO date and any digit added (N12; the approved public cover has no digit). New blocks: page size/background/raster images (N6, N12, N17), chapter pages and printed-only words (N2), regions, p. 9 header and values, figures (H1, H2, N4, N5), class interface (N14), iron-law allow-list (M4), privacy allow-list (M3), `min_findings` (H2).

## Flagged for the users
1. **Approval of `expectations.json` and `visual_baseline.json`**: both normally need your approval; they were changed/created under the implementation prompt and are uncommitted. The baseline was made from the tracked approved public PDF.
2. **Iron law, chapter 2:** `\begin{figure}[t]` and `\includegraphics[width=\textwidth]{noa_week.pdf}` are layout code in a chapter. Allowed once each, not edited. You decide whether they move to the class, and whether the deny-list is right.
3. **docs/assignment-compliance.md, README and PLAN** were not touched; the new family and the test command are not described there.
4. **Makefile** (`make check`, `make pdf`) works unchanged but now fails on warnings such as a rerun request.

## Open
- **Real build log:** no TeX build and no real log or `.blg` here. Log tests use synthetic fixtures; whether the real log passes is unknown. `--no-log` reports these checks as n/a.
- **N7 residue:** a log of another 20-page build of the same class would be accepted.
- **Submission edition** not run (its PDF is not in the repo). Its cover is not fingerprinted (baseline is the public edition), reported n/a.
- **POSIX** not run; paths use pathlib parts.
- **Still not seen:** text inside raster images (also README screenshots); archives and fonts are not scanned; an ID with letters after it or split over lines; word order, punctuation, single letters and formulas in the prose; small changes below the fingerprint tolerance; the same deletion in source and PDF; code boxes have no check beyond "present = fail"; layout commands outside the deny-list.
- The fingerprint depends on the pinned PyMuPDF (1.28.2) and will fail after any intended layout change, until a new baseline is approved.

## Recheck request for the Detector
All families on the approved PDF with `--no-log` and with a synthetic log; D4's claims H1-H3, M2-M5, L3 and N1-N18 again with **own** mutations, above all `visual` (partial covers, other colours), `typeset.text-complete`, privacy formats, log wrapping, and whether the valid project gives false alarms.
