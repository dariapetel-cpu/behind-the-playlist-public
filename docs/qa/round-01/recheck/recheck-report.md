> Author: Detector agent · 2026-11-18 · PDF: build/behind-the-playlist-candidate.pdf (SHA-256 34334e9d15ab)

# Recheck report, red-team QA round 1 (Task D2, recheck mode)

**Inputs**
- Candidate: `build/behind-the-playlist-candidate.pdf` (SHA-256 34334e9d15ab), log `build/candidate/main.log` (+ `main.blg`)
- Compared with: `docs/qa/round-01/detect/detector-report.md` (D1), `docs/qa/round-01/fix/fixer-report.md` (F1)
- Approved PDF (read only): `submission/behind-the-playlist.pdf`, SHA-256 still 43608a86aae3 (unchanged, same as `build/behind-the-playlist-lualatex.pdf`)
- Automated pass: `.venv/bin/python tools/qa/qa_lib.py --pdf build/behind-the-playlist-candidate.pdf --log build/candidate/main.log --checks all --out docs/qa/round-01/recheck` → `findings.json`, `pages/page-01..20.png`
- Negative tests of the new `check_bib` were run on in-memory modified copies of the candidate (scratch script outside the project; no project file written).

## Result in one line

qa-super `--checks all`: **55 pass, 1 fail, 1 n/a**, the same as D1. The single fail is still `qa-infra-56` (stale source ZIP, D1-01, packaging). Both Fixer changes (D1-02, D1-03) are **verified fixed**. No new defect was found.

## Page count and page-19 footer regression

- **Page count:** 20 (`qa-typeset-02` pass). The approved PDF also has 20.
- **Page-19 footer regression: PASS.** `qa-footer-50`: p.19 shows `20` left and `19` right, bar not mirrored. Confirmed visually on `pages/page-19.png`. Dot x positions pp.2–20 are strictly decreasing (…, 138, 119, 99), identical to D1.

## Per finding

| ID | Kind | Status | Evidence |
|---|---|---|---|
| D1-01 (qa-infra-56) | packaging | **still open (flagged for the users)** | Recheck still reports "ZIP PDF matches submission PDF: False; ZIP contains .cls: False". The ZIP is outside the Fixer's remit. Note: if the users adopt the candidate, the rebuilt ZIP must carry class v1.1 and the new PDF. |
| D1-02 | skill | **verified fixed** | See "D1-02 verification" below. |
| D1-03 | template | **verified fixed** | See "D1-03 verification" below. |
| D1-04 | content (figure) | **still open (flagged for the users)** | p.14 is byte-identical in extracted text and pixel-identical in rendering to the approved PDF, so the label spacing in Fig. 6.1 is unchanged. Cosmetic, not blocking. |

### D1-02 verification (code read, not taken from the Fixer's claim)

`tools/qa/qa_lib.py` l.190–204, `check_bib`:
- The heading is now a text line whose stripped text equals exactly `מקורות` **and** whose largest span is >= 16 pt. Pass requires `heads == [want]` with `want = EXP["chapter_starts"]["מקורות"]` (19), so the heading must be on exactly one page and that page must be 19. A missing, duplicated or moved heading fails.
- Line sizes found in the candidate: p.19 heading 23.2 pt (counted); p.20 running header 8.7 pt (excluded); p.3 TOC line `מקורות19` (not an exact match, 10.5 pt, excluded); body mentions on pp.11, 14, 15 (not exact, 10.5 pt, excluded). Only p.19 qualifies.
- Evidence string now reads "heading 'מקורות' on p.19; 18 entries; min x0=70.9" (correct page; D1 said p.20).

My own negative tests (modified in-memory copies of the candidate):

| Test | New check | Old D1 logic |
|---|---|---|
| Candidate as built | pass, p.19 | (reported p.20) |
| p.19 deleted | **fail** (heading p.[], 7 entries) | n/a |
| p.19 heading redacted, running header on p.20 kept | **fail** (heading p.[]) | would pass: still finds p.20 running header |
| p.18 deleted, so the heading moves to p.18 | **fail** (heading p.18) | would pass |
| Extra 20 pt `מקורות` inserted on p.18 | pass (inconclusive) | n/a |

The last test is inconclusive, not a defect: text inserted with PyMuPDF is stored in visual order, so it does not extract as `מקורות` and the check never saw a second heading. By the code (`heads == [want]`), a real second heading would fail. Conclusion: the check genuinely detects the p.19 heading and fails without it. `expectations.json` was not weakened.

### D1-03 verification (rendered pp.19–20)

- `pages/page-20.png`: entry [13] now reads "… [Online]. Available:" / `https://developers.google.com/machine-` / `learning/recommendation/overview/types`. The approved PDF had `https:` / `//developers…`.
- Extracted text: the candidate has 0 lines ending in `https:` and 0 lines starting with `//` on pp.19–20 (approved p.20: 1 and 1).
- All URLs on pp.19–20 ([1], [3], [4], [9], [11], [13]) have `https://` unbroken. The remaining breaks are after `machine-` ([9], [13]) and after `paper_files/` ([11]), both accepted in D1.
- Link URIs on pp.19 and 20 are identical to the approved PDF.
- Layout: p.20 text spans x0 70.9 to x1 522.7 (inside the margins). The bottom of the text moved from y 511.7 to 528.3 (one extra line in [13]) and the lower page stays clear. Entries [1]–[11] are on p.19 and [12]–[18] on p.20, as before. p.19 is identical to the approved PDF. The log has 0 overfull boxes, and qa-typeset reports 0 errors.
- No new layout problem was found on either page. The running header ("מקורות" / "מאחורי הפלייליסט") and the footer are correct.
- Class version: `\ProvidesClass` v1.1, CHANGELOG v1.1, log v1.1 (`qa-cls-version-57` pass).

## Candidate vs. approved PDF

| Comparison | Pages that differ |
|---|---|
| Extracted text, per page (pp.1–20) | **p.20 only** |
| Rendered pixels at 72 dpi, per page | **p.20 only** |

This matches the expected scope of D1-03: only [13] on p.20 changes. Pages 1–19 are unchanged.

## Passes per family (candidate)

| Family | Pass | Fail | n/a | Notes |
|---|---|---|---|---|
| qa-typeset | 5 | 0 | 0 | 0 errors/glyphs/overfull/undefined; 20 pages; 10 chapter starts; heading on p.19 (stricter check), 18 entries, min x0 = 70.9; 0 biber warnings |
| qa-bidi | 35 | 0 | 0 | unchanged from D1 |
| qa-table | 3 | 0 | 0 | unchanged |
| qa-img | 4 | 0 | 0 | unchanged |
| qa-code | 0 | 0 | 1 | n/a, the book has no code boxes |
| qa-footer | 3 | 0 | 0 | p.19 regression pass |
| qa-infra | 4 | 1 | 0 | ZIP freshness fail (D1-01, packaging) |
| qa-cls-version | 1 | 0 | 0 | v1.1 / v1.1 / v1.1 |
| **Total** | **55** | **1** | **1** | |

## New findings

None. No new actionable defects were found in the candidate.

## Verdict

**Candidate acceptable.** Both Fixer changes are verified, and only p.20 differs from the approved PDF, as expected. The one remaining fail (D1-01) and D1-04 are flagged for the users and do not depend on the candidate. Adopting the candidate as the submission is the users' decision. It would need a new approval, the new SHA in the docs, and a rebuilt source ZIP with class v1.1.
