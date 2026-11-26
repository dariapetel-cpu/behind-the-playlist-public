> Author: Detector agent · 2026-11-25 · PDF: pdf/behind-the-playlist.pdf (SHA-256 first 12 hex: 7ab8276ae14f)

# D4 Detector report: QA-harness failures before any fix

**Setup.** All mutations ran on a `git clone` (commit 12efa82, branch roni-qa-improvements) in a scratch directory. Python 3.12.2, PyMuPDF 1.28.2, PYTHONUTF8=1, PYTHONDONTWRITEBYTECODE=1, Windows. Public edition.

**Stub log.** The repo has no build log, and no TeX build was run. Every run uses a two-line stub log (a marker line and `Document Class: behind-the-playlist 2026/11/18 v1.1 ...`) and a stub `.blg` containing `INFO - stub`, except where a row changes them. A pass in a log-based check therefore says nothing about the real build. Fake IDs only.

**Baseline** (unmutated): 55 pass, 0 fail, 2 n/a, exit 0. Per family: typeset 5, bidi 35, table 3, img 4, footer 3, infra 4 (+1 n/a), cls-version 1, code 0 (1 n/a).

**Page-19 footer regression:** PASS on the real PDF (automated; also seen in the rendered page: 20 left, 19 right). Control: wiping the p.19 footer text gives 2 fails, so the check detects a footer missing from the text layer. See D4-N3 for what it misses.

Totals are written pass/fail/n-a. "Control" rows show that the check can fail.

## Claims

### H1 visual blindness: REPRODUCED (Fig. 6.1 depends on the rectangle)

Rectangles are opaque, drawn on top (points: x0,y0,x1,y1); `--checks all`.

| Mutation | Totals | Exit |
|---|---|---|
| cover (40,40,555,800), black; and, separately, white | 55/0/2 both | 0 |
| Fig. 2.1 p.7 (75,80,521,276), black; white | 55/0/2 both | 0 |
| p.9 formulas (85,220,330,232)+(85,262,507,354), black; white | 55/0/2 both | 0 |
| Table 4.1 p.11 (71,192,524,326), black; white | 55/0/2 both | 0 |
| p.12 prose (71,300,524,745), black; white | 55/0/2 both | 0 |
| Fig. 6.1 p.14, within the text block (71,425,524,588), black | 55/0/2 | 0 |
| Fig. 6.1 p.14, including the label at its right (71,425,529,588), white | 55/0/2 | 0 |
| same wider rectangle, black | 54/1/2 (side-margin ink, not the figure) | 0 |
| p.12 text layer (60,300,535,745) redacted: 2266 -> 507 characters | 55/0/2 | 0 |

### H2 silent skips: REPRODUCED (Fig. 6.1 only under a wider mutation)

| Mutation | Totals | Exit | Effect |
|---|---|---|---|
| p.9 data table text redacted (345,166,510,235) | 54/0/2 | 0 | check "p.9 data table" vanishes |
| only its header row redacted (345,166,510,183) | 54/0/2 | 0 | same |
| `.blg` absent | 54/0/2 | 0 | biber check vanishes |
| control: `.blg` containing WARN | 54/1/2 | 0 | fails as expected |
| Fig. 6.1 labels redacted on p.14 only, `img` | 3/1/0 | 0 | not skipped: fails, but blamed on p.15 (D4-N5) |
| same plus the two search words redacted on p.15, `img` | 3/0/0 | 0 | Fig. 6.1 block check vanishes |
| same, `all` | 52/2/2 | 0 | block check vanishes; two bidi checks fail |

### H3 exit codes and logs: REPRODUCED

- `qa_lib.py`: every completed run with failures (up to 3) exited 0. Nonzero exits came only from crashes.
- `check_pdf.py`: empty log exit 0 PASS; `./chapters/05-hasha.tex:12: error: Undefined control sequence.` together with `./main.tex:30: Undefined control sequence.` exit 0, errors=0; `Overfull \vbox (50.0pt too high)` exit 0, overfull=0.
- Controls: `! ...` exit 1; `Overfull \hbox (50.0pt` exit 1; undefined reference on one line exit 1.
- Empty log, `qa_lib.py --checks all`: 54/1/2, exit 0. The only fail is cls-version.

### M3 ID scan: REPRODUCED

| Mutation (`infra`) | Totals | Exit |
|---|---|---|
| fake ID in `docs/leak.txt`; `main.tex` unchanged (it has no `\studentid`) | 4/0/1 | 0 |
| control: same ID also as `\studentid{..}` in a `main.tex` comment | 3/1/1 (docs\leak.txt) | 0 |
| ID declared in `main.tex`; copies only in `.git/` and `.venv/` | 3/1/1 (.git\leak.txt, .venv\leak.txt) | 0 |

The last row shows that on Windows neither `.git` nor `.venv` is excluded.

### M4 iron law: REPRODUCED

Each appended alone to `book/chapters/05-hasha.tex`, `infra`: `\vspace{2cm}`, `\resizebox`, `\newpage`, `wrapfigure`: 4/0/1 each, exit 0. All four together, `all`: 55/0/2, exit 0. Control: `\begin{minipage}` 3/1/1.

### M5 qa-code: REPRODUCED

`lstlisting`, `verbatim`, `pythonbox` appended to chapter 5, `code`: each 0/0/1, exit 0, evidence still "the book contains no code boxes".

### L3 PDF outside the project: PARTLY

Absolute outside path: REPRODUCED. All checks run, then ValueError ("is not in the subpath"), exit 1, no summary and no `findings.json`. A relative outside path (`../outside.pdf`, `code`) does not crash, exit 0.

### M2 Skill frontmatter: REPRODUCED

PyYAML `safe_load` fails ("mapping values are not allowed here") on exactly eight: qa-bidi, qa-cls-version, qa-code, qa-footer, qa-img, qa-infra, qa-table, qa-typeset. qa-super, the five role Skills and the five agent files parse. In this session Claude Code still listed these eight, but with the bare name as the description.

## New findings (all executed; `--checks all` unless stated)

Every `qa_lib.py` run below exited 0 unless the row says it crashed.

| ID | Check | Page/file | Evidence | Expected | Severity | Kind | Actionable by |
|---|---|---|---|---|---|---|---|
| D4-N1 | all | PDF | full-page white rectangle on every page: 55/0/2 | fail | blocker | skill | Fixer |
| D4-N2 | all | pp. 2, 3, 5, 13, 17, 18 | body redacted and whited out, one page at a time: 55/0/2 each (p.15: 52/3/2; p.19: 54/1/2) | fail | blocker | skill | Fixer |
| D4-N3 | qa-footer | p.19 | white box over the p.19 footer: 55/0/2. PDF cut to 1 page, `footer`: 3/0/0, "page 19 footer correct". Cut to 10 pages, `footer`: 2/1/0, with p.19 and dot checks passing | fail when the page is absent or hidden | blocker | skill | Fixer |
| D4-N4 | qa-img, qa-bidi | p.7 | all Fig. 2.1 text redacted (789 -> 592 characters): 55/0/2; the phrases are found in prose elsewhere | fail | major | skill | Fixer |
| D4-N5 | qa-img, qa-bidi | wrong page | the baseline reports "Fig. 2.1 p.6" (the figure is on p.7). Four diagram phrases are matched only outside Fig. 6.1 (p.15, one also p.18). With p.14 labels wiped, the figure fail is blamed on p.15 | evidence from the figure itself | major | skill | Fixer |
| D4-N6 | all | pp. 9, 11, 12 | p.12 rotated 180 degrees; wrong image over p.9 formulas; black annotation over Table 4.1; 20pt text over p.12 prose: 55/0/2 each | fail | major | skill | Fixer |
| D4-N7 | check_pdf | log | exit 0 for: unrelated text as log; "Fatal error occurred, no output PDF file produced"; "Rerun to get cross-references right"; an undefined reference wrapped at 79 columns; an unrelated one-page PDF | fail, or evidence that log and PDF belong together | major | skill | Fixer |
| D4-N8 | qa-typeset | findings.json | on a white-text fail, the evidence is only "errors=0 missing_chars=0 ...": the reason is lost | reason shown | minor | skill | Fixer |
| D4-N9 | qa-typeset | log name | log named `main.txt`, no `.blg`: the log is read as the biber log, "main.txt: 0 biber warnings/errors", 55/0/2 | not a biber pass | major | skill | Fixer |
| D4-N10 | all | findings.json | good run, then a crashing run (log absent) on a different PDF, same `--out`: the old all-pass `findings.json` is left byte-identical | no stale result | major | skill | Fixer |
| D4-N11 | qa-typeset | p.1, CLI | 9-digit ID on cover: crash (CalledProcessError), exit 1, no findings.json, so the cover check never reports (`--checks bidi`: 34/1/0). `--edition submission` on the public PDF crashes the same way; `--checks typest` raises KeyError | reported as a fail or a clear usage error | major | skill | Fixer |
| D4-N12 | qa-bidi, qa-infra | PDF | 55/0/2 for each of: ID hyphenated on cover; ID on p.5; ID in PDF metadata; ID as raster image on cover; ISO date on cover. Control: spaced ID on cover is caught (54/1/2) | fail | blocker | skill | Fixer |
| D4-N13 | qa-infra | text files | ID declared in main.tex, but leak spaced, UTF-16 or in a filename: 4/0/1 each. `\studentid {..}` (with a space) does not produce a fail: 4/0/1 | fail or declared ID recognised | major | skill | Fixer |
| D4-N14 | qa-infra | book/ | chapters 00 and 02-08 deleted, `infra`: 4/0/1. `references.bib` emptied: 55/0/2. Class body removed, version lines kept, `cls-version,infra`: 5/0/1 | fail | major | skill | Fixer |
| D4-N15 | qa-infra | README.md | README emptied: 4/0/1. Broken `<img src>` and reference-style link: 4/0/1. Control: broken inline link fails (3/1/1) | fail | minor | skill | Fixer |
| D4-N16 | qa-infra | chapters | these also pass (4/0/1 each): `\hspace*`, `\setlength`, `figure[H]`, `figure[ht!]`, `\begin {minipage}`, `\includegraphics[width=..]`, `tikzpicture`. False alarm: `\begin{minipage}` inside a comment fails (3/1/1) | consistent iron law; which commands count is for the users | minor | skill | Fixer |
| D4-N17 | qa-img | margins | black ink at y 757-779 and at y 10-70, and pale ink (0.85,0.9,0.9) at y 300-330: 55/0/2 each. Control: black at y 300-330 fails (54/1/2) | fail | minor | skill | Fixer |
| D4-N18 | check_pdf | p.12 | near-white text (0.99), `typeset`: 5/0/0. Control: pure white 4/1/0 | fail | minor | skill | Fixer |

**Red-team look at the real PDF.** Contact sheets of all 20 unmutated pages (75 dpi): no reversed or garbled text, clipping, overlap or footer error seen at that resolution. **No actionable defects found in the book itself.**

## Not verified

- The real build log and `.blg`, and whether any log-based check passes on the real build.
- The submission edition (its PDF, ZIP and real cover are not in the public repo); ZIP freshness was not tested.
- POSIX behaviour of the `/.git` exclusion; everything ran on Windows.
- Table column swaps, reversed Hebrew glyph order and font substitution: not executed.
- Chapter claims against research-notes.md: not re-read (the target is the harness).
- Fine typographic inspection at high resolution.
- Whether Claude Code drops the broken frontmatter descriptions in every version.
- Whether the mutated sources would compile (no TeX build allowed).
