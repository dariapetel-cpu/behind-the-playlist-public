> Author: Detector agent · 2026-11-18 · PDF: submission/behind-the-playlist.pdf (SHA-256 43608a86aae3)

# Detector report, red-team QA round 1 (Task D1)

**Inputs**
- PDF: `submission/behind-the-playlist.pdf`, 20 pages. Identical to `build/lualatex/main.pdf` (same SHA-256).
- Log: `build/lualatex/main.log`, `build/lualatex/main.blg`
- Automated pass: `.venv/bin/python tools/qa/qa_lib.py --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log --checks all --out docs/qa/round-01/detect` → `findings.json`, `pages/page-01..20.png`
- Red-team pass: all 20 rendered pages viewed, with zoomed crops of p.4, p.10 (time-stamp bidi) and p.14 (feedback-loop label). Chapter sources were read against `docs/agents/research-notes.md`.

## Result in one line

qa-super: **55 pass, 1 fail, 1 n/a**. The single fail is a **packaging** finding (stale source ZIP). The red-team pass adds one **minor skill** defect (misleading evidence in the bibliography check) and two **low/cosmetic** observations. No content claim contradicts the research notes.

## Page-19 footer regression check

**PASS.** `qa-footer-50`: p.19 shows `20` on the left and `19` on the right, and the bar is not mirrored. I confirmed this visually on `pages/page-19.png`. The pink dot sits near the left end (x=119 pt), between p.18 (x=138) and p.20 (x=99).

## Findings (every fail plus every red-team finding)

| ID | Check | Page/file | Evidence | Expected | Severity | Kind | Actionable by |
|---|---|---|---|---|---|---|---|
| D1-01 (= qa-infra-56) | qa-infra: source ZIP freshness | `submission/project-source.zip` | The ZIP is dated 2026-11-14 (17:26–17:29). Its `submission/behind-the-playlist.pdf` is 256,033 bytes, while the approved PDF is 267,398 bytes, so "ZIP PDF matches submission PDF: False". It contains no `.cls` file, so "ZIP contains .cls: False". | The source package contains the approved PDF (SHA 43608a86aae3) and the current sources, including `book/behind-the-playlist.cls`. | major | packaging | flag for the users |
| D1-02 | Red team: qa-typeset bibliography check (`check_bib`) | `tools/qa/qa_lib.py` l.191–198; findings `qa-typeset-04` | The evidence says "heading 'מקורות' on p.20". The heading is actually on **p.19** (TOC, `expectations.json` `chapter_starts.מקורות = 19`, `page-19.png`). The check picks the *last* page whose first 30 characters contain "מקורות". On p.20 that text is the running header (`'מאחורי הפלייליסט\nמקורות\n[12]…'`). It never compares the page with `chapter_starts`, so a missing or moved heading would still pass as long as a running header said "מקורות". | The check locates the real bibliography heading (the first page, or a non-header line) and asserts it is on the expected page, 19. | minor | skill | Fixer |
| D1-03 | Red team: bibliography URL break | p.20, entry [13] | The URL breaks right after the scheme: `https:` ends one line and `//developers.google.com/…` starts the next. ([9] on p.19 breaks after `machine-`, which is acceptable.) The cause is the class setting `biburl*penalty = 0`, which allows breaks at any `/`. | URL breaks that do not split `https://` from the host. This is cosmetic only: the entry stays inside the margins (min x0 = 70.9). | low (cosmetic) | template | Fixer (optional) |
| D1-04 | Red team: Fig. 6.1 label placement | p.14, `book/figures/pipeline.tex` l.41 | The rotated label "לולאת משוב" sits right against the pink dashed loop line between blocks 8 and 1. In the 3× crop the glyphs almost touch the dashes. The label is legible and inside the text block, and qa-img passes. | A small gap between the label and the dashed line. | low (cosmetic) | content (figure file under `book/`) | flag for the users |

No other defects were found. Severity of D1-03 and D1-04 is cosmetic. They are listed so that nothing seen is left unreported. Neither needs to block submission.

## Red-team review by focus area (no defect found unless listed above)

- **Cover (p.1):** title, subtitle, waveform, tagline and metadata block are all RTL and correctly ordered. The two student-ID cells appear masked as "ID hidden" in the rendered PNGs. No ID number is reproduced in this report.
- **p.7 (Fig. 2.1 graph):** the legend, axis titles, Hebrew bar labels (אוטובוס, חדר כושר, לימודים) and the "נתונים בדיוניים" tag are all inside the plot frame. I cross-checked the data against the p.6 text: 344 songs in total, 99 skipped (28.8%); bus 07–09: 34 of 82 skipped (41%); gym 17–19: 11 of 57 (19%); studies 22–24: 5 of 45 (11%). All bar heights add up to these figures.
- **pp. 8–9 (cosine formula and lab box):** the formula renders correctly, and the box breaks cleanly across pages. All the arithmetic checks out: n·y = 26, ‖y‖ = 5, √30 ≈ 5.48, cos ≈ 0.95; n·m = 10, ‖m‖ ≈ 5.10, √780 ≈ 27.93, cos ≈ 0.36. The data table's values match the vectors, and its first column (מאזין/ה) is on the right.
- **p.11 (Table 4.1):** RTL column order, flush-right cells and the "דוגמה לימודית" tag are correct. A style note, not a defect: rows have no separators, so wrapped cells such as "ממליץ רק על מה שדומה למה / שכבר אהבת" depend on vertical alignment alone. It is still readable.
- **p.14 (Fig. 6.1 diagram):** all 8 blocks are present, and every label is inside its block. Numbering, arrows and the legend (נתונים / מודל / משתמש) are consistent with the text on pp.14–15. The only note is D1-04.
- **pp. 18–20 (footer and bibliography):** the footer is correct on all three pages (left `20`, right = page number). The bibliography heading is on p.19 as in the TOC. 18 numbered entries [1]–[18], all inside the margins. The running header on p.20 reads "מקורות". The only note is D1-03.
- **Bidi spot checks:** I zoomed in on the time stamps at the start of RTL lines: "07:30." (p.4), "יום רביעי, 08:10." (p.10), "18:00," (p.12) and "21:00." (p.14). All have the digits intact and the punctuation on the correct (left) side. Mixed Latin terms in parentheses read correctly, including the line-broken "(implicit / feedback)" on p.6.
- **Consistency:** chapter openings (pp. 4, 6, 8, 10, 12, 14, 16, 18) share one layout (רצועה NN, waveform, title, rule, סצנה box with בדיוני tag). Callout styles (רגע, זה אמיתי? / בקצרה / מעבדה) are consistent. Pages 2–20 have no visible ink in the side margins.

### Content vs. research notes (flagged, never judged final)
I checked every cited claim on pp.2–18 against `docs/agents/research-notes.md`. **No contradiction found.** The text respects every listed gap: no skip percentage from Brost et al. (p.7 says so explicitly); Tapestry is cited only for the year and name; no "spectrograms"; time of day is explicitly not attributed to Spotify (p.13); Schwartz is presented as an argument; the eight-station pipeline is presented as the book's own simplification (p.14). Spotify-authored papers are attributed as research, not as the production algorithm.

## Passes per family (automated)

| Family | Pass | Fail | n/a | Notes |
|---|---|---|---|---|
| qa-typeset | 5 | 0 | 0 | 0 errors / missing glyphs / overfull / undefined refs; 20 pages; all 10 chapter starts match; 18 bib entries inside the margins; 0 biber warnings. (The p.20 heading evidence is wrong, see D1-02.) |
| qa-bidi | 35 | 0 | 0 | All diagram, graph, table, mixed-direction and cover phrases read RTL from glyph positions; multi-number citations ascending. |
| qa-table | 3 | 0 | 0 | Table 4.1 RTL column order and flush-right edges; Ch. 3 data table first column on the right. |
| qa-img | 4 | 0 | 0 | 8/8 diagram labels inside their blocks; Fig. 2.1 and 6.1 captioned and tagged; no ink in side margins. |
| qa-code | 0 | 0 | 1 | n/a: the book has no code boxes. |
| qa-footer | 3 | 0 | 0 | Totals/page numbers on pp.2–20; **p.19 regression pass**; dot moves strictly right-to-left. |
| qa-infra | 4 | 1 | 0 | Required files, iron law, 40 README links, ID-leak scan pass; **ZIP freshness fail (D1-01)**. |
| qa-cls-version | 1 | 0 | 0 | v1.0 in `\ProvidesClass`, CHANGELOG and the build log. |
| **Total** | **55** | **1** | **1** | |

## Actionable summary

- **For the Fixer (template/skill):** D1-02 (minor, skill: the bibliography heading-page check). D1-03 is optional (cosmetic, template: the URL break after `https:`). No template defect affects the approved PDF's correctness.
- **Flag for the users:** D1-01 (major, packaging): rebuild `submission/project-source.zip` so that it holds the approved PDF and the `.cls`. D1-04 (cosmetic, content figure).
- **Page-19 footer regression:** pass.
