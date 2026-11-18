> Author: Detector agent · 2026-11-18 · PDF: build/behind-the-playlist-candidate.pdf (SHA-256 ed844348feb6)

# Recheck report 2, red-team QA round 1 (Task D3, recheck mode)

**Inputs**
- Candidate: `build/behind-the-playlist-candidate.pdf` (SHA-256 ed844348feb6), log `build/candidate/main.log`
- Approved PDF for comparison (read only, not modified): `submission/behind-the-playlist.pdf`, SHA-256 43608a86aae3 (unchanged)
- Earlier reports: `docs/qa/round-01/detect/detector-report.md` (D1), `docs/qa/round-01/recheck/recheck-report.md` (D2)
- Change under test: `book/figures/pipeline.tex`, where the label „לולאת משוב" moved from x = 15.7 cm to 15.894 cm (+5.5 pt) as an overlay, with a `\phantom` copy left at the old position (Prompt 24, the users' decision on D1-04)
- Automated pass: `.venv/bin/python tools/qa/qa_lib.py --pdf build/behind-the-playlist-candidate.pdf --log build/candidate/main.log --checks all --out docs/qa/round-01/recheck-2` produced `findings.json` and `pages/page-01..20.png`
- Measurements: PyMuPDF (glyph `rawdict`, `get_drawings`, pixel renders at 144, 288 and 1200 dpi), using scratch scripts outside the project
- Evidence crops in this directory: `p14-label-cand-1200dpi.png`, `p14-label-appr-1200dpi.png`, `p14-context-cand.png`, `p14-context-appr.png`

## Result in one line

qa-super `--checks all`: **55 pass, 1 fail, 1 n/a**, the same as D1 and D2. The single fail is still `qa-infra-56` (stale source ZIP, D1-01, packaging). The label change on p.14 does what was asked: the gap is about 2 mm, the label is legible, the blocks have not moved, and only the label's pixels changed.

## 1. qa-super (candidate)

| Family | Pass | Fail | n/a | Notes |
|---|---|---|---|---|
| qa-typeset | 5 | 0 | 0 | 20 pages; 0 errors, missing glyphs, overfull boxes or undefined refs/cites; 10 chapter starts correct; heading 'מקורות' on p.19 only, 18 entries, min x0 = 70.9; 0 biber warnings |
| qa-bidi | 35 | 0 | 0 | includes 'לולאת משוב' (qa-bidi-14, but see note D3-01) and ascending citations |
| qa-table | 3 | 0 | 0 | unchanged |
| qa-img | 4 | 0 | 0 | 8 blocks with labels inside; captions and tags; no ink in the side margins |
| qa-code | 0 | 0 | 1 | n/a, the book has no code boxes |
| qa-footer | 3 | 0 | 0 | p.19 regression pass |
| qa-infra | 4 | 1 | 0 | ZIP freshness fail (D1-01, packaging) |
| qa-cls-version | 1 | 0 | 0 | v1.1 / v1.1 / v1.1 |
| **Total** | **55** | **1** | **1** | |

**Page-19 footer regression: PASS.** `qa-footer-50`: p.19 shows `20` on the left and `19` on the right, and the bar is not mirrored. I confirmed this visually on `pages/page-19.png`. The dot x positions on pp.2–20 decrease strictly (451 … 119, 99), the same as D1 and D2.

## 2. Is the label readable? (p.14, 1200 dpi)

`p14-label-cand-1200dpi.png` and `p14-context-cand.png`: the label „לולאת משוב" is rotated 90° and reads bottom-to-top in the correct letter order (ל-ו-ל-א-ת, then מ-ש-ו-ב). It is complete, with no clipped glyphs. It does not overlap the dashed line, the arrowhead into block 1, the badge "8" or any block. It is charcoal on the page background, in the same font and size as before (Heebo 8.7 pt). Extracted text on p.14 is `'לולאת משוב'` with direction (0, −1), so the logical order is correct too.

## 3. Gap to the dashed line

| Quantity | Candidate | Approved |
|---|---|---|
| Vertical dashed segment, path x (centre of stroke, `get_drawings`) | 513.25 pt | 513.25 pt |
| Dashed stroke width | 1.295 pt | 1.295 pt |
| Dashed line ink, right edge (1200 dpi) | 513.90 pt | 513.90 pt |
| Label glyph box, left edge (`rawdict`) | 518.93 pt | 513.43 pt |
| Label ink, left edge (1200 dpi) | 519.18 pt | 513.72 pt |
| **Gap, ink to ink** | **5.28 pt = 1.86 mm** | 0 pt (touching or overlapping by about 0.2 pt) |
| Gap, line centre to label ink | 5.93 pt = 2.09 mm | 0.47 pt |
| Gap, line edge to label glyph box | 5.03 pt = 1.77 mm | |

The shift is exactly +5.50 pt (518.93 − 513.43). The ink-to-ink gap is about 1.9 mm, which is "about 2 mm" as requested. D1-04 is resolved.

## 4. All eight blocks in place

- p.14 has 63 vector drawings in each PDF, and the full lists (type, rect, colours, dashes, width, item count) are **identical** between the candidate and the approved PDF.
- The 8 block rectangles have the same coordinates in both PDFs. Top row y 434.765–475.867, x 412.124–499.999 / 298.736–386.612 / 185.349–273.225 / 71.962–159.837. Bottom row y 512.718–553.821, same x columns.
- The pink dashed loop (500.497, 455.316, 513.253, 533.270) is identical in both PDFs.
- At 288 dpi, the pixel difference on p.14 is limited to the box x 513.5–526.0, y 472.25–516.25, which is the label's old and new position only. The `\phantom` copy works as intended: the picture's bounding box did not change, and nothing else moved.

## 5. Margin: how far the label extends past the text block (x = 524.4 pt)

| Measure | Right edge | Past 524.4 pt |
|---|---|---|
| Label ink (1200 dpi) | 525.84 pt | **1.44 pt = 0.51 mm** |
| Label glyph box (`rawdict`) | 527.63 pt | **3.23 pt = 1.14 mm** |

In the approved PDF the label stayed inside (ink 520.32 pt, box 522.13 pt). `qa-img-47` still passes because it allows 4 pt past the text block edge at 36 dpi (ink would have to pass 528.4 pt). The label is about 2.6 pt inside that limit. The figure is an `overlay` node, so no overfull box is logged (0 overfull). Nothing else on p.14 extends past 524.4 pt. This is visible only on close inspection, but it is a real 0.5 mm overhang into the right margin.

## 6. Differences from the approved PDF

| Comparison | Pages that differ |
|---|---|
| Extracted text (plain), per page, pp.1–20 | **p.20 only** (class v1.1, D1-03 fix to entry [13]) |
| Rendered pixels at 144 dpi, per page | **p.14 and p.20** |
| Word positions on p.14 | only the two label words: x 513.43→518.93 (`לולאת` y 472.17–494.67, `משוב` y 496.83–516.40) |

The plain text of p.14 is unchanged, so the text-only diff shows just p.20, as expected. p.14 differs only in the pixels and word coordinates of the label, which is the intended change.

## Per finding (compared with D1/D2)

| ID | Kind | Status |
|---|---|---|
| D1-01 (qa-infra-56) | packaging | **still open (flag for the users).** If the candidate is adopted, the rebuilt ZIP must carry class v1.1, the new `pipeline.tex` and the new PDF. |
| D1-02 | skill | verified fixed in D2; still passes |
| D1-03 | template | verified fixed in D2; p.20 still the only text difference |
| D1-04 | content (figure) | **resolved**: gap 1.86 mm ink-to-ink (2.09 mm from the line's centre) |

## New findings (red team)

| ID | Check | Page/file | Evidence | Expected | Severity | Kind | Actionable by |
|---|---|---|---|---|---|---|---|
| D3-01 | qa-bidi coverage of the figure label | `tools/qa` qa-bidi-14; p.14 | qa-bidi-14 passes on **p.15** (body text), not on p.14. It never matches the rotated figure label, in D1, D2 or D3. I verified the label manually (section 2). | a bidi check of 'לולאת משוב' that covers the rotated label inside Fig. 6.1 | low (coverage gap, not a defect in the book) | skill | Fixer (optional) |
| D3-02 | Label vs. text block edge | p.14, `book/figures/pipeline.tex` l.49 | the label's ink ends at 525.84 pt, 1.44 pt (0.51 mm) past x = 524.4 (glyph box 3.23 pt); inside the 4 pt tolerance of qa-img-47 | inside the text block, or accepted by the users as a known overhang | low (cosmetic, informational) | content (figure file under `book/`) | flag for the users |

The red-team pass found no other problems on p.14 (Hebrew order, arrows, badges, legend, caption and tag all correct) or p.19 (heading, entries [1]–[11], footer).

**No actionable template or skill defects were found.** D3-01 is an optional improvement to the checks. D3-02 is a measurement that the users asked for, flagged for their decision.

## Verdict

**Candidate acceptable.** The label change gives the requested gap of about 2 mm. The label is legible and correct. All eight blocks and the dashed line have the same coordinates as in the approved PDF, and only the label pixels on p.14 and the expected p.20 change differ. The 0.5 mm overhang past the text block (D3-02) is within the margin tolerance and is for the users to accept or not. Adopting the candidate is the users' decision. It would need a new approval, the new SHA in the docs, and a rebuilt source ZIP (D1-01).
